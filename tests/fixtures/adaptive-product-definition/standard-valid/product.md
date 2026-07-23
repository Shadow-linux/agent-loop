# Product Requirement: Approval Request

Requirement ID: REQ-STANDARD-001
Product Definition Profile: standard
Product Review: confirmed

## Problem / Background

People need one reviewed request flow whose approval result remains distinguishable from submission.

## Target User / Scenario

A requester submits a request and an authorized operator reviews it.

## Goal / Expected Product Outcome

Make submission and approval observable without allowing an unauthorized actor to approve.

## In Scope

- Request submission, authorized approval, observable result, and rejected-review recovery.

## Out Of Scope / Non-goals

- Technical storage, API, queue, migration, and deployment design.

## Acceptance Direction

- A requester can submit; only an authorized operator can approve; rejection stays observable.

## Source Evidence

| Source | Type | Product Claim Used | Preserved / Referenced |
|---|---|---|---|
| reviewed conversation on 2026-07-22 | conversation | actors, approval rule, states, and rejection behavior | referenced without rewriting |

## Open Questions / Remaining Risk

- Notification wording is non-blocking and remains outside this product definition.

## Product Capability Scope

- Submit one request.
- Approve an eligible pending request.
- Observe an approved or rejected review result.

## Concept Definitions

| Concept ID | Canonical Name | Definition / Non-example | Identity | Owner | Evidence |
|---|---|---|---|---|---|
| C-REQUEST | Request | a reviewable product object; not the approval result | request ID | requester context | reviewed conversation |
| C-OPERATOR | Operator | an authorized reviewer; not every signed-in user | operator ID | operations boundary | reviewed conversation |

## Concept Relationships

| Relationship ID | From Concept ID | Relationship | To Concept ID | Invariant | Evidence |
|---|---|---|---|---|---|
| REL-OPERATOR-REQUEST | C-OPERATOR | reviews | C-REQUEST | one accepted result is recorded per request | reviewed conversation |

## Role / Permission Matrix

| Permission Rule ID | Role Concept ID | Product Object Concept ID | Advance / Decide | Boundary / Evidence |
|---|---|---|---|---|
| PERM-APPROVE | C-OPERATOR | C-REQUEST | approve eligible pending request | explicit human rule |

## Commands / Events

| Action ID | Type | Name | Actor / Producer Concept ID | Target Concept ID | Result / Event | Evidence |
|---|---|---|---|---|---|---|
| CMD-SUBMIT | command | Submit Request | C-REQUEST | C-REQUEST | request becomes pending | reviewed scenario |
| CMD-APPROVE | command | Approve Request | C-OPERATOR | C-REQUEST | approval is recorded | explicit human rule |
| EVT-APPROVED | event | Request Approved | C-OPERATOR | C-REQUEST | approved result is observable | acceptance direction |

## Primary Business Flow

| Flow Step ID | Actor Concept ID | Action ID | Input / Target Concept IDs | Product State Change | Result / Next Step |
|---|---|---|---|---|---|
| FLOW-SUBMIT | C-REQUEST | CMD-SUBMIT | C-REQUEST | new to pending | await review |
| FLOW-APPROVE | C-OPERATOR | CMD-APPROVE | C-REQUEST | pending to approved | publish approval result |

## Product State Model

| State Model ID | State-bearing Concept ID | From | Action / Event ID | Guard / Invariant | To | Terminal / Recovery |
|---|---|---|---|---|---|---|
| STATE-REQUEST | C-REQUEST | pending | CMD-APPROVE | PERM-APPROVE holds | approved | approved is terminal for this review |

## Requirement Product Model

| Product Model ID | Product Object / Fact | Concept IDs | Owner / Allowed Changer | Product Invariant | Product Fact Meaning |
|---|---|---|---|---|---|
| PM-APPROVAL | approval result | C-REQUEST, C-OPERATOR | authorized operator | submission alone is not approval | reviewed product result |

## Exception Paths

| Scenario ID | Concept / State / Action IDs | Trigger | Expected Handling | Recovery / Responsible Actor | Observable Result |
|---|---|---|---|---|---|
| EX-REJECTED | C-REQUEST / STATE-REQUEST / CMD-APPROVE | request is ineligible at review | reject without approval | requester may submit a corrected new request | rejection remains observable |

## Product Rules

### Approval Authority

Only an actor satisfying PERM-APPROVE may apply CMD-APPROVE to C-REQUEST; submission never implies approval.

## Product View Applicability

| View | Applicability | Reason / Evidence | Section / Stable IDs |
|---|---|---|---|
| Concepts | included | two actors and one state-bearing request need stable meaning | Concept Definitions / C-REQUEST / C-OPERATOR |
| Relationships | included | operator acts on one request | Concept Relationships / REL-OPERATOR-REQUEST |
| Permissions | included | only operator may approve | Role / Permission Matrix / PERM-APPROVE |
| Actions / Outcomes | included | submit and approve are observable product actions | Commands / Events / CMD-SUBMIT / CMD-APPROVE / EVT-APPROVED |
| Flow | included | request closes through submit and approve | Primary Business Flow / FLOW-SUBMIT / FLOW-APPROVE |
| State | included | request has pending and approved states | Product State Model / STATE-REQUEST |
| Product Facts | included | approval result and owner are durable facts | Requirement Product Model / PM-APPROVAL |
| Exceptions / Recovery | included | rejected approval remains observable | Exception Paths / EX-REJECTED |
| Product Rules | included | approval requires an authorized operator | Product Rules / product.md#approval-authority |

## Product Traceability

| Product Claim | Source Evidence | Stable References | Downstream Direction |
|---|---|---|---|
| approval requires an authorized operator | reviewed conversation | PERM-APPROVE / CMD-APPROVE / STATE-REQUEST / product.md#approval-authority | ADR and Feature Product Slice |

## Decision Candidates

| Candidate | Why It Matters | Suggested Destination | Status |
|---|---|---|---|
| approval persistence and consistency | technical landing must preserve PM-APPROVAL | Decision & Design | proposed |

## Product Human Review Evidence

Decision: confirmed
Confirmed By: human maintainer
Confirmed At: 2026-07-22
Evidence: human confirmed the request identity, operator authority, approval terminal, and rejection behavior
Implementation Authorized: separately-confirmed
