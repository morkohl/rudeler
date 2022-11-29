#!/usr/bin/env bash

source $(dirname $0)/utils.sh

info "Getting google cloud secrets for integration tests"

export ASVZ_USERNAME=$(gcloud secrets versions access latest --secret=rudeler-dev-asvz-username)
export ASVZ_PASSWORD=$(gcloud secrets versions access latest --secret=rudeler-dev-asvz-password)
export SPOND_USERNAME=$(gcloud secrets versions access latest --secret=rudeler-dev-spond-username)
export SPOND_PASSWORD=$(gcloud secrets versions access latest --secret=rudeler-dev-spond-password)

info "Running integration tests"

venv/bin/coverage run --source=src -m pytest tests/integration
