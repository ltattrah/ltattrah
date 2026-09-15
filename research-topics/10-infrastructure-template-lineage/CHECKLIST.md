# Checklist — Topic 10

How Insecure Infrastructure Templates Propagate and Persist Across Repository Lineages

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 55). Copy lineage cannot be inferred with acceptable precision on hand-labelled edges → stop (portfolio stop condition).
- [ ] Gate 2 (Day 75). Repair-lag comparison confounded beyond repair → drop RQ2 claims and reframe around triage.

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on IaC security, clone provenance, ecosystem propagation; run an existing scanner on a sample; verify API access | [ ] |
| Days 15–30 | Freeze ecosystems, rules, lineage signals, uncertainty model, metrics, stop conditions; small deterministic pipeline | [ ] |
| Days 31–60 | Pilot on a few hundred repositories; label edges; estimate precision; attempt one repair-lag estimate | [ ] |
| Days 61–90 | Full mining; diffusion analysis; triage evaluation; disclosure; package; draft | [ ] |

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
- [ ] Fallback plan for IEEE Transactions on Software Engineering (TSE) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
