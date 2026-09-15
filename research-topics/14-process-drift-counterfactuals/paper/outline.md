# Paper outline — Topic 14

**Working title.** From Process Drift Alerts to Action: Counterfactual Explanations for Operational Diagnosis

**Primary target.** Information Systems  
**Secondary target.** Decision Support Systems (DSS)

**One-sentence contribution.**
> Counterfactual process explanations that identify the smallest actionable changes needed to restore a target outcome improve analyst diagnosis compared with alert-only and feature-importance explanations.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. Can counterfactuals over resource, control-flow, timing, and outcome perspectives be generated under process-feasibility constraints with acceptable fidelity and stability on controlled and natural drift?
   - RQ2. Do counterfactual explanations improve analyst diagnosis accuracy, intervention selection, and time, and reduce inappropriate actions, relative to alert-only, before/after diagrams, feature ranking, and existing explainable-drift output?
   - RQ3. Which drift types (seasonality, case mix, workload, structural change) are diagnosed better, and where do counterfactuals mislead?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Constrained counterfactuals achieve higher fidelity and stability than unconstrained ones at a modest sparsity cost.
- H2. Analysts with counterfactuals select the correct intervention more often and take fewer inappropriate actions than with feature ranking.
- H3. Gains are largest for structural process change and smallest for seasonality, where counterfactuals may suggest spurious interventions.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
