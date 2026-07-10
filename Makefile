.PHONY: setup check lint format test docs serve clean

setup:
	uv sync --locked --all-extras

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest

docs:
	uv run mkdocs build --strict

serve:
	uv run mkdocs serve

check: lint test docs

clean:
	rm -rf site .pytest_cache .ruff_cache .coverage htmlcov
