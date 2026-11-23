"""Toy-data tests of the verdict diagnosis checks; none of them runs a declared check on the real records."""

import math

import numpy as np
from scipy import sparse
from scipy.spatial import cKDTree

from ctr import diagnosis_verdict as dv
from ctr.gates import REPO
from ctr.verdict_calibration import RunRecord

NO_TAUS = {"tau_tree": None, "tau_lin": None, "tau_pt": None}


def rec(cov=1.0, tree=0.5, lin=1.0, pt=1.0, group="control", name="blob/seed3", method="paga_dpt"):
    return RunRecord(group, name, 3, method, cov, ((1.0, tree),), lin, pt, 2)


def knn(points, k=8):
    dist, idx = cKDTree(points).query(points, k=k + 1)
    rows = np.repeat(np.arange(len(points)), k)
    return sparse.csr_matrix((dist[:, 1:].ravel(), (rows, idx[:, 1:].ravel())), shape=(len(points),) * 2)


def test_hand_verdict_is_coverage_alone_without_taus():
    assert dv.hand_verdict(rec(cov=0.95), NO_TAUS, 0.95) == "supported"
    assert dv.hand_verdict(rec(cov=0.949), NO_TAUS, 0.95) == "not_supported"
    assert dv.hand_verdict(rec(cov=math.nan), NO_TAUS, 0.95) == "not_supported"
    assert dv.hand_verdict(rec(tree=0.0, lin=0.0, pt=0.0), NO_TAUS, 0.95) == "supported"


def test_hand_verdict_uses_a_tau_when_there_is_one():
    taus = {"tau_tree": 0.8, "tau_lin": 0.5, "tau_pt": None}
    assert dv.hand_verdict(rec(tree=0.7), taus, 0.95) == "not_supported"
    assert dv.hand_verdict(rec(tree=0.9, lin=0.4), taus, 0.95) == "weak"
    assert dv.hand_verdict(rec(tree=0.9, lin=0.5, pt=0.0), taus, 0.95) == "supported"


def test_criterion_table_counts_passes_and_margins():
    calib = [rec(group="matrix", name=f"t/seed{i}", tree=0.9, lin=1.0, pt=0.99) for i in range(5)]
    controls = [rec(cov=1.0, tree=t, lin=1.0, pt=0.5, name=f"c/seed{i}") for i, t in enumerate((0.95, 0.5))]
    t = dv.criterion_table(controls, calib, 0.95, 0.10)
    assert t["bars"]["C2"]["matrix_q"] == 0.9
    assert t["criteria"]["C1@fixed"]["passes"] == 2
    assert t["criteria"]["C2@matrix_q"]["passes"] == 1
    assert math.isclose(t["criteria"]["C2@matrix_q"]["margin_median"], 0.05)
    assert t["criteria"]["C4@matrix_q"]["passes"] == 0
    assert t["combos"]["C1+C2@matrix_q"] == 1
    assert t["combos"]["C1+C2+C3+C4@matrix_q"] == 0


def test_twonn_reads_a_line_as_one_and_a_plane_as_two():
    rng = np.random.default_rng(0)
    line = np.c_[rng.random(3000), np.zeros((3000, 4))]
    plane = np.c_[rng.random((3000, 2)), np.zeros((3000, 3))]
    assert 0.8 < dv.twonn_dimension(line) < 1.2
    assert 1.7 < dv.twonn_dimension(plane) < 2.3


def test_four_point_defect_is_small_on_a_tree_and_large_on_a_loop():
    rng = np.random.default_rng(1)
    t = rng.random(400) * 3
    tree = np.vstack(  # a "Y": a trunk and two branches
        [np.c_[t, np.zeros(400)], np.c_[3 + t * 0.7, t * 0.7], np.c_[3 + t * 0.7, -t * 0.7]]
    ) + rng.normal(0, 0.01, (1200, 2))
    angle = rng.random(1200) * 2 * np.pi
    loop = np.c_[3 * np.cos(angle), 3 * np.sin(angle)] + rng.normal(0, 0.01, (1200, 2))
    kwargs = {"n_landmarks": 150, "n_quads": 20_000}
    assert dv.four_point_defect(knn(tree), **kwargs) < dv.four_point_defect(knn(loop), **kwargs)


def test_components_counts_parts():
    graph = sparse.block_diag([sparse.csr_matrix(np.ones((3, 3))), np.ones((2, 2))])
    assert dv.n_components(sparse.csr_matrix(graph)) == 2


def test_separated_needs_no_overlap_with_the_tree_range():
    assert dv.separated([5.0, 6.0], [1.0, 2.0])
    assert not dv.separated([1.5, 6.0], [1.0, 2.0])


def test_latent_correlation_handles_missing_pieces():
    t = np.array([0.0, 0.1, 0.2, np.nan, 0.4])
    assert dv.latent_correlation(t, np.arange(5.0)) == 1.0
    assert math.isnan(dv.latent_correlation(t, None))
    assert math.isnan(dv.latent_correlation(np.full(5, np.nan), np.arange(5.0)))


def test_record_differences_flags_a_changed_field_and_a_new_error():
    doc = {
        "records": [
            {
                "group": "control",
                "dataset": "x/seed3",
                "seed": 3,
                "method": "palantir",
                "coverage": 1.0,
                "tree_likeness": [[1.0, 0.5]],
                "lineage_stability": 1.0,
                "pseudotime_stability": 0.9,
                "n_lineages": 3,
                "error": None,
            }
        ]
    }
    same = RunRecord("control", "x/seed3", 3, "palantir", 1.0, ((1.0, 0.5),), 1.0, 0.9, 3)
    assert dv.record_differences(doc, [same]) == []
    failed = RunRecord(
        "control", "x/seed3", 3, "palantir", math.nan, ((1.0, 0.5),), math.nan, math.nan, 0, "E: x"
    )
    assert any("error" in d for d in dv.record_differences(doc, [failed]))


def test_the_declaration_names_what_the_code_hard_codes():
    text = (REPO / "docs" / "paper" / "declaration-verdict-diagnosis.md").read_text()
    for run in dv.HAND_RUNS:
        assert run in text
    assert f"{dv.N_LANDMARKS} landmarks" in text and "200,000" in text and "default_rng(0)" in text
