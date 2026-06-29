# Proposal: Evidence-Graph + DDD Module Playbook Onboarding

状态：讨论草案

目标版本：v1.2.x

创建时间：2026-06-28

默认语言：中文；代码符号、文件路径、命令、API、配置名、错误信息、第三方产品名保持原文。

## 目的

重构 `agent-loop` 的 onboarding 能力，把 `.agent-loop/onboarding-db/` 从“学习路径文档集合”升级为“新人 / 技术支持 / Agent 都能用的项目接手手册”。

新的 onboarding-db 不应靠目录数量证明完整，也不应一口气生成大量薄文档。它应先建立 Evidence Graph，再写 Onboarding Spec，再拆 Onboarding Tasks，最后按 DDD 模块和跨模块业务流程分批生产文档。

核心目标：

```text
代码事实
→ Evidence Graph
→ Onboarding Spec
→ Onboarding Tasks
→ 分批写模块手册 / 流程手册 / 运行手册 / 变更指南
→ Batch Review + Coverage Score
→ Human Review / Newcomer Ready
```

这份 proposal 主要给后续 Agent 执行使用，因此要求偏“生产说明书”，不是概念介绍。

## 背景问题

真实项目试跑暴露了当前 onboarding 的几个大问题：

1. **容易空心化**：Agent 会生成结构正确但没有细节的文档，只有组件名、路径和几句摘要。
2. **缺少模块级接手手册**：没有按 DDD / 模块边界讲清楚每个模块的用例、领域对象、数据对象、状态流转、失败模式和验证方式。
3. **流程表达不清晰**：普通 flowchart 只表达 A→B→C，不能很好呈现模块边界、信息输入输出、领域服务、状态对象、存储、外部依赖。
4. **文件生成策略摇摆**：既有过目录拆很细导致碎片化，也有过单文件总览导致泛泛而谈。
5. **缺少 Evidence Graph 前置**：Agent 没有先整理证据就写文档，容易凭文件名和经验猜测。
6. **缺少分批和评分机制**：一次性生成大量文档，review 时不知道哪些主题真的可接手。

因此需要用 Evidence Graph、DDD module playbook、state-first ASCII diagram 表达、batch task 和 score gate 重新约束 onboarding。

## 非目标

本 proposal 不做以下事情：

- 不把 Project Entry Scan 变成新人文档生成；
- 不要求一次生成完整 onboarding-db；
- 不要求每个模块都拆成多个小文件；
- 不创建空目录或空文件占位；
- 不把 Markdown 网站化作为本轮目标；
- 不把临时 TODO、未来 backlog 或未确认需求写入 `project.md`；
- 不把人类提供的示例当成固定主题列表、固定数量或固定领域名称。

## 核心原则

1. `project.md` 服务 Agent 执行；`onboarding-db` 服务人类和 Agent 理解项目。
2. onboarding-db 的第一产物是 Evidence Graph，不是 README。
3. Onboarding Spec 是后续文件生产的规格书，主要给 Agent 使用。
4. Module / Flow 文档默认使用单个长文件，只有足够复杂时才拆目录。
5. 优先使用线框图表达模块结构和流程边界；Mermaid 只做辅助。
6. 文档必须有项目事实、代码证据、用例、数据对象、状态变化、失败路径和排障/验证方式。
7. 当前 batch 才创建文件；不通过空文件表示计划。
8. coverage 跟踪主题可接手度，不跟踪文件数量。
9. 低分主题不能标记为 `newcomer-ready`。
10. 人类示例只代表详细程度和解释质量，不代表 topic、数量、领域词或项目结构。

## 总流程

```text
┌─────────────────────────────────────────────────────────────┐
│ Human asks for onboarding                                    │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Check reliable project memory                                │
│ - yes: continue                                               │
│ - no: Project Entry Scan first                                │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Evidence Graph                                                │
│ deploy units / modules / flows / data objects / async / risks │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Onboarding Spec                                               │
│ module plan / flow plan / DDD model / quality bar / batches   │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Human confirms spec                                           │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Onboarding Tasks                                              │
│ batch-by-batch production plan                                │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Batch Implementation                                          │
│ only current modules / flows / infra docs                     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Batch Review + Coverage Score                                 │
│ low score cannot be newcomer-ready                            │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Next Batch / Focused Update / Human Ready                     │
└─────────────────────────────────────────────────────────────┘
```

## 推荐信息架构

默认结构：

```text
.agent-loop/onboarding-db/
  README.md
  onboarding-spec.md
  onboarding-tasks.md
  coverage-matrix.md
  batch-review.md

  00-overview/
    system-context.md
    architecture-map.md
    code-organization.md
    learning-path.md
    glossary.md

  01-domain/
    domain-map.md
    bounded-contexts.md
    aggregates-and-entities.md
    domain-events.md
    cross-domain-data-flow.md

  02-modules/
    <module-name>.md

  03-flows/
    <flow-name>.md

  04-jobs-and-async/
    cronjobs.md
    consumers.md
    callbacks.md
    async-tasks.md

  05-infra/
    dependencies.md
    config.md
    storage-cache-mq.md
    observability.md
    security-license.md

  06-deploy/
    environments.md
    startup-order.md
    test-env.md
    runbooks.md

  07-change-guides/
    add-provider.md
    change-billing.md
    change-apikey-quota.md
    change-wallet.md
    change-runtime.md

  08-review/
    evidence-graph.md
    open-questions.md
    human-review-summary.md
```

### Module / Flow 文件策略

模块和流程默认使用单个长文件：

```text
02-modules/wallet.md
03-flows/model-request-charge.md
```

不要默认生成：

```text
02-modules/wallet/
  README.md
  module-wireframe.md
  use-cases.md
  ...
```

只有满足以下条件之一，才允许把单文件升级为目录：

- 单文件超过 1500-2000 行且难以阅读；
- 模块内部存在多个独立复杂子域；
- 某个章节需要频繁单独维护；
- 一个主题有多个长流程或多套状态机；
- 人类明确要求拆分。

升级示例：

```text
02-modules/wallet/
  README.md
  redis-wallet.md
  mysql-transaction.md
  recharge-callback.md
  reconciliation.md
```

## Phase 0: Entry Gate

进入 onboarding 前必须确认：

1. 已有可靠 `.agent-loop/project.md`；或
2. Project Entry Scan 已完成；或
3. 人类明确接受先做 onboarding evidence scan，并知道项目记忆可能不完整。

如果项目记忆缺失、过期、互相矛盾，必须先建议 Project Entry Scan 或 stale-memory recovery。

Project Entry Scan 不生成 onboarding-db。

## Phase 1: Evidence Graph

正式写 onboarding 文档前，先写：

```text
08-review/evidence-graph.md
```

Evidence Graph 是证据索引，不是摘要。它决定后续模块、流程、数据对象、异步任务、infra、deploy 和风险主题怎么选。

最低结构：

```md
# Evidence Graph

## Deployable Units

| Unit | Entry | Config | Depends On | Called By | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Bounded Context Candidates

| Context | Modules | Core Objects | Responsibilities | Evidence | Confidence |
|---|---|---|---|---|---|

## Module Candidates

| Module | Why It Is A Module | APIs | Data Objects | Use Cases | Evidence | Confidence |
|---|---|---|---|---|---|---|

## Flow Candidates

| Flow | Trigger | Participants | State Changes | External Dependencies | Evidence | Risk |
|---|---|---|---|---|---|---|

## Data Object Inventory

| Object | Kind | Owner | Key Fields / State | Used By | Evidence |
|---|---|---|---|---|---|

## Async / Job / Callback Inventory

| Name | Trigger | Consumer / Handler | State Changed | Retry / Compensation | Evidence |
|---|---|---|---|---|---|

## Infra / Dependency Inventory

| Dependency | Kind | Used By | Purpose | Config Source | Failure Symptom | Evidence |
|---|---|---|---|---|---|---|

## High-Risk Areas

| Area | Why Risky | Evidence | Required Docs |
|---|---|---|---|

## Unknowns

| Question | Why It Matters | Evidence Missing | Human Needed? |
|---|---|---|---|
```

规则：

- 没有 Evidence Graph，不允许写正式 module / flow docs。
- Evidence Graph 可以低置信，但必须标 `Confidence`。
- 不确定的地方进入 `Unknowns`，不要编造。

## Phase 2: Onboarding Spec

写：

```text
onboarding-spec.md
```

这个文件是给 Agent 后续执行用的生产规格。

必须包含：

- 目标读者：新人研发、技术支持、操作支持、未来 Agent；
- 本轮 scope：全项目还是 focused area；
- 模块计划；
- flow 计划；
- DDD bounded context 计划；
- jobs / async / callback 计划；
- infra / deploy 计划；
- 文件策略：默认单文件，何时拆目录；
- 线框图规范；
- 每类文档质量门禁；
- batch 切分；
- 本轮不做什么；
- 需要人类确认的问题。

`onboarding-spec.md` 写完后必须让人类确认。未确认前，不创建大批正式文档。

### Module Plan 示例

```md
## Module Plan

| Module | Bounded Context | Why Required | Planned Path | Priority | Evidence |
|---|---|---|---|---|---|
| router | API Gateway / Request Orchestration | 所有模型请求入口 | `02-modules/router.md` | P0 | ... |
| wallet | Billing / Balance | 资金状态核心 | `02-modules/wallet.md` | P0 | ... |
```

### Flow Plan 示例

```md
## Flow Plan

| Flow | Why Required | Planned Path | Participants | Risk | Evidence |
|---|---|---|---|---|---|
| model-request-charge | 核心模型请求与扣费闭环 | `03-flows/model-request-charge.md` | router/provider/model/charge/wallet | high | ... |
```

## Phase 3: Onboarding Tasks

写：

```text
onboarding-tasks.md
```

任务按 batch 拆，用于 Agent 自己组织执行、review 和进度记录。batch 不是人类闸门。

规则：

- batch 大小由 Agent 按证据和上下文压力决定，不是总量限制；
- 人类确认 Onboarding Spec / Onboarding Tasks 后，Agent 可以全盘执行，连续创建并完成计划内能写透的 onboarding-db 文档；
- 可以一次性创建计划内的完整 onboarding-db，但每个落盘文件都必须是内容型文档；
- 不创建空目录、空文件、薄 README、planned/later 占位文件、TBD/待补充文件；
- 写不透但有证据可推断的内容，要标明“推断”、证据、置信度和待验证点；
- 完全缺少关键证据的主题，只记录在 `coverage-matrix.md` / `onboarding-tasks.md`，不落薄文档；
- 每个 task 必须写明 evidence source 和 quality gate；
- 每个 task 完成后更新 `coverage-matrix.md` 和 `batch-review.md`。

示例：

```md
# Onboarding Tasks

## Batch 1: Core Request Path

| Task | Output | Evidence Required | Quality Gate |
|---|---|---|---|
| B1-T1 | `02-modules/router.md` | router server/check/chat/fallback/model_factory | wireframe + use cases + data/state + failure modes |
| B1-T2 | `02-modules/provider.md` | provider route/chat/biz/provider clients | wireframe + provider adapter examples |
| B1-T3 | `03-flows/model-request-charge.md` | router/provider/charge/wallet/model | end-to-end data/state flow + troubleshooting |
```

## Phase 4: Batch Implementation

当前 batch 才写文档。

### Module 文档模板

默认路径：

```text
02-modules/<module-name>.md
```

最低结构：

```md
# Module: <module-name>

## 1. 模块定位

## 2. 模块线框图

## 3. Bounded Context / DDD 视角

## 4. 核心用例

## 5. 领域模型

## 6. 数据对象

## 7. 信息传递

## 8. API / Events / Jobs

## 9. 状态流转

## 10. 失败模式

## 11. 验证和排障

## 12. 关键代码索引

## 13. 变更指南
```

每个模块必须包含：

- 至少一个模块线框图；
- 至少 3 个核心 use case，除非 Evidence Graph 证明少于 3 个；
- 领域对象表；
- 数据对象表；
- inbound / outbound 信息传递；
- 状态变化；
- 失败、重试、补偿、降级；
- 验证和排障入口；
- 代码证据。

### Flow 文档模板

默认路径：

```text
03-flows/<flow-name>.md
```

最低结构：

```md
# Flow: <flow-name>

## 1. 用例

## 2. 线框流程图

## 3. 阶段说明

## 4. 数据流转

## 5. 状态变化

## 6. 示例

## 7. 失败路径

## 8. 排障路径

## 9. 变更指南

## 10. 代码证据
```

每个 flow 必须包含：

- 触发入口；
- 参与模块；
- 线框式流程图；
- 阶段说明；
- 数据对象如何传递；
- 状态如何变化；
- 成功路径；
- 失败路径；
- 重试 / 补偿 / 降级；
- 示例请求 / 示例对象；
- 排障路径；
- 变更指南；
- 代码证据。

## Wireframe 规范

默认使用 ASCII wireframe / box diagram 表达模块结构和流程边界。

不要把普通 flowchart 当作主图：

```text
A --> B --> C
```

优先使用这种结构化线框：

```text
┌─────────────────────────────────────────────────────────────┐
│ Wallet Module                                                │
├─────────────────────────────────────────────────────────────┤
│ Inbound                                                      │
│  - charge.ModelCharge -> wallet.Consume                      │
│  - payment callback -> rechargeCb                            │
│  - user register gift -> OperationGift                       │
├─────────────────────────────────────────────────────────────┤
│ Application / Domain Services                                │
│  - WalletBackendSvc.CanConsume                               │
│  - WalletBackendSvc.Consume                                  │
│  - WalletConsume.doWalletConsume                             │
├─────────────────────────────────────────────────────────────┤
│ Domain State                                                 │
│  - WalletUser: current balance                               │
│  - WalletOrder: idempotent consume order                     │
│  - WalletBill: balance movement record                       │
│  - PayBill: payment/recharge order                           │
├─────────────────────────────────────────────────────────────┤
│ Persistence / Infrastructure                                 │
│  - MySQL transaction path                                    │
│  - Redis wallet fast path                                    │
│  - Mongo wallet change mgmt                                  │
├─────────────────────────────────────────────────────────────┤
│ Outbound / Side Effects                                      │
│  - reconciliation                                            │
│  - invite reward notify                                      │
│  - wallet alarm                                              │
└─────────────────────────────────────────────────────────────┘
```

线框图必须表达：

- 模块边界；
- inbound caller；
- application / domain services；
- domain state；
- persistence / infrastructure；
- outbound side effects；
- high-risk edge if applicable。

Mermaid 可作为辅助：

- sequenceDiagram：详细交互；
- erDiagram：领域实体关系；
- stateDiagram：状态机；
- flowchart：只用于小范围决策，不作为默认主图。

## DDD 映射要求

每个模块和 flow 必须尽量映射到：

- Bounded Context；
- Aggregate / Entity；
- Value Object；
- Domain Service；
- Repository；
- External Adapter；
- Domain Event / Async Message；
- State Machine。

如果项目不是严格 DDD，也要用 DDD 视角帮助新人理解“谁拥有事实、谁改变状态、谁只是适配器”。

示例表：

```md
| DDD Concept | Project Object | Evidence | Notes |
|---|---|---|---|
| Aggregate | WalletUser | `services/wallet/model/wallet_user.go` | 当前余额事实来源 |
| Domain Service | WalletConsume | `services/wallet/service/wallet_consume.go` | 扣费策略和事务边界 |
| External Adapter | Payment Client | ... | 支付系统适配 |
```

## 内容门禁

### 禁止泛泛而谈

以下写法不合格：

- “wallet 负责钱包余额和充值”；
- “provider 负责协议转换”；
- “router 调用 provider 然后计费”；
- “失败时查看日志”；
- 只列文件名；
- 只画 A→B→C；
- 用 TODO 代替证据；
- 每个文件只有几行。

合格写法必须包含：

- 真实 use case；
- 真实对象名；
- 真实代码证据；
- 状态变化；
- 信息传递；
- 失败模式；
- 排障路径；
- 变更验证方式。

### Use Case 门禁

每个 use case 至少包含：

| Field | Required |
|---|---|
| Trigger | yes |
| Caller | yes |
| Input object | yes |
| Domain objects touched | yes |
| State changes | yes |
| Output | yes |
| Failure path | yes |
| Code evidence | yes |

### Data Object 门禁

必须区分：

- API / proto object；
- DB model；
- DTO / internal struct；
- config object；
- event / message object；
- external object。

每个对象必须包含：

- owner；
- meaning；
- key fields；
- state semantics；
- read/write path；
- evidence。

### Failure Mode 门禁

每个 failure mode 必须包含：

- 失败现象；
- 可能原因；
- 先查什么；
- 关键日志 / 字段 / request id / order id；
- 是否可重试；
- 是否需要人工确认；
- 代码证据。

## Coverage Matrix

`coverage-matrix.md` 跟踪主题可接手度，不跟踪文件数量。

推荐字段：

```md
| Topic | Type | Doc Path | Score | Status | Missing Evidence | Next Action |
|---|---|---|---|---|---|---|
```

Topic type：

- overview；
- domain；
- module；
- flow；
- jobs-async；
- infra；
- deploy；
- change-guide。

Status：

- discovered；
- planned；
- in-progress；
- draft；
- needs-review；
- newcomer-ready；
- stale；
- blocked-by-unknown；
- not-applicable。

## Review Score

每个 batch 完成后必须评分。

评分维度：

| Dimension | Meaning |
|---|---|
| Wireframe clarity | 线框图是否清楚表达边界和信息流 |
| Use case completeness | 用例是否能支撑新人理解模块 |
| Data object completeness | 数据对象是否区分 proto/DB/DTO/config/event |
| State transition clarity | 状态变化是否讲清楚 |
| Code evidence | 是否有具体文件 / symbol / 行为证据 |
| Failure troubleshooting | 失败路径和排障是否可用 |
| Change guidance | 新人要改代码时是否知道从哪里下手 |
| Newcomer readability | 是否能被新人连续阅读 |

规则：

- 低于 4/5 的主题不能标记 `newcomer-ready`；
- 低于 3/5 的主题必须进入下一 batch 或标记 `blocked-by-unknown`；
- review 必须记录缺口，不允许只写 “done”。

## Batch Review

`batch-review.md` 记录每批：

- batch id；
- scope；
- files changed；
- evidence read；
- coverage changes；
- score；
- gaps；
- unknowns；
- recommended next batch；
- human review status。

最低结构：

```md
# Onboarding Batch Review

## Batch <n>: <name>

## Scope

## Files Changed

## Evidence Read

## Coverage Changes

## Score

## Gaps / Unknowns

## Recommended Next Batch

## Human Review Status
```

## Guided Use / Focused Update

当 onboarding-db 已存在，人类问项目理解或线上支持问题时：

1. 先读 `README.md`、`coverage-matrix.md` 和相关 module / flow；
2. 检查代码现实，避免依赖 stale docs；
3. 直接回答问题；
4. 如果文档薄、过期或冲突，提出 focused update；
5. focused update 只更新相关 module / flow / review，不重跑全量 onboarding；
6. 只有发现稳定项目事实缺失时，才建议 Project Memory Update。

## Project Memory 边界

- `project.md` 只存当前状态、索引、稳定事实和下一步建议；
- onboarding-db 存新人理解材料；
- onboarding-spec / tasks / review 留在 onboarding-db；
- 不把临时 TODO、未来 backlog、未确认需求写入 `project.md`；
- onboarding 发现稳定项目事实时，可以建议回写 project memory；
- 代码变化导致 onboarding 过期时，coverage 标记 `stale` 或 `needs-refresh`。

## Validation Scenarios

后续实现必须至少覆盖这些场景：

### Scenario 1: Prevent outline-only module docs

输入：人类要求 “深度 onboarding 这个多服务项目”，项目包含 wallet/charge/provider/router。

期望：

- Agent 先写 Evidence Graph；
- Agent 写 Onboarding Spec 并等待确认；
- Agent 不直接创建大量 module 文件；
- module 文档必须包含 wireframe、use cases、data objects、failure modes、code evidence；
- 只有当前 batch 的文件被创建。

### Scenario 2: Module default single-file

输入：spec 计划写 wallet module。

期望：

- 默认创建 `02-modules/wallet.md`；
- 不创建 `02-modules/wallet/use-cases.md` 等碎片文件；
- 只有当单文件过大或人类要求时才拆目录。

### Scenario 3: Flow default single-file

输入：spec 计划写 model request charge flow。

期望：

- 默认创建 `03-flows/model-request-charge.md`；
- 文档包含线框流程图、阶段说明、数据流转、状态变化、示例、失败路径、排障路径和代码证据。

### Scenario 4: Human example is quality reference only

输入：人类提供一个 stars 文件作为详细程度参考。

期望：

- Agent 不复制该文件主题数量；
- Agent 不硬控 5 个 topic；
- Agent 按 Evidence Graph 决定模块和流程；
- Agent 只借鉴解释深度和结构质量。

### Scenario 5: Existing onboarding-db migration

输入：项目已有旧 directory-first onboarding-db。

期望：

- Agent 将旧文档作为 evidence；
- Agent 不直接刷新旧结构；
- Agent 写 spec 说明迁移策略；
- 新文档按 single-file module / flow 默认策略创建。

## Implementation Notes

后续实现应更新：

- `references/onboarding-knowledge-base.md`
- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/validation-scenarios.md`
- `templates/onboarding-db/`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

旧学习路径式 onboarding proposal 已废弃；本 proposal 是当前 onboarding 设计参考，避免两个 onboarding proposal 互相冲突。

## Open Questions

1. 是否保留 `00-overview/` 和 `01-domain/` 下多个文件，还是也默认压缩为 `overview.md` / `domain.md`？
2. 是否需要提供一个真实项目的 golden sample onboarding-db 作为对标？
3. 是否要加入脚本检查空心文档，例如检测 module docs 是否包含 wireframe/use cases/data objects/failure modes/code evidence 标题？
4. 是否把 score gate 做成人工 checklist，还是提供可选 validator？

## 当前建议

接受本 proposal 后，下一步不是直接改现有 onboarding 文档，而是：

1. 以本 proposal 作为当前 onboarding 方案参考；
2. 先补 validation scenarios；
3. 再改 reference 和 templates；
4. 最后用真实项目进行压力测试。
