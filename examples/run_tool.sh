#!/usr/bin/env bash
set -euo pipefail
example_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
"${PYTHON:-python3}" "$example_dir/run_examples.py" "$@"
