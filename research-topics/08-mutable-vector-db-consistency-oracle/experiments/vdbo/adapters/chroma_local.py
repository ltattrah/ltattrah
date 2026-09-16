"""Chroma with ``PersistentClient``: SQLite metadata store plus an HNSW index, in-process."""
from __future__ import annotations

import logging
from typing import Optional

import chromadb
import numpy as np

from ..model import Filter, Hit, Record
from .base import EngineAdapter

logging.getLogger("chromadb").setLevel(logging.ERROR)
COLLECTION = "vdbo"


class ChromaEngine(EngineAdapter):
    name = "chroma"
    has_flush = False
    has_restart = True
    advertised = {
        "insert_visibility": "immediate after add/upsert returns",
        "read_your_write": "expected",
        "version_replacement": "upsert replaces embedding and metadata",
        "delete_safety": "deleted ids are not returned",
        "filter_consistency": "where-filter evaluated on current metadata (pre-filter)",
        "durability": "persisted to path on write",
        "restart_recovery": "collection reloads from path; HNSW index persisted",
    }

    sync_threshold: Optional[int] = None  # HNSW persistence interval (writes); None = Chroma default (1000)
    batch_size: Optional[int] = None

    def open(self) -> None:
        self.client = chromadb.PersistentClient(path=self.path)
        space = {"l2": "l2", "cosine": "cosine", "dot": "ip"}[self.metric]
        hnsw = {"space": space}
        if self.sync_threshold is not None:
            hnsw["sync_threshold"] = self.sync_threshold
        if self.batch_size is not None:
            hnsw["batch_size"] = self.batch_size
        try:
            self.col = self.client.get_or_create_collection(COLLECTION, configuration={"hnsw": hnsw})
        except Exception:  # noqa: BLE001 - older API: hnsw settings via metadata keys
            meta = {f"hnsw:{k}": v for k, v in hnsw.items()}
            self.col = self.client.get_or_create_collection(COLLECTION, metadata=meta)

    def close(self) -> None:
        # drop the cached system so the next open really reloads from disk
        try:
            from chromadb.api.client import SharedSystemClient
            SharedSystemClient.clear_system_cache()
        except Exception:  # noqa: BLE001
            pass
        self.client = None
        self.col = None

    def upsert(self, records: list[Record]) -> None:
        self.col.upsert(ids=[str(r.id) for r in records], embeddings=[r.vector.astype(float).tolist() for r in records], metadatas=[r.payload() for r in records])

    def delete(self, ids: list[int]) -> None:
        self.col.delete(ids=[str(i) for i in ids])

    @staticmethod
    def _where(filt: Filter) -> Optional[dict]:
        conds = []
        if filt.cat is not None:
            conds.append({"cat": {"$eq": filt.cat}})
        if filt.num_min is not None:
            conds.append({"num": {"$gte": filt.num_min}})
        if filt.num_max is not None:
            conds.append({"num": {"$lte": filt.num_max}})
        if not conds:
            return None
        return conds[0] if len(conds) == 1 else {"$and": conds}

    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]:
        n = self.col.count()
        if n == 0:
            return []
        res = self.col.query(query_embeddings=[vector.astype(float).tolist()], n_results=min(k, n), where=self._where(filt), include=["metadatas", "distances"])
        out = []
        for rid, meta, dist in zip(res["ids"][0], res["metadatas"][0], res["distances"][0]):
            meta = meta or {}
            out.append(Hit(id=int(rid), version=meta.get("_v"), distance=float(dist), metadata={k: v for k, v in meta.items() if k != "_v"}))
        return out

    def get(self, record_id: int) -> Optional[Hit]:
        res = self.col.get(ids=[str(record_id)], include=["metadatas"])
        if not res["ids"]:
            return None
        meta = res["metadatas"][0] or {}
        return Hit(id=record_id, version=meta.get("_v"), distance=None, metadata={k: v for k, v in meta.items() if k != "_v"})

    def count(self) -> Optional[int]:
        return int(self.col.count())

    def version_info(self) -> str:
        extra = f", sync_threshold={self.sync_threshold}, batch_size={self.batch_size}" if self.sync_threshold else ""
        return f"chromadb {chromadb.__version__} (PersistentClient, HNSW{extra})"

    @classmethod
    def small_sync(cls, **kw) -> "ChromaEngine":
        eng = cls(**kw)
        eng.sync_threshold, eng.batch_size = 20, 10
        eng.name = "chroma-smallsync"
        return eng
