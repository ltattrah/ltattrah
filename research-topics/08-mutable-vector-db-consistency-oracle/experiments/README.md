# Experiments — Topic 08

Black-box consistency and freshness oracle for mutable vector databases. See `model/semantic-model.md` for the contracts and failure classes, `LOG.md` for the dated lab log.

## Setup

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt        # numpy, pyyaml, pytest, pyarrow, qdrant-client, chromadb, lancedb
python -m pytest tests -q              # classifier self-validation (reference + single-fault engines)
python reproduce.py --small            # tests + short restart and crash campaigns on every available engine
```

## Layout

- `vdbo/` — the oracle package: `model.py`, `generator.py`, `snapshot.py`, `oracle.py`, `runner.py`, `reducer.py`, `adapters/`.
- `campaign.py` — engines × intensities × seeds × (restart | crash); writes `summary.jsonl`, `findings.jsonl`, `table.md`, `minimized/` into `runs/<stamp>-<hash>/` with `run.json` provenance.
- `reproduce.py` — one-command entry point (`--small` for the smoke version).
- `tests/` — pytest suite validating classifier precision against known faults.
- `model/semantic-model.md` — contracts C1–C7, failure classes, decision procedure, probe protocol.
- `runs/` — raw outputs (git-ignored); commit only `table.md` snapshots you cite, under `analysis/`.
- `config.yaml` — minimum evidence package; frozen at the protocol freeze.

## Adding an engine

Subclass `vdbo.adapters.base.EngineAdapter`, implement `open/close/upsert/delete/query/get/count`, set `advertised`, and register it in `vdbo/adapters/__init__.py::available_real_engines`. Keep adapters thin; the model must not depend on product names.
