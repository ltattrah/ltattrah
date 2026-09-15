# Checklist — Topic 11

Early Warning of Software Supply Chain Incidents with Positive-Unlabeled Temporal Risk Models

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 30). Fewer than ~100 credible dated incidents → narrow outcome (for example typosquat incidents only) or abandon predictive claims.
- [ ] Gate 2 (Day 80). No feature set provides lead time beyond a trivial baseline under any budget → stop.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers; verify registry dump and advisory access; reproduce one metadata-detection baseline | [ ] |
| Days 15–30 | Freeze snapshot rules, incident definition, features, models, budgets, metrics, stop conditions; small deterministic snapshot builder | [ ] |
| Days 31–60 | Pilot on two years of snapshots; variance; hardest baseline; one held-out year | [ ] |
| Days 61–90 | Full preregistered evaluation; label uncertainty; package; draft | [ ] |

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

- [ ] Cover letter for IEEE Transactions on Dependable and Secure Computing (TDSC) written from `paper/cover-letter.md`
- [ ] Fallback plan for IEEE Transactions on Information Forensics and Security (TIFS) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
