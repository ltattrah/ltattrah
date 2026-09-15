# Paper outline — Topic 03

**Working title.** Silent Privacy Regression in Encrypted DNS Fallback Under Loss, Outage, and Resolver Failure

**Primary target.** IEEE Transactions on Network and Service Management (TNSM)  
**Secondary target.** IEEE Transactions on Information Forensics and Security (TIFS)

**One-sentence contribution.**
> Encrypted DNS implementations expose distinct privacy and reliability failure states under impairment, and a state-aware resolver policy can reduce failure without increasing plaintext fallback or observable metadata.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. What failure states (retry storm, endpoint switch, plaintext fallback, stale-cache serve, hard failure) do at least four client implementations enter under eight or more impairment regimes, and do they match advertised behavior?
   - RQ2. Under a stated on-path observer model, how much information (queried domain, resolver identity, query timing, fallback event) leaks in each failure state, measured rather than assumed?
   - RQ3. Does a state-aware policy (detect impairment state, choose transport and endpoint accordingly) reduce failure rate and tail latency without raising plaintext fallback or leakage, and does it hold on a second OS or access network?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. At least one widely used client silently falls back to plaintext under resolver outage or captive-portal-style interruption, contrary to or absent from its documentation.
- H2. Failure-state distribution differs across clients more than across encrypted transports (implementation, not protocol, drives privacy regression).
- H3. The state-aware policy has lower failure and equal or lower leakage than default client behavior and any fixed protocol.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
