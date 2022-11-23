#!/usr/bin/env bash

set -e

if [[ -z $1 ]]; then
    echo "Error: usage: make_deploy <environment>"
    exit 1
fi

cd terraform

terraform init \
  -backend-config="bucket=rudeler-bucket-tfstate" \
  -backend-config="prefix=terraform/state/$1"

terraform apply -var="environment=$1"
