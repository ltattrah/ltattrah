# Topic 04 — Detectability-Preserving Adaptive Flow Sampling for Rare Network Attacks Under Fixed Telemetry Budgets

**Area:** Computer networking
**Original topic:** Sampling-Induced Blind Spots in Flow-Based Anomaly Detection

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 55 |
| Upgraded potential | 82 |
| Priority | Medium |
| Decision | Add a new method |
| Laptop fit | Good |
| Primary journal | IEEE Transactions on Network and Service Management (TNSM) |
| Secondary journal | IEEE Transactions on Dependable and Secure Computing (TDSC) |
| Main risk | Known sampling effect |
| Portfolio order | Not in top six |

**Audit verdict.** Keep the problem but change the output from an audit to a sampling algorithm with explicit cost and bias accounting. Use simple detectors unless a more complex model is necessary for the research question.

## 1. Objective

Design a **rarity- and uncertainty-aware flow sampler** that records inclusion probabilities, preserves the detectability of sparse attacks at the same byte and record budget as uniform sampling, and supports bias-corrected estimates of prevalence. The output is a method, a bound or controlled approximation, and an equal-budget comparison.

## 2. Why the original framing fails

Sampling's effect on anomaly detection was studied at IMC 2006 (Mai et al. [16]) and remains active [17][18]. Quantifying accuracy loss on public intrusion datasets is not enough. The article needs a **new mechanism**, a **cost model**, and a **bias-aware evaluation**.

## 3. Defensible contribution

> A rarity- and uncertainty-aware sampler with recorded inclusion probabilities can preserve detectability of sparse attacks and support corrected estimates at the same telemetry cost as uniform sampling.

## 4. Research questions and hypotheses

- **RQ1.** At equal byte and record budgets, does the adaptive sampler retain more attack evidence (per-attack recall, detection delay) than uniform packet, uniform flow, hash-based, sample-and-hold, heavy-hitter, and active-uncertainty baselines?
- **RQ2.** When are inverse-probability-corrected prevalence estimators stable under adaptive sampling, and what is the detectability bound (or controlled empirical approximation) as a function of budget and attack rarity?
- **RQ3.** Does the detectability gain transfer across chronologically partitioned datasets and survive mislabeled or duplicated flows?

Hypotheses:

- **H1.** Adaptive sampling improves per-attack recall for the rarest attack classes at equal budget with no worse false positives per hour.
- **H2.** Corrected prevalence estimates have bounded bias when minimum inclusion probability is floored; unfloored adaptive sampling produces unstable estimates.
- **H3.** Gains persist on a dataset not used for design, and degrade gracefully under injected label noise and duplicate flows.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Mai et al. [16] | Shows sampling hurts anomaly detection | Establishes the problem; no adaptive sampler |
| Campazas-Vega et al. [17] | Malicious traffic detection on sampled flows | Evaluation only |
| Alikhanov et al. [18] | Sampling effect on ML-based NIDS | Evaluation only |
| Sample-and-hold, sketch-based heavy hitters | Bias toward large flows | Baselines; the target here is *rare* evidence |
| Active learning / uncertainty sampling for NIDS | Chooses labels, not telemetry retention | Baseline; here retention is decided online under a byte budget with recorded probabilities |

## 6. Study design

### Phase A — Sampler design and cost model (Days 1–30)
1. Define the budget precisely: bytes stored, records stored, per-record processing cost. State the unit of retention (flow record, packet header, sketch update).
2. Derive the sampler: retention probability combines novelty (against a decayed sketch of seen tuples), rare destination or service evidence, and sketch-estimated change; floor the probability to keep estimators finite. Record inclusion probability for every retained record.
3. Establish a detectability bound: probability that at least k records of an attack with rate r are retained under budget B; or a controlled empirical approximation with stated assumptions.

### Phase B — Estimators (Days 20–45)
1. Inverse-probability (Horvitz–Thompson) correction for prevalence and feature aggregates.
2. Analyze stability: variance as a function of the probability floor; report when estimators fail.

### Phase C — Equal-budget evaluation (Days 35–75)
1. Datasets: ≥ 3 chronologically partitioned public flow datasets (design on one, evaluate on others), plus controlled sparse attack injections into benign traffic.
2. Recompute all features **after** sampling to avoid leakage.
3. Detectors: simple (logistic regression, isolation forest, threshold rules) unless the RQ demands more.
4. Baselines at equal byte and record budgets: uniform packet, uniform flow, hash-based, sample-and-hold, heavy-hitter, active-uncertainty.

### Phase D — Transfer and robustness (Days 65–90)
1. Cross-dataset transfer without re-tuning.
2. Sensitivity to mislabeled flows and duplicated flows (known shortcuts in public NIDS datasets).

## 7. Baselines, metrics, and minimum evidence

| Metric | Reported per |
|---|---|
| Precision and recall | Attack class |
| False positives per hour | Dataset, budget |
| Detection delay | Attack class |
| Calibration | Detector, budget |
| Records and bytes retained | Budget |
| Detection gain per storage unit | Method |
| Estimator bias and variance | Budget, floor |

Include cross-dataset transfer and label-noise sensitivity.

## 8. Artifact and tooling plan

- Python sampler with streaming sketches (count-min, HyperLogLog via `datasketch` or own implementation), `numpy` for probabilities, `pandas` for flow records.
- Attack injection tool that writes synthetic sparse attack flows with ground-truth labels into benign captures.
- **OMNeT++/INET option.** INET can generate controlled traffic mixes with known rare-attack flows for the injection scenarios when public data lack a needed pattern; export flow records via a Python post-processor. Public datasets remain the primary evidence.
- Every run stores: budget, seed, sampler parameters, dataset partition hash, inclusion probabilities file.
- One-command reproduction on one small dataset partition.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Public datasets contain shortcuts and duplicates | Deduplicate, report duplicate rates, run sensitivity analyses, use chronological partitions |
| Adaptive sampling biases prevalence estimates | Recorded inclusion probabilities with Horvitz–Thompson correction; report where correction fails |
| A deep detector distracts from the sampling contribution | Simple detectors by default; a complex detector only as a robustness check |
| Equal-budget comparison is unfair to a baseline | Match on both bytes and records; report both |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 30).** No bound or controlled approximation can be stated → reframe as purely empirical; TDSC target dropped.
- **Gate 2 (Day 75).** Adaptive sampler does not beat sample-and-hold and active-uncertainty at equal budget on the design dataset → stop.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on sampling, sketches, and NIDS evaluation pitfalls; reproduce Mai et al.-style degradation curve on one dataset |
| Days 15–30 | Freeze budget definition, sampler, estimator, dataset partitions, baselines, metrics, stop conditions; deterministic small artifact |
| Days 31–60 | Pilot on the design dataset with 3 budgets; variance and runtime; attempt the active-uncertainty baseline; one transfer test |
| Days 61–90 | Preregistered evaluation on held-out datasets and injections; robustness; package; draft |

## 12. Journal strategy

- **TNSM** for telemetry and deployability (lead with the cost model and equal-budget results).
- **TDSC** if the method has a security model (adversary aware of the sampler), strong cross-dataset evidence, and a dependable estimator.

## 13. Ethics and disclosure

Public datasets under their licenses; no collection from networks without authorization. No human subjects.

## 14. Folder layout

```
04-detectability-preserving-flow-sampling/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     sampler/, estimators/, injection/, datasets/ (manifests + hashes), runs/, analysis/
└── paper/
```
