# Paper outline — Topic 11

**Working title.** Early Warning of Software Supply Chain Incidents with Positive-Unlabeled Temporal Risk Models

**Primary target.** IEEE Transactions on Dependable and Secure Computing (TDSC)  
**Secondary target.** IEEE Transactions on Information Forensics and Security (TIFS)

**One-sentence contribution.**
> Positive-unlabeled temporal models can estimate review priority and incident lead time without treating every unlabeled package as benign or publishing accusatory package scores.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. Reconstructing monthly ecosystem snapshots and incident labels *as known at each date*, what lead time do ownership churn, release anomalies, dependency reach, provenance indicators, maintenance activity, and name confusion provide before documented incidents?
   - RQ2. Under a fixed analyst review budget, how do PU and survival models compare with naive supervised classification in incidents caught, lead time, calibration, and false-accusation risk?
   - RQ3. How sensitive are conclusions to label incompleteness and selective reporting, and which package subgroups bear higher error?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Treating unlabeled packages as benign underestimates risk prevalence and inflates apparent precision; PU estimation corrects this by a measurable margin.
- H2. Ownership churn and name confusion carry the most lead time; release anomalies carry the least (they often coincide with the incident).
- H3. Expanding-window evaluation shows lead time is stable across years only for a subset of features.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
