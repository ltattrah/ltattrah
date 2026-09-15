"""Delta-debugging (ddmin) reducer for failing histories.

Given a history and a target failure class that the engine exhibits on it, find a 1-minimal subset of
operations (always keeping the final query) that still triggers the class. Each trial re-runs the
engine from a fresh path, so the result is a reproducible minimal history, not a heuristic.
"""
from __future__ import annotations

from typing import Callable

from .adapters.base import EngineAdapter
from .model import History, OpKind
from .oracle import FailureClass
from .runner import run_history


def _triggers(factory: Callable[[str], EngineAdapter], hist: History, target: FailureClass) -> bool:
    res = run_history(factory, hist, probe_sample=10, stop_on_first=True)
    return target in {f.failure for f in res.findings}


def ddmin(factory: Callable[[str], EngineAdapter], history: History, target: FailureClass, max_trials: int = 400) -> tuple[History, int]:
    """Return (minimal history, trials used). Preserves relative order of operations."""
    n_all = len(history.ops)
    # keep every query and the structural ops as candidates too; ddmin decides what survives
    idx = list(range(n_all))
    if not _triggers(factory, history, target):
        raise ValueError("history does not trigger the target class on this engine")
    trials = 1
    granularity = 2
    while len(idx) >= 2 and trials < max_trials:
        chunk = max(1, len(idx) // granularity)
        chunks = [idx[i : i + chunk] for i in range(0, len(idx), chunk)]
        reduced = False
        for c in chunks:
            complement = [i for i in idx if i not in set(c)]
            if not complement:
                continue
            trials += 1
            if _triggers(factory, history.subset(complement), target):
                idx = complement
                granularity = max(granularity - 1, 2)
                reduced = True
                break
        if not reduced:
            if granularity >= len(idx):
                break
            granularity = min(len(idx), granularity * 2)
    return history.subset(idx), trials


def describe(history: History) -> str:
    return "\n".join(f"{i:4d}  {op.describe()}" for i, op in enumerate(history.ops))
