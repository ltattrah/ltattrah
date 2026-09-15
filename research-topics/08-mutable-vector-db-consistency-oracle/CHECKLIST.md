# Checklist — Topic 08

Beyond Static Recall: A Black-Box Consistency and Freshness Oracle for Mutable Vector Databases

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 25). Fewer than 4 engines with mutation, filter, and restart support runnable locally → substitute or stop.
- [ ] Gate 2 (Day 60). No reproducible semantic anomaly after four engines and stress histories → stop (portfolio stop condition); move to Topic 06.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on dynamic ANN, consistency testing, vector DB internals; reproduce one static recall result to anchor tolerance settings | [ ] |
| Days 15–30 | Freeze the semantic model, failure classes, generator, checkpoint scheme, engines, stop conditions; small deterministic artifact | [~] artifact and model v0.1 done 2026-09-15 (`experiments/`, `experiments/model/semantic-model.md`); freeze pending literature review |
| Days 31–60 | Pilot at 100k vectors on 2 engines; failure prevalence, runtime, storage; hardest engine; one concurrent-history transfer | [ ] |
| Days 61–90 | Full preregistered campaign; reducer; disclosure; package; draft around RQ1–RQ3 | [ ] |

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
- [x] Artifact `experiments/reproduce.py --small` passes (2026-09-15, venv per `experiments/README.md`)
- [ ] Limitations section separates measured findings from plausible explanations
