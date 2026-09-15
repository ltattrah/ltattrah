# Topic 08 — Beyond Static Recall: A Black-Box Consistency and Freshness Oracle for Mutable Vector Databases

**Area:** Databases
**Original topic:** Consistency and Freshness Failures in Vector Databases Under Incremental Updates

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 77 |
| Upgraded potential | 94 |
| Priority | Highest |
| Decision | Retain and sharpen semantics |
| Laptop fit | Excellent |
| Primary journal | The VLDB Journal |
| Secondary journal | ACM Transactions on Database Systems (TODS) |
| Main risk | Approximation confused with staleness |
| Portfolio order | 1 of 6 (recommended primary for databases) |

**Audit verdict.** The strongest topic in the portfolio. Freeze engine versions, make the semantic model independent of product names, and treat confirmed anomalies as evidence for the oracle rather than the only contribution.

## 1. Objective

Define a **system-independent semantic model** of mutable vector search (insert visibility, read-your-write, version replacement, delete safety, metadata filter consistency, durability, restart recovery) and a **black-box oracle** that, from version-tagged operation histories and snapshot-exact reference computations, classifies each discrepancy as approximation, stale version, ghost result, visibility lag, filter inconsistency, or durability loss. Validate on ≥ 4 engines with a history reducer.

## 2. Why the original framing fails

Dynamic vector search moves fast: SPFresh [24] handles update-intensive search and recent work formalizes dynamic consistency for quantization under streaming updates [25]. A product comparison ages quickly. The defensible contribution is the semantic model plus an oracle that separates acceptable approximation from real contract violations.

## 3. Defensible contribution

> Version-tagged operation histories and snapshot-exact oracles can classify mutable vector search failures independently of approximation tolerance and reduce them to developer-useful histories.

## 4. Research questions and hypotheses

- **RQ1.** What observable contracts do mutable vector databases advertise (or leave undocumented) for visibility, versioning, deletion, filters, durability, and recovery, and can they be expressed in one engine-independent model?
- **RQ2.** Given a deterministic version-tagged history and exact neighbor sets at checkpoints, can discrepancies be classified into the six failure classes with high precision, independent of the engine's approximation tolerance?
- **RQ3.** How prevalent are each class of failure across ≥ 4 engines, three mutation intensities, sequential and concurrent histories, and restarts; and can the reducer minimize failing histories to developer-actionable size?

Hypotheses:

- **H1.** Approximation accounts for most discrepancies at low mutation intensity, while stale-version and ghost results grow with mutation intensity and compaction.
- **H2.** Classification precision (against ground truth from the logical snapshot) exceeds a preregistered threshold for every class except visibility lag, whose boundary with approximation depends on stated consistency windows.
- **H3.** At least one engine exhibits a reproducible contract violation (ghost deletion, filter inconsistency, or durability loss after restart) that is independently reproducible from a minimized history.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| SPFresh [24] | In-place updates for billion-scale search | System; no black-box correctness oracle |
| Quantization under streaming updates [25] | Formalizes consistency for a specific technique | Technique-level; this model is engine-independent and black-box |
| ANN benchmarks (ann-benchmarks, big-ann) | Static recall and latency | No mutations, versions, deletes, or restarts |
| Jepsen-style consistency testing | Histories and linearizability checkers for KV/SQL | Adapted to approximate top-k where exact equality is not the contract |
| Vector DB vendor consistency docs | Product-specific contracts | Treated as claims to test |

## 6. Study design

### Phase A — Semantic model (Days 1–25)
1. Define contracts formally: insert visibility (bounded lag), read-your-write, version replacement (upsert replaces, old vector never returned), delete safety (no ghost results after acknowledgement), metadata filter consistency (results satisfy filter at snapshot), durability, restart recovery.
2. Record, per engine and version, which contracts are advertised, weakened, or undocumented.

### Phase B — History generator and exact oracle (Days 15–50)
1. Python generator produces deterministic histories: version-tagged vectors and metadata; interleaved query, insert, upsert, delete, rebuild, compaction, crash/restart events; sequential and concurrent (with recorded scheduling) modes.
2. At checkpoints compute exact neighbor sets for the logical snapshot (brute force in `numpy`/`faiss` flat index) with explicit tie rules.
3. Classifier maps each discrepancy to: approximation (within tolerance and all returned ids are live and version-correct), stale version, ghost result, visibility lag, filter inconsistency, durability loss.

### Phase C — Campaign (Days 40–75)
1. ≥ 4 engines pinned in containers; 100k–1M vectors for most tests; three mutation intensities; restarts.
2. Reducer minimizes failing histories (delta debugging over operations while preserving the classified failure).
3. Report confirmed defects and contract ambiguities separately.

### Phase D — Disclosure and ablation (Days 65–90)
1. Report to maintainers; track confirmations.
2. Ablate checkpoint density, tolerance settings, and history features; measure oracle cost.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Vectors | 100k–1M for most tests |
| Engines | ≥ 4 |
| Mutation intensities | 3 |
| History modes | Sequential and concurrent |
| Restarts | Included |
| Checkpoints | Exact |
| Evidence | Developer confirmation or independently reproducible contract violations |
| Baseline | Static recall measurement (shows what it misses) |

## 8. Artifact and tooling plan

- Python harness with engine adapters (for example pgvector, Qdrant, Milvus Lite, Weaviate embedded, Chroma, LanceDB); adapters are thin so releases do not invalidate the model.
- Exact oracle with `numpy` and `faiss` flat indexes; deterministic scheduling for concurrent histories via a recorded interleaving log.
- Histories stored as JSON; `python -m experiments.reproduce --history <id>` replays and re-classifies.
- Container images pinned by digest; restart events implemented via container stop/start.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Engine contracts undocumented or intentionally weak | Report ambiguities as a first-class finding; classify against the *advertised* contract and against the strict model separately |
| Concurrent histories hard to reproduce | Record interleavings; use deterministic schedulers where the client allows; fall back to sequential reproduction of the same failure |
| Frequent releases invalidate adapters | Thin adapters, pinned digests, results keyed by version; re-run smoke tests on latest before submission |
| Approximation confused with staleness | Exact snapshot oracle plus version tags make the distinction observable |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 25).** Fewer than 4 engines with mutation, filter, and restart support runnable locally → substitute or stop.
- **Gate 2 (Day 60).** No reproducible semantic anomaly after four engines and stress histories → stop (portfolio stop condition); move to Topic 06.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on dynamic ANN, consistency testing, vector DB internals; reproduce one static recall result to anchor tolerance settings |
| Days 15–30 | Freeze the semantic model, failure classes, generator, checkpoint scheme, engines, stop conditions; small deterministic artifact |
| Days 31–60 | Pilot at 100k vectors on 2 engines; failure prevalence, runtime, storage; hardest engine; one concurrent-history transfer |
| Days 61–90 | Full preregistered campaign; reducer; disclosure; package; draft around RQ1–RQ3 |

## 12. Journal strategy

- **The VLDB Journal** as primary (archival work on database architectures and novel system applications); lead with the model and oracle, then prevalence.
- **TODS** if the semantic model and oracle are developed with formal rigor and the empirical campaign is secondary.

## 13. Ethics and disclosure

Responsible disclosure to each engine's maintainers before publication; anonymize engines in drafts until confirmation or a fixed disclosure window elapses. No human subjects.

## 14. Folder layout

```
08-mutable-vector-db-consistency-oracle/
├── RESEARCH_STRATEGY.md
├── literature/      closest-work.md, contracts-by-engine.md
├── experiments/     model/, adapters/, generator/, oracle/, reducer/, campaigns/, histories/ (minimized), analysis/
└── paper/
```
