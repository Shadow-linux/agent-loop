#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || {
    printf 'FAIL: %s missing: %s\n' "$file" "$text" >&2
    exit 1
  }
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains references/external-skill-adapters.md 'Optional Visual Communication Adapter'
assert_contains references/external-skill-adapters.md 'https://github.com/tt-a1i/archify'
assert_contains references/external-skill-adapters.md 'preferred when a Visual Trigger materially lowers misunderstanding risk'
assert_contains references/external-skill-adapters.md 'Installation Authorization'
assert_contains references/external-skill-adapters.md 'Visual Scope Grant'
assert_contains references/external-skill-adapters.md 'Do not offer Markdown / table / Mermaid / ASCII as the first drawing path merely because Archify is absent.'
assert_contains references/external-skill-adapters.md 'recommend Archify before fallback when it would materially improve review'
assert_contains references/external-skill-adapters.md 'do not hard-code one cross-runtime install command'
assert_contains references/external-skill-adapters.md 'does not authorize Product Human Review, ADR acceptance, Feature start, Git, release, publish, or future external actions'
assert_contains references/skill-routing.md 'optional visual communication adapter'
assert_not_contains references/skill-routing.md '| Requirements Visual Communication | `archify` |'
assert_contains references/skill-routing.md '| Feature Spec | spec writing; optional visual communication on a Visual Trigger |'
assert_contains references/runtime.md 'recommend Archify before offering Mermaid / table / ASCII fallback'
assert_contains references/runtime.md 'Feature Spec may use a visual only to explain the accepted Product Slice, feature responsibility, or feature-local implementation and acceptance path.'
assert_contains references/external-skill-adapters.md 'Feature Spec visuals may explain only the accepted Product Slice, feature responsibility, and its feature-local implementation or acceptance path.'
assert_contains references/product-definition.md 'render to converge, text to record'
assert_contains references/product-definition.md 'source-render-v1'
assert_contains references/project-decisions.md 'Optional Visual Evidence'
assert_contains references/onboarding-knowledge-base.md 'archify-source-render'
assert_contains templates/product.md 'Visual Manifest Contract: source-render-v1'
assert_contains templates/decision.md '## Optional Visual Evidence'
assert_contains templates/onboarding-db/flow.md 'Representation: embedded-mermaid | embedded-ascii | archify-source-render'
assert_contains README.md 'https://github.com/tt-a1i/archify'
assert_contains Usage.md 'Visual Scope Grant'
assert_contains Usage.md '不要因为 Archify 尚未安装就先把 Mermaid 当成默认画图方案'
assert_contains references/validation-scenarios.md 'Archify-first Recommendation Before Mermaid Fallback'
assert_contains references/stage-guides.md 'rewrite accepted feature-local clarification into `spec.md`; if the view reveals new product meaning, stop and return to Requirements Discussion'
assert_contains references/workflow-checklists.md 'Feature Spec visuals may explain only the accepted Product Slice and its feature-local implementation or acceptance path'
assert_contains references/validation-scenarios.md 'Feature Spec Visual Cannot Create Product Meaning'
assert_contains README.md 'In Feature Spec, a visual may explain only the accepted Product Slice, feature responsibility, and feature-local implementation or acceptance path.'
assert_contains Usage.md '在 Feature Spec 中，图只能解释已接受的 Product Slice、Feature 责任和 Feature-local 实现/验收路径。'
assert_contains Usage.md '遇到 Visual Trigger 时仍按 active project-local visual skill → installed Archify → materially useful recommendation → Mermaid/ASCII fallback 选择'
assert_contains CHANGELOG.md 'accepted Product Slice, feature responsibility, and feature-local implementation/acceptance path'

printf 'PASS: optional visual communication adapter routing, gates, durable source/render, fallback, and compatibility contract is complete\n'
