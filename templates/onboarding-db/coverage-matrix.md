# Coverage Matrix

Coverage tracks topic readiness, not file count.

| Topic | Type | Doc Path | Score | Status | Missing Evidence | Next Action |
|---|---|---|---|---|---|---|

## Status Definitions

| Status | Meaning |
|---|---|
| discovered | 证据图中发现，但尚未计划 |
| planned | 已进入 Onboarding Spec / Tasks |
| in-progress | 当前 batch 正在写 |
| draft | 草稿存在，但未 review |
| needs-review | 等待人类或 Agent review |
| newcomer-ready | 评分 >= 4/5 且人类确认新人可读 |
| stale | 代码现实已变化，需要刷新 |
| blocked-by-unknown | 缺少代码证据或业务确认 |
| not-applicable | 明确不适用 |

## Score Dimensions

| Dimension | Score | Notes |
|---|---|---|
| Required diagram set present |  |  |
| Architecture diagram clarity |  |  |
| State diagram clarity |  |  |
| Timeline / sequence clarity |  |  |
| Use case completeness |  |  |
| Data object completeness |  |  |
| State transition clarity |  |  |
| Code evidence |  |  |
| Failure troubleshooting |  |  |
| Change guidance |  |  |
| Newcomer readability |  |  |

Rules:

- Below 4/5 cannot be `newcomer-ready`.
- Below 3/5 must enter next batch or be `blocked-by-unknown`.
- Every formal topic should include at least architecture/boundary + ASCII state diagram. Module and flow docs should also include Timeline / sequence diagrams by default. Mermaid flowchart / sequenceDiagram is preferred for normal flow and timing; ASCII is preferred for state-machine / decision diagrams and complex examples. Swimlane-style ownership lanes are optional supporting detail, but the timeline explanation is required for module/flow docs unless explicitly exempted in the accepted spec.
