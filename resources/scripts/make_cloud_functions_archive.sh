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

ZIP_DIRECTORY=temp
ZIP_FILE=rudeler.zip

[ -e ${ZIP_FILE} ] && rm ${ZIP_FILE}

info "Creating archive ${ZIP_FILE}"

mkdir -p ${ZIP_DIRECTORY}

cp -r src/* ${ZIP_DIRECTORY}
cp requirements.txt ${ZIP_DIRECTORY}
cp .env.$1 ${ZIP_DIRECTORY}

(cd ${ZIP_DIRECTORY}; zip -r ../${ZIP_FILE} .)

info "Removing archive staging directory"

rm -rf ${ZIP_DIRECTORY}
