"""Logical snapshot: the state a correct engine must reflect after each acknowledged operation.

The snapshot is engine-independent. It tracks live records with their current version, deleted ids
with the version they had and the *epoch* (restart count) in which they were deleted, and the write
position of every record so the oracle can tell a fresh write from an old one.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .model import Filter, Op, OpKind, Record


@dataclass
class WriteInfo:
    op_index: int  # position in the history of the write that produced the current version
    epoch: int  # restart epoch when written
    synced: bool  # whether a flush/rebuild/restart has happened since the write


@dataclass
class DeleteInfo:
    last_version: int
    op_index: int
    epoch: int
    synced: bool


@dataclass
class Snapshot:
    live: dict[int, Record] = field(default_factory=dict)
    writes: dict[int, WriteInfo] = field(default_factory=dict)
    deleted: dict[int, DeleteInfo] = field(default_factory=dict)
    ever_seen: set[int] = field(default_factory=set)
    epoch: int = 0  # incremented on every restart
    op_index: int = -1

    def apply(self, op: Op, op_index: int) -> None:
        self.op_index = op_index
        if op.kind in (OpKind.INSERT, OpKind.UPSERT):
            rec = op.record
            self.live[rec.id] = rec
            self.writes[rec.id] = WriteInfo(op_index, self.epoch, synced=False)
            self.deleted.pop(rec.id, None)
            self.ever_seen.add(rec.id)
        elif op.kind == OpKind.DELETE:
            rec = self.live.pop(op.id, None)
            self.writes.pop(op.id, None)
            if rec is not None:
                self.deleted[op.id] = DeleteInfo(rec.version, op_index, self.epoch, synced=False)
        elif op.kind in (OpKind.FLUSH, OpKind.REBUILD, OpKind.RESTART, OpKind.CRASH):
            # every acknowledged write is expected to be visible and durable from here on
            for w in self.writes.values():
                w.synced = True
            for d in self.deleted.values():
                d.synced = True
            if op.kind in (OpKind.RESTART, OpKind.CRASH):
                self.epoch += 1

    # ---- exact retrieval ----
    def candidates(self, filt: Filter) -> list[Record]:
        return [r for r in self.live.values() if filt.matches(r.metadata)]

    def exact_topk(self, query: np.ndarray, k: int, filt: Filter, metric: str = "l2") -> tuple[list[tuple[int, float]], float | None]:
        """Return the exact ranked list [(id, distance)] and the k-th distance (None if fewer than k)."""
        cands = self.candidates(filt)
        if not cands:
            return [], None
        ids = np.fromiter((r.id for r in cands), dtype=np.int64, count=len(cands))
        mat = np.stack([r.vector for r in cands]).astype(np.float32)
        d = distances(query, mat, metric)
        order = np.lexsort((ids, d))  # by distance, then id: the documented tie rule
        ranked = [(int(ids[i]), float(d[i])) for i in order]
        kth = ranked[k - 1][1] if len(ranked) >= k else None
        return ranked, kth


def distances(query: np.ndarray, mat: np.ndarray, metric: str) -> np.ndarray:
    q = query.astype(np.float32)
    if metric == "l2":
        diff = mat - q
        return np.einsum("ij,ij->i", diff, diff)  # squared L2; monotone in L2 so ranking is identical
    if metric == "cosine":
        qn = q / (np.linalg.norm(q) + 1e-12)
        mn = mat / (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-12)
        return 1.0 - mn @ qn
    if metric == "dot":
        return -(mat @ q)
    raise ValueError(metric)
