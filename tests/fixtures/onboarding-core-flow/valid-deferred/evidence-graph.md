# Evidence Graph

| Flow ID | Flow | Business Outcome | Criticality | Success Terminal | Failure Terminals | Selection | Selection Reason |
|---|---|---|---|---|---|---|---|
| CF-REFUND | refund | return captured funds | important | REFUNDED | REFUND_FAILED / MANUAL_REVIEW | deferred | impact=refund onboarding unavailable; missing=evidence for provider callback; next=inspect refund webhook and retry worker |
