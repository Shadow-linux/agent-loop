# Feature Spec: Refund Completion

Created: 2026-07-12
Updated: 2026-07-12
Status: draft
Feature Type: normal

Source Requirements:
- Requirement: requirement.md

Product Brief: product.md

Summary:
- Implement the accepted separation between refund request review and settlement outcome.

## Problem / Goal

Preserve the accepted product terminals in feature behavior and acceptance.

## Applicable Decisions

- none accepted

## Accepted Concept References

Concept Foundation Status: accepted
Source Requirement: requirement.md
Effective Concept Source: requirement.md

| Concept ID | Canonical Name | Feature Use | Source Definition / Trace |
|---|---|---|---|
| C-CUSTOMER | Customer | submits and observes | requirement.md#concept-definitions / TRACE-01 |
| C-REFUND-ADMIN | Refund Administrator | reviews and reconciles | requirement.md#concept-definitions / TRACE-02 |
| C-PAYMENT-PROVIDER | Payment Provider | reports settlement | requirement.md#concept-definitions / TRACE-03 |
| C-REFUND-REQUEST | Refund Request | request lifecycle | requirement.md#concept-definitions / TRACE-01 / TRACE-02 |
| C-REFUND-SETTLEMENT | Refund Settlement | settlement lifecycle | requirement.md#concept-definitions / TRACE-02 / TRACE-03 |

## Requirement Product Model Trace

| Requirement Model ID | Concept / Action / Flow / State IDs | Feature Behavior / Story | Acceptance / Verification Direction | Coverage |
|---|---|---|---|---|
| PM-01 | C-CUSTOMER / C-REFUND-ADMIN / C-REFUND-REQUEST / PERM-CUSTOMER-REQUEST / PERM-ADMIN-REQUEST / CMD-SUBMIT / CMD-APPROVE / FLOW-01 / FLOW-02 / STATE-REQUEST-01 / STATE-REQUEST-02 | US1 / US2 | approval never claims funds success | covered |
| PM-02 | C-PAYMENT-PROVIDER / C-REFUND-SETTLEMENT / PERM-ADMIN-SETTLEMENT / PERM-PROVIDER-SETTLEMENT / EVT-SETTLED / EVT-FAILED / CMD-RECONCILE / FLOW-03 / FLOW-04 / STATE-SETTLEMENT-01 / STATE-SETTLEMENT-02 / STATE-SETTLEMENT-03 / STATE-SETTLEMENT-04 / EX-01 / EX-02 | US3 | settlement terminals and recovery are observable | covered |

## Scope

- Request/review and settlement outcomes remain separate.
- Customer success notification follows STATE-SETTLEMENT-02 only.

## Stories

### US1: Submit refund request

Acceptance scenarios:
- Given eligibility, when CMD-SUBMIT runs, then STATE-REQUEST-01 is observable.

### US2: Approve without false completion

Acceptance scenarios:
- Given a submitted request, when CMD-APPROVE runs, then request is approved and settlement is pending.

### US3: Observe settlement terminal

Acceptance scenarios:
- Given a pending settlement, when EVT-SETTLED arrives, then success is observable and customer is notified.
- Given missing/failure evidence, when CMD-RECONCILE runs, then failure or manual-review is observable.

## Acceptance Criteria

- Accepted Concept IDs and PM-01/PM-02 meanings are unchanged.
- Approval alone never emits customer success.
- Duplicate or delayed provider results cannot create conflicting terminals.

## Out of Scope

- Concept-to-table/store/event/provider mapping.

## Open Questions

- none at product-semantics level
