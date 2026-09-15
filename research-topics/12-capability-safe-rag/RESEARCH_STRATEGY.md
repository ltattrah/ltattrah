# Topic 12 — Capability-Safe Retrieval-Augmented Generation with Provenance-Enforced Control Flow Under Adaptive Indirect Prompt Injection

**Area:** Computer security
**Original topic:** Indirect Prompt Injection Attacks and Defenses for Local Retrieval-Augmented Generation

## Audit snapshot

| Field | Value |
|---|---|
| Current score | 73 |
| Upgraded potential | 93 |
| Priority | Highest |
| Decision | Retain with systems focus |
| Laptop fit | Good |
| Primary journal | IEEE Transactions on Dependable and Secure Computing (TDSC) |
| Secondary journal | ACM Transactions on Privacy and Security (TOPS) |
| Main risk | Prompt filter only |
| Portfolio order | 3 of 6 (recommended primary for security) |

**Audit verdict.** A top-three recommendation. Keep the models small, but make the security boundary external, test adaptive attackers, and report utility costs honestly.

## 1. Objective

Design and evaluate a local RAG and tool-use system in which **every retrieved span and derived argument carries provenance**, operator instructions, user requests, retrieved data, and tool policies are separated in the control flow, and **tool capabilities are enforced by deterministic checks outside the model**. Show that unauthorized actions are prevented even when an adaptive attacker controls retrieved text and the model follows the injected instruction, and report the benign-utility cost honestly.

## 2. Why the original framing fails

Adaptive attacks bypass multiple indirect prompt injection defenses (Zhan et al. [32]); a 2026 study reports end-to-end attacks in RAG and agentic systems (Chang et al. [33]). Keyword filters and defensive prompts are not competitive. StruQ [34] is the structured-query baseline to beat. The contribution must be a **system design** that moves the security boundary outside the language model.

## 3. Defensible contribution

> Provenance-tagged context and an external capability policy can prevent unauthorized actions even when an adaptive attacker controls retrieved text and the model follows the injected instruction.

## 4. Research questions and hypotheses

- **RQ1.** With provenance propagation and an external capability policy, what fraction of adaptive injection attempts result in unauthorized action or data exposure, compared with filtering, defensive prompting, StruQ, and strict no-tool policies?
- **RQ2.** What benign-utility, refusal, latency, and policy-error cost does the design impose across document QA, email/support workflows, and a tool-using task, for three quantized local models?
- **RQ3.** Which components (provenance tags, control-flow separation, capability checks, argument-taint rules) contribute to security and to utility loss, and do results hold on a held-out model family?

Hypotheses:

- **H1.** Unauthorized-action rate under adaptive attack is near zero for the capability-safe design and is bounded by the policy, not by the model's compliance; prompting and filtering fail under adaptation.
- **H2.** The design's utility loss on benign tasks is smaller than that of the strict no-tool policy and comparable to StruQ.
- **H3.** Removing provenance propagation (keeping only capability checks) reopens data-exposure paths through tool arguments.

## 5. Closest work and the gap

| Work | What it does | How this differs |
|---|---|---|
| Zhan et al. [32] | Adaptive attacks break IPI defenses | Attack methodology reused; defense here is external and evaluated adaptively |
| Chang et al. [33] | IPI in the wild for LLM systems | Threat realism; informs task and attack design |
| StruQ [34] | Structured queries separating data and instruction | Baseline; StruQ hardens the model, this design enforces outside it |
| Information-flow control for LLM agents (taint tracking proposals) | Label propagation | Implemented end-to-end with tools, provenance on arguments, and adaptive evaluation on local models |
| Tool-permission frameworks | Coarse allow/deny | Provenance-conditioned, per-argument capability policy |

## 6. Study design

### Phase A — System and threat model (Days 1–30)
1. Assets, privileges, actions: define explicitly (for example read mailbox, send email, write file, HTTP fetch) with which principals may authorize each.
2. Provenance tagging: every retrieved span and every derived tool argument carries source, trust level, and derivation chain.
3. Control-flow separation: operator instructions, user request, retrieved data, tool policy are distinct channels; the model never sees a merged untyped prompt.
4. Capability policy: deterministic checks outside the model on (action, argument provenance, user authorization); denial and audit logging.

### Phase B — Attacks (Days 20–55)
1. Adaptive attacker with observation of the defense: varies placement, encoding, retrieval rank (poisoning to reach top-k), multi-turn setup, exfiltration strategy (arguments, URLs, filenames).
2. Attack generation partly automated (templates plus optimization against observed outcomes); ≥ 1000 attack–task combinations.

### Phase C — Evaluation (Days 45–80)
1. Three quantized local models (for example 3B–8B classes) across document QA, email/support workflow, one tool-using task.
2. Baselines: input filtering, defensive prompting, StruQ, strict no-tool.
3. Metrics separated: unauthorized action, data exposure, benign utility, refusal, latency, policy errors.
4. Held-out model family evaluation.

### Phase D — Ablation and honesty checks (Days 70–90)
1. Component ablations.
2. Policy-restrictiveness control: show that the policy permits the benign tasks (utility on benign tool use must be high) so success is not from over-restriction.

## 7. Baselines, metrics, and minimum evidence

| Item | Requirement |
|---|---|
| Attack–task combinations | ≥ 1000 |
| Attacker | Adaptive, observes defense |
| Models | 3 local quantized, plus held-out family |
| Tasks | Document QA, email/support, tool-using |
| Baselines | Filtering, prompting, StruQ, strict no-tool |
| Metrics | Unauthorized action, data exposure, benign utility, refusal, latency, policy errors (each separate) |
| Ablations | Every component |

## 8. Artifact and tooling plan

- Python system: local inference via `llama.cpp` bindings or `vLLM`/`transformers` with quantized weights; retrieval with a local vector store; tools as sandboxed Python functions.
- Provenance as a typed data structure attached to spans and arguments; capability policy as a pure-Python rule engine with unit tests.
- Attack harness with recorded attacker observations; every episode logged.
- One-command reproduction on a small attack set with one model.

## 9. Desk-rejection risks and mitigations

| Risk | Mitigation |
|---|---|
| Defense succeeds only because the policy is too restrictive | Benign tool-use utility reported; policy-restrictiveness control; compare with strict no-tool |
| Results do not transfer across model families | Held-out family; report per-model |
| Attack benchmark appears synthetic | Ground tasks in realistic workflows and consequences (actual send, write, fetch in sandbox); adaptive attacker |
| "Just a prompt filter" | The security claim depends on the external policy; ablations show it |

## 10. Stop conditions and decision gates

- **Gate 1 (Day 30).** Cannot express the three workflows' benign needs as capability policies without denying them → redesign policy model before proceeding.
- **Gate 2 (Day 80).** External policy cannot preserve benign utility against adaptive attacks → stop (portfolio stop condition).

## 11. 90-day validation plan

| Window | Work |
|---|---|
| Days 1–14 | Review 25–40 papers on IPI, agent security, IFC for LLMs; reproduce StruQ baseline locally; verify model and hardware |
| Days 15–30 | Freeze threat model, assets/actions, provenance schema, policy language, tasks, metrics, stop conditions; small deterministic system |
| Days 31–60 | Pilot with 1 model, 200 attack–task combinations; variance; hardest baseline (StruQ); one held-out-model test |
| Days 61–90 | Full preregistered evaluation; ablations; package; draft |

## 12. Journal strategy

- **TDSC** for an enforceable systems-security design (lead with the architecture and adaptive evaluation).
- **TOPS** when provenance, data exposure, and the threat model receive equal depth.

## 13. Ethics and disclosure

Attacks run only against the researcher's sandbox. Do not publish attack strings that target named deployed products without disclosure. Local models under their licenses.

## 14. Folder layout

```
12-capability-safe-rag/
├── RESEARCH_STRATEGY.md
├── literature/
├── experiments/     system/ (provenance, policy, tools), tasks/, attacks/, baselines/, runs/, ablations/, analysis/
└── paper/
```
