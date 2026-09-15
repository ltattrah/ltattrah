"""One-command reproduction entry point for Topic 12.

    python reproduce.py --small     # smoke run on the small deterministic artifact
    python reproduce.py             # full reproduction of the headline result

Every run records provenance through ``common/provenance.Run``. Replace the body of
``main`` with the pipeline for this topic; keep the ``--small`` path under a few minutes.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
from provenance import Run  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", default=Path(__file__).with_name("config.yaml"))
    ap.add_argument("--small", action="store_true", help="run the small deterministic artifact only")
    ap.add_argument("--out", default=Path(__file__).with_name("runs"))
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())
    cfg["small"] = bool(args.small)

    with Run(out_dir=args.out, config=cfg, seed=cfg.get("seed")) as run:
        # TODO(topic 12): implement the pipeline. Phases from RESEARCH_STRATEGY.md section 6:
        #   - Phase A — System and threat model (Days 1–30)
        #   - Phase B — Attacks (Days 20–55)
        #   - Phase C — Evaluation (Days 45–80)
        #   - Phase D — Ablation and honesty checks (Days 70–90)
        raise NotImplementedError("pipeline not implemented yet; see RESEARCH_STRATEGY.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
