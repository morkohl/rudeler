#!/usr/bin/env bash

source $(dirname $0)/deploy_utils.sh

info "Planning rudeler deployment for environment '${ENVIRONMENT}'"

terraform apply -var-file="configurations/rudeler_${ENVIRONMENT}.tfvars" -auto-approve
