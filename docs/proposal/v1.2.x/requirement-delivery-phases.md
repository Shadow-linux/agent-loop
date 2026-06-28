# Proposal: Requirement Delivery Phases

状态：讨论草案
目标版本：v1.2.x
创建时间：2026-06-28

## 目的

这份 proposal 讨论 `agent-loop` 在较复杂需求中如何建议使用 `Delivery Phases`，让人类先确认需求落地节奏，再逐步转换为 feature 实施。

它要解决的问题不是工程任务拆分，而是需求阶段的人类可理解交付路线：

- 这个需求是否太大，需要分期；
- 当前应该先做哪一段；
- 每一段包含什么、不包含什么；
- 做到什么算这一段完成；
- 哪一段已经转成 feature；
- 哪些后续能力应保持 deferred/backlog，而不是塞进 `project.md`。

## 核心观点

```text
Requirement owns demand and delivery intent.
Delivery Phases express human-readable delivery slices.
Feature owns implementation scope for one accepted phase or phase slice.
Tasks own engineering execution.
```

`Delivery Phases` 是 requirement 层的可选能力。Agent 应在复杂需求中建议使用，但不能强制每个需求都分 phase。

## 为什么需要 Phase

当前 `requirements/` 已经支持 lifecycle/backlog：

```text
proposed | accepted | deferred | in-progress | implemented | superseded | rejected | reference-only
```

这能表达需求状态，但不能表达一个大需求如何逐段落地。

例如 `pigeon_cli MVP` 这类需求既包含 runtime、permission、model、TUI、history、memory、build release、E2E acceptance 等多个交付段，又需要让人类知道当前阶段在哪里。仅靠一个 requirement status 会过粗，直接进入 feature 又会过早工程化。

`Delivery Phases` 补的是中间层：

```text
Requirement lifecycle = 这个需求现在是什么状态。
Delivery Phases = 这个需求分几步交付，每步做什么。
Feature = 其中一步进入实施后的工作区。
```

## 反目标

`Delivery Phases` 不做这些事：

| 不做什么 | 原因 |
|---|---|
| 不替代 `feature/spec.md` | phase 是需求分期，不是工程行为规范 |
| 不替代 `tasks.md` | phase 面向人类交付节奏，tasks 面向工程执行 |
| 不创建新的 `.agent-loop/phases/` 目录 | 第一版保持 requirement set 目录稳定 |
| 不引入 roadmap graph | v1.x 先用 Markdown 表达，避免复杂图谱系统 |
| 不要求每个 requirement 都分 phase | 小需求直接 requirement -> feature 即可 |
| 不把 future work 写入 `project.md` | deferred/backlog 仍属于 requirements/INDEX 或 requirement README |

## 触发条件

Agent 应建议使用 `Delivery Phases`，当任一条件成立：

| 触发信号 | 为什么建议 phase |
|---|---|
| 一个需求明显会拆成多个 feature | 人类需要先确认交付顺序 |
| 需求包含 MVP / 后续增强 / Post-MVP | 需要区分当前范围和未来范围 |
| 需求有多个用户旅程、角色、权限或业务对象 | 一次性进入 spec 会过大 |
| 需求跨多个技术边界，如前端、后端、支付、权限、运营后台 | 需要先定义阶段边界 |
| 人类说“先做核心闭环，后面再补” | 这是天然 phase 信号 |
| 人类说“这个先记一下/后面做/下一轮做” | 需要 deferred phase 或 backlog 记录 |
| feature 开始前发现 scope 太大 | 先回到 requirement phase，避免 feature 爆炸 |
| 已有 requirement README 变成长 roadmap | 应把散落状态收敛成 Delivery Phases 表 |

不建议 phase 的情况：

| 场景 | 推荐路径 |
|---|---|
| 小 bugfix | 直接 maintenance-fix feature |
| 清晰小技术任务 | requirement -> spec |
| 单一用户故事且一次能交付 | 不需要 phase |
| 只是原始材料归档 | 只建 requirement set |
| 人类明确不想做文档整理 | 保持 chat 或普通 requirement archive |

## Artifact 位置

第一版不改变 requirements 目录结构。

推荐结构：

```text
.agent-loop/
  requirements/
    YYYY-MM-DD-<topic>/
      README.md
      requirement.md
      notes.phase-<n>-<slug>.md
      prototype.*
      feedback.*
      change-request.*
  features/
    YYYY-MM-DD-<feature-slug>/
      product.md
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
```

职责分工：

| 文件 | 负责 | 不负责 |
|---|---|---|
| `requirements/<set>/README.md` | lifecycle、Delivery Phases、Feature Mapping、状态历史 | 详细工程执行计划 |
| `requirements/<set>/requirement.md` | 人类确认后的需求来源材料 | 后续状态流转、实现进度 |
| `requirements/<set>/notes.phase-*.md` | 某个 phase 的补充确认、参考方向、约束 | 替代正式 feature spec |
| `features/<feature>/spec.md` | 某个 phase 转实施后的工程行为规范 | 拥有 requirement lifecycle |

## README 标准章节

建议在 requirement set `README.md` 中新增：

```md
## Delivery Phases

| Phase | Goal | Scope | Out Of Scope | Acceptance Direction | Status | Feature Mapping | Source Notes |
|---|---|---|---|---|---|---|---|
| Phase 1: MVP | 先闭环核心流程 | <本阶段包含> | <明确不做> | <完成方向> | accepted | none | none |
```

字段说明：

| 字段 | 含义 |
|---|---|
| `Phase` | 阶段编号和人类可读名称 |
| `Goal` | 这一阶段要达成的业务/产品目标 |
| `Scope` | 这一阶段包含的能力边界 |
| `Out Of Scope` | 明确不在本阶段做的内容 |
| `Acceptance Direction` | 人类能理解的完成判断，不要求等同测试用例 |
| `Status` | `proposed | accepted | deferred | in-progress | implemented | rejected | superseded` |
| `Feature Mapping` | 已转 feature 的路径，未转则 `none` |
| `Source Notes` | phase note、原型、反馈或 change request |

Status 与 requirement lifecycle 使用同一组状态词，避免另造一套词汇。

## Phase Note

当某个 phase 有较多补充设计、参考、截图、交互细节或人类确认，可以追加独立 note：

```text
requirements/<set>/notes.phase-11-tui-polish.md
requirements/<set>/notes.phase-13-input-attachments-paste.md
```

Phase note 推荐结构：

```md
# Phase <N> Note: <Title>

Recorded: YYYY-MM-DD
Status: proposed | accepted | deferred | superseded
Feature: not created | .agent-loop/features/<feature>/
Activation Gate: <什么时候转 feature>

## Goal

## Human Decisions

## Scope Direction

## Out Of Scope

## Acceptance Direction

## Conversion Rule
```

Phase note 是 requirement source material 的一部分。正式进入实现时，feature `spec.md` 必须把对应 note 列入 `Source Requirements`。

## Phase 到 Feature 的转换规则

一个 phase 不等于一个 feature，但它可以映射到一个或多个 feature。

推荐规则：

| 情况 | 转换方式 |
|---|---|
| phase 范围清晰且可一次交付 | 创建一个 feature |
| phase 仍然过大 | 先拆出一个 phase slice，再创建 feature |
| phase 涉及多个项目或 durable contract | 创建 group-level feature 或 delivery contract |
| phase 是未来增强 | 保持 `deferred`，不创建 feature |
| phase 被后续方向替代 | 标记 `superseded`，链接新 phase 或 requirement set |

Feature `spec.md` 应引用 phase：

```md
Source Requirements:
- Requirement Set: `.agent-loop/requirements/<date-topic>/README.md`
- Delivery Phase: `Phase 3: <name>`
- Phase Note: `.agent-loop/requirements/<date-topic>/notes.phase-3-<slug>.md`
```

Requirement README 应回写 mapping：

```md
| Phase 3: <name> | ... | in-progress | `.agent-loop/features/<feature>/spec.md` | `notes.phase-3-<slug>.md` |
```

## Stage 接入点

建议在这些阶段运行轻量 Phase Scan：

| Stage | 行为 |
|---|---|
| Requirements Discussion | 当需求变大时，建议人类确认 Delivery Phases |
| Requirement Archive | 归档复杂需求时，在 README 写入初版 Delivery Phases |
| Product Brief If Needed | 如果产品范围仍过大，回到 requirement phase 先收敛交付顺序 |
| Feature Spec | 创建 feature 前确认它来自哪个 phase 或 phase slice |
| Work Breakdown | 如果 feature 任务过大，检查是否应退回 phase/scope split |
| Drift Check / Close Feature | 更新 phase status 和 Feature Mapping |
| Requirement Reconciliation | feature close 后把 phase 标为 implemented/in-progress/deferred |

## Human Gate

Agent 可以主动建议 phase，但以下动作需要人类确认：

- 创建或重排 Delivery Phases；
- 把 phase status 改为 `accepted`、`deferred`、`rejected`、`superseded`；
- 把某个 phase 转成 feature；
- 把一个 active feature 拆回 phase；
- 更改已经 accepted 的 phase scope/out-of-scope；
- 将 future/post-MVP 内容移入当前 phase。

Agent 可以自主做的轻量动作：

- 在总结中提示“这个需求建议拆 phase”；
- 草拟 phase 表供人类审阅；
- 在 feature spec 中引用已确认 phase；
- 在 close/drift 总结中建议更新 phase 状态。

## 示例

```md
## Delivery Phases

| Phase | Goal | Scope | Out Of Scope | Acceptance Direction | Status | Feature Mapping | Source Notes |
|---|---|---|---|---|---|---|---|
| Phase 1: MVP | 先闭环核心流程 | 充值、余额、预冻结、扣费 | 发票、复杂退款 | 能完成一次充值到扣费闭环 | accepted | `.agent-loop/features/2026-06-28-wallet-mvp/spec.md` | none |
| Phase 2: Reliability | 补齐异常恢复 | 对账、补偿任务、告警 | 财务报表 | 异常 reservation 可恢复 | deferred | none | `notes.phase-2-reliability.md` |
| Phase 3: Operations | 运营和财务管理 | 后台查询、人工冲正、报表 | 自动风控 | 能支持人工排查 | proposed | none | none |
```

## 与现有设计的关系

这份 proposal 不改变 `agent-loop` 核心目录模型。

它扩展的是 requirement set README 的表达能力：

```text
requirements/ = source material + lifecycle/backlog + optional Delivery Phases
features/ = implementation workspaces
product.md = feature-level product intent when needed
spec.md = feature behavior specification
tasks.md = engineering breakdown
```

它也不替代 `product.md`：

```text
Delivery Phases 说明大需求怎么分期。
product.md 说明当前 feature 的产品意图。
spec.md 说明当前 feature 具体实现行为。
```

## 后续落地建议

如果这份 proposal 被接受，后续应更新：

- `templates/requirement-set-README.md`：增加 `Delivery Phases` 章节；
- `references/requirement-management.md`：增加 Phase Scan 触发和规则；
- `references/stage-guides.md`：在 Requirements Discussion、Requirement Archive、Feature Spec、Drift Check 增加 phase routing；
- `references/document-templates.md`：增加 phase 表和 phase note 模板；
- `workflow-checklists.md`：增加复杂需求是否建议 phase 的检查项；
- `Usage.md`：增加人类如何使用 phase 的说明。

## 待讨论问题

- Phase status 是否完全复用 requirement status，还是需要 `planned` / `active` 等更人类化状态？
- Phase note 是否应命名为 `notes.phase-<n>-<slug>.md`，还是 `phase-<n>-<slug>.md`？
- 一个 phase 映射多个 feature 时，`Feature Mapping` 用逗号列表还是单独表？
- 是否允许 requirement.md 中也包含初始 Delivery Phases，还是统一只在 README 维护？
- 当 phase scope 变化较大时，是更新同一 phase，还是创建新 phase 并 supersede？
