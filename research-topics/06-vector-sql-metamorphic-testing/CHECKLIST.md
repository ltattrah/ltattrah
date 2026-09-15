# Checklist — Topic 06

Metamorphic Testing of Vector SQL and Hybrid Search Semantics Across Database Engines

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 25). Fewer than 4 engines runnable locally with mutation support → stop or substitute.
- [ ] Gate 2 (Day 60). Oracle produces mostly documented differences or false positives after the pilot campaign → stop (portfolio stop condition).

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on DBMS testing and vector search semantics; reproduce one SQLancer-found bug class; verify engine access | [ ] |
| Days 15–30 | Freeze semantics document, relation set, validity rules, engines, metrics, stop conditions; small deterministic generator | [ ] |
| Days 31–60 | Pilot campaign (≈ 100k tests per engine); estimate failure prevalence and runtime; hardest engine; first reports | [ ] |
| Days 61–90 | Full campaign; reducer and ablations; confirmation tracking; package; draft | [ ] |

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

- [ ] Cover letter for ACM Transactions on Database Systems (TODS) written from `paper/cover-letter.md`
- [ ] Fallback plan for The VLDB Journal noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
