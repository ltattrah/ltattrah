# Topic 15 — Cumulative Effects of Repeated Consent Manipulation on Preference Alignment and Privacy Fatigue

**Area:** Information systems
**Original topic:** Dark Patterns, Privacy Fatigue, and Consent Quality in Digital Information Systems

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 52 |
| Upgraded potential | 82 |
| Priority | Medium |
| Decision | Make the design longitudinal |
| Laptop fit | Compute excellent; participant burden high |
| Primary journal | Information Systems Research (ISR) |
| Secondary journal | ACM Transactions on Computer-Human Interaction (TOCHI) |
| Main risk | Single-screen experiments are saturated |
| Portfolio order | Not in top six; do not recruit until theory, power, ethics, and budget are complete |

**Audit verdict.** Retain only as a longitudinal study of cumulative effects and recovery. A one-screen A/B test should not be submitted to a high-impact journal.

## 1. Objective

Test whether **repeated** manipulative consent encounters reduce the alignment between users' stated data-sharing preferences and their choices through measurable fatigue, and whether a **persistent neutral control** (privacy dashboard, neutral defaults, cooling-off summary) restores alignment more effectively than a one-time disclosure, using a multi-session longitudinal design.

## 2. Why the original framing fails

Dark pattern taxonomies, large-scale audits (Mathur et al. [40]; Nouwens et al. [42]), and consent banner experiments including future effects (Bielova et al. [41]) are established. A one-session comparison of defaults or button colors is too close to existing work. The gap is **cumulative exposure, preference alignment over time, recovery, and durability of fatigue**.

## 3. Defensible contribution

> Repeated manipulative consent encounters reduce preference-choice alignment through measurable fatigue, and a persistent neutral control can restore alignment more effectively than a one-time disclosure.

## 4. Research questions and hypotheses

- **RQ1.** Does preference-choice alignment decline with repeated exposure to manipulative consent interfaces, and is the decline mediated by fatigue rather than by changed preferences?
- **RQ2.** Do recovery conditions (persistent dashboard, neutral defaults, cooling-off summary) restore alignment, and does restoration persist after the manipulation ends?
- **RQ3.** Which manipulation dimensions (asymmetry, default, complexity, repetition) drive fatigue, under a parsimonious factorial design?

Hypotheses:

- **H1.** Alignment declines over sessions in manipulative conditions (treatment × time interaction); fatigue mediates.
- **H2.** Persistent neutral controls restore alignment more than a one-time disclosure, and the effect persists in the post-manipulation session.
- **H3.** Repetition and complexity contribute more to fatigue than default direction alone.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Mathur et al. [40] | Dark patterns at scale (crawl) | Prevalence; no user effects over time |
| Bielova et al. [41] | Present and future effects of consent designs | Two time points; here multi-session cumulative exposure and recovery |
| Nouwens et al. [42] | Consent popups after GDPR and their influence | Single-session influence |
| Privacy fatigue scales | Measurement of fatigue | Used and validated within a longitudinal manipulation |
| Choice architecture and nudge persistence | Durability of nudges | Applied to consent with recovery interventions |

## 6. Study design

### Phase A — Preferences and measures (Days 1–30)
1. Elicit data-sharing preferences in plain language *before* treatment, separate from the experimental interface; this is the alignment reference.
2. Validate fatigue and perceived-control measures; preregister; power analysis for treatment × time interactions with expected attrition.

### Phase B — Longitudinal exposure (Days 25–70)
1. Several sessions (for example 5–8 over 3–4 weeks) of realistic consent decisions in a simulated service environment.
2. Parsimonious factorial: asymmetry, default, complexity, repetition; randomize at participant level.
3. Realistic but non-sensitive incentives tied to choices.

### Phase C — Recovery and persistence (Days 55–90)
1. Recovery conditions introduced mid-study: persistent privacy dashboard, neutral defaults, cooling-off summary, vs one-time disclosure.
2. Final session after manipulation ends measures persistence.
3. Outcomes: preference alignment, comprehension, reversals, regret, fatigue, perceived control, abandonment, persistence.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Sample | Longitudinal, powered for treatment × time interactions |
| Measures | Validated fatigue and control scales; objective choice alignment |
| Attrition | Analysis and sensitivity to differential attrition |
| Preregistration | Full |
| Ethics | Full protocol |

## 8. Artifact and tooling plan

- Simulated service environment as a web app (Python backend) logging every consent interaction with timestamps.
- Analysis in Python (`statsmodels` mixed models for treatment × time; mediation via `semopy`); preregistered scripts.
- Anonymized data release under ethics approval.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Attrition creates selection bias | Incentives for completion; attrition modelling; inverse-probability weights; report bounds |
| Hypothetical choices lack stakes | Realistic non-sensitive incentives tied to choices |
| Too many factors blur the mechanism | Parsimonious factorial; preregistered primary contrast |
| Saturated single-screen literature | Longitudinal cumulative and recovery design is the contribution |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 30).** No ethics approval, power analysis, and recruitment budget → do not recruit; pause the topic.
- **Gate 2 (Day 45).** Pilot attrition so high that powered completion is infeasible → redesign sessions before continuing.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers; extract effect sizes; submit ethics application; secure budget |
| Days 15–30 | Freeze theory, factorial design, measures, recovery conditions, analysis plan; preregister; build environment |
| Days 31–60 | Pilot with a small cohort over 2 weeks; attrition, variance, timing |
| Days 61–90 | Launch the main longitudinal cohort (completion may extend beyond 90 days); package materials; draft theory and methods |

## 12. Journal strategy

- **ISR** if the article develops theory about repeated digital choice and platform design.
- **TOCHI** for a stronger interaction-design and human-autonomy contribution.

## 13. Ethics and disclosure

Ethics approval before recruitment; informed consent covering manipulative interfaces; debriefing; no collection of actual sensitive data (choices are about simulated data categories).

## 14. Folder layout

```
15-cumulative-consent-manipulation/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     preferences/, environment/, design/, preregistration/, cohorts/, analysis/
└── paper/
```
