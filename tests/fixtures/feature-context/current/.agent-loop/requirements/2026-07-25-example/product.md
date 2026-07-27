# Product Requirement: Account Recharge

Requirement ID: REQ-2026-07-25-EXAMPLE
Product Definition Profile: standard
Product Review: confirmed

## Problem / Background

An authorized operator needs a recharge result that never creates duplicate credit.

## Target User / Scenario

An operator starts a recharge and observes a recoverable result.

## Goal / Expected Product Outcome

One confirmed payment produces one observable account credit.

## In Scope

- Recharge initiation, payment result visibility, confirmed credit, and unknown recovery.

## Out Of Scope / Non-goals

- Provider migration and technical persistence design.

## Acceptance Direction

- Only confirmed success produces credit, and unknown remains recoverable.

## Source Evidence

| Source | Type | Product Claim Used | Preserved / Referenced |
|---|---|---|---|
| reviewed conversation on 2026-07-25 | conversation | actor, flow, state, credit rule, recovery | referenced without rewriting |

## Open Questions / Remaining Risk

- Provider-specific timeout wording remains outside this definition.

## Product Capability Scope

- Start a recharge.
- Observe the payment result.
- Credit exactly once after confirmed success.

## Concept Definitions

| Concept ID | Canonical Name | Definition / Non-example | Identity | Owner | Evidence |
|---|---|---|---|---|---|
| C-ACCOUNT | Account | credited product account; not the payment result | account ID | account boundary | reviewed conversation |
| C-OPERATOR | Operator | authorized recharge initiator; not every signed-in user | operator ID | operations boundary | reviewed conversation |

## Concept Relationships

| Relationship ID | From Concept ID | Relationship | To Concept ID | Invariant | Evidence |
|---|---|---|---|---|---|
| REL-OPERATOR-ACCOUNT | C-OPERATOR | recharges | C-ACCOUNT | confirmed payment credits one account once | reviewed conversation |

## Role / Permission Matrix

| Permission Rule ID | Role Concept ID | Product Object Concept ID | Advance / Decide | Boundary / Evidence |
|---|---|---|---|---|
| PERM-RECHARGE | C-OPERATOR | C-ACCOUNT | start an eligible recharge | explicit human rule |

## Commands / Events

| Action ID | Type | Name | Actor / Producer Concept ID | Target Concept ID | Result / Event | Evidence |
|---|---|---|---|---|---|---|
| CMD-RECHARGE | command | Start Recharge | C-OPERATOR | C-ACCOUNT | recharge becomes pending | reviewed scenario |
| EVT-CONFIRMED | event | Payment Confirmed | C-OPERATOR | C-ACCOUNT | credit becomes eligible | acceptance direction |

## Primary Business Flow

| Flow Step ID | Actor Concept ID | Action ID | Input / Target Concept IDs | Product State Change | Result / Next Step |
|---|---|---|---|---|---|
| FLOW-RECHARGE | C-OPERATOR | CMD-RECHARGE | C-ACCOUNT | new to pending | await payment result |

## Product State Model

| State Model ID | State-bearing Concept ID | From | Action / Event ID | Guard / Invariant | To | Terminal / Recovery |
|---|---|---|---|---|---|---|
| STATE-RECHARGE | C-ACCOUNT | pending | EVT-CONFIRMED | confirmed result exists | credited | credited is terminal |

## Requirement Product Model

| Product Model ID | Product Object / Fact | Concept IDs | Owner / Allowed Changer | Product Invariant | Product Fact Meaning |
|---|---|---|---|---|---|
| PM-CREDIT | account credit | C-ACCOUNT, C-OPERATOR | account boundary | one confirmed result creates one credit | observable credited balance |

## Exception Paths

| Scenario ID | Concept / State / Action IDs | Trigger | Expected Handling | Recovery / Responsible Actor | Observable Result |
|---|---|---|---|---|---|
| EX-PAYMENT-UNKNOWN | C-ACCOUNT / STATE-RECHARGE / CMD-RECHARGE | payment result is unknown | preserve unknown without credit | operator can query the original recharge | unknown remains visible |

## Product Rules

### Confirmed Credit

Only a confirmed success may credit C-ACCOUNT, and one confirmed result may credit it only once.

## Product View Applicability

| View | Applicability | Reason / Evidence | Section / Stable IDs |
|---|---|---|---|
| Concepts | included | account and operator need stable meanings | Concept Definitions / C-ACCOUNT / C-OPERATOR |
| Relationships | included | operator acts on one account | Concept Relationships / REL-OPERATOR-ACCOUNT |
| Permissions | included | only an authorized operator may start recharge | Role / Permission Matrix / PERM-RECHARGE |
| Actions / Outcomes | included | recharge and confirmation are observable actions | Commands / Events / CMD-RECHARGE / EVT-CONFIRMED |
| Flow | included | recharge has one visible core journey | Primary Business Flow / FLOW-RECHARGE |
| State | included | recharge has pending and credited states | Product State Model / STATE-RECHARGE |
| Product Facts | included | credited balance is a durable fact | Requirement Product Model / PM-CREDIT |
| Exceptions / Recovery | included | unknown payment needs recovery | Exception Paths / EX-PAYMENT-UNKNOWN |
| Product Rules | included | confirmed success is required for credit | Product Rules / product.md#confirmed-credit |

## Product Traceability

| Product Claim | Source Evidence | Stable References | Downstream Direction |
|---|---|---|---|
| confirmed payment credits once | reviewed conversation | FLOW-RECHARGE / STATE-RECHARGE / product.md#confirmed-credit | ADR and Feature Product Slice |

## Decision Candidates

| Candidate | Why It Matters | Suggested Destination | Status |
|---|---|---|---|
| credit idempotency | technical landing must preserve PM-CREDIT | Decision & Design | proposed |

## Product Human Review Evidence

Decision: confirmed
Confirmed By: human maintainer
Confirmed At: 2026-07-25
Evidence: human confirmed the operator, flow, unknown recovery, and one-credit rule
Implementation Authorized: separately-confirmed
