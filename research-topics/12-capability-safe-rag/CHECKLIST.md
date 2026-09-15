# Checklist — Topic 12

Capability-Safe Retrieval-Augmented Generation with Provenance-Enforced Control Flow Under Adaptive Indirect Prompt Injection

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 30). Cannot express the three workflows' benign needs as capability policies without denying them → redesign policy model before proceeding.
- [ ] Gate 2 (Day 80). External policy cannot preserve benign utility against adaptive attacks → stop (portfolio stop condition).

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on IPI, agent security, IFC for LLMs; reproduce StruQ baseline locally; verify model and hardware | [ ] |
| Days 15–30 | Freeze threat model, assets/actions, provenance schema, policy language, tasks, metrics, stop conditions; small deterministic system | [ ] |
| Days 31–60 | Pilot with 1 model, 200 attack–task combinations; variance; hardest baseline (StruQ); one held-out-model test | [ ] |
| Days 61–90 | Full preregistered evaluation; ablations; package; draft | [ ] |

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
- [ ] Fallback plan for ACM Transactions on Privacy and Security (TOPS) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
