"""Gate evaluation from lumencell, with this repo's research declarations merged over the tool's policy.

lumencell ships the synthetic gates, the [clonal] and [tree_support] definitions, the regression
rule and the baseline (lumencell/bench/policy). benchmarks/thresholds.toml here holds only what
the research owns: [real.*], [case_study.*], [clonal.calibration*], [tree_support.calibration] and
[tree_support.verification]. It is deep-merged over the tool's file, so a key set here wins.
"""

from pathlib import Path
from typing import Any

from lumencell.bench.gates import (
    BASELINE,
    HIGHER_IS_BETTER,
    GateFailure,
    check_gates,
    check_regression,
    load_baseline,
)
from lumencell.bench.gates import THRESHOLDS as TOOL_THRESHOLDS
from lumencell.bench.gates import load_thresholds as _load_toml

REPO = Path(__file__).resolve().parents[2]
THRESHOLDS = REPO / "benchmarks" / "thresholds.toml"

__all__ = [
    "BASELINE",
    "HIGHER_IS_BETTER",
    "REPO",
    "THRESHOLDS",
    "TOOL_THRESHOLDS",
    "GateFailure",
    "check_gates",
    "check_regression",
    "deep_merge",
    "load_baseline",
    "load_thresholds",
]


def deep_merge(base: dict[str, Any], over: dict[str, Any]) -> dict[str, Any]:
    """``base`` with ``over`` laid on top: tables merge key by key, any other value is replaced."""
    out = dict(base)
    for key, value in over.items():
        both_tables = isinstance(value, dict) and isinstance(out.get(key), dict)
        out[key] = deep_merge(out[key], value) if both_tables else value
    return out


def load_thresholds(path: Path = THRESHOLDS) -> dict[str, Any]:
    return deep_merge(_load_toml(TOOL_THRESHOLDS), _load_toml(path))
