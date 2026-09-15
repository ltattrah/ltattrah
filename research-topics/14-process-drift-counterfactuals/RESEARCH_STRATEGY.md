# Topic 14 — From Process Drift Alerts to Action: Counterfactual Explanations for Operational Diagnosis

**Area:** Information systems
**Original topic:** Detecting and Explaining Business Process Drift from Enterprise Event Logs

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 56 |
| Upgraded potential | 84 |
| Priority | Medium-high |
| Decision | Move from explanation to action |
| Laptop fit | Good |
| Primary journal | Information Systems |
| Secondary journal | Decision Support Systems (DSS) |
| Main risk | Explainable drift already established |
| Portfolio order | Not in top six |

**Audit verdict.** A credible mid-to-high priority topic after changing the dependent variable from explanation quality to diagnosis and intervention quality.

## 1. Objective

Generate **process-feasible counterfactual explanations** for detected drift (the smallest actionable changes that would restore a target outcome) from object-centric or multi-perspective event data, and show in a preregistered analyst study that they improve diagnosis accuracy and intervention selection over alert-only and feature-importance explanations.

## 2. Why the original framing fails

Explainable process drift is established, including a framework linking drift across perspectives and causal relationships (Adams et al. [38]) and work on causal explainability of temporal deviations [39]. Detecting a change and listing affected activities is incremental. The dependent variable must be **diagnosis and intervention quality**.

## 3. Defensible contribution

> Counterfactual process explanations that identify the smallest actionable changes needed to restore a target outcome improve analyst diagnosis compared with alert-only and feature-importance explanations.

## 4. Research questions and hypotheses

- **RQ1.** Can counterfactuals over resource, control-flow, timing, and outcome perspectives be generated under process-feasibility constraints with acceptable fidelity and stability on controlled and natural drift?
- **RQ2.** Do counterfactual explanations improve analyst diagnosis accuracy, intervention selection, and time, and reduce inappropriate actions, relative to alert-only, before/after diagrams, feature ranking, and existing explainable-drift output?
- **RQ3.** Which drift types (seasonality, case mix, workload, structural change) are diagnosed better, and where do counterfactuals mislead?

Hypotheses:

- **H1.** Constrained counterfactuals achieve higher fidelity and stability than unconstrained ones at a modest sparsity cost.
- **H2.** Analysts with counterfactuals select the correct intervention more often and take fewer inappropriate actions than with feature ranking.
- **H3.** Gains are largest for structural process change and smallest for seasonality, where counterfactuals may suggest spurious interventions.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Adams et al. [38] | Explainable concept drift detection in process mining | Explanation of drift; here counterfactual action recommendations and a human evaluation |
| Causal explainability of temporal deviations [39] | Causal explanations | Causal attribution; here minimal actionable changes under feasibility constraints |
| Counterfactual explanations in predictive process monitoring | Case-level counterfactuals for predictions | Applied at the drift (population) level for diagnosis |
| Object-centric process mining | Multi-object event representation | Used as the representation |
| Decision-support user studies | Evaluate decision quality | Provides the study-design template |

## 6. Study design

### Phase A — Representation and scenarios (Days 1–30)
1. Object-centric or multi-perspective event representation so resource, control-flow, timing, and outcome changes are distinguishable.
2. Controlled drift library: inject seasonality, case-mix shift, workload change, structural change with known causes into public logs; plus naturally changing public logs.

### Phase B — Counterfactual generation (Days 20–55)
1. Define target outcome (for example throughput time, rework rate) and feasibility constraints (process model conformance, resource availability, precedence).
2. Generate minimal counterfactual changes (search over actionable variables under constraints); measure fidelity (does applying the change restore the outcome in simulation/replay) and stability (across bootstrap samples).
3. Baselines: alert-only, before/after process diagrams, feature importance ranking, existing explainable-drift framework output.

### Phase C — Analyst study (Days 50–90)
1. Preregistered between-subjects study with analysts or advanced students; within-subject scenarios.
2. Measures: diagnosis accuracy, intervention selection, time, explanation fidelity rating, inappropriate action rate.
3. Power analysis for the primary contrast (counterfactual vs feature ranking).

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Logs | Several public logs |
| Scenarios | Library of controlled drift with known causes |
| Explanation tests | Fidelity and stability |
| User study | Sufficiently powered, preregistered |
| Outcomes | Diagnosis accuracy, intervention selection, time, fidelity, inappropriate actions |

## 8. Artifact and tooling plan

- Python with `pm4py` for logs and object-centric event data; drift injection library; counterfactual search in Python (constraint handling via `ortools` or custom search).
- Study interface in `oTree` or a web app with pre-rendered explanations.
- Analysis in `statsmodels`; preregistered scripts.
- One-command reproduction of counterfactual generation on one scenario.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Counterfactuals violate process constraints | Feasibility constraints in the generator; conformance check on every counterfactual |
| Injected drift is easier than real change | Natural-drift logs alongside injections; report both |
| Small user study overstates value | Power analysis; preregistration; effect sizes with intervals; inappropriate-action metric |
| Explanation quality vs decision quality conflated | Decision quality is the primary outcome |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 55).** Counterfactual fidelity on controlled scenarios below a preregistered floor → stop.
- **Gate 2 (Day 60).** No ethics approval or participant access for the study → publish technical part as a workshop paper only.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers; reproduce Adams et al.-style drift detection on one log; submit ethics application |
| Days 15–30 | Freeze representation, scenarios, counterfactual definition, baselines, metrics, study design, stop conditions; small deterministic generator |
| Days 31–60 | Pilot generation on all logs; fidelity and stability; pilot study interface with a few participants |
| Days 61–90 | Preregistered analyst study; analysis; package; draft |

## 12. Journal strategy

- **Information Systems** for process models, data management, and implemented methods.
- **DSS** when the main evidence is improved human diagnosis and intervention.
- ISR or JAIS would need a deeper organizational theory contribution; not the default target.

## 13. Ethics and disclosure

Ethics approval before recruitment; informed consent; public logs under license.

## 14. Folder layout

```
14-process-drift-counterfactuals/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     representation/, scenarios/, counterfactuals/, baselines/, study/, analysis/
└── paper/
```
