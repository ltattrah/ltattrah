# Research Topics Portfolio

Source: *Publication Readiness Audit of Fifteen Laptop Feasible Computer Science Topics* (September 2026 edition).

Each folder below holds one topic. Every folder contains:

- `RESEARCH_STRATEGY.md` – the research strategy for the revised topic (contribution, research questions, study design, evidence package, artifact plan, risks, stop conditions, 90-day plan, journal strategy).
- `literature/` – closest-work matrix, reading notes, systematic search logs.
- `experiments/` – code, configurations, seeds, raw and derived results.
- `paper/` – manuscript drafts, figures, cover letter, reviewer response.

## Audit rubric

| Criterion | Weight | Journal standard |
|---|---|---|
| Novelty and contribution | 25 | Changes a concept, method, system, or interpretation rather than applying a known model |
| Methodological identification | 20 | Design supports the claimed causal, comparative, or correctness conclusion |
| External validity | 15 | Result transfers across time, data, systems, users, or environments |
| Significance and journal fit | 15 | Outcome matters to the journal community and fits its article scope |
| Feasibility and artifact | 15 | Study is executable and its central result can be reproduced |
| Ethics and transparency | 10 | Data rights, participant protection, disclosure, and uncertainty handled explicitly |

Score bands: 80–100 strong after redesign; 70–79 plausible with novelty or validation risk; 60–69 needs a different contribution; below 60 likely desk rejection in the original form.

## Ranked journal potential

| Rank | Folder | Revised topic | Current | Revised | Decision |
|---|---|---|---|---|---|
| 1 | [08](08-mutable-vector-db-consistency-oracle/) | Beyond Static Recall: A Black-Box Consistency and Freshness Oracle for Mutable Vector Databases | 77 | 94 | Retain and sharpen semantics |
| 2 | [12](12-capability-safe-rag/) | Capability-Safe RAG with Provenance-Enforced Control Flow Under Adaptive Indirect Prompt Injection | 73 | 93 | Retain with systems focus |
| 3 | [06](06-vector-sql-metamorphic-testing/) | Metamorphic Testing of Vector SQL and Hybrid Search Semantics Across Database Engines | 71 | 92 | Narrow to emerging semantics |
| 4 | [01](01-network-claim-stability/) | When Networking Results Reverse: A Cross-Emulator Benchmark of Claim Stability in Congestion Control Experiments | 69 | 88 | Retain and reframe |
| 5 | [05](05-optimizer-stability-boundaries/) | Learning Query Optimizer Stability Boundaries Under Continuous Skew and Correlation Drift | 68 | 88 | Retain and formalize |
| 6 | [10](10-infrastructure-template-lineage/) | How Insecure Infrastructure Templates Propagate and Persist Across Repository Lineages | 54 | 85 | Shift from prevalence to lineage |
| 7 | [03](03-encrypted-dns-privacy-regression/) | Silent Privacy Regression in Encrypted DNS Fallback Under Loss, Outage, and Resolver Failure | 62 | 84 | Retain with narrow gap |
| 8 | [14](14-process-drift-counterfactuals/) | From Process Drift Alerts to Action: Counterfactual Explanations for Operational Diagnosis | 56 | 84 | Move from explanation to action |
| 9 | [07](07-risk-calibrated-streaming-entity-resolution/) | Risk-Calibrated Streaming Entity Resolution Under Hard Byte and Latency Budgets | 60 | 82 | Formalize the resource problem |
| 10 | [04](04-detectability-preserving-flow-sampling/) | Detectability-Preserving Adaptive Flow Sampling for Rare Network Attacks Under Fixed Telemetry Budgets | 55 | 82 | Add a new method |
| 11 | [15](15-cumulative-consent-manipulation/) | Cumulative Effects of Repeated Consent Manipulation on Preference Alignment and Privacy Fatigue | 52 | 82 | Make the design longitudinal |
| 12 | [02](02-safe-online-controller-selection/) | Safety-Constrained Online Controller Selection for Intermittent and Asymmetric Access Networks | 57 | 81 | Major redesign |
| 13 | [13](13-explanation-confidence-transfer/) | When Explanations Transfer Confidence Without Improving Accuracy: A Multi-Study Test of Calibrated Reliance | 51 | 80 | Add theory and a second study |
| 14 | [11](11-supply-chain-early-warning/) | Early Warning of Software Supply Chain Incidents with Positive-Unlabeled Temporal Risk Models | 50 | 80 | Replace classification with early warning |
| 15 | [09](09-prospective-selective-phishing-detection/) | Prospective Selective Phishing Detection Under Campaign, Source, and Collection Shift | 47 | 77 | High-risk redesign |

## Areas

| Area | Topics | Area-level requirement |
|---|---|---|
| Computer networking | 01, 02, 03, 04 | General protocol or measurement insight; bounded claims; at least one cross-environment validation |
| Databases | 05, 06, 07, 08 | Formalized correctness and semantics; no product rankings |
| Computer security | 09, 10, 11, 12 | Precise threat model, adversarial evaluation, responsible disclosure, operational error metrics |
| Information systems | 13, 14, 15 | Theory, construct validity, evidence about decisions or organizational outcomes; ethics approval |

## Recommended research order

Manage the portfolio as a sequence of feasibility decisions: one primary topic and one backup that share tools but not the same uncertain data source.

| Order | Topic | Reason | Stop condition |
|---|---|---|---|
| 1 | 08 Vector database consistency | Best novelty and artifact balance | No reproducible semantic anomaly after four engines and stress histories |
| 2 | 06 Vector SQL testing | Low compute and confirmable correctness | Oracle produces mostly documented differences or false positives |
| 3 | 12 Capability-safe RAG | Timely security problem with system contribution | External policy cannot preserve benign utility against adaptive attacks |
| 4 | 05 Optimizer stability | Strong database question with controllable data | No transferable stability boundary or useful guard |
| 5 | 01 Network claim stability | Clear reproducibility contribution | Artifact sample cannot be reconstructed or no general factors emerge |
| 6 | 10 Infrastructure template lineage | Useful longitudinal security evidence | Copy lineage cannot be inferred with acceptable precision |

Primary choice by preferred area: Topic 08 (databases), Topic 12 (security with a local small-model setup), Topic 01 (lowest data-access risk). Topics 13 and 15 must not start recruitment until theory, power analysis, ethics review, and recruitment budget are complete.

## Common 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Structured review of the closest 25–40 papers; claim–method–data–limitation matrix; reproduce one current baseline; verify data and tool access |
| Days 15–30 | Formal problem statement, primary hypothesis or correctness property, unit of analysis, baselines, metrics, exclusions, stop conditions; small deterministic artifact |
| Days 31–60 | Pilot large enough to estimate variance, failure prevalence, runtime, storage; hardest baseline and one transfer evaluation; revise claim only before the confirmatory protocol is frozen |
| Days 61–90 | Preregistered core study on held-out cases; package logs, seeds, versions, scripts, small reproduction; draft results around research questions |

## Non-negotiable journal requirements (every topic)

- [ ] Closest-work table stating exactly how the claim differs from at least five neighboring papers
- [ ] One primary contribution that stays valuable even when the method does not dominate every baseline
- [ ] Final held-out evaluation across time, data, systems, users, or environments
- [ ] Operational metrics (tail latency, false positives per hour, failure prevalence, review budget, decision quality)
- [ ] Reproducible artifact with versions, seeds, configurations, raw-to-result lineage, and a one-command test
- [ ] Limitations section separating measured findings from plausible explanations
- [ ] Ethics approval before human-participant recruitment; responsible disclosure before publishing security defects
- [ ] Journal-specific cover letter explaining fit without acceptance or impact claims

## Shared tooling conventions

- Python is the primary language for generators, harnesses, analysis, and figures (`numpy`, `pandas`, `scipy`, `statsmodels`, `matplotlib`; `hypothesis` for property-based generators where useful).
- Every experiment records: git commit, engine or tool versions, OS and kernel, CPU model, seed, configuration hash, start and end time.
- Raw outputs are written once and never edited; derived tables are regenerated by scripts from raw outputs.
- One-command reproduction (`make reproduce` or `python -m experiments.reproduce --small`) is a deliverable, not an afterthought.
