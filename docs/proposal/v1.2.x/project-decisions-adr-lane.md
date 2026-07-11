# Proposal: Decision & Design / ADR Lane

状态：Decision & Design 增强版已实施
目标版本：v1.2.4
创建时间：2026-06-16

实施说明：v1.2.4 已将 Decision & Design / ADR Lane 落到 `references/project-decisions.md`、`templates/decision.md`、stage guidance、workflow checklist、README、Usage 和验证脚本，并补充 Design Readiness、Design Slice Coverage 与实现一致性检查。本文保留为设计背景和后续扩展讨论。

## 目的

这份 proposal 先讨论 `agent-loop` 中项目级决策记录的目录规范、介入时机、上游输入和技术设计内容。

它暂不定义完整 ADR 方法论，也不要求所有需求都创建 ADR。当前目标是先把这些问题收敛清楚：

- 项目级长期决策放在哪里；
- requirement、feature、project memory 如何引用这些决策；
- 什么情况下 Agent 应该建议创建 ADR；
- 在 agent-loop 哪些边界执行 Design Readiness，并何时进入 Decision & Design；
- Product Brief / PRD / `to-prd` 输出如何作为 Decision & Design 输入；
- Decision / ADR 中技术设计部分应该覆盖什么；
- feature-local 小决策什么时候直接写进 `spec.md`，什么时候升级为独立 ADR。

## 核心观点

```text
Design Readiness Check 是 Requirement 进入 feature construction 前的必选方法。
Decision Scan / Placement 是 Decision & Design 阶段内部的分流方法。
Decision File / ADR 全局可选；当共享设计是需求落地前提且没有 accepted decision 覆盖时，它是有条件必需的 Human-gated 产物。
决策记录应该放在它影响范围的最小稳定层级。
```

更具体地说，ADR 是 requirement 和 feature 之间的设计桥梁：

```text
Requirement -> Design Readiness Check -> Decision & Design If Needed -> Feature Mapping -> Product Brief / Feature Spec
```

Requirement 说明人类要什么以及如何验收；Decision & Design 说明完整业务如何闭环、共享领域与数据规则如何成立、架构如何支撑目标；Feature 只实现并验证被分配的 Design Slice。

这里的触发条件不要求存在技术争议。一个 requirement 只要会拆成多个 feature，或需要共享业务流程、状态机、事实源、一致性、恢复、性能、高可用、安全、可观测性设计，就应该进入 Decision & Design。

ADR 不是 feature spec 的替代品，也不是 project memory 的替代品。

同时，first-version exclusion 仍然禁止 complex ADR system。本 proposal 只定义一条轻量 Decision Lane：它允许 Agent 识别、建议、草拟和引用长期决策，但不要求每个需求、每个 feature 或每个技术选择都创建 ADR。

| 对象 | 主要职责 | 不负责 |
|---|---|---|
| `requirements/<set>/` | 保存人类原始需求材料和来源索引 | 不承载可变工程设计 |
| `features/<feature>/spec.md` | 记录 feature 行为、约束、验收标准和轻量设计决策 | 不承载跨 feature 的长期项目决策 |
| `project.md` | 当前工作状态、长期记忆入口、enterprise memory 索引 | 不成为完整决策历史库 |
| `project/*.md` | enterprise mode 下的长期事实分片 | 不解释每个事实当初为什么成立 |
| `.agent-loop/decisions/*.md` | 记录跨 feature / 长期项目决策的原因、取舍、结果 | 不记录普通执行日志 |

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

`.agent-loop/decisions/` 是 simple 和 enterprise memory mode 都可使用的一等长期 artifact，不属于 enterprise-only `project/` memory 分片。

它和 `project.md`、`project/*.md` 的职责不同：

```text
project.md = 当前状态、入口索引、memory 路由。
project/*.md = enterprise mode 下的当前长期事实和导航。
decisions/*.md = 为什么形成这些事实和约束。
```

因此 `.agent-loop/decisions/` 可以在 simple memory mode 和 enterprise memory mode 下使用。创建 `decisions/` 不应自动触发 enterprise mode；enterprise mode 仍只由 `project.md` 可读性、项目复杂度、边界数量等 memory trigger 决定。

## 决策放置规则

决策记录按影响范围放置：

| 决策范围 | 推荐位置 | 示例 |
|---|---|---|
| 只影响当前 feature，且取舍简单或中等复杂 | `features/<feature>/spec.md` 的 `Design Decisions` | 某个交互、内部实现选择、单 feature 状态机 |
| 来自某个 requirement，影响多个 feature | 优先 `.agent-loop/decisions/`，requirement README 只引用 | 需求拆分策略、统一工作流约束 |
| 影响长期项目结构、边界、依赖、工作流 | `.agent-loop/decisions/` | artifact ownership、技术栈、数据存储、跨 feature 规则 |

第一版只正式支持两类决策记录：

```text
1. feature-local 小决策写入 `features/<feature>/spec.md` 的 `Design Decisions`。
2. project / cross-feature 长期决策写入 `.agent-loop/decisions/*.md`。
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

## Design Readiness Check

Design Readiness Check 不是独立 stage，而是 Requirement Archive、Product Brief、Feature Spec 边界上的必选检查。它判断 Requirement 是否已经具备直接进入 feature construction 的条件，还是需要先形成跨 feature 的整体落地设计。

| 检查信号 | 进入 Decision & Design 的原因 |
|---|---|
| 一个 requirement 会拆成多个 feature | 需要共享蓝图，不能让 feature 各自发明规则 |
| 需要端到端业务闭环 | 独立 story 通过不代表整体流程闭环 |
| 共享领域概念、状态机、事实源或不变量 | 多个 feature 必须使用同一语义 |
| 涉及事务、一致性、并发、幂等、补偿、对账或恢复 | 异常行为跨越 feature 边界 |
| 有性能、高可用、安全、成本、审计、可观测性目标 | 目标需要分配 owner 和验证路径 |
| 新增跨系统或长期边界 | 后续 feature 必须继承同一约束 |

检查输出写入 requirement README：`design-not-needed`、`candidate`、`required` 或 `completed`，并记录触发信号、共享设计问题、推荐阶段、decision records 和 coverage status。

## Decision & Design / ADR 介入时机

Decision & Design 不应等 feature story 或技术实现已经拆完才介入。更合适的规则是：

```text
需求沟通 / 产品目标成形
→ 记录 Design Readiness evidence / Decision Candidates
→ 产品文档 / requirement README / product.md 明确
→ Design Readiness Check
→ Decision & Design If Needed
→ Feature Mapping / Design Slice Coverage
→ Product Brief / Feature Spec
→ Technical Design / Code Context
→ 新信号则回到 Design Readiness / Decision & Design
→ Plan Gate 前
→ Design Slice Coverage 检查
→ Implementation
→ Review / Drift Check / Feature Completion Check
```

核心原则：

```text
Design Readiness 早介入，Decision File 在 Requirement 被接受且共享设计需要长期记录时创建。
```

含义：

- 在需求沟通、产品目标成形时，Agent 就应该开始扫描长期决策信号。
- 在 requirement README / product.md / PRD 明确后，Agent 才判断是否需要创建 `.agent-loop/decisions/*.md`。
- 在 Feature Spec 前，如果不先确定共同约束会导致多个 feature 各写各的，应建议创建 decision file。
- 在 Technical Design / Code Context 或 Plan Gate 前，如果技术设计引入长期边界、依赖、存储、协议、一致性模型、并发控制或运行约束，应再次扫描。
- 在 Drift Check / Close Feature 时，如果实现改变了长期事实，应建议补写 decision、更新引用，或回补 project memory。

Decision Scan 是一个轻量检查，不等于创建 ADR。

建议在这些阶段触发：

| 阶段 | 行为 |
|---|---|
| 需求沟通 / 产品目标成形 | 检查需求是否可能触发跨 feature、长期项目约束或业务概念定义 |
| Requirement Intake / Archive 后 | 检查 requirement README 是否需要引用已有 decisions，或记录 triggered decisions |
| Product Brief / PRD / `product.md` 后 | 检查产品范围、用户角色、权限、术语、业务流程是否形成长期约束 |
| Work Breakdown / Feature Split 前 | 检查一个 requirement 是否会拆多个 feature，以及是否需要共同决策 |
| Feature Spec 前 | 检查 spec 是否必须引用已有 project decisions，或是否有新 decision 需要先确认 |
| Technical Design / Code Context | 检查实现方案是否引入新边界、依赖、存储、接口、状态协议 |
| Plan Gate 前 | 确认 plan 没有绕过未接受的 decision |
| Drift Check / Close Feature | 检查实现是否改变了长期项目事实，是否需要补写或更新 decision 引用 |

## Decision & Design Inputs

Decision & Design 应从多个上游来源读取需求落地和候选决策信号，而不是只看 feature spec。Decision Scan / Placement 只负责在阶段内部决定稳定归属。

| Input | 读取什么 | 输出倾向 |
|---|---|---|
| requirement README | 人类目标、Delivery Phases、scope、out of scope、source index | 是否需要共同约束或引用已有 decision |
| product.md / PRD | Problem、Solution、User Stories、Out of Scope、Product Decisions | 是否存在跨 feature 产品约束或业务流程决策 |
| to-prd `Implementation Decisions` | 模块、接口、架构、schema、API、交互等候选实现决策 | 进入 Decision Candidate Routing |
| to-prd `Testing Decisions` | 外部行为测试、关键模块测试、先例测试 | 进入 `tests.md` 或 decision verification plan |
| feature spec draft | added/modified/removed behavior、acceptance、edge cases | 是否需要引用 existing decisions 或补充 design decisions |
| Technical Design / Code Context | 边界、依赖、存储、事务、协议、状态、一致性 | 是否需要 project-level decision |
| current project memory | `project.md`、enterprise `project/*.md`、Domain Language、boundaries | 是否已有长期事实或需要回补 |
| existing decisions | `.agent-loop/decisions/*.md` | 是否已有 accepted decision 覆盖 |

## Decision Candidate Routing

`to-prd` 的 `Implementation Decisions` 和 `Testing Decisions` 不能直接等同于 ADR。它们是候选输入，需要分流。

| Candidate | Destination | Rule |
|---|---|---|
| Product-level decision | `product.md` | 只影响产品范围、用户价值、角色、非目标，不形成工程长期约束 |
| Feature-local implementation decision | `spec.md` 的 `Design Decisions` 或 `plan.md` | 只约束当前 feature，未来可改，或没有跨 feature 影响 |
| Cross-feature or long-term architecture decision | `.agent-loop/decisions/*.md` | 跨 feature、长期、难逆转、有真实 trade-off，或未来读者会问为什么 |
| Testing decision | `tests.md`；必要时同步到 decision verification plan | 描述如何证明需求、流程或架构目标满足 |
| Human-gated question | 阶段总结 / Human Review Summary | 影响范围、目标、方案或风险尚不清楚 |

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

## Design Slice Coverage

Decision & Design 不能只被 feature 引用，还必须证明整体设计已经被 feature 完整承接。

每个会产生实现工作的业务流程步骤、不变量、恢复责任和非功能目标都分配稳定 ID：`DS-01`、`DS-02`、`DS-03`。Decision record 保存反向覆盖表：

| Design Slice ID | Required Capability / Rule | Owning Feature(s) | Verification | Coverage Status |
|---|---|---|---|---|
| DS-01 |  |  |  | unassigned / planned / implemented / verified / deferred / out-of-scope |

进入 Feature Spec 前，所有 required slice 必须至少有一个 planned owner；feature `spec.md` 必须在 `Implements Decisions` 中引用被分配的 Design Slice ID。`Applicable Decisions` 只证明 feature 知道这个约束，不能证明它已经承接实现责任。

Review、Drift Check 和 Feature Completion Check 继续验证 Design Slice 的实现与证据。任何偏离 accepted design 的实现都必须回到 Decision & Design 或 superseding decision，不能只凭本地 story 测试通过就 close。

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

## 技术设计部分

Decision / ADR 中的技术部分不应该只写“用了什么技术”。它应该说明技术设计如何支撑业务目标、业务流程和关键决策。

技术设计至少应覆盖：

| 模块 | 要回答的问题 |
|---|---|
| 技术选型 | 用什么数据库、缓存、队列、事务机制、锁、框架、外部服务，为什么 |
| 架构组件 | 有哪些组件，各自负责什么，不负责什么 |
| 数据模型 | 哪些表、对象、事件是事实源，关键字段和约束是什么 |
| 接口 / 协议 | 服务之间、前后端之间、外部系统之间如何交互 |
| 事务边界 | 哪些操作必须在一个事务里，哪些可以异步 |
| 一致性模型 | 强一致、最终一致、对账补偿分别用在哪里 |
| 并发控制 | 如何避免重复提交、扣穿、乱序、竞态 |
| 幂等设计 | 重试、回调、消息消费、支付通知如何幂等 |
| 失败恢复 | 超时、中断、部分成功、外部服务失败后怎么恢复 |
| 性能设计 | 延迟、吞吐、热点、索引、缓存、批处理、限流 |
| 高可用设计 | 降级、重试、熔断、隔离、任务补偿 |
| 安全 / 风控 | 权限、签名、防重放、敏感数据、审计 |
| 可观测性 | 日志、指标、trace、告警、对账报表 |
| 验证计划 | 单测、集成测试、压测、故障演练、对账验证 |

对于充值、支付、钱包、token 实时扣费这类设计，技术部分必须能回答：

- 余额事实源在哪里；
- 流水是否 append-only；
- 扣费是预冻结、后扣，还是组合模式；
- LLM 请求前如何检查余额；
- LLM 返回后如何按 token 计算费用并扣费；
- 中途失败如何补偿；
- 钱包扣完如何停止服务；
- 对账如何证明数据库数目准确；
- 高并发下如何避免扣穿；
- 外部支付回调如何幂等。

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
Scope: project | cross-feature
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

## 6. Technical Architecture Design

说明技术设计如何支撑业务主体流程。这里要把技术选型、组件职责、数据事实源、接口协议、事务边界、一致性、并发幂等、失败恢复讲清楚。

### 6.1 Technology Choices

| Area | Choice | Why | Alternatives Rejected | Risk |
|---|---|---|---|---|
| <database/cache/queue/provider> | <chosen technology> | <why it satisfies goals> | <rejected options> | <risk / mitigation> |

### 6.2 Component Responsibilities

| Component | Responsibility | Owns | Does Not Own |
|---|---|---|---|
| <component> | <职责> | <数据/行为> | <不负责什么> |

### 6.3 Data Model And Source Of Truth

| Data Object | Purpose | Source Of Truth | Key Fields | Invariant |
|---|---|---|---|---|
| <table/model/event> | <用途> | <DB / ledger / provider / event stream> | <关键字段> | <必须保持的规则> |

### 6.4 Interfaces And Protocols

| Interface | Producer | Consumer | Contract | Failure / Retry |
|---|---|---|---|---|
| <API/event/callback/job> | <producer> | <consumer> | <request/event/schema> | <failure behavior> |

### 6.5 Transaction And Consistency Boundaries

| Boundary | In Transaction | Outside Transaction | Consistency Model |
|---|---|---|---|
| <operation> | <同步事务内完成> | <异步副作用> | strong / eventual |

### 6.6 Idempotency And Concurrency

| Scenario | Idempotency Key | Concurrency Control | Expected Behavior |
|---|---|---|---|
| <场景> | <key> | <DB lock / unique index / queue> | <结果> |

### 6.7 Failure Recovery And Compensation

| Failure | Detection | Recovery / Compensation | Owner | Evidence |
|---|---|---|---|---|
| <failure mode> | <logs/metric/job/query> | <retry/release/rollback/reconcile> | <component/team> | <test/runbook/alert> |

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

它只增加一条条件触发的轻量 lane：

```text
Requirement
→ Design Readiness Check
→ Decision & Design If Needed
→ Feature Mapping / Design Slice Coverage
→ Feature Spec
→ Tasks / Tests / Plan
→ Implementation
→ Drift Check
```

其中：

```text
Design Readiness Check = Requirement 进入 feature construction 前的必选方法。
Decision & Design = 形成跨 feature 的业务与架构落地蓝图。
Decision Scan / Placement = 阶段内部决定内容写在 product/spec/tests/notes，还是建议 decisions/*.md。
decisions/*.md = 当共享设计需要长期记录且没有 accepted decision 覆盖时，在 Human Gate 后创建。
```

## 与 grill-with-docs / to-prd 的关系

`grill-with-docs` 和 `to-prd` 都适合作为 Decision / ADR 的上游，但职责不同：

```text
grill-with-docs = 问清楚领域语言、业务场景和边界。
to-prd = 将已知上下文合成为 product.md / PRD-like Product Brief。
Decision & Design / ADR = 把复杂 Requirement 推导为跨 feature 的业务闭环、领域/数据规则、架构、恢复、非功能目标和可验证设计。
```

建议组合：

| 工具 / 阶段 | 主要作用 | 写入 agent-loop |
|---|---|---|
| grill-with-docs | 拷问术语、场景、边界、领域模型冲突 | requirement README、product.md、project.md Domain Language 候选 |
| to-prd | 从已知上下文合成 Problem、Solution、User Stories、Implementation Decisions、Testing Decisions | `product.md`，并把共享设计信号交给 Design Readiness |
| Design Readiness Check | 判断 Requirement 是否可直接进入 feature construction | requirement README summary、recommended next stage |
| Decision Scan / Placement | 在 Decision & Design 内判断候选内容的稳定归属 | Human Review Summary、decision draft、feature-local placement |
| Decision & Design / ADR | 记录跨 feature 的业务与技术落地蓝图、Design Slice Coverage 和验证链路 | `.agent-loop/decisions/*.md` |

注意：

- `to-prd` 默认发布 issue tracker 的行为不应直接照搬；agent-loop 应将内容翻译到 `product.md`，除非人类明确要求发布 issue。
- `grill-with-docs` 默认写 `CONTEXT.md` / `docs/adr/` 的路径不应直接照搬；agent-loop 应把领域语言写入 requirement / product / project memory，把长期决策写入 `.agent-loop/decisions/`。
- `Implementation Decisions` 不是 accepted ADR；它们只是 Design Readiness / Decision & Design 输入。
- `Testing Decisions` 优先进入 `tests.md`，只有当它用于证明长期设计目标时才同步到 decision verification plan。

## 待讨论问题

- 是否需要在 simple memory mode 下限制 `decisions/` 的创建门槛？
- requirement README 的固定 `Applicable Decisions` / `Triggered Decisions` 字段已在轻量版实施，后续可观察是否过重。
- feature spec 的 `Applicable Decisions` / `Implements Decisions` / `Design Decisions` 已成为标准字段，后续可观察是否需要裁剪。
- accepted decision 是否需要 supersede 机制和编号规则？
- 独立 `references/project-decisions.md` 已实施。
