.PHONY: lint format tests
lint:
	@python -m ruff src/

format:
	@python -m black src/
	@python -m isort --profile black src/

tests:
	@newman run tests/eidos-api-testing.postman_collection.json -e tests/development.postman_environment.json