# Paper outline — Topic 13

**Working title.** When Explanations Transfer Confidence Without Improving Accuracy: A Multi-Study Test of Calibrated Reliance

**Primary target.** Information Systems Research (ISR)  
**Secondary target.** MIS Quarterly (MISQ)

**One-sentence contribution.**
> Explanations can transfer confidence from the AI to the user independently of decision accuracy, and feedback or reflection can interrupt that transfer under identifiable task conditions.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. Does explanation fluency increase perceived understanding and user confidence even when recommendation correctness is held constant or manipulated to be wrong?
   - RQ2. Does confidence transfer persist across repeated work decisions with delayed outcome feedback, and does it persist after AI assistance ends?
   - RQ3. Under what task conditions (difficulty, initial self-confidence, explanation plausibility) do feedback or reflection interventions restore calibrated reliance?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1a (transfer). Fluent explanations raise confidence regardless of correctness; calibration worsens.
- H1b (diagnostic). Fluent explanations raise confidence only for correct recommendations; calibration improves.
- H2. Delayed feedback reduces transfer over rounds; reflection prompts reduce it within rounds.
- H3. Transfer is strongest under high difficulty and low initial self-confidence.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
