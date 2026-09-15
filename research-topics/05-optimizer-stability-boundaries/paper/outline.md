# Paper outline — Topic 05

**Working title.** Learning Query Optimizer Stability Boundaries Under Continuous Skew and Correlation Drift

**Primary target.** The VLDB Journal  
**Secondary target.** ACM Transactions on Database Systems (TODS)

**One-sentence contribution.**
> Query plans have measurable stability regions in a continuous distribution space. Boundary-aware monitoring can identify high-regret plan transitions before a severe latency cliff occurs.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. For a fixed query template, how do plan choice and latency vary along continuous paths of Zipf skew, pairwise and higher-order correlation, selectivity, and statistics age, and where are the plan transitions?
   - RQ2. Are stability region, boundary distance, cliff magnitude, and worst-case regret consistent in structure across PostgreSQL, DuckDB, and a third engine, even when absolute values differ?
   - RQ3. Can a guard that monitors boundary distance trigger selective reoptimization, sampling, or plan alternatives with overhead and false-alarm rate lower than the regret it avoids?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Plan transitions cluster near a small number of boundaries in the distribution space; most of the space is stable.
- H2. Cliff magnitude is dominated by cardinality misestimation on correlated predicates, and the *location* of correlation-driven boundaries transfers across engines better than skew-driven boundaries.
- H3. The guard reduces worst-case regret on held-out real-data drift paths at an overhead below a preregistered fraction of query latency.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
