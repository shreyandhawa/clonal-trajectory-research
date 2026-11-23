# clonal-trajectory-research

Real-data benchmarks, calibration studies and case studies behind the trust claims of
[lumencell](https://github.com/shreyandhawa/lumenCell_V2), an interactive explorer for
single-cell pseudotime and lineage trajectories.

lumencell is the tool. This repo is the evidence: how well trajectory methods and the clonal
(TCR clonotype) checks hold up on real datasets, the gates declared before each analysis, and the
written case studies. History for the moved files was kept from the original repo.

## Layout

| Path | What |
|---|---|
| `src/ctr/` | Dataset registry, downloads and builders, real-data runner, calibration, report |
| `benchmarks/thresholds.toml` | Gates declared before each analysis (a frozen copy of lumencell 0.4.0's, extended here) |
| `benchmarks/results/` | Result JSON per run |
| `docs/results.md`, `docs/benchmarks.md`, `docs/case-studies/` | Write-ups and generated tables |
| `docs/HANDOFF.md` | Project record from before the split |

## Use

```bash
uv sync
uv run ctr fetch all     # asks before each download
uv run ctr real          # run methods on the downloaded datasets, check the gates
uv run ctr report        # tables from the latest results
uv run pytest -m "not real_data"
```

Needs lumencell with the research modules removed (0.5.0). Until that is on PyPI,
`pyproject.toml` installs lumencell from the `main` branch of its GitHub repo, so `uv sync` works
on any machine with network access. To build against a local checkout of the tool instead, run
`uv pip install -e ../lumenCell_V2` after `uv sync`.
