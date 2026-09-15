# Topic 10 — How Insecure Infrastructure Templates Propagate and Persist Across Repository Lineages

**Area:** Computer security
**Original topic:** Security Debt in Container and Infrastructure-as-Code Templates

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 54 |
| Upgraded potential | 85 |
| Priority | High after redesign |
| Decision | Shift from prevalence to lineage |
| Laptop fit | Good |
| Primary journal | IEEE Transactions on Dependable and Secure Computing (TDSC) |
| Secondary journal | IEEE Transactions on Software Engineering (TSE) |
| Main risk | Security smell studies already mature |
| Portfolio order | 6 of 6 |

**Audit verdict.** Retain only the lineage, repair-diffusion, and triage contribution. Remove broad claims about discovering new security smells unless the audit finds a genuinely missing class.

## 1. Objective

Establish **template lineage** as an explanatory variable for recurring infrastructure security debt: reconstruct how vulnerable fragments spread through templates, forks, tutorials, generators, and copied files across two ecosystems; measure how downstream repair lags upstream fixes; and show that provenance-aware triage improves on existing scanners.

## 2. Why the original framing fails

Security smells in IaC were established in 2019 (Rahman et al. [26]); practice adoption has been measured (Verdet et al. [27]); a 2025 taxonomy extends the field and includes an evolution study (War et al. [28]). Another scanner and prevalence count is not novel. The gap is **causal provenance** and **repair diffusion**.

## 3. Defensible contribution

> Template lineage explains a substantial share of recurring infrastructure security debt, and upstream corrections diffuse unevenly according to repository dependency and copy relationships.

## 4. Research questions and hypotheses

- **RQ1.** What fraction of high-confidence security-rule violations in Terraform modules and Kubernetes/Helm templates can be attributed, with quantified uncertainty, to an inherited fragment rather than to independent authoring?
- **RQ2.** After an upstream fix, how is downstream repair lag distributed, and does it differ between dependency-linked (module reference) and copy-linked (fork, paste) lineages?
- **RQ3.** Does provenance-aware triage (collapsing duplicate warnings, prioritizing inherited flaws with verified exposure) reduce reviewer effort per true positive compared with existing scanners?

Hypotheses:

- **H1.** Inherited fragments account for a substantial preregistered share of recurring violations, higher in Helm charts than in Terraform modules.
- **H2.** Copy-linked lineages have longer and heavier-tailed repair lag than dependency-linked lineages.
- **H3.** Provenance-aware triage reduces warnings per true positive without reducing recall of verified-exposure flaws.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Rahman et al. [26] | Seven security smells in IaC | Smell definitions reused; no lineage |
| Verdet et al. [27] | Security practices in IaC | Practice adoption; no provenance |
| War et al. [28] | Taxonomy update and evolution | Evolution within repos; this study tracks fragments *across* repos and estimates repair diffusion |
| Code clone and provenance studies (Stack Overflow snippet propagation) | Snippet copying in application code | Adapted to IaC templates with deployment exposure rules |
| Vulnerability propagation in package ecosystems | Dependency-graph diffusion | Adds copy-based lineage and mixed-uncertainty edges |

## 6. Study design

### Phase A — Ecosystems and rules (Days 1–25)
1. Two ecosystems: Terraform modules; Kubernetes manifests and Helm charts.
2. High-confidence rules only, tied to deployment exposure (for example public ingress with no auth, privileged containers, wildcard IAM, unencrypted storage with public access). Document precision on a manually labelled sample before use.

### Phase B — Lineage construction (Days 20–55)
1. Collect thousands of repositories via the GitHub API and registry metadata, with logged sampling criteria.
2. Fragment extraction: normalize templates (AST-level for HCL and YAML), hash fragments, compute token similarity.
3. Lineage edges from: repository ancestry (forks), commit timestamps, token similarity above a threshold, template dependencies (module source, chart dependencies), provenance metadata (README attributions, generator markers).
4. Quantify edge uncertainty (probability of copy vs independent authoring) with a calibrated model validated on hand-labelled edges.

### Phase C — Repair diffusion (Days 45–75)
1. Identify upstream fixes (commits that remove a violation in a source fragment).
2. Estimate downstream repair lag; use matched comparison (similar repos without upstream fix) or interrupted time series to separate diffusion from unrelated edits.

### Phase D — Triage tool and validation (Days 65–90)
1. Provenance-aware triage: collapse duplicate warnings across a lineage, prioritize inherited flaws with verified exposure.
2. Manual validation of a stratified sample of findings; responsible disclosure for live exposures.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Repositories | Thousands |
| Validated lineages | Hundreds |
| Rules | High precision, documented on labelled sample |
| Repair lag | Distributions per lineage type |
| Uncertainty | Edge-level, propagated to share estimates |
| Triage | Warnings per true positive vs existing scanners (Checkov, tfsec, kube-linter) |

## 8. Artifact and tooling plan

- Python mining pipeline (`PyGithub`/GraphQL, `python-hcl2`, `ruamel.yaml`), fragment hashing, similarity via MinHash (`datasketch`).
- Lineage graph in `networkx`; uncertainty model in `scikit-learn`; survival analysis for repair lag in `lifelines`.
- Rule engine wraps existing scanners and filters to the high-confidence subset.
- Anonymized derived dataset released; raw repository content referenced by commit hash.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Similarity does not prove copying or causation | Multi-signal edges with calibrated uncertainty; hand-labelled validation; matched or interrupted-time comparisons |
| 2025 taxonomy already covers persistence and evolution | Position explicitly: cross-repository lineage and repair diffusion, not within-repo evolution |
| Context-dependent warnings create false positives | High-confidence rule subset; exposure verification; report precision |
| Ethical exposure of live misconfigurations | Responsible disclosure; anonymized release |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 55).** Copy lineage cannot be inferred with acceptable precision on hand-labelled edges → stop (portfolio stop condition).
- **Gate 2 (Day 75).** Repair-lag comparison confounded beyond repair → drop RQ2 claims and reframe around triage.

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on IaC security, clone provenance, ecosystem propagation; run an existing scanner on a sample; verify API access |
| Days 15–30 | Freeze ecosystems, rules, lineage signals, uncertainty model, metrics, stop conditions; small deterministic pipeline |
| Days 31–60 | Pilot on a few hundred repositories; label edges; estimate precision; attempt one repair-lag estimate |
| Days 61–90 | Full mining; diffusion analysis; triage evaluation; disclosure; package; draft |

## 12. Journal strategy

- **TDSC** for the systemic security and dependable-infrastructure framing.
- **TSE** for a longitudinal software-evolution and tool study with strong causal care.

## 13. Ethics and disclosure

Public repositories only, under GitHub terms. Responsible disclosure of live exposures to repository owners. No naming of individual maintainers.

## 14. Folder layout

```
10-infrastructure-template-lineage/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     mining/, rules/, lineage/, labels/, diffusion/, triage/, analysis/
└── paper/
```
