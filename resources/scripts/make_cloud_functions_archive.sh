#!/usr/bin/env bash

set -e

if [[ -z $1 ]]; then
    echo "Error: usage: make_archive <environment>"
    exit 1
fi

ZIP_DIRECTORY=cloud_functions_sources_archive
ZIP_FILE=rudeler.zip

[ -e ${ZIP_FILE} ] && rm ${ZIP_FILE}

mkdir -p ${ZIP_DIRECTORY}

cp -r src/* ${ZIP_DIRECTORY}
cp requirements.txt ${ZIP_DIRECTORY}
cp .env.$1 ${ZIP_DIRECTORY}

(cd ${ZIP_DIRECTORY}; zip -r ../${ZIP_FILE} .)

rm -rf ${ZIP_DIRECTORY}
