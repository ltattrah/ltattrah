"""LanceDB embedded. ``LanceDBEngine`` searches flat (exact); ``LanceDBEngine.indexed`` builds an IVF
index at every rebuild so freshly written rows sit outside the index until the next rebuild."""
from __future__ import annotations

from typing import Optional

import lancedb
import numpy as np
import pyarrow as pa

from ..model import Filter, Hit, Record
from .base import EngineAdapter

TABLE = "vdbo"


class LanceDBEngine(EngineAdapter):
    name = "lancedb"
    has_flush = False
    has_restart = True
    use_index = False
    advertised = {
        "insert_visibility": "immediate; unindexed rows are scanned with the index (when present)",
        "read_your_write": "expected",
        "version_replacement": "merge_insert on id updates the row",
        "delete_safety": "deleted rows are filtered out",
        "filter_consistency": "SQL where-clause, pre-filter",
        "durability": "each write commits a new table version",
        "restart_recovery": "table reopens at latest committed version",
    }

    def open(self) -> None:
        self.db = lancedb.connect(self.path)
        schema = pa.schema([
            pa.field("id", pa.int64()),
            pa.field("vector", pa.list_(pa.float32(), self.dim)),
            pa.field("cat", pa.string()),
            pa.field("num", pa.int64()),
            pa.field("ver", pa.int64()),
        ])
        if TABLE in self.db.table_names():
            self.tbl = self.db.open_table(TABLE)
        else:
            self.tbl = self.db.create_table(TABLE, schema=schema)
        self.has_index = False

    def close(self) -> None:
        self.tbl = None
        self.db = None

    @staticmethod
    def _row(r: Record) -> dict:
        return {"id": r.id, "vector": r.vector.astype(np.float32).tolist(), "cat": r.metadata["cat"], "num": int(r.metadata["num"]), "ver": r.version}

    def upsert(self, records: list[Record]) -> None:
        self.tbl.merge_insert("id").when_matched_update_all().when_not_matched_insert_all().execute([self._row(r) for r in records])

    def delete(self, ids: list[int]) -> None:
        self.tbl.delete(f"id IN ({', '.join(str(i) for i in ids)})")

    @staticmethod
    def _where(filt: Filter) -> Optional[str]:
        parts = []
        if filt.cat is not None:
            parts.append(f"cat = '{filt.cat}'")
        if filt.num_min is not None:
            parts.append(f"num >= {filt.num_min}")
        if filt.num_max is not None:
            parts.append(f"num <= {filt.num_max}")
        return " AND ".join(parts) or None

    def query(self, vector: np.ndarray, k: int, filt: Filter) -> list[Hit]:
        q = self.tbl.search(vector.astype(np.float32).tolist(), vector_column_name="vector").distance_type(self.metric).limit(k)
        w = self._where(filt)
        if w:
            q = q.where(w, prefilter=True)
        rows = q.to_list()
        return [Hit(id=int(r["id"]), version=int(r["ver"]), distance=float(r["_distance"]), metadata={"cat": r["cat"], "num": int(r["num"])}) for r in rows]

    def get(self, record_id: int) -> Optional[Hit]:
        rows = self.tbl.search().where(f"id = {record_id}").limit(2).to_list()
        if not rows:
            return None
        r = rows[0]
        return Hit(id=int(r["id"]), version=int(r["ver"]), distance=None, metadata={"cat": r["cat"], "num": int(r["num"])})

    def count(self) -> Optional[int]:
        return int(self.tbl.count_rows())

    def rebuild(self) -> None:
        if self.use_index and self.tbl.count_rows() >= 64:
            self.tbl.create_index(metric=self.metric, index_type="IVF_FLAT", num_partitions=4, replace=True)
            self.has_index = True
        self.tbl.optimize()  # compaction: rewrites fragments and prunes old versions

    def version_info(self) -> str:
        return f"lancedb {lancedb.__version__} ({'IVF_FLAT at rebuild' if self.use_index else 'flat scan'})"

    @classmethod
    def indexed(cls, **kw) -> "LanceDBEngine":
        eng = cls(**kw)
        eng.use_index = True
        eng.name = "lancedb-ivfflat"
        return eng
