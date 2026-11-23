.PHONY: install lint typecheck test test-all real report

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
