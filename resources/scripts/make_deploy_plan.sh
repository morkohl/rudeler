#!/usr/bin/env bash

set -e

source $(dirname $0)/utils.sh

if [[ -z ${1} ]]; then
  error "Usage: <environment>"
fi

ENVIRONMENT=${1}

cd terraform

info "Deploying terraform for environment ${ENVIRONMENT}"

terraform plan -var-file="configurations/rudeler_${ENVIRONMENT}.tfvars"
