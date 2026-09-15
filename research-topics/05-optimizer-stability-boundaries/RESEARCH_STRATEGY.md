# Topic 05 — Learning Query Optimizer Stability Boundaries Under Continuous Skew and Correlation Drift

**Area:** Databases
**Original topic:** Query Plan Instability Under Data Skew and Correlation Drift

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 68 |
| Upgraded potential | 88 |
| Priority | High |
| Decision | Retain and formalize |
| Laptop fit | Excellent |
| Primary journal | The VLDB Journal |
| Secondary journal | ACM Transactions on Database Systems (TODS) |
| Main risk | Descriptive engine comparison |
| Portfolio order | 4 of 6 (low-risk backup) |

**Audit verdict.** A strong journal topic. Lead with stability boundaries and the guard, not with an engine ranking.

## 1. Objective

Define query plan **stability regions** in a continuous distribution space (skew, correlation, selectivity, statistics age), map their boundaries with adaptive search, show that boundary quantities transfer across engines, and build a low-overhead **guard** that flags high-regret plan transitions before a latency cliff.

## 2. Why the original framing fails

Optimizer errors under skew and correlation are well known; drift-aware benchmarking is emerging. A list of slow queries on three engines is descriptive. The topic becomes journal-worthy only with a **new stability object**, **systematic boundary mapping**, and a **mitigation**.

## 3. Defensible contribution

> Query plans have measurable stability regions in a continuous distribution space. Boundary-aware monitoring can identify high-regret plan transitions before a severe latency cliff occurs.

## 4. Research questions and hypotheses

- **RQ1.** For a fixed query template, how do plan choice and latency vary along continuous paths of Zipf skew, pairwise and higher-order correlation, selectivity, and statistics age, and where are the plan transitions?
- **RQ2.** Are stability region, boundary distance, cliff magnitude, and worst-case regret consistent in structure across PostgreSQL, DuckDB, and a third engine, even when absolute values differ?
- **RQ3.** Can a guard that monitors boundary distance trigger selective reoptimization, sampling, or plan alternatives with overhead and false-alarm rate lower than the regret it avoids?

Hypotheses:

- **H1.** Plan transitions cluster near a small number of boundaries in the distribution space; most of the space is stable.
- **H2.** Cliff magnitude is dominated by cardinality misestimation on correlated predicates, and the *location* of correlation-driven boundaries transfers across engines better than skew-driven boundaries.
- **H3.** The guard reduces worst-case regret on held-out real-data drift paths at an overhead below a preregistered fraction of query latency.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Cardinality estimation benchmarks (JOB, CEB) | Static workloads expose estimation error | Static; no continuous drift paths or stability object |
| Plan diagram / parametric query optimization | Plan choice over selectivity space | Two-parameter selectivity space; here skew, correlation, statistics age; plus a guard |
| Adaptive and re-optimization techniques | Re-plan on runtime feedback | Reactive; the guard is proactive from boundary distance |
| Drift-aware benchmarking (emerging) | Workloads under drift | No stability regions or regret formalization |
| Learned cardinality estimators | Reduce estimation error | Orthogonal; the guard works with any estimator |

## 6. Study design

### Phase A — Distribution space and data generator (Days 1–25)
1. Define the space: Zipf exponent per column, pairwise correlation, one higher-order correlation, selectivity of key predicates, statistics age (rows changed since ANALYZE).
2. Python generator emits data along **continuous paths** through the space; calibrate selected paths from public real datasets (for example IMDB, TPC-DS-derived skew profiles).
3. Query templates: ≥ 20, covering joins, group-bys, and filter chains that are known to be sensitive.

### Phase B — Measurement and boundary search (Days 20–55)
1. Capture per point: plan structure (hash), estimated vs actual cardinalities, operator cost, memory spill, compilation time, latency.
2. Adaptive boundary search (bisection along paths, then local refinement) rather than a dense grid.
3. Multiple data scales; fresh and stale statistics.

### Phase C — Stability formalization and transfer (Days 45–70)
1. Definitions: **stability region** (connected set with the same plan and latency within a tolerance), **boundary distance** (from current state to nearest transition), **cliff magnitude** (latency ratio across a transition), **worst-case regret** (best plan latency vs chosen plan latency).
2. Test transfer of these quantities across PostgreSQL, DuckDB, and one additional engine (for example SQLite or MySQL).

### Phase D — Guard (Days 60–90)
1. Implement a low-overhead guard outside the engine: track distribution statistics incrementally, estimate boundary distance, trigger selective reoptimization (re-ANALYZE, hint alternative, sampling) near a boundary.
2. Evaluate overhead, false alarms, regret avoided on two real-data validations.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Query templates | ≥ 20 |
| Data scales | Multiple |
| Engines | 3 |
| Statistics | Fresh and stale |
| Real-data validations | 2 |
| Metrics | Stability region size, boundary distance, cliff magnitude, worst-case regret, guard overhead, false-alarm rate, regret avoided, cost of detecting a boundary |

## 8. Artifact and tooling plan

- Python data generator (`numpy` copulas for correlation, Zipf sampling), loader per engine, plan capture via `EXPLAIN (ANALYZE, FORMAT JSON)` and DuckDB `EXPLAIN ANALYZE`.
- Boundary search and stability computation in Python; guard as a Python sidecar process.
- Engines pinned in containers; record versions and configuration.
- One-command reproduction on one template and one path.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Synthetic paths do not resemble production drift | Calibrate paths from real datasets; two real-data validations |
| Engine differences prevent a shared causal explanation | Report transfer of *structure* (boundary locations, cliff causes) separately from absolute values; instrument cardinality errors as the explanatory variable |
| The guard costs more than it saves | Report overhead and regret avoided on the same axis; include false alarms |
| Product ranking creeps in | Never present engine leaderboards; engines are replicates of the phenomenon |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 55).** No boundary structure beyond trivial selectivity switches → stop.
- **Gate 2 (Day 70).** No transferable boundary quantity across engines → reframe as single-engine study for a workshop; do not submit to VLDBJ.
- **Stop.** No transferable stability boundary or useful guard.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on cardinality estimation, plan diagrams, re-optimization, drift benchmarking; reproduce one known correlation-induced misestimate |
| Days 15–30 | Freeze space definition, templates, definitions, engines, metrics, stop conditions; generator and capture working on 2 templates |
| Days 31–60 | Pilot on 6 templates across 2 engines; variance and runtime; hardest engine; one real-data path |
| Days 61–90 | Full preregistered mapping; guard evaluation; second real-data validation; package; draft |

## 12. Journal strategy

- **The VLDB Journal** for benchmark plus mitigation with archival systems depth.
- **TODS** when the stability definitions and optimizer analysis are technically deep and the guard is secondary.

## 13. Ethics and disclosure

No human subjects. Public datasets under license. Report engine misbehavior (for example crashes found during mapping) to maintainers.

## 14. Folder layout

```
05-optimizer-stability-boundaries/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     generator/, templates/, capture/, boundary-search/, guard/, runs/, analysis/
└── paper/
```
