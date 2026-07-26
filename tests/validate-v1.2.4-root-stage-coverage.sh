#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
template="$root/templates/root-AGENTS.md"
expected_revision="1.5.1-20260725.1"

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

managed_count=$(grep -c '^<!-- agent-loop:managed-start' "$template" || true)
if [ "$managed_count" -ne 13 ]; then
  printf 'FAIL: expected 13 managed blocks, found %s\n' "$managed_count" >&2
  exit 1
fi

if grep '^<!-- agent-loop:managed-start' "$template" | grep -Fvq "block-version:$expected_revision"; then
  printf 'FAIL: every managed block must use same-day-distinguishable revision %s\n' "$expected_revision" >&2
  exit 1
fi

assert_contains "templates/root-AGENTS.md" "## Workflow Gateway Map"
assert_contains "templates/root-AGENTS.md" '| Accepted upstream meaning is ready for implementation or current Feature work continues | Feature Construction / Runtime Continuation | `references/runtime.md`, `references/stage-guides.md` |'
assert_contains "references/runtime.md" "## Stage Order"

assert_contains "references/project-guidance.md" 'Use `block-version:<agent-loop-version>-<YYYYMMDD>[.<same-day-revision>]`'
assert_contains "AGENTS.md" "canonical stage order, routing axes or precedence, root Stage Map signals/references, gate/stop rules, or controller fallback"
assert_contains "AGENTS.md" "update the matching runtime/design source, root Stage Map, project guidance, validation scenarios, and regression tests in the same change"

cd "$root"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_root_agents_lossless_slimming
printf 'PASS: root Gateway projection and runtime leaf-stage coverage are complete\n'
