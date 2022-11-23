#!/usr/bin/env bash

set -e

source $(dirname $0)/utils.sh

if [[ -z ${1} ]]; then
  error "Usage: <environment>"
fi

ENVIRONMENT=${1}

cd terraform

info "Initialize terraform for environment ${ENVIRONMENT}"

terraform init \
  -backend-config="bucket=rudeler-bucket-tfstate" \
  -backend-config="prefix=terraform/state/${ENVIRONMENT}"
