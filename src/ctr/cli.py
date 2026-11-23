"""Command line for the research: fetch datasets, run the real-data benchmarks, render the tables."""

from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(
    name="ctr",
    help="Clonal trajectory research: real-data benchmarks and case studies for lumencell.",
    no_args_is_help=True,
    add_completion=False,
)


@app.callback()
def main() -> None:
    """Clonal trajectory research."""


@app.command("fetch")
def fetch_cmd(
    dataset: Annotated[str, typer.Argument(help="Dataset id, or 'all'.")],
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Download without asking.")] = False,
) -> None:
    """Download a real benchmark dataset (asks first; shows source and size)."""
    from ctr.datasets import (
        CASE_STUDIES,
        DATASETS,
        CaseStudyDataset,
        FetchError,
        RealDataset,
        fetch,
        is_cached,
        local_path,
        sha256_of,
    )
    from ctr.download import build_dataset, is_downloaded, source_path

    known: dict[str, RealDataset | CaseStudyDataset] = {
        **DATASETS,
        **CASE_STUDIES,
    }  # `all` covers DATASETS only; a case study is fetched by its id
    ids = list(DATASETS) if dataset == "all" else [dataset]
    unknown = [i for i in ids if i not in known]
    if unknown:
        raise typer.BadParameter(f"unknown dataset {unknown[0]!r}; choose from {', '.join(known)} or all")
    for i in ids:
        ds = known[i]
        if is_cached(ds):
            typer.echo(f"{ds.id}: already at {local_path(ds)}")
            continue
        missing = [s for s in ds.sources if not is_downloaded(s)]
        try:
            if not missing:
                # Nothing to download: only the derived file is missing, so build without asking.
                typer.echo(f"{ds.id}: building {local_path(ds)}")
                build_dataset(ds)
                typer.echo("  built")
                continue
            typer.echo(f"{ds.id}: {ds.title} ({ds.citation})")
            typer.echo(f"  licence: {ds.licence}")
            for s in missing:
                typer.echo(f"  from {s.url}\n    {s.size / 1e6:,.1f} MB -> {source_path(s)}")
            total = sum(s.size for s in missing)
            typer.echo(f"  total {total / 1e6:,.1f} MB ({total:,} bytes)")
            if not yes and not typer.confirm("  download it?", default=False):
                typer.echo("  skipped")
                continue
            from ctr.download import fetch_source

            for s in missing:
                digest = sha256_of(fetch_source(s))
                note = "" if s.sha256 else " (unverified until its SHA-256 is recorded in the registry)"
                typer.echo(f"  {s.filename}: sha256 {digest}{note}")
            if ds.build is not None:
                typer.echo(f"  building {local_path(ds)}")
            fetch(ds)
            if ds.build is not None:
                typer.echo("  built")
        except FetchError as exc:
            raise typer.BadParameter(str(exc)) from exc


@app.command("real")
def real_cmd(
    methods: Annotated[
        str, typer.Option(help="Comma-separated method names.")
    ] = "paga_dpt,palantir,scfates_ppt",
    datasets: Annotated[str, typer.Option(help="Comma-separated dataset ids; default all downloaded.")] = "",
    out: Annotated[
        Path | None, typer.Option(help="Results JSON (default benchmarks/results/real-<date>.json).")
    ] = None,
    stability: Annotated[
        bool, typer.Option("--stability/--no-stability", help="Also run stability and the tree verdict.")
    ] = True,
) -> None:
    """Run methods on the downloaded real datasets and check the release gates."""
    import json
    import subprocess
    from datetime import UTC, datetime

    from lumencell.engine.registry import METHODS

    from ctr.datasets import DATASETS, is_cached, lineage_gates_note
    from ctr.gates import REPO, check_gates, load_thresholds
    from ctr.real_case import run_real_case

    cfg = load_thresholds()["real"]
    ids = [d for d in (datasets.split(",") if datasets else DATASETS) if d]
    missing = [d for d in ids if d not in DATASETS or not is_cached(DATASETS[d])]
    if missing:
        raise typer.BadParameter(f"not downloaded: {', '.join(missing)} (ctr fetch ...)")
    rows: dict[str, dict[str, object]] = {}
    failures = []
    for d in ids:
        for method in methods.split(","):
            if not METHODS[method].available().ok:
                typer.echo(f"{d:24s} {method:12s} skipped (not installed)")
                continue
            row = run_real_case(d, method, stability=stability).row()
            rows.setdefault(method, {})[d] = row
            failed = check_gates(row, cfg[d]["gates"])
            failures += [(method, f) for f in failed]
            # A dataset with no gated lineage measured nothing: never PASS (a failure still shows).
            verdict = "FAIL" if failed else (lineage_gates_note(DATASETS[d]) or "PASS")
            typer.echo(
                f"{d:24s} {method:12s} sp={row['pt_spearman_global']:.3f} "
                f"sp_lin={row['pt_spearman_lineage']:.3f} branch={row['branch_accuracy']:.3f} "
                f"recall={row['lineage_recall']:.2f} terminal={row['terminal_share']:.3f} "
                f"verdict={row['tree_support']} clonal={row['clonal_status']} {verdict} "
                f"({row['runtime_seconds']}s)"
            )
    for method, f in failures:
        typer.echo(f"gate     {method}: {f}")
    sha = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    date = datetime.now(UTC).date().isoformat()
    target = out or REPO / "benchmarks" / "results" / f"real-{date}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"generated": date, "commit": sha, "methods": rows}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    typer.echo(f"wrote {target}")


@app.command("report")
def report_cmd(
    readme: Annotated[bool, typer.Option(help="Rewrite the results section of docs/benchmarks.md.")] = False,
) -> None:
    """Markdown tables of the synthetic baseline (frozen copy) and the latest real-data results."""
    from ctr.report import render, update_readme

    text = render()
    if readme:
        update_readme(text)
        typer.echo("docs/benchmarks.md updated")
    else:
        typer.echo(text)
