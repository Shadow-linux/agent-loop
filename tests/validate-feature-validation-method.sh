#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
method="$root/docs/maintenance/feature-validation-method.md"
report="$root/docs/reports/project-local-skills-feature-validation-2026-07-11.md"

assert_file() {
  local path=$1
  if [ ! -f "$root/$path" ]; then
    printf 'FAIL: missing required file: %s\n' "$path" >&2
    exit 1
  fi
}

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_file "docs/maintenance/feature-validation-method.md"
assert_file "docs/reports/project-local-skills-feature-validation-2026-07-11.md"

assert_contains "$method" "Requirement And Scope Fidelity | 15"
assert_contains "$method" "Logic, State, And Human Gates | 30"
assert_contains "$method" "Cross-Surface Consistency | 20"
assert_contains "$method" "Pressure Resistance | 25"
assert_contains "$method" "Evidence And Maintainability | 10"
assert_contains "$method" "Critical"
assert_contains "$method" "unresolved High"
assert_contains "$method" "RED -> GREEN -> REFACTOR"
assert_contains "$method" "Feature-Scoped Test Boundary"
assert_contains "$method" "does not replace mandatory full validation"

assert_contains "$root/AGENTS.md" "single-feature scoring report"
assert_contains "$root/docs/maintenance/full-validation-method.md" "feature-validation-method.md"

assert_contains "$report" "Total: 96/100"
assert_contains "$report" "Grade: STRONG"
assert_contains "$report" "Requirement And Scope Fidelity"
assert_contains "$report" "Pressure Resistance"
assert_contains "$report" "3/3 PASS"
assert_contains "$report" "tests/validate-project-local-skills.sh"
assert_contains "$report" "Full repository tests: not part of feature score."
assert_contains "$report" "human-deferred"

method_weight_sum=$(awk -F'|' '
  /^\| (Requirement And Scope Fidelity|Logic, State, And Human Gates|Cross-Surface Consistency|Pressure Resistance|Evidence And Maintainability) / {
    value=$3
    gsub(/[^0-9]/, "", value)
    sum += value
  }
  END { print sum + 0 }
' "$method")

if [ "$method_weight_sum" -ne 100 ]; then
  printf 'FAIL: feature-validation weights must total 100, got %s\n' "$method_weight_sum" >&2
  exit 1
fi

score_pair=$(awk -F'|' '
  /^\| (Requirement And Scope Fidelity|Logic, State, And Human Gates|Cross-Surface Consistency|Pressure Resistance|Evidence And Maintainability) / && $3 ~ /\// {
    value=$3
    gsub(/[[:space:]]/, "", value)
    split(value, parts, "/")
    score += parts[1]
    maximum += parts[2]
  }
  END { printf "%d:%d", score, maximum }
' "$report")

score_total=${score_pair%%:*}
score_max=${score_pair##*:}
declared_total=$(sed -n 's/^Total: \([0-9][0-9]*\)\/100.*/\1/p' "$report")
declared_grade=$(sed -n 's/^Grade: \([A-Z][A-Z]*\).*/\1/p' "$report")

if [ "$score_total" -ne "$declared_total" ] || [ "$score_max" -ne 100 ]; then
  printf 'FAIL: report score mismatch: domains=%s/%s declared=%s/100\n' "$score_total" "$score_max" "$declared_total" >&2
  exit 1
fi

if [ "$score_total" -ge 90 ]; then
  expected_grade=STRONG
elif [ "$score_total" -ge 75 ]; then
  expected_grade=STABLE
elif [ "$score_total" -ge 60 ]; then
  expected_grade=FRAGILE
else
  expected_grade=BROKEN
fi

if [ "$declared_grade" != "$expected_grade" ]; then
  printf 'FAIL: report grade mismatch: score=%s expected=%s declared=%s\n' "$score_total" "$expected_grade" "$declared_grade" >&2
  exit 1
fi

for domain in \
  "Logic, State, And Human Gates" \
  "Cross-Surface Consistency" \
  "Pressure Resistance" \
  "Evidence And Maintainability"; do
  assert_contains "$report" "| $domain | -1 |"
done

for evidence in \
  '| `bash tests/validate-project-local-skills.sh` | PASS |' \
  '| Ruby parse `SKILL.md`, `agents/openai.yaml`, `plugin.json` | PASS |' \
  '| Markdown fence balance | PASS |' \
  '| `git diff --check` | PASS |'; do
  assert_contains "$report" "$evidence"
done

printf 'PASS: single-feature logic and pressure scoring method is durable\n'
