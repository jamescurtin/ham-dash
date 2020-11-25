#!/usr/bin/env bash

set -euo pipefail

. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here

# Evaluating passed command:
exec "$@"
