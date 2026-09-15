# Topic 06 — Metamorphic Testing of Vector SQL and Hybrid Search Semantics Across Database Engines

**Area:** Databases
**Original topic:** Differential Testing of SQL Engines for Semantic Inconsistencies

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 71 |
| Upgraded potential | 92 |
| Priority | Very high |
| Decision | Narrow to emerging semantics |
| Laptop fit | Excellent |
| Primary journal | ACM Transactions on Database Systems (TODS) |
| Secondary journal | The VLDB Journal |
| Main risk | Generic differential testing is established |
| Portfolio order | 2 of 6 |

**Audit verdict.** A top-three recommendation. Target vector and hybrid query semantics and make confirmed logic bugs the validation of a general oracle contribution.

## 1. Objective

Build a **feature-aware metamorphic testing oracle** for vector SQL and hybrid search (vector distance plus filters, top-k, ties, nulls, metadata updates, deletes, exact vs approximate modes) and show that it exposes wrong-result and consistency defects that cross-engine comparison alone cannot classify. Validation is developer-confirmed bugs across ≥ 4 engines.

## 2. Why the original framing fails

SQLancer, query partitioning (Rigger and Su [20]), and SQLxDiff [21] already establish differential and metamorphic testing for logic bugs. A generic SQL fuzzer will not clear the novelty bar. Vector SQL and hybrid search are an emerging target where engines differ in distance functions, normalization, top-k semantics, ties, null handling, approximate indexes, and mutation visibility, so plain cross-engine comparison produces unclassifiable differences.

## 3. Defensible contribution

> Feature-aware metamorphic relations can expose wrong-result and consistency defects in vector SQL and hybrid search that cross-engine comparison alone cannot classify reliably.

## 4. Research questions and hypotheses

- **RQ1.** What is the common semantics, and what are the documented deviations, of vector distance, normalization, top-k, filters, ties, nulls, metadata updates, deletes, and exact vs approximate modes across ≥ 4 local engines?
- **RQ2.** Which metamorphic relations (monotonic filtering, distance-preserving transforms, exact-index equivalence, insertion/deletion consistency) detect defects, and how does each compare with cross-engine differential testing in precision (true bug vs documented difference)?
- **RQ3.** How many confirmed wrong-result and consistency bugs does the oracle find, and what do reducer ablations show about each generator and oracle component?

Hypotheses:

- **H1.** Cross-engine differential testing alone classifies most discrepancies as "documented semantics" or "approximation", giving low precision for bugs.
- **H2.** Feature-aware metamorphic relations combined with exact small-data oracles yield a higher confirmed-bug rate per test at equal test budget.
- **H3.** Mutation-history relations (insert/update/delete then query) find a distinct bug class not reachable by static query relations.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| SQLancer [19] | Automatic DBMS testing with several oracles | Relational SQL; no vector or hybrid semantics |
| Query partitioning [20] | Metamorphic oracle for SQL | Partition relations on relational predicates; here relations are over distance, top-k, ties, approximate modes |
| SQLxDiff [21] | Differential testing in emerging databases | Differential; this paper argues differential alone is insufficient for vector semantics |
| ANN benchmark suites | Recall/latency of vector indexes | Performance, not correctness under filters and mutations |
| Vector DB conformance tests (vendor) | Product-specific | Cross-engine, semantics-first |

## 6. Study design

### Phase A — Semantics specification (Days 1–25)
1. Write a semantics document: for each feature, the common expectation and each engine's documented deviation (with citations to docs and versions).
2. Engines (≥ 4 local): for example pgvector, DuckDB VSS, SQLite-vec, Chroma/LanceDB/Qdrant-embedded, Milvus Lite. Pin versions.

### Phase B — Generators and oracles (Days 15–50)
1. Python generator: typed schemas, vectors (varied dimension, normalization, duplicates, nulls), filters, and **query histories** (insert, upsert, delete, index rebuild interleaved with queries).
2. Oracles: exact small-data reference (brute-force top-k in `numpy` with explicit tie and null rules) plus metamorphic relations: monotonic filtering (adding a conjunct cannot add results), distance-preserving transforms (rotation, translation for L2; scaling for cosine), exact-index equivalence (exact mode result set equals reference), history consistency (delete then query never returns deleted id).
3. Validity filtering so only engine-valid queries are counted.

### Phase C — Testing campaign and reduction (Days 40–75)
1. Run millions of valid tests across engines; store failing cases with full history.
2. Reducer minimizes across query, schema, data, index parameters, and mutation history; report reduction ratios.
3. Classify: standard/documented deviation vs implementation defect vs approximation tolerance.

### Phase D — Reporting and ablation (Days 65–90)
1. Submit minimized reports; track confirmation and fixes.
2. Ablate every generator and oracle component; report bugs found per component and per test budget.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Valid tests | Millions |
| Engines | ≥ 4 |
| Validity filtering | Strong, with rejection statistics |
| Reduction ratios | High, reported |
| Confirmed bugs | Developer-confirmed wrong-result bugs |
| Artifact | Reproduce each confirmed defect with one command |
| Baseline | Cross-engine differential testing at equal budget |

## 8. Artifact and tooling plan

- Python harness with engine adapters (`psycopg`, `duckdb`, `sqlite3`, vendor clients); `hypothesis` for structured generation and shrinking of schemas and histories; own reducer for cross-dimension minimization.
- Exact reference oracle in `numpy` with explicit tie-breaking and null semantics defined in the spec document.
- Each failing test stored as a self-contained JSON history; `python -m experiments.reproduce --bug <id>` replays it.
- Engines pinned in containers; results keyed by engine version.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Differences reflect documented semantics rather than bugs | Semantics document written first; classifier separates deviation from defect; report both counts |
| Approximate search error mistaken for wrong result | Exact mode and exact small-data oracles for correctness claims; approximate mode tested only with relations that hold under approximation (for example deleted ids never returned) |
| Low confirmed-bug count exposes weak oracle | Gate 2 below; ablations show which components carry the weight |
| Reduction produces engine-invalid cases | Validity check inside the reducer loop |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 25).** Fewer than 4 engines runnable locally with mutation support → stop or substitute.
- **Gate 2 (Day 60).** Oracle produces mostly documented differences or false positives after the pilot campaign → stop (portfolio stop condition).

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on DBMS testing and vector search semantics; reproduce one SQLancer-found bug class; verify engine access |
| Days 15–30 | Freeze semantics document, relation set, validity rules, engines, metrics, stop conditions; small deterministic generator |
| Days 31–60 | Pilot campaign (≈ 100k tests per engine); estimate failure prevalence and runtime; hardest engine; first reports |
| Days 61–90 | Full campaign; reducer and ablations; confirmation tracking; package; draft |

## 12. Journal strategy

- **TODS** for the semantic oracle and correctness analysis (lead with the semantics model and relations).
- **The VLDB Journal** if the system, empirical findings, and implications for emerging database architectures dominate.

## 13. Ethics and disclosure

Responsible disclosure to maintainers before publication; no public naming of unconfirmed defects. No human subjects.

## 14. Folder layout

```
06-vector-sql-metamorphic-testing/
├── RESEARCH_STRATEGY.md
├── literature/      closest-work.md, semantics-spec.md
├── experiments/     adapters/, generator/, oracles/, reducer/, campaigns/, bugs/ (minimized histories), analysis/
└── paper/
```
