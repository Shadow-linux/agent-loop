# Onboarding Tasks

| Task | Output | Flow ID | Required Slice IDs | Required / Conditional Diagram IDs | Evidence Required | Completeness Hard Gate | Quality Score Target | Status |
|---|---|---|---|---|---|---|---|---|
| Document order-payment closure | `03-flows/order-payment.md` | CF-ORDER-PAYMENT | CF-ORDER-PAYMENT/S01, CF-ORDER-PAYMENT/S02, CF-ORDER-PAYMENT/S03, CF-ORDER-PAYMENT/S04, CF-ORDER-PAYMENT/S05, CF-ORDER-PAYMENT/S06, CF-ORDER-PAYMENT/S07 | D-BOUNDARY, D-STATE, D-SEQUENCE, D-RECOVERY, D-ASYNC | handler/client/webhook/reconcile symbols and direction | must PASS before score | >=4 | complete |

## Full Execution Gate

- Status: accepted
- Scope: CF-ORDER-PAYMENT/S01-S07 and Diagram IDs listed above
