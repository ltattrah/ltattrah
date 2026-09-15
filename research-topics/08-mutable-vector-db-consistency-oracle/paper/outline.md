# Paper outline — Topic 08

**Working title.** Beyond Static Recall: A Black-Box Consistency and Freshness Oracle for Mutable Vector Databases

**Primary target.** The VLDB Journal  
**Secondary target.** ACM Transactions on Database Systems (TODS)

**One-sentence contribution.**
> Version-tagged operation histories and snapshot-exact oracles can classify mutable vector search failures independently of approximation tolerance and reduce them to developer-useful histories.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. What observable contracts do mutable vector databases advertise (or leave undocumented) for visibility, versioning, deletion, filters, durability, and recovery, and can they be expressed in one engine-independent model?
   - RQ2. Given a deterministic version-tagged history and exact neighbor sets at checkpoints, can discrepancies be classified into the six failure classes with high precision, independent of the engine's approximation tolerance?
   - RQ3. How prevalent are each class of failure across ≥ 4 engines, three mutation intensities, sequential and concurrent histories, and restarts; and can the reducer minimize failing histories to developer-actionable size?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Approximation accounts for most discrepancies at low mutation intensity, while stale-version and ghost results grow with mutation intensity and compaction.
- H2. Classification precision (against ground truth from the logical snapshot) exceeds a preregistered threshold for every class except visibility lag, whose boundary with approximation depends on stated consistency windows.
- H3. At least one engine exhibits a reproducible contract violation (ghost deletion, filter inconsistency, or durability loss after restart) that is independently reproducible from a minimized history.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
