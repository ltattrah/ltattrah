# Paper outline — Topic 06

**Working title.** Metamorphic Testing of Vector SQL and Hybrid Search Semantics Across Database Engines

**Primary target.** ACM Transactions on Database Systems (TODS)  
**Secondary target.** The VLDB Journal

**One-sentence contribution.**
> Feature-aware metamorphic relations can expose wrong-result and consistency defects in vector SQL and hybrid search that cross-engine comparison alone cannot classify reliably.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. What is the common semantics, and what are the documented deviations, of vector distance, normalization, top-k, filters, ties, nulls, metadata updates, deletes, and exact vs approximate modes across ≥ 4 local engines?
   - RQ2. Which metamorphic relations (monotonic filtering, distance-preserving transforms, exact-index equivalence, insertion/deletion consistency) detect defects, and how does each compare with cross-engine differential testing in precision (true bug vs documented difference)?
   - RQ3. How many confirmed wrong-result and consistency bugs does the oracle find, and what do reducer ablations show about each generator and oracle component?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Cross-engine differential testing alone classifies most discrepancies as "documented semantics" or "approximation", giving low precision for bugs.
- H2. Feature-aware metamorphic relations combined with exact small-data oracles yield a higher confirmed-bug rate per test at equal test budget.
- H3. Mutation-history relations (insert/update/delete then query) find a distinct bug class not reachable by static query relations.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
