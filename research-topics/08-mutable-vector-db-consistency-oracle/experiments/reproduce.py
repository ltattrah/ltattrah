"""One-command reproduction entry point for Topic 08.

    python reproduce.py --small     # oracle self-validation + a short campaign on every locally available engine
    python reproduce.py             # full pilot: three mutation intensities, three seeds, clean restarts and SIGKILL crashes

Runs write to ``runs/<timestamp>-<confighash>/`` with provenance (see ``../../common/provenance.py``).
Requires the packages in ``requirements.txt`` (a virtualenv is recommended; see ``README.md``).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import campaign  # noqa: E402
from vdbo.adapters import available_real_engines  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--small", action="store_true")
    ap.add_argument("--skip-tests", action="store_true")
    args = ap.parse_args()

    if not args.skip_tests:
        print("== oracle self-validation (reference + single-fault engines) ==", flush=True)
        rc = subprocess.call([sys.executable, "-m", "pytest", str(HERE / "tests"), "-q"])
        if rc != 0:
            print("self-validation failed; not running engines", file=sys.stderr)
            return rc

    real = sorted(available_real_engines())
    engines = ["reference", "faulty-ghost", "faulty-stale", "faulty-lag", "faulty-filter", "faulty-durability", *real]
    print(f"== engines: {engines} ==", flush=True)
    if args.small:
        common = ["--engines", *engines, "--n-initial", "300", "--n-ops", "300", "--dim", "8", "--k", "5", "--seeds", "1"]
        rc = campaign.main([*common, "--intensities", "0.6", "--reduce"])
        rc |= campaign.main([*common, "--intensities", "0.6", "--crash", "--crash-every", "100"])
        return rc
    common = ["--engines", *engines, "--n-initial", "5000", "--n-ops", "3000", "--dim", "32", "--k", "10", "--seeds", "1", "2", "3", "--intensities", "0.3", "0.6", "0.9"]
    rc = campaign.main([*common, "--reduce"])
    rc |= campaign.main([*common, "--crash", "--crash-every", "250"])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
