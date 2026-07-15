#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
checker="$root/scripts/check-root-agents-blocks.py"
template="$root/templates/root-AGENTS.md"
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    printf '%s\n' '--- file content ---' >&2
    cat "$file" >&2
    exit 1
  fi
}

assert_not_contains() {
  local file=$1
  local text=$2
  if grep -Fq -- "$text" "$file"; then
    printf 'FAIL: %s contains unexpected text: %s\n' "$file" "$text" >&2
    printf '%s\n' '--- file content ---' >&2
    cat "$file" >&2
    exit 1
  fi
}

remove_section() {
  local section=$1
  local source=$2
  local target=$3
  awk -v section="$section" '
    $0 ~ "<!-- agent-loop:managed-start section:" section "([ >]| )" { skip=1; next }
    $0 ~ "<!-- agent-loop:managed-end section:" section " -->" { skip=0; next }
    skip != 1 { print }
  ' "$source" > "$target"
}

if [ ! -f "$checker" ]; then
  printf 'FAIL: checker script is missing: %s\n' "$checker" >&2
  exit 1
fi

cp "$template" "$tmpdir/ok.md"
mkdir -p "$tmpdir/.agent-loop"
touch "$tmpdir/.agent-loop/project.md"

python3 "$checker" --template "$template" --target "$tmpdir/ok.md" > "$tmpdir/ok.out"
assert_contains "$tmpdir/ok.out" "PASS root AGENTS managed blocks are current"
assert_not_contains "$tmpdir/ok.out" "FAIL root AGENTS drift found"

remove_section "message-intent" "$template" "$tmpdir/missing.md"
if python3 "$checker" --template "$template" --target "$tmpdir/missing.md" > "$tmpdir/missing.out"; then
  printf 'FAIL: checker should fail when a template managed section is missing\n' >&2
  cat "$tmpdir/missing.out" >&2
  exit 1
fi
assert_contains "$tmpdir/missing.out" "FAIL root AGENTS drift found"
assert_contains "$tmpdir/missing.out" "message-intent | missing"

remove_section "workflow-stage-map" "$template" "$tmpdir/missing-stage-map.md"
if python3 "$checker" --template "$template" --target "$tmpdir/missing-stage-map.md" > "$tmpdir/missing-stage-map.out"; then
  printf 'FAIL: checker should fail when Workflow Stage Map is missing\n' >&2
  cat "$tmpdir/missing-stage-map.out" >&2
  exit 1
fi
assert_contains "$tmpdir/missing-stage-map.out" "FAIL root AGENTS drift found"
assert_contains "$tmpdir/missing-stage-map.out" "workflow-stage-map | missing"

sed 's/block-version:1\.4\.0-20260715/block-version:1.4.0/' "$template" > "$tmpdir/stale.md"
if python3 "$checker" --template "$template" --target "$tmpdir/stale.md" > "$tmpdir/stale.out"; then
  printf 'FAIL: checker should fail when block-version values are stale\n' >&2
  cat "$tmpdir/stale.out" >&2
  exit 1
fi
assert_contains "$tmpdir/stale.out" "message-intent | stale-block-version"
assert_contains "$tmpdir/stale.out" "expected 1.4.0-20260715"

awk '
  /<!-- agent-loop:managed-end section:ownership -->/ { next }
  { print }
' "$template" > "$tmpdir/broken.md"
if python3 "$checker" --template "$template" --target "$tmpdir/broken.md" > "$tmpdir/broken.out"; then
  printf 'FAIL: checker should fail when managed markers are broken\n' >&2
  cat "$tmpdir/broken.out" >&2
  exit 1
fi
assert_contains "$tmpdir/broken.out" "ownership | broken-markers"

awk '
  /<!-- agent-loop:managed-start section:ownership/ && inserted != 1 {
    print
    print "<!-- agent-loop:managed-start section:nested source:.agent-loop/project.md block-version:1.4.0-20260715 -->"
    print "nested"
    print "<!-- agent-loop:managed-end section:nested -->"
    inserted = 1
    next
  }
  { print }
' "$template" > "$tmpdir/nested.md"
if python3 "$checker" --template "$template" --target "$tmpdir/nested.md" > "$tmpdir/nested.out"; then
  printf 'FAIL: checker should fail when managed blocks are nested\n' >&2
  cat "$tmpdir/nested.out" >&2
  exit 1
fi
assert_contains "$tmpdir/nested.out" "ownership | nested-managed-block"

awk '
  { print }
  /<!-- agent-loop:managed-end section:ownership -->/ && inserted != 1 {
    print "<!-- agent-loop:managed-start section:ownership source:.agent-loop/project.md block-version:1.4.0-20260715 -->"
    print "duplicate"
    print "<!-- agent-loop:managed-end section:ownership -->"
    inserted = 1
  }
' "$template" > "$tmpdir/duplicate.md"
if python3 "$checker" --template "$template" --target "$tmpdir/duplicate.md" > "$tmpdir/duplicate.out"; then
  printf 'FAIL: checker should fail when a managed section is duplicated\n' >&2
  cat "$tmpdir/duplicate.out" >&2
  exit 1
fi
assert_contains "$tmpdir/duplicate.out" "ownership | duplicate-section"

{
  cat "$template"
  printf '\n<!-- agent-loop:managed-start section:legacy-extra source:.agent-loop/project.md block-version:1.4.0-20260715 -->\n'
  printf '## Legacy Extra\n\n'
  printf '<!-- agent-loop:managed-end section:legacy-extra -->\n'
} > "$tmpdir/extra.md"
if python3 "$checker" --template "$template" --target "$tmpdir/extra.md" > "$tmpdir/extra.out"; then
  printf 'FAIL: checker should fail when target has an unexpected managed section\n' >&2
  cat "$tmpdir/extra.out" >&2
  exit 1
fi
assert_contains "$tmpdir/extra.out" "legacy-extra | unexpected-managed-section"

awk '
  replaced != 1 && /source:\.agent-loop\/project\.md/ {
    sub(/source:\.agent-loop\/project\.md/, "source:absent-source.md")
    replaced = 1
  }
  { print }
' "$template" > "$tmpdir/source-missing.md"
if python3 "$checker" --template "$template" --target "$tmpdir/source-missing.md" > "$tmpdir/source-missing.out"; then
  printf 'FAIL: checker should fail when a local managed block source is missing\n' >&2
  cat "$tmpdir/source-missing.out" >&2
  exit 1
fi
assert_contains "$tmpdir/source-missing.out" "source-missing"

{
  cat "$template"
  printf '\n<!-- agent-loop:managed-start-->\n'
} > "$tmpdir/bare-start.md"
if python3 "$checker" --template "$template" --target "$tmpdir/bare-start.md" > "$tmpdir/bare-start.out"; then
  printf 'FAIL: checker should fail when a bare managed-start marker is malformed\n' >&2
  cat "$tmpdir/bare-start.out" >&2
  exit 1
fi
assert_contains "$tmpdir/bare-start.out" "malformed-marker"

{
  cat "$template"
  printf '\n<!-- agent-loop:managed-end -->\n'
} > "$tmpdir/bare-end.md"
if python3 "$checker" --template "$template" --target "$tmpdir/bare-end.md" > "$tmpdir/bare-end.out"; then
  printf 'FAIL: checker should fail when a bare managed-end marker is malformed\n' >&2
  cat "$tmpdir/bare-end.out" >&2
  exit 1
fi
assert_contains "$tmpdir/bare-end.out" "malformed-marker"

{
  cat "$template"
  printf '\n<!-- agent-loop:managed-start section:same-line source:.agent-loop/project.md block-version:1.4.0-20260715 --><!-- agent-loop:managed-end section:same-line -->\n'
} > "$tmpdir/same-line.md"
if python3 "$checker" --template "$template" --target "$tmpdir/same-line.md" > "$tmpdir/same-line.out"; then
  printf 'FAIL: checker should fail when multiple managed markers are on the same line\n' >&2
  cat "$tmpdir/same-line.out" >&2
  exit 1
fi
assert_contains "$tmpdir/same-line.out" "malformed-marker"

printf 'PASS: root AGENTS block checker contract is complete\n'
