PY = python3
VENV = venv
BIN = $(VENV)/bin

.PHONY: venv

# Targets for service setup
venv:
	./resources/scripts/make_env.sh

# Targets for service release
release: test deploy

# Targets for rudeler deployment
package:
	./resources/scripts/make_cloud_functions_archive.sh

deploy-init:
	./resources/scripts/make_deploy_init.sh $(environment)

deploy-plan: package deploy-init
	./resources/scripts/make_deploy_plan.sh $(environment)

deploy: package deploy-init
	./resources/scripts/make_deploy.sh $(environment)

# Targets for testing and coverage
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
