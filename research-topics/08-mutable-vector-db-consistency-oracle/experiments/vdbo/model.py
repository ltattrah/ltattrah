"""Observable vocabulary shared by the generator, the snapshot, the oracle, and every adapter.

Everything an engine can be asked to do, and everything it can answer, is expressed here so the
semantic model in ``model/semantic-model.md`` stays independent of any product's API.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

import numpy as np

CATEGORIES = ("a", "b", "c", "d", "e")
NUM_RANGE = (0, 99)


@dataclass(frozen=True)
class Filter:
    """Metadata predicate: optional category equality and optional inclusive numeric range."""

    cat: Optional[str] = None
    num_min: Optional[int] = None
    num_max: Optional[int] = None

    def matches(self, metadata: dict[str, Any]) -> bool:
        if self.cat is not None and metadata.get("cat") != self.cat:
            return False
        num = metadata.get("num")
        if self.num_min is not None and (num is None or num < self.num_min):
            return False
        if self.num_max is not None and (num is None or num > self.num_max):
            return False
        return True

    @property
    def is_empty(self) -> bool:
        return self.cat is None and self.num_min is None and self.num_max is None

    def describe(self) -> str:
        parts = []
        if self.cat is not None:
            parts.append(f"cat={self.cat}")
        if self.num_min is not None or self.num_max is not None:
            parts.append(f"num∈[{self.num_min},{self.num_max}]")
        return " ∧ ".join(parts) or "∅"


@dataclass
class Record:
    """A version-tagged vector with metadata. ``version`` increases on every upsert of the same id."""

    id: int
    version: int
    vector: np.ndarray
    metadata: dict[str, Any]

    def payload(self) -> dict[str, Any]:
        """Metadata as stored in the engine, including the version tag ``_v``."""
        return {**self.metadata, "_v": self.version}


@dataclass
class Hit:
    """One item returned by an engine query."""

    id: int
    version: Optional[int]  # from the ``_v`` payload field; None if the engine did not return it
    distance: Optional[float]  # engine-reported, informational only
    metadata: dict[str, Any] = field(default_factory=dict)


class OpKind(str, Enum):
    INSERT = "insert"
    UPSERT = "upsert"
    DELETE = "delete"
    QUERY = "query"
    REBUILD = "rebuild"
    FLUSH = "flush"
    RESTART = "restart"
    CRASH = "crash"  # SIGKILL of the engine process, then reopen from disk


@dataclass
class Op:
    kind: OpKind
    record: Optional[Record] = None  # insert / upsert
    id: Optional[int] = None  # delete
    query: Optional[np.ndarray] = None  # query
    k: int = 10
    filter: Filter = field(default_factory=Filter)

    def describe(self) -> str:
        if self.kind in (OpKind.INSERT, OpKind.UPSERT):
            r = self.record
            return f"{self.kind.value}(id={r.id}, v={r.version}, cat={r.metadata['cat']}, num={r.metadata['num']})"
        if self.kind == OpKind.DELETE:
            return f"delete(id={self.id})"
        if self.kind == OpKind.QUERY:
            return f"query(k={self.k}, filter={self.filter.describe()})"
        return self.kind.value


@dataclass
class History:
    """A deterministic sequence of operations plus the parameters that produced it."""

    ops: list[Op]
    dim: int
    seed: int
    params: dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.ops)

    def subset(self, keep: list[int]) -> "History":
        return History(ops=[self.ops[i] for i in keep], dim=self.dim, seed=self.seed, params={**self.params, "reduced_from": len(self.ops)})

    def to_jsonable(self) -> dict[str, Any]:
        out = []
        for op in self.ops:
            d: dict[str, Any] = {"kind": op.kind.value}
            if op.record is not None:
                d["record"] = {"id": op.record.id, "version": op.record.version, "vector": op.record.vector.tolist(), "metadata": op.record.metadata}
            if op.id is not None:
                d["id"] = op.id
            if op.query is not None:
                d["query"] = op.query.tolist()
                d["k"] = op.k
                d["filter"] = {"cat": op.filter.cat, "num_min": op.filter.num_min, "num_max": op.filter.num_max}
            out.append(d)
        return {"dim": self.dim, "seed": self.seed, "params": self.params, "ops": out}

    @classmethod
    def from_jsonable(cls, d: dict[str, Any]) -> "History":
        ops = []
        for o in d["ops"]:
            kind = OpKind(o["kind"])
            rec = None
            if "record" in o:
                r = o["record"]
                rec = Record(r["id"], r["version"], np.asarray(r["vector"], dtype=np.float32), r["metadata"])
            q = np.asarray(o["query"], dtype=np.float32) if "query" in o else None
            f = Filter(**o["filter"]) if "filter" in o else Filter()
            ops.append(Op(kind=kind, record=rec, id=o.get("id"), query=q, k=o.get("k", 10), filter=f))
        return cls(ops=ops, dim=d["dim"], seed=d["seed"], params=d.get("params", {}))
