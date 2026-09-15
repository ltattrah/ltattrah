# Paper outline — Topic 04

**Working title.** Detectability-Preserving Adaptive Flow Sampling for Rare Network Attacks Under Fixed Telemetry Budgets

**Primary target.** IEEE Transactions on Network and Service Management (TNSM)  
**Secondary target.** IEEE Transactions on Dependable and Secure Computing (TDSC)

**One-sentence contribution.**
> A rarity- and uncertainty-aware sampler with recorded inclusion probabilities can preserve detectability of sparse attacks and support corrected estimates at the same telemetry cost as uniform sampling.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. At equal byte and record budgets, does the adaptive sampler retain more attack evidence (per-attack recall, detection delay) than uniform packet, uniform flow, hash-based, sample-and-hold, heavy-hitter, and active-uncertainty baselines?
   - RQ2. When are inverse-probability-corrected prevalence estimators stable under adaptive sampling, and what is the detectability bound (or controlled empirical approximation) as a function of budget and attack rarity?
   - RQ3. Does the detectability gain transfer across chronologically partitioned datasets and survive mislabeled or duplicated flows?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Adaptive sampling improves per-attack recall for the rarest attack classes at equal budget with no worse false positives per hour.
- H2. Corrected prevalence estimates have bounded bias when minimum inclusion probability is floored; unfloored adaptive sampling produces unstable estimates.
- H3. Gains persist on a dataset not used for design, and degrade gracefully under injected label noise and duplicate flows.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
