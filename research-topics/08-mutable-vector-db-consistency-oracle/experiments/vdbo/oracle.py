"""Discrepancy classifier.

Given the logical snapshot at a query and the engine's answer, every returned item and every missing
exact neighbour is assigned exactly one class. Item-level checks (ghost, stale version, filter) never
depend on the approximation tolerance; only the *approximation* class does, and it is reported as a
recall figure rather than as a violation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional

import numpy as np

from .model import Filter, Hit
from .snapshot import Snapshot, distances

TIE_EPS = 1e-5  # relative tolerance for "same distance" when applying the tie rule


class FailureClass(str, Enum):
    APPROXIMATION = "approximation"  # valid item outside the exact set, or exact item missing (recall)
    STALE_VERSION = "stale_version"  # id is live but returned with a superseded version
    GHOST_RESULT = "ghost_result"  # id was deleted (or never existed) yet is returned
    VISIBILITY_LAG = "visibility_lag"  # fresh write not yet visible, becomes visible after flush
    FILTER_INCONSISTENCY = "filter_inconsistency"  # returned item does not satisfy the query filter
    DURABILITY_LOSS = "durability_loss"  # acknowledged write or delete lost or undone across a restart
    OK = "ok"


@dataclass
class Finding:
    op_index: int
    failure: FailureClass
    record_id: Optional[int]
    detail: str
    filter: str = "∅"

    def as_row(self) -> dict:
        return {"op_index": self.op_index, "class": self.failure.value, "id": self.record_id, "detail": self.detail, "filter": self.filter}


@dataclass
class QueryVerdict:
    op_index: int
    k: int
    n_exact: int  # size of the exact set actually available (min(k, candidates))
    recall: float
    findings: list[Finding] = field(default_factory=list)
    hits_valid: int = 0

    def classes(self) -> set[FailureClass]:
        return {f.failure for f in self.findings}


def classify_query(
    snap: Snapshot,
    op_index: int,
    query: np.ndarray,
    k: int,
    filt: Filter,
    hits: list[Hit],
    hits_after_flush: Optional[list[Hit]],
    metric: str,
    hits_repeat: Optional[list[Hit]] = None,
    lookup: Optional[Callable[[int], Optional[Hit]]] = None,
) -> QueryVerdict:
    """``hits_repeat`` is a second query issued *before* any flush. Visibility lag is declared only when
    the discrepancy is stable across both pre-flush queries and resolves after the flush; otherwise a
    nondeterministic approximate engine could be mistaken for a lagging one.

    ``lookup`` is a point-lookup callable used only for exact neighbours that are missing after a
    restart or crash: if the record cannot be fetched by id (or comes back with an old version) the
    miss is durability loss, not approximation."""
    ranked, kth = snap.exact_topk(query, k, filt, metric)
    n_exact = min(k, len(ranked))
    exact_ids = {i for i, _ in ranked[:n_exact]}
    # tie-equivalent items: anything at the k-th distance is an acceptable substitute
    tie_ok = {i for i, d in ranked if kth is not None and d <= kth * (1 + TIE_EPS) + 1e-12}
    verdict = QueryVerdict(op_index=op_index, k=k, n_exact=n_exact, recall=0.0)
    fdesc = filt.describe()

    after_by_id: Optional[dict[int, Hit]] = {h.id: h for h in hits_after_flush} if hits_after_flush is not None else None
    repeat_by_id: Optional[dict[int, Hit]] = {h.id: h for h in hits_repeat} if hits_repeat is not None else None

    def stable_before_flush(rid: int, version: Optional[int]) -> bool:
        if repeat_by_id is None:
            return True
        return rid in repeat_by_id and repeat_by_id[rid].version == version

    def stably_missing_before_flush(rid: int) -> bool:
        return repeat_by_id is None or rid not in repeat_by_id

    returned: set[int] = set()
    valid_returned: set[int] = set()
    for h in hits:
        returned.add(h.id)
        if h.id not in snap.live:
            if h.id in snap.deleted:
                d = snap.deleted[h.id]
                if snap.epoch > d.epoch:
                    verdict.findings.append(Finding(op_index, FailureClass.DURABILITY_LOSS, h.id, f"deleted id returned after restart (delete at op {d.op_index}, v{d.last_version})", fdesc))
                elif not d.synced and after_by_id is not None and h.id not in after_by_id and stable_before_flush(h.id, h.version):
                    verdict.findings.append(Finding(op_index, FailureClass.VISIBILITY_LAG, h.id, f"unsynced delete (op {d.op_index}) still visible; gone after flush", fdesc))
                else:
                    verdict.findings.append(Finding(op_index, FailureClass.GHOST_RESULT, h.id, f"deleted id returned (delete at op {d.op_index}, v{d.last_version}, synced={d.synced})", fdesc))
            else:
                verdict.findings.append(Finding(op_index, FailureClass.GHOST_RESULT, h.id, "id never written in this history", fdesc))
            continue
        rec = snap.live[h.id]
        if h.version is not None and h.version != rec.version:
            w = snap.writes[h.id]
            resolved = after_by_id is not None and (h.id not in after_by_id or after_by_id[h.id].version == rec.version)
            if snap.epoch > w.epoch:
                verdict.findings.append(Finding(op_index, FailureClass.DURABILITY_LOSS, h.id, f"version v{h.version} returned after restart; current v{rec.version} written at op {w.op_index}", fdesc))
            elif not w.synced and resolved and stable_before_flush(h.id, h.version):
                verdict.findings.append(Finding(op_index, FailureClass.VISIBILITY_LAG, h.id, f"unsynced upsert (op {w.op_index}) not yet visible: returned v{h.version}; current after flush", fdesc))
            else:
                verdict.findings.append(Finding(op_index, FailureClass.STALE_VERSION, h.id, f"returned v{h.version}, current v{rec.version} (written op {w.op_index}, synced={w.synced})", fdesc))
            continue
        if not filt.matches(rec.metadata):
            verdict.findings.append(Finding(op_index, FailureClass.FILTER_INCONSISTENCY, h.id, f"metadata {rec.metadata} violates filter", fdesc))
            continue
        valid_returned.add(h.id)
        if h.id not in exact_ids and h.id not in tie_ok:
            verdict.findings.append(Finding(op_index, FailureClass.APPROXIMATION, h.id, "valid item outside exact top-k", fdesc))

    verdict.hits_valid = len(valid_returned)
    exact_or_tie_returned = valid_returned & (exact_ids | tie_ok)
    verdict.recall = (min(len(exact_or_tie_returned), n_exact) / n_exact) if n_exact else 1.0

    after = {h.id for h in hits_after_flush} if hits_after_flush is not None else None
    # Items strictly inside the k-th distance must be returned. Items *at* the k-th distance form a tie
    # group; any member may stand in for another, so a boundary item is "missing" only when the engine
    # returned fewer boundary members than the exact set needs.
    strict = {i for i, d in ranked[:n_exact] if kth is None or d < kth * (1 - TIE_EPS) - 1e-12}
    boundary_needed = n_exact - len(strict)
    boundary_returned = len(valid_returned & (tie_ok - strict))
    missing = (strict - returned) | (set() if boundary_returned >= boundary_needed else (exact_ids - strict - returned))
    for mid in sorted(missing):
        w = snap.writes[mid]
        if snap.epoch > w.epoch and lookup is not None:
            got = lookup(mid)
            cur = snap.live[mid].version
            if got is None:
                verdict.findings.append(Finding(op_index, FailureClass.DURABILITY_LOSS, mid, f"acknowledged record (op {w.op_index}, v{cur}) absent after restart/crash", fdesc))
                continue
            if got.version is not None and got.version != cur:
                verdict.findings.append(Finding(op_index, FailureClass.DURABILITY_LOSS, mid, f"record reverted to v{got.version} after restart/crash, expected v{cur}", fdesc))
                continue
        if not w.synced and after is not None and mid in after and stably_missing_before_flush(mid):
            verdict.findings.append(Finding(op_index, FailureClass.VISIBILITY_LAG, mid, f"fresh write (op {w.op_index}) missing, visible after flush", fdesc))
        elif not w.synced and after is None:
            verdict.findings.append(Finding(op_index, FailureClass.APPROXIMATION, mid, f"fresh write (op {w.op_index}) missing; no flush probe available", fdesc))
        else:
            verdict.findings.append(Finding(op_index, FailureClass.APPROXIMATION, mid, "exact neighbour missing", fdesc))
    return verdict


def classify_probe(snap: Snapshot, op_index: int, live_probe: dict[int, Optional[Hit]], deleted_probe: dict[int, Optional[Hit]], count: Optional[int]) -> list[Finding]:
    """Point-lookup probes run after a restart: acknowledged live ids must exist with the current
    version, deleted ids must not, and the total count must match the snapshot."""
    out: list[Finding] = []
    for rid, hit in live_probe.items():
        rec = snap.live[rid]
        if hit is None:
            out.append(Finding(op_index, FailureClass.DURABILITY_LOSS, rid, f"acknowledged record missing after restart (v{rec.version}, written op {snap.writes[rid].op_index})"))
        elif hit.version is not None and hit.version != rec.version:
            out.append(Finding(op_index, FailureClass.DURABILITY_LOSS, rid, f"v{hit.version} found after restart, expected v{rec.version}"))
    for rid, hit in deleted_probe.items():
        if hit is not None:
            out.append(Finding(op_index, FailureClass.DURABILITY_LOSS, rid, f"deleted id present after restart (delete at op {snap.deleted[rid].op_index})"))
    if count is not None and count != len(snap.live):
        out.append(Finding(op_index, FailureClass.DURABILITY_LOSS, None, f"count {count} after restart, snapshot has {len(snap.live)} live records"))
    return out
