# Coverage Matrix

Document Language: 中文
Created:
Last Updated:
Last Verified:
Confidence:
Source Evidence:
Human Review Status: draft

## Purpose

Coverage Matrix 分离 `Confidence` 和 `Completion Status`。`high / medium / low` 只说明证据强度；完成度必须使用 completion status。

Completion status path:

```text
discovered -> graph-only -> needs-deep-trace -> newcomer-ready
discovered -> supporting-summary
discovered -> not-applicable
needs-deep-trace -> blocked-by-unknown
blocked-by-unknown -> needs-deep-trace -> newcomer-ready
```

Quick completion status options include: graph-only | needs-deep-trace | newcomer-ready.

## Coverage Table

| Item | Type | Graph Node / Edge | Core Role | Required For Deep Complete? | Required Doc / Diagram | Current Evidence | Confidence | Completion Status | Human Review Status | Blocker / Unknown | Next Action |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Deep Completion Decision

| Gate | Pass? | Evidence | Missing / Blocker | Completion Impact |
|---|---|---|---|---|
| Evidence Graph covers required-core services, entrypoints, domains, data, runtime, and risks | | | | |
| Core Domain Inventory has fact sources and owning modules | | | | |
| Core Flow Inventory lists required-core flows and trace priority | | | | |
| Required-core flows are newcomer-ready | | | | |
| Required-core modules are newcomer-ready | | | | |
| Service Startup Matrix covers runnable services/processes | | | | |
| Verification and observability are linked to core flows | | | | |

Allowed decisions:

```text
Quick onboarding complete; Deep onboarding not complete.
Onboarding DB draft is usable but incomplete.
Deep onboarding complete.
Targeted onboarding complete for <scope>. Full Deep onboarding remains incomplete unless global gates pass.
```
