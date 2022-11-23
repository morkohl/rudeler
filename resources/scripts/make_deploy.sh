#!/usr/bin/env bash

set -e

RED="\033[0;31m"
GREEN="\033[0;32m"
NC="\033[0;0m"

function info() {
  echo -e "\n${GREEN}#### ${1}... #####${NC}\n"
}

function error() {
  echo -e "${RED}Error: ${1}${NC}"
  exit 1
}

if [[ -z ${1} ]]; then
  error "Usage: <environment>"
fi

ENVIRONMENT=${1}

cd terraform

info "Initialize terraform for environment ${ENVIRONMENT}"

terraform init \
  -backend-config="bucket=rudeler-bucket-tfstate" \
  -backend-config="prefix=terraform/state/${ENVIRONMENT}"

info "Deploying terraform for environment ${ENVIRONMENT}"

terraform apply -var="environment=${ENVIRONMENT}"
