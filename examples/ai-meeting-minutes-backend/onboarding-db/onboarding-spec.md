# Onboarding Spec

## Core Flow Selection

| Flow ID | Criticality | Business Outcome | Success / Failure Terminals | Variants / Recovery | Selection | Selection Reason / Impact | Evidence Chain |
|---|---|---|---|---|---|---|---|
| CF-ORDER-PAYMENT | critical | 订单得到最终支付结果 | PAID / FAILED / CANCELLED / PAYMENT_UNKNOWN / MANUAL_REVIEW | webhook / retry / DLQ / reconciliation / cancel | planned | 决定收入状态和用户可见结果 | handler -> payment client -> webhook -> reconciler |

## Flow Slice Plan

| Flow ID | Required Slice IDs | Main / Branch / Failure / Recovery Scope | State / Side Effect / Terminal Owned | Required Evidence | Planned Document |
|---|---|---|---|---|---|
| CF-ORDER-PAYMENT | CF-ORDER-PAYMENT/S01, CF-ORDER-PAYMENT/S02, CF-ORDER-PAYMENT/S03, CF-ORDER-PAYMENT/S04, CF-ORDER-PAYMENT/S05, CF-ORDER-PAYMENT/S06, CF-ORDER-PAYMENT/S07 | create / processing / webhook / duplicate / retry-DLQ / reconcile / cancel race | order terminals and OrderPaidEvent | file + symbol + direction | `03-flows/order-payment.md` |

## Diagram Plan

| Topic / Flow ID | Planned Path | Content Doc? | Complexity Signals | Required Architecture/Boundary Diagram | Required State Diagram | Required Timeline / Sequence | Conditional Diagram Types | Covered Slice IDs | Exemption / Reason |
|---|---|---|---|---|---|---|---|---|---|
| CF-ORDER-PAYMENT | `03-flows/order-payment.md` | yes | callback/retry/reconcile/idempotency/async | D-BOUNDARY | D-STATE | D-SEQUENCE | D-RECOVERY, D-ASYNC | S01-S07 | none |
