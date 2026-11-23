from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from lumencell.bench.runner import ClonalRow
from lumencell.bench.synth import generate, truth_from_adata
from lumencell.bench.synth_clones import DEFAULT_LAYER, ClonalLayer, add_clones, clone_truth
from lumencell.bench.truth import Truth

from ctr.real_case import run_real_case
from ctr.report import render


def _clone_truth(layer: ClonalLayer = DEFAULT_LAYER, topology: str = "bifurcation") -> Truth:
    adata = generate(topology, "realistic", n_cells=1500, n_genes=200, seed=0)
    return clone_truth(truth_from_adata(adata), add_clones(adata, layer, seed=0))


def test_the_report_says_the_clonal_gate_is_not_a_branch_gate() -> None:
    assert "not a branch gate" in render()


def test_a_real_case_row_is_not_applicable(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    truth = _clone_truth()
    spec = SimpleNamespace(root_spec="r", label_key=None, clonal=None, report_time_key=None)
    monkeypatch.setattr("ctr.real_case.DATASETS", {"d": spec})
    monkeypatch.setattr("ctr.real_case.is_cached", lambda ds: True)
    monkeypatch.setattr("ctr.real_case.local_path", lambda ds: tmp_path)
    monkeypatch.setattr("ctr.real_case.truth_for", lambda ds, obs: truth)
    monkeypatch.setattr("ctr.real_case.parse_root", lambda s: s)
    monkeypatch.setattr("ctr.real_case.load", lambda p: SimpleNamespace(obs=None))
    monkeypatch.setattr(
        "ctr.real_case.PrepCache",
        lambda data: SimpleNamespace(run=lambda pp: SimpleNamespace(artifacts={})),
    )
    monkeypatch.setattr(
        "lumencell.engine.context.InferenceContext.from_prep",
        lambda *a, **k: SimpleNamespace(leiden=np.array([0, 1])),
    )
    monkeypatch.setattr(
        "ctr.real_case.run_method",
        lambda *a, **k: SimpleNamespace(
            pseudotime=truth.order.astype(np.float32), membership=truth.membership(), warnings=[]
        ),
    )
    res = run_real_case("d")
    assert repr(res.clonal) == repr(ClonalRow("not_applicable"))


def test_the_report_counts_failures_per_gate() -> None:
    text = render()
    line = next(x for x in text.splitlines() if x.startswith("Cases failing each gate"))
    assert "`clonal_excess_ratio`" in line
    assert "PAGA + DPT" in line


def test_the_clonal_column_never_rounds_up_across_the_gate() -> None:
    from ctr.report import _range

    rows = [{"clonal_excess_ratio": 0.4996}, {"clonal_excess_ratio": 0.5004}]
    assert _range(rows, "clonal_excess_ratio", floor=True) == "0.499–0.500"
    assert _range([{"clonal_excess_ratio": 0.4996}], "clonal_excess_ratio", floor=True) == "0.499–0.499"
