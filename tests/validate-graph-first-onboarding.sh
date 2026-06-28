#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1
  local text=$2
  if ! grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s missing required text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_file_exists() {
  local file=$1
  if [[ ! -f "$root/$file" ]]; then
    printf 'FAIL: expected file missing: %s\n' "$file" >&2
    exit 1
  fi
}

assert_contains "SKILL.md" "Quick Onboarding creates a lightweight Graph-first onboarding skeleton"
assert_contains "SKILL.md" "Quick onboarding complete; Deep onboarding not complete."

assert_contains "references/existing-project-onboarding.md" "Quick Onboarding creates a lightweight Graph-first onboarding skeleton"
assert_contains "references/existing-project-onboarding.md" ".agent-loop/onboarding-db/maps/evidence-graph.md"
assert_contains "references/existing-project-onboarding.md" "Quick onboarding complete; Deep onboarding not complete."

assert_contains "references/project-onboarding-scan.md" "Graph-first scan order"
assert_contains "references/project-onboarding-scan.md" "Evidence Graph -> Core Domain Inventory -> Core Flow Inventory -> Main Traffic Flow"
assert_contains "references/project-onboarding-scan.md" "Quick Onboarding creates the lightweight Evidence Graph package"
assert_contains "references/project-onboarding-scan.md" "Targeted Onboarding Scan produces a graph slice"
assert_contains "references/project-onboarding-scan.md" "required-core"
assert_contains "references/project-onboarding-scan.md" "graph-only"
assert_contains "references/project-onboarding-scan.md" "needs-deep-trace"
assert_contains "references/project-onboarding-scan.md" "newcomer-ready"
assert_contains "references/project-onboarding-scan.md" "supporting-summary"
assert_contains "references/project-onboarding-scan.md" "blocked-by-unknown"
assert_contains "references/project-onboarding-scan.md" "HTML/SVG auxiliary visual artifacts cannot replace markdown evidence tables, Mermaid source, or deep trace docs."
assert_contains "references/project-onboarding-scan.md" "Required core flow cannot be marked newcomer-ready while fact source, state writer, Redis key, Kafka topic, callback route, idempotency, retry, compensation, verification, or observability evidence is unknown."

assert_contains "references/onboarding-db-templates.md" "Graph-First Template Set"
assert_contains "references/onboarding-db-templates.md" 'templates/onboarding-db/core-flow-deep-trace.md'
assert_contains "references/onboarding-db-templates.md" 'templates/onboarding-db/core-module-deep-dive.md'
assert_contains "references/onboarding-db-templates.md" 'ordinary/supporting flow template'
assert_contains "references/onboarding-db-templates.md" 'Required core flows must use `core-flow-deep-trace.md`'
assert_contains "references/onboarding-db.md" "Evidence Graph status"
assert_contains "references/onboarding-db.md" "the onboarding-db predates Graph-first onboarding"

assert_contains "references/workflow-checklists.md" "create or refresh the Graph-first Quick package: Evidence Graph, Core Domain Inventory, Core Flow Inventory, Coverage Matrix, and Service Startup Matrix."
assert_contains "references/workflow-checklists.md" "Run Deep in Graph-first order before writing module/flow detail docs."
assert_contains "references/workflow-checklists.md" "Required-core flows cannot remain graph-only, needs-deep-trace, or blocked-by-unknown when Deep onboarding is marked complete."

assert_contains "references/validation-scenarios.md" "Graph-First Quick Onboarding Creates Evidence Graph"
assert_contains "references/validation-scenarios.md" "Core Flow Deep Trace Rejects Thin Flow"
assert_contains "references/validation-scenarios.md" "HTML Diagram Cannot Replace Evidence"

assert_file_exists "templates/onboarding-db/evidence-graph.md"
assert_file_exists "templates/onboarding-db/core-domain-inventory.md"
assert_file_exists "templates/onboarding-db/core-flow-inventory.md"
assert_file_exists "templates/onboarding-db/coverage-matrix.md"
assert_file_exists "templates/onboarding-db/service-startup-matrix.md"
assert_file_exists "templates/onboarding-db/main-traffic-flow.md"
assert_file_exists "templates/onboarding-db/core-flow-deep-trace.md"
assert_file_exists "templates/onboarding-db/core-module-deep-dive.md"
assert_file_exists "templates/onboarding-db/graph-slice.md"

assert_contains "templates/onboarding-db/evidence-graph.md" "Node ID | Type | Name | Scope | Owner / Fact Source | Core Role | Evidence | Confidence | Completion Status | Notes"
assert_contains "templates/onboarding-db/evidence-graph.md" "Edge ID | Source Node ID | Edge Type | Target Node ID | Direction | Sync / Async | Trigger / Condition | Data / State | Evidence Path | Symbol / Config | Risk | Required For Complete | Confidence"
assert_contains "templates/onboarding-db/core-flow-deep-trace.md" "Step ID | Branch | Service | File | Symbol | Input | State Read | State Write | External Call / Message | Failure Path | Verification / Observability"
assert_contains "templates/onboarding-db/core-flow-deep-trace.md" "Concrete Example Linked To Trace Steps"
assert_contains "templates/onboarding-db/core-flow-deep-trace.md" "Branch And Failure Matrix"
assert_contains "templates/onboarding-db/core-flow-deep-trace.md" "HTML/SVG auxiliary visual artifacts cannot replace"
assert_contains "templates/onboarding-db/core-module-deep-dive.md" "Module Role Vocabulary"
assert_contains "templates/onboarding-db/coverage-matrix.md" "graph-only | needs-deep-trace | newcomer-ready"
assert_contains "templates/onboarding-db/graph-slice.md" "Local Completion Decision"
assert_contains "templates/onboarding-db/graph-slice.md" "Global Coverage Impact"
assert_contains "templates/onboarding-db/service-startup-matrix.md" "Service / Process | Command | Config Path | Required Dependencies | Port / Protocol | Health / Failure Signal | Local Runnable? | Evidence | Confidence | Completion Status"

assert_contains "templates/onboarding-db/README.md" "Evidence Graph First Reading Path"
assert_contains "templates/onboarding-db/flow-template.md" 'Required core flows must use `core-flow-deep-trace.md`'
assert_contains "templates/onboarding-db/module-template.md" 'Required-core modules must use `core-module-deep-dive.md`'
assert_contains "templates/onboarding-db/diagram.md" "HTML/SVG auxiliary visual artifacts cannot replace"
assert_contains "templates/onboarding-db/batch-review.md" "Graph / Coverage / Completion Decision"

printf 'PASS: graph-first onboarding contract is complete\n'
