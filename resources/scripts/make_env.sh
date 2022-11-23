#!/usr/bin/env bash

set -e

source $(dirname $0)/utils.sh

info "Removing old environment"

[ -d venv ] && rm -rf venv

info "Creating virtual environment"

python3 -m venv venv

info "Activating virtual environment"

source venv/bin/activate

info "Installing packages"

python3 -m pip install -r requirements.txt

info "Installing dev packages"

python3 -m pip install -r requirements-dev.txt

info "Use 'source venv/bin/activate' to use the environment"
