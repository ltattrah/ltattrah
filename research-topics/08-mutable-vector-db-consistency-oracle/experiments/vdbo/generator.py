"""Deterministic history generator.

Given a seed and a small parameter set it produces the same ``History`` every time. Vectors are drawn
from a Gaussian mixture so near-ties are rare, and a controlled fraction of inserts duplicate an
existing vector exactly so the oracle's tie rule is exercised on purpose.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .model import CATEGORIES, NUM_RANGE, Filter, History, Op, OpKind, Record


@dataclass
class GenParams:
    n_initial: int = 500  # records inserted before the first query
    n_ops: int = 400  # operations after the initial load
    dim: int = 16
    k: int = 10
    mutation_intensity: float = 0.5  # fraction of post-load ops that mutate (insert/upsert/delete)
    upsert_share: float = 0.4  # of mutations: share that are upserts (rest split insert/delete)
    delete_share: float = 0.3
    filter_share: float = 0.6  # of queries: share that carry a metadata filter
    duplicate_share: float = 0.05  # of inserts: share that copy an existing live vector exactly
    rebuild_every: int = 100  # ops between rebuild hints (0 disables)
    flush_every: int = 50  # ops between flushes (0 disables)
    restart_every: int = 150  # ops between clean restarts (0 disables)
    crash_every: int = 0  # ops between SIGKILL crashes (0 disables; needs a crashable adapter)
    crash_rebuild_every: int = 0  # ops between crashes injected during a rebuild (0 disables)
    n_clusters: int = 8
    cluster_spread: float = 0.35


def _sample_vector(rng: np.random.Generator, centers: np.ndarray, spread: float) -> np.ndarray:
    c = centers[rng.integers(len(centers))]
    return (c + rng.normal(0.0, spread, size=c.shape)).astype(np.float32)


def _sample_metadata(rng: np.random.Generator) -> dict:
    return {"cat": str(CATEGORIES[rng.integers(len(CATEGORIES))]), "num": int(rng.integers(NUM_RANGE[0], NUM_RANGE[1] + 1))}


def _sample_filter(rng: np.random.Generator) -> Filter:
    kind = rng.integers(3)
    if kind == 0:
        return Filter(cat=str(CATEGORIES[rng.integers(len(CATEGORIES))]))
    lo = int(rng.integers(NUM_RANGE[0], NUM_RANGE[1] - 20))
    hi = lo + int(rng.integers(10, 40))
    if kind == 1:
        return Filter(num_min=lo, num_max=min(hi, NUM_RANGE[1]))
    return Filter(cat=str(CATEGORIES[rng.integers(len(CATEGORIES))]), num_min=lo, num_max=min(hi, NUM_RANGE[1]))


def generate(seed: int, params: GenParams | None = None) -> History:
    p = params or GenParams()
    rng = np.random.default_rng(seed)
    centers = rng.normal(0.0, 1.0, size=(p.n_clusters, p.dim)).astype(np.float32)

    live: dict[int, Record] = {}
    next_id = 1
    ops: list[Op] = []

    def new_record(rng: np.random.Generator) -> Record:
        nonlocal next_id
        if live and rng.random() < p.duplicate_share:
            src = live[int(rng.choice(list(live.keys())))]
            vec = src.vector.copy()
        else:
            vec = _sample_vector(rng, centers, p.cluster_spread)
        rec = Record(id=next_id, version=1, vector=vec, metadata=_sample_metadata(rng))
        next_id += 1
        return rec

    for _ in range(p.n_initial):
        rec = new_record(rng)
        live[rec.id] = rec
        ops.append(Op(OpKind.INSERT, record=rec))
    if p.flush_every:
        ops.append(Op(OpKind.FLUSH))

    for i in range(1, p.n_ops + 1):
        if p.rebuild_every and i % p.rebuild_every == 0:
            ops.append(Op(OpKind.REBUILD))
        if p.flush_every and i % p.flush_every == 0:
            ops.append(Op(OpKind.FLUSH))
        if p.restart_every and i % p.restart_every == 0:
            ops.append(Op(OpKind.RESTART))
        if p.crash_every and i % p.crash_every == 0:
            ops.append(Op(OpKind.CRASH))
        if p.crash_rebuild_every and i % p.crash_rebuild_every == 0:
            ops.append(Op(OpKind.CRASH_REBUILD))

        if rng.random() < p.mutation_intensity and live:
            u = rng.random()
            if u < p.upsert_share:
                old = live[int(rng.choice(list(live.keys())))]
                new = Record(id=old.id, version=old.version + 1, vector=_sample_vector(rng, centers, p.cluster_spread), metadata=_sample_metadata(rng))
                live[old.id] = new
                ops.append(Op(OpKind.UPSERT, record=new))
            elif u < p.upsert_share + p.delete_share:
                victim = int(rng.choice(list(live.keys())))
                del live[victim]
                ops.append(Op(OpKind.DELETE, id=victim))
            else:
                rec = new_record(rng)
                live[rec.id] = rec
                ops.append(Op(OpKind.INSERT, record=rec))
        else:
            q = _sample_vector(rng, centers, p.cluster_spread * 1.5)
            f = _sample_filter(rng) if rng.random() < p.filter_share else Filter()
            ops.append(Op(OpKind.QUERY, query=q, k=p.k, filter=f))

    ops.append(Op(OpKind.FLUSH))
    ops.append(Op(OpKind.QUERY, query=_sample_vector(rng, centers, p.cluster_spread), k=p.k, filter=Filter()))
    return History(ops=ops, dim=p.dim, seed=seed, params=asdict(p))
