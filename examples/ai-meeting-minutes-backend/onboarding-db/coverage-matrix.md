# Coverage Matrix

## Completeness Hard Gate

| Flow ID | Criticality | Business Terminals Closed? | Required Slice IDs | Missing / Blocked Slice IDs | Evidence + Diagram + Section Trace Complete? | Result | Next Action |
|---|---|---|---|---|---|---|---|
| CF-ORDER-PAYMENT | critical | yes | CF-ORDER-PAYMENT/S01, CF-ORDER-PAYMENT/S02, CF-ORDER-PAYMENT/S03, CF-ORDER-PAYMENT/S04, CF-ORDER-PAYMENT/S05, CF-ORDER-PAYMENT/S06, CF-ORDER-PAYMENT/S07 | none | yes | PASS | keep evidence current |

| Topic | Type | Doc Path | Score | Status | Missing Evidence | Next Action |
|---|---|---|---:|---|---|---|
| CF-ORDER-PAYMENT | flow | `03-flows/order-payment.md` | 4.5 | newcomer-ready | production race trace | focused update after trace capture |
