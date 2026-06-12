# Agent Loop 使用指南

**版本：** 1.2.1

这份文档是给人类看的。你不需要记住 agent-loop 的内部阶段名，只要用自然语言告诉 Agent 你的目标，Agent 会判断当前项目处在哪个阶段，并推荐一个下一步动作。

核心约定：

```text
你提出目标 -> Agent 判断阶段 -> Agent 推荐下一步 -> 你确认 -> Agent 执行 -> Agent 记录证据 -> Agent 推荐下一步
```

Agent 的职责是主导研发闭环。你主要负责提出目标、确认关键决策、检查结果。

---

## 一句话触发指南

| 你可以这样说 | 会触发什么能力 | Agent 会做什么 |
|---|---|---|
| “帮我在这个项目里启用 agent-loop” | 初始化项目（Init Project） | 创建 `.agent-loop/project.md`、root `AGENTS.md`、`CLAUDE.md` 指针 |
| “接管这个旧项目” | 旧项目接管（Existing Project Onboarding） | 扫描现有代码和文档，建立项目记忆 |
| “深度接管这个项目，让新人能看懂” | 深度项目接管（Deep Project Onboarding Scan） | 生成 `.agent-loop/onboarding-db/` 项目理解文档、图、证据链 |
| “我只想先知道怎么启动和测试” | 快速接管（Quick Onboarding） | 只建立足够继续开发的项目记忆和启动信息 |
| “解释一下这个模块/流程/异步任务” | 定向接管扫描（Targeted Onboarding Scan） | 聚焦扫描一个模块、流程、异步任务、部署路径或问题点 |
| “这个项目以前用过 agent-loop，但最近没维护” | 重新托管 / 回补（Re-Adopt / Recovery Backfill） | 以代码现实为准，回补 `.agent-loop/` 文档 |
| “我要做一个登录功能” | 需求归档 -> 功能规范（Feature Spec） | 整理需求，生成功能规范 |
| “这是需求文档和原型图” | 需求归档（Requirement Archive） | 归档人类原始材料到 `.agent-loop/requirements/` |
| “先帮我梳理产品需求” | 产品说明（Product Brief） | 生成 feature 级 `product.md` |
| “把这个需求拆成任务” | 任务拆分（Work Breakdown） | 生成 `tasks.md` 或复杂任务目录 |
| “设计测试方案” | 测试设计（Test Design） | 生成 `tests.md`、测试矩阵、E2E 候选用例 |
| “开始执行这个 task” | 计划确认 / 执行任务（Plan Gate / Execute Task） | 先确认 plan，再按 TDD、验证、review、drift 执行 |
| “这个 task 你自己跑完” | 单任务自动执行（Task Auto-Run） | 确认 plan 后，自动完成该 task 的开发、测试、review、记录 |
| “这个 feature 后续你自动推进” | 单功能自动推进（Feature Auto-Loop） | 确认 spec 后，Agent 自动推进 Agent-ready 阶段 |
| “测试发现上次那个功能有 bug” | 功能回流（Feature Follow-up / Flow-back） | 先查最近 feature，判断回流旧 feature、开 linked 新 feature，还是先定位 |
| “这个字段/算法/API 要调整” | 功能回流或新 feature 判定 | 根据最近 30 天 feature 和代码证据，推荐一个处理流 |
| “检查现在做到哪了” | 继续 / 完成检查（Resume / Feature Completion Check） | 读取项目记忆和 feature 状态，推荐下一步 |
| “提交一下” | 提交集成（Submit / Integrate） | 检查 diff、验证证据、生成规范 commit，提交前再次确认 |
| “关闭这个 feature” | 关闭功能（Close Feature） | 做 close review、drift check、memory update，最后让你确认 close |

---

## 项目第一次使用

### 新项目

你可以说：

```text
帮我在这个项目里启用 agent-loop。
```

Agent 会先检查当前目录，然后向你确认是否创建：

```text
.agent-loop/project.md
AGENTS.md
CLAUDE.md
```

`AGENTS.md` 是未来 Agent 进入项目时最先读的启动说明。`CLAUDE.md` 默认只指向 `AGENTS.md`，不复制一整套规则。

root `AGENTS.md` 里会出现 agent-loop 托管块，例如：

```md
<!-- agent-loop:managed-start section:architecture source:.agent-loop/project.md -->
...
<!-- agent-loop:managed-end section:architecture -->
```

托管块内是 agent-loop 可以建议更新的内容。托管块外是人类或项目原生内容，Agent 不能自动覆盖。

### 旧项目接管

你可以说：

```text
接管这个旧项目，先帮我搞明白现在是什么结构。
```

Agent 会先做浅层扫描：

- README / docs
- package、脚本、测试命令
- 主要目录
- 技术栈
- 启动入口
- 测试入口
- 是否已有 `AGENTS.md` / `CLAUDE.md`

然后向你推荐：

| 模式 | 适合什么时候 | 会生成什么 |
|---|---|---|
| 快速接管（Quick Onboarding） | 你想尽快开始开发 | `.agent-loop/project.md`、root 启动说明、关键命令和目录概览 |
| 深度项目接管（Deep Project Onboarding Scan） | 你想让新人系统看懂项目 | `.agent-loop/onboarding-db/`、模块/流程/数据模型文档、图、证据链 |
| 定向接管扫描（Targeted Onboarding Scan） | 你只关心一个问题 | 某个模块、流程、异步任务、部署路径、状态变化的解释和图 |

旧项目 onboarding 不算完成，除非：

- root `AGENTS.md` 已存在、已创建，或你明确暂缓
- root `AGENTS.md` 有 agent-loop 托管块，或你明确暂缓
- `CLAUDE.md` 指向 `AGENTS.md`，已创建指针，或你明确暂缓

---

## 深度项目接管

你可以说：

```text
做一次 Deep Project Onboarding Scan，让新人能靠文档接手项目。
```

Deep onboarding 默认使用 Expanded onboarding-db。也就是说，它优先生成分类清晰、可长期维护的文档，而不是为了少文件把所有内容挤在一起。

Expanded 不是“只生成最少文件”。它有最小覆盖集，也有“发现即创建”的规则：扫描发现核心模块、复杂流程、异步任务、部署、安全、观测、复杂实体时，Agent 必须创建对应文档，或者明确写出为什么跳过。

复杂项目不会只画几张总览图就结束。模块越多、流程越复杂、状态流转越多，Agent 应该生成更多聚焦图：模块调用链图、核心流程图、状态流转图、状态写入追踪图、异步/job 图、数据实体图、模型使用流图、部署拓扑图。图不够就拆多张。

默认入口：

```text
.agent-loop/onboarding-db/README.md
```

常见目录：

```text
maps/
modules/
flows/
runtime/
domain/
quality/
```

Deep onboarding 应该覆盖：

| 内容 | 说明 |
|---|---|
| 一页项目总览 | 项目用途、技术栈、启动命令、测试命令、主要目录 |
| 模块图 | 重要模块之间怎么调用，不画全仓库爆炸图 |
| 模块详解 | 每个核心模块做什么、入口在哪、调用链是什么 |
| 核心流程图 | 登录、下单、会议纪要生成等业务链路 |
| 数据模型 | 表、模型、实体关系、状态字段、谁读写 |
| 异步 / 队列 / 任务 | producer、queue、consumer、retry、失败路径 |
| 部署和运行 | 本地启动、环境变量、部署、健康检查、日志 |
| 测试和风险 | 测试命令、验证路径、已知风险、未知项 |
| 证据链 | 文件路径、核心函数/对象/参数、这些证据证明什么 |

Compact / Standard 只在这些情况下使用：

- 你明确说“少生成点文件”
- 你明确说“合并成少数几个文档”
- 你明确选择 Compact 或 Standard
- 项目已有 onboarding-db，并且已经是 Compact 或 Standard 结构

即使选择 Compact / Standard，也不能减少理解维度、图、证据链和风险记录。

图不是只放 Mermaid。每张图都必须配两段文字：

| 说明 | 用途 |
|---|---|
| `How To Read` | 解释这张图回答什么问题、怎么看、颜色/形状/箭头是什么意思 |
| `Step-by-Step Walkthrough` | 按执行顺序一步步解释从哪里开始、经过哪些节点、在哪里结束 |

每次给你解释完项目后，Agent 还应该推荐一个下一步：继续读哪个文档、看哪个模块/流程、是否需要补一张聚焦图、是否运行启动/测试命令，或者是否回到 feature 开发。

---

## 人类确认点

默认是 Strict Mode：每个阶段开始前，Agent 都会问你确认。

你也可以开启自动模式：

| 模式 | 你可以这样说 | 自动范围 |
|---|---|---|
| Feature Auto-Loop | “这个 feature spec 确认了，后续 Agent-ready 阶段你自动推进” | 当前 feature |
| Task Auto-Run | “这个 task 的 plan 确认了，你自己跑完” | 一个 task 或一个 story |

自动模式不会跳过风险门禁。遇到下面情况 Agent 必须停下来问你：

- 需求范围变化
- 决策不清楚或证据不足
- 会修改人类原始需求材料
- 架构、安全、数据、权限、公共接口变化
- 测试环境不可用
- 多次验证失败
- drift check 需要人类批准
- AGENTS.md / CLAUDE.md / 目录级 guidance 需要变更
- 触及第一版明确排除的能力
- 有无关 dirty work
- 需要创建或接受 Delivery Contract
- 需要 subagent dispatch
- submit、commit、PR、merge、release、publish
- close feature

---

## 做新功能时怎么说

### 需求输入

你可以说：

```text
我要做一个登录功能，支持手机号验证码登录。
```

或者：

```text
这里有需求文档和原型图，你先归档并整理成 feature spec。
```

Agent 会把人类原始材料归档到：

```text
.agent-loop/requirements/YYYY-MM-DD-<topic>/
```

日期是归档日期，不是截止日期，也不是开发周期。

### 产品需求

你可以说：

```text
先帮我梳理这个功能的产品意图。
```

Agent 会生成 feature 级：

```text
product.md
```

这里记录用户目标、产品共识、领域语言、非目标，以及和后续 spec 的关系。

### 功能规范

你可以说：

```text
把这个需求写成 feature spec。
```

Agent 会生成：

```text
spec.md
```

它包含：

- 问题和目标
- 用户故事
- 验收标准
- 行为变化
- 依赖和非目标
- 未决问题

确认 `spec.md` 后，才进入任务拆分。

### 任务拆分

你可以说：

```text
把 spec 拆成可执行 task。
```

Agent 会生成：

```text
tasks.md
```

原则是优先 vertical slice，也就是一个 task 尽量形成可验证闭环，而不是简单按 DB / API / UI 横切。

复杂 feature 会启用复杂目录：

```text
tasks/
tests/
plans/
```

这些目录不会默认创建，只有复杂度触发且你确认后才创建。

### 测试设计

你可以说：

```text
设计测试方案。
```

Agent 会生成：

```text
tests.md
```

测试会分成：

- 模块 / 核心逻辑测试
- API 测试
- Web E2E 测试候选
- 回归测试
- 手动验证
- 命令和证据记录方式

Web E2E 不会凭空假设。Agent 会先检查项目真实环境，再决定能不能用浏览器自动化。

### 执行任务

你可以说：

```text
开始执行 T003。
```

Agent 不能创建完 task 就直接写代码。非简单 task 必须先生成或确认 plan：

```text
plan.md
```

复杂场景会写到：

```text
plans/YYYY-MM-DD-T003-<slug>.md
```

plan 需要包含：

- 要读和要改的文件
- 现有函数、接口、参数、调用关系
- 测试代码或测试命令
- RED / GREEN 预期
- 风险和回滚方式
- review 和验证方式

### 任务完成标准

task 写完代码不等于 done。

```text
done =
实现完成
+ 测试或替代验证已新鲜运行
+ 证据写入 notes.md
+ Spec Review 通过
+ Standards Review 在触发时完成
+ Drift decision 已记录
+ tasks.md 或 task detail 指向证据位置
```

---

## 接着做、回补和漂移

### 继续上次工作

你可以说：

```text
继续上次的功能。
```

Agent 会读：

```text
.agent-loop/project.md
.agent-loop/features/<feature>/
```

然后告诉你当前状态和一个推荐下一步。

### 一段时间没用 agent-loop

你可以说：

```text
这个项目最近有些代码没通过 agent-loop 做，你重新托管一下。
```

Agent 会进入 re-adopt：

- 以代码现实为准
- 对比 `.agent-loop/` 记录
- 找出缺失、过期、冲突
- 先提出 backfill 方案
- 你确认后再回补文档

### 文档和代码不一致

你可以说：

```text
检查一下现在文档和代码有没有漂移。
```

Agent 会做 drift check。长期事实变化会回补 `project.md` 或 enterprise memory；feature 行为变化会回补 `spec.md` / `tasks.md` / `tests.md` / `notes.md`。

### 关闭后发现 bug 或要改字段/算法

你可以说：

```text
测试发现上次那个功能有 bug。
```

或者：

```text
这个字段要改一下，应该影响最近做的那个 feature。
```

Agent 不应该直接新建一个孤立 feature。它会先做 Feature Follow-up / Flow-back：

| 步骤 | Agent 会做什么 |
|---|---|
| 查最近 feature | 默认检查最近 30 天的 active / paused / closed feature |
| 匹配证据 | 对比 spec、tasks、tests、notes、代码路径、API、模型、UI、测试失败 |
| 给候选表 | 列出可能归属哪个 feature、匹配强度、证据 |
| 推荐处理流 | 回流旧 feature、创建 linked 新 feature、创建 maintenance-fix feature、或先调查 |
| 等你确认 | 关闭的 feature 不会自动重开，必须你确认 |

几个重要边界：

- 30 天只是默认检查窗口，不是硬边界；如果你说“上次/之前/某个旧 feature”，或代码/API/测试证据明显重叠，Agent 应该继续做扩展扫描。
- 只有 “500 / 白屏 / unknown error” 这类低信息错误时，Agent 不应该随便匹配最近 feature，而是先建议 `investigate-first`。
- “字段小改一下 / 规则微调” 也要判断是否影响验收标准、API、数据、状态流、算法或可见 UX；不清楚时 Agent 应该先追问或定位。
- 如果你不想 reopen 旧 feature，Agent 可以尊重你的选择，但新的 linked feature 或 maintenance-fix 必须记录关联旧 feature、拒绝回流原因、继承的验收/测试/证据和影响路径。

如果确认回流到已关闭 feature：

- 原来的 Close Record 不会被覆盖
- `notes.md` 会新增 Follow-up Intake
- 必要时更新 `spec.md` / `tasks.md` / `tests.md` / `plan.md`
- 重新走测试、review、drift check、project memory update
- 最后再次让你确认 close

如果没有关联的 feature，或者你不愿意回流旧 feature，但这只是一个窄修复而不是新业务能力，Agent 应该创建一个新的 maintenance-fix feature：

```text
.agent-loop/features/YYYY-MM-DD-fix-<问题描述>/
```

它仍然要写：

```text
spec.md    Feature Type: maintenance-fix
tasks.md
tests.md
plan.md
notes.md
```

maintenance-fix 不是裸改。它也要验证、review、drift check，并判断是否需要更新 project memory。

---

## 提交和关闭

### 提交代码

你可以说：

```text
准备提交。
```

Agent 会：

- 检查 diff 和 untracked files
- 区分业务代码和 `.agent-loop/` 文档变更
- 只纳入本次确认范围内的目标文件，排除无关 dirty work
- 运行必要验证
- 做 review 和 drift check
- 给出 commit message
- 等你明确确认后才 commit，并把 commit hash 回写到当前 feature 的 `notes.md`

commit message 优先中文，使用类似：

```text
feat: 添加手机号验证码登录

- 新增验证码登录接口
- 补充登录表单校验
- 增加 API 和核心模块测试
- 更新 agent-loop feature 证据记录
```

### 关闭功能

你可以说：

```text
关闭这个 feature。
```

Agent 会先检查：

- spec 是否满足
- tasks 是否 done / skipped / removed
- tests 是否有新鲜证据
- review 是否完成
- drift 是否处理
- project memory 是否更新

最后仍然需要你明确确认 close。

---

## 常用产物位置

| 文件 | 用途 | 不应该放什么 |
|---|---|---|
| `.agent-loop/project.md` | 长期项目记忆、当前工作、下一步 | 任务日志、原始测试输出 |
| `.agent-loop/onboarding-db/` | 给人类读的项目理解文档、图、证据链 | 当前 task 状态 |
| `requirements/` | 人类原始需求材料归档 | Agent 改写后的执行计划 |
| `product.md` | feature 级产品意图 | 工程执行细节 |
| `spec.md` | feature 行为规范 | 执行日志 |
| `tasks.md` | 任务拆分和状态 | 原始测试输出 |
| `tests.md` | 测试方案和矩阵 | 长篇测试日志 |
| `plan.md` | 当前 task/story 执行计划 | 历史记录 |
| `notes.md` | 决策、证据、drift、pause/close | 原始需求 |
| `contracts.md` | 可选交付契约索引 | 临时 subagent 分工 |

---

## 你不需要记住的细节

你不需要说准确阶段名。下面这些自然语言都可以：

```text
接管这个项目。
我想做一个新功能。
先帮我问清楚需求。
把需求写成 spec。
拆 task。
设计测试。
执行 T001。
这个 task 你自己跑完。
检查有没有漂移。
提交前 review 一下。
关闭这个 feature。
带我理解这个项目。
解释这个模块为什么这么写。
我改这里会影响哪里？
这个状态是谁改的？
```

Agent 应该主动判断阶段、推荐一个下一步，并在需要你确认的地方停下来。
