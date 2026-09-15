# Paper outline — Topic 10

**Working title.** How Insecure Infrastructure Templates Propagate and Persist Across Repository Lineages

**Primary target.** IEEE Transactions on Dependable and Secure Computing (TDSC)  
**Secondary target.** IEEE Transactions on Software Engineering (TSE)

**One-sentence contribution.**
> Template lineage explains a substantial share of recurring infrastructure security debt, and upstream corrections diffuse unevenly according to repository dependency and copy relationships.

## Structure

1. **Introduction** — observable failure, why existing work does not settle it, contribution sentence, summary of evidence.
2. **Background and closest work** — the closest-work table (≥ 5 papers, exact differences) from `../literature/closest-work.md`.
3. **Problem formulation / semantic model / theory** — definitions, unit of analysis, threat model or constructs where applicable.
4. **Method** — the mechanism (oracle, sampler, policy, design) and its assumptions.
5. **Experimental / study design** — preregistered protocol, baselines, metrics, held-out evaluation.
6. **Results** — one subsection per research question, not per software component:
   - RQ1. What fraction of high-confidence security-rule violations in Terraform modules and Kubernetes/Helm templates can be attributed, with quantified uncertainty, to an inherited fragment rather than to independent authoring?
   - RQ2. After an upstream fix, how is downstream repair lag distributed, and does it differ between dependency-linked (module reference) and copy-linked (fork, paste) lineages?
   - RQ3. Does provenance-aware triage (collapsing duplicate warnings, prioritizing inherited flaws with verified exposure) reduce reviewer effort per true positive compared with existing scanners?
7. **Discussion** — measured findings vs plausible explanations; operational implications.
8. **Limitations and threats to validity** — from `RESEARCH_STRATEGY.md` section 9, updated with what was measured.
9. **Ethics and disclosure** statement.
10. **Artifact availability** — one-command reproduction, versions, seeds.

## Hypotheses to report (confirmed, refuted, or inconclusive)

- H1. Inherited fragments account for a substantial preregistered share of recurring violations, higher in Helm charts than in Terraform modules.
- H2. Copy-linked lineages have longer and heavier-tailed repair lag than dependency-linked lineages.
- H3. Provenance-aware triage reduces warnings per true positive without reducing recall of verified-exposure flaws.

## Figures and tables plan

| # | Content | Source script | RQ |
|---|---|---|---|
| T1 | Closest-work table | manual | — |
| T2 | Minimum evidence summary | `../experiments/analysis/` | all |
| F1 | Headline result | `../experiments/analysis/` | RQ1 |
