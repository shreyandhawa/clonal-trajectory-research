"""Is the clonal agreement score confounded by time? (declared in docs/paper/declaration-clonal-confound.md)

Nothing here changes a definition, null, seed or threshold of the score; it calls ``score_clonal`` as the
runtime does. Two checks:

- ``run_synthetic``: planted clones with a time-point variable and no, some or all lineage signal, scored
  against N1, N2 and N3 (arms T0-T3), then ``summarise`` and ``decide``.
- ``run_sheih``: a clone bootstrap (``clone_bootstrap``) of every per-patient Sheih run.

Run as ``python -I -m ctr.diagnosis_clonal synthetic|sheih --out PATH``.
"""

import argparse
import math
import sys
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
from lumencell.bench.synth_clones import draw_clone_size
from lumencell.clonal.labels import CloneCodes
from lumencell.clonal.scores import ClonalResult, score_clonal
from scipy.stats import rankdata

from ctr.calibration import rejection_bound
from ctr.verdict_calibration import write_json

SEEDS = range(600, 640)  # fresh: clear of 0-5, 100-499, 500-519 and 900-904
TOPOLOGIES = ("bifurcation", "trifurcation", "binary2")
SIGMAS = (0.1, 0.4)
N_TIMEPOINTS = 4
LABEL_RATE = 0.85
TP_STREAM, CLONE_STREAM = 7100601, 7100602
ALPHA, QUANTILE = 0.05, 0.99
ETA_MIN = 0.05  # the repo's oracle_eta_min: R is only read where eta(N1) is at least this
N_BOOT, BOOT_PERMUTATIONS = 500, 100
# arm -> (fate_bias, clones confined to one time point)
ARMS: dict[str, tuple[float, bool]] = {
    "T0": (0.0, False),
    "T1": (0.0, True),
    "T2": (0.7, False),
    "T3": (0.7, True),
}
NULLS = ("N1", "N2", "N3")
F64 = npt.NDArray[np.float64]


def assign_timepoints(
    t: F64, sigma: float, rng: np.random.Generator, k: int = N_TIMEPOINTS
) -> npt.NDArray[np.str_]:
    """Time point of each cell: the quartile (k-ile) of ``rank(t) / n + Normal(0, sigma)``."""
    u = rankdata(t) / t.size + rng.normal(0.0, sigma, t.size)
    rank = rankdata(u, method="ordinal") - 1
    return np.array([f"t{int(i)}" for i in np.minimum(k - 1, (k * rank) // t.size)])


def plant_clones(
    seg: npt.NDArray[np.str_],
    leaves: Sequence[str],
    tp: npt.NDArray[np.str_],
    fate_bias: float,
    confined: bool,
    rng: np.random.Generator,
    label_rate: float = LABEL_RATE,
) -> npt.NDArray[np.object_]:
    """Clone ids (None where unlabelled), as ``synth_clones.add_clones`` plants them for one donor.

    With probability ``fate_bias`` a labelled cell on a leaf segment draws from that leaf's pool, else from
    the trunk pool. ``confined`` builds the pools inside each time point, so a clone never spans two.
    The label and leaf-join draws are the same for every arm of a seed.
    """
    n = seg.size
    labelled = rng.random(n) < label_rate
    join = rng.random(n) < fate_bias
    clone = np.full(n, None, dtype=object)
    count = 0
    for g in np.unique(tp) if confined else [None]:
        mine = labelled if g is None else labelled & (tp == g)
        on_leaf = mine & join & np.isin(seg, leaves)
        pools = [np.flatnonzero(mine & ~on_leaf)] + [
            np.flatnonzero(on_leaf & (seg == leaf)) for leaf in leaves
        ]
        for pool in pools:
            cells = rng.permutation(pool)
            pos = 0
            while pos < cells.size:
                size = draw_clone_size(rng)
                clone[cells[pos : pos + size]] = f"c{count}"
                pos += size
                count += 1
    return clone


def summary_of(r: ClonalResult) -> dict[str, Any]:
    """The numbers a row keeps: eta and p against each null, delta_eta, the status."""
    by = {n.null: n for n in r.nulls}
    return {
        "status": r.status,
        "n_cells": r.n_cells,
        "n_clones": r.n_clones,
        "eta": {k: (by[k].eta if k in by else math.nan) for k in NULLS},
        "p": {k: (by[k].p if k in by else math.nan) for k in NULLS},
        "delta_eta": r.delta_eta,
    }


def ratio(eta1: float, eta3: float) -> float:
    """R = eta(N3) / eta(N1); NaN unless eta(N1) >= ``ETA_MIN`` (two near-zeros give noise)."""
    return eta3 / eta1 if eta1 >= ETA_MIN and not math.isnan(eta3) else math.nan


def boot_median_ci(values: Sequence[float], n: int = 2000, seed: int = 0) -> tuple[float, float, float]:
    """Median and a 95% percentile bootstrap interval over the finite values; NaN with none."""
    v = np.array([x for x in values if not math.isnan(x)], dtype=float)
    if v.size == 0:
        return math.nan, math.nan, math.nan
    draws = np.random.default_rng(seed).choice(v, size=(n, v.size))
    lo, hi = np.percentile(np.median(draws, axis=1), [2.5, 97.5])
    return float(np.median(v)), float(lo), float(hi)


def summarise(rows: Sequence[Mapping[str, Any]], n_seeds: int) -> dict[str, Any]:
    """Per (mode, sigma, arm): medians with seed-bootstrap intervals, rejections against the bound, R."""
    bound = rejection_bound(n_seeds, ALPHA, QUANTILE)
    out: dict[str, Any] = {"bound": bound, "n_seeds": n_seeds, "cells": {}}
    keys = sorted({(r["mode"], r["sigma"], r["arm"]) for r in rows})
    for mode, sigma, arm in keys:
        sel = [r for r in rows if (r["mode"], r["sigma"], r["arm"]) == (mode, sigma, arm)]
        eta = {k: [r["eta"][k] for r in sel] for k in NULLS}
        rej = {k: sum(r["p"][k] <= ALPHA for r in sel if not math.isnan(r["p"][k])) for k in NULLS}
        rs = [ratio(r["eta"]["N1"], r["eta"]["N3"]) for r in sel]
        finite = [x for x in rs if not math.isnan(x)]
        out["cells"][f"{mode}/{sigma}/{arm}"] = {
            "n": len(sel),
            "eta_median_ci": {k: boot_median_ci(eta[k]) for k in NULLS},
            "rejections": rej,
            "ratio_median_ci": boot_median_ci(rs),
            "ratio_defined": len(finite),
            "share_ratio_below_half": float(np.mean([x < 0.5 for x in finite])) if finite else math.nan,
        }
    return out


def decide(summary: Mapping[str, Any], mode: str = "oracle") -> dict[str, Any]:
    """The declared decision rules D0-D3 and the outcome, for each sigma, in one mode."""
    bound, cells = summary["bound"], summary["cells"]

    def get(sigma: float, arm: str) -> Mapping[str, Any]:
        cell: Mapping[str, Any] = cells[f"{mode}/{sigma}/{arm}"]
        return cell

    per_sigma: dict[str, Any] = {}
    for sigma in sorted({float(k.split("/")[1]) for k in cells if k.startswith(mode + "/")}):
        t0, t1, t2, t3 = (get(sigma, a) for a in ("T0", "T1", "T2", "T3"))
        d0 = all(t0["rejections"][k] <= bound for k in NULLS)
        d1 = (
            t1["eta_median_ci"]["N1"][0] >= ETA_MIN
            and t1["rejections"]["N1"] > bound
            and t1["rejections"]["N3"] <= bound
            and abs(t1["eta_median_ci"]["N3"][0]) < 0.02
        )
        d2 = (
            t2["eta_median_ci"]["N3"][0] >= 0.5 * t2["eta_median_ci"]["N1"][0]
            and t2["rejections"]["N3"] > bound
        )
        d3 = t3["ratio_median_ci"][0] >= 0.5
        if not d0:
            outcome = "harness invalid (D0 failed): nothing else is read"
        elif not d1:
            outcome = "time does not inflate eta(N1) here: the Sheih pattern is not explained by it"
        elif not d2:
            outcome = "N3 over-corrects even when time and lineage separate: the halving is an artefact"
        elif d3:
            outcome = "the halving is a confound signature: eta(N1) is overstated by time, report eta(N3)"
        else:
            outcome = "N1 is confounded, but the halving is also what a real signal does (clones follow time)"
        per_sigma[str(sigma)] = {"D0": d0, "D1": d1, "D2": d2, "D3": d3, "outcome": outcome}
    agree = len({v["outcome"] for v in per_sigma.values()}) == 1
    return {"mode": mode, "per_sigma": per_sigma, "sigmas_agree": agree}


# ---- Sheih: the clone bootstrap --------------------------------------------------------------------
def percentile_ci(values: Sequence[float]) -> tuple[float, float]:
    v = np.array([x for x in values if not math.isnan(x)], dtype=float)
    return (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) if v.size else (math.nan, math.nan)


def clone_bootstrap(
    membership: npt.NDArray[np.bool_],
    codes: CloneCodes,
    pseudotime: F64,
    baseline: npt.NDArray[np.int64],
    n_boot: int = N_BOOT,
    n_permutations: int = BOOT_PERMUTATIONS,
    min_clone_size: int = 2,
) -> dict[str, Any]:
    """Resample the scored clones with replacement and re-score each replicate (lineages, pseudotime,
    strata and baseline fixed). A clone drawn twice is two clones. Returns intervals and shares."""
    from lumencell.clonal.scores import _scored_cells

    candidates = membership.sum(axis=0) == 1  # own-cells mode
    cells, dense, sizes = _scored_cells(codes.clone, candidates, min_clone_size)
    k = sizes.size
    by_clone = np.split(np.argsort(dense, kind="stable"), np.cumsum(sizes)[:-1])
    rng = np.random.default_rng(0)
    reps: dict[str, list[float]] = {"N1": [], "N2": [], "N3": [], "delta_eta": [], "R": []}
    for b in range(n_boot):
        drawn = rng.integers(0, k, size=k)
        idx = cells[np.concatenate([by_clone[i] for i in drawn])]
        new = CloneCodes(
            clone=np.repeat(np.arange(k, dtype=np.int64), sizes[drawn]),
            donor=codes.donor[idx],
            stratum=None if codes.stratum is None else codes.stratum[idx],
            n_missing_donor=0,
        )
        res = score_clonal(
            membership[:, idx], new, pseudotime[idx], baseline[idx],
            n_permutations=n_permutations, min_clone_size=min_clone_size, seed=b,
        )  # fmt: skip
        s = summary_of(res)
        for name in NULLS:
            reps[name].append(s["eta"][name])
        reps["delta_eta"].append(s["delta_eta"])
        reps["R"].append(ratio(s["eta"]["N1"], s["eta"]["N3"]))
    ci = {name: percentile_ci(v) for name, v in reps.items()}
    ok_delta = [x for x in reps["delta_eta"] if not math.isnan(x)]
    ok_r = [x for x in reps["R"] if not math.isnan(x)]
    return {
        "n_clones": int(k),
        "ci": ci,
        "share_delta_eta_positive": float(np.mean([x > 0 for x in ok_delta])) if ok_delta else math.nan,
        "share_ratio_below_half": float(np.mean([x < 0.5 for x in ok_r])) if ok_r else math.nan,
        "n_ratio_defined": len(ok_r),
    }


# ---- drivers (slow) --------------------------------------------------------------------------------
def run_synthetic(cfg: dict[str, Any], workdir: Path) -> dict[str, Any]:
    from lumencell.bench.synth import generate, truth_from_adata
    from lumencell.clonal.labels import encode_clones
    from lumencell.clonal.scores import score_with_baseline
    from lumencell.data.loader import load
    from lumencell.engine.context import InferenceContext
    from lumencell.engine.registry import run_method
    from lumencell.engine.roots import ClusterRoot
    from lumencell.prep.pipeline import run_pipeline
    from lumencell.prep.stages import PrepParams

    syn = cfg["synthetic"]
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        base = generate(
            TOPOLOGIES[(seed - SEEDS[0]) % 3],
            syn["preset"],
            n_cells=syn["n_cells"],
            n_genes=syn["n_genes"],
            seed=seed,
        )
        truth = truth_from_adata(base)
        segs = dict(base.uns["lumencell_truth"]["segments"])
        leaves = sorted(set(segs) - {str(v["parent"]) for v in segs.values()})
        seg = base.obs["true_segment"].astype(str).to_numpy()
        t = base.obs["true_pseudotime"].to_numpy(dtype=np.float64)
        path = workdir / f"syn-{seed}.h5ad"
        base.write_h5ad(path)
        ds = load(path)
        pp = PrepParams()
        prep = run_pipeline(ds, pp)
        ctx = InferenceContext.from_prep(ds, prep, pp)
        result = run_method(ctx, "paga_dpt", ClusterRoot("true_label", truth.meta["root_label"]))
        pca = np.asarray(prep.artifacts["pca"])
        path.unlink(missing_ok=True)
        for sigma in SIGMAS:
            tp = assign_timepoints(t, sigma, np.random.default_rng([seed, TP_STREAM]))
            for arm, (fate_bias, confined) in ARMS.items():
                clone = plant_clones(
                    seg, leaves, tp, fate_bias, confined, np.random.default_rng([seed, CLONE_STREAM])
                )
                codes = encode_clones(clone, None, [tp.astype(object)])
                oracle = score_clonal(
                    truth.membership(), codes, truth.order, np.zeros(truth.n_obs, dtype=np.int64),
                    oracle_cells=truth.exclusive() >= 0,
                )  # fmt: skip
                own = score_with_baseline(
                    result.membership,
                    codes,
                    result.pseudotime,
                    pca,
                    pp.neighbors_pcs,
                    int(result.membership.shape[0]),
                )
                rows += [
                    {"mode": m, "sigma": sigma, "arm": arm, "seed": seed, **summary_of(r)}
                    for m, r in (("oracle", oracle), ("paga_dpt", own))
                ]
        print(f"synthetic: seed {seed} done", file=sys.stderr, flush=True)
    summary = summarise(rows, len(SEEDS))
    return {
        "rows": rows,
        "summary": summary,
        "decisions": {m: decide(summary, m) for m in ("oracle", "paga_dpt")},
    }


def run_sheih(workdir: Path) -> dict[str, Any]:
    from lumencell.clonal.labels import encode_clones
    from lumencell.clonal.scores import baseline_space, kmeans_partition
    from lumencell.data.loader import load
    from lumencell.engine.context import InferenceContext
    from lumencell.engine.registry import run_method
    from lumencell.prep.cache import PrepCache
    from lumencell.prep.stages import PrepParams
    from lumencell.trust.clonal import settings_columns

    from ctr.case_study import load_declaration, split_units
    from ctr.datasets import CASE_STUDIES
    from ctr.download import local_path

    decl = load_declaration("sheih2020")
    s = decl.settings
    out: dict[str, Any] = {}
    for unit, path in split_units(
        local_path(CASE_STUDIES["sheih2020"]), decl.unit_key, workdir / "units"
    ).items():
        ds = load(path)
        pp = PrepParams()
        prep = PrepCache(ds, workdir / "cache").run(pp)
        ctx = InferenceContext.from_prep(ds, prep, pp, clonal_columns=settings_columns(s))
        pca = np.asarray(prep.artifacts["pca"])
        obs = ds.obs
        codes = encode_clones(
            obs[s.clone_key].to_numpy(dtype=object),
            None if s.donor_key is None else obs[s.donor_key].to_numpy(dtype=object),
            [obs[k].to_numpy(dtype=object) for k in s.strata_keys],
        )
        for method in decl.methods:
            res = run_method(ctx, method, decl.root)
            pt = np.asarray(res.pseudotime, dtype=np.float64)
            base = kmeans_partition(baseline_space(pca, pp.neighbors_pcs), int(res.membership.shape[0]), 0)
            point = score_clonal(res.membership, codes, pt, base)
            out[f"{unit}/{method}"] = {
                "point": summary_of(point),
                "bootstrap": clone_bootstrap(res.membership, codes, pt, base),
                "eta_base": point.eta_base,
            }
            print(f"sheih: {unit} {method} done", file=sys.stderr, flush=True)
    return out


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("part", choices=["synthetic", "sheih"])
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    from ctr.gates import load_thresholds

    with tempfile.TemporaryDirectory(prefix="ctr-clonal-") as tmp:
        payload = (
            run_synthetic(load_thresholds(), Path(tmp)) if args.part == "synthetic" else run_sheih(Path(tmp))
        )
    write_json(args.out, payload)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
