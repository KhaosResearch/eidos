.PHONY: lint format tests

lint:
	@python -m ruff check --extend-select I .

format:
	@python -m ruff format .

tests:
	@python -m pytest tests/