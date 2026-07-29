#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing Feature Archive soft-gate contract: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains references/design.md "reference findings are evidence, not Checker authorization"
assert_contains references/runtime.md "Agent decides whether reference coverage is sufficient"
assert_contains references/stage-guides.md "exact plan SHA-256 Batch Human Gate remains"
assert_contains references/artifact-rules.md "Apply cannot write outside the reviewed plan or project"
assert_contains references/checker-recovery.md "ordinary Archive reference findings do not trigger Checker Recovery"

printf 'PASS: Feature Archive reference findings are Agent-reviewed evidence, not a hard Checker Gate\n'
