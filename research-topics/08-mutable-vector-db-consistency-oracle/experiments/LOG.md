# Lab log — Topic 08

## 2026-09-15 — Day 1: oracle skeleton, classifier validation, first engine runs

**Built.** `vdbo/` package: version-tagged history generator (deterministic from seed), logical snapshot, exact top-k with a documented tie rule, six-class discrepancy classifier, reference engine, five single-fault engines plus an approximate one, adapters for Qdrant local, Chroma, LanceDB (flat and IVF_FLAT), a SIGKILL crash harness, a ddmin reducer, and `campaign.py`. `tests/test_oracle.py` (9 tests) passes.

**Two classifier refinements found by fault injection, both now in the semantic model (§4–5):**

1. A buffered-write engine (`faulty-lag`) also delays deletes and upserts. Before its flush a deleted id is still returned and an upserted id carries the old version. Under its advertised eventual semantics these are *visibility lag of the delete/upsert*, not ghost/stale violations, provided a flush resolves them. Rules 2 and 5 encode this.
2. A nondeterministic approximate engine (`faulty-approx`) can return a missing item on the re-query after flush by chance, which looked like visibility lag. The protocol now needs a repeat query *before* the flush; lag is declared only if the discrepancy is stable pre-flush and resolved post-flush.

**Harness lesson.** The first reference engine kept its "disk" in process memory, so SIGKILL wiped it and produced 205 durability findings. That was the harness, not a finding. The reference engine now writes an atomic, fsynced pickle on every acknowledged write.

**Engine runs (sequential histories, 1k vectors, dim 16, k 10, three mutation intensities, clean restarts every 200 ops):** Qdrant local, Chroma, LanceDB flat, LanceDB IVF_FLAT all show **zero contract violations**; recall 1.0 except Chroma 0.9985 at intensity 0.9 (HNSW approximation). SIGKILL crashes every 120 ops at 600 vectors: also zero violations on all four.

**Interpretation.** Negative so far, but the histories are small, sequential, and the engines are embedded/local modes. Gate 2 (Day 60) is the decision point, not today. Highest-yield next probes: (a) scale to 100k with Chroma's HNSW and LanceDB IVF where deletes and unindexed rows interact with index rebuilds; (b) concurrent writers; (c) crash *during* a rebuild/compaction rather than between ops; (d) Chroma `hnsw:sync_threshold` and batch-size settings that change when the index is persisted; (e) server-mode Qdrant and one more engine (Milvus Lite or SQLite-vec) to reach the four-engine requirement with production code paths.

## 2026-09-16 — Day 2: five engines, crash-during-rebuild, first scale run

**Built.** Adapters for Milvus Lite (`Strong` and `Eventually` consistency, `flush` = segment seal, `rebuild` = `compact`) and sqlite-vec (`vec0`, exact, `synchronous=FULL`); a Chroma variant with `sync_threshold=20, batch_size=10` so HNSW persistence happens every 20 writes; a `crash_rebuild` operation that SIGKILLs the engine while `rebuild`/`optimize`/`compact` is in flight; write batching in the runner (consecutive inserts with distinct ids go in one call, snapshot unchanged) which cut LanceDB from 65 s to 10 s per history; `analysis/recall_breakdown.py`.

**Engine set now:** Qdrant local, Chroma, Chroma small-sync, LanceDB flat, LanceDB IVF_FLAT, Milvus Lite (Strong, Eventually), sqlite-vec. Five distinct code bases, satisfying the "≥ 4 engines" line of the evidence package, though two (Qdrant local, Milvus Lite) are embedded builds rather than the server engines.

**Runs.**

| Campaign | Config | Result |
|---|---|---|
| Restart, all 9 configs | 2k vectors, dim 16, mi 0.6, restart every 200 | 0 violations, recall 1.0 everywhere (`analysis/2026-09-16-restart-2k-all-engines.md`) |
| Crash + crash-during-rebuild, all 9 configs, 2 seeds | 2k vectors, crash every 200, crash-rebuild every 300 | 0 violations, recall 1.0 everywhere (`analysis/2026-09-16-crash-and-crash-rebuild-2k-2seeds.md`) |
| Scale, 6 configs | 50k vectors, dim 32, 3000 ops, restart every 500 | in progress; Chroma 0.9852, Chroma small-sync 0.9884, LanceDB IVF_FLAT 1.0, Milvus Lite 1.0 recall, 0 violations so far |
| Recall breakdown | Chroma 10k, dim 32 | 11 of 582 queries below 1.0, **all unfiltered**, each missing exactly one neighbour (recall 0.900); every filtered query exact |

**Observations.**

1. **Approximation is separable from staleness in practice, not only in the model.** Across ~5k queries on real engines every discrepancy the classifier saw was an approximation miss; none was a version, ghost, filter, or durability finding. The oracle's tolerance-free rules stayed silent while its recall figure moved. That is the behaviour the paper needs to demonstrate, and the fault-injected engines show the rules do fire when contracts break.
2. **Chroma: filtered queries are exact, unfiltered are approximate.** Consistent with a brute-force scan over the filter's allowed ids versus an HNSW traversal. Worth confirming in the source and stating as a documented deviation, since it means filter selectivity *improves* recall in Chroma, the opposite of the usual filtered-ANN story.
3. **Milvus Lite ignores or hides `Eventually`.** No visibility difference between Strong and Eventually; the documented weakening is not observable in the embedded build. Server-mode Milvus is needed to test it.
4. **SIGKILL is not power loss.** Everything the engines handed to the kernel survived. The result rules out application-buffer loss, not missing `fsync`. Logged as a limitation in the semantic model §8.
5. **Crash-during-rebuild timing.** Rebuilds at 2k vectors take milliseconds, so most kills land just after completion. At 50k+ the window is real (LanceDB `optimize` and IVF training take seconds).

**Decision.** Still negative on contract violations. Two of the five Day-1 "next probes" are done (fourth engine, crash-during-rebuild, persistence settings); remaining: 100k+ scale with rebuilds inside the crash window, concurrent writers (Phase B), and server-mode engines. Gate 2 remains Day 60.
