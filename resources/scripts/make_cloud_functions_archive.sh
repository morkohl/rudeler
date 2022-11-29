#!/usr/bin/env bash

source $(dirname $0)/utils.sh

ZIP_DIRECTORY=temp
ZIP_FILE=rudeler.zip

[ -e ${ZIP_FILE} ] && rm ${ZIP_FILE}

info "Creating archive ${ZIP_FILE}"

mkdir -p ${ZIP_DIRECTORY}

cp -r src/* ${ZIP_DIRECTORY}
cp requirements.txt ${ZIP_DIRECTORY}

(cd ${ZIP_DIRECTORY}; zip -r ../${ZIP_FILE} .)

info "Removing archive staging directory"

rm -rf ${ZIP_DIRECTORY}
