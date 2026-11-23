"""Diagnosis of the 28-of-31 verdict verification (declared in docs/paper/declaration-verdict-diagnosis.md).

Nothing here changes a rule, threshold, seed or control. Checks:

- (a) ``hand_verdict`` re-derives a level from the saved numbers and the rule text, not from the tool's code.
- (c) ``criterion_table``: the pass rate of each criterion alone on the controls, and its margin.
- (b) ``twonn_dimension``, ``n_components``, ``four_point_defect``: structure measures that use none of C1-C4.
- (d) ``latent_correlation`` and ``structure_runs``: whether a method's pseudotime follows the control's
  latent coordinate.

Run as ``python -I -m ctr.diagnosis_verdict rederive|criteria|structure|reproduce --out PATH``.
"""

import argparse
import json
import math
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.sparse.csgraph import connected_components, dijkstra
from scipy.spatial import cKDTree
from scipy.stats import spearmanr

from ctr.gates import REPO, load_thresholds
from ctr.verdict_calibration import RunRecord, records_from_payload, write_json

RESULTS = REPO / "benchmarks" / "results"
VERIFICATION = RESULTS / "verdict-verification-2026-11-17.json"
CALIBRATION = RESULTS / "verdict-calibration-2026-11-17.json"
# Declared in the doc: the three hand-derived runs, plus the odd supported and an unsupported control.
HAND_RUNS = (
    "blob/seed4 paga_dpt",
    "loop/seed4 paga_dpt",
    "sheet/seed4 paga_dpt",
    "two_groups/seed5 palantir",
    "two_groups/seed4 paga_dpt",
)
N_LANDMARKS = 300
N_QUADS = 200_000
SEED = 0
F64 = npt.NDArray[np.float64]


# ---- (a) re-derive a verdict from the saved numbers and the rule text -----------------------------
def hand_verdict(r: RunRecord, taus: Mapping[str, float | None], coverage_min: float) -> str:
    """The level of a run with no clones, from the text of ``[tree_support]`` in thresholds.toml.

    C1 passes iff coverage >= coverage_min. A check whose tau is None is left out. C5 does not apply.
    not_supported if C1 or C2 fails; weak if C3 or C4 fails; supported otherwise (``verified=True``).
    """
    tree = dict(r.tree_likeness)[1.0]
    if not r.coverage >= coverage_min:  # NaN fails
        return "not_supported"
    if taus["tau_tree"] is not None and not tree >= taus["tau_tree"]:
        return "not_supported"
    for tau, value in ((taus["tau_lin"], r.lineage_stability), (taus["tau_pt"], r.pseudotime_stability)):
        if tau is not None and not value >= tau:
            return "weak"
    return "supported"


def rederive(doc: Mapping[str, Any], cfg: Mapping[str, Any]) -> dict[str, Any]:
    """Every recorded verdict of a verification file against ``hand_verdict`` and the tool's own verdict."""
    from lumencell.engine.tree_support import (  # the tool, imported late so the toy tests do not need it
        ClonalEvidence,
        StabilityEvidence,
        Thresholds,
        verdict,
    )

    calibrated = cfg["tree_support"]["calibrated"]
    taus = {k: calibrated.get(k) for k in ("tau_tree", "tau_lin", "tau_pt")}
    cov_min = float(cfg["tree_support"]["coverage_min"])
    th = Thresholds(**taus, coverage_min=cov_min)
    recorded = {(d, m): lvl for d, m, lvl in doc["verdicts"]}
    rows, mismatches = [], []
    for r in records_from_payload(doc):
        if r.error is not None:
            continue
        hand = hand_verdict(r, taus, cov_min)
        tool = verdict(
            r.coverage,
            dict(r.tree_likeness)[1.0],
            StabilityEvidence("done", r.lineage_stability, r.pseudotime_stability),
            ClonalEvidence("not_configured", r.n_lineages),
            th,
            verified=True,
        ).level
        rec = recorded[(r.dataset, r.method)]
        rows.append(
            {
                "run": f"{r.dataset} {r.method}",
                "group": r.group,
                "coverage": r.coverage,
                "recorded": rec,
                "hand": hand,
                "tool": tool,
            }
        )
        if not rec == hand == tool:
            mismatches.append(rows[-1])
    return {
        "n": len(rows),
        "n_control": sum(x["group"] == "control" for x in rows),
        "mismatches": mismatches,
        "rows": rows,
        "hand_runs": [x for x in rows if x["run"] in HAND_RUNS],
    }


# ---- (c) pass rate of each criterion alone ---------------------------------------------------------
def _q(values: Sequence[float], q: float) -> float:
    return float(np.quantile(np.asarray(values, dtype=float), q, method="linear"))


def criterion_table(
    verif: Sequence[RunRecord], calib: Sequence[RunRecord], coverage_min: float, matrix_quantile: float
) -> dict[str, Any]:
    """Pass counts and margins of C1-C4 alone on the verification controls.

    C2-C4 bars come from the calibration matrix: its ``matrix_quantile`` and its minimum (C2: one value
    per dataset, NaN as 0, factor 1.0). The bars are not fitted to the controls.
    """

    def c2(r: RunRecord) -> float:
        v = dict(r.tree_likeness)[1.0]
        return 0.0 if math.isnan(v) else v

    getters = {"C2": c2, "C3": lambda r: r.lineage_stability, "C4": lambda r: r.pseudotime_stability}
    ok_cal = [r for r in calib if r.error is None and r.group == "matrix"]
    per_dataset = {r.dataset: r for r in ok_cal}.values()  # C2 repeats across methods
    bars: dict[str, dict[str, float]] = {"C1": {"fixed": coverage_min}}
    for name, get in getters.items():
        vals = [get(r) for r in (per_dataset if name == "C2" else ok_cal)]
        bars[name] = {"matrix_q": _q(vals, matrix_quantile), "matrix_min": float(min(vals))}
    controls = [r for r in verif if r.error is None and r.group == "control"]
    values = {
        "C1": [r.coverage for r in controls],
        **{n: [g(r) for r in controls] for n, g in getters.items()},
    }
    out: dict[str, Any] = {"n_controls": len(controls), "bars": bars, "criteria": {}, "combos": {}}
    for name, vals in values.items():
        for bar_name, bar in bars[name].items():
            passed = [v - bar for v in vals if v >= bar]
            out["criteria"][f"{name}@{bar_name}"] = {
                "bar": bar,
                "passes": len(passed),
                "margin_median": float(np.median(passed)) if passed else None,
                "margin_min": min(passed) if passed else None,
                "margin_max": max(passed) if passed else None,
            }
    for bar_name in ("matrix_q", "matrix_min"):
        for combo in (("C1", "C2"), ("C1", "C3"), ("C1", "C4"), ("C1", "C2", "C3", "C4")):
            n = sum(
                all(values[c][i] >= bars[c].get(bar_name, bars[c].get("fixed", math.nan)) for c in combo)
                for i in range(len(controls))
            )
            out["combos"][f"{'+'.join(combo)}@{bar_name}"] = n
    return out


# ---- (b) structure measures that do not use C1-C4 --------------------------------------------------
def twonn_dimension(x: F64) -> float:
    """TwoNN (Facco et al. 2017): d = (n - 1) / sum log(r2 / r1) over cells with r1 > 0."""
    dist, _ = cKDTree(x).query(x, k=3)
    r1, r2 = dist[:, 1], dist[:, 2]
    keep = r1 > 0
    mu = np.log(r2[keep] / r1[keep])
    return float((keep.sum() - 1) / mu.sum())


def n_components(graph: sparse.spmatrix) -> int:
    edges = sparse.csr_matrix(graph, copy=True)
    edges.eliminate_zeros()
    return int(connected_components(edges, directed=False)[0])


def four_point_defect(
    distances: sparse.spmatrix, n_landmarks: int = N_LANDMARKS, n_quads: int = N_QUADS, seed: int = SEED
) -> float:
    """99th percentile of (largest - middle) / diameter of the three pair sums, over random landmark
    quadruples inside the largest connected part. A tree metric gives 0."""
    rng = np.random.default_rng(seed)
    _, labels = connected_components(distances, directed=False)
    biggest = np.flatnonzero(labels == np.bincount(labels).argmax())
    land = rng.choice(biggest, size=min(n_landmarks, biggest.size), replace=False)
    d = dijkstra(distances, directed=False, indices=land)[:, land]
    diameter = d.max()
    q = rng.integers(0, land.size, size=(n_quads, 4))
    q = q[(np.diff(np.sort(q, axis=1), axis=1) > 0).all(axis=1)]  # four distinct landmarks
    a, b, c, e = q.T
    sums = np.sort(np.stack([d[a, b] + d[c, e], d[a, c] + d[b, e], d[a, e] + d[b, c]]), axis=0)
    return float(np.quantile((sums[2] - sums[1]) / diameter, 0.99))


# ---- (d) does the pseudotime follow the latent coordinate? -----------------------------------------
def latent_coordinate(obs: Any, kind: str) -> npt.NDArray[np.float64] | None:
    """The generator's own coordinate: angular distance from the root (loop), distance from the root
    corner (sheet), the group (two_groups), true pseudotime (a tree); None for a blob."""
    if kind == "loop":
        theta = obs["control_angle"].to_numpy(dtype=np.float64)
        return np.minimum(theta, 2 * np.pi - theta)
    if kind == "sheet":
        return np.hypot(
            obs["control_x"].to_numpy(dtype=np.float64), obs["control_y"].to_numpy(dtype=np.float64)
        )
    if kind == "two_groups":
        return obs["control_group"].to_numpy(dtype=np.float64)
    if kind == "blob":
        return None
    return obs["true_pseudotime"].to_numpy(dtype=np.float64)


def latent_correlation(pseudotime: F64, latent: F64 | None) -> float:
    """|Spearman| over cells with a finite pseudotime; NaN with no latent coordinate or <3 cells."""
    if latent is None:
        return math.nan
    finite = np.isfinite(pseudotime)
    if finite.sum() < 3 or np.ptp(latent[finite]) == 0 or np.ptp(pseudotime[finite]) == 0:
        return math.nan
    return abs(float(spearmanr(pseudotime[finite], latent[finite]).statistic))


def structure_runs(
    cfg: dict[str, Any], seeds: Sequence[int], methods: Sequence[str], workdir: Path
) -> dict[str, Any]:
    """Slow: for each (group, kind, seed), the dataset's structure measures and each method's |rho|."""
    from lumencell.data.loader import load
    from lumencell.engine.context import InferenceContext
    from lumencell.engine.registry import run_method
    from lumencell.prep.pipeline import run_pipeline
    from lumencell.prep.stages import PrepParams

    from ctr.verdict_calibration import _datasets, _generate  # private, same package

    datasets, runs = [], []
    for group, name, seed in _datasets(cfg, {"matrix": seeds, "control": seeds}):
        adata, root = _generate(cfg, group, name, seed)
        path = workdir / f"{group}-{name}-{seed}.h5ad"
        adata.write_h5ad(path)
        ds = load(path)
        params = PrepParams()
        prep = run_pipeline(ds, params)
        pcs = np.asarray(prep.artifacts["pca"], dtype=np.float64)[:, : params.neighbors_pcs]
        latent = latent_coordinate(adata.obs, name if group == "control" else "tree")
        datasets.append(
            {
                "group": group,
                "kind": name,
                "seed": seed,
                "twonn": twonn_dimension(pcs),
                "components": n_components(prep.artifacts["connectivities"]),
                "defect99": four_point_defect(prep.artifacts["distances"]),
            }
        )
        ctx = InferenceContext.from_prep(ds, prep, params)
        for method in methods:
            try:
                res = run_method(ctx, method, root)
                runs.append(
                    {
                        "group": group,
                        "kind": name,
                        "seed": seed,
                        "method": method,
                        "n_lineages": len(res.lineages),
                        "abs_rho": latent_correlation(np.asarray(res.pseudotime, dtype=np.float64), latent),
                    }
                )
            except Exception as exc:  # recorded: a method that refuses is a result
                runs.append(
                    {
                        "group": group,
                        "kind": name,
                        "seed": seed,
                        "method": method,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
        path.unlink(missing_ok=True)
        print(f"structure: {group}/{name}/seed{seed} done", file=sys.stderr, flush=True)
    return {"datasets": datasets, "runs": runs}


def separated(control: Sequence[float], tree: Sequence[float]) -> bool:
    """Declared rule: the control values and the tree range [min, max] do not overlap."""
    lo, hi = min(tree), max(tree)
    return all(v < lo or v > hi for v in control)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("part", choices=["rederive", "criteria", "structure", "reproduce"])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workdir", type=Path, default=Path("/tmp/ctr-diagnosis"))
    args = ap.parse_args(argv)
    cfg = load_thresholds()
    args.workdir.mkdir(parents=True, exist_ok=True)
    ver, cal = json.loads(VERIFICATION.read_text()), json.loads(CALIBRATION.read_text())
    if args.part == "rederive":
        payload = rederive(ver, cfg)
    elif args.part == "criteria":
        payload = criterion_table(
            records_from_payload(ver),
            records_from_payload(cal),
            float(cfg["tree_support"]["coverage_min"]),
            float(cfg["tree_support"]["calibration"]["matrix_quantile"]),
        )
    elif args.part == "structure":
        payload = structure_runs(cfg, range(6), cfg["tree_support"]["calibration"]["methods"], args.workdir)
    else:  # reproduce: R1/R2 (which lumencell is imported is decided by PYTHONPATH)
        import lumencell
        from lumencell.engine.tree_support import calibrated_thresholds

        from ctr.verdict_calibration import collect_records, verify

        v = cfg["tree_support"]["verification"]
        recs = collect_records(
            cfg,
            {"matrix": v["matrix_seeds"], "control": v["control_seeds"]},
            cfg["tree_support"]["calibration"]["methods"],
            args.workdir,
        )
        out = verify(recs, calibrated_thresholds(), int(v["max_controls_supported"]))
        payload = {
            "lumencell_file": lumencell.__file__,
            "controls_supported": list(out.controls_supported),
            "n_controls_supported": len(out.controls_supported),
            "n_failed": out.n_failed,
            "records": [r.__dict__ for r in recs],
            "differences": record_differences(ver, recs),
        }
    write_json(args.out, payload)
    print(f"wrote {args.out}")
    return 0


def record_differences(doc: Mapping[str, Any], fresh: Sequence[RunRecord], tol: float = 1e-9) -> list[str]:
    """Fields of the fresh records that differ from the recorded file (numbers within ``tol``)."""
    old = {(r.dataset, r.method): r for r in records_from_payload(doc)}
    diffs: list[str] = []
    for r in fresh:
        o = old.get((r.dataset, r.method))
        if o is None:
            diffs.append(f"{r.dataset} {r.method}: not in the recorded file")
            continue
        for field in ("coverage", "lineage_stability", "pseudotime_stability"):
            a, b = getattr(o, field), getattr(r, field)
            if not (a == b or (math.isnan(a) and math.isnan(b)) or abs(a - b) <= tol):
                diffs.append(f"{r.dataset} {r.method}: {field} {a} -> {b}")
        if o.tree_likeness != r.tree_likeness and not all(
            f1 == f2 and (v1 == v2 or (math.isnan(v1) and math.isnan(v2)) or abs(v1 - v2) <= tol)
            for (f1, v1), (f2, v2) in zip(o.tree_likeness, r.tree_likeness, strict=False)
        ):
            diffs.append(f"{r.dataset} {r.method}: tree_likeness changed")
        if (o.n_lineages, o.error) != (r.n_lineages, r.error):
            diffs.append(
                f"{r.dataset} {r.method}: n_lineages/error "
                f"{(o.n_lineages, o.error)} -> {(r.n_lineages, r.error)}"
            )
    return diffs


if __name__ == "__main__":
    sys.exit(main())
