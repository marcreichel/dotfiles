#!/bin/sh
# Run a model script with stlkit importable. Creates the venv on first use.
# Usage: run.sh model.py [args...]   (outputs land in the current directory)
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -x "$DIR/.venv/bin/python" ]; then
  python3 -m venv "$DIR/.venv"
  "$DIR/.venv/bin/pip" install -q manifold3d numpy matplotlib
fi
PYTHONPATH="$DIR${PYTHONPATH:+:$PYTHONPATH}" exec "$DIR/.venv/bin/python" "$@"
