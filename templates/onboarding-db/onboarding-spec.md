# Onboarding Spec

本文件是给 Agent 使用的文档生产规格。人类确认本 spec 和 onboarding tasks 后，Agent 可以全盘执行计划，连续创建并完成计划内能写透的 onboarding-db 文档。

## Target Readers

- 新人研发：
- 技术支持：
- 操作支持：
- 未来 Agent：

## Scope

- 范围：
- 非目标：
- 默认语言：

## Module Plan

| Module | Bounded Context | Why Required | Planned Path | Priority | Evidence |
|---|---|---|---|---|---|

## Flow Plan

| Flow | Why Required | Planned Path | Participants | Risk | Evidence |
|---|---|---|---|---|---|

## DDD Plan

| Bounded Context | Aggregates / Entities | Domain Services | Repositories | External Adapters | Evidence |
|---|---|---|---|---|---|

## Jobs / Async / Callback Plan

| Topic | Planned Path | Trigger | State Changed | Risk | Evidence |
|---|---|---|---|---|---|

## Infra / Deploy Plan

| Topic | Planned Path | Why Required | Evidence |
|---|---|---|---|

## Gateway / Runtime Plan

如果项目包含 Nginx、OpenResty、ingress、API gateway、reverse proxy、sidecar 或 runtime routing scripts，必须计划如何讲清楚 route matching、header 透传、鉴权、限流、超时、重试、upstream、日志字段和排障入口。

| Topic | Planned Path | Route / Runtime Scope | Required Evidence | Risk |
|---|---|---|---|---|

## File Strategy

- Module docs default to `02-modules/<module-name>.md`.
- Flow docs default to `03-flows/<flow-name>.md`.
- Split into directory only when justified by size, subdomains, update frequency, or human request.
- 计划确认后 Agent 可以全盘执行，可以一次性创建计划内的完整 onboarding-db。
- batch 是 Agent 的组织和 review 单位，不是人类闸门。
- 不创建空目录、薄 README、planned/later 占位文件、TBD/待补充文件。
- 写不透但有证据可推断的内容，要写出“推断”、证据、置信度和待验证点；完全缺少关键证据时，只在 coverage/tasks 记录 planned / blocked，不落薄文档。

## Diagram Rules

- Mermaid flowchart / sequenceDiagram 是普通流程图和时序图的首选格式；ASCII 文本图 / 纯文本线框图用于状态机、复杂原理图、复杂示例图和 Mermaid 不够清楚的局部。
- 状态图优先；状态机/决策图默认用 ASCII。
- 不要把复杂流程画成 stacked box diagram / 阶段堆叠图。
- 每个正式文档至少规划架构/边界图和 ASCII 状态图 / 状态机图。
- 模块文档默认必须规划架构/边界图、ASCII 状态图、Timeline / 时序图。
- 流程文档默认必须规划架构/边界图、ASCII 状态图、Timeline / 时序图。
- Every planned module/flow doc must have Required Architecture/Boundary Diagram, Required ASCII State Diagram, and Required Timeline/Sequence Diagram in the Diagram Plan, unless it is listed under Exemptions with a concrete reason.
- Mermaid flowchart / sequenceDiagram 可用于架构/边界图、普通流程图和 Timeline / 时序图。
- 每张图必须带讲解：说明图要看什么、表达什么结论、涉及哪些数据对象/状态字段/消息/配置和代码证据。
- 按需求选择 diagram type：
  - 架构/边界图：模块在哪、模块边界、输入输出、组件关系、Redis Key 布局、钱包类型结构、网关/DB/MQ 依赖；可用 Mermaid flowchart 或 ASCII。
  - ASCII 状态机/决策图：状态流转、校验分支、加锁/Lua/Kafka/Rollback、重试/补偿。
  - Timeline / 时序图：模块/流程默认必填，用于讲清流程按时间怎么跑、谁先读写什么、哪个阶段引用哪些数据模型；优先用 Mermaid sequenceDiagram。
  - ASCII 泳道图：可选项，用于责任归属、跨角色协作、多系统所有权。
  - Timeline Diagram：T1/T2/T3 故障恢复、回调重试、对账窗口、延迟一致性。
- Timeline / 时序图对 module / flow 默认必填。只有当前模块/流程确实没有有意义的时间顺序、状态阶段或数据流动时，才允许在 Exemptions 写明豁免原因。
- ASCII 原理机制图 / 示例图用于 `工作原理与示例`：当算法、路由选择、配额/计费、锁/事务/缓存/MQ 协作、provider 协议转换等不容易直接读懂时必须规划。
- 普通 Mermaid flowchart 可以作为架构/边界图或普通流程图；不要用 `A-->B-->C` 这种无边界、无状态、无数据对象的图当主图。
- 每个 planned content doc 都必须写明图类型；不要只给 module / flow 做图，overview / domain / jobs / infra / deploy / change-guide 只要是正式内容文档也要遵守双图要求。

## Diagram Plan

| Topic | Planned Path | Content Doc? | Required Architecture/Boundary Diagram | Required State Diagram | Required Timeline / Sequence | Principle / Example Diagram | Optional Swimlane / Timeline Window | Exemption / Reason |
|---|---|---|---|---|---|---|---|---|

## Exemptions

默认只有控制/审计文档可以豁免双图要求，例如 `onboarding-spec.md`、`onboarding-tasks.md`、`coverage-matrix.md`、`batch-review.md`、`08-review/evidence-graph.md`、`08-review/open-questions.md`、`08-review/human-review-summary.md`。正式内容文档如需豁免，必须在上方 Diagram Plan 写清楚原因。

## Quality Gates

- 模块文档必须包含：图解、架构/边界图、ASCII 状态图、Timeline / 时序图、Bounded Context / DDD 视角、核心用例、领域模型、数据对象、信息传递、状态流转、失败模式、工作原理与示例、验证/排障、代码证据和变更指南。
- 流程文档必须包含：架构/边界图、ASCII 状态图/状态机图、Timeline / 时序图、阶段、数据流转、状态变化、示例、失败路径、排障路径、变更指南、代码证据。
- 全部正式文档默认使用中文；代码符号、路径、命令、API、配置键、错误信息和第三方产品名保持原文。
- 低于 4/5 的 topic 不能标记 `newcomer-ready`。
- 关键 claim 必须带文件路径、符号/配置键、调用方向或数据流方向。
- 示例必须来自真实测试、fixture、API contract、日志、配置或代码构造对象；推断示例必须标明 inferred。
- 涉及 wallet、billing、quota、apikey、order、balance、message retry 的流程必须讲清楚一致性、幂等、事务边界、补偿和对账。
- 涉及 apikey / token / credential 的模块必须讲清楚 key 生成、hash/加密存储、脱敏展示、权限 scope、过期/轮换/吊销、泄露处置、审计日志。
- 提交前必须清除 `<...>`、TBD、TODO、待补充、空 required row、泛泛“看代码/see code”证据。

## Batch Plan

| Batch | Scope | Outputs | Required Evidence | Review Gate |
|---|---|---|---|---|

## Human Confirmation Questions

-

## Spec Acceptance Gate

- [ ] Evidence Graph 已有具体 code/config evidence。
- [ ] Module / Flow Plan 没有无证据候选项。
- [ ] 全量 planned docs 和 execution scope 已明确。
- [ ] Gateway / Runtime、consistency / idempotency 风险已决定是否适用。
- [ ] 人类已确认 Agent 可以按计划全盘执行。
