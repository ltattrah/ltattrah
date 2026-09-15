"""Correct engine used to validate the oracle itself.

It keeps an in-memory table and a pickle file on disk written atomically (write temp, fsync, rename) on
every acknowledged write, so it satisfies every contract in the semantic model including durability
under SIGKILL. Faulty variants override single methods to violate one contract each.
"""
from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Optional

import numpy as np

from ..model import Filter, Hit, Record
from ..snapshot import distances
from .base import EngineAdapter

class ReferenceEngine(EngineAdapter):
    name = "reference"
    has_flush = True
    has_restart = True
    advertised = {c: "strict" for c in ("insert_visibility", "read_your_write", "version_replacement", "delete_safety", "filter_consistency", "durability", "restart_recovery")}

    def _store(self) -> Path:
        return Path(self.path) / "store.pkl"

    def open(self) -> None:
        sp = self._store()
        self.disk: dict[int, Record] = pickle.loads(sp.read_bytes()) if sp.exists() else {}
        self.mem: dict[int, Record] = dict(self.disk)

    def close(self) -> None:
        pass

    def _write_disk(self) -> None:
        sp = self._store()
        sp.parent.mkdir(parents=True, exist_ok=True)
        tmp = sp.with_suffix(".tmp")
        with open(tmp, "wb") as fh:
            pickle.dump(self.disk, fh)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, sp)

    def _persist(self, rec: Record) -> None:
        self.disk[rec.id] = rec
        self._write_disk()

    def _unpersist(self, rid: int) -> None:
        self.disk.pop(rid, None)
        self._write_disk()

    def upsert(self, records: list[Record]) -> None:
        for r in records:
            self.mem[r.id] = r
            self._persist(r)

    def delete(self, ids: list[int]) -> None:
        for i in ids:
            self.mem.pop(i, None)
            self._unpersist(i)

    def _visible(self) -> dict[int, Record]:
        return self.mem

    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]:
        vis = [r for r in self._visible().values() if self._filter_ok(r, filt)]
        if not vis:
            return []
        mat = np.stack([r.vector for r in vis])
        d = distances(vector, mat, self.metric)
        ids = np.array([r.id for r in vis])
        order = np.lexsort((ids, d))[:k]
        return [Hit(id=int(ids[i]), version=vis[i].version, distance=float(d[i]), metadata=dict(vis[i].metadata)) for i in order]

    def _filter_ok(self, rec: Record, filt: Filter) -> bool:
        return filt.matches(rec.metadata)

    def get(self, record_id: int) -> Optional[Hit]:
        r = self._visible().get(record_id)
        return None if r is None else Hit(id=r.id, version=r.version, distance=None, metadata=dict(r.metadata))

    def count(self) -> Optional[int]:
        return len(self._visible())
