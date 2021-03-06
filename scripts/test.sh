#!/usr/bin/env bash
set -euo pipefail

CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE_DIR="$(dirname "$CURRENT_DIR")"

pytest --cov-report term-missing:skip-covered --cov-report=xml --cov-fail-under=95 --cov="${BASE_DIR}/app" "${BASE_DIR}/test" "$*"
