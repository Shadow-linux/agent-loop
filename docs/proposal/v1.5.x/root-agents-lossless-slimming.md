# Proposal: Root AGENTS Lossless Slimming

状态：已实施，等待 Human Review；未 commit / push / tag / release / installed-skill sync
目标版本：v1.5.0
创建时间：2026-07-21
默认语言：中文；canonical `templates/root-AGENTS.md` 保持英文

实施证据：

- Implementation Plan：`docs/proposal/v1.5.x/root-agents-lossless-slimming-implementation-plan.md`
- RED baseline：`docs/reports/agent-loop-v1.5.0-root-agents-lossless-slimming-red-baseline-2026-07-21.md`
- Full validation：`docs/reports/agent-loop-v1.5.0-full-validation-2026-07-21.1.md`

## 摘要

实施前 `templates/root-AGENTS.md` 为 224 行。它已经具备强 Agent Ownership、Message Intent Guard、完整 Stage Map、Gate Modes、Required Stops、Completion、Submit 和 Project Memory 约束，但一部分阶段算法、停止条件和 artifact 细节在 root 与 published references 之间重复表达。

实施后 canonical template 为 170 行，保留 13 个 managed blocks，并把 startup projection 更新为精确 16-row Workflow Gateway Map；完整 leaf-stage 顺序继续由 `references/runtime.md` 管理。

本 Proposal 建议在不改变 Agent Loop 运行语义的前提下，将 canonical root template 压缩到 **190 行以内**，推荐落点为 **170–185 行**。Root 只保留启动时必须立即看见的第一跳导航、项目主人意识、核心 Gate 和关闭证据；完整 leaf-stage 顺序与能力算法继续由 `SKILL.md`、`references/runtime.md` 和 owning references 负责。

行数是约束，不是成功标准。只有 capability-equivalence、完整回归和六域评分同时通过，才允许接受瘦身结果。

## 1. 最高原则

> Root AGENTS 瘦身减少的是启动上下文和重复规则，不减少项目主人意识、路由准确性、验证强度、记忆责任或 Human Gate。

具体要求：

- Root 必须让新 Agent 在不等待人类逐步指挥的情况下完成 Project Entry、意图分类和唯一下一步推荐；
- Root 必须明确 Agent 对项目结果而不只是流程负责；
- Root 必须保留 skill unavailable/load-failed 的 fail-closed 边界；
- Root 必须保留所有关键工作入口和发布包 reference 的可达性；
- Root 可以把完整 leaf-stage 顺序委托给 `references/runtime.md`，但必须通过机械测试证明没有入口丢失；
- Root 不复制 Bug、Lightweight、ADR、Archive、Project Skill 或 Memory Reconciliation 的详细算法；
- 任何压缩不得合并或隐含授权 Requirement、Feature、Project Skill、external mutation、Git 或 lifecycle action；
- canonical template 保持英文，managed block 外的人类内容保持原语言和原字节。

## 2. 实施前基线

| 项目 | 实施前事实 |
|---|---:|
| Root 行数 | 224 |
| Managed blocks | 13 |
| 当前工作区 revision | `1.5.0-20260721.1` |
| Agent Ownership | 包含 project-outcome ownership |
| Stage navigation | 完整 `Workflow Stage Map` |
| Required Stops | 逐项列举 |
| 当前全量验证 | Shell 39/39、Python 215/215 |
| 当前六域评分 | 99/100，STRONG |

历史提交 `1980368` 曾把模板压缩到 152 行并获得 99/100 验证，证明 Gateway delegation 方法可行。但该版本包含后来被回退的 Product Consensus 路由和旧 reference 集合，只能作为压缩方法证据，不能直接恢复或 cherry-pick。

## 3. 目标

1. 将 canonical root template 控制在 190 行以内。
2. 推荐保持 170–185 行，不为追求最低行数牺牲启动可读性。
3. 保留 13 个 managed block 的 identity、顺序、source 和完整 revision。
4. 保留 Project Entry、Remote、Recovery、Requirements、Decision / ADR、Feature、Bug、Lightweight、Operational Support、Project Skill、Archive、Onboarding、Memory Reconciliation、Submit 和 Chat 入口。
5. 保留 Core workflow spine 与 Product delivery spine，帮助 Agent 和人类理解全局闭环。
6. 保留 project-outcome ownership、唯一下一步、主动补齐缺失 artifact、调查后再询问和验证后才完成。
7. 把重复 leaf-stage 行和能力算法下沉到现有 published references，不新增第二事实源。
8. 保留所有独立 Human Gate 和 Auto Mode non-bypass 边界。
9. 通过精确 tuple、reference existence、leaf-stage coverage 和 mutation pressure tests 证明行为等价。
10. 最终六域评分不低于 99/100，且 Critical、High、Medium 全部为 0。

## 4. 非目标

本 Proposal 不做以下事情：

- 不恢复 `1980368` 的旧文件内容；
- 不恢复已回退的 Product Consensus、Product Design Hub 或 Workbench 路由；
- 不改变 Requirements Discussion、ADR、Feature、Bug 或 Lightweight 的语义和优先级；
- 不新增 canonical stage、message intent、status、lifecycle 或 Auto Mode；
- 不删除 project-outcome ownership；
- 不把完整 runtime Stage Order 再复制到 root；
- 不弱化 controller unavailable fallback；
- 不合并 commit、push、PR、merge、tag、release、publish、pause 或 close 的独立 Gate；
- 不改变 Skill version；
- 不修改 managed block 外的目标项目人类内容；
- 不以“测试仍然通过”替代语义审计和压力测试。

## 5. 推荐设计

### 5.1 两层运行权威

```text
root AGENTS.md
  = startup contract
  = intent + first hop + owner + gates + completion projection

SKILL.md / references/runtime.md / owning references
  = complete stage order
  = detailed eligibility and algorithms
  = artifact/state/gate procedures
```

Root 不需要离线复制整个 Agent Loop，但必须在 controller 不可用时 fail closed，不能假装自己能够执行完整工作流。

### 5.2 保留两条主流程

Root 必须保留紧凑的两条 spine：

```text
Core workflow:
Inspect -> Classify Intent And Project State -> Recommend One Next Action
-> Human Gate When Required -> Act Through Loaded Reference
-> Verify -> Review / Drift -> Record Memory -> Submit / Pause / Close

Product delivery:
Requirements / Concept -> Decision / ADR If Needed -> Feature
-> Plan -> Execute -> Verify / Review / Drift -> Memory -> Submit / Close
```

它们表达全局关系，不替代 Stage Map 或 runtime Stage Order。

### 5.3 Bootstrap 压缩

把当前逐条 Bootstrap 合并为约 8 个步骤：

1. root 是 bootstrap cache，优先加载 Agent Loop controller；
2. controller 不可用时进入 Strict fail-closed；
3. 发现唯一 memory root，缺失则进入 Init / Project Entry；
4. 读取阶段相关 memory、Active Feature 和 remote entry；
5. stale/outside-loop/remote 冲突进入 Recovery / Remote Discovery；
6. Project Skill discovery 在 generic executable fallback 前完成，loading 不授权执行；
7. Stage Helper Scan 在 controller 激活之后；
8. 检查最近目录 guidance，分类当前状态并推荐唯一下一步。

不得删除 project memory、remote、legacy root、project skill 或 directory guidance 的入口。

### 5.4 Agent Ownership 压缩

保留以下不可合并丢失的能力：

- `Own the project outcome, not only the workflow`；
- 询问人类前调查所有安全可得的 code、Git、tests、docs、environment 和 memory evidence；
- 在授权范围内持续推进至 verified completion 或具体 Human Gate；
- 自主诊断、排序、验证、Review、Drift 和 Memory Update；
- 推荐唯一下一步并主动提出缺失 artifact；
- helper 只是方法，Agent Loop 保留状态、Gate 和 lifecycle 控制；
- 每个有意义阶段报告 artifact、evidence、drift 和 next recommendation。

### 5.5 Message Intent Guard

保留紧凑且互斥的意图分类：

- Chat；
- Requirements Discussion；
- already-defined actionable ordinary non-Bug change；
- explicit Bug / Feature Follow-up；
- Feature Request；
- Operational Support；
- Project Skill Management；
- Feature Archive / Rehydrate；
- Post-Merge Memory Reconciliation；
- Proposal / Deferred Requirement / Lifecycle boundary。

意图可以随人类消息变化。真正不明确时，只询问一个阻塞问题；询问前先调查安全可得事实。

### 5.6 Workflow Gateway Map

把当前完整 leaf-stage 表改为 First-Hop Gateway。建议保留以下 gateway families：

| Signal family | First Hop | Published owner |
|---|---|---|
| No reliable memory | Project Entry / Init | project entry + project guidance |
| Remote source of truth | Remote Project Discovery | remote discovery |
| Memory conflicts / outside-loop work | Recovery / Re-Adopt | recovery |
| Explicit closed-history archive / rehydrate | Feature Monthly Archive | archive references |
| Explicit Bug / owned regression | Bug / Feature Follow-up | bug + follow-up |
| Already-defined actionable bounded non-Bug change | Lightweight Assessment | lightweight reference |
| Product need or meaning still being shaped | Requirements Discussion | requirement references |
| Human confirms requirement record/lifecycle action | Requirement Archive | requirement + stage guidance |
| Durable newcomer documentation requested | Evidence Graph + DDD Onboarding | onboarding reference |
| Accepted requirement needs shared technical landing | Decision & Design If Needed | project decisions |
| Accepted upstream meaning ready for implementation | Feature Construction / Runtime Continuation | runtime + stage guides |
| Current behavior use/test/run/diagnosis | Operational Support | stage guides + runtime |
| Reusable project workflow | Project Skill Creation / Update | project skills |
| Verified code integration requires memory reconciliation | Post-Merge Memory Reconciliation | memory reconciliation |
| Submit / Pause / Close / integration | Lifecycle Boundary | submit + stage guidance |
| Ordinary question without artifact/action intent | Chat | runtime when unclear |

完整 Product Brief、Feature Spec、Requirement Checklist、Work Breakdown、Contract、Test Design、E2E、Technical Design、Plan、Execute、Verify、Review、Drift、Memory 和 Completion 顺序由 `references/runtime.md` 负责，并通过 leaf-stage coverage test 证明仍然可达。

### 5.7 六类 Required Stops

把逐项列表归纳为六类，不删除任何语义：

1. **Semantic Gate**：Requirement、Concept、acceptance、Product、Decision / ADR 意义未决或会被下游重定义；
2. **Scope And Risk Gate**：scope expansion、architecture、security、data、permission、dependency、migration、public interface、customer isolation 或 durable boundary；
3. **Execution Gate**：Requirement/Feature action、plan execution、Project Skill、subagent、Contract、Archive 等需要独立授权；
4. **Evidence Gate**：基础设施不可用、验证反复失败、memory/artifact 冲突、dirty work、Review/Drift/Memory evidence 缺失；
5. **External Mutation Gate**：secrets、paid quota、credentials、configuration、external service、production/staging、deploy、destructive action；
6. **Git And Lifecycle Gate**：branch mutation、commit、push、PR、merge、tag、release、publish、pause、close、cleanup。

Auto Mode 不得绕过这六类 Gate。

### 5.8 Completion、Submit 与 Artifact Authority

Root 只保留不可丢失的不变量：

- code changed 不等于 `done`；
- fresh verification、Review、Drift 和 Memory evidence 是完成前置；
- Feature Completion Check 和 Feature Close Review 保持可达；
- submit、commit、push、PR、merge、tag、release、publish 独立确认；
- commit 只包含批准范围，保护 unrelated human work；
- code integration 后先校准 memory，再进行需要独立授权的后续动作；
- Requirement owns human source/product meaning；ADR owns technical landing；Feature owns implementation；Bug owns defect identity；Lightweight card owns bounded evidence；project memory owns durable current facts；
- root 不保存 task log、raw requirement、temporary plan、test transcript 或 backlog detail。

## 6. 预计行数预算

| 区域 | 当前 | 目标 |
|---|---:|---:|
| Opening | 7 | 3–4 |
| Bootstrap | 25 | 12–14 |
| Agent Ownership | 17 | 9–11 |
| Message Intent | 15 | 12–15 |
| Stage/Gateway Map | 42 | 25–30 |
| Gate Modes | 10 | 7–8 |
| Required Stops | 29 | 11–14 |
| Completion | 12 | 7–8 |
| Submit | 12 | 8–9 |
| Artifacts | 17 | 8–10 |
| Architecture / Directory / Commands / Constraints | 26 | 23–26 |
| 标题、markers、空行余量 | 已包含于各区 | 约 20 |

目标总计：**170–185 行**。硬上限：**190 行**。

如果保真内容需要 186–190 行，应保留内容；不得为了追求 170 行删除能力。如果超过 190 行，应重新消除重复表达，不得放宽测试或删 Gate。

## 7. 能力保真矩阵

| 能力 | Root 必须保留 | Detailed owner | 机械证据 |
|---|---|---|---|
| Controller loading / fallback | load controller + fail-closed | runtime | exact string + mutation test |
| Project outcome ownership | outcome、evidence-first、authorized continuation | runtime/design | exact string test |
| Unique next action | classify + one recommendation | runtime | exact string + scenario |
| Message intent | gateway-level intents | runtime | intent coverage test |
| Project Entry / Remote / Recovery | first hop | owning references | gateway tuple + reference exists |
| Requirements / ADR / Feature | product spine + first hops | requirement/project-decisions/runtime | leaf-stage coverage |
| Bug / Lightweight | precedence + first hops | bug/lightweight references | focused contracts |
| Operational Support | read-only default + mutation Gate | stage guides/runtime | focused contract |
| Project Skill | discovery/loading does not execute | project-skills/runtime | focused contract |
| Archive / Memory Reconciliation | first hops + Human Gate | archive/memory references | focused contracts |
| Auto Modes | prerequisites + non-bypass | runtime | exact six-Gate coverage |
| Completion | fresh verify/review/drift/memory | runtime/checklists | completion contract |
| Submit / lifecycle | independent Human Gates | submit reference | submit contract |
| Artifact authority | concise ownership split | artifact rules | authority assertions |
| Managed refresh | 13 blocks + full revision | project guidance/checker | structural/checker tests |

## 8. RED / GREEN 验证设计

### 8.1 RED 基线

实施前必须：

1. 记录当前 224 行、word/byte、13 blocks 和 current revision；
2. 重跑完整 Shell、Python、YAML、JSON、Shell syntax、Markdown fence 和 `git diff --check`；
3. 新增瘦身契约测试，并在 production template 尚未修改时看到目标 RED；
4. 保存中文 RED baseline report。

### 8.2 新增保真测试

至少覆盖：

- line count `<= 190`；
- canonical template 无 CJK；
- 13 个 managed blocks 完整、唯一、顺序不变；
- 精确解析每一行 `(Signal, First Hop, References)` tuple；
- 每个 reference 真实存在；
- 所有 runtime leaf stages 仍可达；
- Core workflow spine 和 Product delivery spine 存在；
- project-outcome ownership 精确句存在；
- 六类 Gate 全部存在，Auto Mode 明确 non-bypass；
- completion、submit 和 artifact authority 不变量存在；
- 详细算法词不得重新进入 root；
- 删除 gateway、交换 reference、删除 ownership 或 Gate 时测试必须 RED；
- managed block 外人类内容保持原字节。

### 8.3 GREEN 与全量评分

实现后必须：

1. focused slimming tests 全绿；
2. 全部 `tests/*.sh` 全绿；
3. 全部 Python tests 全绿；
4. YAML、JSON、Shell syntax、Markdown fence 和 `git diff --check` 全绿；
5. 六域语义审计覆盖 Requirement -> ADR -> Feature、no-ADR Feature、Bug、Lightweight、Operational、Project Skill、Archive、Memory、Completion、Submit 和 fallback；
6. 最终评分不低于 99/100；
7. Critical、High、Medium 必须为 0；
8. 报告明确 Windows 未实际运行时的边界，不把跨平台 contract 冒充 native runner 证据。

## 9. 实施顺序

```text
Human accepts Proposal
-> write Implementation Plan
-> RED baseline + new contract tests
-> compress root blocks without semantic change
-> update project guidance / workflow checklists / live revision consumers
-> focused GREEN
-> independent semantic review
-> repair any real gaps with RED/GREEN
-> full validation + 99/100 scoring report
-> Human Review
-> separate commit / push authorization
```

若实施发生在当前 `1.5.0-20260721.1` 之后的同一天，下一 managed revision 使用 `.2`；若跨日，使用新的 `1.5.0-<YYYYMMDD>`。所有 13 blocks 和 live consumers 同步更新，历史 Changelog、Proposal 和 Report 中的旧 revision 保持历史事实。

## 10. 回滚

瘦身实施必须保持为可审阅的文本变更。回滚范围包括：

- `templates/root-AGENTS.md`；
- coordinated project guidance/checklists；
- live revision consumers；
- 新增 focused tests；
- Changelog 和验证报告。

如果 capability-equivalence、full validation 或评分未达到门槛，恢复实施前 root template 和 live revision，不以“行数已经达标”为理由保留不可信瘦身。

## 11. Human Gates

本 Proposal 的接受只授权后续编写 Implementation Plan，不授权修改生产模板。

以下动作继续分别需要明确确认：

- 开始实施 Root slimming；
- 接受任何 Stage/Gate/authority 的语义变化；
- commit；
- push；
- tag、PR、merge、release、publish；
- 同步 installed Skill。

## 12. 验收标准

只有以下条件全部满足，Proposal 才能判定实施成功：

- canonical root template `<= 190` 行；
- 推荐落点 170–185 行，超出推荐区间有明确保真理由；
- 13 managed blocks 完整且 current revision 一致；
- project-outcome ownership、两条 spine、Gateway、六类 Gate、Completion、Submit 和 Artifact Authority 全部保留；
- runtime leaf-stage coverage 无缺失；
- focused mutation tests 能捕获删行、换 reference、缺 Gate 和缺 ownership；
- full Shell/Python/mechanical validation 全绿；
- 最终六域评分 `>= 99/100`；
- Critical 0、High 0、Medium 0；
- 没有无关 dirty work、目标项目 `.agent-loop/` 产物或未解决占位标记；
- 未经人类确认不执行 commit、push、tag、PR、merge、release、publish 或 installed Skill sync。
