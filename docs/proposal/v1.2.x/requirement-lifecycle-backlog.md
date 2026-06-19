# Proposal: Requirement Lifecycle / Backlog

状态：讨论草案

目标版本：v1.2.3

创建时间：2026-06-19

默认语言：中文

## 背景

`agent-loop` 当前的 project memory 语义基本正确：

- `.agent-loop/project.md` 保存长期项目事实、当前工作状态、恢复入口和稳定规则；
- feature `notes.md` 保存历史审计、handoff、决策过程和执行证据；
- `.agent-loop/requirements/` 保存人类原始需求材料或其引用。

问题不在 project memory，而在 requirement archive 的调用能力偏弱。

当人类说“这个先记一下”“后面做”“下一轮补”，或者 Agent 在 feature 开发中发现后续需求时，当前规则没有一个足够明确、轻量的需求待办落点。Agent 容易把这类“未来需求 / 暂缓事项 / 待开发意图”写进 `project.md` 的 planned/current/next 区域，导致 project memory 变成便利贴墙。

这类内容不应进入长期项目事实；它应该进入 requirement lifecycle。

## 目标

本 proposal 目标是增强 `requirements/`，让它承担“需求记忆”和“待办索引”的职责：

1. 让未来需求、暂缓需求、已接受但未实现需求有明确落点；
2. 避免把 future TODO、backlog、planned capability 明细写进 `project.md`；
3. 让 feature close 时能更新需求状态，而不是遗留无用 planned 记录；
4. 让后续“开始做之前那个 X”可以从 requirements 召回；
5. 保持 requirement 系统轻量，不新增一批细碎模板。

## 非目标

本 proposal 不做以下事情：

- 不重做 project memory 模型；
- 不新增 `.agent-loop/backlog.md`；
- 不新增独立 `requirement.md`、`feedback.md`、`change-request.md`、`deferred-requirement.md`、`bug-report.md`、`backlog-item.md` 模板；
- 不把 requirements 变成完整 issue tracker、Jira 或 task 系统；
- 不允许 Agent 改写人类原始需求材料；
- 不替代 feature `spec.md`、`tasks.md`、`tests.md`、`plan.md`；
- 不改变 Feature Follow-up / Flow-back 的 bug/change 归属判断。

## 核心观点

```text
project.md 记录项目已经是什么。
requirements/ 记录人类曾经要求、接受、暂缓、拒绝、实现过什么。
feature notes.md 记录当时为什么这么做。
```

未来需求和暂缓需求是 requirement lifecycle，不是 project memory。

## Artifact 职责边界

| Artifact | 负责 | 不负责 |
|---|---|---|
| `.agent-loop/project.md` | 长期项目事实、当前工作指针、恢复入口、稳定能力、稳定规则 | future TODO、backlog 明细、未实现 planned capability |
| `.agent-loop/requirements/<set>/README.md` | 单个需求集合的来源、状态、生命周期、关联 feature | feature 规格、执行计划、任务拆分 |
| `.agent-loop/requirements/INDEX.md` | requirement inventory、backlog/deferred 视图、实现状态索引 | 原始需求正文、任务管理 |
| `features/<feature>/notes.md` | 过程证据、handoff、决策历史、发现后续需求的上下文 | 跨 feature 待办池 |
| `features/<feature>/spec.md` | 当前 feature 行为、验收、scope、source requirements | 原始需求归档 |

## Requirement Set 生命周期

扩展 requirement set 的 `Status`。

当前状态：

```text
active | superseded | reference-only
```

建议改为：

```text
proposed | accepted | deferred | in-progress | implemented | superseded | rejected | reference-only
```

状态含义：

| Status | 含义 |
|---|---|
| `proposed` | 人类提过，但尚未确认要做 |
| `accepted` | 已确认要做，但尚未进入 feature |
| `deferred` | 暂缓，未来可能做 |
| `in-progress` | 已进入某个 active feature |
| `implemented` | 已由 feature 实现 |
| `superseded` | 被新需求替代 |
| `rejected` | 明确不做 |
| `reference-only` | 仅作为背景材料 |

## Requirement Set README 增强

只增强现有 `templates/requirement-set-README.md`。

建议结构：

```md
# Requirement Set: <Topic>

Archived: YYYY-MM-DD
Topic: <topic-slug>
Status: proposed | accepted | deferred | in-progress | implemented | superseded | rejected | reference-only

## Date Meaning

- The date is the archive date only.
- It is not a deadline, feature duration, implementation start date, or implementation end date.

## Lifecycle

Intake Type: human-request | follow-up | deferred-from-feature | ops-discovery | bug-report | idea | reference
Decision: proposed | accepted | deferred | rejected | converted-to-feature | implemented | superseded
Priority: unset | low | medium | high
Owner Feature:
Implemented By:
Superseded By:
Last Reviewed:
Exit Condition:

## Summary

One-line summary:

## Source Files

- Requirement:
- Prototype:
- Feedback:
- Screenshots:
- Recordings:
- Links:
- Change Requests:
- Other:

## Original Sources

-

## Used By

- `.agent-loop/features/<feature>/spec.md`

## Status History

- YYYY-MM-DD:
  - Status:
  - Reason:
  - Human Decision:

## Notes

-
```

### Source 文件仍保持自由

不新增这些模板：

- `requirement.md`
- `feedback.md`
- `change-request.md`
- `deferred-requirement.md`
- `bug-report.md`
- `backlog-item.md`

原因：

- 原始材料形态差异大，过度模板化会增加 Agent 选择成本；
- `deferred` 和 `backlog` 是生命周期状态/索引视图，不是文件类型；
- bug/change 已有 Feature Follow-up / Flow-back 主流程；
- change request 可以作为自由源文件追加到 requirement set，但不需要标准模板；
- requirement system 应保持轻量。

## Source Files 不可变规则

Requirement source files 默认不可变，包括常见的 `requirement.md`。

规则：

- 不覆盖、重写或“整理”人类原始需求正文；
- 不为了让旧需求匹配当前实现而修改 `requirement.md`；
- 不在 feature 实现完成后回写 `requirement.md`；
- lifecycle、状态、实现信息写入 requirement set `README.md` 和可选 `requirements/INDEX.md`；
- 新的 follow-up、变更说明、反馈材料作为自由 source file 追加到同一 requirement set，或在冲突较大时新建 requirement set；
- 若 `requirement.md` 是 Agent 根据聊天新建的轻量记录，也仍按 source material 处理，后续修改需要人类明确确认。

示例：

```text
requirements/2026-06-19-provider-config/
  README.md
  requirement.md                  # keep immutable by default
  2026-06-21-follow-up.md          # append new material
```

状态变化写入 `README.md`：

```md
Status: implemented

## Lifecycle

Implemented By: .agent-loop/features/2026-06-22-provider-config/
Last Reviewed: 2026-06-22

## Status History

- 2026-06-22:
  - Status: implemented
  - Reason: Feature closed after verification
  - Human Decision: confirmed close
```

## Requirements Index 增强

只增强现有 `templates/requirements-index.md`。

`requirements/INDEX.md` 仍是 inventory，但允许承担 backlog/deferred 视图。

建议结构：

```md
# Human Requirements Index

Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Status: active

## Rule

This index is an inventory and backlog view. Original source material lives in requirement sets or original external paths.

Requirement-set dates are archive dates only. They are not deadlines or feature lifecycle dates.

## Requirement Sets

| Requirement Set | Status | Topic | Type | Used By | Notes |
|---|---|---|---|---|---|

## Backlog / Deferred Requirements

| Requirement Set | Status | Summary | Priority | Next Action | Related Feature |
|---|---|---|---|---|---|

## In Progress

| Requirement Set | Feature | Stage | Notes |
|---|---|---|---|

## Implemented

| Requirement Set | Implemented By | Closed At | Project Memory Updated |
|---|---|---|---|

## Superseded / Rejected

| Requirement Set | Final Status | Reason | Superseded By |
|---|---|---|---|
```

## 路由规则

### Future / Deferred Requirement Intake

当人类说或暗示以下内容时，进入 Requirement Archive 的 backlog/deferred 子模式：

- “先记一下”
- “后面做”
- “之后补”
- “下一轮做”
- “这个暂时不做”
- “以后加”
- “backlog”
- “defer this”
- “follow-up later”
- “not in this feature”

默认行为：

1. 不写 `project.md` planned capability 明细；
2. 推荐创建或更新 requirement set；
3. 根据人类表达设置 `Status: proposed | accepted | deferred`；
4. 如果 `requirements/INDEX.md` 已存在或触发 index 条件，更新 backlog/deferred 视图；
5. 如果此项来自当前 feature，先在当前 feature `notes.md` 记录来源，并链接 requirement set。

### 不进入 Requirement Backlog 的情况

| 场景 | 正确落点 |
|---|---|
| 当前 feature 内的实现步骤 | `tasks.md` / task detail |
| 当前 feature 的临时 handoff | `notes.md` |
| 已实现能力 | `project.md` / enterprise project memory |
| 稳定架构、命令、规则、领域语言 | `project.md` / enterprise project memory |
| 最近 feature 的 bug/change | Feature Follow-up / Flow-back |
| 原始外部需求文件 | requirement set source files or original external path |

## Follow-up 冲突与需求重建

Follow-up material 不总是追加到旧 requirement set。

当 follow-up 与原始需求存在重大冲突时，Agent 不应静默追加，也不应修改旧 `requirement.md`。Agent 必须先做 Requirement Conflict Review，推荐是否重建需求，并让人类确认。

### 追加到同一 requirement set

适合这些情况：

- 原用户目标不变；
- 只是补充细节、边界条件、验收说明、原型反馈；
- scope 仍属于同一个用户目标；
- 没有推翻核心业务规则；
- 原 out-of-scope 没有变成核心 scope；
- 继续沿用旧 requirement set 不会误导后续 Agent。

### 新建 requirement set

适合这些情况：

- 用户目标改变；
- 核心业务规则改变；
- 原 out-of-scope 变成核心 scope；
- 原 acceptance criteria 大量失效；
- 原 prototype 或产品方向被推翻；
- 新需求会形成独立 feature 或一组 feature；
- 继续沿用旧 requirement set 会误导后续 Agent。

### Requirement Conflict Review

当冲突可能较大时，Agent 应给出对比表：

```md
## Requirement Conflict Review

| Area | Original Requirement | Follow-up Request | Conflict |
|---|---|---|---|
| User goal |  |  | low/medium/high |
| Business rule |  |  | low/medium/high |
| Acceptance |  |  | low/medium/high |
| Out of scope |  |  | low/medium/high |
| Existing feature impact |  |  | low/medium/high |

Recommended action:
- append to existing requirement set | create linked new requirement set | create new requirement set and mark old one superseded
```

Human decision options:

1. append as same requirement set;
2. create a linked new requirement set and keep the old one active/reference-only;
3. create a new requirement set and mark the old one superseded;
4. defer decision and record conflict only in feature `notes.md`.

### Supersession 记录

如果人类确认新需求替代旧需求，旧 README 记录：

```md
Status: superseded

## Status History

- YYYY-MM-DD:
  - Status: superseded
  - Reason: Human accepted a new requirement direction
  - Human Decision: create new requirement set and supersede this one
  - Superseded By: ../YYYY-MM-DD-new-topic/
```

新 README 记录：

```md
Status: accepted

## Lifecycle

Intake Type: follow-up
Decision: accepted
Supersedes: ../YYYY-MM-DD-old-topic/
```

部分替代不要求第一版新增 `partially-superseded` 状态。保守做法是保持旧 requirement set 的当前状态，在 `Status History` 记录 partial supersession 和 related requirement。

## Feature Close / Project Memory Update 规则

Feature close 或 Project Memory Update 时增加 Requirement Reconciliation：

1. 检查当前 feature 是否引用 requirement set；
2. 若 requirement 已实现，将 requirement set 状态改为 `implemented`，记录 `Implemented By`；
3. 若 feature 产生了跨 feature 后续需求，创建或更新 requirement set，状态为 `proposed`、`accepted` 或 `deferred`；
4. 将已实现的长期能力写入 `project.md`；
5. 不把 deferred/backlog 明细写入 `project.md`；
6. 在 feature `notes.md` 记录 requirement 状态更新和链接。

## Project Memory 防污染规则

只需补一条轻量约束，不改变 memory 模型：

```text
Project memory must not be used as a backlog.
```

允许写入 `project.md`：

- implemented capabilities
- stable project facts
- active/paused feature pointers
- current resume action
- durable constraints and decisions

默认不允许写入 `project.md`：

- future feature ideas
- temporary TODOs
- deferred requirements
- unimplemented planned capability details
- backlog lists

如确需从 `project.md` 提醒未来工作，只写 requirement set 指针：

```md
Next Suggested Action:
- Review deferred requirement: .agent-loop/requirements/YYYY-MM-DD-<topic>/
```

不复制需求正文或 backlog 明细。

## Backward Compatibility

现有 requirement set 通常只有一个旧格式 `README.md`，例如：

```md
# Requirement Set: login

Archived: 2026-05-26
Topic: login
Status: active

Date Meaning:
...

Source Files:
...

Used By:
...

Notes:
...
```

这些旧格式必须继续有效。

兼容规则：

1. 旧 README 缺少 `Lifecycle`、`Summary`、`Status History` 时，不视为 stale；
2. 不因为缺少 v1.2.3 字段要求批量迁移；
3. 读取旧 requirement set 时保持只读兼容；
4. 只有在人类确认 lifecycle/status/backlog 更新时，才升级被触碰的 README；
5. 不自动创建 `requirements/INDEX.md`；
6. 旧 source files 继续自由命名，不要求改名或套模板；
7. 不因为旧格式 status 是 `active` 就自动判断为未实现或待开发。

旧状态解释：

| Old Status | Compatible Meaning |
|---|---|
| `active` | valid/usable source material; do not automatically rewrite to `accepted` or `in-progress` |
| `superseded` | `superseded` |
| `reference-only` | `reference-only` |

`active` 的含义必须通过 `Used By`、feature docs、close records、project memory 和 human context 判断。上下文不足时，只能说“source material is active/usable”，不能推断“需求尚未实现”。

迁移原则：

```text
Read old requirement set as valid.
Write new lifecycle fields only when touching that requirement set for lifecycle/backlog/status update.
Never bulk migrate requirements automatically.
Never mark old project stale only because README lacks v1.2.3 fields.
```

## Human Gates

Ask before:

- creating a new requirement set;
- changing requirement set lifecycle status;
- creating or updating `requirements/INDEX.md`;
- copying/moving/renaming source materials;
- marking a requirement `implemented`, `superseded`, or `rejected`;
- rebuilding a requirement set because follow-up conflicts with original requirements;
- writing any project memory update derived from requirement completion.

Do not ask before:

- explaining that a future/deferred item belongs in requirements rather than project memory;
- recommending the exact requirement set path;
- reading existing requirement index or requirement set README files.

## Implementation Scope

Minimal v1.2.3 implementation should update:

- `references/requirement-management.md`
- `templates/requirement-set-README.md`
- `templates/requirements-index.md`
- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/project-memory-mode.md` only for the no-backlog-in-project-memory constraint
- `references/validation-scenarios.md`
- `README.md` / `Usage.md` only for human-facing examples
- `CHANGELOG.md`

Do not add new source-file templates in v1.2.3.

## Validation Scenarios

### 1. Human Says “先记一下，下轮做”

Input:

```text
这个先记一下，下轮做 provider 配置化。
```

Expected:

- classify as requirement backlog/deferred intake;
- do not write planned capability details into `project.md`;
- propose requirement set path;
- ask before creating/updating requirement set;
- status should be `proposed`, `accepted`, or `deferred` based on human confirmation;
- update `requirements/INDEX.md` only if index exists or trigger conditions apply.

### 2. Feature Discovers Out-of-Scope Future Work

Input during feature:

```text
这里以后应该支持多 provider 策略，但本轮不做。
```

Expected:

- record discovery in current feature `notes.md`;
- recommend requirement set for cross-feature future work;
- set status to `deferred` after confirmation;
- do not add backlog details to `project.md`;
- continue current feature without scope creep.

### 3. Accepted Requirement Is Implemented

Input:

```text
这个 feature 已经实现了之前那个 accepted requirement。
```

Expected:

- during close/project-memory update, update requirement set status to `implemented`;
- record `Implemented By` feature path;
- update `requirements/INDEX.md` if present;
- write implemented capability to `project.md` only if it is a durable project fact;
- leave feature `notes.md` as historical evidence.

### 4. Bug Report Still Uses Feature Follow-up

Input:

```text
线上发现上次那个功能有 bug。
```

Expected:

- route to Feature Follow-up / Flow-back first;
- do not create a requirement backlog item by default;
- only archive durable source feedback under requirements after confirmation.

### 5. Old Requirement Set Remains Valid

Setup:

```text
requirements/2026-05-26-login/README.md uses old v1.2.2 fields only:
Archived, Topic, Status: active, Date Meaning, Source Files, Used By, Notes.
```

Expected:

- read old README as valid;
- do not classify requirement memory as stale;
- do not require migration before using source references;
- do not infer `active` means unimplemented;
- only add lifecycle fields if a confirmed lifecycle/status update is being written.

### 6. Requirement Source File Is Not Rewritten

Input:

```text
这个需求现在做完了，更新一下记录。
```

Expected:

- do not edit `requirement.md`;
- update requirement set `README.md` status/lifecycle after confirmation;
- update `requirements/INDEX.md` if present;
- record feature evidence in feature `notes.md`;
- update `project.md` only for durable implemented capability.

### 7. Large Follow-up Conflict Requires Requirement Rebuild Review

Input:

```text
原来是邮箱密码登录，现在改成只支持企业 SSO，不再支持密码登录。
```

Expected:

- do not modify old `requirement.md`;
- do not silently append as a small change;
- present Requirement Conflict Review comparing original vs follow-up;
- recommend create new requirement set and mark old one superseded, unless evidence suggests linked coexistence;
- ask human confirmation before creating new requirement set or changing old status.

## Open Questions

1. `requirements/INDEX.md` 是否应在第一个 backlog/deferred item 出现时自动建议创建，还是继续沿用原有 index trigger？
2. `Priority` 是否需要第一版保留，还是先只用 `unset` 避免 Agent 主观排序？
3. `accepted` 与 `deferred` 的区别是否需要人类确认措辞，避免 Agent 擅自判断优先级？
4. 已实现 requirement 是否必须在 feature close 时更新，还是允许在 Project Memory Update 阶段统一处理？
5. 第一版是否需要正式字段 `Supersedes`，还是只在 `Status History`/`Notes` 中自由记录？

## Recommended First Implementation

第一版建议采用保守策略：

1. `requirements/INDEX.md` 仍按原触发条件创建，但如果人类明确说“backlog / 待办索引”，可以建议创建；
2. `Priority` 默认 `unset`，只有人类明确排序时填写；
3. Agent 不自行把未来需求标记为 `accepted`，除非人类明确表示“要做”；默认使用 `proposed` 或 `deferred`；
4. Feature close 前必须检查 referenced requirement status，但写入状态仍需要人类确认；
5. 旧格式 requirement set 只读兼容，不批量迁移；
6. `requirement.md` 等 source files 默认不可变；
7. 大冲突 follow-up 先做 Requirement Conflict Review，再由人类确认是否新建 requirement set 或 supersede；
8. 不新增 source-file 模板。
