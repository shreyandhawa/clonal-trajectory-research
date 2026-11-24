"""The paper's marked numbers match the result files.

A number in docs/paper/claim.md or draft.md is written ``<!--n:KEY-->value<!--/n-->``;
``ctr.paper_numbers.numbers()`` computes KEY from the saved result files.
"""

import json
import re

import pytest

from ctr import paper_numbers

PAPER = paper_numbers.REPO / "docs" / "paper"
TAG = re.compile(r"<!--n:([^>]+?)-->(.*?)<!--/n-->", re.S)
DOCS = [p for p in (PAPER / "claim.md", PAPER / "draft.md") if p.exists()]


def _tags(text: str) -> list[tuple[str, str]]:
    # A tagged value may wrap across lines, inside a blockquote or an indented footnote.
    return [(k, re.sub(r"\s*\n[>\s]*", " ", v).strip()) for k, v in TAG.findall(text)]


@pytest.fixture(scope="module")
def nums() -> dict[str, str]:
    return paper_numbers.numbers()


@pytest.mark.parametrize("doc", DOCS, ids=lambda p: p.name)
def test_marked_numbers_match_the_result_files(doc, nums):
    tags = _tags(doc.read_text())
    assert tags, f"{doc.name} marks no numbers"
    wrong = [(k, v, nums.get(k, "<no such key>")) for k, v in tags if nums.get(k) != v]
    assert not wrong, "\n".join(f"{k}: text {v!r}, result files {n!r}" for k, v, n in wrong)


def test_headline_numbers(nums):
    # The values the diagnosis pages state; a change to a result file must be seen here first.
    assert nums["verdict.r2"] == "27 of 30"
    assert nums["verdict.recorded"] == "28 of 31"
    assert nums["verdict.r1"] == "31 of 34"
    assert nums["verdict.r1_match"] == "69 of 72"
    assert nums["verdict.all_four_q10"] == "2 of 31"
    assert nums["verdict.all_four_min"] == "4 of 31"
    assert nums["verdict.rederive"] == "67 of 67"
    assert nums["clonal.R_under_half"] == "12 of 12"
    assert nums["clonal.R_range"] == "0.03 to 0.49"
    assert nums["clonal.delta_ci_above"] == "4"
    assert nums["clonal.delta_ci_below"] == "3"
    assert nums["clonal.pass"] == "4 of 12"
    assert nums["clonal.syn.D1"] == "fails"


def test_tag_parsing_unwraps_lines():
    assert _tags("x <!--n:a-->0.03 to\n> 0.49<!--/n--> y") == [("a", "0.03 to 0.49")]


def test_fresh_run_compares_against_saved(tmp_path, monkeypatch, capsys):
    v = json.loads(paper_numbers.VERDICT.read_text())
    c = json.loads(paper_numbers.CLONAL.read_text())
    monkeypatch.setattr(paper_numbers, "assemble", lambda _: (v, c))
    assert paper_numbers.main(["--fresh", str(tmp_path)]) == 0
    v["reproduce_on_0_5_0"]["controls_supported"].pop()
    assert paper_numbers.main(["--fresh", str(tmp_path)]) == 1
    assert "DIFFERS verdict.r2: saved 27 of 30, fresh 26 of 30" in capsys.readouterr().out
