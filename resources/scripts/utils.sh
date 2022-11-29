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
