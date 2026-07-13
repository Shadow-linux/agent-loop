# Proposal: Concept Foundation For Requirement Modeling

状态：已批准；Phase 1 / Phase 2 已实现并完成 review repair，待最终人类验收

目标版本：v1.3.x 候选

创建时间：2026-07-12

## 摘要

当前 Agent Loop 已经通过 Requirement/Product Grill、Requirement Document、Product Brief 和 Decision & Design 支持术语澄清、角色、业务流程、异常路径、事实源、产品决策和跨 Feature 设计。

现有缺口位于所有这些模型之前：Agent 会在术语模糊时提问，却没有稳定要求复杂需求先固化核心业务概念，再沿着概念推导角色、关系、流程、状态机、产品数据模型、ADR、UI 设计输入和 E2E 场景。结果可能是每一份下游文档单独看都合理，但它们对“订单”“申请”“余额”“审核”“完成”等概念的身份、边界和生命周期理解并不一致。

本 proposal 建议在 Requirements Discussion / Requirement Product Grill 内增加触发式 `Concept Foundation` 方法和前置 Gate：

```text
真实场景与目标
→ 提取候选概念
→ Concept Foundation
→ 角色 / 权限与概念关系
→ 业务流程
→ 状态机
→ 产品数据模型
→ 异常与恢复
→ Design Readiness / Decision & Design
→ Design Skill / Feature Spec / E2E
```

`Concept Foundation` 不是新的 canonical stage，不新增顶层 artifact，也不要求人类先懂领域建模。Agent 先从人类语言、案例、现有项目记忆、代码、测试和历史 Feature 中提取名词、动作和冲突，再一次只提出一个真正阻塞后续模型的问题，并附带推荐定义。

## 背景与问题定义

### 当前已经具备的能力

当前 Requirement/Product Grill 已经要求：

- 在术语、角色、权限、业务流程、状态流转、异常路径或事实源不清楚时进行针对性澄清；
- 先检查项目记忆、需求来源、代码、测试和相关历史 Feature；
- 把确认后的术语写入 requirement document 的 `Terminology / Domain Language`；
- 把长期或跨 Feature 信号送入 Design Readiness / Decision & Design；
- 避免从模糊聊天直接创建 ADR。

当前 requirement document 也已经包含：

- `Roles / Operators / Permission Boundary`；
- `Terminology / Domain Language`；
- `Primary Business Flow`；
- `Exception Paths`；
- `Data / Source of Truth`；
- `Acceptance Scenarios`；
- `Decision Candidates`。

这些能力为 Concept Foundation 提供了可复用基础，不需要推翻现有 Requirements Discussion 或新建复杂领域建模体系。

### 当前结构性缺口

#### 1. 术语澄清是条件动作，不是复杂需求的前置方法

当前规则只在术语模糊或冲突时触发。一个词即使看起来清楚，也可能缺少身份、边界、所有者、生命周期和关系定义。例如“退款”可能表示请求、审核过程、资金动作或最终结果；仅记录一句自然语言定义无法支撑后续状态机和数据模型。

#### 2. Requirement 模板先列功能，再补术语

现有结构允许 Agent 先写 `Requirements`，再填写 `Terminology / Domain Language` 和 `Primary Business Flow`。这会让下游模型继承未经确认的名词，而不是从稳定概念推导行为。

#### 3. 没有 Concept Foundation Gate

当前没有明确阻止 Agent 在关键概念仍有歧义时继续设计流程、状态机、数据模型、页面或 E2E。人类可能直到看到原型或代码才发现双方对“完成”“取消”“用户”“账户”等概念理解不同。

#### 4. 缺少概念到下游模型的推导链

当前 artifacts 能记录流程、数据和 Decision Candidate，但没有稳定说明：

```text
概念名词       → 领域对象
概念关系       → 产品数据模型
业务动作       → Command / Event
生命周期       → 状态机
角色与责任     → 流程泳道和权限
不变量         → Guard 和校验规则
失败场景       → 异常、补偿与恢复
状态与动作     → UI 页面状态和 E2E 场景
```

#### 5. 概念变化没有明确的 Drift 扇出

当已确认概念的含义、身份或生命周期变化时，当前规则没有要求统一回查关系、流程、状态机、数据模型、Decision、UI 设计和 E2E。局部修改可能留下多个互相矛盾的真相源。

## 目标

本 proposal 的目标是：

1. 让复杂需求在流程和状态设计前形成可确认的 Concept Foundation。
2. 让 Agent 从真实场景和项目证据提取概念，而不是要求人类先完成抽象领域建模。
3. 让每个关键概念拥有足以支撑流程、状态机和产品数据模型的定义。
4. 让概念关系、生命周期、不变量和事实源问题能够稳定进入 Design Readiness。
5. 让 Decision & Design 引用已确认的产品概念，而不是在技术设计阶段重新发明产品语义。
6. 给未来偏 UI / 交互的 Design Skill 提供稳定、可消费的页面设计输入。
7. 给未来 E2E Skill 提供状态转换、业务规则和异常闭环的统一测试来源。
8. 在概念发生变化时触发可追踪的下游 Drift 检查。
9. 保持简单需求轻量，不让小改动被迫进入完整概念建模。

## 非目标

本轮不做以下事情：

- 不新增 `Concept Foundation` canonical stage；
- 不新增 `.agent-loop/concepts/`、`domain-model/` 或其他顶层目录；
- 不要求所有需求创建 ADR；
- 不要求所有概念进入 `project.md Domain Language`；
- 不把 requirement document 变成数据库 schema 或技术 ERD；
- 不要求人类使用 DDD、UML 或状态机术语与 Agent 对话；
- 不让 Design Skill 自行修改业务概念、状态机或事实源；
- 不让 E2E Skill 从页面结构反推并覆盖业务真相；
- 不在第一版引入 YAML / JSON 可执行 Schema；
- 不改变原始人类需求材料不可静默重写的规则；
- 不改变 Decision、Feature、Submit、Pause、Close 等既有 Human Gate；
- 不在 proposal 阶段修改已发布 runtime、template 或 validation 行为。

## 方案比较

### 方案 A：只增强术语表

做法：给 `Terminology / Domain Language` 增加身份、关系和生命周期列。

优点：改动最小，容易落地。

限制：仍然没有前置 Gate、推导链和 Drift 规则；Agent 可能填写完表格后继续生成彼此割裂的流程与状态机。

### 方案 B：触发式 Concept Foundation + Downstream Traceability

做法：在 Requirements Discussion 内增加 Concept Foundation 方法、触发条件、Gate、稳定 Concept ID、推导矩阵和下游 Drift 检查。Concept Foundation 仍写在 human-reviewed requirement document，不新增 stage 或目录。

优点：直接解决概念不稳导致的流程、状态、数据、UI 和 E2E 漂移；与现有 Requirement/Product Grill、Design Readiness 和 Decision & Design 兼容。

代价：正式实施时需要协调 runtime/design、stage guidance、templates、root guidance、validation scenarios 和 regression tests。

### 方案 C：可执行领域 Schema

做法：使用 YAML / JSON 定义实体、关系、状态、事件、Guard 和权限，并让 Design Skill 与 E2E Skill直接读取。

优点：机器可读，未来可用于自动生成页面状态矩阵和测试场景。

限制：过早固化 Schema 会把产品澄清变成格式维护；还会显著扩大第一版解析、兼容和迁移成本。

### 推荐

采用方案 B。保留方案 C 作为 Concept Foundation 已被多个真实项目验证后的独立 proposal，不阻塞 v1.3.x。

## 核心设计

### 1. Concept Foundation 的定位

`Concept Foundation` 是 Requirements Discussion / Requirement Product Grill 内部的前置方法，不是新的 stage：

```text
Requirements Discussion
  → Scenario Intake
  → Concept Candidate Extraction
  → Concept Foundation Gate if triggered
  → Business Flow / State / Product Data Modeling
  → Human-reviewed Requirement Document
  → Requirement Archive
```

它只约束产品语义形成的顺序，不改变 canonical stage order。

### 2. 触发条件

发现任一信号时，Concept Foundation 状态至少进入 `candidate`：

| Signal | Why It Matters |
|---|---|
| 同一术语可能表示多个对象、动作或结果 | 流程和数据会把不同事物误当成一个概念 |
| 新增或改变有生命周期的业务对象 | 状态机需要稳定身份和生命周期边界 |
| 多角色、租户、运营方或外部系统参与 | 权限、所有权和流程泳道依赖概念定义 |
| 需求会拆成多个 Feature | 各 Feature 必须共享同一业务语言 |
| 涉及事实源、余额、库存、订单、审批、任务或额度 | 数据所有权和不变量通常难以逆转 |
| 现有 Domain Language、代码、测试或历史 Feature 与新说法冲突 | 必须先决定复用、覆盖还是新 scope |
| Design Skill 需要依据数据模型和状态流转设计页面 | 页面不能自行发明业务状态和允许动作 |
| E2E 需要证明跨页面或跨系统闭环 | 测试必须知道对象身份、事件和终态 |

以下情况可以记录 `concept-foundation-not-needed`：

- 纯文案、样式或局部布局调整；
- 不改变语义的窄 bugfix；
- 单一配置修改；
- 只复用已有 accepted Domain Language、状态机和事实源，且没有新增概念或关系；
- 没有状态、所有权、跨角色、跨 Feature 或数据语义变化的简单功能。

`concept-foundation-not-needed` 必须包含一句理由，不能作为跳过模糊需求澄清的默认值。

### 3. Scenario-first 概念提取

Agent 不应先问抽象问题“请定义你的领域模型”。推荐方法：

1. 收集一个正常成功场景和必要的异常场景；
2. 从自然语言中提取名词、动作、结果和约束；
3. 对照项目 Domain Language、原始需求、代码、测试和相关历史 Feature；
4. 合并同义词，拆开一词多义，标记冲突；
5. 形成 Concept Candidate Inventory；
6. 一次只向人类确认一个会改变流程、状态或数据模型的阻塞问题；
7. 每个问题都附带 Agent 的推荐定义、依据和不采用时的影响。

示例：

```text
你提到“客户提交退款，管理员审核后退回余额”。

我识别到“退款”可能同时表示退款申请、审核流程和资金退回结果。
推荐定义：
- Refund Request = 客户发起、可审核的申请对象；
- Refund Review = 管理员对申请作出的审批动作；
- Refund Settlement = 实际资金退回结果。

这样状态机和事实源不会把申请状态与资金状态混为一体。
是否接受这三个概念边界？
```

### 4. Concept Candidate Inventory

在深入确认前，先用轻量清单展示候选概念：

| Concept ID | Candidate Name | Kind | Evidence / Example | Ambiguity / Conflict | Status |
|---|---|---|---|---|---|
| C-REFUND-REQUEST | Refund Request | entity | human scenario | “退款”也可能指资金结果 | candidate |
| C-REFUND-REVIEW | Refund Review | action / decision | admin flow | 是否允许多次审核 | candidate |
| C-REFUND-SETTLEMENT | Refund Settlement | entity / result | payment callback | 外部支付还是内部余额为事实源 | candidate |

Concept ID 在 requirement scope 内稳定，用于连接后续关系、流程、状态、Decision Candidate 和验收场景。第一版不要求 Concept ID 成为全项目永久编号。

### 5. Concept Definition

只有影响当前需求的字段才需要填写；不适用字段写 `n/a`，不允许为了完整表格编造事实。

| Field | Meaning |
|---|---|
| Concept ID | requirement 内稳定引用，例如 `C-ORDER` |
| Canonical Name | 本需求中的唯一推荐名称 |
| Definition | 精确定义这个概念是什么 |
| Examples / Non-examples | 用正反例排除相邻含义 |
| Identity | 如何判断两个记录是否代表同一个对象 |
| Owner / Responsible Actor | 谁创建、管理、推进或负责该概念 |
| Lifecycle Boundary | 何时产生、何时结束、结束后能否恢复 |
| Relationships | 与其他概念的基数、依赖或包含关系 |
| Invariants | 始终必须成立的业务规则 |
| State-bearing | 是否具有业务状态和状态生命周期 |
| Source Of Truth | 已知事实源或待 Decision & Design 的候选 |
| Synonyms / Avoid | 可接受同义词和禁止混用的词 |
| Evidence | 人类确认、原始需求、代码、测试或历史 Feature |

推荐 requirement document 结构：

```md
## Concept Foundation

Status: concept-foundation-not-needed | candidate | accepted | reopened

### Concept Candidate Inventory

### Concept Definitions

### Concept Relationships

### Blocking Ambiguities

### Human Confirmation
```

### 6. Concept Foundation Gate

复杂需求在进入 `Primary Business Flow`、状态机或产品数据模型前必须满足：

| Check | Gate Rule |
|---|---|
| 关键概念拥有唯一推荐含义 | blocking |
| 一词多义、同义词和历史冲突已处理 | blocking when downstream meaning changes |
| 关键实体的身份和生命周期边界明确 | blocking |
| 角色、所有权和权限边界明确 | blocking when multiple actors participate |
| 关键概念关系明确到足以设计流程 | blocking |
| 哪些概念拥有状态已明确 | blocking |
| 关键不变量已列出 | blocking |
| 事实源已确认或明确标为 Decision Candidate | blocking only if flow cannot proceed without the choice |
| 未解决问题不会改变当前流程模型 | required |
| 人类确认 Concept Foundation | required for triggered complex requirements |

Gate 输出：

- `concept-foundation-not-needed`：不触发，记录理由；
- `candidate`：候选概念已提取，但存在会改变下游模型的问题；
- `accepted`：阻塞概念已由人类确认，可以继续推导流程、状态和数据；
- `reopened`：下游设计、代码现实或人类反馈改变了已接受概念，必须先处理 Drift。

Concept Foundation 的确认可以作为 Requirements Discussion 的一次前置 Human Gate，也可以与一组概念的 Batch Human Review 合并；它不新增 canonical stage，也不授权 Requirement Archive、ADR 创建或 Feature construction。

### 7. 从概念推导下游产品模型

Concept Foundation 接受后，Agent 按以下关系推导并检查，而不是把每个 artifact 独立生成：

| Concept Evidence | Derived Model | Required Check |
|---|---|---|
| Canonical Name + Definition | Domain Language | 后续 artifacts 使用同一名称和含义 |
| Identity + Relationships | Conceptual Product Data Model | 对象、关系和基数不互相矛盾 |
| Owner + Responsible Actor | Role / Permission Matrix | 谁能读取、创建、推进、撤销和恢复 |
| Lifecycle Boundary + State-bearing | State Machine | 初始态、终态、恢复和禁止转换明确 |
| Human Verbs / System Actions | Commands / Events | 每个动作有 actor、precondition 和结果 |
| Invariants | Guards / Validation Rules | 状态转换和数据写入不能破坏不变量 |
| Relationships + Commands + Events | Primary Business Flow | 每一步使用已确认概念并闭合到终态 |
| Failure Scenarios | Exception / Compensation / Recovery | 每类失败有可观察结果和责任方 |
| States + Permissions + Commands | UI Design Input | 页面状态、可见动作和反馈不自行发明规则 |
| Transitions + Invariants + Terminals | E2E Scenario Matrix | 正常、禁止、失败和恢复路径可验证 |

### 8. Product Data Model 与 Technical Data Model 分离

Requirement Document 只描述产品层概念模型：

- 哪些业务对象存在；
- 对象如何识别；
- 对象之间是什么关系；
- 哪些事实和不变量必须成立；
- 谁拥有或能够改变这些事实。

Decision & Design 再决定技术实现：

- 对应哪些 table、document、event、ledger 或外部 provider；
- 哪个存储是技术事实源；
- 如何实现事务、一致性、并发、幂等和恢复；
- 如何把产品状态映射为系统状态；
- 如何迁移、兼容和验证。

ADR 应引用 Concept ID，并增加产品概念到技术实现的映射，而不是重新定义概念：

| Concept ID | Product Meaning | Technical Representation | Source Of Truth | Invariant Enforcement | Migration / Compatibility |
|---|---|---|---|---|---|

### 9. 与 Decision & Design / ADR 的关系

不是每个概念都生成 ADR。Concept Foundation 只把以下内容标记为 Decision Candidate：

- 跨 Feature 的共享概念定义；
- 难以逆转的数据身份或事实源；
- 多个合理边界方案之间的真实取舍；
- 会改变项目级所有权、协议、状态语义或一致性模型的选择；
- 如果不记录原因，未来维护者会问“为什么这样定义”的规则。

Decision & Design 负责：

- 接受已确认 Concept Foundation 作为输入；
- 运行 Decision Scan / Placement；
- 记录需要长期保存的边界和取舍；
- 把 Concept、Flow、State、Invariant 和 Recovery 映射为 Design Slice；
- 分配 owning Feature 和验证证据。

它不得在没有人类确认的情况下改变 requirement 中已接受的概念语义。

### 10. 给 Design Skill 的输入

未来偏 UI / 交互的 Design Skill 消费一个由已接受 requirement、Product Brief 和 Decision & Design 派生的只读 `UI Design Input View`。第一版不新增独立 source-of-truth 文件；该 view 可以在 Design Skill 的输入摘要或 owning artifact 中生成。

输入至少包括：

- Concept ID、名称和产品含义；
- 角色、权限和所有权；
- 产品对象关系和页面所需信息；
- 状态、事件、Guard 和允许操作；
- 正常、异常、恢复和人工处理路径；
- 不可被 UI 改写的业务不变量；
- Loading、Empty、Error、Success 所对应的业务语义；
- 尚未解决、禁止 Design Skill 自行假设的问题。

Design Skill 可以提交 `Design Feedback`：

```text
Design Feedback
→ Agent Loop impact scan
→ reopen Concept Foundation / Product / Decision if semantics change
→ human confirmation
→ regenerate affected UI design input
```

Design Skill 不得静默增加业务状态、改变事实源或放宽 Guard。

### 11. 给 E2E Skill 的输入

未来 E2E Skill 使用同一模型生成或检查：

- 每个关键状态转换的 happy path；
- Guard 不满足时的禁止转换；
- 重复事件和幂等行为；
- 失败、重试、补偿和人工恢复；
- 角色权限与页面动作可见性；
- 成功终态、失败终态和可观察证据；
- 概念不变量在跨页面、跨服务流程中的保持情况。

E2E Skill 不从当前页面行为反向覆盖 accepted Concept Foundation；发现不一致时进入 Drift / Design Feedback。

### 12. Concept Drift

已接受概念发生以下变化时，Concept Foundation 状态转为 `reopened`：

- Canonical Name 的含义改变，而非只改展示文案；
- Identity、Owner、Lifecycle Boundary 或 Relationship 改变；
- State-bearing 属性或业务终态改变；
- Source Of Truth 或关键 Invariant 改变；
- 一个概念被拆分、合并或废弃；
- Design Skill、E2E、实现或历史 Feature 暴露语义冲突。

必须执行影响扇出：

```text
Concept Change
→ Relationship Drift
→ Business Flow Drift
→ State Machine Drift
→ Product Data Model Drift
→ Decision / Design Slice Drift
→ Feature Spec / Test Drift
→ UI Design Drift
→ E2E Drift
→ Project Domain Language update if applicable
```

Agent 先列影响和推荐修订，不静默重写人类原始需求或 accepted Decision。

## Artifact Ownership

| Artifact / Surface | Owns | Does Not Own |
|---|---|---|
| Human source requirement | 人类原始表达 | 不被 Agent 静默改写 |
| Requirement document | requirement-local Concept Foundation、关系、流程、状态、产品数据、异常和验收 | 不拥有技术 schema 或项目长期事实 |
| Requirement README | 来源、生命周期、Delivery Phase、Feature Mapping、Design Readiness、decision links，以及归档后 `Effective Concept Foundation` 状态/来源指针 | 不复制完整 Concept Foundation；不改写历史 source |
| `project.md Domain Language` | 人类确认后需要跨 Feature 复用的稳定概念 | 不保存每个需求的局部概念 |
| `product.md` | 当前 Feature 的产品旅程、范围、体验和产品取舍 | 不重新定义 accepted shared concepts |
| `.agent-loop/decisions/*.md` | 跨 Feature、长期、难逆转的概念边界和技术实现决策 | 不成为所有术语的字典 |
| `spec.md` | Feature 行为、验收和 assigned Design Slices | 不复制整套产品模型 |
| Design Skill output | 页面、交互、组件状态和原型 | 不拥有业务概念、事实源或状态机真相 |
| E2E Skill output | 从 accepted 模型推导的端到端验证 | 不通过测试结果静默改写需求语义 |

## Agent Interaction Contract

触发 Concept Foundation 时，Agent 必须：

1. 先读取可用的 Domain Language、source requirement、相关代码/测试和历史 Feature；
2. 用真实场景提取候选概念；
3. 展示推荐定义和证据；
4. 一次只问一个会改变下游模型的阻塞问题；
5. 说明接受或拒绝推荐定义分别影响哪些流程、状态或数据设计；
6. 在进入 Business Flow 前展示 Concept Foundation Human Review Summary；
7. 未获得确认时保留 `candidate`，不伪装为 accepted；
8. 简单需求不触发时记录 `concept-foundation-not-needed` 和理由。

推荐 Human Review Summary：

| Concept ID | Recommended Definition | Identity / Boundary | Relationship | State / Lifecycle | Open Conflict | Decision |
|---|---|---|---|---|---|---|

## 实施影响面

本 proposal 获得实施批准后，至少需要协调检查和更新：

- `references/design.md`：加入 concept-first 的核心约束；
- `references/runtime.md`：Requirements Discussion routing、Gate 和 stop condition；
- `SKILL.md`：精简入口和对应 reference 路由；
- `references/requirement-product-grill.md`：Scenario-first、Concept Foundation、提问和输出映射；
- `references/requirement-management.md`：requirement review、archive 和 concept status；
- `references/project-decisions.md`：Concept ID、产品到技术映射和 concept drift；
- `references/product-brief.md`：复用 accepted concepts，不重新定义共享语义；
- `references/stage-guides.md`：Requirements Discussion、Requirement Archive、Decision & Design、Product Brief、Feature Spec；
- `references/workflow-checklists.md`：Concept Foundation Gate 和 downstream traceability；
- `references/document-templates.md`：Requirement Document 的 Concept Foundation、关系、状态和产品数据模型；
- `templates/decision.md`：产品概念到技术实现映射；
- `templates/product.md`、`templates/spec.md`、`templates/tests.md`：Concept / State / Design Slice 引用；
- `templates/root-AGENTS.md` 和 `references/project-guidance.md`：root Stage Map signal/reference 与 required stop；
- `README.md`、`Usage.md`、`CHANGELOG.md`：人类触发方式和版本行为；
- `references/validation-scenarios.md` 与 focused regression tests；
- `examples/`：至少一个状态型业务需求的完整 Concept → Flow → State → Decision → Feature 示例。

由于正式实施会改变 Requirements Discussion 的 Gate、stop rule 和跨文件 workflow invariant，必须按 `docs/maintenance/full-validation-method.md` 执行完整验证并保存中文报告。Proposal 阶段不把这些规则声明为已发布能力。

## 验证与压力场景

正式实现至少需要覆盖：

### 1. 一词多义

人类说“退款完成”，但申请审批完成和资金到账完成是两个不同终态。Agent 必须拆分概念并在流程前确认。

### 2. 相邻概念混用

需求把 User、Customer、Member 和 Tenant 混用。Agent 必须检查项目 Domain Language 并提出 canonical boundaries。

### 3. 状态对象识别

“审批”既可能是动作，也可能是有生命周期的 Approval Instance。Agent 必须通过场景判断是否需要独立对象。

### 4. 历史冲突

历史 Feature 定义余额不足立即停止服务，新需求描述允许透支。Agent 必须先提出冲突和推荐选择，不能直接生成新流程。

### 5. 简单需求保持轻量

按钮文案修改且不改变权限、状态和数据语义。Agent 应记录 `concept-foundation-not-needed`，不得生成大型概念表。

### 6. ADR 不过度生成

单 Feature 内局部筛选概念不应创建 project decision；共享事实源或跨 Feature 状态语义才进入 Decision Candidate。

### 7. Design Feedback 回流

Design Skill 发现某状态下没有可恢复入口。Agent 必须判断是 UI 缺失还是业务模型缺失；后者重新打开 Concept Foundation / Decision，而不是让 Design Skill自行增加状态。

### 8. E2E 追踪

每个关键状态转换、禁止转换和恢复终态都能追踪到 acceptance / tests，不允许只验证页面存在。

### 9. Concept Drift 扇出

accepted Concept 的身份或生命周期改变时，Agent 必须列出 Flow、State、Data、Decision、Feature、UI 和 E2E 影响，并停在 Human Gate。

## 分阶段实施建议

### Phase 1: Requirement Concept Foundation

- 加入触发条件、Concept Candidate Inventory、Definition、Gate 和 requirement template；
- 增加简单需求 not-needed 路由；
- 增加 pressure scenarios 和 focused regression test。

### Phase 2: Product Model Derivation

- 增加 Concept Relationship、State Machine、Product Data Model 和 Business Flow 推导规则；
- 增加 upstream-to-downstream traceability；
- 更新 Product Brief 和 Feature Spec 引用。

### Phase 3: Decision & Design Mapping

- 增加 Concept ID 到 technical representation、source of truth、invariant enforcement 的映射；
- 把 shared concepts、states、flows 和 recovery obligations 转为 Design Slices；
- 加入 Concept Drift 检查。

### Phase 4: Jam Kits Integration

- 定义 Design Skill 的 UI Design Input View；
- 定义 Design Feedback 回流；
- 定义 E2E Skill 的 State / Invariant / Terminal 输入；
- 等真实项目验证稳定后，再评估可执行 Schema proposal。

各 Phase 只是实施切片，不改变 Human Gate。若分阶段发布，每个阶段都必须保持 artifacts 和 routing 自洽，不能让 Requirement 模板先产生无法被下游消费的字段。

## 批准时的决策与后续问题

1. Phase 1 / Phase 2 使用 requirement-local 稳定 Concept ID；项目级永久编号不属于本轮。
2. Concept Foundation Human Gate 是 Requirements Discussion 内的产品语义确认；按 Human Grill Contract 每次只确认一个 downstream-blocking 问题，不用模糊 Batch Review 绕过。
3. 产品层 Concept Relationship 和 State Model 以可追踪表格为 source of truth；可视化图仅作派生视图。
4. `UI Design Input View` 的 artifact 形式保留到 Phase 4 / Jam Kits Integration 再评审。
5. Concept Drift 的 rename 自动传播与 Human Gate 分界保留到 Phase 3 再评审。

## 推荐结论

建议接受以下方向进入后续实施规划：

```text
Concept Foundation 是复杂 Requirements Discussion 内部的前置 Gate。
它不新增 canonical stage 或顶层 artifact。
Agent 从真实场景和项目证据提取概念，并由人类确认阻塞语义。
流程、状态机、产品数据模型、ADR、UI Design 和 E2E 都沿 accepted concepts 推导。
简单需求使用 concept-foundation-not-needed 保持轻量。
概念变化触发显式 downstream drift，不静默改写 accepted artifacts。
```
