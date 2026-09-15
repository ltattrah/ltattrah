# Checklist — Topic 02

Safety-Constrained Online Controller Selection for Intermittent and Asymmetric Access Networks

## Decision gates (from RESEARCH_STRATEGY.md section 10)

- [ ] Gate 1 (Day 25). If a single fixed controller is safe in all regimes, the selection problem is trivial → stop and redirect effort to Topic 01.
- [ ] Gate 2 (Day 50). If neither a theoretical bound nor a stable empirical bound can be stated → stop.
- [ ] Stop. Safety cannot be enforced without collapsing to the safe controller (no adaptation benefit).

## 90-day plan

| Window | Work | Done |
|---|---|---|
| Days 1–14 | Review 25–40 papers on learned CC, safe bandits, and regime-specific controllers; reproduce one baseline (BBR vs CUBIC on a public cellular trace) | [ ] |
| Days 15–30 | Freeze regime definitions, constraints, action set, metrics, split policy, stop conditions; small deterministic harness | [ ] |
| Days 31–60 | Pilot on 6 trace families; estimate violation variance; attempt Mutant baseline; one unseen-family transfer test | [ ] |
| Days 61–90 | Preregistered run on all families; Linux prototype; package artifact; draft around RQ1–RQ3 | [ ] |

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
- [ ] Fallback plan for IEEE Transactions on Mobile Computing (TMC) noted
- [ ] Artifact `experiments/reproduce.py --small` passes on a clean machine
- [ ] Limitations section separates measured findings from plausible explanations
