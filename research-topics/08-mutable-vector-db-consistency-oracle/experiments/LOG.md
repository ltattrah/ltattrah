# Lab log — Topic 08

## 2026-09-15 — Day 1: oracle skeleton, classifier validation, first engine runs

**Built.** `vdbo/` package: version-tagged history generator (deterministic from seed), logical snapshot, exact top-k with a documented tie rule, six-class discrepancy classifier, reference engine, five single-fault engines plus an approximate one, adapters for Qdrant local, Chroma, LanceDB (flat and IVF_FLAT), a SIGKILL crash harness, a ddmin reducer, and `campaign.py`. `tests/test_oracle.py` (9 tests) passes.

**Two classifier refinements found by fault injection, both now in the semantic model (§4–5):**

1. A buffered-write engine (`faulty-lag`) also delays deletes and upserts. Before its flush a deleted id is still returned and an upserted id carries the old version. Under its advertised eventual semantics these are *visibility lag of the delete/upsert*, not ghost/stale violations, provided a flush resolves them. Rules 2 and 5 encode this.
2. A nondeterministic approximate engine (`faulty-approx`) can return a missing item on the re-query after flush by chance, which looked like visibility lag. The protocol now needs a repeat query *before* the flush; lag is declared only if the discrepancy is stable pre-flush and resolved post-flush.

**Harness lesson.** The first reference engine kept its "disk" in process memory, so SIGKILL wiped it and produced 205 durability findings. That was the harness, not a finding. The reference engine now writes an atomic, fsynced pickle on every acknowledged write.

**Engine runs (sequential histories, 1k vectors, dim 16, k 10, three mutation intensities, clean restarts every 200 ops):** Qdrant local, Chroma, LanceDB flat, LanceDB IVF_FLAT all show **zero contract violations**; recall 1.0 except Chroma 0.9985 at intensity 0.9 (HNSW approximation). SIGKILL crashes every 120 ops at 600 vectors: also zero violations on all four.

**Interpretation.** Negative so far, but the histories are small, sequential, and the engines are embedded/local modes. Gate 2 (Day 60) is the decision point, not today. Highest-yield next probes: (a) scale to 100k with Chroma's HNSW and LanceDB IVF where deletes and unindexed rows interact with index rebuilds; (b) concurrent writers; (c) crash *during* a rebuild/compaction rather than between ops; (d) Chroma `hnsw:sync_threshold` and batch-size settings that change when the index is persisted; (e) server-mode Qdrant and one more engine (Milvus Lite or SQLite-vec) to reach the four-engine requirement with production code paths.
