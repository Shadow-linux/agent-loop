# Feature Spec: <Feature Name>

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: draft | active | blocked | paused | closed
Feature Type: normal | maintenance-fix | follow-up

Source Requirements:
- Requirement:
- Prototype:

## Feature Authority

Authority Type: <descriptive authority label>
Primary Authority Reference: <project-relative artifact, stable external/ticket locator, or Human decision locator>
Supporting Authority References: none | <semicolon-separated references>
Authority Summary: <behavior and boundary established by this authority>
Agent Authority Assessment: current | changed | unresolved

`Authority Type` is descriptive metadata, not a closed enum. Feature Authority, Bug Authority, and Human Authority are known open adapter families. Requirement Product Definition is the compatible Feature Authority sub-adapter. Existing Features with only `## Product Requirement Source` remain readable without migration. This block defines evidence to inspect; it never accepts itself or authorizes Feature construction, implementation, Bug/Requirement mutation, Git, release, or external action.

## Product Requirement Source

- Requirement Set:
- Effective Product Definition:
- Product Definition Profile:
- Product Review Evidence:
- Applicable Decisions:

Use this section only when the Requirement Product Definition sub-adapter applies. Resolve the Requirement Set README before Feature Spec. An explicit Requirement Product Definition primary authority must identify the same Requirement Set README; applicable ADRs and contracts remain supporting evidence. New Requirement-driven work uses exactly one confirmed `Effective Product Definition`; legacy work may resolve `Effective Concept Foundation` without migration. Bug/Human/custom authority does not invent these fields. Product Review is product-definition evidence only and does not authorize Feature start, implementation, or Git actions.

## Feature Context Snapshot

Authority Type: <same descriptive value as Feature Authority or inferred legacy Requirement Product Definition>
Authority Adapter: <detected open family or named custom adapter>
Primary Authority Reference:
Supporting Authority References: none | <references>
Authority Applicability: applicable | advisory | not-applicable
Authority Facts: <resolver-emitted facts in deterministic semicolon-separated order, including Authority Summary>
Authority Source SHA-256: none | <project-local source>=<sha256>

Requirement Product Definition fields when applicable:

Requirement Set: .agent-loop/requirements/<requirement-id>/README.md
Requirement Lifecycle: accepted | in-progress | partially-implemented | implemented
Resolved Product Source: .agent-loop/requirements/<requirement-id>/product.md
Product Definition Profile: brief | standard | legacy
Product Review: confirmed | accepted | concept-foundation-not-needed
Product Source SHA-256:
Applicable Decisions: none | .agent-loop/decisions/<decision>.md
Decision Source SHA-256: none | .agent-loop/decisions/<decision>.md=<sha256>
Product Slice References:

Bug Authority fields when applicable:

Bug ID:
Expected Behavior Evidence Locator:
Resolution Path / Fix Feature Locator:
Feature Location: flat | archived:<YYYY-MM>

Human/custom authority fields when applicable:

Evidence Locator:
Agent Review Required: yes | no

Verified At: <ISO-8601 timestamp with timezone>
Freshness: current | changed | blocked

### Product Outcome

### Actors And Core Journey

### Applicable Product Rules And Invariants

### Applicable States, Exceptions, And Recovery

### Feature Boundary And Acceptance Context

This Snapshot is derived execution context, not product or authorization authority. Include only fields applicable to the resolved adapter; do not write `none` as a fake local path. Copy `Authority Facts` from the resolver in deterministic semicolon-separated order; do not paraphrase it, and rerun the scanner after `Authority Summary` or any resolved fact changes. Project-local paths are project-root-relative, while external/ticket/Human locators remain evidence strings. Generate applicable Markdown SHA-256 values after canonicalizing `CRLF` and lone `CR` to `LF`; legacy raw LF/CRLF digests remain reader-compatible. Run the read-only `scripts/check-feature-context.py` before relying on the Snapshot and read its prefix: `CURRENT` reports matching applicable facts, `CHANGED` requires Agent impact assessment/repair/route, `NOT_APPLICABLE` from a specialized Checker selects another adapter/direct evidence, and `BLOCKED` means safe authority resolution failed. Exit `0` alone is not execution permission. `## Product Slice` remains conditional Requirement Product Definition responsibility and coverage.

## Product Slice

| Source Section / Model ID | Feature Responsibility | Acceptance Mapping | Coverage |
|---|---|---|---|
| FLOW-... / STATE-... / product.md#... |  |  | in-scope / out-of-scope / not-applicable |

Use Product Slice only when the Requirement Product Definition sub-adapter applies. It selects this Feature's responsibility and acceptance mapping and must not redefine the Requirement Product Definition. Return to Requirements Discussion when product meaning must change. Bug/Human/custom Feature authorities use their accepted Feature boundary and acceptance evidence without fabricating Product model IDs.

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
