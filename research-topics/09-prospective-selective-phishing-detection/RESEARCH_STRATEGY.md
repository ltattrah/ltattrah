# Topic 09 — Prospective Selective Phishing Detection Under Campaign, Source, and Collection Shift

**Area:** Computer security
**Original topic:** Temporal Robustness of Lightweight Phishing URL Detectors

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 47 |
| Upgraded potential | 77 |
| Priority | Low unless data are unique |
| Decision | High-risk redesign |
| Laptop fit | Excellent |
| Primary journal | IEEE Transactions on Information Forensics and Security (TIFS) |
| Secondary journal | ACM Transactions on Privacy and Security (TOPS) |
| Main risk | Severely saturated topic |
| Portfolio order | Not in top six; lowest ranked |

**Audit verdict.** Do not pursue the original version. Continue only if a defensible longitudinal corpus and prospective protocol are available.

## 1. Objective

Show that **campaign-grouped and source-held-out evaluation** reveals deployment error hidden by standard splits, and that **selective prediction plus drift-triggered maintenance** preserves precision under a fixed review budget, evaluated prospectively. The contribution is evaluation and maintenance, not a new classifier.

## 2. Why the original framing fails

Phishing URL classification is saturated. Temporal evaluation is expected, not novel. A high-impact article must contribute a prospective benchmark or an operational maintenance mechanism, quantify label delay and source leakage, and evaluate at realistic false-positive budgets.

## 3. Defensible contribution

> Campaign-grouped and source-held-out evaluation reveals deployment error hidden by standard splits, while selective prediction and drift-triggered maintenance can preserve precision under a fixed review budget.

## 4. Research questions and hypotheses

- **RQ1.** How much of reported phishing-detector performance is optimism from random splits, source artifacts, and ignored label delay, measured on an 18-month timestamped multi-source corpus?
- **RQ2.** Under a fixed review budget, does a calibrated reject option combined with a cheap drift trigger maintain precision over an expanding-window prospective replay better than periodic retraining and no maintenance?
- **RQ3.** Which benign site classes and sources dominate false positives in prospective operation?

Hypotheses:

- **H1.** Source-held-out evaluation lowers precision at a fixed FPR by a substantial, preregistered margin relative to random splits.
- **H2.** Label-delay simulation shifts effective training data by weeks and measurably reduces early-campaign recall.
- **H3.** Selective prediction with drift-triggered retraining keeps selective risk within budget while periodic retraining alone does not.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Lexical / lightweight URL detectors | Compact feature classifiers | Reused as the model; contribution is evaluation and maintenance |
| Temporal-split phishing studies | Show decay over time | No campaign grouping, source hold-out, label delay, or prospective replay together |
| Concept drift in malware detection (Tesseract-style) | Time-aware evaluation | Adapted to URLs with campaign and source structure and a review budget |
| Selective classification | Reject option | Applied with drift triggers under a fixed analyst budget |
| Phishing feed studies (PhishTank, OpenPhish) | Feed characteristics | Feed artifacts are treated as confounders and measured |

## 6. Study design

### Phase A — Corpus (Days 1–30) — feasibility gate
1. Assemble ≥ 18 months of timestamped URLs from multiple malicious and benign sources; record first observation, label time, source, registered domain, campaign grouping (by registered domain, path template, and infrastructure clustering).
2. Document licenses and collection artifacts. If a unique corpus cannot be assembled, **stop**.

### Phase B — Evaluation protocol (Days 20–50)
1. Expanding-window evaluation; source-held-out tests; label-delay simulation (training uses only labels known at each date).
2. Random splits run only to quantify optimism.
3. Compact lexical and registration features; small models.

### Phase C — Maintenance mechanism (Days 40–70)
1. Calibrated reject option (temperature or isotonic calibration on the current window; abstain below confidence).
2. Cheap drift trigger (for example feature-distribution divergence or abstention-rate change) that requests retraining.
3. Fixed review budget: number of URLs a human can review per week.

### Phase D — Prospective replay (Days 60–90)
1. Weekly prospective replay or limited shadow deployment on the researcher's own mail or web filter proxy.
2. Audit false positives by benign site class and source.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Corpus | Unique, time-ordered, multi-source, ≥ 18 months |
| Metrics | Precision at fixed FPR, false positives per week, selective risk and coverage, calibration, lead time on campaigns |
| Transfer | Campaign and source transfer |
| Evaluation | Prospective replay or shadow deployment |
| Baselines | Random split (optimism), periodic retraining, no maintenance, threshold-only abstention |

## 8. Artifact and tooling plan

- Python pipeline (`pandas`, `scikit-learn`); feature extraction from URL lexical structure and registration data (`tldextract`, WHOIS/RDAP where licensed).
- Corpus manifest with per-record source, timestamps, and label time; raw feeds stored with hashes.
- Replay driver that enforces "known at date" constraints via automated leakage tests.
- One-command reproduction on a public subset with the same protocol.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Source artifacts dominate performance | Source-held-out evaluation is primary; report per-source results |
| Timestamps and ground truth delayed or wrong | Label-delay simulation; sensitivity to timestamp error |
| Another classifier comparison gets desk rejected | Keep the model compact and fixed; the paper is about evaluation and maintenance |
| Benign corpus unrepresentative | Multiple benign sources with site-class labels; FP audit by class |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 30).** No unique corpus with timestamps, label times, and multiple sources → stop; this topic is dropped.
- **Gate 2 (Day 70).** Maintenance mechanism does not beat periodic retraining under the budget → reframe as an evaluation-only note; not a TIFS submission.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers; verify feed access and licenses; reproduce one lightweight detector on a public dataset |
| Days 15–30 | Freeze protocol, corpus rules, metrics, budget, stop conditions; small deterministic replay |
| Days 31–60 | Pilot expanding-window replay on 6 months; variance; source hold-out; label-delay effect |
| Days 61–90 | Full preregistered replay; prospective weeks; FP audit; package; draft |

## 12. Journal strategy

- **TIFS** only with a strong detection or measurement contribution.
- **TOPS** is the more natural target for a careful security evaluation with transparent limitations.

## 13. Ethics and disclosure

Do not fetch or render phishing pages beyond URL metadata. Respect feed licenses. If shadow deployment touches real users' traffic, obtain ethics approval and consent.

## 14. Folder layout

```
09-prospective-selective-phishing-detection/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     corpus/ (manifests, hashes), features/, protocol/, maintenance/, replay/, analysis/
└── paper/
```
