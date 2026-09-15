# Paper outline — Topic 07

**Working title.** Risk-Calibrated Streaming Entity Resolution Under Hard Byte and Latency Budgets

**Primary target.** IEEE Transactions on Knowledge and Data Engineering (TKDE)  
**Secondary target.** Data Mining and Knowledge Discovery (DMKD)

**One-sentence contribution.**
> A cache policy based on future disambiguation value, combined with calibrated selective matching, can reduce expected false-match cost under hard state and latency budgets.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. Given byte-level state, per-record latency, false-match cost, abstention cost, and correction delay, what retention policy minimizes expected cost, and how does it differ from recency, frequency, reservoir, and uncertainty-only caches?
   - RQ2. Can calibrated or conformal selective matching keep coverage guarantees under drift without assuming exchangeability, when recalibrated in windows, and how does coverage vary with entity frequency?
   - RQ3. Across ≥ 6 chronologically replayed datasets with burstiness, new-entity arrival, duplication changes, and missing-attribute drift, where does the joint policy sit on the Pareto frontier of accuracy, coverage, correction delay, throughput, and serialized state bytes?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. A retention score combining ambiguity, representativeness, novelty, and expected future use dominates single-signal caches at equal serialized bytes.
- H2. Windowed recalibration keeps selective risk within target on frequent entities but under-covers rare entities; reporting coverage conditional on entity frequency exposes this.
- H3. The joint policy achieves lower false-match cost than the full-memory upper bound's cost plus a small margin at a fraction of state bytes.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
