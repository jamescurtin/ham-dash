#!/usr/bin/env bash
# TOOD: Customize
set -euo pipefail

CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE_DIR="$(dirname "$CURRENT_DIR")"

BLACK_ARGS=""
ISORT_ARGS=""

while test $# -gt 0
do
    case "$1" in
        --check-only)
            BLACK_ARGS="--check"
            ISORT_ARGS="--check"
            ;;
        *)
            ;;
    esac
    shift
done

echo "Running black..."
black ${BLACK_ARGS} --config "${BASE_DIR}/pyproject.toml" "${BASE_DIR}"
echo "Running isort..."
isort ${ISORT_ARGS} --settings-path "${BASE_DIR}/pyproject.toml" "${BASE_DIR}"
echo "Running flake8..."
flake8
echo "Running pydocstyle..."
pydocstyle
