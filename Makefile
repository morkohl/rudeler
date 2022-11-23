PY = python3
VENV = venv
BIN = $(VENV)/bin

.PHONY: venv

venv:
	./resources/scripts/make_env.sh

release: test deploy

package:
	./resources/scripts/make_cloud_functions_archive.sh $(environment)

deploy-init:
	./resources/scripts/make_deploy_init.sh	$(environment)

deploy-plan: package deploy-init
	./resources/scripts/make_deploy_plan.sh $(environment)

deploy: package deploy-init
	./resources/scripts/make_deploy.sh $(environment)

test:
	./resources/scripts/make_tests.sh
	make coverage

unit-test:
	./resources/scripts/make_unit_tests.sh
	make coverage

integration-test:
	./resources/scripts/make_integration_tests.sh
	make coverage

coverage:
	$(BIN)/coverage report

coverage-html:
	$(BIN)/coverage html
