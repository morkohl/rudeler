#!/usr/bin/env bash

set -e

source $(dirname $0)/utils.sh

info "Getting google cloud secrets for integration tests"

export ASVZ_USERNAME=$(gcloud secrets versions access latest --secret=dev-asvz-username)
export ASVZ_PASSWORD=$(gcloud secrets versions access latest --secret=dev-asvz-password)
export SPOND_USERNAME=$(gcloud secrets versions access latest --secret=dev-spond-username)
export SPOND_PASSWORD=$(gcloud secrets versions access latest --secret=dev-spond-password)

info "Running integration tests"

venv/bin/coverage run --source=src -m pytest tests/integration
