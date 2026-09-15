"""Classifier validation against engines with known, single-contract faults."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vdbo.adapters import REGISTRY  # noqa: E402
from vdbo.generator import GenParams, generate  # noqa: E402
from vdbo.model import History  # noqa: E402
from vdbo.oracle import FailureClass  # noqa: E402
from vdbo.reducer import ddmin  # noqa: E402
from vdbo.runner import run_history  # noqa: E402

SMALL = GenParams(n_initial=200, n_ops=300, dim=8, k=5, restart_every=100, rebuild_every=120, flush_every=60)
EXPECTED = {
    "faulty-ghost": FailureClass.GHOST_RESULT,
    "faulty-stale": FailureClass.STALE_VERSION,
    "faulty-lag": FailureClass.VISIBILITY_LAG,
    "faulty-filter": FailureClass.FILTER_INCONSISTENCY,
    "faulty-durability": FailureClass.DURABILITY_LOSS,
}


def factory(name):
    return lambda path: REGISTRY[name](path=path, dim=SMALL.dim)


def test_generator_is_deterministic():
    a, b = generate(7, SMALL), generate(7, SMALL)
    assert [o.describe() for o in a.ops] == [o.describe() for o in b.ops]
    assert History.from_jsonable(a.to_jsonable()).to_jsonable() == a.to_jsonable()


def test_reference_engine_is_clean():
    res = run_history(factory("reference"), generate(1, SMALL))
    assert res.error is None
    assert res.violation_classes() == set()
    assert res.mean_recall() == 1.0
    assert res.class_counts().get("approximation", 0) == 0


@pytest.mark.parametrize("engine,expected", sorted(EXPECTED.items()))
def test_single_fault_engines_are_classified_precisely(engine, expected):
    res = run_history(factory(engine), generate(3, SMALL))
    assert res.error is None, res.error
    classes = res.violation_classes()
    assert expected in classes, f"{engine}: expected {expected}, got {res.class_counts()}"
    # precision: the injected fault must be the only violation class (approximation may co-occur for lag engines)
    assert classes == {expected}, f"{engine}: spurious classes {classes - {expected}}: {res.class_counts()}"


def test_approximate_engine_only_costs_recall():
    res = run_history(factory("faulty-approx"), generate(5, SMALL))
    assert res.violation_classes() == set()
    assert res.mean_recall() < 1.0
    assert res.class_counts()["approximation"] > 0


def test_reducer_finds_small_ghost_history():
    hist = generate(11, SMALL)
    minimal, trials = ddmin(factory("faulty-ghost"), hist, FailureClass.GHOST_RESULT, max_trials=300)
    assert len(minimal.ops) < len(hist.ops) // 4
    res = run_history(factory("faulty-ghost"), minimal)
    assert FailureClass.GHOST_RESULT in res.violation_classes()
