#!/usr/bin/env bash

source $(dirname $0)/deploy_utils.sh

info "Initialize rudeler terraform for environment '${ENVIRONMENT}'"

terraform init \
  -reconfigure \
  -backend-config="bucket=rudeler-bucket-tfstate" \
  -backend-config="prefix=terraform/state/${ENVIRONMENT}/service"
