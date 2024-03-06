.PHONY: lint format tests

lint:
	@python -m ruff --extend-select I src/ tests/

format:
	@python -m ruff format src/ tests/

tests:
	@python -m pytest tests/