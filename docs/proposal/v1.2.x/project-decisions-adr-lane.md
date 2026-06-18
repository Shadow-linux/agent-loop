# Proposal: Project Decisions / ADR Lane

状态：讨论草案
目标版本：v1.2.x
创建时间：2026-06-16

## 目的

这份 proposal 先讨论 `agent-loop` 中项目级决策记录的目录规范和触发时机。

它暂不定义完整 ADR 方法论，也不要求所有需求都创建 ADR。当前目标是先把这些问题收敛清楚：

- 项目级长期决策放在哪里；
- requirement、feature、project memory 如何引用这些决策；
- 什么情况下 Agent 应该建议创建 ADR；
- 在 agent-loop 哪些阶段执行 Decision Scan；
- feature-local 小决策什么时候直接写进 `spec.md`，什么时候升级为独立 ADR。

## 核心观点

```text
Decision Scan 是必选检查。
ADR / project decision file 是可选产物。
决策记录应该放在它影响范围的最小稳定层级。
```

ADR 不是 feature spec 的替代品，也不是 project memory 的替代品。

| 对象 | 主要职责 | 不负责 |
|---|---|---|
| `requirements/<set>/` | 保存人类原始需求材料和来源索引 | 不承载可变工程设计 |
| `features/<feature>/spec.md` | 记录 feature 行为、约束、验收标准和轻量设计决策 | 不承载跨 feature 的长期项目决策 |
| `project.md` | 当前工作状态、长期记忆入口、enterprise memory 索引 | 不成为完整决策历史库 |
| `project/*.md` | enterprise mode 下的长期事实分片 | 不解释每个事实当初为什么成立 |
| `decisions/*.md` | 记录跨 feature / 长期项目决策的原因、取舍、结果 | 不记录普通执行日志 |

## 建议目录

建议新增顶层长期决策目录：

```text
.agent-loop/
  project.md
  decisions/
    0001-use-markdown-agent-loop-artifacts.md
    0002-keep-requirements-as-source-archive.md
    0003-use-decision-scan-before-feature-spec.md
  project/
    architecture.md
    boundaries.md
```

`decisions/` 是 `.agent-loop/` 的一等长期 artifact，不属于 enterprise-only `project/` memory 分片。

它和 `project.md`、`project/*.md` 的职责不同：

```text
project.md = 当前状态、入口索引、memory 路由。
project/*.md = enterprise mode 下的当前长期事实和导航。
decisions/*.md = 为什么形成这些事实和约束。
```

因此 `decisions/` 可以在 simple memory mode 和 enterprise memory mode 下使用。创建 `decisions/` 不应自动触发 enterprise mode；enterprise mode 仍只由 `project.md` 可读性、项目复杂度、边界数量等 memory trigger 决定。

## 决策放置规则

决策记录按影响范围放置：

| 决策范围 | 推荐位置 | 示例 |
|---|---|---|
| 只影响当前 feature，且取舍简单 | `features/<feature>/spec.md` 的 `Design Decisions` | 某个交互或内部实现小选择 |
| 只影响当前 feature，但取舍复杂 | `features/<feature>/decisions/`，需另行讨论是否支持 | 某个 feature 的状态机或迁移策略 |
| 来自某个 requirement，影响多个 feature | 优先 `decisions/`，requirement README 只引用 | 需求拆分策略、统一工作流约束 |
| 影响长期项目结构、边界、依赖、工作流 | `decisions/` | artifact ownership、技术栈、数据存储、跨 feature 规则 |

v1.2.x 建议先只正式支持两类：

```text
1. feature-local 小决策：写入 feature/spec.md。
2. project-level 长期决策：写入 decisions/*.md。
```

暂不把 requirement-level ADR 和 feature-level ADR 复杂体系纳入正式规则，避免第一版把 artifact 体系变重。

## 引用关系

### Requirement 引用

Requirement set 不拥有项目级决策，但可以引用：

```md
## Applicable Project Decisions

- [ADR-0002: Keep requirements as source archive](../../decisions/0002-keep-requirements-as-source-archive.md)

## Decisions Triggered By This Requirement

- [ADR-0003: Use decision scan before feature spec](../../decisions/0003-use-decision-scan-before-feature-spec.md)
```

含义：

```text
Applicable Project Decisions = 这个需求受哪些长期决策约束。
Decisions Triggered By This Requirement = 这个需求触发了哪些新的项目级决策。
```

原始 `requirement.md` 不应被重写。引用应放在 `README.md` 或 requirement set 的索引文件中。

### Feature 引用

Feature spec 应引用源需求和适用决策：

```md
## Source Requirements

- [.agent-loop/requirements/2026-06-16-agent-loop-adr/requirement.md](../../requirements/2026-06-16-agent-loop-adr/requirement.md)

## Applicable Decisions

- [ADR-0001: Use markdown agent-loop artifacts](../../decisions/0001-use-markdown-agent-loop-artifacts.md)
- [ADR-0002: Keep requirements as source archive](../../decisions/0002-keep-requirements-as-source-archive.md)

## Design Decisions

- Inline feature-local decisions that do not need standalone ADR files.
```

含义：

```text
Source Requirements = 这个 feature 从哪些需求材料推导出来。
Applicable Decisions = 这个 feature 实施时必须遵守哪些长期决策。
Design Decisions = 当前 feature 内部的小型设计取舍。
```

### Project Memory 引用

`project.md` 应把 decisions 作为索引项，而不是复制完整决策内容：

```md
## Project Memory Index

- Architecture: .agent-loop/project/architecture.md
- Boundaries: .agent-loop/project/boundaries.md
- Decisions: .agent-loop/decisions/ | none
```

如果某个 decision 改变了长期事实，应同时回补对应 memory 文件：

```text
decisions/0003-use-decision-scan-before-feature-spec.md
  explains why.

project/architecture.md or project/boundaries.md
  records current project reality after the decision is accepted.
```

## Decision Scan 触发阶段

Decision Scan 是一个轻量检查，不等于创建 ADR。

建议在这些阶段触发：

| 阶段 | 行为 |
|---|---|
| Requirement Intake / Archive 后 | 检查需求是否可能触发跨 feature 或长期项目决策 |
| Product Brief 后 | 检查产品范围、用户角色、权限、术语是否形成长期约束 |
| Work Breakdown / Feature Split 前 | 检查一个 requirement 是否会拆多个 feature，以及是否需要共同决策 |
| Feature Spec 前 | 检查 spec 是否必须引用已有 project decisions，或是否有新 decision 需要先确认 |
| Technical Design / Code Context | 检查实现方案是否引入新边界、依赖、存储、接口、状态协议 |
| Plan Gate 前 | 确认 plan 没有绕过未接受的 decision |
| Drift Check / Close Feature | 检查实现是否改变了长期项目事实，是否需要补写或更新 decision 引用 |

## ADR 建议触发条件

Agent 应该建议创建 project-level decision file，当发现以下任一情况：

| 触发信号 | 为什么需要记录 |
|---|---|
| 一个 requirement 会拆成多个 feature，并共享同一技术/流程约束 | 避免每个 feature 重复解释同一个取舍 |
| 决策影响多个 feature 或未来需求 | 需要长期可追溯 |
| 新增或改变架构边界、模块边界、数据边界、运行边界 | 后续改动需要知道边界为何存在 |
| 引入新依赖、存储方式、协议、队列、事件、外部服务 | 这些选择会带来维护成本 |
| 改变 artifact ownership 或 agent-loop 阶段规则 | 影响未来 Agent 如何工作 |
| 出现多个合理方案，且选择会排除其他路线 | 需要记录 alternatives 和 trade-offs |
| 人类明确问“为什么这么做”或“以后怎么判断” | 说明决策需要沉淀 |

不建议创建 ADR 的情况：

| 场景 | 推荐记录方式 |
|---|---|
| 单个 feature 内部的小实现选择 | `spec.md` 的 `Design Decisions` |
| 临时 workaround | `notes.md`，必要时后续提升 |
| 普通 bugfix 或小配置调整 | `notes.md` 或 task evidence |
| 没有长期影响的 UI 文案、布局、小型交互 | `spec.md` |
| 已有 accepted decision 完全覆盖 | 只引用已有 decision |

## Human Gate

创建、接受、废弃 project-level decision 都应该是 Human-gated。

Agent 可以自主执行：

- 发现可能的 decision point；
- 在阶段总结中建议创建 ADR；
- 草拟 decision 文件；
- 在 requirement README / feature spec 中建议引用。

Agent 不应静默执行：

- 把草案 decision 标记为 accepted；
- 创建会约束未来 feature 的 project decision；
- 修改 accepted decision 的含义；
- 删除或重编号旧 decision；
- 把 feature-local 小决策升级成 project-level 约束。

## Decision And Design 模板草案

这里的文件不应该只是传统 ADR 的简短结论，而应该记录一条完整推导链：

```text
需求与目标
→ 业务概念定义
→ 主体业务流程
→ 关键决策
→ 架构与数据设计
→ 稳定性 / 高可用 / 性能 / 一致性 / 闭环验证
```

换句话说，它既是 decision record，也是 architecture design record。它回答的不只是“选了什么”，还要回答“为什么这个设计能满足需求目标，以及如何证明它满足”。

```md
# ADR-0001: <decision and design title>

Status: proposed | accepted | superseded | deprecated
Created: YYYY-MM-DD
Scope: project | cross-feature | feature
Triggered By:
- .agent-loop/requirements/<set>/
- .agent-loop/features/<feature>/spec.md

## 1. Requirement And Decision Context

这个决策来自什么需求、业务目标、项目现状或技术约束。

| Item | Description |
|---|---|
| Source Requirement | <requirement path / summary> |
| Current Project State | <当前项目实现、限制、历史包袱> |
| Problem To Solve | <这次必须解决的问题> |
| Decision Needed | <现在需要拍板的设计问题> |
| Affected Features | <受影响的 feature 或未来能力> |

## 2. Goals And Non-Goals

目标必须能约束后续设计。涉及性能、可用性、一致性、成本、扩展性时，要尽量给出可验证口径。

| Goal | Target / Meaning | Verification |
|---|---|---|
| <业务目标> | <目标描述> | <如何证明满足> |
| <一致性目标> | <例如不允许余额扣穿> | <事务测试 / 对账> |
| <性能目标> | <例如 P95 latency / TPS> | <压测 / 指标> |
| <高可用目标> | <例如单点失败后的行为> | <故障演练 / 降级策略> |

Non-Goals:
- <本次明确不解决什么>
- <哪些能力留到后续 ADR / feature>

## 3. Domain Concepts

先定义业务概念，再设计表和流程。每个关键概念都要说明事实源。

| Concept | Definition | Responsibility | Source Of Truth |
|---|---|---|---|
| <概念> | <业务含义> | <负责什么> | <表 / 外部系统 / ledger / provider> |

## 4. Business Flow

从用户或外部系统视角描述主体业务流程。这里先讲业务发生了什么，不急着讲代码怎么写。

```text
Step 1
→ Step 2
→ Step 3
→ Final state
```

关键流程表：

| Step | Actor | Action | State Change | Failure / Compensation |
|---|---|---|---|---|
| 1 | <actor> | <action> | <state> | <failure handling> |

## 5. Options Considered

方案比较必须围绕目标，而不是泛泛比较优缺点。

| Option | Design Summary | Meets Goals | Advantages | Disadvantages | Decision |
|---|---|---|---|---|---|
| A | <方案摘要> | <满足/不满足哪些目标> | <优势> | <缺点> | chosen/rejected |
| B | <方案摘要> | <满足/不满足哪些目标> | <优势> | <缺点> | chosen/rejected |

## Decision

明确最终采用的业务和技术设计。

```text
We will ...
```

## 6. Architecture Design

说明架构如何支撑业务主体流程。这里要把组件、数据、事务边界、异步边界讲清楚。

### 6.1 Component Responsibilities

| Component | Responsibility | Owns | Does Not Own |
|---|---|---|---|
| <component> | <职责> | <数据/行为> | <不负责什么> |

### 6.2 Data Model

| Data Object | Purpose | Key Fields | Invariant |
|---|---|---|---|
| <table/model> | <用途> | <关键字段> | <必须保持的规则> |

### 6.3 Transaction And Consistency Boundaries

| Boundary | In Transaction | Outside Transaction | Consistency Model |
|---|---|---|---|
| <operation> | <同步事务内完成> | <异步副作用> | strong / eventual |

### 6.4 Idempotency And Concurrency

| Scenario | Idempotency Key | Concurrency Control | Expected Behavior |
|---|---|---|---|
| <场景> | <key> | <DB lock / unique index / queue> | <结果> |

## 7. Non-Functional Design

这一节说明架构如何满足稳定性、高可用、性能、一致性、安全、可观测性和成本目标。

| Concern | Design | Trade-off | Verification / Metric |
|---|---|---|---|
| Stability | <如何避免异常扩散> | <代价> | <验证方式> |
| High Availability | <如何降级/重试/恢复> | <代价> | <验证方式> |
| Performance | <如何满足延迟/吞吐> | <代价> | <指标> |
| Data Consistency | <强一致/最终一致策略> | <代价> | <对账/测试> |
| Security / Risk | <权限/风控/防重复> | <代价> | <审计/测试> |
| Observability | <日志/指标/追踪/告警> | <代价> | <dashboard/alert> |

## 8. Closure And Verification Plan

说明这个设计如何闭环。没有验证计划的 decision 不能算完整。

| Requirement / Goal | Verification Method | Evidence Location |
|---|---|---|
| <目标> | <测试 / 压测 / 对账 / 监控 / 演练> | <tests.md / notes.md / dashboard> |

Required evidence before close:
- <必须完成的验证>
- <必须记录的对账或监控证据>

## 9. Consequences

Positive:
- <这个设计让什么变得更可靠、更清晰或更可扩展>

Negative:
- <这个设计增加了什么复杂度、成本或限制>

Operational Burden:
- <运行、监控、修复、迁移上的代价>

Open / Follow-up:
- <需要后续 ADR、feature 或验证继续闭环的内容>

## 10. References

- Requirement:
- Feature:
- Related decisions:
- Related project memory:
```

## 与 v1.2.x 现有设计的关系

这份 proposal 应保持轻量，不引入 complex ADR system。

它只增加一条可选 lane：

```text
Requirement
→ Decision Scan
→ Decision Placement
→ Feature Spec
→ Tasks / Tests / Plan
→ Implementation
→ Drift Check
```

其中：

```text
Decision Scan = 阶段检查。
Decision Placement = 决定写在 spec.md、notes.md，还是建议 decisions/*.md。
decisions/*.md = 只有长期/跨 feature 决策才创建。
```

## 待讨论问题

- 顶层目录应命名为 `decisions/` 还是 `adr/`？
- 是否需要在 simple memory mode 下限制 `decisions/` 的创建门槛？
- 是否需要 requirement README 的固定 `Applicable Project Decisions` 字段？
- feature spec 的 `Applicable Decisions` 是否应成为标准字段？
- accepted decision 是否需要 supersede 机制和编号规则？
- 后续是否需要独立 `references/project-decisions.md`？
