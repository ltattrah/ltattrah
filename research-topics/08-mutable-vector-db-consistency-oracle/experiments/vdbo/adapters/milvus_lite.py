"""Milvus Lite through ``MilvusClient(uri=<file>)``: the embedded build of Milvus core.

Milvus documents consistency *levels* (Strong, Bounded, Session, Eventually) and a ``flush`` that seals
growing segments. The adapter runs at ``Strong`` by default so every discrepancy is a contract question,
not a chosen weakening; ``MilvusLiteEngine.eventually`` runs the same history at ``Eventually``.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
from pymilvus import DataType, MilvusClient

from ..model import Filter, Hit, Record
from .base import EngineAdapter

COLLECTION = "vdbo"


class MilvusLiteEngine(EngineAdapter):
    name = "milvus-lite"
    has_flush = True
    has_restart = True
    consistency = "Strong"
    advertised = {
        "insert_visibility": "Strong: reads see all acknowledged writes; weaker levels documented",
        "read_your_write": "Session level or stronger",
        "version_replacement": "upsert = delete + insert on primary key",
        "delete_safety": "deleted PKs filtered at query time (bitset) until compaction",
        "filter_consistency": "scalar filter on current entity",
        "durability": "WAL + flush seals segments",
        "restart_recovery": "reload from local file",
    }

    def open(self) -> None:
        self.client = MilvusClient(uri=f"{self.path}/milvus.db")
        if not self.client.has_collection(COLLECTION):
            schema = self.client.create_schema(auto_id=False, enable_dynamic_field=False)
            schema.add_field("id", DataType.INT64, is_primary=True)
            schema.add_field("vector", DataType.FLOAT_VECTOR, dim=self.dim)
            schema.add_field("cat", DataType.VARCHAR, max_length=8)
            schema.add_field("num", DataType.INT64)
            schema.add_field("ver", DataType.INT64)
            idx = self.client.prepare_index_params()
            idx.add_index(field_name="vector", index_type="FLAT", metric_type={"l2": "L2", "cosine": "COSINE", "dot": "IP"}[self.metric])
            self.client.create_collection(COLLECTION, schema=schema, index_params=idx, consistency_level=self.consistency)
        self.client.load_collection(COLLECTION)

    def close(self) -> None:
        try:
            self.client.close()
        except Exception:  # noqa: BLE001
            pass

    @staticmethod
    def _row(r: Record) -> dict:
        return {"id": r.id, "vector": r.vector.astype(np.float32).tolist(), "cat": r.metadata["cat"], "num": int(r.metadata["num"]), "ver": r.version}

    def upsert(self, records: list[Record]) -> None:
        self.client.upsert(COLLECTION, data=[self._row(r) for r in records])

    def delete(self, ids: list[int]) -> None:
        self.client.delete(COLLECTION, ids=ids)

    @staticmethod
    def _expr(filt: Filter) -> str:
        parts = []
        if filt.cat is not None:
            parts.append(f"cat == '{filt.cat}'")
        if filt.num_min is not None:
            parts.append(f"num >= {filt.num_min}")
        if filt.num_max is not None:
            parts.append(f"num <= {filt.num_max}")
        return " and ".join(parts)

    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]:
        res = self.client.search(COLLECTION, data=[vector.astype(np.float32).tolist()], limit=k, filter=self._expr(filt),
                                 output_fields=["cat", "num", "ver"], consistency_level=self.consistency)
        out = []
        for h in res[0]:
            e = h["entity"]
            out.append(Hit(id=int(h["id"]), version=int(e["ver"]), distance=float(h["distance"]), metadata={"cat": e["cat"], "num": int(e["num"])}))
        return out

    def get(self, record_id: int) -> Optional[Hit]:
        rows = self.client.get(COLLECTION, ids=[record_id], output_fields=["cat", "num", "ver"])
        if not rows:
            return None
        r = rows[0]
        return Hit(id=int(r["id"]), version=int(r["ver"]), distance=None, metadata={"cat": r["cat"], "num": int(r["num"])})

    def count(self) -> Optional[int]:
        rows = self.client.query(COLLECTION, filter="", output_fields=["count(*)"], consistency_level=self.consistency)
        return int(rows[0]["count(*)"])

    def flush(self) -> None:
        try:
            self.client.flush(COLLECTION)
        except Exception:  # noqa: BLE001 - Lite may not expose flush; then it is not a sync point
            pass

    def rebuild(self) -> None:
        try:
            self.client.compact(COLLECTION)
        except Exception:  # noqa: BLE001
            pass

    def version_info(self) -> str:
        import importlib.metadata as im
        return f"pymilvus {im.version('pymilvus')} / milvus-lite {im.version('milvus-lite')} ({self.consistency}, FLAT)"

    @classmethod
    def eventually(cls, **kw) -> "MilvusLiteEngine":
        eng = cls(**kw)
        eng.consistency = "Eventually"
        eng.name = "milvus-lite-eventually"
        eng.advertised = {**cls.advertised, "insert_visibility": "Eventually: no visibility guarantee for recent writes", "read_your_write": "not guaranteed"}
        return eng
