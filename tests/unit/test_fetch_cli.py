from pathlib import Path

from typer.testing import CliRunner

from ctr.cli import app

runner = CliRunner()


def test_bench_fetch_lists_every_source_and_asks_once(tmp_path: Path, monkeypatch: object) -> None:
    from ctr import datasets as dsmod
    from ctr import download as dl
    from tests.unit.test_datasets import TwoFile

    two = TwoFile(tmp_path, monkeypatch)  # type: ignore[arg-type]
    monkeypatch.setitem(dsmod.DATASETS, "twofile", two.ds)  # type: ignore[attr-defined]
    assert dl is not None
    declined = runner.invoke(app, ["fetch", "twofile"], input="n\n")
    assert declined.exit_code == 0
    for s in two.ds.sources:
        assert s.url in declined.output
    assert "test licence" in declined.output and "skipped" in declined.output
    assert two.opens == 0
    done = runner.invoke(app, ["fetch", "twofile", "--yes"])
    assert done.exit_code == 0, done.output
    assert done.output.count("sha256") == 2 and "built" in done.output


def test_bench_fetch_builds_without_asking_when_only_the_derived_file_is_missing(
    tmp_path: Path, monkeypatch: object
) -> None:
    from ctr import datasets as dsmod
    from ctr.download import local_path
    from tests.unit.test_datasets import TwoFile

    two = TwoFile(tmp_path, monkeypatch)  # type: ignore[arg-type]
    monkeypatch.setitem(dsmod.DATASETS, "twofile", two.ds)  # type: ignore[attr-defined]
    assert runner.invoke(app, ["fetch", "twofile", "--yes"]).exit_code == 0
    local_path(two.ds).unlink()
    opens, builds = two.opens, two.builds
    # No input is given: a confirm() call would abort with exit code 1.
    again = runner.invoke(app, ["fetch", "twofile"])
    assert again.exit_code == 0, again.output
    assert "built" in again.output and "download it?" not in again.output
    assert two.opens == opens
    assert two.builds == builds + 1 and local_path(two.ds).exists()


def test_bench_fetch_totals_only_the_missing_sources(tmp_path: Path, monkeypatch: object) -> None:
    from ctr import datasets as dsmod
    from ctr.download import fetch_source
    from tests.unit.test_datasets import PAYLOADS, TwoFile

    two = TwoFile(tmp_path, monkeypatch)  # type: ignore[arg-type]
    monkeypatch.setitem(dsmod.DATASETS, "twofile", two.ds)  # type: ignore[attr-defined]
    first, second = two.ds.sources
    fetch_source(first)
    out = runner.invoke(app, ["fetch", "twofile"], input="n\n").output
    assert second.url in out and first.url not in out
    assert f"({len(PAYLOADS[second.filename]):,} bytes)" in out


def test_bench_fetch_flags_a_file_without_a_checksum(tmp_path: Path, monkeypatch: object) -> None:
    from dataclasses import replace

    from ctr import datasets as dsmod
    from tests.unit.test_datasets import TwoFile

    two = TwoFile(tmp_path, monkeypatch)  # type: ignore[arg-type]
    loose = tuple(replace(s, sha256=None) for s in two.ds.sources)
    ds = replace(two.ds, sources=loose[:1], build=None)
    monkeypatch.setitem(dsmod.DATASETS, "twofile", ds)  # type: ignore[attr-defined]
    out = runner.invoke(app, ["fetch", "twofile", "--yes"]).output
    assert "unverified until its SHA-256 is recorded" in out
