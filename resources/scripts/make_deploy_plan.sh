#!/usr/bin/env bash

source $(dirname $0)/deploy_utils.sh

info "Deploying rudeler for environment '${ENVIRONMENT}'"

terraform plan -var-file="configurations/rudeler_${ENVIRONMENT}.tfvars"
