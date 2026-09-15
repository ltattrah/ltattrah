# Paper outline — Topic 15

**Working title.** Cumulative Effects of Repeated Consent Manipulation on Preference Alignment and Privacy Fatigue

**Primary target.** Information Systems Research (ISR)  
**Secondary target.** ACM Transactions on Computer-Human Interaction (TOCHI)

**One-sentence contribution.**
> Repeated manipulative consent encounters reduce preference-choice alignment through measurable fatigue, and a persistent neutral control can restore alignment more effectively than a one-time disclosure.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. Does preference-choice alignment decline with repeated exposure to manipulative consent interfaces, and is the decline mediated by fatigue rather than by changed preferences?
   - RQ2. Do recovery conditions (persistent dashboard, neutral defaults, cooling-off summary) restore alignment, and does restoration persist after the manipulation ends?
   - RQ3. Which manipulation dimensions (asymmetry, default, complexity, repetition) drive fatigue, under a parsimonious factorial design?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Alignment declines over sessions in manipulative conditions (treatment × time interaction); fatigue mediates.
- H2. Persistent neutral controls restore alignment more than a one-time disclosure, and the effect persists in the post-manipulation session.
- H3. Repetition and complexity contribute more to fatigue than default direction alone.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
