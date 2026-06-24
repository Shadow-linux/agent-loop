# Proposal: Chat 与 Requirements Discussion Entry

状态：已实施，待提交

目标版本：v1.2.x

创建时间：2026-06-24

默认语言：中文

## 背景

当前 `agent-loop` 的 Entry Classification 能识别项目状态和工作类型，例如：

- `new-project`
- `existing-project`
- `resume`
- `operational-support`
- `feature-follow-up`
- `blocked`

但它缺少两个常见的人类入口：

1. **chat**：普通讨论、规则咨询、状态确认、设计闲聊；
2. **requirements-discussion**：人类正在聊产品需求、业务目标、功能想法、约束和取舍，但尚未授权开始实现。

这会导致 Agent 容易把普通聊天或需求讨论误路由到 Feature Spec、Work Breakdown、Plan 或 Execute。

更严重的是，当前流程虽然有 Requirement Archive、Brainstorm / Clarify、Product Brief 和 Feature Spec，但缺少一条明确路径：

```text
requirements-discussion
-> Brainstorm / Clarify
-> human-reviewed requirement document
-> .agent-loop/requirements/<date-topic>/
-> later feature references requirement set
```

## 目标

新增两个入口意图：

1. `chat`
2. `requirements-discussion`

目标效果：

- 普通聊天不会被误当成 feature 构建；
- 聊需求不会被误当成普通 chat 而丢失；
- 聊需求不会跳过 requirements 管理直接进入 feature workspace；
- 经过头脑风暴产生的需求文档统一归入 `.agent-loop/requirements/`；
- 后续开始实现时，feature 只引用 requirement set，并从需求派生 `product.md` / `spec.md`。

## 非目标

本 proposal 不做以下事情：

- 不把所有聊天都强制进入 agent-loop；
- 不把 `requirements/` 变成 issue tracker；
- 不允许 Agent 自动开始实现；
- 不允许 Agent 把需求生命周期放到 feature docs；
- 不允许 Agent 把需求待办写入 `project.md`；
- 不改变现有 Feature Spec、Product Brief、Work Breakdown、Plan Gate 的职责；
- 不要求立即实现真实 runtime hook。

## 核心原则

```text
chat answers or discusses.
requirements-discussion shapes demand into requirements.
requirements/ owns requirement source and lifecycle.
features/ implement accepted requirements.
```

## Entry Intent 分层

建议在 Project Entry / Runtime Classification 前增加一层轻量 Message Intent 判断。

```text
Message Intent
-> chat
-> requirements-discussion
-> feature-request
-> operational-support
-> feature-follow-up
-> deferred-requirement
-> project-entry / resume / other runtime state
```

`chat` 和 `requirements-discussion` 是消息意图，不是项目状态。

项目状态仍由现有 Entry Classification 负责。

## Chat Entry

### 定义

`chat` 表示人类当前主要是在交流、询问、确认、讨论概念或查看状态，没有要求沉淀需求，也没有要求开始构建。

典型输入：

- “现在规则是什么？”
- “你觉得这个设计合理吗？”
- “这种情况是不是应该加 hook？”
- “我想先问个问题。”
- “这个会不会影响 Agent 自主性？”
- “先别改，先说说你的看法。”

### 默认行为

当消息被判断为 `chat`：

1. 直接回答或讨论；
2. 可以读取相关文档帮助解释；
3. 不创建 feature；
4. 不创建 requirement set；
5. 不进入 Work Breakdown / Plan / Execute；
6. 如果讨论逐渐变成需求，应转为 `requirements-discussion`；
7. 如果人类明确要求“开始做”，再转为 `feature-request`。

## Requirements Discussion Entry

### 定义

`requirements-discussion` 表示人类正在表达或探索需求，但还没有授权开始实现。

典型输入：

- “我们聊一下这个需求。”
- “我想做一个能力，让 Agent 进来先区分聊天和需求。”
- “这个功能应该支持几种场景？”
- “用户如果只是咨询，不应该进 feature；如果在聊需求，应该产出需求文档。”
- “先把需求梳理清楚，不要开始实现。”

### 默认路径

`requirements-discussion` 的默认路径是：

```text
requirements-discussion
-> Brainstorm / Clarify
-> Requirement Document Draft
-> Human Review
-> .agent-loop/requirements/<archive-date>-<topic>/
```

关键点：

- 先头脑风暴，再写需求文档；
- 需求文档必须经过人类 review；
- 确认后的需求文档归入 `.agent-loop/requirements/`；
- 不创建 feature workspace，除非人类明确说开始实现；
- 不进入 Work Breakdown / Plan / Execute。

## Brainstorm / Clarify 在聊需求中的职责

当进入 `requirements-discussion`：

1. 使用 Brainstorm / Clarify 方法；
2. 如果可用，加载 brainstorming / product discovery helper；
3. 只问会影响需求质量的问题；
4. 优先一问一答，必要时短列表；
5. 澄清背景、用户、目标、约束、非目标、验收方向；
6. 形成可审阅需求文档；
7. 不把 brainstorm 输出直接当作 feature spec。

## Requirement Document

### 默认落点

需求文档应归入 requirement set：

```text
.agent-loop/requirements/<archive-date>-<topic>/
  README.md
  requirement.md
```

`requirement.md` 是经 brainstorm 形成、由人类确认的需求文档。

创建后，它是 requirement source material。后续不应静默改写。

生命周期、状态和实现关系写入：

```text
.agent-loop/requirements/<archive-date>-<topic>/README.md
.agent-loop/requirements/INDEX.md   # optional
```

### 推荐结构

```md
# Requirement: <topic>

Status: proposed | accepted | deferred | rejected | reference-only
Created: YYYY-MM-DD
Source: conversation

## Background

## Problem

## Users / Operators

## Goals

## Requirements

## Non-goals

## Constraints / Assumptions

## Acceptance Direction

## Open Questions

## Source Conversation Summary
```

## Requirements 与 Feature 的关系

需求永远在 `.agent-loop/requirements/` 管理。

Feature docs 只引用和派生：

```text
requirements/<date-topic>/requirement.md
-> features/<feature>/product.md
-> features/<feature>/spec.md
```

`product.md` 和 `spec.md` 不是需求管理源：

- `product.md` 是当前 feature 的产品理解；
- `spec.md` 是当前 feature 的工程规格；
- requirement set 才拥有需求来源、生命周期、状态和后续变更历史。

如果需求后续变化：

- 追加 source material 到同一个 requirement set，或
- 当变化和原需求冲突较大时，新建 requirement set / supersede old set，
- 不直接重写旧 `requirement.md`。

## Deferred Requirement

如果人类说：

- “先记一下”
- “以后做”
- “下一轮补”
- “暂时不做”
- “backlog”
- “defer this”

仍然归入 `.agent-loop/requirements/`。

区别只是 status 通常是：

```text
deferred
```

而不是 active feature。

## Chat 与 Requirements Discussion 的分界

| 输入 | 默认分类 | 行为 |
|---|---|---|
| “现在规则是什么？” | `chat` | 解释规则，不写 artifact |
| “你觉得还缺什么？” | `chat` 或 `requirements-discussion` | 如果只是问看法则 chat；如果在塑造能力则 requirements-discussion |
| “我们聊一下这个需求” | `requirements-discussion` | Brainstorm 后形成需求文档 |
| “先把需求文档写出来” | `requirements-discussion` | 写 requirement set，不建 feature |
| “这个先记一下以后做” | `deferred-requirement` | 写 requirement set，status deferred |
| “开始实现这个需求” | `feature-request` | 从 requirement set 派生 feature |

如果无法判断，Agent 应问：

```text
你是想普通讨论一下，还是想把这个梳理成 requirements 下的需求文档？
```

如果无法判断是需求讨论还是开始实现，Agent 应问：

```text
你是想先形成需求文档，还是现在就开始进入 feature 构建？
```

## 与现有阶段的关系

### Requirement Archive

保留。

但它需要支持两种来源：

1. 人类提供的外部/原始需求材料；
2. requirements-discussion 经过 brainstorm 形成、经人类确认的需求文档。

### Product Brief If Needed

保留。

但它不拥有需求生命周期。

Product Brief 只在准备 feature 时，从 requirement set 派生产品理解。

### Feature Spec

保留。

但 Feature Spec 不能替代需求文档。

Feature Spec 应记录 Source Requirements，链接到 requirement set。

### Project Memory

不变。

`project.md` 不记录 future TODO、backlog、deferred requirements 或需求正文。最多记录当前 active feature 或 requirement set 指针。

## 建议实现范围

如果本 proposal 被接受，建议修改：

- `references/runtime.md`
- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/requirement-management.md`
- `references/document-templates.md`
- `references/validation-scenarios.md`
- `SKILL.md`
- README / Usage
- root `AGENTS.md` managed block template

建议新增：

- `tests/validate-chat-requirements-entry.sh`

可选新增：

- `templates/requirement.md`

但如果想继续保持模板轻量，也可以只增强 `templates/requirement-set-README.md`，并把 `requirement.md` 作为自由格式 source file。

## Validation Scenarios

### Scenario A: Normal chat

Prompt:

```text
现在 agent-loop 的 Complex Mode 是什么规则？
```

Expected:

- classify message intent as `chat`
- answer only
- do not create requirement set
- do not create feature workspace
- do not enter Work Breakdown / Plan / Execute

### Scenario B: Requirements discussion

Prompt:

```text
我们聊一下需求：Agent 进来的时候应该区分普通聊天和聊需求。聊需求时要经过头脑风暴产生需求文档，先不要实现。
```

Expected:

- classify message intent as `requirements-discussion`
- use Brainstorm / Clarify behavior
- ask only requirement-shaping questions
- produce a requirement document draft
- recommend archiving confirmed document under `.agent-loop/requirements/<date-topic>/`
- do not create feature workspace
- do not enter Work Breakdown / Plan / Execute

### Scenario C: Requirements document request

Prompt:

```text
先把这个需求整理成需求文档，不要开始开发。
```

Expected:

- classify as `requirements-discussion`
- write requirement document after sufficient clarification
- store under requirement set after human confirmation
- set status to `proposed` or `accepted` based on human decision
- do not create feature docs unless human later says start implementation

### Scenario D: Start implementation from requirement

Prompt:

```text
开始实现刚刚那个 chat entry 需求。
```

Expected:

- find or ask for the relevant requirement set
- create feature workspace only after human confirms implementation
- feature `spec.md` references Source Requirements
- requirement set remains the demand source and lifecycle owner

### Scenario E: Ambiguous chat vs requirements discussion

Prompt:

```text
你觉得这个入口还应该怎么设计？
```

Expected:

- if context is only conceptual, classify as `chat`
- if context shows the human is shaping a product/workflow capability, ask whether to keep discussing or form a requirements document
- do not silently create feature

## Open Questions

1. `requirements-discussion` 是否应该写进正式 Entry Classification 表，还是作为 Message Intent 层？
2. `requirement.md` 是否要模板化，还是保持自由格式 source material？
3. 经 brainstorm 形成的需求文档默认 status 是 `proposed` 还是由人类选择？
4. 当需求讨论发生在 active feature 中，是否默认追加到当前 feature notes，并询问是否建立独立 requirement set？
5. 是否需要一个 `requirements-discussion` 的 Human Review Summary 表？

## 推荐决策

建议采用 Message Intent 层，而不是把 `chat` / `requirements-discussion` 混进项目状态层。

推荐路径：

```text
Message Intent
-> chat: answer-only
-> requirements-discussion: brainstorm -> requirement document -> requirements/
-> feature-request: feature workflow
```

这样可以保持边界清楚：

- chat 不沉淀；
- requirements-discussion 沉淀需求；
- feature-request 才进入实现。
