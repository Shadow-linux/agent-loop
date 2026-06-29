# Agent Loop 使用指南

**版本：** 1.2.4

这份文档是给人类看的。你不需要记住内部阶段名，只要用自然语言说出你想做什么，Agent 应该自己判断当前状态、推荐一个下一步，并在需要你确认的地方停下来。

核心节奏：

```text
你提出目标 -> Agent 判断状态 -> Agent 推荐下一步 -> 你确认 -> Agent 执行 -> Agent 记录证据 -> Agent 推荐下一步
```

---

## 你可以怎么说

### 我想接管一个项目

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “帮我在这个项目里启用 agent-loop。” | 检查当前目录，确认后创建 `.agent-loop/project.md`、root `AGENTS.md`、`CLAUDE.md` 指针。 |
| “接管这个旧项目，先别写代码。” | 进入 Project Entry Scan，只建立安全继续工作的项目记忆、命令、边界、root guidance 状态和未知项。 |
| “我只想先知道怎么启动、测试、部署。” | 默认走只读扫描或操作支持，整理启动/测试/部署 checklist，不生成新人文档，不改代码。 |
| “这个项目以前用过 agent-loop，但最近没维护。” | 进入 Re-Adopt / Recovery Backfill，以代码现实为准，先回补 `.agent-loop/` 文档再继续。 |
| “这是远程项目，本地只是入口。” | 先做 Remote Project Discovery，确认远程路径、执行环境、memory 放在哪里，再扫描项目。 |

Project Entry Scan 不是新人文档生成。它不会创建：

```text
.agent-loop/onboarding-db/
onboarding-spec.md
onboarding-tasks.md
module / flow docs
onboarding diagrams
```

Project Entry Scan 不算完成，除非 root `AGENTS.md` 已存在、已创建、或你明确暂缓；`CLAUDE.md` 也必须指向 `AGENTS.md`、已创建指针、或你明确暂缓。

### 我想让新人能看懂项目

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “我想让新人能靠文档接手项目。” | 先确认 Project Entry Scan 或可靠项目记忆，再进入 Evidence-Graph + DDD Onboarding。 |
| “给这个项目做一套新人知识库。” | 先做 Evidence Graph，再给你看 Onboarding Spec 和 Onboarding Tasks，确认后写 onboarding-db。 |
| “重点讲清楚支付/钱包/任务调度这块。” | 先从现有代码和文档回答；如果要沉淀长期文档，再走聚焦的 onboarding-db 更新。 |
| “这个旧 onboarding-db 还能信吗？” | 把旧文档当 evidence，先和代码现实核对；不直接按旧布局刷新。 |

当前 1.2.4 使用的是 **Evidence-Graph + DDD Onboarding**，不是旧 Quick / Deep / Targeted 模式。

推荐流程：

```text
可靠项目记忆
-> 08-review/evidence-graph.md
-> onboarding-spec.md
-> onboarding-tasks.md
-> 02-modules/<module-name>.md
-> 03-flows/<flow-name>.md
-> coverage-matrix.md / batch-review.md
```

新人文档默认使用中文；代码符号、路径、命令、API、配置键、错误信息和第三方产品名保持原文。

Agent 不应该用空目录、薄 README、planned/later 占位文件、`TBD`、`TODO`、`待补充` 来假装完整。写不透但有证据可推断的地方，应该标明“推断”、证据、置信度和待验证点。

模块和流程文档默认要讲清楚：

- 这个模块/流程解决什么问题
- 边界在哪里，和谁交互
- 领域对象、数据对象、状态怎么变化
- 正常路径、失败路径、异常恢复
- 关键代码路径和证据
- 怎么验证、怎么排查、怎么安全修改
- 架构/边界图、ASCII 状态图、Timeline / 时序图

普通流程图和时序图可以优先使用 Mermaid flowchart / sequenceDiagram；状态机、复杂原理图和复杂示例图优先使用 ASCII。

### 我只是想问问题

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “解释一下这个模块为什么这么写。” | 作为普通讨论或代码解释，不默认创建需求、feature 或 onboarding 文档。 |
| “我改这里会影响哪里？” | 先基于代码和现有 memory 分析影响；如果需要长期沉淀，再问你是否写入文档。 |
| “这个状态是谁改的？” | 走代码/文档追踪或操作支持，必要时建议 focused scan。 |
| “先讨论一下，不要记录。” | 保持 chat，不创建 `.agent-loop/requirements/` 或 feature workspace。 |

如果讨论逐渐变成需求整理，Agent 应该问你是否要把它整理成 requirement document。讨论本身不等于开始实现。

### 我想知道版本更新或用法

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “1.2.4 更新了什么？” | 读取 `CHANGELOG.md` 的 1.2.4 段落，按能力分类总结，不凭记忆回答。 |
| “和 1.2.2 比有什么变化？” | 对比 `CHANGELOG.md` 里的两个版本段落，说明新增、删除、替换和迁移影响。 |
| “现在 agent-loop 怎么用？” | 基于 `Usage.md` 用人类语言介绍常见触发方式。 |
| “这个功能怎么触发？” | 从 `Usage.md` 找对应说法，再说明 Agent 会进入哪个处理流。 |
| “agent-loop 是什么，怎么安装？” | 读取 `README.md`，解释总览、安装和 quick-start。 |

维护规则很简单：每个有意义版本都要更新 `CHANGELOG.md`；只有人类触发方式、使用入口或工作流口径变化时才需要更新 `Usage.md`；只有总览、安装、quick-start 变化时才需要更新 `README.md`。

### 我想整理需求，但还不实现

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “先帮我梳理这个需求，不要实现。” | 进入 Requirements Discussion，问清目标、用户、范围、约束、验收方向。 |
| “这个需求比较大，先拆成几个阶段。” | 建议在 requirement README 里写 `Delivery Phases`，让你确认先做哪一段。 |
| “这个先记一下，后面做。” | 作为 deferred requirement 写进 requirement set 或 optional `requirements/INDEX.md`，不写进 `project.md`。 |
| “这是需求文档、原型图和反馈。” | 归档到 `.agent-loop/requirements/<archive-date>-<topic>/`，保留人类原始材料。 |

需求归档目录示例：

```text
.agent-loop/requirements/YYYY-MM-DD-<topic>/
  README.md
  requirement.md
  prototype.*
  feedback.*
  notes.*
```

日期是归档日期，不是 deadline，也不是 feature 周期。

`Delivery Phases` 是给人类确认“现在做什么、先不做什么、做到什么算完成”的需求层分期。它不是 task、不是 feature、不是 ADR、也不是 project memory。

示例：

```md
## Delivery Phases

| Phase | Goal | Scope | Out Of Scope | Acceptance Direction | Status | Feature Mapping | Source Notes |
|---|---|---|---|---|---|---|---|
```

当你确认实现某个 phase 后，Agent 再创建 feature，并在 `spec.md` 里引用这个 requirement set 和 phase。

### 我想开始做一个功能

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “我要做手机号验证码登录。” | 先确认项目状态和需求来源，再创建 feature spec。 |
| “把这个需求写成 feature spec。” | 写 `spec.md`，包含目标、用户故事、验收标准、行为变化、非目标和未决问题。 |
| “先帮我梳理这个 feature 的产品意图。” | 必要时写 feature 级 `product.md`，记录产品目标、共识、领域语言和非目标。 |
| “把 spec 拆成 task。” | 写 `tasks.md`，优先 vertical slice，让每个 task 尽量能验证闭环。 |
| “设计测试方案。” | 写 `tests.md`，包含模块/API/E2E/回归/手动验证和证据记录方式。 |
| “开始执行 T003。” | 先过 Plan Gate；非简单 task 要写或确认 `plan.md` 后再执行。 |

常见 feature 产物：

```text
.agent-loop/features/YYYY-MM-DD-<feature-slug>/
  product.md optional
  spec.md
  tasks.md
  tests.md
  plan.md
  notes.md
  contracts.md optional
```

如果来源 requirement 使用了 Delivery Phases，一个 feature 默认只实现一个已确认 phase，或一个 phase 里的更小切片。不要为了省事把多个 phase 合并进一个 feature；要合并时先回到 requirement README 让你确认。

### 我想让 Agent 自己往前推进

| 你可以这样说 | Agent 可以自动做什么 |
|---|---|
| “这个 feature spec 确认了，后续 Agent-ready 阶段你自动推进。” | Feature Auto-Loop：在当前 feature 内推进拆任务、测试设计、计划、执行、验证、review、drift、memory update。 |
| “这个 task 的 plan 确认了，你自己跑完。” | Task Auto-Run：只完成当前 task/story，从 TDD 到验证、review、drift 和状态更新。 |

自动模式不会跳过风险门禁。遇到这些情况必须停下来问你：

- 需求范围变化或决策不清楚
- 要修改人类原始需求材料
- 架构、安全、数据、权限、公共接口变化
- 测试环境不可用或多次验证失败
- drift check 需要你批准
- root/directory `AGENTS.md` 或 `CLAUDE.md` 要变更
- 需要创建或接受 Delivery Contract
- 需要未批准的 subagent dispatch
- 有无关 dirty work
- submit、commit、PR、merge、release、publish、pause、close

### 我想测试、部署、排查线上问题

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “新资源账号，先安排测试，跑通上线。” | 默认走 Code-Guided Operational Support，先只读查代码、配置、脚本、部署流程和风险。 |
| “帮我看看这个线上问题怎么处理。” | 先根据现有代码和 runbook 给排查/验证/回滚 checklist；需要改代码时再问你是否进入 feature/fix。 |
| “切一下模型/账号/配置，先确认风险。” | 先定位配置入口、依赖、验证方式、回滚方式；涉及外部服务、付费额度、生产/预发操作前要停下来确认。 |

操作支持默认不写代码、不改配置、不部署、不读取或暴露 secrets。它输出的是当前理解、必要输入、操作步骤、验证、回滚、风险和未决问题。

### 关闭后发现 bug 或要小改

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “测试发现上次那个功能有 bug。” | 先查最近 feature，判断是否回流旧 feature、创建 linked feature、maintenance-fix，或先调查。 |
| “这个字段/算法/API 要调整。” | 先判断是否影响最近 feature 的验收、API、数据、状态流、算法或可见 UX。 |
| “这个只是个窄修复。” | 如果没有归属 feature，创建 `Feature Type: maintenance-fix`，仍然要 spec/tasks/tests/plan/notes。 |

Feature Follow-up / Flow-back 默认看最近 30 天，但这不是硬限制。如果你明确说“上次/之前/某个旧 feature”，或证据明显重叠，Agent 应该扩展扫描。

低信息错误，比如 “500 / 白屏 / unknown error”，不应该随便归到最近 feature；Agent 应先建议 investigate-first。

### 我想同步 AGENTS.md

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “agent-loop skill 更新了，检查一下这个项目的 AGENTS.md 要不要同步。” | 读取 root `AGENTS.md` / `CLAUDE.md`，运行只读 checker，报告哪些 managed blocks stale。 |
| “按最新 agent-loop 刷新这个项目的 AGENTS.md 托管块。” | 先给 Human Review Summary，说明要改哪些 block、为什么、风险是什么；你确认后才写。 |
| “不要覆盖我自己写的项目规则。” | 保留 managed block 外的人类/项目内容；冲突规则单独列出来让你决定。 |

如果当前 skill 提供脚本，Agent 应先运行：

```text
scripts/check-root-agents-blocks.sh
```

这个脚本只读检查，不写文件。它会报告 missing / stale / broken managed block、`block-version` 漂移、marker 问题、unexpected section、source 缺失等。

注意：managed block 不等于都能模板覆盖。规则块可以按模板刷新；项目事实块必须结合 `.agent-loop/project.md` 或 enterprise memory 重新生成，并经过你确认。

### 我想提交或关闭

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “准备提交。” | 进入 Submit / Integrate，检查 diff、feature docs、requirement records、verification、review、drift、memory 和 unrelated changes。 |
| “提交一下。” | 这只授权进入提交检查；真正 commit 前还要给你 Human Review Summary 并再次确认。 |
| “关闭这个 feature。” | 先做 Feature Close Review、drift check、project memory update，再让你确认 close。 |

提交前 Agent 应同时复核 feature 文档、requirement 记录、代码 diff、验证证据、drift、project memory、root/directory guidance 影响和 unrelated changes。具体包括：

- 本次代码 diff 和 untracked files
- `product.md` / `spec.md` / `tasks.md` / `tests.md` / `plan.md` / `notes.md`
- 关联 requirement 的 lifecycle、Delivery Phase、Feature Mapping
- 新鲜验证证据
- Spec Review / Standards Review
- drift check
- project memory 和 root/directory guidance 影响
- unrelated dirty work

如果 feature 文档、requirement 文档或 memory 不需要更新，Agent 要说明原因；如果需要延后，必须由你确认。

---

## 你不需要记住这些阶段名

你可以自然地说：

```text
接管这个项目。
先别写代码，帮我搞清楚怎么启动。
我想让新人能看懂这个项目。
解释一下钱包扣费流程。
这个需求先聊清楚，不要实现。
这个需求比较大，拆成 phase。
我要做一个新功能。
把需求写成 spec。
拆 task。
设计测试。
执行 T001。
这个 task 你自己跑完。
检查文档和代码有没有漂移。
测试发现上次那个功能有 bug。
提交前 review 一下。
关闭这个 feature。
```

Agent 的责任是把这些话翻译成正确的下一步，而不是让你背阶段名。

---

## 常用产物位置

| 文件 | 用途 | 不应该放什么 |
|---|---|---|
| `.agent-loop/project.md` | 长期项目记忆、当前工作、当前恢复动作 | 任务日志、原始测试输出、需求待办 |
| `.agent-loop/project/*.md` | enterprise memory 下的长期项目细节 | 临时执行日志 |
| `.agent-loop/onboarding-db/` | Evidence-Graph + DDD 新人/项目理解知识库 | 当前 task 状态、原始需求、测试长日志 |
| `.agent-loop/requirements/` | 人类原始需求材料、需求生命周期、待办、Delivery Phases | Agent 的工程执行计划 |
| `product.md` | feature 级产品意图 | 工程执行细节 |
| `spec.md` | feature 行为规范 | 执行日志 |
| `tasks.md` | 任务拆分和状态 | 原始测试输出 |
| `tests.md` | 测试方案和矩阵 | 长篇测试日志 |
| `plan.md` | 当前 task/story 执行计划 | 历史记录 |
| `notes.md` | 决策、证据、drift、pause/close、submit 记录 | 原始需求正文 |
| `contracts.md` | 可选交付契约索引 | 临时 subagent 分工 |

---

## 人类确认规则

你控制目标、需求源材料、关键决策和阶段门禁。Agent 控制流程、产物、实现、验证和回补。

Agent 可以推荐下一步，但不能替你批准：

- 创建或改写 root/directory `AGENTS.md`
- 创建或接受 Delivery Contract
- 修改人类原始需求材料
- 合并多个 Delivery Phases
- 提交、PR、merge、release、publish
- pause / close feature
- 执行会接触 secrets、付费额度、生产/预发、破坏性操作的命令

如果你明确说“只讨论，不记录”，Agent 应该保持讨论模式。如果你说“开始做”，Agent 才进入 feature / task 执行流程。
