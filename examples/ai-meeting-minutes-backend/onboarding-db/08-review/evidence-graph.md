# Evidence Graph

This reference uses synthetic code paths to demonstrate the onboarding artifact contract.

## Core Flow Inventory

| Flow ID | Flow | Business Outcome | Criticality | Trigger / Entry | Success Terminal | Failure Terminals | Variants / Branches | Participants / Owners | State / Data Owners | Async / Jobs / Callbacks | External Side Effects | Recovery Responsibility | Evidence Chain | Selection | Selection Reason | Confidence / Unknowns |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CF-ORDER-PAYMENT | 订单支付闭环 | 已创建订单最终得到可确认的支付结果 | critical | `POST /orders` -> `OrderHandler.Create` | `PAID` + `OrderPaidEvent` | `FAILED` / `CANCELLED` / `PAYMENT_UNKNOWN` / `MANUAL_REVIEW` | sync processing / webhook / retry / reconcile / cancel | Order API / Payment Adapter / Webhook Consumer / Reconciler | `orders.status` owned by OrderService | `PaymentWebhookConsumer` / retry topic / DLQ / `ReconcileJob` | provider charge + paid event | idempotent callback, retry, reconcile, manual review | `internal/order/handler.go#Create` -> `internal/payment/client.go#CreatePayment` -> `internal/payment/webhook.go#Handle` -> `internal/order/reconcile.go#Run` | planned | 新人必须理解同步非终态与异步恢复闭环 | high; cancel/reconcile race requires conditional update |

## Async / Job / Callback Inventory

| Name | Trigger | Consumer / Handler | State Changed | Retry / Compensation | Evidence |
|---|---|---|---|---|---|
| payment webhook | provider callback | `PaymentWebhookConsumer.Handle` | `PROCESSING -> PAID/FAILED` | provider event idempotency | `internal/payment/webhook.go#Handle` |
| payment reconcile | 10-minute schedule | `ReconcileJob.Run` | `PAYMENT_UNKNOWN -> PAID/MANUAL_REVIEW` | query provider and republish | `internal/order/reconcile.go#Run` |

## Unknowns

| Question | Why It Matters | Evidence Missing | Human Needed? |
|---|---|---|---|
| cancel and late webhook ordering | prevents illegal terminal overwrite | production race trace | yes |
