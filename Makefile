PY = python3
VENV = venv
BIN = $(VENV)/bin

.PHONY: venv

venv:
	./resources/scripts/make_env.sh

test:
	RUDELER_ENV_FILE=.env.integrationtest $(BIN)/coverage run --source=src -m pytest tests/unit tests/integration
	$(BIN)/coverage report

unittest:
	$(BIN)/coverage run --source=src -m pytest tests/unit
	$(BIN)/coverage report

integrationtest:
	RUDELER_ENV_FILE=.env.integrationtest $(BIN)/coverage run --source=src -m pytest tests/integration
	$(BIN)/coverage report

coverage: test
	$(BIN)/coverage html