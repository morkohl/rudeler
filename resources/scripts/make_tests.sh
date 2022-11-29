#!/usr/bin/env bash

source $(dirname $0)/utils.sh

info "Running all tests"

./$(dirname $0)/make_unit_tests.sh
./$(dirname $0)/make_integration_tests.sh

