"""Execute a history against an adapter in lockstep with the logical snapshot and collect findings."""
from __future__ import annotations

import shutil
import tempfile
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import numpy as np

from .adapters.base import EngineAdapter
from .model import History, Op, OpKind
from .oracle import FailureClass, Finding, QueryVerdict, classify_probe, classify_query
from .snapshot import Snapshot


@dataclass
class RunResult:
    engine: str
    engine_version: str
    n_ops: int
    n_queries: int
    verdicts: list[QueryVerdict] = field(default_factory=list)
    probe_findings: list[Finding] = field(default_factory=list)
    seconds: float = 0.0
    error: Optional[str] = None

    @property
    def findings(self) -> list[Finding]:
        out = [f for v in self.verdicts for f in v.findings]
        out.extend(self.probe_findings)
        return out

    def class_counts(self) -> Counter:
        return Counter(f.failure.value for f in self.findings)

    def violation_classes(self) -> set[FailureClass]:
        return {f.failure for f in self.findings if f.failure not in (FailureClass.APPROXIMATION, FailureClass.OK)}

    def mean_recall(self) -> float:
        return float(np.mean([v.recall for v in self.verdicts])) if self.verdicts else float("nan")

    def queries_with_violation(self) -> int:
        return sum(1 for v in self.verdicts if v.classes() - {FailureClass.APPROXIMATION, FailureClass.OK})

    def summary(self) -> dict:
        c = self.class_counts()
        return {
            "engine": self.engine,
            "version": self.engine_version,
            "ops": self.n_ops,
            "queries": self.n_queries,
            "mean_recall": round(self.mean_recall(), 4),
            "queries_with_violation": self.queries_with_violation(),
            **{k.value: c.get(k.value, 0) for k in FailureClass if k != FailureClass.OK},
            "seconds": round(self.seconds, 2),
            "error": self.error,
        }


def run_history(
    adapter_factory: Callable[[str], EngineAdapter],
    history: History,
    probe_sample: int = 25,
    workdir: Optional[str] = None,
    stop_on_first: bool = False,
    batch_writes: bool = True,
) -> RunResult:
    """``adapter_factory(path)`` must return an *unopened* adapter bound to a fresh path.

    With ``batch_writes`` consecutive insert/upsert ops with distinct ids are sent in one ``upsert`` call.
    No query, delete, or structural op sits between them, so the logical snapshot is identical."""
    tmp = workdir or tempfile.mkdtemp(prefix="vdbo-")
    adapter = adapter_factory(tmp)
    snap = Snapshot()
    result = RunResult(engine=adapter.name, engine_version="", n_ops=len(history.ops), n_queries=0)
    rng = np.random.default_rng(history.seed ^ 0xC0FFEE)
    t0 = time.time()
    try:
        adapter.open()
        result.engine_version = adapter.version_info()
        ops = history.ops
        i = 0
        while i < len(ops):
            op = ops[i]
            if op.kind in (OpKind.INSERT, OpKind.UPSERT):
                batch = [op.record]
                seen = {op.record.id}
                j = i + 1
                while batch_writes and j < len(ops) and ops[j].kind in (OpKind.INSERT, OpKind.UPSERT) and ops[j].record.id not in seen and len(batch) < 512:
                    batch.append(ops[j].record)
                    seen.add(ops[j].record.id)
                    j += 1
                adapter.upsert(batch)
                for jj in range(i, j):
                    snap.apply(ops[jj], jj)
                i = j
                continue
            if op.kind == OpKind.DELETE:
                adapter.delete([op.id])
            elif op.kind == OpKind.FLUSH:
                adapter.flush()
            elif op.kind == OpKind.REBUILD:
                adapter.rebuild()
            elif op.kind == OpKind.RESTART:
                if adapter.has_restart:
                    adapter.restart()
            elif op.kind == OpKind.CRASH:
                if getattr(adapter, "has_crash", False):
                    adapter.crash()
            elif op.kind == OpKind.CRASH_REBUILD:
                if getattr(adapter, "has_crash", False):
                    adapter.crash_during("rebuild")
            snap.apply(op, i)

            crashable = getattr(adapter, "has_crash", False)
            probe_now = (op.kind == OpKind.RESTART and adapter.has_restart) or (op.kind in (OpKind.CRASH, OpKind.CRASH_REBUILD) and crashable)
            if probe_now:
                live_ids = list(snap.live)
                del_ids = list(snap.deleted)
                live_s = [int(x) for x in rng.choice(live_ids, size=min(probe_sample, len(live_ids)), replace=False)] if live_ids else []
                del_s = [int(x) for x in rng.choice(del_ids, size=min(probe_sample, len(del_ids)), replace=False)] if del_ids else []
                pf = classify_probe(snap, i, {r: adapter.get(r) for r in live_s}, {r: adapter.get(r) for r in del_s}, adapter.count())
                result.probe_findings.extend(pf)
            elif op.kind == OpKind.QUERY:
                result.n_queries += 1
                hits = adapter.query(op.query, op.k, op.filter)
                after = None
                repeat = None
                if adapter.has_flush:
                    ranked, _ = snap.exact_topk(op.query, op.k, op.filter, adapter.metric)
                    hit_ids = {h.id for h in hits}
                    fresh_missing = [rid for rid, _ in ranked[: op.k] if rid not in hit_ids and not snap.writes[rid].synced]
                    unsynced_ghosts = [h.id for h in hits if h.id in snap.deleted and not snap.deleted[h.id].synced]
                    unsynced_stale = [h.id for h in hits if h.id in snap.live and h.version is not None and h.version != snap.live[h.id].version and not snap.writes[h.id].synced]
                    if fresh_missing or unsynced_ghosts or unsynced_stale:
                        repeat = adapter.query(op.query, op.k, op.filter)
                        adapter.flush()
                        after = adapter.query(op.query, op.k, op.filter)
                v = classify_query(snap, i, op.query, op.k, op.filter, hits, after, adapter.metric, hits_repeat=repeat, lookup=adapter.get)
                if after is not None:
                    snap.apply(Op(OpKind.FLUSH), i)  # the probe flush is itself a sync point for later ops
                result.verdicts.append(v)
                if stop_on_first and (v.classes() - {FailureClass.APPROXIMATION, FailureClass.OK}):
                    break
            i += 1
    except Exception as exc:  # noqa: BLE001 - report, never hide, adapter failures
        result.error = f"{type(exc).__name__}: {exc}"
    finally:
        try:
            adapter.close()
        except Exception:  # noqa: BLE001
            pass
        if workdir is None:
            shutil.rmtree(tmp, ignore_errors=True)
        result.seconds = time.time() - t0
    return result
