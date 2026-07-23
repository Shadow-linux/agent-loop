#!/usr/bin/env bash
# DEPRECATED COMPATIBILITY ENTRY: use check-root-agents-blocks.py directly.
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if [[ -n "${PYTHON:-}" ]]; then
  python_cmd=("$PYTHON")
elif command -v py >/dev/null 2>&1; then
  python_cmd=(py -3)
elif command -v python3 >/dev/null 2>&1; then
  python_cmd=(python3)
elif command -v python >/dev/null 2>&1; then
  python_cmd=(python)
else
  printf '%s\n' 'usage error: Python 3.10+ is required' >&2
  exit 2
fi

exec "${python_cmd[@]}" "$script_dir/check-root-agents-blocks.py" "$@"
