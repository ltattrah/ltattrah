# Paper outline — Topic 02

**Working title.** Safety-Constrained Online Controller Selection for Intermittent and Asymmetric Access Networks

**Primary target.** IEEE/ACM Transactions on Networking (ToN)  
**Secondary target.** IEEE Transactions on Mobile Computing (TMC)

**One-sentence contribution.**
> A conservative online selector can adapt across intermittent and asymmetric regimes while bounding excess delay and loss relative to a safe controller and retaining performance on unseen traces.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. Under what regime definition (outage duration, asymmetry ratio, reverse-path congestion level) do fixed controllers (CUBIC, BBR, delay-based) each fail, and is any single controller safe across all regimes?
   - RQ2. Can a conservative bandit (conservative LinUCB or constrained Thompson sampling with fallback) keep excess delay and loss within a stated budget relative to the safe controller, with a regret bound under stated assumptions or a falsifiable empirical bound?
   - RQ3. Does the safety guarantee hold on trace families never seen during tuning and in a Linux prototype rather than only in simulation?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. No fixed controller is within the safety budget in every regime (motivates selection).
- H2. The conservative selector violates the safety budget in fewer than a preregistered fraction of episodes, versus a substantially higher fraction for an unconstrained bandit and a rule-based switcher.
- H3. Safety violation rate on held-out trace families is statistically indistinguishable from the tuning families (transfer).

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
