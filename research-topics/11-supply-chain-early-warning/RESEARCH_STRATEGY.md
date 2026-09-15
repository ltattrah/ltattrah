# Topic 11 — Early Warning of Software Supply Chain Incidents with Positive-Unlabeled Temporal Risk Models

**Area:** Computer security
**Original topic:** Predicting Software Supply Chain Risk from Package Ecosystem Metadata

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 50 |
| Upgraded potential | 80 |
| Priority | Medium-low |
| Decision | Replace classification with early warning |
| Laptop fit | Good |
| Primary journal | IEEE Transactions on Dependable and Secure Computing (TDSC) |
| Secondary journal | IEEE Transactions on Information Forensics and Security (TIFS) |
| Main risk | Metadata detection already exists |
| Portfolio order | Not in top six |

**Audit verdict.** A difficult but viable topic only as an early-warning and triage study. Do not frame the model as predicting which maintainers or packages are malicious.

## 1. Objective

Estimate how much **lead time** public ecosystem changes provide before a documented supply-chain incident, under incomplete labels and a fixed analyst review budget, using positive-unlabeled (PU) and time-to-event models on as-of-date ecosystem snapshots. Outputs are review-priority curves and lead-time estimates, not package accusations.

## 2. Why the original framing fails

Metadata-based malicious package detection exists (Halder et al. [29]); MalGuard provides real-time actionable detection for PyPI [30]. A supervised classifier over registry metadata is weak. The gap is prospective early warning with honest handling of unlabeled data.

## 3. Defensible contribution

> Positive-unlabeled temporal models can estimate review priority and incident lead time without treating every unlabeled package as benign or publishing accusatory package scores.

## 4. Research questions and hypotheses

- **RQ1.** Reconstructing monthly ecosystem snapshots and incident labels *as known at each date*, what lead time do ownership churn, release anomalies, dependency reach, provenance indicators, maintenance activity, and name confusion provide before documented incidents?
- **RQ2.** Under a fixed analyst review budget, how do PU and survival models compare with naive supervised classification in incidents caught, lead time, calibration, and false-accusation risk?
- **RQ3.** How sensitive are conclusions to label incompleteness and selective reporting, and which package subgroups bear higher error?

Hypotheses:

- **H1.** Treating unlabeled packages as benign underestimates risk prevalence and inflates apparent precision; PU estimation corrects this by a measurable margin.
- **H2.** Ownership churn and name confusion carry the most lead time; release anomalies carry the least (they often coincide with the incident).
- **H3.** Expanding-window evaluation shows lead time is stable across years only for a subset of features.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Halder et al. [29] | Metadata-based malicious package detection | Cross-sectional classification; here temporal, as-of-date, PU |
| MalGuard [30] | Real-time detection for PyPI | Detection at publish time; here early warning before incident with lead time |
| OSSF malicious packages repo [31] | Incident labels | Used as the positive set, with discovery-time preserved |
| Survival analysis in software defect prediction | Time-to-event modelling | Applied to ecosystem incidents with PU correction |
| Package popularity and maintenance risk scores (Scorecard) | Heuristic risk scores | Baseline; not evaluated for lead time under a budget |

## 6. Study design

### Phase A — As-of-date data (Days 1–30) — feasibility gate
1. Reconstruct monthly snapshots (PyPI primarily; npm optionally) from registry metadata dumps and archives; record label discovery time and advisory publication time from OSSF and advisory databases.
2. If fewer than roughly one hundred credible incidents with reliable dates can be assembled, **narrow the outcome or abandon predictive claims**.

### Phase B — Modelling (Days 25–55)
1. PU learning (for example class-prior estimation with nnPU) and survival or time-to-event models; controls matched by package age, popularity, and ecosystem segment.
2. Features: ownership churn, release anomalies, dependency reach, provenance indicators (attestations, signed releases), maintenance activity, name confusion.
3. Automated leakage tests: every feature must be computable from data dated before the snapshot.

### Phase C — Budgeted evaluation (Days 45–80)
1. Expanding-window validation; alerts ranked under fixed review budgets (for example 50, 200, 1000 packages per month).
2. Report incidents caught, lead time distribution, calibration, false-accusation risk (unlabeled flagged that never become incidents, with uncertainty), subgroup error.

### Phase D — Label uncertainty (Days 70–90)
1. Sensitivity to label incompleteness (simulate hidden positives) and selective reporting.
2. Keep package-level predictions private; publish only aggregate curves.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Snapshots | Several years, monthly |
| Incidents | Enough for stable estimation (target ≥ 100) |
| Validation | Expanding window |
| Curves | Analyst budget vs incidents caught and lead time |
| Uncertainty | Label uncertainty analysis |
| Baselines | Naive supervised classifier, heuristic scorecards, random under budget |

## 8. Artifact and tooling plan

- Python (`pandas`, `scikit-learn`, `lifelines`, PU implementations); snapshot builder from registry dumps with hashes.
- Leakage test suite runs as part of CI for the pipeline.
- Release: aggregate results, feature definitions, and code; no package-level scores.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Incomplete, selectively reported labels | PU estimation, discovery-time preservation, sensitivity analysis |
| Unusual maintenance behavior misread as malicious | Frame outputs as review priority; never publish per-package scores; subgroup error reported |
| Public scores harm maintainers | Private predictions; ethics statement; aggregate publication only |
| Leakage from future data | Automated leakage tests, as-of-date reconstruction |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 30).** Fewer than ~100 credible dated incidents → narrow outcome (for example typosquat incidents only) or abandon predictive claims.
- **Gate 2 (Day 80).** No feature set provides lead time beyond a trivial baseline under any budget → stop.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers; verify registry dump and advisory access; reproduce one metadata-detection baseline |
| Days 15–30 | Freeze snapshot rules, incident definition, features, models, budgets, metrics, stop conditions; small deterministic snapshot builder |
| Days 31–60 | Pilot on two years of snapshots; variance; hardest baseline; one held-out year |
| Days 61–90 | Full preregistered evaluation; label uncertainty; package; draft |

## 12. Journal strategy

- **TDSC** for a careful ecosystem risk and dependability study.
- **TIFS** if the detection mechanism and adversarial robustness (attacker adapting features) are central.

## 13. Ethics and disclosure

No package-level accusations. Registry data under terms of use. Ethics statement on maintainer harm. Coordinate with ecosystem security teams before any public release of aggregate findings that could identify packages.

## 14. Folder layout

```
11-supply-chain-early-warning/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     snapshots/ (manifests), incidents/, features/, models/, leakage-tests/, evaluation/, analysis/
└── paper/
```
