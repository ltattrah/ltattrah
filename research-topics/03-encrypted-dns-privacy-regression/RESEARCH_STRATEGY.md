# Topic 03 — Silent Privacy Regression in Encrypted DNS Fallback Under Loss, Outage, and Resolver Failure

**Area:** Computer networking
**Original topic:** Encrypted DNS Under Impaired Networks

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 62 |
| Upgraded potential | 84 |
| Priority | Medium-high |
| Decision | Retain with narrow gap |
| Laptop fit | Excellent |
| Primary journal | IEEE Transactions on Network and Service Management (TNSM) |
| Secondary journal | IEEE Transactions on Information Forensics and Security (TIFS) |
| Main risk | Latency comparison already known |
| Portfolio order | Not in top six |

**Audit verdict.** Retain, but remove generic protocol benchmarking from the main claim. Center the article on privacy failure states and cross-implementation behavior.

## 1. Objective

Characterize the **privacy and reliability failure states** that encrypted DNS clients (DoH, DoT, DoQ) enter when the encrypted path is impaired, measure what an on-path observer learns in each state, and show that a state-aware resolver policy reduces failure without increasing plaintext fallback or observable metadata.

## 2. Why the original framing fails

DoH performance has been measured globally [14]; DoQ has been compared with DoH and DoT [13]; mobile measurements cover encrypted DNS reliability [15]. Another latency table under loss is incremental. The gap is **silent privacy regression**: retries, endpoint changes, plaintext fallback, cache behavior, and metadata leakage when the encrypted path fails.

## 3. Defensible contribution

> Encrypted DNS implementations expose distinct privacy and reliability failure states under impairment, and a state-aware resolver policy can reduce failure without increasing plaintext fallback or observable metadata.

## 4. Research questions and hypotheses

- **RQ1.** What failure states (retry storm, endpoint switch, plaintext fallback, stale-cache serve, hard failure) do at least four client implementations enter under eight or more impairment regimes, and do they match advertised behavior?
- **RQ2.** Under a stated on-path observer model, how much information (queried domain, resolver identity, query timing, fallback event) leaks in each failure state, measured rather than assumed?
- **RQ3.** Does a state-aware policy (detect impairment state, choose transport and endpoint accordingly) reduce failure rate and tail latency without raising plaintext fallback or leakage, and does it hold on a second OS or access network?

Hypotheses:

- **H1.** At least one widely used client silently falls back to plaintext under resolver outage or captive-portal-style interruption, contrary to or absent from its documentation.
- **H2.** Failure-state distribution differs across clients more than across encrypted transports (implementation, not protocol, drives privacy regression).
- **H3.** The state-aware policy has lower failure and equal or lower leakage than default client behavior and any fixed protocol.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Chhabra et al. [14] | Global DoH performance | Performance; no failure-state or leakage measurement |
| Hounsel et al. [13] | DoQ vs DoH/DoT web performance | Protocol comparison; not impairment-driven fallback |
| Mobile DNS protocol measurement [15] | Reliability in mobile networks | Passive reliability; no controlled impairment or observer model |
| DNS privacy leakage studies (padding, traffic analysis) | Observer inference on healthy encrypted DNS | Here the observer model is applied to *failure states* |
| Client fallback policy documents (browsers, OS resolvers) | Advertised behavior | Treated as claims to test |

## 6. Study design

### Phase A — Threat model and testbed (Days 1–25)
1. State the observer precisely: on-path passive observer at the access link; sees IP/port, sizes, timing, SNI where present, plaintext DNS if it occurs. No active manipulation beyond the impairment injector unless stated.
2. Select ≥ 4 clients (for example a browser resolver, an OS stub resolver, two standalone proxies) and ≥ 4 resolver endpoints including a **controlled local resolver**. Pin versions; record advertised fallback behavior in a table.
3. Build a Python-orchestrated testbed: network namespaces, `tc netem` for impairment, packet capture per run.

### Phase B — Impairment matrix (Days 20–55)
1. Regimes (≥ 8): delay, burst loss, reordering, resolver outage, path switching, IPv4-only failure, IPv6-only failure, captive-portal-style interruption.
2. Separate transport effects from resolver distance by pairing each public resolver with the local resolver under identical impairment.
3. Cold and warm sessions; repeated trials for confidence intervals on tail latency and failure.

### Phase C — Instrumentation and state classification (Days 35–65)
1. Instrument: connection reuse, retries, endpoint changes, cache hits, plaintext fallback, and observer-visible features (packet sizes, timing, destination).
2. Define failure states from the instrumented traces; classify each trial with a deterministic rule set; report inter-rule agreement.
3. Leakage metric per state: what the observer can infer, quantified (for example domain identifiability from size/timing, resolver identity, fallback detection).

### Phase D — State-aware policy and validation (Days 55–90)
1. Implement a state-aware policy in a local proxy: detect impairment state, select transport and endpoint, never fall back to plaintext without explicit user policy.
2. Compare with fixed DoH, fixed DoT, fixed DoQ, and default client behavior.
3. Validate the most important failures on a second OS or access network.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Clients | ≥ 4, versions pinned |
| Resolvers | ≥ 4 including local controlled |
| Impairment regimes | ≥ 8 |
| Sessions | Cold and warm |
| Metrics | Failure rate, tail latency (CI), retries, endpoint changes, plaintext fallback rate, cache hits, measured leakage per state |
| Validation | Second OS or access network |

## 8. Artifact and tooling plan

- Python orchestrator (namespaces, `tc`, `dnspython` for query generation, `scapy`/`pyshark` for capture parsing).
- Local resolver (Unbound or Knot Resolver) in a container with pinned config; `doh-proxy`/`dnsdist` style endpoints under control.
- State classifier and leakage metrics in Python; all pcaps kept with hashes.
- **OMNeT++ note.** Not needed for the core study; a simulated access network is a weaker substitute for the real client implementations that are the subject.
- One-command reproduction with the local resolver only (no public endpoints), reproducing the failure-state table.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Client behavior changes across versions | Pin versions, record them, re-run a smoke subset on the latest version before submission and report differences |
| Public resolver geography confounds comparisons | Local resolver pairing; report resolver RTT as a covariate |
| Fallback alone does not establish harm | Measured leakage under a stated observer model; map each state to a concrete inference |
| Testbed artifacts (netem) not representative | Second access network validation for the key failures |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 25).** If no client exhibits any fallback or endpoint-change behavior under any regime → the topic reduces to a reliability comparison; stop or reframe narrowly.
- **Gate 2 (Day 65).** If leakage cannot be measured beyond "fallback happened" → TIFS framing is dead; keep TNSM framing only.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on encrypted DNS measurement and DNS traffic analysis; reproduce one published latency result on the testbed |
| Days 15–30 | Freeze threat model, client and resolver list, regime list, state definitions, leakage metrics, stop conditions; small deterministic testbed |
| Days 31–60 | Pilot: 2 clients × 2 resolvers × all regimes; estimate variance; attempt the hardest regime (captive portal) |
| Days 61–90 | Full preregistered matrix; policy evaluation; second-OS validation; package pcaps and classifier; draft |

## 12. Journal strategy

- **TNSM** for the operational reliability and policy contribution (lead with failure states and the state-aware policy).
- **TIFS** only if the observer model, leakage measurement, and privacy consequences are central and quantitatively strong.

## 13. Ethics and disclosure

No human subjects; only synthetic query lists. Report silent plaintext fallback to the affected client maintainers before publication under a coordinated disclosure timeline.

## 14. Folder layout

```
03-encrypted-dns-privacy-regression/
├── RESEARCH_STRATEGY.md
├── literature/      closest-work.md, advertised-fallback-table.md
├── experiments/     testbed/, regimes/, captures/ (hashes only in git), classifier/, policy/, analysis/
└── paper/
```
