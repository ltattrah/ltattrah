# Topic 07 — Risk-Calibrated Streaming Entity Resolution Under Hard Byte and Latency Budgets

**Area:** Databases
**Original topic:** Memory-Bounded Streaming Entity Resolution with Calibrated Abstention

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 60 |
| Upgraded potential | 82 |
| Priority | Medium |
| Decision | Formalize the resource problem |
| Laptop fit | Good |
| Primary journal | IEEE Transactions on Knowledge and Data Engineering (TKDE) |
| Secondary journal | Data Mining and Knowledge Discovery (DMKD) |
| Main risk | Abstention appears appended |
| Portfolio order | Not in top six |

**Audit verdict.** Viable after a formal resource-constrained formulation. If theory and six credible streams are not feasible, select Topic 05 or 06 instead.

## 1. Objective

Formulate streaming entity resolution as a **joint decision problem** in which cache retention, candidate generation, matching, abstention, and delayed correction are optimized under hard byte, latency, and false-match cost constraints. Show that a retention policy based on **future disambiguation value**, combined with calibrated selective matching, reduces expected false-match cost at equal budgets.

## 2. Why the original framing fails

Streaming and progressive entity resolution have foundations (Lian et al. [22], Gazzarri et al. [23]). Adding a confidence threshold to an existing matcher is incremental. The contribution must be the joint formulation and a cache policy that is *derived* from it.

## 3. Defensible contribution

> A cache policy based on future disambiguation value, combined with calibrated selective matching, can reduce expected false-match cost under hard state and latency budgets.

## 4. Research questions and hypotheses

- **RQ1.** Given byte-level state, per-record latency, false-match cost, abstention cost, and correction delay, what retention policy minimizes expected cost, and how does it differ from recency, frequency, reservoir, and uncertainty-only caches?
- **RQ2.** Can calibrated or conformal selective matching keep coverage guarantees under drift without assuming exchangeability, when recalibrated in windows, and how does coverage vary with entity frequency?
- **RQ3.** Across ≥ 6 chronologically replayed datasets with burstiness, new-entity arrival, duplication changes, and missing-attribute drift, where does the joint policy sit on the Pareto frontier of accuracy, coverage, correction delay, throughput, and serialized state bytes?

Hypotheses:

- **H1.** A retention score combining ambiguity, representativeness, novelty, and expected future use dominates single-signal caches at equal serialized bytes.
- **H2.** Windowed recalibration keeps selective risk within target on frequent entities but under-covers rare entities; reporting coverage conditional on entity frequency exposes this.
- **H3.** The joint policy achieves lower false-match cost than the full-memory upper bound's cost plus a small margin at a fraction of state bytes.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Lian et al. [22] | Online topic-aware ER over incomplete streams | No hard byte budget or abstention |
| Gazzarri et al. [23] | Progressive ER over incremental data | Prioritizes comparisons; no joint retention-abstention decision |
| Selective prediction / conformal classification | Abstention with coverage guarantees | Applied under drift and hard state budgets; coverage conditional on frequency |
| Cache replacement (LRU, LFU, learned caches) | Retention by access patterns | Retention by *disambiguation value* |
| Blocking and candidate generation for streams | Candidate pruning | Reused as a component |

## 6. Study design

### Phase A — Formal problem (Days 1–30)
1. Define state as serialized bytes (not process RSS), per-record latency budget, false-match cost, abstention cost, correction delay cost.
2. Write the objective as a constrained or transparent multi-objective problem; derive the retention score as its greedy approximation; state assumptions.

### Phase B — Policy and selective matcher (Days 20–50)
1. Retention score: ambiguity (entropy over candidate matches), representativeness (cluster coverage), novelty, expected future use (arrival-rate estimate).
2. Selective matching with windowed calibration or conformal thresholds; explicit handling of non-exchangeability (weighted or adaptive conformal).

### Phase C — Replay evaluation (Days 40–80)
1. ≥ 6 datasets replayed in chronological order; inject burstiness, new entities, duplication-rate changes, missing-attribute drift where the data lack them.
2. Baselines: recency, frequency, reservoir, uncertainty-only caches; threshold-only abstention; full-memory upper bound.
3. Equal-memory and equal-latency comparisons.

### Phase D — Frontiers and analysis (Days 70–90)
1. Pareto frontiers over accuracy, accepted coverage, correction delay, throughput, serialized bytes.
2. Ablate each retention signal.

## 7. Baselines, metrics, and minimum evidence

| Metric | Note |
|---|---|
| Precision, recall, F1 on accepted decisions | Plus accepted coverage |
| Selective risk and coverage | Conditional on entity frequency |
| Correction delay | Time from wrong decision to correction |
| Throughput and p99 latency | Per record |
| Serialized state bytes | The memory measure; never process-level RSS |
| Full-memory upper bound | Always included |

## 8. Artifact and tooling plan

- Python streaming harness (`pandas` replay, `numpy`/`scikit-learn` matchers, own cache and conformal modules); serialization via `pickle` or `msgpack` measured in bytes.
- Dataset manifests with hashes and the chronological ordering rule per dataset.
- One-command reproduction on one dataset at one budget.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Small static benchmarks do not stress the cache | Chronological replay with injected drift; ≥ 6 streams; report budget where policies diverge |
| Selective prediction raises precision trivially by rejecting most records | Report coverage beside precision; Pareto frontiers; abstention cost in the objective |
| Process-level memory is ambiguous | Serialized bytes only |
| Abstention looks appended | Derive it from the objective; ablate it |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 30).** No clean formal objective yielding a non-trivial retention score → stop; move to Topic 05 or 06.
- **Gate 2 (Day 50).** Fewer than 6 credible chronologically ordered streams → stop.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on streaming/progressive ER, selective prediction, caches; reproduce one progressive ER baseline |
| Days 15–30 | Freeze formulation, retention score, calibration scheme, datasets, budgets, metrics, stop conditions; small deterministic harness |
| Days 31–60 | Pilot on 2 datasets and 3 budgets; variance and throughput; hardest baseline; one drift-injection transfer test |
| Days 61–90 | Preregistered replay on all datasets; frontiers and ablations; package; draft |

## 12. Journal strategy

- **TKDE** for a scalable data-management-plus-learning contribution.
- **DMKD** for a principled uncertainty and streaming method with broad predictive relevance.

## 13. Ethics and disclosure

Use only datasets with clear licenses; if person records are involved, use anonymized or synthetic variants.

## 14. Folder layout

```
07-risk-calibrated-streaming-entity-resolution/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     formulation/ (notes, derivations), policy/, matcher/, replay/, datasets/ (manifests), runs/, analysis/
└── paper/
```
