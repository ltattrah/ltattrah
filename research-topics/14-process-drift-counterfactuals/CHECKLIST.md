# Checklist — Topic 14

From Process Drift Alerts to Action: Counterfactual Explanations for Operational Diagnosis

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 55). Counterfactual fidelity on controlled scenarios below a preregistered floor → stop.
- [ ] Gate 2 (Day 60). No ethics approval or participant access for the study → publish technical part as a workshop paper only.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers; reproduce Adams et al.-style drift detection on one log; submit ethics application | [ ] |
| Days 15–30 | Freeze representation, scenarios, counterfactual definition, baselines, metrics, study design, stop conditions; small deterministic generator | [ ] |
| Days 31–60 | Pilot generation on all logs; fidelity and stability; pilot study interface with a few participants | [ ] |
| Days 61–90 | Preregistered analyst study; analysis; package; draft | [ ] |

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

- [ ] Cover letter for Information Systems written from `paper/cover-letter.md`
- [ ] Fallback plan for Decision Support Systems (DSS) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
