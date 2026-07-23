# Evidence Graph

## Core Flow Inventory

| Flow ID | Flow | Business Outcome | Criticality | Trigger / Entry | Success Terminal | Failure Terminals | Variants / Branches | Recovery Responsibility | Evidence Chain | Selection | Selection Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CF-ORDER-PAYMENT | order payment | final payment result | critical | CreateOrder | PAID | FAILED / CANCELLED / PAYMENT_UNKNOWN | webhook / retry / reconcile / cancel | retry and reconcile | handler -> webhook -> reconcile | planned | core revenue flow |
