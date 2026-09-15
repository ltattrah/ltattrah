# Checklist — Topic 07

Risk-Calibrated Streaming Entity Resolution Under Hard Byte and Latency Budgets

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 30). No clean formal objective yielding a non-trivial retention score → stop; move to Topic 05 or 06.
- [ ] Gate 2 (Day 50). Fewer than 6 credible chronologically ordered streams → stop.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on streaming/progressive ER, selective prediction, caches; reproduce one progressive ER baseline | [ ] |
| Days 15–30 | Freeze formulation, retention score, calibration scheme, datasets, budgets, metrics, stop conditions; small deterministic harness | [ ] |
| Days 31–60 | Pilot on 2 datasets and 3 budgets; variance and throughput; hardest baseline; one drift-injection transfer test | [ ] |
| Days 61–90 | Preregistered replay on all datasets; frontiers and ablations; package; draft | [ ] |

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

- [ ] Cover letter for IEEE Transactions on Knowledge and Data Engineering (TKDE) written from `paper/cover-letter.md`
- [ ] Fallback plan for Data Mining and Knowledge Discovery (DMKD) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
