"""Campaign driver: engines × mutation intensities × (restart | crash) histories, with provenance.

    python campaign.py --engines reference faulty-ghost qdrant-local chroma lancedb --intensities 0.3 0.6 0.9 \
                       --n-initial 1000 --n-ops 800 --crash --seeds 1 2 3 --out runs

Writes ``summary.jsonl`` (one row per engine × history), ``findings.jsonl`` (every non-approximation
finding), and ``minimized/`` histories for the first violation of each class per engine.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))

from provenance import Run  # noqa: E402
from vdbo.adapters import REGISTRY, available_real_engines  # noqa: E402
from vdbo.adapters.crash import CrashableEngine  # noqa: E402
from vdbo.generator import GenParams, generate  # noqa: E402
from vdbo.oracle import FailureClass  # noqa: E402
from vdbo.reducer import ddmin, describe  # noqa: E402
from vdbo.runner import run_history  # noqa: E402


def factory_for(engine: str, dim: int, crash: bool):
    if crash:
        return lambda path: CrashableEngine(engine, path=path, dim=dim)
    reg = {**REGISTRY, **available_real_engines()}
    return lambda path: reg[engine](path=path, dim=dim)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engines", nargs="+", default=["reference", *sorted(available_real_engines())])
    ap.add_argument("--intensities", nargs="+", type=float, default=[0.3, 0.6, 0.9])
    ap.add_argument("--seeds", nargs="+", type=int, default=[1])
    ap.add_argument("--n-initial", type=int, default=1000)
    ap.add_argument("--n-ops", type=int, default=800)
    ap.add_argument("--dim", type=int, default=16)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--crash", action="store_true", help="SIGKILL the engine process every --crash-every ops instead of clean restarts")
    ap.add_argument("--crash-every", type=int, default=120)
    ap.add_argument("--crash-rebuild", action="store_true", help="also SIGKILL the engine while a rebuild/compaction is in flight")
    ap.add_argument("--crash-rebuild-every", type=int, default=170)
    ap.add_argument("--restart-every", type=int, default=200)
    ap.add_argument("--reduce", action="store_true", help="ddmin the first failing history per engine and class")
    ap.add_argument("--out", default=Path(__file__).with_name("runs"))
    args = ap.parse_args(argv)
    if args.engines == ["all"]:
        args.engines = ["reference", *sorted(available_real_engines())]
    if args.crash_rebuild:
        args.crash = True

    config = {k: (str(v) if isinstance(v, Path) else v) for k, v in vars(args).items()}
    with Run(out_dir=args.out, config=config, seed=args.seeds[0], extra={"topic": 8, "tool": "campaign"}) as run:
        summary_f = (run.dir / "summary.jsonl").open("w")
        findings_f = (run.dir / "findings.jsonl").open("w")
        approx_f = (run.dir / "approximation.jsonl").open("w")
        reduced_dir = run.dir / "minimized"
        versions: dict[str, str] = {}
        table: list[dict] = []
        for engine in args.engines:
            reduced_classes: set[FailureClass] = set()
            for mi in args.intensities:
                for seed in args.seeds:
                    p = GenParams(n_initial=args.n_initial, n_ops=args.n_ops, dim=args.dim, k=args.k, mutation_intensity=mi,
                                  restart_every=0 if args.crash else args.restart_every, crash_every=args.crash_every if args.crash else 0,
                                  crash_rebuild_every=args.crash_rebuild_every if args.crash_rebuild else 0)
                    hist = generate(seed, p)
                    res = run_history(factory_for(engine, args.dim, args.crash), hist, probe_sample=40)
                    row = {**res.summary(), "mutation_intensity": mi, "seed": seed, "crash": args.crash, "gen": asdict(p)}
                    versions[row["engine"]] = res.engine_version
                    summary_f.write(json.dumps(row) + "\n")
                    table.append(row)
                    for f in res.findings:
                        row_f = {"engine": engine, "seed": seed, "mutation_intensity": mi, **f.as_row()}
                        (approx_f if f.failure == FailureClass.APPROXIMATION else findings_f).write(json.dumps(row_f) + "\n")
                    for v in res.verdicts:
                        if v.recall < 1.0:
                            approx_f.write(json.dumps({"engine": engine, "seed": seed, "mutation_intensity": mi, "op_index": v.op_index, "class": "recall", "recall": v.recall, "k": v.k, "n_exact": v.n_exact, "filter": v.findings[0].filter if v.findings else "∅"}) + "\n")
                    print(f"{engine:22s} mi={mi:.1f} seed={seed} recall={res.mean_recall():.4f} viol_q={res.queries_with_violation()} "
                          f"{dict((k, v) for k, v in res.class_counts().items() if k != 'approximation')} {res.seconds:.1f}s"
                          + (f" ERROR {res.error}" if res.error else ""), flush=True)
                    if args.reduce:
                        for cls in res.violation_classes() - reduced_classes:
                            if args.crash:
                                continue  # ddmin over crash histories is slow; reduce restart histories only
                            minimal, trials = ddmin(factory_for(engine, args.dim, False), hist, cls, max_trials=250)
                            reduced_dir.mkdir(exist_ok=True)
                            (reduced_dir / f"{engine}-{cls.value}-seed{seed}.json").write_text(json.dumps(minimal.to_jsonable()))
                            (reduced_dir / f"{engine}-{cls.value}-seed{seed}.txt").write_text(describe(minimal))
                            print(f"    reduced {cls.value}: {len(hist.ops)} -> {len(minimal.ops)} ops in {trials} trials", flush=True)
                            reduced_classes.add(cls)
        summary_f.close(); findings_f.close(); approx_f.close()
        run.record(engine_versions=versions)
        # compact per-engine table
        agg: dict[str, Counter] = {}
        for r in table:
            c = agg.setdefault(r["engine"], Counter())
            for k in ("queries", "queries_with_violation", "stale_version", "ghost_result", "visibility_lag", "filter_inconsistency", "durability_loss"):
                c[k] += r[k]
            c["recall_sum"] += r["mean_recall"] * r["queries"]
        lines = ["| engine | version | queries | mean recall | queries w/ violation | stale | ghost | lag | filter | durability |", "|---|---|---|---|---|---|---|---|---|---|"]
        for e, c in agg.items():
            rec = c["recall_sum"] / c["queries"] if c["queries"] else float("nan")
            lines.append(f"| {e} | {versions.get(e, '')} | {c['queries']} | {rec:.4f} | {c['queries_with_violation']} | {c['stale_version']} | {c['ghost_result']} | {c['visibility_lag']} | {c['filter_inconsistency']} | {c['durability_loss']} |")
        (run.dir / "table.md").write_text("\n".join(lines) + "\n")
        print("\n".join(lines))
        print(f"\nwrote {run.dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
