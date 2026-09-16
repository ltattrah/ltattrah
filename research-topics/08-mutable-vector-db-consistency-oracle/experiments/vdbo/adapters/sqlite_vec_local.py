"""sqlite-vec ``vec0`` virtual table: exact KNN inside SQLite, durable through SQLite's journal."""
from __future__ import annotations

import sqlite3
from typing import Optional

import numpy as np
import sqlite_vec

from ..model import Filter, Hit, Record
from .base import EngineAdapter


class SqliteVecEngine(EngineAdapter):
    name = "sqlite-vec"
    has_flush = False
    has_restart = True
    advertised = {c: "SQLite transactional semantics (exact search, synchronous=FULL)" for c in ("insert_visibility", "read_your_write", "version_replacement", "delete_safety", "filter_consistency", "durability", "restart_recovery")}

    def open(self) -> None:
        self.db = sqlite3.connect(f"{self.path}/vec.db", isolation_level=None)
        self.db.enable_load_extension(True)
        sqlite_vec.load(self.db)
        self.db.enable_load_extension(False)
        self.db.execute("PRAGMA synchronous=FULL")
        dist = {"l2": "l2", "cosine": "cosine", "dot": "l2"}[self.metric]
        self.db.execute(f"CREATE VIRTUAL TABLE IF NOT EXISTS vec USING vec0(id INTEGER PRIMARY KEY, vector float[{self.dim}] distance_metric={dist}, cat TEXT, num INTEGER, +ver INTEGER)")

    def close(self) -> None:
        self.db.close()

    def upsert(self, records: list[Record]) -> None:
        self.db.execute("BEGIN")
        for r in records:
            blob = sqlite_vec.serialize_float32(r.vector.astype(np.float32).tolist())
            cur = self.db.execute("UPDATE vec SET vector = ?, cat = ?, num = ?, ver = ? WHERE id = ?", (blob, r.metadata["cat"], int(r.metadata["num"]), r.version, r.id))
            if cur.rowcount == 0:
                self.db.execute("INSERT INTO vec(id, vector, cat, num, ver) VALUES (?, ?, ?, ?, ?)", (r.id, blob, r.metadata["cat"], int(r.metadata["num"]), r.version))
        self.db.execute("COMMIT")

    def delete(self, ids: list[int]) -> None:
        self.db.execute("BEGIN")
        for i in ids:
            self.db.execute("DELETE FROM vec WHERE id = ?", (i,))
        self.db.execute("COMMIT")

    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]:
        where, params = ["vector MATCH ?", "k = ?"], [sqlite_vec.serialize_float32(vector.astype(np.float32).tolist()), k]
        if filt.cat is not None:
            where.append("cat = ?"); params.append(filt.cat)
        if filt.num_min is not None:
            where.append("num >= ?"); params.append(filt.num_min)
        if filt.num_max is not None:
            where.append("num <= ?"); params.append(filt.num_max)
        rows = self.db.execute(f"SELECT id, distance, cat, num, ver FROM vec WHERE {' AND '.join(where)} ORDER BY distance", params).fetchall()
        return [Hit(id=int(r[0]), version=int(r[4]), distance=float(r[1]), metadata={"cat": r[2], "num": int(r[3])}) for r in rows]

    def get(self, record_id: int) -> Optional[Hit]:
        r = self.db.execute("SELECT id, cat, num, ver FROM vec WHERE id = ?", (record_id,)).fetchone()
        return None if r is None else Hit(id=int(r[0]), version=int(r[3]), distance=None, metadata={"cat": r[1], "num": int(r[2])})

    def count(self) -> Optional[int]:
        return int(self.db.execute("SELECT count(*) FROM vec").fetchone()[0])

    def rebuild(self) -> None:
        self.db.execute("VACUUM")

    def version_info(self) -> str:
        return f"sqlite-vec {sqlite_vec.__version__} on SQLite {sqlite3.sqlite_version}"
