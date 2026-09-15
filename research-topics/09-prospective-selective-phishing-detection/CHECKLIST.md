# Checklist — Topic 09

Prospective Selective Phishing Detection Under Campaign, Source, and Collection Shift

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 30). No unique corpus with timestamps, label times, and multiple sources → stop; this topic is dropped.
- [ ] Gate 2 (Day 70). Maintenance mechanism does not beat periodic retraining under the budget → reframe as an evaluation-only note; not a TIFS submission.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers; verify feed access and licenses; reproduce one lightweight detector on a public dataset | [ ] |
| Days 15–30 | Freeze protocol, corpus rules, metrics, budget, stop conditions; small deterministic replay | [ ] |
| Days 31–60 | Pilot expanding-window replay on 6 months; variance; source hold-out; label-delay effect | [ ] |
| Days 61–90 | Full preregistered replay; prospective weeks; FP audit; package; draft | [ ] |

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

- [ ] Cover letter for IEEE Transactions on Information Forensics and Security (TIFS) written from `paper/cover-letter.md`
- [ ] Fallback plan for ACM Transactions on Privacy and Security (TOPS) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
