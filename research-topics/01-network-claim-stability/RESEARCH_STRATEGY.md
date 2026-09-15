# Topic 01 — When Networking Results Reverse: A Cross-Emulator Benchmark of Claim Stability in Congestion Control Experiments

**Area:** Computer networking
**Original topic:** Reproducibility of Network Emulation Studies

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 69 |
| Upgraded potential | 88 |
| Priority | High |
| Decision | Retain and reframe |
| Laptop fit | Excellent |
| Primary journal | IEEE/ACM Transactions on Networking (ToN) |
| Secondary journal | IEEE Transactions on Network and Service Management (TNSM) |
| Main risk | Replication only |
| Portfolio order | 5 of 6 (lowest data-access risk backup) |

**Audit verdict.** One of the strongest laptop topics after reframing. Do not present it as a general reproducibility survey. Present a measurable claim-stability construct, a benchmark corpus, and evidence that the construct predicts cross-environment reliability.

## 1. Objective

Establish that networking conclusions have measurable stability boundaries: a compact set of emulator, queue, timing, and host factors predicts when a published congestion-control algorithm ranking or effect direction will reverse across implementations. The deliverable is a validated **Claim Stability Index (CSI)**, a benchmark corpus of re-executed artifacts, and a mixed-effects decomposition of where instability comes from.

## 2. Why the original framing fails

Reproducible network emulation is not a new objective. Container-based emulation (Handigol et al. [9]) and time-controlled reproduction (Popescu and Moore [10]) already exist. Repeating experiments in Mininet and ns-3 is an engineering replication. The unit of analysis must change from *the experiment* to *the claim*: does the reported ranking or effect direction survive reasonable implementation choices?

## 3. Defensible contribution

> Networking conclusions have measurable stability boundaries. A compact set of emulator, queue, timing, and host factors can predict when reported algorithm rankings will reverse across implementations.

The contribution survives even if reversals turn out to be rare: the paper then reports defensible stability bounds and the factors that do not matter, which is itself a general experimental principle.

## 4. Research questions and hypotheses

- **RQ1.** How often do published congestion-control claims (ranking, sign, effect size) reverse when re-executed across Mininet, ns-3, and Linux `tc`-based testbeds under documented variation of nuisance factors?
- **RQ2.** Which factors (queue discipline, buffer size, timer resolution, seed, warm-up, traffic generator, CPU load, kernel version) explain the largest share of claim variance, and are these factors consistent across papers?
- **RQ3.** Does a Claim Stability Index computed on a screening subset predict cross-environment reliability on held-out experiments and on a second host?

Hypotheses (stated before data collection):

- **H1.** Sign reversals are concentrated in claims whose reported effect size is below a threshold relative to cross-seed variance (small-effect claims are fragile).
- **H2.** Buffer size and queue discipline account for more claim variance than emulator identity once timing resolution is controlled.
- **H3.** CSI on the screening subset predicts held-out cross-environment agreement with rank correlation above a preregistered floor.

Competing hypothesis to report honestly: emulator identity dominates (which would strengthen the operational TNSM framing instead of the ToN framing).

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Handigol et al. [9] | Container-based emulation for reproducible experiments | Tool for reproduction; no measure of claim stability |
| Popescu and Moore [10] | Time-controlled emulation environment | Controls timing; does not benchmark published claims across backends |
| Mutant, Aurora [11][12] | Learned congestion control | Subjects of study, not competitors; their artifacts are candidates for the corpus |
| ACM artifact evaluation practice | Badges for reproducibility | Binary outcome; no quantitative stability construct |
| ns-3 / Mininet cross-validation studies | Fidelity comparisons of one tool | Compare tools, not the survival of a specific claim under factor screening |

Fill the closest-work table in `literature/closest-work.md` to at least five entries with exact claim differences before Day 14.

## 6. Study design

### Phase A — Corpus construction (Days 1–20)
1. Define inclusion criteria *before* searching: open artifact, congestion-control or transport claim, emulation or testbed evaluation, published 2018–2026 in a defined venue list.
2. Search systematically (DBLP, venue proceedings) and log every included and excluded paper with a reason.
3. Target 12–20 artifacts. For each, record: primary claim (verbatim), claim type (ranking / sign / magnitude), the exact figure or table needed to reproduce it, and the minimal experiment that supports it.

### Phase B — Cross-backend re-execution (Days 15–55)
1. Implement a common experiment description (YAML) that compiles to Mininet, ns-3, and Linux `tc`/netem runs.
2. Screen nuisance factors with a fractional factorial design: queue discipline, buffer size, timer resolution, seed, warm-up period, traffic generator, background CPU load, kernel version.
3. Repeat every influential factor level with enough trials to estimate variance (pilot decides the trial count; preregister it).

### Phase C — Claim Stability Index (Days 40–70)
1. Define CSI as a weighted combination of sign agreement, rank agreement (Kendall tau), standardized effect size (Cohen's d or Cliff's delta across environments), and coefficient of variation across environments.
2. Fit CSI weights on a calibration subset; validate on held-out experiments. Report the preregistered rank-correlation threshold.

### Phase D — Second-host validation and decomposition (Days 60–90)
1. Repeat a reduced protocol on a second host or OS.
2. Fit mixed-effects models: claim outcome ~ factors + (1 | paper) + (1 | algorithm) + (1 | emulator) + (1 | host). Report variance components.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Artifacts | ≥ 12 independent |
| Backends | 3 (Mininet, ns-3, Linux tc) |
| Trials | Repeated under every influential factor |
| Validation | Second host or OS |
| Reconstruction | Headline table or figure rebuilt for each paper |
| Metrics | Sign agreement, rank agreement, standardized effect size, cross-environment variance, CSI, variance components |

Report reversal prevalence with confidence intervals. If reversals are rare, report stability bounds instead of forcing a positive result.

## 8. Artifact and tooling plan

- `experiments/spec/` — YAML experiment descriptions; `experiments/backends/{mininet,ns3,tc}/` — Python drivers that compile a spec to each backend.
- Python: `pandas` for result tables, `statsmodels` (`MixedLM`) for variance decomposition, `scipy.stats` for Kendall tau and effect sizes.
- ns-3 driven through its Python bindings or generated C++ scenarios with a Python harness.
- Provenance per run: kernel version (`uname -r`), `tc` version, ns-3 commit, Mininet version, CPU model, governor, seed, config hash.
- **Optional OMNeT++/INET backend.** The spec compiler can gain a fourth target that emits INET `.ini` and `.ned` files. Keep it out of the minimum evidence package; use it only if it adds a discrete-event backend with different timing semantics and the three core backends are already complete.
- One-command reproduction: `python -m experiments.reproduce --paper <id> --backend tc --small`.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Convenience sample invalidates prevalence claims | Preregistered inclusion criteria, logged search, report prevalence only for the defined population |
| Unrecorded kernel or hardware effects misclassified as emulator effects | Record kernel, CPU, governor, and load per run; include host as a random effect; second-host validation |
| Checklist without a validated measure is incremental | CSI validated on held-out experiments; predictive validity is a headline result |
| Artifact rot prevents reconstruction | Pin container images; keep a reconstruction log; drop and replace artifacts using the same criteria |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 20).** Fewer than 12 reconstructable artifacts → widen the venue list once; if still below 12, stop and switch to Topic 05.
- **Gate 2 (Day 55).** No factor explains a meaningful share of variance and no reversals → reframe as "stability bounds" paper for TNSM; do not claim prediction.
- **Stop.** Artifact sample cannot be reconstructed, or no general factors emerge across papers.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 closest papers; build claim–method–data–limitation matrix; reproduce one artifact end-to-end on one backend |
| Days 15–30 | Freeze inclusion criteria, factor list, CSI definition, mixed-model specification, and stop conditions; spec compiler working for 3 backends on 2 papers |
| Days 31–60 | Pilot on 6 papers across 3 backends; estimate variance and runtime; attempt the hardest artifact; decide trial counts |
| Days 61–90 | Preregistered run on remaining papers plus held-out validation; second-host replication; package artifact; draft around RQ1–RQ3 |

## 12. Journal strategy

- **ToN** if the paper establishes a general experimental principle and connects instability to transport behavior (for example, which algorithm properties make claims fragile).
- **TNSM** if the main contribution is the operational benchmarking and reproducibility framework.
- Decide at Gate 2 based on whether the mechanism story (ToN) or the framework story (TNSM) is better supported. Write the cover letter around fit, not impact.

## 13. Ethics and disclosure

No human subjects. Contact original authors when a claim reverses, before publication, and offer them the reproduction package. Frame results as stability boundaries, not as errors by the original authors.

## 14. Folder layout

```
01-network-claim-stability/
├── RESEARCH_STRATEGY.md
├── literature/      closest-work.md, search-log.csv, inclusion-decisions.csv
├── experiments/     spec/, backends/, runs/ (raw), analysis/ (derived), reproduce.py
└── paper/           manuscript, figures, cover-letter.md
```
