.PHONY: install lint typecheck test test-all real report paper-numbers paper-reproduce

install:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .

typecheck:
	uv run mypy

test:
	uv run pytest -m "not real_data and not slow"

test-all:
	uv run pytest -m "not real_data"

# Real datasets (download first: uv run ctr fetch all). A release gate, not CI.
real:
	uv run pytest -m real_data -q
	uv run ctr real

report:
	uv run ctr report --readme

# The paper's headline numbers, from the saved result files (seconds).
paper-numbers:
	uv run python -m ctr.paper_numbers

# Re-run both diagnoses from the cached datasets (uv run ctr fetch sheih2020 first) and check that
# every headline number comes out the same. About 30 minutes. R1 reads lumenCell_V2 commit 37197c8
# through a bare clone and git archive into $(W), never a checkout of that repo.
W ?= $(or $(TMPDIR),/tmp/)ctr-paper-reproduce
LC_URL ?= https://github.com/shreyandhawa/lumenCell_V2.git
paper-reproduce:
	rm -rf $(W) && mkdir -p $(W)/lc-37197c8
	uv run python -m ctr.diagnosis_verdict rederive --out $(W)/rederive.json
	uv run python -m ctr.diagnosis_verdict criteria --out $(W)/criteria.json
	uv run python -m ctr.diagnosis_verdict structure --out $(W)/structure.json --workdir $(W)/work-structure
	uv run python -m ctr.diagnosis_verdict reproduce --out $(W)/r2.json --workdir $(W)/work-r2
	git clone -q --bare $(LC_URL) $(W)/lc.git
	git -C $(W)/lc.git archive 37197c8 src benchmarks | tar -x -C $(W)/lc-37197c8
	PYTHONPATH=$(W)/lc-37197c8/src uv run python -m ctr.diagnosis_verdict reproduce --out $(W)/r1.json --workdir $(W)/work-r1
	uv run python -m ctr.diagnosis_clonal synthetic --out $(W)/synthetic.json
	uv run python -m ctr.diagnosis_clonal sheih --out $(W)/sheih.json
	uv run python -m ctr.paper_numbers --fresh $(W)
