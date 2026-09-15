# Checklist — Topic 05

Learning Query Optimizer Stability Boundaries Under Continuous Skew and Correlation Drift

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 55). No boundary structure beyond trivial selectivity switches → stop.
- [ ] Gate 2 (Day 70). No transferable boundary quantity across engines → reframe as single-engine study for a workshop; do not submit to VLDBJ.
- [ ] Stop. No transferable stability boundary or useful guard.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on cardinality estimation, plan diagrams, re-optimization, drift benchmarking; reproduce one known correlation-induced misestimate | [ ] |
| Days 15–30 | Freeze space definition, templates, definitions, engines, metrics, stop conditions; generator and capture working on 2 templates | [ ] |
| Days 31–60 | Pilot on 6 templates across 2 engines; variance and runtime; hardest engine; one real-data path | [ ] |
| Days 61–90 | Full preregistered mapping; guard evaluation; second real-data validation; package; draft | [ ] |

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

- [ ] Cover letter for The VLDB Journal written from `paper/cover-letter.md`
- [ ] Fallback plan for ACM Transactions on Database Systems (TODS) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
