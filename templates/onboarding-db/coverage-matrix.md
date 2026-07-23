# Coverage Matrix

Coverage tracks topic readiness, not file count.

| Topic | Type | Doc Path | Score | Status | Missing Evidence | Next Action |
|---|---|---|---|---|---|---|

## Completeness Hard Gate

先判完整性，再评分。任何 `critical` / `important` flow 有 missing/blocked critical slice，都不能进入 `newcomer-ready`，也不能靠其他维度高分抵消。

| Flow ID | Criticality | Business Terminals Closed? | Required Slice IDs | Missing / Blocked Slice IDs | Evidence + Diagram + Section Trace Complete? | Result | Next Action |
|---|---|---|---|---|---|---|---|

`Result` 只使用 `PASS` / `FAIL` / `blocked-by-unknown`。Focused scope 通过只代表明确边界内通过，不能写成 whole-project ready。

## Status Definitions

| Status | Meaning |
|---|---|
| discovered | 证据图中发现，但尚未计划 |
| planned | 已进入 Onboarding Spec / Tasks |
| in-progress | 当前 batch 正在写 |
| draft | 草稿存在，但未 review |
| needs-review | 等待人类或 Agent review |
| newcomer-ready | Completeness Hard Gate PASS、评分 >= 4/5、证据与 gap 记录完整 |
| stale | 代码现实已变化，需要刷新 |
| blocked-by-unknown | 缺少代码证据或业务确认 |
| not-applicable | 明确不适用 |

## Score Dimensions

| Dimension | Score | Notes |
|---|---|---|
| Core flow discovery completeness |  |  |
| Slice and branch coverage |  |  |
| Required diagram set present |  |  |
| Architecture diagram clarity |  |  |
| State diagram clarity |  |  |
| Timeline / sequence clarity |  |  |
| Use case completeness |  |  |
| Data object completeness |  |  |
| State transition clarity |  |  |
| Code evidence |  |  |
| Evidence granularity |  |  |
| Example authenticity |  |  |
| Failure / recovery |  |  |
| Troubleshooting |  |  |
| Consistency / gateway risk |  |  |
| Change guidance |  |  |
| Newcomer readability |  |  |

Rules:

- Completeness Hard Gate must pass before quality scoring.
- Below 4/5 cannot be `newcomer-ready`.
- Below 3/5 must enter next batch or be `blocked-by-unknown`.
- `critical` / `important` flow docs require Core Flow Overview / Boundary, ASCII State Machine / Decision, and Timeline / Sequence. Other topics select diagrams that explain real semantics; stateless topics do not invent state diagrams.

## Score Anchors

| Score | Anchor |
|---:|---|
| 5 | 完整且证据闭合，新人可以独立解释、验证和排障 |
| 4 | 核心路径完整，只有不影响接手的低风险缺口 |
| 3 | 主路径可理解，但分支、恢复或证据有明显缺口 |
| 2 | 结构存在，内容主要是概览或泛化描述 |
| 1 | 无法依靠该文档理解或操作 |
