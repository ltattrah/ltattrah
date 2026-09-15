# Paper outline — Topic 12

**Working title.** Capability-Safe Retrieval-Augmented Generation with Provenance-Enforced Control Flow Under Adaptive Indirect Prompt Injection

**Primary target.** IEEE Transactions on Dependable and Secure Computing (TDSC)  
**Secondary target.** ACM Transactions on Privacy and Security (TOPS)

**One-sentence contribution.**
> Provenance-tagged context and an external capability policy can prevent unauthorized actions even when an adaptive attacker controls retrieved text and the model follows the injected instruction.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. With provenance propagation and an external capability policy, what fraction of adaptive injection attempts result in unauthorized action or data exposure, compared with filtering, defensive prompting, StruQ, and strict no-tool policies?
   - RQ2. What benign-utility, refusal, latency, and policy-error cost does the design impose across document QA, email/support workflows, and a tool-using task, for three quantized local models?
   - RQ3. Which components (provenance tags, control-flow separation, capability checks, argument-taint rules) contribute to security and to utility loss, and do results hold on a held-out model family?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Unauthorized-action rate under adaptive attack is near zero for the capability-safe design and is bounded by the policy, not by the model's compliance; prompting and filtering fail under adaptation.
- H2. The design's utility loss on benign tasks is smaller than that of the strict no-tool policy and comparable to StruQ.
- H3. Removing provenance propagation (keeping only capability checks) reopens data-exposure paths through tool arguments.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
