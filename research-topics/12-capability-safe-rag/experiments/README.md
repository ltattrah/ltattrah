# Experiments — Topic 12

Layout (see `RESEARCH_STRATEGY.md` section 14 for the topic-specific subfolders to add):

- `config.yaml` — parameters and the minimum evidence package; frozen at the protocol freeze (Day 30).
- `reproduce.py` — one-command reproduction; `--small` must finish in minutes on a laptop.
- `runs/` — raw outputs, one directory per run with `run.json` provenance (never edited after writing). Large raw data stays out of git; commit manifests and hashes.
- `analysis/` — scripts that turn `runs/` into the tables and figures in `../paper/`.

Phases:
1. Phase A — System and threat model (Days 1–30)
2. Phase B — Attacks (Days 20–55)
3. Phase C — Evaluation (Days 45–80)
4. Phase D — Ablation and honesty checks (Days 70–90)

Conventions: seeds fixed and logged; engine, tool, kernel, and CPU recorded per run; derived tables regenerated from raw outputs; nothing in `runs/` is hand-edited.
