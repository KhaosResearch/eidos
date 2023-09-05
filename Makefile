lint:
	@python -m ruff src/

format:
	@python -m black src/
	@python -m isort --profile black src/