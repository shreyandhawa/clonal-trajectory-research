import tomllib

from ctr.gates import THRESHOLDS, TOOL_THRESHOLDS, deep_merge, load_thresholds


def test_deep_merge_merges_tables_and_replaces_values() -> None:
    base = {"a": {"x": 1, "y": {"p": 1}}, "b": [1]}
    assert deep_merge(base, {"a": {"y": {"q": 2}, "z": 3}, "b": [2]}) == {
        "a": {"x": 1, "y": {"p": 1, "q": 2}, "z": 3},
        "b": [2],
    }
    assert base == {"a": {"x": 1, "y": {"p": 1}}, "b": [1]}


def test_the_research_file_only_holds_what_research_owns() -> None:
    ours = tomllib.loads(THRESHOLDS.read_text(encoding="utf-8"))
    assert set(ours) == {"real", "case_study", "clonal", "tree_support"}
    assert set(ours["clonal"]) == {"calibration", "calibration_n2_amended"}
    assert set(ours["tree_support"]) == {"calibration", "verification"}


def test_loaded_thresholds_are_the_tools_with_the_research_on_top() -> None:
    tool = tomllib.loads(TOOL_THRESHOLDS.read_text(encoding="utf-8"))
    cfg = load_thresholds()
    assert cfg["synthetic"] == tool["synthetic"] and cfg["regression"] == tool["regression"]
    assert cfg["clonal"]["metric_version"] == tool["clonal"]["metric_version"]
    assert "pancreas" in cfg["real"] and "sheih2020" in cfg["case_study"]
