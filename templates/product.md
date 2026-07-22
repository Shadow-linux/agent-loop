# Product Requirement: <Requirement Name>

Requirement ID: <REQ-ID>
Product Definition Profile: brief | standard
Product Review: pending | confirmed

Template rule: keep all Brief sections. For `standard`, add only evidence-backed adaptive sections and complete Product View Applicability. Remove non-applicable section bodies instead of creating placeholder rows.

## Problem / Background

## Target User / Scenario

## Goal / Expected Product Outcome

## In Scope

-

## Out Of Scope / Non-goals

-

## Acceptance Direction

-

## Source Evidence

| Source | Type | Product Claim Used | Preserved / Referenced |
|---|---|---|---|

Human original source materials remain byte-stable. Record references or copied-source paths; do not paste over or edit the original.

## Open Questions / Remaining Risk

-

## Product Capability Scope

Standard-only when needed. A capability is product scope, not an Agent Loop Feature workspace.

## User Segments / Roles / Scenarios

Standard-only when needed.

## Concept Definitions

Standard-only when Concepts are `included`.

| Concept ID | Canonical Name | Definition / Non-example | Identity | Owner | Evidence |
|---|---|---|---|---|---|

## Concept Relationships

Standard-only when Relationships are `included`.

| Relationship ID | From Concept ID | Relationship | To Concept ID | Invariant | Evidence |
|---|---|---|---|---|---|

## Role / Permission Matrix

Standard-only when Permissions are `included`.

| Permission Rule ID | Role Concept ID | Product Object Concept ID | Advance / Decide | Boundary / Evidence |
|---|---|---|---|---|

## Commands / Events

Standard-only when Actions / Outcomes are `included`.

| Action ID | Type | Name | Actor / Producer Concept ID | Target Concept ID | Result / Event | Evidence |
|---|---|---|---|---|---|---|

## Primary Business Flow

Standard-only when Flow is `included`.

| Flow Step ID | Actor Concept ID | Action ID | Input / Target Concept IDs | Product State Change | Result / Next Step |
|---|---|---|---|---|---|

## Product State Model

Standard-only when State is `included`.

| State Model ID | State-bearing Concept ID | From | Action / Event ID | Guard / Invariant | To | Terminal / Recovery |
|---|---|---|---|---|---|---|

## Requirement Product Model

Standard-only when Product Facts are `included`. This is product meaning, not a technical table/store/schema.

| Product Model ID | Product Object / Fact | Concept IDs | Owner / Allowed Changer | Product Invariant | Product Fact Meaning |
|---|---|---|---|---|---|

## Exception Paths

Standard-only when Exceptions / Recovery are `included`.

| Scenario ID | Concept / State / Action IDs | Trigger | Expected Handling | Recovery / Responsible Actor | Observable Result |
|---|---|---|---|---|---|

## Product Rules

Standard-only when Product Rules are `included`. Use descriptive `###` headings and reference them as `product.md#<rule-anchor>`; do not invent `RULE-*` IDs.

### <Rule Name>

<Accepted product rule and evidence.>

## Product View Applicability

Required for `standard`; absent for `brief`.

| View | Applicability | Reason / Evidence | Section / Stable IDs |
|---|---|---|---|
| Concepts | included / not-applicable |  | Concept Definitions / IDs, or none |
| Relationships | included / not-applicable |  | Concept Relationships / IDs, or none |
| Permissions | included / not-applicable |  | Role / Permission Matrix / IDs, or none |
| Actions / Outcomes | included / not-applicable |  | Commands / Events / IDs, or none |
| Flow | included / not-applicable |  | Primary Business Flow / IDs, or none |
| State | included / not-applicable |  | Product State Model / IDs, or none |
| Product Facts | included / not-applicable |  | Requirement Product Model / IDs, or none |
| Exceptions / Recovery | included / not-applicable |  | Exception Paths / IDs, or none |
| Product Rules | included / not-applicable |  | Product Rules / product.md#anchor, or none |

## Experience / Operations / Measurement

Standard-only adaptive details: feedback, empty/error states, notification, manual handling, operations, and success measurement when applicable.

## Delivery Phases

Use only after human review; Requirement README owns phase lifecycle and Feature Mapping.

| Phase | Goal | Scope | Out Of Scope | Acceptance Direction | Status |
|---|---|---|---|---|---|

## Derived Visuals

Optional and only after Archify Scoped Confirmation.

| Path | Type | Source IDs | Product Semantic SHA-256 | Status | Human Confirmed |
|---|---|---|---|---|---|

## Decision Candidates

| Candidate | Why It Matters | Suggested Destination | Status |
|---|---|---|---|

## Applicable Decisions

- none | `.agent-loop/decisions/000N-<slug>.md`

## Product Traceability

| Product Claim | Source Evidence | Stable References | Downstream Direction |
|---|---|---|---|

## Product Human Review Evidence

Decision: pending | confirmed
Confirmed By:
Confirmed At: YYYY-MM-DD
Evidence:
Implementation Authorized: no | separately-confirmed

Product Review confirmation does not authorize Requirement acceptance, Feature start, ADR acceptance, code execution, or Git actions.
