# Product Requirement: Approval Request With Stale Visual

Requirement ID: REQ-STANDARD-STALE
Product Definition Profile: standard
Product Review: confirmed

## Problem / Background

The approval workflow needs a reviewed visual derived from one accepted flow.

## Target User / Scenario

An operator reviews a pending request.

## Goal / Expected Product Outcome

The reviewed flow stays traceable to the accepted product source.

## In Scope

- Approval flow review.

## Out Of Scope / Non-goals

- Technical landing.

## Acceptance Direction

- The flow and its visual use the same accepted source meaning.

## Source Evidence

| Source | Type | Product Claim Used | Preserved / Referenced |
|---|---|---|---|
| reviewed conversation | conversation | approval flow | referenced without rewriting |

## Open Questions / Remaining Risk

- none after product review.

## Primary Business Flow

| Flow Step ID | Actor Concept ID | Action ID | Input / Target Concept IDs | Product State Change | Result / Next Step |
|---|---|---|---|---|---|
| FLOW-APPROVE | C-OPERATOR | CMD-APPROVE | C-REQUEST | pending to approved | publish result |

## Product View Applicability

| View | Applicability | Reason / Evidence | Section / Stable IDs |
|---|---|---|---|
| Concepts | not-applicable | existing domain terms already own all involved concepts | none |
| Relationships | not-applicable | no new relationship meaning is introduced by this review | none |
| Permissions | not-applicable | existing authorization rule remains unchanged by this review | none |
| Actions / Outcomes | not-applicable | existing action semantics remain unchanged by this review | none |
| Flow | included | one reviewed approval flow is the product scope | Primary Business Flow / FLOW-APPROVE |
| State | not-applicable | the existing state model remains unchanged by this review | none |
| Product Facts | not-applicable | no new durable fact or fact ownership is introduced | none |
| Exceptions / Recovery | not-applicable | existing failure handling remains unchanged by this review | none |
| Product Rules | not-applicable | no new product rule is introduced by this visual review | none |

## Derived Visuals

| Path | Type | Source IDs | Product Semantic SHA-256 | Status | Human Confirmed |
|---|---|---|---|---|---|
| visuals/approval-workflow.html | workflow | FLOW-APPROVE | 0000000000000000000000000000000000000000000000000000000000000000 | current | human confirmed this workflow output on 2026-07-22 |

## Product Human Review Evidence

Decision: confirmed
Confirmed By: human maintainer
Confirmed At: 2026-07-22
Evidence: human confirmed the product flow before the later semantic change made the visual stale
Implementation Authorized: no
