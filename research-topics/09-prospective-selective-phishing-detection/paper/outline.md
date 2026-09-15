# Paper outline — Topic 09

**Working title.** Prospective Selective Phishing Detection Under Campaign, Source, and Collection Shift

**Primary target.** IEEE Transactions on Information Forensics and Security (TIFS)  
**Secondary target.** ACM Transactions on Privacy and Security (TOPS)

**One-sentence contribution.**
> Campaign-grouped and source-held-out evaluation reveals deployment error hidden by standard splits, while selective prediction and drift-triggered maintenance can preserve precision under a fixed review budget.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. How much of reported phishing-detector performance is optimism from random splits, source artifacts, and ignored label delay, measured on an 18-month timestamped multi-source corpus?
   - RQ2. Under a fixed review budget, does a calibrated reject option combined with a cheap drift trigger maintain precision over an expanding-window prospective replay better than periodic retraining and no maintenance?
   - RQ3. Which benign site classes and sources dominate false positives in prospective operation?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Source-held-out evaluation lowers precision at a fixed FPR by a substantial, preregistered margin relative to random splits.
- H2. Label-delay simulation shifts effective training data by weeks and measurably reduces early-campaign recall.
- H3. Selective prediction with drift-triggered retraining keeps selective risk within budget while periodic retraining alone does not.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
