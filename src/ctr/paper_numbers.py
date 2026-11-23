"""Every headline number in the paper, computed from the saved result files.

    python -m ctr.paper_numbers              print each number with its key
    python -m ctr.paper_numbers --fresh DIR  rebuild the numbers from a fresh run's part files
                                             (``make paper-reproduce``) and fail on any difference

The paper's Markdown marks each number as ``<!--n:KEY-->value<!--/n-->``; the test
``tests/unit/test_paper_numbers.py`` checks every marked value against :func:`numbers`.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
RESULTS = REPO / "benchmarks" / "results"
VERDICT = RESULTS / "diagnosis-verdict-2026-11-23.json"
CLONAL = RESULTS / "diagnosis-clonal-2026-11-23.json"
RECORDED = RESULTS / "verdict-verification-2026-11-17.json"
P_MAX = 0.01  # the declared clone-check bar ([clonal] p_max)

Doc = Mapping[str, Any]


def _of(k: int, n: int) -> str:
    return f"{k} of {n}"


def _ci(point: float, ci: list[float]) -> str:
    return f"{point:.3f} [{ci[0]:.3f}, {ci[1]:.3f}]"


def _range(values: list[float]) -> str:
    return f"{min(values):.3f}-{max(values):.3f}"


def _supported(rep: Doc) -> tuple[int, int]:
    scored = [r for r in rep["records"] if r["group"] == "control" and r["error"] is None]
    return len(rep["controls_supported"]), len(scored)


def verdict_numbers(v: Doc, recorded: Doc) -> dict[str, str]:
    out: dict[str, str] = {}
    out["verdict.recorded"] = _of(*_supported(recorded))
    out["verdict.r2"] = _of(*_supported(v["reproduce_on_0_5_0"]))
    r1 = v["reproduce_at_37197c8"]
    out["verdict.r1"] = _of(*_supported(r1))
    changed = {d.split(":")[0] for d in r1["differences"]}
    out["verdict.r1_match"] = _of(len(r1["records"]) - len(changed), len(r1["records"]))
    kinds = ("blob", "loop", "sheet", "two_groups")
    by_kind = [s.split("/")[0] for s in v["reproduce_on_0_5_0"]["controls_supported"]]
    out["verdict.r2_by_kind"] = ", ".join(f"{k} {by_kind.count(k)}" for k in kinds)
    out["verdict.rederive"] = _of(v["rederive"]["n"] - len(v["rederive"]["mismatches"]), v["rederive"]["n"])
    crit, n = v["criteria"], v["criteria"]["n_controls"]
    out["verdict.c1_alone"] = _of(crit["criteria"]["C1@fixed"]["passes"], n)
    for c in ("C2", "C3", "C4"):
        out[f"verdict.{c.lower()}_alone"] = _of(crit["criteria"][f"{c}@matrix_q"]["passes"], n)
    out["verdict.all_four_q10"] = _of(crit["combos"]["C1+C2+C3+C4@matrix_q"], n)
    out["verdict.all_four_min"] = _of(crit["combos"]["C1+C2+C3+C4@matrix_min"], n)
    ds = v["structure"]["datasets"]
    out["verdict.defect.trees"] = _range([d["defect99"] for d in ds if d["group"] == "matrix"])
    for k in kinds:
        out[f"verdict.defect.{k}"] = _range([d["defect99"] for d in ds if d["kind"] == k])
    return out


def clonal_numbers(c: Doc) -> dict[str, str]:
    out: dict[str, str] = {}
    runs = c["sheih_bootstrap"]
    ratios, deltas, above, below, passes = [], [], 0, 0, 0
    for run, r in runs.items():
        p, ci = r["point"], r["bootstrap"]["ci"]
        ratio = p["eta"]["N3"] / p["eta"]["N1"]
        ratios.append(ratio)
        deltas.append(p["delta_eta"])
        above += ci["delta_eta"][0] > 0
        below += ci["delta_eta"][1] < 0
        passes += max(p["p"].values()) <= P_MAX and p["delta_eta"] > 0
        for null in ("N1", "N3"):
            out[f"clonal.{run}.eta_{null}"] = _ci(p["eta"][null], ci[null])
        out[f"clonal.{run}.R"] = _ci(ratio, ci["R"])
        out[f"clonal.{run}.delta"] = _ci(p["delta_eta"], ci["delta_eta"])
        out[f"clonal.{run}.R_hi"] = f"{ci['R'][1]:.3f}"
    n = len(runs)
    out["clonal.n_runs"] = str(n)
    out["clonal.R_under_half"] = _of(sum(x < 0.5 for x in ratios), n)
    out["clonal.R_range"] = f"{min(ratios):.2f} to {max(ratios):.2f}"
    out["clonal.delta_range"] = f"{min(deltas):+.3f} to {max(deltas):+.3f}"
    out["clonal.delta_abs_max"] = f"{max(abs(d) for d in deltas):.2f}"
    out["clonal.delta_ci_above"] = str(above)
    out["clonal.delta_ci_below"] = str(below)
    out["clonal.pass"] = _of(passes, n)
    cells = c["synthetic"]["summary"]["cells"]
    for sigma in ("0.1", "0.4"):
        out[f"clonal.syn.T1.eta_N1.{sigma}"] = f"{cells[f'oracle/{sigma}/T1']['eta_median_ci']['N1'][0]:.3f}"
        out[f"clonal.syn.T2.R.{sigma}"] = f"{cells[f'oracle/{sigma}/T2']['ratio_median_ci'][0]:.2f}"
    out["clonal.syn.n_seeds"] = str(c["synthetic"]["summary"]["n_seeds"])
    d1 = {m["per_sigma"][s]["D1"] for m in c["synthetic"]["decisions"].values() for s in m["per_sigma"]}
    out["clonal.syn.D1"] = "fails" if d1 == {False} else "holds" if d1 == {True} else "mixed"
    return out


def _load(path: Path) -> dict[str, Any]:
    doc: dict[str, Any] = json.loads(path.read_text())
    return doc


def numbers(
    verdict: Doc | None = None, clonal: Doc | None = None, recorded: Doc | None = None
) -> dict[str, str]:
    """Every number the paper may cite, keyed, formatted as the text writes it."""
    v, r, c = verdict or _load(VERDICT), recorded or _load(RECORDED), clonal or _load(CLONAL)
    return verdict_numbers(v, r) | clonal_numbers(c)


def assemble(fresh: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """The two diagnosis documents, rebuilt from ``make paper-reproduce``'s part files."""

    def part(name: str) -> dict[str, Any]:
        return _load(fresh / f"{name}.json")

    verdict = {k: part(k) for k in ("rederive", "criteria", "structure")}
    verdict |= {"reproduce_at_37197c8": part("r1"), "reproduce_on_0_5_0": part("r2")}
    return verdict, {"synthetic": part("synthetic"), "sheih_bootstrap": part("sheih")}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fresh", type=Path, help="directory of a fresh run's part files")
    args = ap.parse_args(argv)
    saved = numbers()
    if args.fresh is None:
        for k, val in saved.items():
            print(f"{k:40s} {val}")
        return 0
    fresh = numbers(*assemble(args.fresh))
    bad = {k: (saved[k], fresh.get(k)) for k in saved if fresh.get(k) != saved[k]}
    for k, (a, b) in bad.items():
        print(f"DIFFERS {k}: saved {a}, fresh {b}")
    print(f"{len(saved) - len(bad)} of {len(saved)} numbers reproduce")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
