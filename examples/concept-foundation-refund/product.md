# Product Brief: Refund Completion

Created: 2026-07-12
Updated: 2026-07-12
Status: draft

Source Requirements:
- Requirement: requirement.md

Summary:
- Separate request approval from actual funds settlement in customer-visible behavior.

## Applicable Decisions

- none; technical settlement design remains a candidate

## Accepted Concept References

Concept Foundation Status: accepted
Source Requirement: requirement.md
Effective Concept Source: requirement.md
Not-Needed Reason: n/a

| Concept ID | Canonical Name | Product Brief Use | Source Definition / Trace |
|---|---|---|---|
| C-CUSTOMER | Customer | submits and receives outcome | requirement.md#concept-definitions / TRACE-01 |
| C-REFUND-ADMIN | Refund Administrator | reviews and recovers | requirement.md#concept-definitions / TRACE-02 |
| C-PAYMENT-PROVIDER | Payment Provider | reports funds outcome | requirement.md#concept-definitions / TRACE-03 |
| C-REFUND-REQUEST | Refund Request | request/review journey | requirement.md#concept-definitions / TRACE-01 / TRACE-02 |
| C-REFUND-SETTLEMENT | Refund Settlement | terminal customer outcome | requirement.md#concept-definitions / TRACE-02 / TRACE-03 |

## Requirement Product Model Coverage

| Requirement Model ID | Concept IDs | Feature Product Journey / Story | Coverage | Notes |
|---|---|---|---|---|
| PM-01 / FLOW-01 / FLOW-02 / STATE-REQUEST-01 / STATE-REQUEST-02 | C-CUSTOMER, C-REFUND-ADMIN, C-REFUND-REQUEST | submit and review | in-scope | approval is not funds success |
| PM-02 / FLOW-03 / FLOW-04 / STATE-SETTLEMENT-01 / STATE-SETTLEMENT-02 / STATE-SETTLEMENT-03 / STATE-SETTLEMENT-04 | C-PAYMENT-PROVIDER, C-REFUND-SETTLEMENT | observe and recover settlement | in-scope | success notification uses settlement terminal |

## Problem Statement

Customers currently cannot distinguish “approved” from “funds returned.”

## Target Users / Actors

- C-CUSTOMER
- C-REFUND-ADMIN
- C-PAYMENT-PROVIDER

## Solution Summary

Show request review and settlement outcome as separate accepted product facts.

## Primary User Journey

1. Customer submits C-REFUND-REQUEST.
2. Refund Administrator approves it and starts C-REFUND-SETTLEMENT.
3. Customer sees success only after settlement succeeds.

## User Stories

### US1: Customer submits a request

As a customer, I want to submit an eligible request, so that refund review can begin.

Acceptance Direction: FLOW-01 and STATE-REQUEST-01 remain traceable.

### US2: Administrator reviews without claiming funds success

As a refund administrator, I want approval to start settlement, so that review and funds outcomes remain distinct.

Acceptance Direction: FLOW-02 and STATE-SETTLEMENT-01 remain traceable.

### US3: Customer receives an observable settlement outcome

As a customer, I want success/failure/manual outcomes, so that no approval is misreported as funds returned.

Acceptance Direction: FLOW-03 / FLOW-04 and settlement states remain traceable.

## Product Scope

- Request submission and review status.
- Settlement success/failure/unknown/manual outcome.

## Out Of Scope

- Technical storage and provider adapter choices.

## Terminology

- `funds returned`:
  - Accepted Concept ID: C-REFUND-SETTLEMENT
  - Feature display wording / alias: Refund completed
  - Promote to project Domain Language: pending

## Open Product Questions

- Question: provider latency target
  - Recommended answer: route to later technical design
  - Blocks: none
