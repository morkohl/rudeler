#!/usr/bin/env bash

source $(dirname $0)/utils.sh

if [[ -z ${1} ]]; then
  error "Usage: <environment>"
fi

ENVIRONMENT=${1}

cd deployment/service
