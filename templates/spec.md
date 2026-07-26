# Feature Spec: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: draft | active | blocked | paused | closed
Feature Type: normal | maintenance-fix | follow-up

Source Requirements:
- Requirement:
- Prototype:

## Product Requirement Source

- Requirement Set:
- Effective Product Definition:
- Product Definition Profile:
- Product Review Evidence:
- Applicable Decisions:

Resolve the Requirement Set README before Feature Spec. New work uses exactly one confirmed `Effective Product Definition`; legacy work may resolve `Effective Concept Foundation` without migration. Product Review is product-definition evidence only and does not authorize Feature start, implementation, or Git actions.

## Feature Context Snapshot

Requirement Set: .agent-loop/requirements/<requirement-id>/README.md
Requirement Lifecycle: accepted | in-progress | partially-implemented | implemented
Resolved Product Source: .agent-loop/requirements/<requirement-id>/product.md
Product Definition Profile: brief | standard | legacy
Product Review: confirmed | accepted | concept-foundation-not-needed
Product Source SHA-256:
Applicable Decisions: none | .agent-loop/decisions/<decision>.md
Decision Source SHA-256: none | .agent-loop/decisions/<decision>.md=<sha256>
Product Slice References:
Verified At: <ISO-8601 timestamp with timezone>
Freshness: current | refresh-required | blocked

### Product Outcome

### Actors And Core Journey

### Applicable Product Rules And Invariants

### Applicable States, Exceptions, And Recovery

### Feature Boundary And Acceptance Context

This Snapshot is derived execution context, not product authority. The Requirement README resolves the current Effective Product Definition; every Requirement, product, and decision path above is project-root-relative. Generate Product and Decision Markdown SHA-256 values after canonicalizing `CRLF` and lone `CR` to `LF`; legacy raw LF/CRLF digests remain reader-compatible. Run the read-only `scripts/check-feature-context.py` before relying on the Snapshot. `## Product Slice` remains the Feature responsibility and coverage table.

## Product Slice

| Source Section / Model ID | Feature Responsibility | Acceptance Mapping | Coverage |
|---|---|---|---|
| FLOW-... / STATE-... / product.md#... |  |  | in-scope / out-of-scope / not-applicable |

The Product Slice selects this Feature's responsibility and acceptance mapping. It must not redefine the Requirement Product Definition. Return to Requirements Discussion when product meaning must change.

Related Bugs:
Bug Resolution Path: none | flow-back | linked-feature | maintenance-fix

Related Feature:
Flow-back Decision: none | flow-back | linked-new-feature | maintenance-fix | investigate-first | declined-reopen | defer

Bug references point to the owning Bug README and do not copy full Report Origin, reproduction, or evidence into this Feature Spec. Feature acceptance does not authorize Bug close.

Summary:
- 

## Problem / Goal

## Applicable Decisions

-

## Maintenance Fix Scope

Use this section only when `Feature Type: maintenance-fix`.

Problem:

Why this is not flow-back to a recent feature:

Why this is not a new product feature:

Regression / safety risk:

Long-term project memory impact: none | possible | required

## Follow-up / Continuity

Use this section only when this feature is a follow-up, linked new feature, or maintenance fix related to earlier work.

Related Feature:

Original Feature Status:

Why this is not direct reopen / flow-back:

Acceptance / tests / evidence inherited or linked:

Affected paths / APIs / models / jobs:

## Scope

## Stories

### US1: <Story Title>

Why this matters:

Independent test:

Acceptance scenarios:
- Given ..., when ..., then ...

## Acceptance Criteria

## Behavior Changes

### Added

### Modified

### Removed

## Dependencies

## Implements Decisions

| Decision | Design Slice ID | Responsibility | Verification | Coverage Status |
|---|---|---|---|---|
|  | DS-00 |  |  | planned / implemented / verified |

## Design Decisions

Feature-local decisions that do not need standalone project ADR files:

- Decision:
  - Reason:
  - Applies To:
  - Placement: feature-local / Decision & Design candidate / project-decision-not-needed

## Out of Scope

## Open Questions
