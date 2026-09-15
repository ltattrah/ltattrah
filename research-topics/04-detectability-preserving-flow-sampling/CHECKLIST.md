# Checklist — Topic 04

Detectability-Preserving Adaptive Flow Sampling for Rare Network Attacks Under Fixed Telemetry Budgets

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 30). No bound or controlled approximation can be stated → reframe as purely empirical; TDSC target dropped.
- [ ] Gate 2 (Day 75). Adaptive sampler does not beat sample-and-hold and active-uncertainty at equal budget on the design dataset → stop.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on sampling, sketches, and NIDS evaluation pitfalls; reproduce Mai et al.-style degradation curve on one dataset | [ ] |
| Days 15–30 | Freeze budget definition, sampler, estimator, dataset partitions, baselines, metrics, stop conditions; deterministic small artifact | [ ] |
| Days 31–60 | Pilot on the design dataset with 3 budgets; variance and runtime; attempt the active-uncertainty baseline; one transfer test | [ ] |
| Days 61–90 | Preregistered evaluation on held-out datasets and injections; robustness; package; draft | [ ] |

## Non-negotiable journal requirements

- [ ] Closest-work table stating exactly how the claim differs from at least five neighboring papers
- [ ] One primary contribution that stays valuable even when the method does not dominate every baseline
- [ ] Final held-out evaluation across time, data, systems, users, or environments
- [ ] Operational metrics (tail latency, false positives per hour, failure prevalence, review budget, decision quality)
- [ ] Reproducible artifact with versions, seeds, configurations, raw-to-result lineage, and a one-command test
- [ ] Limitations section separating measured findings from plausible explanations
- [ ] Ethics approval before human-participant recruitment; responsible disclosure before publishing security defects
- [ ] Journal-specific cover letter explaining fit without acceptance or impact claims

## Submission

- [ ] Cover letter for IEEE Transactions on Network and Service Management (TNSM) written from `paper/cover-letter.md`
- [ ] Fallback plan for IEEE Transactions on Dependable and Secure Computing (TDSC) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
