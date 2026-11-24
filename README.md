# clonal-trajectory-research

Real-data benchmarks, calibration studies and case studies behind the trust claims of
[lumencell](https://github.com/shreyandhawa/lumenCell_V2), an interactive explorer for
single-cell pseudotime and lineage trajectories.

lumencell is the tool. This repo is the evidence: how well trajectory methods and the clonal
(TCR clonotype) checks hold up on real datasets, the gates declared before each analysis, and the
written case studies. History for the moved files was kept from the original repo.

## What it found

Two findings so far. Both are about these checks on this data, not about trajectory methods in
general.

1. **The verdict rule cannot tell a tree from a non-tree.** As it was checked, lumencell's verdict
   rule looks at one thing: whether at least 95% of cells get a pseudotime. On lumencell 0.5.0 it
   rated 27 of 30 negative-control runs (blobs, loops, sheets, two separate groups) as "supported".
   A tree measure the rule does not use separates all four control kinds from the tree datasets.
   So lumencell never shows "supported" on real data; it caps it at "not shown to be a tree".
2. **Clone agreement is weaker than the default comparison suggests.** In one public CAR-T dataset
   (Sheih et al. 2020: four patients, three methods, 12 runs), agreement between T-cell-receptor
   clones and the inferred lineages falls to under half when clones are shuffled within a time
   point instead of within a patient (ratio 0.03 to 0.49 as point estimates; the two widest
   intervals reach 0.625 and 0.770). A k-means clustering that uses no trajectory comes within
   0.05 of the score in every run.

What explains the drop in the second finding is open: a synthetic test of clones confined to time
points did not reproduce it. It is one dataset and four patients.

Details and limits: [docs/results.md](docs/results.md),
[the claim and its sources](docs/paper/claim.md), and the two diagnosis pages
([verdict](docs/paper/diagnosis-verdict.md), [clonal](docs/paper/diagnosis-clonal.md)).

## Layout

| Path | What |
|---|---|
| `src/ctr/` | Dataset registry, downloads and builders, real-data runner, calibration, report |
| `benchmarks/thresholds.toml` | What the research declared before each analysis: real-data gates, case studies, calibration and verification. Merged over the thresholds lumencell ships |
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

Needs lumencell 0.5 from PyPI. The synthetic gates and the baseline come from the installed
lumencell (`lumencell/bench/policy`).
