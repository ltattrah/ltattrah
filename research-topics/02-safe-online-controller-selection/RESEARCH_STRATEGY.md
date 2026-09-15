# Topic 02 — Safety-Constrained Online Controller Selection for Intermittent and Asymmetric Access Networks

**Area:** Computer networking
**Original topic:** Contextual Bandit Congestion Control for Intermittent and Asymmetric Networks

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 57 |
| Upgraded potential | 81 |
| Priority | Medium |
| Decision | Major redesign |
| Laptop fit | Good |
| Primary journal | IEEE/ACM Transactions on Networking (ToN) |
| Secondary journal | IEEE Transactions on Mobile Computing (TMC) |
| Main risk | Crowded learning space |
| Portfolio order | Not in top six |

**Audit verdict.** Pursue only if the work can prove or enforce a meaningful safety condition and compare with current online-learning baselines. Otherwise Topic 01 offers a clearer contribution for similar effort.

## 1. Objective

Show that a *conservative* online selector over a small set of existing controllers can adapt across intermittent and asymmetric regimes while **bounding** excess delay and loss relative to a designated safe controller, and that the bound holds on unseen trace families and in a Linux data-plane prototype.

## 2. Why the original framing fails

Learning-based congestion control is mature: Aurora [12] and Mutant [11] already learn online from existing protocols. A contextual bandit that picks pacing gains is not novel by itself. The defensible gap is **safe adaptation under a precisely defined regime** (outages, reverse-path delay, abrupt asymmetric capacity change) with a formal or empirically enforceable safety constraint, not a higher average utility.

## 3. Defensible contribution

> A conservative online selector can adapt across intermittent and asymmetric regimes while bounding excess delay and loss relative to a safe controller and retaining performance on unseen traces.

The safety bound is the contribution. Utility gains are secondary evidence.

## 4. Research questions and hypotheses

- **RQ1.** Under what regime definition (outage duration, asymmetry ratio, reverse-path congestion level) do fixed controllers (CUBIC, BBR, delay-based) each fail, and is any single controller safe across all regimes?
- **RQ2.** Can a conservative bandit (conservative LinUCB or constrained Thompson sampling with fallback) keep excess delay and loss within a stated budget relative to the safe controller, with a regret bound under stated assumptions or a falsifiable empirical bound?
- **RQ3.** Does the safety guarantee hold on trace families never seen during tuning and in a Linux prototype rather than only in simulation?

Hypotheses:

- **H1.** No fixed controller is within the safety budget in every regime (motivates selection).
- **H2.** The conservative selector violates the safety budget in fewer than a preregistered fraction of episodes, versus a substantially higher fraction for an unconstrained bandit and a rule-based switcher.
- **H3.** Safety violation rate on held-out trace families is statistically indistinguishable from the tuning families (transfer).

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Mutant [11] | Online RL that learns from existing protocols | No explicit safety constraint; compared as a baseline when the artifact is available |
| Aurora [12] | Deep RL congestion control | Learned actions, offline training; here the action set is existing controllers and safety is enforced online |
| Conservative bandits (Wu et al.), safe exploration literature | Regret with performance constraints | Applied to a networking regime with delay, loss, and fairness constraints; needs a networking insight |
| Rule-based controller switchers | Heuristic switching | Baseline; the paper must show the learner is not merely a tuned heuristic |
| Satellite / cellular CC studies | Regime-specific controllers | Regime definitions reused; contribution is the safe selector across regimes |

## 6. Study design

### Phase A — Regime and constraint definition (Days 1–25)
1. Define the regime space: outage length and frequency, uplink/downlink asymmetry, ACK compression, reverse-path congestion, abrupt capacity steps.
2. State constraints **before** tuning the learner: maximum excess queuing delay, maximum excess loss, and a fairness floor (Jain's index) relative to the safe controller over a window.
3. Fix the action set: CUBIC, BBR, one delay-based controller, and bounded parameter variants.

### Phase B — Learner and analysis (Days 20–50)
1. Implement conservative LinUCB and constrained Thompson sampling with a fallback to the safe controller when the confidence interval crosses the constraint.
2. Provide either a regret and safety analysis under stated assumptions (stationarity within a regime, bounded context) or a falsifiable empirical bound with confidence intervals.

### Phase C — Trace-driven evaluation (Days 35–70)
1. Assemble ≥ 20 trace families (cellular, Wi-Fi, satellite-style). Group splits by **source**, never randomly.
2. Run ≥ 5 seeds per condition. Include abrupt outages, ACK compression, reverse-path congestion.
3. Compare: CUBIC, BBR, delay-based, rule-based switcher, oracle (best fixed controller per episode), unconstrained bandit, and Mutant when its artifact runs.

### Phase D — Linux prototype (Days 60–90)
1. Implement the selector in a Linux data plane (user-space switching among kernel CC modules via `setsockopt(TCP_CONGESTION)` or a Mahimahi/netem testbed).
2. Report at least one implementation result outside the simulator, with the same constraint metrics.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Trace families | ≥ 20, source-grouped splits |
| Seeds | ≥ 5 per condition |
| Baselines | CUBIC, BBR, delay-based, rule-based switcher, oracle, Mutant (if available) |
| Safety metrics | Explicit violation counts, violation magnitude, adaptation time after change |
| Fairness | With competing flows |
| Transfer | Unseen trace families |
| Implementation | One result outside the simulator |

Never report a scalar utility alone; always report the constraint metrics beside it.

## 8. Artifact and tooling plan

- Python bandit implementation (`numpy`) with deterministic seeds; trace replay harness in Python driving Mahimahi or netem.
- Regime generator that emits labelled trace segments for controlled experiments; real traces stored with source metadata.
- **OMNeT++/INET option.** INET's TCP models and link-layer models give a discrete-event environment for the intermittent and asymmetric regimes; a Python harness (`omnetpp` runs via `opp_run`, results parsed with `pandas`) can run the same regime definitions for a simulator cross-check. This does not replace the Linux prototype the audit requires.
- Provenance: kernel CC module versions, trace file hashes, seeds, constraint parameters.
- One-command reproduction on a small trace subset.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Method reduces to a tuned heuristic with a small action space | Include the rule-based switcher and the oracle; show the learner's gap to oracle and its advantage over the switcher on unseen sources |
| Simulation-only evidence | Linux prototype with the same metrics |
| Scalar utility hides delay or fairness regressions | Constraints are first-class metrics; report violations before utility |
| Trace leakage across splits | Source-grouped splits, logged and hashed |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 25).** If a single fixed controller is safe in all regimes, the selection problem is trivial → stop and redirect effort to Topic 01.
- **Gate 2 (Day 50).** If neither a theoretical bound nor a stable empirical bound can be stated → stop.
- **Stop.** Safety cannot be enforced without collapsing to the safe controller (no adaptation benefit).

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on learned CC, safe bandits, and regime-specific controllers; reproduce one baseline (BBR vs CUBIC on a public cellular trace) |
| Days 15–30 | Freeze regime definitions, constraints, action set, metrics, split policy, stop conditions; small deterministic harness |
| Days 31–60 | Pilot on 6 trace families; estimate violation variance; attempt Mutant baseline; one unseen-family transfer test |
| Days 61–90 | Preregistered run on all families; Linux prototype; package artifact; draft around RQ1–RQ3 |

## 12. Journal strategy

- **ToN** requires a networking insight, not an application of bandits: lead with the regime analysis (RQ1) and the safety mechanism, then the learner.
- **TMC** becomes plausible if the evaluation is grounded in mobile-access behavior with trace diversity or a small real-network validation.

## 13. Ethics and disclosure

No human subjects. Public traces used under their licenses; own traces collected only on networks the researcher controls.

## 14. Folder layout

```
02-safe-online-controller-selection/
├── RESEARCH_STRATEGY.md
├── literature/      closest-work.md, search-log.csv
├── experiments/     regimes/, traces/ (metadata + hashes), bandit/, prototype/, runs/, analysis/
└── paper/
```
