# Topic 13 — When Explanations Transfer Confidence Without Improving Accuracy: A Multi-Study Test of Calibrated Reliance

**Area:** Information systems
**Original topic:** AI Explanations, Decision Quality, and User Confidence

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 51 |
| Upgraded potential | 80 |
| Priority | Medium-low |
| Decision | Add theory and a second study |
| Laptop fit | Compute excellent; participant burden high |
| Primary journal | Information Systems Research (ISR) |
| Secondary journal | MIS Quarterly (MISQ) |
| Main risk | Crowded explanation literature |
| Portfolio order | Not in top six; do not recruit until theory, power, ethics, and budget are complete |

**Audit verdict.** Do not pursue as a single interface experiment. It becomes credible with a new confidence-transfer mechanism, two powered studies, and an organizational decision context.

## 1. Objective

Develop and test a theory of **confidence transfer**: explanations move confidence from the AI to the user independently of decision accuracy, and feedback or reflection can interrupt that transfer under identifiable task conditions. Two preregistered, powered studies: a mechanism study and a repeated-decision organizational study with delayed feedback.

## 2. Why the original framing fails

Explanations, trust, and overreliance are extensively studied. Explanations do not automatically reduce overreliance (Vasconcelos et al. [35]); a 2026 systematic review maps explanation effects (Reinhard et al. [37]). A single online experiment comparing explanation formats lacks theory and external validity for ISR or MISQ.

## 3. Defensible contribution

> Explanations can transfer confidence from the AI to the user independently of decision accuracy, and feedback or reflection can interrupt that transfer under identifiable task conditions.

## 4. Research questions and hypotheses

- **RQ1.** Does explanation fluency increase perceived understanding and user confidence even when recommendation correctness is held constant or manipulated to be wrong?
- **RQ2.** Does confidence transfer persist across repeated work decisions with delayed outcome feedback, and does it persist after AI assistance ends?
- **RQ3.** Under what task conditions (difficulty, initial self-confidence, explanation plausibility) do feedback or reflection interventions restore calibrated reliance?

Competing hypotheses (both stated):

- **H1a (transfer).** Fluent explanations raise confidence regardless of correctness; calibration worsens.
- **H1b (diagnostic).** Fluent explanations raise confidence only for correct recommendations; calibration improves.
- **H2.** Delayed feedback reduces transfer over rounds; reflection prompts reduce it within rounds.
- **H3.** Transfer is strongest under high difficulty and low initial self-confidence.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Vasconcelos et al. [35] | Explanations can reduce overreliance under cost conditions | Focuses on effort; here the mechanism is confidence transfer and its persistence |
| Human-aware confidence communication [36] | Communicating AI confidence | Confidence *display*; here confidence *transfer* via explanation fluency |
| Reinhard et al. [37] | Systematic review of explanation effects | Positions the gap: mechanism plus persistence in organizational decisions |
| Fluency and metacognition literature | Processing fluency raises judged truth | Imported as the theoretical mechanism |
| Appropriate reliance / calibration studies | Measure reliance behavior | Add repeated decisions, delayed feedback, post-assistance persistence |

## 6. Study design

### Phase A — Theory and measures (Days 1–30)
1. Theoretical model: explanation fluency → perceived understanding → confidence transfer → (mis)calibrated reliance; moderators: task difficulty, initial self-confidence, explanation plausibility; interventions: feedback, reflection.
2. Measurement: validated constructs where they exist; new items piloted; behavioral reliance measured separately from self-reported trust.
3. Power analysis for interactions and mediation; preregistration drafted.

### Phase B — Study 1: mechanism (Days 25–60)
1. Controlled online experiment: manipulate recommendation correctness, explanation plausibility, task difficulty; measure initial self-confidence.
2. Outcomes: decision accuracy, confidence, calibration (confidence minus accuracy), reliance switching.
3. Manipulation and comprehension checks; preregistered exclusions.

### Phase C — Study 2: repeated organizational decisions (Days 50–90)
1. Different task and population (for example procurement or scheduling decisions with professional or advanced student participants).
2. Repeated rounds, delayed outcome feedback, realistic incentives; assistance withdrawn in final rounds to test persistence.
3. Mixed-effects models with participant and item random effects.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Participants | Several hundred across two studies, powered for interactions and mediation |
| Constructs | Validated; manipulation and comprehension checks |
| Outcomes | Objective decision accuracy, calibration, behavioral reliance, persistence after assistance ends |
| Replication | Across tasks and populations |
| Preregistration | Design, measures, exclusions, analysis |

## 8. Artifact and tooling plan

- Experiment implemented in Python (`oTree`) or a web framework with a fixed AI-recommendation script (no live model needed; recommendations and explanations pre-generated and pinned).
- Analysis in Python (`statsmodels` mixed models, `pingouin`/`semopy` for mediation) with preregistered scripts committed before data collection.
- Anonymized data and materials released under ethics approval.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Effect is task-specific or driven by explanation length | Length-matched explanations; two tasks and two populations |
| Self-reported trust diverges from reliance | Behavioral reliance is the primary outcome |
| Recruitment and ethics dominate timeline | Start ethics and budget in Days 1–14; Gate 1 below |
| Crowded literature | Theory-first framing with competing hypotheses; persistence and organizational context |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 30).** No ethics approval, power analysis, and recruitment budget → do not recruit; pause the topic.
- **Gate 2 (Day 60).** Study 1 shows no confidence effect under any condition → do not run Study 2; write up as a null-result note.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers; extract effect sizes for power analysis; submit ethics application; secure budget |
| Days 15–30 | Freeze theoretical model, measures, hypotheses, analysis plan, exclusions; preregister; pilot interface with a small sample |
| Days 31–60 | Run Study 1; analysis per preregistration; decide Study 2 |
| Days 61–90 | Run Study 2 rounds (may extend beyond 90 days for delayed feedback); package materials; draft |

## 12. Journal strategy

- **ISR** for theory-driven empirical work across cognitive and organizational traditions.
- **MISQ** if the contribution to IT use, management, and societal implications is explicit and the two studies are strong.

## 13. Ethics and disclosure

Ethics approval before any recruitment. Informed consent, fair compensation, debriefing about manipulated recommendation correctness. No deception beyond what the ethics board approves.

## 14. Folder layout

```
13-explanation-confidence-transfer/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     theory/, measures/, preregistration/, study1/, study2/, analysis/
└── paper/
```
