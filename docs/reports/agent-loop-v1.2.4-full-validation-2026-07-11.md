# Agent Loop v1.2.4 全量验证与压力测试报告

日期：2026-07-11
目标：`skills/agent-loop`
分支：`alpha/v1.2.4`
版本：`1.2.4`
审计对象：当前未提交工作区，而非 Git `HEAD`

## 1. 最终结论

本轮修复后，Agent Loop v1.2.4 的综合评分为 **98/100（STRONG）**。

- 自动化验证：**27/27 通过**
- 六个审计域：**全部 PASS**
- 已知 Critical / High / Medium 问题：**0**
- YAML、JSON、Markdown 代码围栏、28 个 Shell 文件语法：**通过**
- `git diff --check`：**通过**
- root managed block revision：`1.2.4-20260711.1`
- 发布判断：逻辑上已达到可发布标准；`commit`、`push`、`tag` 仍须由人类明确触发

本报告已在 2026-07-11 针对当前未提交工作区重新执行完整验证。相比原验证批次，本次将 `tests/validate-feature-monthly-compaction-proposal.sh` 纳入全量测试，因此自动化验证总数由 26 增至 27；六域评分与发布判断均以本次重新执行的结果为准。

### 六域评分

| 审计域 | 权重 | 得分 | 结论 |
|---|---:|---:|---|
| Logic Correctness | 20% | 96 | PASS |
| Autonomy | 15% | 100 | PASS |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | 100 | PASS |
| Development / Test Workflow | 20% | 100 | PASS |
| Memory | 15% | 96 | PASS |
| Recommendation | 15% | 98 | PASS |
| **加权总分** | **100%** | **98.3，取整为 98** | **STRONG** |

## 2. 本轮修复结果

### 2.1 权威来源与 ADR 主流程

- `references/design.md` 与 `references/runtime.md` 已纳入发布包，Agent 不再依赖仓库外部上下文理解核心工作流。
- `Decision / ADR` 已进入 canonical flow，不再只是 root `AGENTS.md` 中的导航提示。
- ADR 被明确定位为复杂需求与 Feature 落地之间的可选决策桥梁：先确认需求目标和业务流程，再判断是否需要项目级决策，随后派生 Feature Spec。
- 当 accepted ADR、Decision Candidate、需求或实现发生不一致时，必须返回 `Drift Check / Decision Scan`，不得直接 `close` 或 `submit`。

### 2.2 Delivery Contract 与 Feature Gate

- 修复了 Technical Design 在 gate 通过前提前写入 Delivery Contract 的漏洞。
- `Requirement Checklist` 现在必须先于以下动作完成：
  - 接受 Feature Spec
  - 进入 Work Breakdown
  - 启动 Feature Auto-Loop
- 从聊天或需求讨论直接要求写 `product.md` 时，必须先确认 requirement source 或 Feature-start；不能因模板字段完整就绕过 Product Brief Source Gate。
- Direct Feature Spec 路径必须留下 readiness 记录，不能静默跳过需求与产品意图检查。

### 2.3 Root Guidance 与失败关闭

- root `AGENTS.md` 的 stage navigation 已覆盖完整主流程，并把 `Agent Ownership` 前置，强化 Agent 主动推进、主动调查和主动维护的责任。
- root fallback 改为 fail-closed：关键上下文、权限、依赖或证据不足时，不得凭推测继续写入。
- `Strict Mode` 下不允许自动放宽 gate。
- Suspend 状态不会继承或自动授予执行权限。
- root managed block revision 已更新为 `1.2.4-20260711.1`，用于识别本轮 Stage Map 与控制规则更新。

### 2.4 TDD 与执行控制

- 行为变更必须遵循 RED -> GREEN -> REFACTOR，不允许因人类选择而跳过 RED。
- 非行为变更可以将 TDD 标记为 `N/A`，但必须说明为什么不适用，不能把 `N/A` 当作绕过测试的通道。
- `Task Auto-Run` 在执行前会运行 Analyze Consistency，检查需求、决策、Feature Spec、任务与实现之间是否一致。
- `Plan Gate` 的 bypass 只适用于明确的、非行为型一次性操作，不适用于功能实现或行为修复。

### 2.5 路由与阻塞优先级

- 将 intent、workflow stage、permission、blocker 拆成正交判断轴，避免同一句人类指令同时命中多个互相冲突的入口。
- 阻塞条件按顺序处理：先确定意图和当前阶段，再检查 source/gate，再检查权限与运行条件，最后决定是否执行。
- `Project Entry`、`Review`、`Submit`、`Operational Support`、`Feature Follow-up` 的入口和退出条件已经对齐。
- 缺少访问权限或运行依赖时，归入 blocker 处理，不再与普通阶段路由混在一起。

### 2.6 Onboarding 与正式文档 Gate

- DDD Onboarding 现在分别检查 Spec 与 Tasks 的 `Full Execution Gate`，避免只生成其中一种文档便误判为可执行。
- Legacy focused update 不能绕过正式文档 gate。
- root Stage Map 已增加 onboarding 对应入口，并指向正确的详细 reference。
- `Project Entry` 的完成条件与退出路径已经统一。

### 2.7 Feature 生命周期与项目记忆

- 同一时刻只允许一个 `Active Feature`，与项目记忆中的单一活动指针保持一致。
- `Pause`、`Resume`、`Close`、`Reopen` 都必须更新 Feature 状态和项目记忆指针。
- skipped / deferred scope 必须留在 Feature 状态和完成判断中，不能在 close 时消失。
- 多 Phase 或部分实现需求会汇总为 `partially-implemented`，不会因为某个 Feature 完成就错误关闭整个 requirement。
- Durable facts、Delivery Phase、Requirement lifecycle 和 Feature mapping 发生变化时，会进入 `Project Memory Update / Requirement Reconciliation`。

### 2.8 Follow-up 与提交

- Bug、回归、QA 反馈和 post-close correction 默认先调查事实，再决定是否询问人类或创建后续 Feature。
- Follow-up 不会因“Feature 已关闭”而跳过需求、ADR 或 drift 检查。
- Submit / Integrate 的退出顺序已明确：先处理 blocker 和 drift，再完成验证与文档检查，最后才允许提交或集成。
- Feature Completion Check 与 Submit / Integrate 保持分离，避免“看起来做完”直接等价于“可以提交”。

## 3. 专项与回归测试

本轮增加了以下专项验证：

| 测试文件 | 主要覆盖内容 |
|---|---|
| `tests/validate-v1.2.4-critical-control-repairs.sh` | ADR 权威来源、Delivery Contract gate、root fallback、TDD RED 控制 |
| `tests/validate-v1.2.4-state-lifecycle-repairs.sh` | Active Feature、Pause/Resume/Close/Reopen、Phase 汇总、记忆指针 |
| `tests/validate-v1.2.4-root-stage-coverage.sh` | root Stage Map 的阶段完整性、Read Next 索引与 managed revision |
| `tests/validate-v1.2.4-postfix-pressure-repairs.sh` | 修复后的压力场景、路由冲突、follow-up、submit 与 drift 闭环 |
| `tests/validate-feature-monthly-compaction-proposal.sh` | 月度压缩讨论草案的模式、安全 Gate、索引关系和历史保留约束 |

全量测试共 **27 项，27 项通过**。这些测试既检查文档结构，也检查关键规则是否以可检索、不可歧义的方式存在。

其中 `validate-feature-monthly-compaction-proposal.sh` 验证的是 `docs/proposal/v1.2.x/feature-monthly-compaction.md` 讨论草案的契约完整性。该提案仍是历史/设计讨论材料，不是 `SKILL.md`、`references/runtime.md` 或 `references/design.md` 中已经发布的运行时能力；本报告不据此宣称 Feature Monthly Compaction 已实现。

## 4. 修复后压力场景

| 场景 | 预期行为 | 结果 |
|---|---|---|
| 人类提出复杂跨 Feature 需求 | 先完成 Requirement Grill，再触发 Decision Scan | PASS |
| Requirement 已接受但存在架构、数据或长期取舍 | 进入 `Decision / ADR`，不直接拆 Feature | PASS |
| 简单局部需求且无跨 Feature 决策 | ADR 可判定为不需要，并记录理由 | PASS |
| 从聊天直接要求生成 `product.md` | 先确认 requirement source 或 Feature-start | PASS |
| Technical Design 尚未通过 gate | 不得提前写 Delivery Contract | PASS |
| 行为变更被要求“先写代码，之后补测试” | 必须保留 RED，不能由人类授权跳过 | PASS |
| 非行为文档改动 | 可标记 TDD `N/A`，同时记录理由 | PASS |
| 当前已有 Active Feature，又请求开始新 Feature | 先完成、暂停或切换现有 Feature | PASS |
| Feature 被 Pause | 同步更新状态与项目记忆指针 | PASS |
| 某 Phase 完成但后续 Phase deferred | Requirement 汇总为 `partially-implemented` | PASS |
| 实现与 accepted ADR 不一致 | 回到 `Drift Check / Decision Scan` | PASS |
| Feature close 后发现回归 | 先调查，再决定 reopen 或 follow-up | PASS |
| 请求 commit / PR / merge | 先完成 Completion、Drift、文档和验证检查 | PASS |
| 缺少访问权限或运行依赖 | 作为 blocker 失败关闭，不推测执行 | PASS |
| Suspend 后再次收到执行指令 | 不继承旧授权，重新判断当前权限 | PASS |
| 进入陌生项目且无可靠记忆 | 进入 Project Entry Scan / Onboarding | PASS |
| 需求阶段或 Feature mapping 改变 | 更新项目记忆并做 Requirement Reconciliation | PASS |
| 普通讨论且无产物或实施意图 | 保持 Chat，不创建工作流产物 | PASS |
| 月度压缩提案存在且测试通过 | 只确认 proposal 契约完整，不把草案误判为已发布运行时能力 | PASS |

## 5. 已验证的不变量

- Requirement 是业务目标、范围、约束和验收方向的 source of truth。
- Project Decision / ADR 记录跨 Feature、长期有效或高代价的项目级决策。
- Feature Spec 是从 accepted requirement 与相关 decision 派生的实现边界，不反向取代 Requirement。
- Product Brief 不能脱离 requirement source 或明确的 Feature-start confirmation 创建。
- accepted ADR 与实现不一致时，必须先解决 drift。
- 同一时刻只能有一个 Active Feature。
- Feature 状态变化必须同步更新项目记忆。
- 部分 Phase 完成不等于整个 Requirement 完成。
- 行为变更不能跳过 TDD RED。
- Agent 应先调查可获得的事实，再把真正需要裁决的问题交给人类。
- Root Stage Map 只负责导航；详细阶段过程由对应 reference 负责。
- root guidance 不能成为发布包内权威规则的唯一载体。

## 6. 修复前基线

以下内容是修复前的历史基线，用于说明本轮为什么需要调整。它们**不是当前仍存在的问题**。

### 6.1 基线结果

- 综合评分：**61/100（C / FRAGILE）**
- 机械检查：**22/22 通过**
- 语义检查：**失败**
- Critical：**4**
- High：**6**
- Medium：**9**

当时的主要问题不是 Markdown、YAML 或 Shell 是否能被解析，而是规则之间存在冲突、入口不完整、gate 可以被绕过，以及生命周期无法形成闭环。

### 6.2 Critical 基线问题

| 编号 | 修复前问题 | 风险 |
|---|---|---|
| C1 | ADR Lane 没有进入 governing design sources | root 提到了 ADR，但 skill 的权威流程无法稳定发现和执行 |
| C2 | Technical Design 可在 gate 前写 Delivery Contract | Agent 可能把未接受的设计当作已确认交付约束 |
| C3 | root fallback 不完整且倾向继续执行 | 缺少可靠上下文时可能猜测阶段、权限或项目事实 |
| C4 | 验证规则允许人类选择跳过 RED | 行为变更可能绕过 TDD 的失败证据 |

### 6.3 High 基线问题

| 编号 | 修复前问题 | 风险 |
|---|---|---|
| H1 | Entry classification 入口重叠 | 同一信号可能路由到不同阶段 |
| H2 | Onboarding 可绕过正式文档 gate | Spec 或 Tasks 不完整时仍可能开始实施 |
| H3 | 允许多个 Active Feature，但记忆只有单指针 | Feature 状态和项目记忆无法一致 |
| H4 | skipped / deferred 与 close 规则冲突 | 未交付范围可能在关闭时丢失 |
| H5 | 多 Phase requirement 缺少 roll-up | 一个 Feature 完成可能误判整个需求完成 |
| H6 | Follow-up 的 ask-human 与 investigate-first 冲突 | Agent 可能过早把可自行调查的问题抛给人类 |

### 6.4 Medium 基线问题

| 编号 | 修复前问题 | 修复方向 |
|---|---|---|
| M1 | root Stage Map 没有 onboarding 路由 | 增加 Project Entry / DDD Onboarding 入口 |
| M2 | Project Entry 的退出条件不一致 | 统一进入正式工作流前的完成条件 |
| M3 | Execute helper 被错误收窄为仅行为变更 | 区分执行流程与 TDD 适用性 |
| M4 | Review 入口定义不一致 | 对齐 implementation-ready 与 review-ready |
| M5 | Feature 流程漏掉 Requirement Checklist | 在 Spec 接受和执行前设为硬 gate |
| M6 | Direct Feature Spec 没有 readiness record | 要求留下 source 与 readiness 证据 |
| M7 | Pause 没有更新活动指针 | 明确生命周期与记忆同步 |
| M8 | Submit 存在重叠退出路径 | 固定 blocker、drift、verification、submit 顺序 |
| M9 | `accepted` 的使用语义含糊 | 区分 requirement、decision、spec 各自的接受状态 |

## 7. 未采纳或降级的评测意见

| 候选意见 | 处理结果 | 原因 |
|---|---|---|
| Plan Gate 可以被任意 bypass | 不作为独立问题采纳 | `runtime` bypass 仅允许非行为型、一次性操作；功能实现仍受 gate 控制 |
| Missing access 应单列为新阶段 | 合并进 routing / blocker 修复 | 它是执行阻塞条件，不是独立业务阶段 |
| Human interruption 应成为独立 finding | 不单独计分 | 已由 Suspend、Resume 与授权重新判断覆盖 |
| 所有文档必须包含字面字段 `Why` | 不计分 | 评估的是决策理由是否可追溯，不要求固定英文标题 |
| Enterprise memory 一定存在 duplicate truth | 不计分 | 没有足够证据证明当前实现形成双重权威来源 |

## 8. 原修复优先级及完成状态

以下是基线报告给出的修复顺序，目前均已完成。

### P0：控制面与权威来源

- 将 ADR 纳入 canonical design/runtime。
- 修复 Delivery Contract pre-write gate。
- 将 root fallback 改为 fail-closed。
- 禁止行为变更跳过 RED。

状态：**完成并有回归测试覆盖**。

### P1：状态机与路由一致性

- 正交化 intent、stage、permission、blocker。
- 统一 Active Feature 模型。
- 补齐 Pause/Resume/Close/Reopen 记忆更新。
- 建立 Requirement Phase 与 Feature 状态汇总。
- 修复 onboarding、follow-up 和 submit 的 gate 顺序。

状态：**完成并有回归测试覆盖**。

### P2：导航与可维护性

- 补齐 root Stage Map 的阶段入口和 Read Next 索引。
- 对齐 Project Entry、Review、Feature Spec 等术语。
- 增加关键跨文件不变量测试。
- 更新 managed block revision。

状态：**完成并有回归测试覆盖**。

## 9. 最终判断

v1.2.4 已从“机械检查通过但语义脆弱”的 **61/100 FRAGILE**，提升为“关键路径闭环、冲突可判定、状态可追踪”的 **98/100 STRONG**。本次重新验证确认 27/27 自动化测试通过，六域语义结论保持不变。

当前剩余的 2 分主要来自文档型系统不可完全消除的解释空间，以及未来新增阶段或 reference 时仍需要同步维护索引和回归测试。现有规则已经通过 Stage Map 覆盖、权威来源约束和测试断言降低了漂移风险。

本报告审计的是当前未提交工作区。它可以作为提交前验收证据，但不能代替人类对 `commit`、`push` 或 `tag` 的明确授权。
