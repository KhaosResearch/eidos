.PHONY: lint format tests

lint:
	@python -m ruff check --extend-select I .

lint-fix:
	@python -m ruff check --extend-select I --fix .

format:
	@python -m ruff format .

tests:
	@python -m pytest tests/
