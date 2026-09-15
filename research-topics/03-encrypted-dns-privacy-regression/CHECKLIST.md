# Checklist — Topic 03

Silent Privacy Regression in Encrypted DNS Fallback Under Loss, Outage, and Resolver Failure

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 25). If no client exhibits any fallback or endpoint-change behavior under any regime → the topic reduces to a reliability comparison; stop or reframe narrowly.
- [ ] Gate 2 (Day 65). If leakage cannot be measured beyond "fallback happened" → TIFS framing is dead; keep TNSM framing only.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on encrypted DNS measurement and DNS traffic analysis; reproduce one published latency result on the testbed | [ ] |
| Days 15–30 | Freeze threat model, client and resolver list, regime list, state definitions, leakage metrics, stop conditions; small deterministic testbed | [ ] |
| Days 31–60 | Pilot: 2 clients × 2 resolvers × all regimes; estimate variance; attempt the hardest regime (captive portal) | [ ] |
| Days 61–90 | Full preregistered matrix; policy evaluation; second-OS validation; package pcaps and classifier; draft | [ ] |

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
- [ ] Fallback plan for IEEE Transactions on Information Forensics and Security (TIFS) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
