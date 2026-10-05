#!/usr/bin/env bash
# One-time setup: makes a virtualenv next to this script and installs demucs + flask.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-}"
for cand in python3.12 python3.11 python3.13 python3; do
  if [ -z "$PY" ] && command -v "$cand" >/dev/null 2>&1; then PY="$cand"; fi
done
echo "using $PY ($($PY --version))"
"$PY" -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
echo
echo "done. start the app with:  ./run.sh"
