# Checklist — Topic 01

When Networking Results Reverse: A Cross-Emulator Benchmark of Claim Stability in Congestion Control Experiments

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 20). Fewer than 12 reconstructable artifacts → widen the venue list once; if still below 12, stop and switch to Topic 05.
- [ ] Gate 2 (Day 55). No factor explains a meaningful share of variance and no reversals → reframe as "stability bounds" paper for TNSM; do not claim prediction.
- [ ] Stop. Artifact sample cannot be reconstructed, or no general factors emerge across papers.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 closest papers; build claim–method–data–limitation matrix; reproduce one artifact end-to-end on one backend | [ ] |
| Days 15–30 | Freeze inclusion criteria, factor list, CSI definition, mixed-model specification, and stop conditions; spec compiler working for 3 backends on 2 papers | [ ] |
| Days 31–60 | Pilot on 6 papers across 3 backends; estimate variance and runtime; attempt the hardest artifact; decide trial counts | [ ] |
| Days 61–90 | Preregistered run on remaining papers plus held-out validation; second-host replication; package artifact; draft around RQ1–RQ3 | [ ] |

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

- [ ] Cover letter for IEEE/ACM Transactions on Networking (ToN) written from `paper/cover-letter.md`
- [ ] Fallback plan for IEEE Transactions on Network and Service Management (TNSM) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
