"""Break recall shortfalls down by filter type and query position.

    python analysis/recall_breakdown.py runs/<stamp>-<hash>

Reads ``approximation.jsonl`` written by ``campaign.py`` and prints, per engine, mean recall for
unfiltered vs category vs range vs combined filters. Approximation that concentrates on selective
filters points at post-filtering inside the engine; approximation spread evenly points at the index.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def filter_kind(desc: str) -> str:
    if desc == "∅":
        return "none"
    has_cat, has_num = "cat=" in desc, "num∈" in desc
    return "cat+range" if has_cat and has_num else ("cat" if has_cat else "range")


def main(run_dir: str) -> None:
    rows = [json.loads(l) for l in (Path(run_dir) / "approximation.jsonl").read_text().splitlines() if l.strip()]
    summ = [json.loads(l) for l in (Path(run_dir) / "summary.jsonl").read_text().splitlines() if l.strip()]
    total_q = defaultdict(int)
    for s in summ:
        total_q[s["engine"]] += s["queries"]
    per = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r.get("class") == "recall":
            per[r["engine"]][filter_kind(r["filter"])].append(r["recall"])
    print(f"{'engine':24s} {'queries':>8s} {'q<1.0':>6s}  " + "  ".join(f"{k:>12s}" for k in ("none", "cat", "range", "cat+range")))
    for eng in sorted(per):
        kinds = per[eng]
        n_low = sum(len(v) for v in kinds.values())
        cells = []
        for k in ("none", "cat", "range", "cat+range"):
            v = kinds.get(k, [])
            cells.append(f"{len(v):4d}@{(sum(v)/len(v)):.3f}" if v else f"{'-':>12s}")
        print(f"{eng:24s} {total_q[eng]:8d} {n_low:6d}  " + "  ".join(f"{c:>12s}" for c in cells))
    print("\ncells: <number of queries with recall<1> @ <their mean recall>")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sorted(Path(__file__).resolve().parents[1].glob("runs/*"))[-1])
