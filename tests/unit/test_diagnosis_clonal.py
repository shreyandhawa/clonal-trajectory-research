"""Toy-data tests of the clonal confound checks; no declared check is run here."""

import math

import numpy as np
from lumencell.clonal.labels import CloneCodes

from ctr import diagnosis_clonal as dc
from ctr.gates import REPO


def test_timepoints_are_equal_sized_and_follow_time_when_sigma_is_small():
    t = np.random.default_rng(0).random(2000)
    tp = dc.assign_timepoints(t, 0.0, np.random.default_rng(1))
    assert sorted(set(tp)) == ["t0", "t1", "t2", "t3"]
    assert {int((tp == g).sum()) for g in set(tp)} == {500}
    assert t[tp == "t0"].max() < t[tp == "t1"].min()
    noisy = dc.assign_timepoints(t, 0.4, np.random.default_rng(1))
    assert t[noisy == "t0"].max() > t[noisy == "t1"].min()


def _layer(n=4000):
    rng = np.random.default_rng(2)
    seg = rng.choice(["trunk", "a", "b"], size=n)
    tp = np.array([f"t{i}" for i in rng.integers(0, 4, n)])
    return seg, tp


def test_confined_clones_never_span_time_points_and_others_do():
    seg, tp = _layer()
    confined = dc.plant_clones(seg, ["a", "b"], tp, 0.0, True, np.random.default_rng(3))
    free = dc.plant_clones(seg, ["a", "b"], tp, 0.0, False, np.random.default_rng(3))
    spans = lambda clone: max(  # noqa: E731
        len(set(tp[[i for i in np.flatnonzero(clone == c)]])) for c in set(clone) - {None}
    )
    assert spans(confined) == 1
    assert spans(free) > 1


def test_fate_bias_makes_leaf_clones_single_segment_and_arms_share_the_labelled_cells():
    seg, tp = _layer()
    t3 = dc.plant_clones(seg, ["a", "b"], tp, 0.7, True, np.random.default_rng(4))
    t1 = dc.plant_clones(seg, ["a", "b"], tp, 0.0, True, np.random.default_rng(4))
    assert ((t3 == None) == (t1 == None)).all()  # noqa: E711
    assert abs(float(np.mean(t3 != None)) - dc.LABEL_RATE) < 0.03  # noqa: E711
    pure = [len(set(seg[t3 == c])) == 1 for c in set(t3) - {None} if set(seg[t3 == c]) <= {"a", "b"}]
    assert any(pure)


def test_ratio_is_undefined_below_the_eta_floor():
    assert math.isnan(dc.ratio(0.04, 0.0))
    assert dc.ratio(0.4, 0.1) == 0.25


def test_boot_median_ci_ignores_nan_and_handles_none():
    assert math.isnan(dc.boot_median_ci([math.nan])[0])
    m, lo, hi = dc.boot_median_ci([1.0, 2.0, 3.0, math.nan])
    assert m == 2.0 and lo <= m <= hi


def _rows(arm_eta, arm_p, seeds=40):
    """Toy per-seed rows: every seed has the same numbers, so the medians are those numbers."""
    return [
        {
            "mode": "oracle", "sigma": s, "arm": arm, "seed": i,
            "eta": dict(zip(dc.NULLS, arm_eta[arm], strict=True)),
            "p": dict(zip(dc.NULLS, arm_p[arm], strict=True)),
        }
        for s in dc.SIGMAS for arm in dc.ARMS for i in range(seeds)
    ]  # fmt: skip


NULL_P = (0.5, 0.5, 0.5)
SIGNAL_P = (0.001, 0.001, 0.001)
CONFOUND_P = (0.001, 0.5, 0.5)


def test_decide_names_each_outcome():
    p = {"T0": NULL_P, "T1": CONFOUND_P, "T2": SIGNAL_P, "T3": SIGNAL_P}
    base = {"T0": (0, 0, 0), "T1": (0.3, 0.0, 0.0), "T2": (0.5, 0.45, 0.4), "T3": (0.5, 0.45, 0.4)}
    out = lambda eta, pp: dc.decide(dc.summarise(_rows(eta, pp), 40))["per_sigma"]["0.1"]["outcome"]  # noqa: E731
    assert "confound signature" in out(base, p)
    assert "also what a real signal does" in out({**base, "T3": (0.5, 0.45, 0.1)}, p)
    assert "does not inflate" in out({**base, "T1": (0.01, 0.0, 0.0)}, {**p, "T1": NULL_P})
    assert "over-corrects" in out({**base, "T2": (0.5, 0.4, 0.1)}, p)
    assert "harness invalid" in out(base, {**p, "T0": SIGNAL_P})


def test_clone_bootstrap_on_pure_clones_gives_a_high_eta_and_a_positive_lift():
    rng = np.random.default_rng(5)
    n_clones, size = 40, 3
    lineage = np.repeat(np.arange(n_clones) % 2, size)
    membership = np.stack([lineage == 0, lineage == 1])
    n = lineage.size
    codes = CloneCodes(
        clone=np.repeat(np.arange(n_clones), size).astype(np.int64),
        donor=np.zeros(n, dtype=np.int64),
        stratum=rng.integers(0, 2, n).astype(np.int64),
        n_missing_donor=0,
    )
    out = dc.clone_bootstrap(
        membership, codes, rng.random(n), rng.integers(0, 2, n).astype(np.int64), n_boot=6, n_permutations=30
    )
    assert out["n_clones"] == n_clones
    assert out["ci"]["N1"][0] > 0.5
    assert out["share_delta_eta_positive"] == 1.0


def test_the_declaration_names_what_the_code_hard_codes():
    text = (REPO / "docs" / "paper" / "declaration-clonal-confound.md").read_text()
    for needle in (
        "600-639",
        str(dc.TP_STREAM),
        str(dc.CLONE_STREAM),
        "500 replicates",
        "100 permutations",
        "0.05",
    ):
        assert needle in text
    assert dc.N_BOOT == 500 and dc.BOOT_PERMUTATIONS == 100 and range(600, 640) == dc.SEEDS
