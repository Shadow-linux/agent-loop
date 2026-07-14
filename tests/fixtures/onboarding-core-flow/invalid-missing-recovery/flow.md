# Flow: incomplete payment

Flow ID: CF-ORDER-PAYMENT

| Slice ID | Action | Evidence | Diagram IDs | Document Section | Coverage Status |
|---|---|---|---|---|---|
| CF-ORDER-PAYMENT/S01 | create | `order/handler.go#Create` | D-BOUNDARY | §3 | covered |
| CF-ORDER-PAYMENT/S02 | processing | `payment/client.go#Create` | D-SEQUENCE | §4 | covered |
| CF-ORDER-PAYMENT/S03 | webhook | `payment/webhook.go#Handle` | D-SEQUENCE | §5 | covered |
| CF-ORDER-PAYMENT/S04 | duplicate | `payment/webhook.go#event_id` | D-STATE | §6 | covered |
| CF-ORDER-PAYMENT/S05 | retry/DLQ | `config/kafka.yaml#retry` | D-RECOVERY | §7 | covered |
| CF-ORDER-PAYMENT/S06 | reconcile | `order/reconcile.go#Run` | D-RECOVERY | §8 | covered |

The required cancel/race recovery slice S07 is intentionally absent.
