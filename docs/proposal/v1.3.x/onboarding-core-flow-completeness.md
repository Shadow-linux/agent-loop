# Proposal: Onboarding Core Flow Completeness

状态：待人类评审

目标版本：v1.3.0

创建时间：2026-07-11

## 摘要

当前 Evidence-Graph + DDD Onboarding 已经对单篇 Module / Flow 文档提出较强的内容要求，包括架构/边界图、状态图、Timeline / 时序图、数据对象、状态变化、失败路径、排障和代码证据。

现有缺口位于更上游：Agent 可以把“已经选中的流程”写得很详细，却没有足够强的机制证明项目核心流程已经找全、关键阶段和异常分支已经拆全。若 Evidence Graph 只发现“创建订单”，但漏掉支付回调、重复回调、超时关闭、退款、补偿和对账，后续文档即使结构完整，也会在错误的范围内显得详细。

本 proposal 建议在现有 onboarding 顺序和两个 Human Gate 不变的前提下，引入三项能力：

1. `Core Flow Inventory`：在 Evidence Graph 阶段建立带业务关键度、终态、变体、异步链路和恢复责任的核心流程清单。
2. `Flow Slice Coverage`：把每个核心流程拆成可追踪的主路径、分支、失败和恢复 slice，并映射到代码证据、图和文档章节。
3. 产物级语义验证：使用完整示例、缺陷样本和压力场景验证“有没有漏”，不再只验证模板中是否存在标题和关键词。

预期结果：

```text
发现完整的核心流程
→ 选择并解释文档范围
→ 将流程拆成可追踪 slice
→ 用互补图组表达结构、时间、状态和恢复
→ 按 slice 验证覆盖
→ 才允许标记 newcomer-ready
```

## 背景与问题定义

### 当前已经做得好的部分

现有 Flow 文档要求已经覆盖：

- 业务目标、触发入口、参与模块、前置状态和成功结果；
- 架构/边界图；
- ASCII 状态机/决策图；
- Timeline / 时序图；
- 阶段、数据流转和状态变化；
- 示例、失败路径、排障路径、变更指南和代码证据；
- consistency、idempotency、transaction、compensation、reconciliation 等高风险内容。

因此，本轮不需要推翻 Flow 模板，也不需要以增加文件数量来解决问题。

### 当前结构性缺口

#### 1. 核心流程发现没有完整性契约

当前 `Flow Candidates` 可以记录 trigger、participants、state changes、external dependencies、evidence 和 risk，但不能稳定回答：

- 这是核心流程、支持流程，还是局部调用链；
- 业务成功终态和失败终态分别是什么；
- 是否存在同步、异步、回调、job 或人工恢复变体；
- 哪些外部副作用必须发生，哪些允许最终一致；
- 为什么该流程进入 Flow Plan，或为什么可以延期；
- 入口、状态写点、消息消费者和终态是否形成闭合证据链。

#### 2. 上游漏项会在后续阶段被继承

Onboarding Spec 和 Onboarding Tasks 只会规划已经进入候选清单的流程。如果 Evidence Graph 漏掉回调、补偿或对账，后续的 Diagram Plan、Flow 文档和 Coverage Matrix 都无法自动恢复该细节。

#### 3. Topic 级评分会掩盖 slice 级缺失

当前评分以 topic 为单位。某篇 Flow 文档可以在图、可读性和代码证据上得到较高平均分，同时漏掉一个业务关键失败分支。关键分支缺失不应被其他维度的高分抵消。

#### 4. 机械测试不能证明生成产物完整

现有 onboarding 测试主要检查 source、template 和 scenario 中是否存在指定文字或章节。它能够防止规则被误删，但不能证明实际生成的 onboarding：

- 找全了核心流程；
- 覆盖了所有关键终态；
- 图和正文对应真实代码路径；
- 没有用泛化描述填满必填章节。

#### 5. Review 维度存在漂移

`coverage-matrix.md` 分开评分 architecture、state、timeline 等维度，而 `batch-review.md` 使用较粗的 `Wireframe` 列。两套评分口径不一致，会让 review 丢失图解和流程 slice 的具体缺口。

## 目标

本 proposal 的目标是：

1. 让 Agent 在写正式文档前证明核心流程发现足够完整。
2. 让每个核心流程的主路径、分支、失败和恢复都能追踪到代码证据。
3. 让图解承担明确职责，避免一张泛化 flowchart 同时冒充架构、时序和状态说明。
4. 让关键 slice 缺失成为 hard blocker，不能被平均分掩盖。
5. 让验证覆盖真实产物和故意不完整的反例。
6. 保留现有 Onboarding Spec Acceptance Gate 和 Full Execution Gate，不增加第三个人类 Gate。
7. 保持 Module / Flow 默认单长文件，不通过拆文件制造详细感。
8. 只对 `critical` / `important` 核心流程强制 Flow/Slice/Diagram 追踪；supporting flow 和非流程文档保持轻量。

## 非目标

本轮不做以下事情：

- 不改变 Project Entry Scan 与 onboarding-db 的边界；
- 不改变 `Evidence Graph -> Onboarding Spec -> Onboarding Tasks -> formal docs` 的阶段顺序；
- 不增加每个 batch 的人类确认；
- 不要求所有流程使用所有图类型；
- 不要求 glossary、静态配置清单、纯索引或无状态主题编造状态图；
- 不要求固定数量的核心流程或固定数量的图；
- 不从目录名自动推断业务流程；
- 不要求 Agent 生成网站或图片文件；Markdown 中的 Mermaid 和 ASCII 仍是 source of truth；
- 不在本轮建设通用 LLM 自动评审平台；该能力可与未来 self-test harness 对接；
- 不把历史 proposal 或示例升级为运行时 source of truth。

## 方案比较

### 方案 A：只增强 Flow 模板

做法：在 `flow.md` 增加更多章节、表格和自检项。

优点：改动小，容易实施。

限制：无法解决 Evidence Graph 上游漏项；Agent 仍可能把一个不完整范围写得很详细。

### 方案 B：核心流程契约 + Slice Traceability

做法：增强 Evidence Graph、Onboarding Spec、Flow 文档、Coverage 和 Review 的贯通关系；以稳定 Flow ID 和 Slice ID 建立追踪链。

优点：直接处理核心流程发现不完整和关键分支丢失；与现有 Evidence-Graph + DDD 模型兼容；不需要新增 Human Gate。

代价：需要同步多份 reference、template、scenario 和 test，并执行全量验证。

### 方案 C：自动生成静态调用图

做法：扫描 AST、调用关系、数据库访问和消息消费者，自动生成候选流程图。

优点：能提高代码入口和调用链发现效率。

限制：静态调用图通常不知道业务目标、终态、补偿责任和人工恢复语义；多语言项目还需要不同解析器。它适合作为 Evidence Graph 的辅助证据，不适合作为第一版完整性判定源。

### 推荐

采用方案 B。方案 A 可作为方案 B 中的模板改动部分；方案 C 延后为可选 Evidence Adapter，不阻塞 v1.3.0。

## 设计

### 1. Core Flow Inventory

Evidence Graph 在普通 `Flow Candidates` 之上增加核心流程分类和选择信息。推荐表结构：

| 字段 | 含义 |
|---|---|
| Flow ID | 稳定标识，例如 `CF-ORDER-PAYMENT` |
| Flow | 人类可读流程名 |
| Business Outcome | 流程为用户或业务产生的结果 |
| Criticality | `critical`、`important`、`supporting` |
| Trigger / Entry | 外部触发与具体代码入口 |
| Success Terminal | 成功终态和可观察结果 |
| Failure Terminals | 失败、取消、未知、人工处理等终态 |
| Variants / Branches | 同步、异步、回调、降级和业务分支 |
| Participants / Owners | 模块、服务、外部系统和真相所有者 |
| State / Data Owners | 核心状态对象和数据 owner |
| Async / Jobs / Callbacks | Topic、consumer、job、callback 关系 |
| External Side Effects | 扣款、通知、发货、配额、第三方调用等 |
| Recovery Responsibility | retry、compensation、reconciliation、manual action |
| Evidence Chain | 入口、关键写点、消息处理和终态证据 |
| Selection | `planned`、`deferred`、`not-applicable` |
| Selection Reason | 纳入或延期原因 |
| Confidence / Unknowns | 置信度和仍需确认的事实 |

#### 发现方法

Agent 不应只从目录和入口函数生成 Flow Inventory。至少从以下证据方向交叉发现：

1. API、CLI、UI action、webhook、consumer、cron/job 等入口；
2. 核心实体、订单、任务或会话的状态写入点；
3. DB transaction、Redis/Lua、outbox、MQ publish/consume 等副作用；
4. callback、retry、DLQ、compensation、reconciliation 和人工恢复入口；
5. tests、fixtures、API contracts、logs、config 和 runbook 中的真实行为；
6. 项目记忆或人类说明中的业务结果，并用代码现实复核。

#### Core Flow Selection Gate

不新增独立 Human Gate。现有 Spec Acceptance Gate 增加以下检查：

- 每个 `critical` / `important` Flow Candidate 都已进入 Flow Plan，或有具体 deferred reason；
- 每个计划内核心流程都列出成功终态、失败终态和已知变体；
- 入口、关键状态写点、异步处理和终态已形成 Evidence Chain；
- 无证据的推断保留在 Unknowns，不伪装成已确认流程。

人类确认 Onboarding Spec 时，同时确认这份核心流程选择结果。Full Execution Gate 仍只负责确认具体输出、证据要求和执行范围。

### 2. Flow Slice Coverage

每个计划内 `critical` / `important` 核心流程在 Onboarding Spec 或 Flow 文档中建立 slice 清单。Slice 是一个可验证的主路径阶段、业务分支、失败点或恢复动作，不是文档章节数量。`supporting` flow 只有在改变核心状态、产生关键副作用或承担恢复责任时才升级为完整 slice 追踪；否则可保留轻量 Flow Candidate 和证据说明。

推荐结构：

| 字段 | 含义 |
|---|---|
| Flow ID / Slice ID | 例如 `CF-ORDER-PAYMENT/S07` |
| Path Kind | `main`、`branch`、`failure`、`recovery` |
| Trigger / Precondition | 进入该 slice 的条件 |
| Owner | 执行和状态责任模块 |
| Input / Output | 输入和输出对象 |
| Action | 真实行为 |
| State Read / Written | 读取和写入的状态 |
| Transition | before、trigger、after |
| Sync / Async / External | 调用性质和外部副作用 |
| Failure Result | 本 slice 失败后的可观察结果 |
| Recovery | retry、rollback、compensation、reconciliation 或 manual action |
| Evidence | 文件、符号/配置键和调用/数据方向 |
| Diagram IDs | 该 slice 出现在哪些图中 |
| Document Section | 该 slice 在正文中的讲解位置 |
| Coverage Status | `covered`、`inferred`、`blocked` |

追踪链必须闭合：

```text
Core Flow Inventory
  → Flow Plan
  → Onboarding Task
  → Flow Slice Coverage
  → Diagram IDs + narrative sections
  → Code Evidence
  → Coverage Matrix + Batch Review
```

关键 slice 定义：

- 改变核心业务状态；
- 产生不可忽略的外部副作用；
- 决定成功、失败、取消、未知或人工处理终态；
- 承担 retry、compensation、reconciliation 或安全责任；
- 涉及 transaction、lock、idempotency、quota、billing、credential 或权限边界。

任何关键 slice 为 `blocked` 或缺少 Evidence / Diagram / Document Section 映射时，对应 Flow 不能标记 `newcomer-ready`。

### 3. 图解表达规则

#### Critical / Important 核心 Flow 的默认图组

| 图 | 默认性 | 主要回答的问题 |
|---|---|---|
| Core Flow Overview / Branch Map | 必填 | 核心流程有哪些主干、分支、异步出口和终态 |
| Timeline / Sequence Diagram | 必填，正文主图 | 谁在什么时间调用谁、传什么数据、读写什么状态 |
| ASCII State Machine / Decision Diagram | 必填 | 状态如何变化、哪些转换非法、失败后如何恢复 |
| Architecture / Boundary Diagram | 必填，可与全景图合并但职责必须清楚 | 流程跨越哪些模块、服务、数据和外部系统边界 |

架构/边界图可以与 Core Flow Overview 合并，但合并图必须同时显示：

- 模块/系统边界；
- 数据或状态 owner；
- 主路径、关键分支和终态；
- DB、cache、MQ、gateway 和外部依赖的位置。

Timeline / Sequence Diagram 是单个核心流程的主要讲解图。普通 `A -> B -> C` flowchart 只可作为导航图，不能独立满足流程细节要求。

#### 按复杂度增加的图

| 复杂度信号 | 增加的图 | 需要表达的细节 |
|---|---|---|
| callback、retry、补偿、对账、最终一致性 | Failure Recovery Timeline | 时间窗口、观察点、重试和恢复终点 |
| DTO、Command、Entity、DB Record、Event 多次转换 | Data Lineage / Object Transformation | 对象 owner、字段变化、ID 和状态来源 |
| transaction、lock、Lua、outbox、并发、幂等 | Transaction / Concurrency Boundary | 事务内外、锁生命周期、幂等检查、部分成功 |
| 多 Topic、consumer、retry queue、DLQ | Async Message Topology | producer、consumer、delivery、retry、DLQ 和 owner |
| 路由、权限、provider 或策略选择复杂 | Decision Tree | 条件、优先级、fallback 和拒绝结果 |
| 实体关系影响理解 | ERD / Model Relationship | 关系、聚合边界和真相来源 |
| gateway、sidecar、环境拓扑影响行为 | Runtime / Deployment Topology | route、header、timeout、retry、upstream、logs |
| 排障入口分散 | Observability / Troubleshooting Map | request ID、logs、metrics、traces、DB/MQ 检查顺序 |

Diagram Plan 不再只列图类型，还要记录触发该图的复杂度信号和覆盖的 Slice IDs。

非 Flow 内容文档按解释需要选择图，不继承核心 Flow 的固定图组：

- system context / architecture / domain docs 使用能说明边界、关系和数据所有权的图；
- jobs / async / runtime docs 在存在时间、状态或恢复语义时使用 sequence/state/timeline；
- glossary、静态配置清单、纯索引和没有状态语义的说明不强制状态图；
- 任何豁免都不允许掩盖实际存在的状态、分支或恢复行为。

#### 图文绑定

每张图必须具有稳定 Diagram ID，并附带：

- 图要看什么；
- 图支持什么结论；
- 覆盖哪些 Slice IDs；
- 出现哪些数据对象、状态字段、消息和配置；
- 对应哪些代码证据；
- 哪些内容属于 inferred，以及置信度和待验证点。

禁止用同一张泛化图复制到多个章节并声称完成不同职责。

### 4. Coverage 与 Review

#### 两级判定

`newcomer-ready` 使用两级判定：

1. **Completeness Hard Gate**：核心流程和关键 slice 没有未解释的缺失。
2. **Quality Score**：通过 hard gate 后，再评价图解、证据、排障和可读性质量。

Hard Gate 失败时，无论平均分多高，都不能标记 `newcomer-ready`。

#### 统一评分维度

`coverage-matrix.md` 与 `batch-review.md` 使用同一组维度：

- Core flow discovery completeness；
- Slice and branch coverage；
- Architecture / boundary clarity；
- Timeline / sequence clarity；
- State machine clarity；
- Data object / lineage completeness；
- Failure / recovery completeness；
- Evidence granularity and traceability；
- Troubleshooting / observability；
- Change guidance；
- Newcomer readability。

评分继续使用 1-5，但增加锚点：

| 分数 | 锚点 |
|---:|---|
| 5 | 完整、证据闭合，新人可独立解释和排障 |
| 4 | 核心路径完整，只有不影响接手的低风险缺口 |
| 3 | 可以理解主路径，但分支、恢复或证据存在明显缺口 |
| 2 | 结构存在，内容主要是概览或泛化描述 |
| 1 | 无法依靠该文档理解或操作 |

### 5. 任务与 Human Gate

Onboarding Tasks 对每个核心 Flow task 必须列出：

- Flow ID 和计划路径；
- 必须覆盖的 Slice IDs；
- 默认图组；
- 条件触发图；
- evidence required；
- Completeness Hard Gate；
- quality score target。

Human Gate 保持两个：

```text
Gate 1: 接受 Onboarding Spec
  - 包含 Core Flow Inventory 选择结果
  - 只授权创建 Onboarding Tasks

Gate 2: 接受 Onboarding Tasks Full Execution Gate
  - 包含具体 Flow/Slice/Diagram/Evidence 范围
  - 授权连续创建正式 onboarding 文档
```

本 proposal 不引入 Core Flow Gate、Diagram Gate 或 Batch Gate 等额外人工暂停点。

### 6. 验证设计

#### RED 基线

实现前保留以下当前漏洞证据：

1. 现有 onboarding source validation 可以在没有完整 onboarding 示例产物时通过；
2. Flow Candidate 没有终态、变体、恢复责任和选择理由字段；
3. topic 评分没有关键 slice hard blocker；
4. batch review 与 coverage matrix 的图解评分维度不一致。

#### 新增压力场景

至少覆盖：

1. **只写成功路径**：缺少 callback failure 和 reconciliation，必须拒绝 newcomer-ready。
2. **有三张图但图文脱节**：没有 Slice ID、数据对象或代码证据映射，必须判定 incomplete。
3. **漏异步消费者**：API 到 DB 完整，但 event consumer 改变最终状态，必须回到 Evidence Graph 补 flow/slice。
4. **关键失败被平均分掩盖**：其他维度为 5，关键 compensation slice 缺失，仍必须 hard fail。
5. **简单 CRUD**：没有异步、事务或复杂状态时，不强制额外恢复、并发或消息拓扑图。
6. **wallet / billing / quota**：必须触发 transaction/concurrency 和 recovery 表达。
7. **gateway runtime**：必须触发 boundary/runtime 图和 route/header/timeout/log evidence。
8. **延期流程**：critical / important flow 只有在记录 evidence、impact 和 deferred reason 后才可延期。
9. **不新增 Gate**：Spec Acceptance 与 Full Execution Gate 仍是唯二 onboarding 人类确认点。

#### 产物级验证

在 `examples/` 增加一个小而完整的复杂项目 onboarding reference，至少包含：

- API 入口；
- 多模块调用；
- DB 状态变化；
- MQ publish / consume；
- callback；
- retry / reconciliation；
- 一个 transaction / idempotency 风险；

在 `tests/fixtures/` 单独保存一条故意遗漏关键 slice 的最小 invalid fixture，避免复制两套完整 onboarding 树。

可执行 validator 至少检查：

- Flow ID 从 Inventory 贯通到 Plan、Task、Flow doc、Coverage 和 Review；
- 每个 planned critical/important flow 有终态和 Slice IDs；
- 每个关键 Slice ID 有 evidence、diagram 和 document section 映射；
- required / conditionally-triggered diagram 均存在；
- invalid fixture 因目标缺陷失败；
- placeholder、空 required row 和泛化 evidence 仍被拒绝。

validator 不宣称验证业务事实绝对正确；事实正确性继续由证据审计和压力场景负责。

## 实施影响面

### 运行与设计来源

| 文件 | 计划动作 |
|---|---|
| `SKILL.md` | 将 onboarding 摘要从 wireframe preferred 调整为 core-flow inventory、sequence-main、state/branch coverage 的简洁入口 |
| `references/design.md` | 补充核心流程完整性与 Evidence -> Slice -> Evidence 的设计不变量 |
| `references/runtime.md` | 保持阶段顺序和两个 Gate；明确 accepted spec 必须覆盖核心流程选择结果 |
| `references/onboarding-knowledge-base.md` | 承载完整 Core Flow Inventory、Slice Coverage、图选择和 hard gate 规则 |

### 阶段与模板

| 文件 | 计划动作 |
|---|---|
| `references/stage-guides.md` | 对齐 onboarding 执行和 review 步骤 |
| `references/workflow-checklists.md` | 增加发现、slice、图文绑定和 hard gate 检查 |
| `templates/onboarding-db/evidence-graph.md` | 增加 Core Flow Inventory 和完整性检查 |
| `templates/onboarding-db/onboarding-spec.md` | 增加核心流程选择、Flow Slice Plan 和图触发信号 |
| `templates/onboarding-db/onboarding-tasks.md` | 任务记录 Flow/Slice/Diagram/Evidence 范围 |
| `templates/onboarding-db/flow.md` | 增加 Flow/Slice IDs、主图职责、条件图和追踪表 |
| `templates/onboarding-db/coverage-matrix.md` | 增加 Completeness Hard Gate 和统一评分锚点 |
| `templates/onboarding-db/batch-review.md` | 与 Coverage Matrix 使用同一评分维度 |
| `templates/onboarding-db/README.md` | 更新新人阅读顺序和图解职责说明 |

### 验证与示例

| 文件 | 计划动作 |
|---|---|
| `references/validation-scenarios.md` | 加入缺流程、缺 slice、图文脱节和不新增 Gate 的压力场景 |
| `tests/validate-evidence-graph-ddd-onboarding.sh` | 保留 source/template contract regression |
| `tests/validate-onboarding-core-flow-completeness.sh` | 新增跨 artifact ID 和 hard-gate 校验 |
| `examples/ai-meeting-minutes-backend/onboarding-db/` | 增加一套可阅读、可验证的 valid 核心流程 onboarding reference |
| `tests/fixtures/onboarding-core-flow/` | 只保存针对性的 invalid fixture |
| `Usage.md` | 增加面向人类的核心流程图组和完整性说明 |
| `CHANGELOG.md` | 实施完成后记录 v1.3.0 行为变化 |

`templates/root-AGENTS.md` 的 Stage Map 信号和下一阶段不因本设计改变。实施时仍需运行 root guidance validation，只有 managed block 的 onboarding 描述需要表达新不变量时才更新 block 内容和对应测试。

## 兼容与迁移

已有 Evidence-Graph + DDD onboarding-db 不自动判定失效：

- Focused Update 可以为相关核心流程补 Inventory、Slice IDs 和图文映射；
- 全项目缺少核心流程选择证据时，标记 coverage `needs-review`，通过现有 Onboarding Spec migration/update gate 处理；
- 不因为格式升级删除旧文档；旧内容继续作为 evidence；
- 不要求一次性重写所有低风险 supporting flow；优先迁移 `critical` 和 `important` 流程。

## 验收标准

实施完成需同时满足：

- Core Flow Inventory 能区分 critical、important 和 supporting flow；
- critical / important flow 必须 planned 或有证据级 deferred reason；
- supporting flow 只有触及核心状态、副作用或恢复责任时才要求完整 slice 追踪；
- 每个计划内核心流程有成功终态、失败终态、变体和 Evidence Chain；
- 每个关键 slice 能追踪到 evidence、diagram 和 document section；
- 每个核心 Flow 默认使用全景/边界、Timeline / Sequence、ASCII State 三类互补表达；
- 非 Flow 文档按内容相关性选图，不为无状态主题编造状态图；
- 条件复杂度可以可靠触发 recovery、lineage、transaction/concurrency、async topology、decision tree 等附加图；
- Completeness Hard Gate 失败时不能通过平均分成为 newcomer-ready；
- coverage matrix 与 batch review 使用一致的维度和评分锚点；
- valid fixture 通过，invalid fixture 因目标缺陷失败；
- Onboarding Spec Acceptance 和 Full Execution Gate 仍是唯二 onboarding Human Gate；
- 不改变 canonical stage order、Project Entry 边界、Module/Flow 单文件默认策略；
- 运行 onboarding 功能专项测试、直接相关回归、YAML/JSON/Markdown/Shell/diff 检查；
- 按 `docs/maintenance/feature-validation-method.md` 完成单功能逻辑与压力评分报告；全仓库/全技能验证只在人类明确授权时另行执行，不计入默认功能得分。

## 实施顺序建议

```text
1. 固化 RED 漏洞与 invalid fixture
2. 更新 design/runtime/controller summary
3. 更新 onboarding runtime reference
4. 更新 Evidence/Spec/Tasks/Flow/Coverage/Review templates
5. 更新 stage guide/checklist/validation scenarios/Usage/CHANGELOG
6. 实现 artifact validator
7. 运行 focused GREEN
8. 运行 onboarding 功能边界测试和单功能语义验证
9. 形成评分报告
10. 人类确认后再进入 commit / push
```

## 人类评审点

本 proposal 需要人类确认以下设计结论后才能进入实施计划：

1. 采用方案 B：Core Flow Inventory + Flow Slice Traceability；
2. 不新增 onboarding Human Gate；
3. Timeline / Sequence Diagram 作为单流程正文主图；
4. 全景/边界图负责防漏，ASCII State Diagram 负责状态和恢复；
5. 额外图由复杂度信号触发，不固定图数量；
6. newcomer-ready 增加 Completeness Hard Gate；
7. v1.3.0 包含 valid/invalid fixture 和产物级 validator。
