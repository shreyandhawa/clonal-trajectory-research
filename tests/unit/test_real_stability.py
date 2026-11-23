from pathlib import Path
from types import SimpleNamespace
from typing import Any

import click
import pytest
from lumencell.bench.runner import CaseResult, StabilityRow
from typer.testing import CliRunner

from ctr import report
from ctr.cli import app


def test_bench_real_has_a_stability_switch() -> None:
    # Rich colours help under CI (GITHUB_ACTIONS), which splits option names with escape codes.
    out = click.unstyle(CliRunner().invoke(app, ["real", "--help"]).output)
    assert "--no-stability" in out


def test_the_report_shows_the_verdict(monkeypatch: pytest.MonkeyPatch) -> None:
    _, real = report.latest_real() or (None, {"methods": {}})
    d, base = next(iter(real["methods"]["paga_dpt"].items()))
    row = {**base, "tree_support": "weak"}
    data = {"commit": "abc", "methods": {"paga_dpt": {d: row}}}
    monkeypatch.setattr(
        report, "latest_real", lambda: (report.REPO / "benchmarks" / "results" / "real-x.json", data)
    )
    assert "verdict Clones do not back these lineages" in report.render()


def _fake_real(monkeypatch: pytest.MonkeyPatch, now: list[float]) -> list[Any]:
    import numpy as np
    from lumencell.bench.metrics import Scores

    from ctr import real_case as runner

    ds = SimpleNamespace(root_spec="x", label_key="cell_type", clonal=None, report_time_key=None)
    monkeypatch.setattr(runner, "DATASETS", {"d": ds})
    monkeypatch.setattr(runner, "is_cached", lambda d: True)
    monkeypatch.setattr(runner, "local_path", lambda d: "p")
    monkeypatch.setattr(runner, "truth_for", lambda d, obs: None)
    monkeypatch.setattr(runner, "parse_root", lambda s: "root")
    monkeypatch.setattr(runner, "load", lambda p: SimpleNamespace(obs=None))
    monkeypatch.setattr(runner, "PrepCache", lambda data: SimpleNamespace(run=lambda pp: SimpleNamespace()))
    ctx = SimpleNamespace(leiden=np.array([0, 1, 2]))
    monkeypatch.setattr(runner.InferenceContext, "from_prep", lambda *a, **k: ctx)
    res = SimpleNamespace(pseudotime=None, membership=None, warnings=[])
    monkeypatch.setattr(runner, "run_method", lambda *a, **k: res)
    fields = {f: 0.0 for f in Scores.__dataclass_fields__}
    fields.update(n_spurious=0)
    monkeypatch.setattr(runner, "score", lambda *a, **k: Scores(**fields))

    def tick() -> float:
        now[0] += 2.0
        return now[0] - 2.0

    monkeypatch.setattr(runner.time, "perf_counter", tick)
    calls: list[Any] = []
    return calls


def test_run_real_case_stability_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    from ctr import real_case as runner

    now = [10.0]
    calls = _fake_real(monkeypatch, now)
    monkeypatch.setattr(
        runner, "stability_row", lambda *a, **k: calls.append(a) or StabilityRow("ok", 0.5, 0.5, 0.5, "weak")
    )
    off = runner.run_real_case("d", stability=False)
    assert calls == [] and off.stability.status == "not_measured"

    now[0] = 10.0
    sentinel = StabilityRow("ok", 0.1, 0.2, 0.3, "weak")  # type: ignore[arg-type]

    def slow_stability(*a: Any, **k: Any) -> StabilityRow:
        calls.append(a)
        now[0] += 100.0  # stability takes a long time
        return sentinel

    monkeypatch.setattr(runner, "stability_row", slow_stability)
    on = runner.run_real_case("d", stability=True)
    assert len(calls) == 1 and calls[0][4] == "cell_type"
    assert on.stability is sentinel
    assert on.runtime_seconds == 2.0  # stops before stability's 100 s


def test_bench_real_forwards_stability_and_prints_verdict(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from lumencell.bench.metrics import Scores

    from ctr import datasets
    from ctr import real_case as runner

    fields = {f: 0.0 for f in Scores.__dataclass_fields__}
    fields.update(n_spurious=0)
    flags: list[bool] = []

    def fake_case(d: str, method: str, params: Any = None, stability: bool = False) -> CaseResult:
        flags.append(stability)
        st = StabilityRow("ok", 0.5, 0.5, 0.5, "weak")  # type: ignore[arg-type]
        return CaseResult(d, method, Scores(**fields), 3, 1.0, stability=st)

    monkeypatch.setattr(runner, "run_real_case", fake_case)
    monkeypatch.setattr(datasets, "is_cached", lambda ds: True)
    out = str(tmp_path / "o.json")
    args = ["real", "--methods", "paga_dpt", "--datasets", "pancreas", "--out", out]
    default = CliRunner().invoke(app, args)
    CliRunner().invoke(app, [*args, "--no-stability"])
    assert flags == [True, False]
    assert "verdict=weak" in default.output


def _real_data(level: str) -> dict[str, Any]:
    _, real = report.latest_real() or (None, {"methods": {}})
    d, base = next(iter(real["methods"]["paga_dpt"].items()))
    row = {k: v for k, v in base.items() if k != "tree_support"}
    if level:
        row["tree_support"] = level
    return {"commit": "abc", "methods": {"paga_dpt": {d: row}}}


def _render(monkeypatch: pytest.MonkeyPatch, data: dict[str, Any]) -> str:
    monkeypatch.setattr(
        report, "latest_real", lambda: (report.REPO / "benchmarks" / "results" / "real-x.json", data)
    )
    return report.render()


def test_report_hides_not_measured_verdict(monkeypatch: pytest.MonkeyPatch) -> None:
    assert ", verdict" not in _render(monkeypatch, _real_data("not_measured"))


def test_report_adds_footnote_only_with_verdicts(monkeypatch: pytest.MonkeyPatch) -> None:
    assert "The verdict is" not in _render(monkeypatch, _real_data("not_measured"))
    assert "The verdict is" not in _render(monkeypatch, _real_data(""))
    assert "The verdict is" in _render(monkeypatch, _real_data("weak"))


def test_the_report_footnote_says_only_supported_is_capped(monkeypatch: pytest.MonkeyPatch) -> None:
    """Owner ruling H-1: the footnote is the one user-facing statement of the cap."""
    text = _render(monkeypatch, _real_data("provisional"))
    assert "A supported verdict is capped at provisional" in text
    assert "A weak or not_supported verdict is a real failure and is not capped" in text
    assert "supported or weak" not in text
