# Agent Loop 使用指南

**版本：** 1.2.3

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
| “接管这个旧项目” | Project Entry Scan | 浅层扫描现有代码和文档，建立安全继续工作的项目记忆 |
| “深度接管这个项目，让新人能看懂” | Evidence-Graph + DDD Onboarding | 先确认 Project Entry Scan / 可靠项目记忆，再按 Evidence Graph → Onboarding Spec → Onboarding Tasks → 模块/流程 playbook 生成新人知识库 |
| “我只想先知道怎么启动和测试” | 安全接管 / 项目记忆 | 建立项目记忆、root guidance 状态、关键命令、边界和未知项；不生成 onboarding-db 细节文档 |
| “解释一下这个模块/流程/异步任务” | 聊天 / 操作支持 / Targeted Feature Scan | 先基于现有代码和文档解释；需要改代码或沉淀文档时再确认进入对应流程 |
| “这个项目以前用过 agent-loop，但最近没维护” | 重新托管 / 回补（Re-Adopt / Recovery Backfill） | 以代码现实为准，回补 `.agent-loop/` 文档 |
| “agent-loop skill 更新了，检查一下这个项目的 AGENTS.md 要不要同步” | root guidance 版本检查 / 托管块刷新 | 比较 root `AGENTS.md` 的 managed version 和当前 skill 版本，过期时提议刷新托管块 |
| “我要做一个登录功能” | 需求归档 -> 功能规范（Feature Spec） | 整理需求，生成功能规范 |
| “这是需求文档和原型图” | 需求归档（Requirement Archive） | 归档人类原始材料到 `.agent-loop/requirements/` |
| “先帮我梳理这个需求，不要实现” | 需求讨论（Requirements Discussion） | 形成 requirement document，必要时建议 Delivery Phases |
| “先帮我梳理这个 feature 的产品意图” | 产品说明（Product Brief） | 生成 feature 级 `product.md` |
| “把这个需求拆成任务” | 任务拆分（Work Breakdown） | 生成 `tasks.md` 或复杂任务目录 |
| “设计测试方案” | 测试设计（Test Design） | 生成 `tests.md`、测试矩阵、E2E 候选用例 |
| “开始执行这个 task” | 计划确认 / 执行任务（Plan Gate / Execute Task） | 先确认 plan，再按 TDD、验证、review、drift 执行 |
| “这个 task 你自己跑完” | 单任务自动执行（Task Auto-Run） | 确认 plan 后，自动完成该 task 的开发、测试、review、记录 |
| “这个 feature 后续你自动推进” | 单功能自动推进（Feature Auto-Loop） | 确认 spec 后，Agent 自动推进 Agent-ready 阶段 |
| “测试发现上次那个功能有 bug” | 功能回流（Feature Follow-up / Flow-back） | 先查最近 feature，判断回流旧 feature、开 linked 新 feature，还是先定位 |
| “这个字段/算法/API 要调整” | 功能回流或新 feature 判定 | 根据最近 30 天 feature 和代码证据，推荐一个处理流 |
| “检查现在做到哪了” | 继续 / 完成检查（Resume / Feature Completion Check） | 读取项目记忆和 feature 状态，推荐下一步 |
| “新资源账号，先安排测试，跑通上线” | 操作支持（Code-Guided Operational Support） | 默认只读查现有代码、配置、测试和部署流程，输出 checklist/runbook；确认前不写代码、不改配置、不部署 |
| “根据现有代码看看这个线上问题怎么处理” | 操作支持或功能回流判定 | 先按当前项目功能排查和给操作方案；如果必须改代码，再询问是否进入 feature/fix 流程 |
| “提交一下” | 提交集成（Submit / Integrate） | 检查 diff、feature/requirement 文档、memory、验证证据，生成规范 commit，提交前再次确认 |
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

### skill 更新后同步 AGENTS.md

当 `agent-loop` skill 升级后，你可以说：

```text
agent-loop skill 更新了，检查一下这个项目的 AGENTS.md 要不要同步。
```

或者：

```text
帮我按最新 agent-loop 刷新这个项目的 AGENTS.md 托管块。
```

Agent 会做这些事：

- 读取 root `AGENTS.md` 和 `CLAUDE.md`
- 如果当前 agent-loop skill 提供 `scripts/check-root-agents-blocks.sh`，先运行只读 managed-block drift check
- 找到 root `AGENTS.md` 里的 `agent-loop:managed-start section:meta` 托管块
- 读取托管块中的 `version:<x.y.z>`
- 读取当前本地 `agent-loop` skill 的版本
- 按 semantic version（`major.minor.patch`）比较两个版本
- 比较模板里的 managed sections、每个区块的 `block-version`、marker 是否成对、是否缺区块，以及本地 `source` 是否存在
- 如果 root `AGENTS.md` 的 managed version 更旧，或 checker 报告 missing / stale / broken managed block，就把 root guidance 判定为 `stale`
- 通过 Human Review Summary 列出要刷新的托管块、原因和风险，等你确认后再写
- 如果托管块外存在和当前 agent-loop 冲突的长期规则，单独列出冲突，询问你是清除、替换，还是保留为项目 override
- 如果托管块外存在技术栈、命令、架构边界、领域术语、测试策略等长期项目记忆，建议迁移到 `.agent-loop/project.md` 或 enterprise `.agent-loop/project/*.md`

Agent 不会直接覆盖整份 `AGENTS.md`。checker 也只报告，不写文件。托管块外的人类内容、项目原生说明、团队约定都必须保留。`CLAUDE.md` 默认继续只指向 `AGENTS.md`，不复制一整套规则。

同步时你通常会看到一张清理/迁移确认表：

| 内容位置 | 分类 | 建议动作 |
|---|---|---|
| `AGENTS.md` 某段旧规则 | 冲突规则 | 替换为 agent-loop 托管块规则，或确认保留为项目 override |
| `AGENTS.md` 里的测试命令/架构边界 | 长期项目记忆 | 迁移到 `.agent-loop/project.md`，root `AGENTS.md` 只保留启动必读摘要 |

### 旧项目接管

你可以说：

```text
接管这个旧项目，先帮我搞明白现在是什么结构。
```

Agent 现在会做 Project Entry Scan，也就是浅层、安全的项目入口扫描：

- README / docs
- package、脚本、测试命令
- 主要目录
- 技术栈
- 启动入口
- 测试入口
- 是否已有 `AGENTS.md` / `CLAUDE.md`

它只会推荐或生成：

| 内容 | 说明 |
|---|---|
| `.agent-loop/project.md` | 长期项目事实、关键命令、边界、能力、未知项 |
| root guidance 状态 | `AGENTS.md` / `CLAUDE.md` 是否存在、是否过期、是否需要托管块刷新 |
| 后续阶段 | Start Feature、Operational Support、Requirement Archive、Re-Adopt 或 Targeted Feature Scan |

Project Entry Scan 不算完成，除非：

- root `AGENTS.md` 已存在、已创建，或你明确暂缓
- root `AGENTS.md` 有 agent-loop 托管块，或你明确暂缓
- `CLAUDE.md` 指向 `AGENTS.md`，已创建指针，或你明确暂缓

---

## 新人文档 / 深度理解

你可以说：

```text
我想让新人能靠文档接手项目。
```

当前使用 Evidence-Graph + DDD Onboarding，不再通过旧 Quick / Deep / Targeted 模式、目录镜像式模板或一堆空心小文件生成新人文档。

推荐流程：

1. 先做 Project Entry Scan，保证项目记忆、root guidance、命令和边界是可靠的。
2. 进入 Evidence-Graph + DDD Onboarding，先建立 `08-review/evidence-graph.md`，把模块、流程、数据对象、异步任务、配置、部署、风险和证据来源串起来。
3. 写 `onboarding-spec.md`：读者、范围、模块计划、流程计划、DDD 映射、文件策略、图规则、质量门禁和批次计划。
4. 让人类确认 spec / tasks 后，可以全盘执行计划内能写透的 onboarding-db；batch 是 Agent 组织和 review 单位，不是每批都要重新等人类授权。
5. 模块默认写成 `02-modules/<module-name>.md`，流程默认写成 `03-flows/<flow-name>.md`；除非内容过大或人类要求，否则不要拆成一堆小文件。
6. 模块和流程默认必须有架构/边界图、ASCII 状态图、Timeline / 时序图；普通流程图和时序图优先用 Mermaid flowchart / sequenceDiagram，状态机、复杂原理图和复杂示例图优先用 ASCII。
7. 每个模块 / 流程文档都必须讲清楚用例、领域对象、数据对象、信息传递、状态变化、失败路径、排障、验证、示例和代码证据。
8. 再按 coverage 和人类优先级分批推进。批次大小只是 review 节奏，不是总量限制。
9. 未来网站只作为 Markdown 生成的阅读体验，不是本轮事实来源。

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

### 需求待办 / 暂缓需求

你可以说：

```text
这个先记一下，后面做。
```

Agent 不应该把这类未来需求写进 `project.md` 当 planned capability。它会建议写入：

```text
.agent-loop/requirements/YYYY-MM-DD-<topic>/README.md
```

并在需要时更新可选的：

```text
.agent-loop/requirements/INDEX.md
```

旧格式 requirement set `README.md` 仍然有效；缺少 lifecycle 字段不算 stale。`requirement.md` 等原始 source files 默认不可变，需求状态变化写入 README / INDEX。

### 需求分期

当一个需求比较大、会拆成多个 feature，或你想先做 MVP、后面再补增强时，可以说：

```text
这个需求比较大，先帮我拆成 phase。
```

Agent 会建议在 requirement set 的 `README.md` 中维护：

```md
## Delivery Phases

| Phase | Goal | Scope | Out Of Scope | Acceptance Direction | Status | Feature Mapping | Source Notes |
|---|---|---|---|---|---|---|---|
```

`Delivery Phases` 用来让人类确认“现在做哪一段、哪些先不做、做到什么算完成”。它只属于 requirement 层，不会把 project memory、ADR、product brief、feature spec、task、plan 或 close 流程都改成 phase 模式。

它不是 task，也不是 feature；当你确认开始某个 phase 后，Agent 再创建对应 feature，并在 `spec.md` 里引用这个 phase。后续阶段只在需要时引用 phase，或在 Drift Check / Requirement Reconciliation 时回填 phase 状态和 `Feature Mapping`。

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

如果你只是想讨论和整理需求，并明确不要开始实现，Agent 应先走 Requirements Discussion，把内容记录到 `.agent-loop/requirements/<date-topic>/`；只有进入某个 feature 时才生成 feature 级 `product.md`。

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

如果来源需求使用了 `Delivery Phases`，`spec.md` 应明确引用一个已确认 phase，或该 phase 内部的一个更小切片；不要为了加快推进把多个 phase 合并进同一个 feature。多期一起做之前，Agent 应先回到 requirement README 让你确认是否重写或合并 phase。

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

如果当前 Agent CLI 携带 Superpowers 或其他阶段 helper，Brainstorm、Plan Gate、Execute、Diagnose、Verify、Review 和已批准的 Subagent Execution 会先强制解析对应 helper。Agent 按 `superpowers:<name>`、`<name>` 的顺序检查，找到后必须加载完整 skill；只有记录 `unavailable` 或 `load-failed` 后才能走 agent-loop fallback。

helper 只增强阶段内部方法，不接管 agent-loop。产物仍写回当前 agent-loop 阶段的正式 artifact：需求讨论写回 `requirements/<set>/README.md` / `requirement.md`，feature 工作写回 `product.md`、`spec.md`、`plan.md`、`notes.md`、`handoffs/*`；不会因为 Superpowers 的默认规则创建 `docs/superpowers/*`。阶段选择、人类门禁、task done、project memory、submit、pause 和 close 仍由 agent-loop 控制。

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
- 提交前 Agent 应同时复核 feature 文档、requirement 记录、代码 diff、验证证据、drift、project memory、root/directory guidance 影响和 unrelated changes。
- 如果 feature 文档、requirement 文档或 memory 不需要更新，Agent 需要说明原因；如果需要延后，必须由你确认。
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
| `.agent-loop/project.md` | 长期项目记忆、当前工作、当前恢复动作 | 任务日志、原始测试输出、需求待办 |
| `.agent-loop/onboarding-db/` | legacy/deferred 项目理解文档；当前只作为证据读取，不再自动生成 | 当前 task 状态、项目记忆事实源、新 onboarding 生成目标 |
| `requirements/` | 人类原始需求材料归档、需求生命周期、需求待办、可选 Delivery Phases | Agent 改写后的执行计划 |
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
