# Feature Spec: Account Recharge Slice

Status: accepted
Feature Type: normal

## Product Requirement Source

Requirement Set: .agent-loop/requirements/2026-07-25-example/README.md
Effective Product Definition: .agent-loop/requirements/2026-07-25-example/product.md
Product Definition Profile: standard
Product Review Evidence: confirmed by human maintainer on 2026-07-25
Applicable Decisions: .agent-loop/decisions/0001-example.md

## Feature Context Snapshot

Requirement Set: .agent-loop/requirements/2026-07-25-example/README.md
Requirement Lifecycle: accepted
Resolved Product Source: .agent-loop/requirements/2026-07-25-example/product.md
Product Definition Profile: standard
Product Review: confirmed
Product Source SHA-256: 1e7bc739b3a32ec08481aab64fa4f39dd854896f885cd4fb222b4cef6b3dd3fd
Applicable Decisions: .agent-loop/decisions/0001-example.md
Decision Source SHA-256: .agent-loop/decisions/0001-example.md=ef854d72b13067cf932fe2bdb68861ed6c4eb7a10ab02cff9c4efebf0730bf51
Product Slice References: C-ACCOUNT / FLOW-RECHARGE / STATE-RECHARGE / EX-PAYMENT-UNKNOWN / product.md#confirmed-credit
Verified At: 2026-07-25T12:00:00+08:00
Freshness: current

### Product Outcome

An authorized operator can complete one observable recharge without duplicate credit.

### Actors And Core Journey

The operator starts a recharge, observes pending/unknown/success/failure, and receives one confirmed credit.

### Applicable Product Rules And Invariants

`product.md#confirmed-credit` permits credit only after confirmed success.

### Applicable States, Exceptions, And Recovery

`STATE-RECHARGE` and `EX-PAYMENT-UNKNOWN` keep unknown visible and recoverable.

### Feature Boundary And Acceptance Context

This Feature implements the accepted recharge slice and excludes provider migration.

## Product Slice

| Source Section / Model ID | Feature Responsibility | Acceptance Mapping | Coverage |
|---|---|---|---|
| C-ACCOUNT / FLOW-RECHARGE | initiate and observe recharge | operator completes the journey | in-scope |
| STATE-RECHARGE / EX-PAYMENT-UNKNOWN | preserve visible unknown recovery | unknown remains queryable | in-scope |
| PM-CREDIT / product.md#confirmed-credit | credit exactly once after confirmation | one confirmed credit | in-scope |

## Problem / Goal

Implement the accepted recharge Product Slice without redefining source semantics.
