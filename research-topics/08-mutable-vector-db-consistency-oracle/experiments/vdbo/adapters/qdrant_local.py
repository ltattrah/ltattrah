"""Qdrant in local (embedded) mode: ``QdrantClient(path=...)`` persists to disk without a server."""
from __future__ import annotations

from typing import Optional

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client import models as qm

from ..model import Filter, Hit, Record
from .base import EngineAdapter

COLLECTION = "vdbo"


class QdrantLocalEngine(EngineAdapter):
    name = "qdrant-local"
    has_flush = False  # local mode has no explicit sync point exposed to clients
    has_restart = True
    advertised = {
        "insert_visibility": "immediate on acknowledged upsert (local mode is synchronous)",
        "read_your_write": "expected",
        "version_replacement": "upsert on existing id replaces vector and payload",
        "delete_safety": "deleted points are not returned",
        "filter_consistency": "payload filters evaluated on current payload",
        "durability": "local mode persists to the given path",
        "restart_recovery": "collection reloads from path",
    }

    def open(self) -> None:
        self.client = QdrantClient(path=self.path)
        if not self.client.collection_exists(COLLECTION):
            dist = {"l2": qm.Distance.EUCLID, "cosine": qm.Distance.COSINE, "dot": qm.Distance.DOT}[self.metric]
            self.client.create_collection(COLLECTION, vectors_config=qm.VectorParams(size=self.dim, distance=dist))

    def close(self) -> None:
        self.client.close()

    def upsert(self, records: list[Record]) -> None:
        self.client.upsert(COLLECTION, points=[qm.PointStruct(id=r.id, vector=r.vector.astype(float).tolist(), payload=r.payload()) for r in records], wait=True)

    def delete(self, ids: list[int]) -> None:
        self.client.delete(COLLECTION, points_selector=qm.PointIdsList(points=ids), wait=True)

    @staticmethod
    def _filter(filt: Filter) -> Optional[qm.Filter]:
        must = []
        if filt.cat is not None:
            must.append(qm.FieldCondition(key="cat", match=qm.MatchValue(value=filt.cat)))
        if filt.num_min is not None or filt.num_max is not None:
            must.append(qm.FieldCondition(key="num", range=qm.Range(gte=filt.num_min, lte=filt.num_max)))
        return qm.Filter(must=must) if must else None

    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]:
        res = self.client.query_points(COLLECTION, query=vector.astype(float).tolist(), limit=k, query_filter=self._filter(filt), with_payload=True)
        return [Hit(id=int(p.id), version=p.payload.get("_v"), distance=float(p.score), metadata={k: v for k, v in p.payload.items() if k != "_v"}) for p in res.points]

    def get(self, record_id: int) -> Optional[Hit]:
        pts = self.client.retrieve(COLLECTION, ids=[record_id], with_payload=True)
        if not pts:
            return None
        p = pts[0]
        return Hit(id=int(p.id), version=p.payload.get("_v"), distance=None, metadata={k: v for k, v in p.payload.items() if k != "_v"})

    def count(self) -> Optional[int]:
        return int(self.client.count(COLLECTION, exact=True).count)

    def version_info(self) -> str:
        import importlib.metadata as im
        return f"qdrant-client {im.version('qdrant-client')} (local mode)"
