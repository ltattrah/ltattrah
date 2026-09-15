# Experiments — Topic 15

Layout (see `RESEARCH_STRATEGY.md` section 14 for the topic-specific subfolders to add):

- `config.yaml` — parameters and the minimum evidence package; frozen at the protocol freeze (Day 30).
- `reproduce.py` — one-command reproduction; `--small` must finish in minutes on a laptop.
- `runs/` — raw outputs, one directory per run with `run.json` provenance (never edited after writing). Large raw data stays out of git; commit manifests and hashes.
- `analysis/` — scripts that turn `runs/` into the tables and figures in `../paper/`.

Phases:
1. Phase A — Preferences and measures (Days 1–30)
2. Phase B — Longitudinal exposure (Days 25–70)
3. Phase C — Recovery and persistence (Days 55–90)

Conventions: seeds fixed and logged; engine, tool, kernel, and CPU recorded per run; derived tables regenerated from raw outputs; nothing in `runs/` is hand-edited.
