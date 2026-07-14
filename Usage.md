# Agent Loop 使用指南

**版本：** 1.3.0

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
| “给这个项目做一套新人知识库。” | 先做 Evidence Graph；你先确认 Onboarding Spec，Agent 再写 Onboarding Tasks；你另行确认 Full Execution Gate 后才写正式 onboarding-db。 |
| “重点讲清楚支付/钱包/任务调度这块。” | 先从现有代码和文档回答；如果要沉淀长期文档，再走聚焦的 onboarding-db 更新。 |
| “这个旧 onboarding-db 还能信吗？” | 把旧文档当 evidence，先和代码现实核对；不直接按旧布局刷新。 |

当前 1.3.0 使用的是 **Evidence-Graph + DDD Onboarding**，不是旧 Quick / Deep / Targeted 模式。

推荐流程：

```text
可靠项目记忆
-> 08-review/evidence-graph.md
-> Core Flow Inventory（核心流程、业务终态、恢复责任和证据链）
-> onboarding-spec.md（第一次确认）
-> onboarding-tasks.md / Full Execution Gate（第二次确认）
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

核心流程完整性先于文档评分：`critical` / `important` 流程必须从触发闭合到业务成功、失败、取消、未知或人工处理终态；callback、consumer、retry、DLQ、compensation、reconciliation 和 job 不能因为被拆成其他 topic 就从流程中消失。每个关键 slice 都要连接代码证据、图和正文，缺失时不能标记 `newcomer-ready`。

Timeline / Sequence 是单个核心流程的主叙事；Core Flow Overview / Boundary 讲 scope、owner、branch 和 terminal；ASCII State Machine 讲状态、非法转换和恢复。数据血缘、事务并发、异步拓扑、决策树、runtime 和排障图由真实复杂度触发。非流程的 stateless 文档不强制状态图。

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
| “1.3.0 更新了什么？” | 读取 `CHANGELOG.md` 的 1.3.0 段落，按能力分类总结，不凭记忆回答。 |
| “和 1.2.2 比有什么变化？” | 对比 `CHANGELOG.md` 里的两个版本段落，说明新增、删除、替换和迁移影响。 |
| “现在 agent-loop 怎么用？” | 基于 `Usage.md` 用人类语言介绍常见触发方式。 |
| “这个功能怎么触发？” | 从 `Usage.md` 找对应说法，再说明 Agent 会进入哪个处理流。 |
| “agent-loop 是什么，怎么安装？” | 读取 `README.md`，解释总览、安装和 quick-start。 |

维护规则很简单：每个有意义版本都要更新 `CHANGELOG.md`；只有人类触发方式、使用入口或工作流口径变化时才需要更新 `Usage.md`；只有总览、安装、quick-start 变化时才需要更新 `README.md`。

### 我想整理需求，但还不实现

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “先帮我梳理这个需求，不要实现。” | 进入 Requirements Discussion，问清目标、用户、范围、约束、验收方向。 |
| “先按 grill-with-docs 问清这个需求。” | 先问清术语、业务流程、边界和异常场景；提问前会查已有文档、代码和相关历史 feature。 |
| “这个需求概念容易混，先把概念、关系和状态讲清楚。” | 在 Requirements Discussion 内触发 Concept Foundation：先查证据、提取候选概念、给出推荐定义及影响，再一次只确认一个真正阻塞后续模型的问题。 |
| “只是改按钮文案，不要搞复杂建模。” | 没有产品语义变化时记录 `concept-foundation-not-needed` 和理由，不生成大型概念表。 |
| “把这些内容落到 product.md。” | 如果还在聊天或需求澄清阶段，先问你是要创建/引用 requirement set，还是确认进入 feature Product Brief；不会直接创建 feature `product.md`。 |
| “聊需求时遇到复杂架构取舍，要不要 ADR？” | 记录 Design Readiness evidence 和 Decision Candidate；不会直接创建 ADR。requirement 被确认后、feature construction 前判断是否需要 Decision & Design。 |
| “这个需求进入 feature 前先做 ADR / Decision Design。” | 先做 Design Readiness；涉及多 feature、业务闭环、共享状态/事实源、恢复或非功能目标时进入 Decision & Design，不要求先出现技术争议。 |
| “这个需求会拆成多个 feature，先检查整体设计是否完整。” | 运行 Design Readiness Check；需要共享设计时先形成 Decision & Design 和 Design Slice Coverage，再创建各 feature spec。 |
| “检查 ADR 是否完整落地了 requirement model。” | 解析 Effective Requirement Snapshot，逐项检查 Requirement Model Technical Landing Trace、Design Slice 与 Verification；缺失 coverage 或 compatibility 待复核时停在 Decision & Design Human Review。 |
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

当至少一个 Phase 已实现、还有其他 Phase 未实现时，requirement 状态是 `partially-implemented`；只有确认范围内的所有 Phase 都进入实现或明确的终态后，才是 `implemented`。

`grill-with-docs` 在 agent-loop 里是需求/产品澄清方法，不是新的阶段。它会先查 project memory、需求来源、代码文档和相关过往 feature，再问人类一个阻塞问题；如果发现跨 feature、共享状态、恢复或长期取舍，只会记录 Design Readiness evidence / Decision Candidate，不会直接创建 ADR。

Concept Foundation 是这套澄清方法在复杂需求里的前置约束，不是新的 stage。Agent 不会让你先写“领域模型”；它从成功/失败场景和项目证据提取 Concept Candidate，用 requirement-local `Concept ID` 固定定义、identity、owner、lifecycle、relationship、invariant 和 product fact meaning。每轮 Human Grill 只问一个 downstream blocker，并附推荐定义、证据以及接受/拒绝对流程、状态和产品数据的影响。

Concept Foundation 被确认后，effective requirement source 才推导 Concept Relationships、Role / Permission Matrix、Commands / Events、Primary Business Flow、Product State Model 和 Requirement Product Model。`product.md` 与 `spec.md` 同时记录 `Effective Concept Source` 并只引用 accepted Concept/Model IDs；如果归档后要改变产品含义，Agent 保留原 source、把 Gate 设为 `reopened`，经人类确认后追加 follow-up 或新建 requirement set，再更新 README 的 effective pointer，而不是改写历史文档或在下游文档/ADR 里重新定义。

如果用了 Requirement/Product Grill，requirement document 会承接术语、主流程、异常路径、事实源、历史冲突、验收场景和 Decision Candidates，而不是只写一段摘要。

Product Brief Source Gate 的意思是：从聊天或需求澄清直接说“落到 product.md”时，Agent 不能立刻创建 feature 级 `product.md`。它要先问你是要创建/引用 requirement set，还是确认开始 feature Product Brief。如果只是整理产品意图，可以先保留在 requirement artifact 或回复草稿，等 feature context 明确后再写入 `product.md`。

Decision & Design / ADR 是 requirement 和 feature 之间的需求落地层。Requirement 接受后先运行 Design Readiness Check；只要需求会拆成多个 feature，或需要共享业务流程、领域/数据规则、事实源、一致性、恢复、性能、高可用、安全或可观测性设计，就会建议先完成整体 Decision & Design，即使没有技术争议。新的 decision draft 默认是 `proposed`，只有你明确确认后才会变成 `accepted`。每项 required Design Slice 都必须映射到 owning feature 和验证路径，普通 feature 内的小取舍仍写在 `spec.md` 的 `Design Decisions`。

Requirement-driven ADR 会先记录 Effective Requirement Snapshot，再用 Requirement Model Scope Inventory 对来源中的 `REL/PERM/CMD/EVT/FLOW/STATE/PM/EX` 稳定 ID 做完整盘点，最后用 Requirement Model Technical Landing Trace 给 scope 内每个 accepted model ID 安排 `landed`、`covered-by-accepted-decision`、`feature-local` 或 `not-applicable`。`landed` 必须明确技术落点、保留的不变量、Design Slice 和验证方向；inventory/coverage 不完整或 `Upstream Compatibility: review-required` 时，ADR 不能接受，依赖的 Feature Spec、Plan 和实现也会停止。

结构预检期间 ADR 保持 `proposed`；校验通过只表示可以提交人类评审。你明确接受后，Agent 才记录 Human Review Evidence、改为 `accepted` 并运行 accepted-mode validation。对于有具体理由的 `concept-foundation-not-needed`，使用 trace-not-applicable 分支，不伪造数据模型或流程。ADR 仍不能重新定义 Concept、流程、状态、不变量或事实归属；上游变化使既有技术结论失效时，必须经人类确认创建 superseding ADR。

Operational landing 不是每份 ADR 的默认大章节。只有持久化表示、协议/provider、runtime boundary 或上线兼容性发生变化时，才展开 Migration / Backfill、Compatibility、Rollout / Cutover 或 Rollback / Reversibility；未触发时只记录具体原因。

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
| “我要做手机号验证码登录。” | 先确认项目状态并创建/引用一个已接受的 requirement set；窄需求可以只建最小 requirement，再运行 Design Readiness 和创建 feature spec。 |
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
| “这个 feature spec 确认了，后续 Agent-ready 阶段你自动推进。” | Agent 先确认 Requirement Checklist 已通过，再启用 Feature Auto-Loop，在当前 feature 内推进拆任务、测试设计、计划、执行、验证、review、drift、memory update。 |
| “这个 task 的 plan 确认了，你自己跑完。” | Task Auto-Run：先运行 Analyze Consistency，再只完成当前 task/story，从 TDD 到验证、review、drift 和状态更新。 |

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

同一时间最多只有一个 Active Feature。切换功能时，Agent 会先把当前 Feature pause，记录恢复点，再激活另一个 Feature。若 agent-loop Skill 无法加载，已有自动模式授权会被暂停，只保留安全的只读接管、恢复和操作分析。

### 我想测试、部署、排查线上问题

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “新资源账号，先安排测试，跑通上线。” | 默认走 Code-Guided Operational Support，先只读查代码、配置、脚本、部署流程和风险。 |
| “帮我看看这个线上问题怎么处理。” | 先根据现有代码和 runbook 给排查/验证/回滚 checklist；需要改代码时再问你是否进入 feature/fix。 |
| “切一下模型/账号/配置，先确认风险。” | 先定位配置入口、依赖、验证方式、回滚方式；涉及外部服务、付费额度、生产/预发操作前要停下来确认。 |

操作支持默认不写代码、不改配置、不部署、不读取或暴露 secrets。它输出的是当前理解、必要输入、操作步骤、验证、回滚、风险和未决问题。

### 我想把常用流程做成项目技能

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “把这个流程做成技能。” | 进入 Project Skill Creation / Update，先展示 Project Skill Candidate、精确文件树、风险和验证计划，通过 Gate 1 后才在目标项目创建 `.agent-loop/skills/<skill-name>/`。 |
| “把刚才成功的操作沉淀成 skill。” | 复用刚才的新鲜成功证据，但仍要补 RED 基线、GREEN/REFACTOR、结构验证和前向执行测试；成功后自动从 `proposed` 变为 `active`。 |
| “以后这种复杂操作你可以主动建议做成技能。” | Agent 可在当前授权阶段完成且验证成功后主动提出 Candidate；主动建议不等于获准创建。 |
| “使用 deploy-check 技能检查测试环境。” | 如果技能和范围都已明确，Agent 仍先展示执行摘要；计划没有新增未披露动作或影响时，这句话可作为本次调用的 Execution Gate，无需再问一次。扩大范围、换任务或下次调用都要重新确认。 |

Project Skill 只写入使用 Agent Loop 的目标项目：

```text
.agent-loop/skills/
  INDEX.md
  <skill-name>/
    SKILL.md
    validation.md
```

创建或实质更新只有一个文件写入门禁：Gate 1。验证通过后会自动激活，不再增加 activation gate；验证失败则保持 `proposed`，不能进入正常路由。

执行是独立门禁。读取 INDEX、匹配触发条件、加载 `SKILL.md` 都可以只读完成；但真正按照技能步骤运行命令、调用工具、修改文件、访问外部系统或产生副作用前，必须为这一次有边界的调用获得 Execution Gate。`active`、`bootstrap`、Feature Auto-Loop、Task Auto-Run、以前执行成功或以前确认过都不能复用为下一次授权。

### 关闭后发现 bug 或要小改

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “测试发现上次那个功能有 bug。” | 先查最近 feature，判断是否回流旧 feature、创建 linked feature、maintenance-fix，或先调查。 |
| “这个字段/算法/API 要调整。” | 先判断是否影响最近 feature 的验收、API、数据、状态流、算法或可见 UX。 |
| “这个只是个窄修复。” | 如果没有归属 feature，创建 `Feature Type: maintenance-fix`，仍然要 spec/tasks/tests/plan/notes。 |

Feature Follow-up / Flow-back 默认看最近 30 天，但这不是硬限制。如果你明确说“上次/之前/某个旧 feature”，或证据明显重叠，Agent 应该扩展扫描。

低信息错误，比如 “500 / 白屏 / unknown error”，不应该随便归到最近 feature；Agent 应先建议 investigate-first。

### 我想按月份归档已经关闭的 feature

Feature Monthly Archive 只整理目录位置，不压缩或删除 feature 内容，也不会自动提交。一次正常交互是：

```text
Human: 把 2026 年 5 月和 6 月已经关闭的 feature 按月份归档。
Agent: 运行只读 scan，展示 plan SHA-256、eligible/blocked 行、目录移动、引用影响、不变内容和恢复范围。
Human: 确认这个精确批次及其 plan SHA-256。
Agent: 执行整目录移动和精确引用更新，完成 post-check，报告 transaction evidence，不自动 commit。
```

只有 `closed` 且关闭证据、Archive Readiness、drift、project memory 和 open follow-up 检查完整的 feature 才能进入候选。`active`、`blocked`、`paused`、当前月或存在不安全引用的 feature 保持 flat 并被阻断。归档结果是 `.agent-loop/features/YYYY-MM/<feature-id>/`，根级 `.agent-loop/features/archive.md` 只负责按稳定 Feature ID 定位当前位置；原 feature 文档、需求源和 accepted decisions 仍然是事实权威。

如果归档后的 feature 要重新进入 Follow-up / Flow-back，Agent 先运行只读 rehydrate scan 并展示新的 plan SHA-256；你必须通过一个独立的 rehydrate Human Gate。确认后 Agent 才把完整目录移回 `.agent-loop/features/<feature-id>/` 并复验。rehydrate 不会自行把 `spec.md` 从 `closed` 改为 `active`，后续 reopen 仍归 Feature Follow-up 管理。

原生 Python 3.10+ 调用示例：

```text
# macOS：只读生成计划
python3 scripts/scan-feature-monthly-archive.py --project-root <project> --operation archive --month 2026-05 --month 2026-06 --as-of 2026-07-14

# Windows PowerShell：只读生成计划
py -3 scripts\scan-feature-monthly-archive.py --project-root <project> --operation archive --month 2026-05 --month 2026-06 --as-of 2026-07-14
```

真正 apply 还必须提供刚刚经人类确认的 `--expected-plan-sha256`；不能使用 `--force` 绕过 stale-plan、引用阻断、transaction journal、恢复或 post-check。

### 我想同步 AGENTS.md

| 你可以这样说 | Agent 应该怎么做 |
|---|---|
| “agent-loop skill 更新了，检查一下这个项目的 AGENTS.md 要不要同步。” | 读取 root `AGENTS.md` / `CLAUDE.md`，运行只读 checker，报告哪些 managed blocks stale。 |
| “按最新 agent-loop 刷新这个项目的 AGENTS.md 托管块。” | 先给 Human Review Summary，说明要改哪些 block、为什么、风险是什么；你确认后才写。 |
| “不要覆盖我自己写的项目规则。” | 保留 managed block 外的人类/项目内容；冲突规则单独列出来让你决定。 |

如果当前 skill 提供脚本，Agent 应使用 Python 3.10+ 直接运行 canonical `.py` 入口。脚本只使用 Python 标准库；macOS 和 Windows 分别可以这样调用：

```text
# macOS
python3 scripts/check-root-agents-blocks.py --template <agent-loop-skill>/templates/root-AGENTS.md --target <project>/AGENTS.md

# Windows PowerShell
py -3 scripts\check-root-agents-blocks.py --template <agent-loop-skill>\templates\root-AGENTS.md --target <project>\AGENTS.md
```

这个脚本只读检查，不写文件。它会报告 missing / stale / broken managed block、`block-version` 漂移、marker 问题、unexpected section、source 缺失等。如果 Python 3.10+ 不可用，Agent 应报告 capability gap 并停止依赖该 checker 的判断，不能静默退回旧 Bash/Ruby 规则实现。

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
把这个流程做成技能。
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
| `.agent-loop/skills/INDEX.md` | 项目技能状态、加载策略、触发条件、范围和验证证据 | 技能正文、执行授权 |
| `.agent-loop/skills/<skill-name>/` | 项目常驻技能、验证记录和必要资源 | secrets、全局安装副本、feature 状态 |
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
- 创建或实质更新 Project Skill（Gate 1）
- 每次实际执行 Project Skill（Execution Gate）
- 修改人类原始需求材料
- 合并多个 Delivery Phases
- 提交、PR、merge、release、publish
- pause / close feature
- 执行会接触 secrets、付费额度、生产/预发、破坏性操作的命令

如果你明确说“只讨论，不记录”，Agent 应该保持讨论模式。如果你说“开始做”，Agent 才进入 feature / task 执行流程。
