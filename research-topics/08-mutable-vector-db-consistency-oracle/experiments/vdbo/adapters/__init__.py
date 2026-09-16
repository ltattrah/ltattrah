from .base import EngineAdapter
from .reference import ReferenceEngine
from . import faulty

REGISTRY: dict[str, type] = {
    "reference": ReferenceEngine,
    "faulty-ghost": faulty.GhostDeleteEngine,
    "faulty-stale": faulty.StaleVersionEngine,
    "faulty-lag": faulty.VisibilityLagEngine,
    "faulty-filter": faulty.FilterInconsistentEngine,
    "faulty-durability": faulty.DurabilityLossEngine,
    "faulty-approx": faulty.ApproximateEngine,
}


def available_real_engines() -> dict[str, type]:
    out: dict[str, type] = {}
    try:
        from .qdrant_local import QdrantLocalEngine
        out["qdrant-local"] = QdrantLocalEngine
    except ImportError:
        pass
    try:
        from .chroma_local import ChromaEngine
        out["chroma"] = ChromaEngine
        out["chroma-smallsync"] = ChromaEngine.small_sync
    except ImportError:
        pass
    try:
        from .milvus_lite import MilvusLiteEngine
        out["milvus-lite"] = MilvusLiteEngine
        out["milvus-lite-eventually"] = MilvusLiteEngine.eventually
    except ImportError:
        pass
    try:
        from .sqlite_vec_local import SqliteVecEngine
        out["sqlite-vec"] = SqliteVecEngine
    except ImportError:
        pass
    try:
        from .lancedb_local import LanceDBEngine
        out["lancedb"] = LanceDBEngine
        out["lancedb-ivfflat"] = LanceDBEngine.indexed
    except ImportError:
        pass
    return out


def make(name: str, **kw) -> EngineAdapter:
    reg = {**REGISTRY, **available_real_engines()}
    if name not in reg:
        raise KeyError(f"unknown engine {name!r}; known: {sorted(reg)}")
    return reg[name](**kw)


__all__ = ["EngineAdapter", "ReferenceEngine", "REGISTRY", "available_real_engines", "make"]
