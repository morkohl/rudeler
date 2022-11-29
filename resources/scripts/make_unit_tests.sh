#!/usr/bin/env bash

source $(dirname $0)/utils.sh

info "Running unit tests"

venv/bin/coverage run --source=src -m pytest tests/unit
