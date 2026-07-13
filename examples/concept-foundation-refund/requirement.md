# Requirement: Refund Completion

Status: accepted
Created: 2026-07-12
Source: conversation + payment callback evidence

## Background

Customers request refunds; administrators review them; a later payment callback confirms whether funds actually returned.

## Problem

The word “refund” previously mixed the review request with the settlement result, so “completed” had two incompatible terminals.

## Users / Operators

- Customer
- Refund administrator
- Payment provider

## Goals

- Make review completion and funds-settlement completion independently observable.
- Notify the customer only from the accepted settlement terminal.

## Concept Foundation

Concept Foundation Status: accepted
Not-Needed Reason: n/a because identity, lifecycle, actor, and terminal meaning change the downstream model

### Evidence And Scenarios

- Success scenario: customer submits, administrator approves, provider later confirms settlement.
- Failure scenario: administrator approves, but provider callback reports failure or remains unknown.
- Evidence: payment callback test owns the final funds result; historical product notes separate request and settlement.

## Concept Candidate Inventory

| Concept ID | Candidate Name | Kind | Evidence / Example | Ambiguity / Conflict | Status |
|---|---|---|---|---|---|
| C-CUSTOMER | Customer | role | source scenario | none | accepted |
| C-REFUND-ADMIN | Refund Administrator | role | review flow | “admin” must stay refund-scoped | accepted |
| C-PAYMENT-PROVIDER | Payment Provider | external actor | callback contract | provider does not own request review | accepted |
| C-REFUND-REQUEST | Refund Request | entity | submit/review records | previously called “refund” | accepted |
| C-REFUND-SETTLEMENT | Refund Settlement | entity/result | callback and reconciliation | previously called “refund completed” | accepted |

## Concept Definitions

| Concept ID | Canonical Name | Definition / Non-example | Identity | Owner | Lifecycle Boundary / State-bearing | Invariants | Product Fact Owner | Evidence |
|---|---|---|---|---|---|---|---|---|
| C-CUSTOMER | Customer | requester receiving the product outcome; not the payment provider | customer ID | customer account | n/a: role concept | may act only on own request | customer account | source scenario |
| C-REFUND-ADMIN | Refund Administrator | operator reviewing a request; not the settlement actor | operator ID + refund permission | refund operations | n/a: role concept | cannot mark funds settled | refund operations | permission rule |
| C-PAYMENT-PROVIDER | Payment Provider | external actor reporting funds result | provider account | payment boundary | n/a: actor concept | callback result cannot approve request | provider callback | callback contract |
| C-REFUND-REQUEST | Refund Request | reviewable customer request; not proof that funds arrived | request ID | refund operations | submitted to rejected/cancelled/approved | one review terminal per request | refund operations | request model/test |
| C-REFUND-SETTLEMENT | Refund Settlement | actual refund funds attempt/result; not administrator approval | provider reference per request | payment boundary | pending to succeeded/failed/unknown/manual-review | succeeded only from verified provider/reconciliation evidence | payment result | callback/reconcile tests |

## Concept Relationships

| Relationship ID | From Concept ID | Relationship | To Concept ID | Cardinality / Boundary | Invariant | Evidence |
|---|---|---|---|---|---|---|
| REL-01 | C-CUSTOMER | submits | C-REFUND-REQUEST | one customer to many requests | customer owns request visibility | source scenario |
| REL-02 | C-REFUND-REQUEST | authorizes creation of | C-REFUND-SETTLEMENT | one approved request to one active settlement | rejected/cancelled requests have no settlement | review/callback tests |
| REL-03 | C-PAYMENT-PROVIDER | reports result for | C-REFUND-SETTLEMENT | one provider result stream per settlement | duplicate callbacks preserve one terminal | callback contract |

### Blocking Ambiguities

| Blocking Question | Recommended Definition | Evidence | Accept Impact | Reject Impact | Status |
|---|---|---|---|---|---|
| Does “refund completed” mean review approval or funds settlement? | funds settlement succeeded | callback owns actual funds result | notification and recovery use observable terminal | post-success failure remains possible | resolved |

### Human Confirmation

- Confirmed Concept IDs: C-CUSTOMER, C-REFUND-ADMIN, C-PAYMENT-PROVIDER, C-REFUND-REQUEST, C-REFUND-SETTLEMENT
- Human decision: request approval and settlement success are separate product terminals
- Confirmed at: 2026-07-12
- Remaining non-blocking unknowns: provider-specific settlement latency

## Requirements

- A customer can submit one refund request for an eligible purchase.
- Administrator approval creates the settlement attempt but does not notify success.
- Settlement success, failure, unknown, and manual-review outcomes remain observable.

## Terminology / Domain Language

| Concept ID | Canonical Term | Allowed Alias / Display Wording | Avoid / Ambiguity | Promote To Project Domain Language |
|---|---|---|---|---|
| C-REFUND-REQUEST | Refund Request | refund application | “refund completed” | pending |
| C-REFUND-SETTLEMENT | Refund Settlement | funds returned | “approved means paid” | pending |

## Role / Permission Matrix

| Role Concept ID | Product Object Concept ID | Read | Create | Advance / Decide | Cancel / Withdraw | Recover | Boundary / Evidence |
|---|---|---|---|---|---|---|---|
| C-CUSTOMER | C-REFUND-REQUEST | own | yes | no | before approval | no | source scenario |
| C-REFUND-ADMIN | C-REFUND-REQUEST | permitted scope | no | approve/reject | no | manual review | permission rule |
| C-REFUND-ADMIN | C-REFUND-SETTLEMENT | permitted scope | no | reconcile unknown/failed | no | retry/reconcile/manual review | reconciliation responsibility |
| C-PAYMENT-PROVIDER | C-REFUND-SETTLEMENT | callback reference | result only | report result | no | no | callback contract |

## Commands / Events

| Action ID | Type | Name | Actor / Producer Concept ID | Target Concept ID | Preconditions / Guard | Result / Event | Evidence |
|---|---|---|---|---|---|---|---|
| CMD-SUBMIT | command | Submit Refund Request | C-CUSTOMER | C-REFUND-REQUEST | eligible purchase and no active request | request submitted | request test |
| CMD-APPROVE | command | Approve Refund Request | C-REFUND-ADMIN | C-REFUND-REQUEST | submitted request | settlement pending | review test |
| EVT-SETTLED | event | Settlement Succeeded | C-PAYMENT-PROVIDER | C-REFUND-SETTLEMENT | matching provider reference | customer success notification | callback test |
| EVT-FAILED | event | Settlement Failed | C-PAYMENT-PROVIDER | C-REFUND-SETTLEMENT | matching provider reference | failure visible for recovery | callback test |
| CMD-RECONCILE | command | Reconcile Unknown Settlement | C-REFUND-ADMIN | C-REFUND-SETTLEMENT | unknown or timed out | terminal or manual-review result | reconciliation test |

## Primary Business Flow

| Flow Step ID | Actor Concept ID | Action ID | Input / Target Concept IDs | Product State Change | Result / Next Step |
|---|---|---|---|---|---|
| FLOW-01 | C-CUSTOMER | CMD-SUBMIT | C-REFUND-REQUEST | none to submitted | await review |
| FLOW-02 | C-REFUND-ADMIN | CMD-APPROVE | C-REFUND-REQUEST, C-REFUND-SETTLEMENT | request approved; settlement pending | await provider |
| FLOW-03 | C-PAYMENT-PROVIDER | EVT-SETTLED | C-REFUND-SETTLEMENT | pending to succeeded | notify customer success |
| FLOW-04 | C-REFUND-ADMIN | CMD-RECONCILE | C-REFUND-SETTLEMENT | unknown to terminal/manual-review | close observable outcome |

## Product State Model

| State Model ID | State-bearing Concept ID | From | Action / Event ID | Guard / Invariant | To | Terminal / Recovery | Forbidden Transition |
|---|---|---|---|---|---|---|---|
| STATE-REQUEST-01 | C-REFUND-REQUEST | none | CMD-SUBMIT | eligible purchase | submitted | no | none to approved |
| STATE-REQUEST-02 | C-REFUND-REQUEST | submitted | CMD-APPROVE | refund administrator | approved | request terminal | approved to submitted |
| STATE-SETTLEMENT-01 | C-REFUND-SETTLEMENT | none | CMD-APPROVE | request approved | pending | no | none to succeeded |
| STATE-SETTLEMENT-02 | C-REFUND-SETTLEMENT | pending | EVT-SETTLED | provider result verified | succeeded | success terminal | succeeded to failed |
| STATE-SETTLEMENT-03 | C-REFUND-SETTLEMENT | pending | EVT-FAILED | provider result verified | failed | recovery allowed | failed to succeeded without reconcile |
| STATE-SETTLEMENT-04 | C-REFUND-SETTLEMENT | unknown | CMD-RECONCILE | evidence checked | manual-review | manual terminal | manual-review to pending |

## Requirement Product Model

| Product Model ID | Product Object / Fact | Concept IDs | Identity / Relationship | Owner / Allowed Changer | Product Invariant | Product Fact Meaning |
|---|---|---|---|---|---|---|
| PM-01 | refund request fact | C-REFUND-REQUEST, C-CUSTOMER, C-REFUND-ADMIN | request ID; submitted by customer; reviewed by admin | refund operations | approval is not proof of funds | customer intent and review terminal |
| PM-02 | settlement result fact | C-REFUND-SETTLEMENT, C-PAYMENT-PROVIDER | provider reference linked by REL-02 | provider result/reconciliation | one active settlement; succeeded is immutable | observed funds outcome |

## Exception Paths

| Scenario ID | Concept / State / Action IDs | Trigger | Expected Handling | Recovery / Responsible Actor | Observable Result | Acceptance Direction |
|---|---|---|---|---|---|---|
| EX-01 | C-REFUND-SETTLEMENT / EVT-FAILED | provider failure | keep request approved and settlement failed | retry/reconcile by C-REFUND-ADMIN | failure visible | no success notification |
| EX-02 | C-REFUND-SETTLEMENT / CMD-RECONCILE | missing callback | mark unknown then investigate | C-REFUND-ADMIN | terminal or manual-review | no false completion |

## Data / Source of Truth

| Product Model ID | Product Fact | Product Fact Owner | Who Can Change It | Timing / Consistency Need | Decision Candidate |
|---|---|---|---|---|---|
| PM-01 | request/review terminal | C-REFUND-REQUEST | C-REFUND-ADMIN | synchronous review | none |
| PM-02 | actual funds outcome | C-REFUND-SETTLEMENT | C-PAYMENT-PROVIDER or reconciliation | asynchronous | technical storage mapping deferred |

## Concept-To-Product Traceability

| Trace ID | Accepted Concept IDs | Derived Model IDs / Sections | Product Rule / Meaning | Downstream Product Brief / Feature Spec Use |
|---|---|---|---|---|
| TRACE-01 | C-CUSTOMER, C-REFUND-REQUEST | REL-01 / CMD-SUBMIT / FLOW-01 / STATE-REQUEST-01 / PM-01 | customer owns request submission | refund journey and US1 |
| TRACE-02 | C-REFUND-ADMIN, C-REFUND-REQUEST, C-REFUND-SETTLEMENT | REL-02 / CMD-APPROVE / FLOW-02 / STATE-REQUEST-02 / STATE-SETTLEMENT-01 / PM-01 / PM-02 | approval creates settlement but is not funds success | admin journey and US2 |
| TRACE-03 | C-PAYMENT-PROVIDER, C-REFUND-SETTLEMENT | REL-03 / EVT-SETTLED / EVT-FAILED / CMD-RECONCILE / FLOW-03 / FLOW-04 / STATE-SETTLEMENT-02 / STATE-SETTLEMENT-03 / STATE-SETTLEMENT-04 / PM-02 | notification follows observed settlement terminal | callback behavior and US3 |

## Historical Behavior / Prior Conflicts

| Prior Source | Existing Rule / Behavior | Current Requirement Says | Human Decision |
|---|---|---|---|
| prior refund notes | “approved” was sometimes called completed | distinguish review and settlement | override ambiguous wording |

## Acceptance Scenarios

| Scenario | Given | When | Then | Notes |
|---|---|---|---|---|
| settlement success | approved request with pending settlement | verified success callback arrives | settlement succeeds and customer is notified | approval alone does not notify |
| settlement unknown | approved request with no callback | reconciliation runs | terminal or manual-review result is visible | no false completion |

## Decision Candidates

| Candidate | Why It Matters | Signal | Suggested Destination | Status |
|---|---|---|---|---|
| technical settlement storage/consistency | later implementation must preserve PM-02 | shared-design | Decision & Design | proposed |

## Non-goals

- No technical table, topic, provider adapter, or migration mapping.

## Out Of Scope And Why

| Out Of Scope | Why | Revisit Trigger |
|---|---|---|
| provider-specific retries | implementation design | Decision & Design |

## Constraints / Assumptions

- Provider callbacks can be delayed or duplicated.

## Acceptance Direction

- Product artifacts and features preserve TRACE-01 through TRACE-03.

## Open Questions

- Provider latency target is non-blocking for this product model.

## Product / Feature Mapping

| Downstream Artifact | Mapping Direction | Status |
|---|---|---|
| product.md | TRACE-01..03 | created |
| spec.md | PM-01 / PM-02 and state/action IDs | created |
| Design Readiness | storage/consistency candidate | candidate |

## Source Conversation Summary

- Human confirmed that “refund completed” means observed settlement success.
