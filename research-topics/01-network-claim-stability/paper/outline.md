# Paper outline — Topic 01

**Working title.** When Networking Results Reverse: A Cross-Emulator Benchmark of Claim Stability in Congestion Control Experiments

**Primary target.** IEEE/ACM Transactions on Networking (ToN)  
**Secondary target.** IEEE Transactions on Network and Service Management (TNSM)

**One-sentence contribution.**
> Networking conclusions have measurable stability boundaries. A compact set of emulator, queue, timing, and host factors can predict when reported algorithm rankings will reverse across implementations.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. How often do published congestion-control claims (ranking, sign, effect size) reverse when re-executed across Mininet, ns-3, and Linux `tc`-based testbeds under documented variation of nuisance factors?
   - RQ2. Which factors (queue discipline, buffer size, timer resolution, seed, warm-up, traffic generator, CPU load, kernel version) explain the largest share of claim variance, and are these factors consistent across papers?
   - RQ3. Does a Claim Stability Index computed on a screening subset predict cross-environment reliability on held-out experiments and on a second host?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Sign reversals are concentrated in claims whose reported effect size is below a threshold relative to cross-seed variance (small-effect claims are fragile).
- H2. Buffer size and queue discipline account for more claim variance than emulator identity once timing resolution is controlled.
- H3. CSI on the screening subset predicts held-out cross-environment agreement with rank correlation above a preregistered floor.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
