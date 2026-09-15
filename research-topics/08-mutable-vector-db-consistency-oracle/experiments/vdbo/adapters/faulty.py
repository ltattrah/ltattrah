"""Fault-injected variants of the reference engine. Each violates exactly one contract, so the
classifier's precision can be measured against known ground truth before any real engine is tested."""
from __future__ import annotations

from typing import Optional

import numpy as np

from ..model import Filter, Hit, Record
from .reference import ReferenceEngine


class GhostDeleteEngine(ReferenceEngine):
    """Deletes remove the record from storage, but the search index keeps serving it until a rebuild."""

    name = "faulty-ghost"

    def open(self) -> None:
        super().open()
        self.index: dict[int, Record] = dict(self.mem)

    def upsert(self, records: list[Record]) -> None:
        super().upsert(records)
        for r in records:
            self.index[r.id] = r

    def delete(self, ids: list[int]) -> None:
        super().delete(ids)  # storage forgets, index does not

    def rebuild(self) -> None:
        self.index = dict(self.mem)

    def _visible(self) -> dict[int, Record]:
        return self.index

    def get(self, record_id: int) -> Optional[Hit]:  # point lookups go to storage, which is correct
        r = self.mem.get(record_id)
        return None if r is None else Hit(r.id, r.version, None, dict(r.metadata))

    def count(self) -> Optional[int]:
        return len(self.mem)


class StaleVersionEngine(ReferenceEngine):
    """Upserts of an existing id update storage but the index keeps the old vector and payload until rebuild."""

    name = "faulty-stale"

    def open(self) -> None:
        super().open()
        self.index: dict[int, Record] = dict(self.mem)

    def upsert(self, records: list[Record]) -> None:
        super().upsert(records)
        for r in records:
            self.index.setdefault(r.id, r)  # first version wins in the index

    def delete(self, ids: list[int]) -> None:
        super().delete(ids)
        for i in ids:
            self.index.pop(i, None)

    def rebuild(self) -> None:
        self.index = dict(self.mem)

    def _visible(self) -> dict[int, Record]:
        return self.index


class VisibilityLagEngine(ReferenceEngine):
    """Writes are buffered and become searchable only after flush (a documented eventual-visibility engine)."""

    name = "faulty-lag"
    advertised = {**ReferenceEngine.advertised, "insert_visibility": "eventual (after flush)", "read_your_write": "not guaranteed before flush"}

    def open(self) -> None:
        super().open()
        self.buffer: dict[int, Record] = {}
        self.tombstones: set[int] = set()

    def upsert(self, records: list[Record]) -> None:
        for r in records:
            self.buffer[r.id] = r
            self.tombstones.discard(r.id)
            self._persist(r)

    def delete(self, ids: list[int]) -> None:
        for i in ids:
            self.buffer.pop(i, None)
            self.tombstones.add(i)
            self._unpersist(i)

    def flush(self) -> None:
        self.mem.update(self.buffer)
        for i in self.tombstones:
            self.mem.pop(i, None)
        self.buffer.clear()
        self.tombstones.clear()

    def rebuild(self) -> None:
        self.flush()

    def restart(self) -> None:
        self.flush()
        super().restart()


class FilterInconsistentEngine(ReferenceEngine):
    """The filter index is built from the first version of each record's metadata and never updated
    on upsert, so filtered queries return items whose current metadata violates the filter."""

    name = "faulty-filter"

    def open(self) -> None:
        super().open()
        self.first_meta: dict[int, dict] = {i: dict(r.metadata) for i, r in self.mem.items()}

    def upsert(self, records: list[Record]) -> None:
        super().upsert(records)
        for r in records:
            self.first_meta.setdefault(r.id, dict(r.metadata))

    def delete(self, ids: list[int]) -> None:
        super().delete(ids)
        for i in ids:
            self.first_meta.pop(i, None)

    def rebuild(self) -> None:
        self.first_meta = {i: dict(r.metadata) for i, r in self.mem.items()}

    def _filter_ok(self, rec: Record, filt: Filter) -> bool:
        return filt.matches(self.first_meta.get(rec.id, rec.metadata))


class DurabilityLossEngine(ReferenceEngine):
    """Writes and deletes are acknowledged from memory; only flush persists them. A restart loses
    everything since the last flush (writes vanish, deletes are undone)."""

    name = "faulty-durability"
    advertised = {**ReferenceEngine.advertised, "durability": "only after flush"}

    def _persist(self, rec: Record) -> None:
        pass

    def _unpersist(self, rid: int) -> None:
        pass

    def flush(self) -> None:
        self.disk = dict(self.mem)
        self._write_disk()


class ApproximateEngine(ReferenceEngine):
    """Correct on every contract but approximate: with probability p it swaps the k-th result for the (k+1)-th."""

    name = "faulty-approx"

    def __init__(self, path: str, dim: int, metric: str = "l2", p: float = 0.5) -> None:
        super().__init__(path, dim, metric)
        self.p = p
        self.rng = np.random.default_rng(0)

    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]:
        hits = super().query(vector, k + 1, filt)
        if len(hits) > k and self.rng.random() < self.p:
            hits = hits[: k - 1] + [hits[k]]
        return hits[:k]
