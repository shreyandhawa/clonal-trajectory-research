"""Gate evaluation from lumencell, pointed at this repo's own thresholds and baseline.

benchmarks/thresholds.toml and benchmarks/baseline.json here are the pre-registered record of
the research. They were copied from lumencell 0.4.0 and are not kept in sync with the tool.
"""

from pathlib import Path
from typing import Any

from lumencell.bench.gates import (
    HIGHER_IS_BETTER,
    GateFailure,
    check_gates,
    check_regression,
)
from lumencell.bench.gates import load_baseline as _load_baseline
from lumencell.bench.gates import load_thresholds as _load_thresholds

REPO = Path(__file__).resolve().parents[2]
THRESHOLDS = REPO / "benchmarks" / "thresholds.toml"
BASELINE = REPO / "benchmarks" / "baseline.json"

__all__ = [
    "BASELINE",
    "HIGHER_IS_BETTER",
    "REPO",
    "THRESHOLDS",
    "GateFailure",
    "check_gates",
    "check_regression",
    "load_baseline",
    "load_thresholds",
]


def load_thresholds(path: Path = THRESHOLDS) -> dict[str, Any]:
    return _load_thresholds(path)


def load_baseline(path: Path = BASELINE) -> dict[str, dict[str, dict[str, float]]]:
    return _load_baseline(path)
