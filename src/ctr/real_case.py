"""Run a method on a downloaded real dataset and score it."""

import time
from typing import Any

import numpy as np
from lumencell.bench.metrics import score
from lumencell.bench.runner import CaseResult, StabilityRow, stability_row
from lumencell.data.loader import load
from lumencell.engine.context import InferenceContext
from lumencell.engine.registry import run_method
from lumencell.engine.roots import parse_root
from lumencell.prep.cache import PrepCache
from lumencell.prep.stages import PrepParams

from ctr.datasets import DATASETS, is_cached, local_path, truth_for
from ctr.real_clonal import real_clonal_row, reported_metrics


def run_real_case(
    dataset_id: str, method: str = "paga_dpt", params: dict[str, Any] | None = None, stability: bool = False
) -> CaseResult:
    """Run a method on a downloaded real dataset (prep is cached) and score it."""
    ds = DATASETS[dataset_id]
    if not is_cached(ds):
        raise FileNotFoundError(f"{dataset_id} is not downloaded; run: ctr fetch {dataset_id}")
    start = time.perf_counter()
    data = load(local_path(ds))
    pp = PrepParams()
    prep = PrepCache(data).run(pp)
    clonal_columns = ds.clonal.columns() if ds.clonal else ()
    ctx = InferenceContext.from_prep(data, prep, pp, clonal_columns=clonal_columns)
    result = run_method(ctx, method, parse_root(ds.root_spec), params=params, label_key=ds.label_key)
    elapsed = time.perf_counter() - start  # stops before stability, so runtime stays comparable
    stab = (
        stability_row(data, prep, pp, result, ds.label_key, clonal_columns)
        if stability
        else StabilityRow("not_measured")
    )
    truth = truth_for(ds, data.obs)
    pca = np.asarray(prep.artifacts["pca"]) if ds.clonal else None
    return CaseResult(
        case=dataset_id,
        method=method,
        scores=score(result.pseudotime, result.membership, truth),
        n_clusters=int(ctx.leiden.max()) + 1,
        runtime_seconds=elapsed,
        warnings=[w.code for w in result.warnings],
        clonal=real_clonal_row(ds, truth, result, pca, pp.neighbors_pcs),
        stability=stab,
        reported=reported_metrics(ds, data.obs, result, truth, pca, pp.neighbors_pcs),
    )
