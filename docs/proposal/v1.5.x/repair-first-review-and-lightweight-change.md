# Proposal: Repair-First Review Repair and Lightweight Change

状态：implemented, validated, Human Review accepted, released as `stable-v1.5.5` with disclosed accepted risks

目标版本：v1.5.5

创建时间：2026-08-12

默认语言：中文

验证证据：[RED baseline](../../reports/agent-loop-v1.5.5-repair-first-red-baseline-2026-08-12.md)；[v1.5.5 full validation](../../reports/agent-loop-v1.5.5-full-validation-2026-08-12.md)；[发布前定向复核](../../reports/agent-loop-v1.5.5-pre-release-full-validation-2026-08-12.md)。源码实现与全量验证完成；人类已审阅并接受定向复核披露的剩余风险，授权 release commit、`v1.5.5` branch push 与 `stable-v1.5.5` tag 发布。`main` 同步、installed Skill 同步、PR 与 merge 不在本次授权内。

## 摘要

Agent Loop 当前把 TDD 作为行为修改的统一默认：先建立 RED，再写 GREEN，最后重构。该顺序适合 Feature 初次实现、明确 Bug 修复和高风险行为变更，但在以下两类工作中经常产生高于修改本身的流程成本：

1. Feature 已完成实现和验证，在 Review 阶段发现的边界内小缺陷、遗漏或临时调整；
2. 已通过 Lightweight Change Assessment 的低风险、可枚举、可回滚普通变更。

本 Proposal 引入统一的 `Repair-First Verification`（先修改、后验证）策略：

```text
已确认边界内的 Review 修复 / clearly eligible Lightweight Change
-> Agent 默认先修改
-> 立即执行 fresh targeted verification
-> 检查范围、diff、风险和回滚
-> 记录修复与验证证据
-> 向人类建议具体的回归测试
```

新回归测试不再是这两条路径的默认前置条件，也不再要求为了形式完整先制造 RED。回归测试建议属于修复后的质量建议；人类可以决定现在补、以后补或不补。只要原先已承诺的测试义务、fresh verification、Review、Drift 和其他完成条件均已满足，尚未采纳的新增回归测试建议不阻止当前 Review、Task Done、Lightweight Change completion 或 Feature Close。

本 Proposal 不降低验证要求。`先修改` 不等于 `不验证`：若没有新增测试就无法可靠证明当前结果，Agent 必须如实报告验证不足，并停在现有 Human Review，而不能声称已修复或已完成。

## 1. 背景与问题

### 1.1 当前 TDD 默认的价值

现有 TDD 默认能够在正式实现前证明测试确实捕获预期失败，并降低“测试只是在复述实现”的风险。它应继续用于：

- Feature 中尚未实现的新行为；
- 明确进入 Human-Guided Bug Management 的修复；
- 需要系统性诊断的失败；
- Gate 2 已承诺的测试驱动任务；
- 新的产品、接口、状态、数据、安全、权限或架构行为；
- 人类明确要求使用 TDD 的工作。

本 Proposal 不否定 TDD，也不把完整 Feature 流程改成建议。

### 1.2 Review 阶段的效率问题

Feature Review 的目标是发现实现与 accepted Feature definition、Product Slice、ADR、测试和工程规范之间的差异。当前规则在发现行为问题后通常重新进入 Execute / Diagnose，并再次要求：

```text
先写 RED
-> 验证 RED
-> 修改实现
-> 验证 GREEN
-> 回到 Review
```

对于以下问题，这条路径常常过重：

- Review 已准确指出一处条件判断遗漏；
- 人类明确要求调整已实现页面的一个局部交互；
- 代码审查发现一个边界内的错误提示、空值处理或默认值问题；
- 已有测试覆盖相关路径，只需修正实现并重跑；
- 修复可以通过精确脚本、构建、类型检查、API、浏览器或现有用例立即证明。

这些修复没有改变 Feature definition，只是在让实现符合已经接受的定义。机械地要求先补一条失败测试，会延迟人类已经明确要求的修复，并让 Review 修复被当成一次新的正式开发循环。

### 1.3 Lightweight Change 的同类问题

Lightweight Change Lane 已经减少 Feature artifact、Plan 和 helper 仪式，但当前仍规定：

```text
isolatable behavior logic
-> targeted RED
-> minimal GREEN
-> focused regression
```

这会让已经通过严格 eligibility 判断的轻量修改再次承担 TDD 前置成本。其问题不在测试本身，而在顺序被固定：即使目标、范围、回滚和验证方法都很清楚，Agent 仍可能先花时间构造 RED，之后才能执行人类要求的修改。

### 1.4 根因

当前规则没有清楚地区分两种证据责任：

| 责任 | 目的 | 是否必须 |
|---|---|---|
| 当前修复验证 | 证明这次修改现在确实达到预期，且没有明显破坏受影响范围 | 必须 |
| 新增回归测试 | 为未来修改持续保留自动防护 | 默认建议；按人类决定 |

因此，Agent 容易把“必须验证当前修复”错误等同为“必须先新增回归测试”。

## 2. 已确认的人类原则

本轮讨论已经确认以下原则：

1. Feature Review 中的边界内修复默认启用快速路径，不要求人类逐次开启。
2. Lightweight Change 使用同一顺序，默认先修改。
3. 修改后必须立即做 fresh targeted verification。
4. 修复完成后，Agent 向人类建议具体的回归测试。
5. 是否新增该回归测试由人类决定。
6. 不因为没有新增回归测试而自动阻止流程，只要当前修复已经被可靠验证，且既有测试承诺没有缺失。
7. 如果没有新增测试就无法可靠验证，Agent 不能虚报成功，必须说明缺口并请求人类决定。
8. 产品定义、验收范围、架构、公共接口、安全、数据、权限或其他独立 Human Gate 不因快速路径而被绕过。

## 3. 方案比较

### 3.1 方案 A：继续对所有行为修改强制 TDD

优点是规则统一，所有修复都有 RED 证据。缺点是 Review 小修复和 Lightweight Change 仍然承担完整测试前置成本，无法解决本次问题。

结论：不采用。

### 3.2 方案 B：只有人类明确说“先改”时才跳过 TDD

优点是保守。缺点是每次 Review 修复都可能增加一次确认，人类仍需理解并操作流程模式；同一个 Feature 内的连续 Review findings 也会重复中断。

结论：不采用。人类已确认默认启用。

### 3.3 方案 C：默认 Repair-First，验证强制，回归测试后置建议

Agent 在已确认边界内默认先修改，随后立即验证；新增回归测试在修复后以具体建议交给人类。既有测试义务和所有语义、安全、外部及 Git Gate 保持不变。

结论：采用。

## 4. 目标

1. 提高 Feature Review 阶段边界内修复的响应速度。
2. 让 Lightweight Change 真正使用轻量、风险匹配的实施顺序。
3. 把“当前修复是否被证明”和“未来是否需要新增自动防护”分开判断。
4. 保留 fresh verification、diff review、scope control、rollback、Review、Drift 和完成证据。
5. 让回归测试建议具体、集中、可选择，而不是泛泛提示“最好补测试”。
6. 避免每个 Review finding 创建新 Feature、重复 Gate 2 或重新进入完整 TDD。
7. 保持 Feature 初次实现、明确 Bug 管理和高风险边界的现有严谨度。

## 5. 非目标

本 Proposal 不做以下事情：

- 不取消 Agent Loop 的 TDD 能力；
- 不把 Feature 初次实现改成默认先写代码；
- 不允许跳过 Gate 2 已经承诺的测试；
- 不允许以回归测试建议替代 fresh verification；
- 不允许未验证的修改进入 `done`、`completed` 或 `closed`；
- 不改变 Human-Guided Bug Management 的身份、Resolution Path、修复 Feature、验证或关闭规则；
- 不允许 Review 修复重新定义 Requirement、Product Slice、ADR、Delivery Contract 或 Feature acceptance；
- 不新增 canonical stage、message intent、Feature status、Task status、Bug status、Auto Mode 或 Human Gate；
- 不新增 `.agent-loop/review-repairs/`、`.agent-loop/test-debt/` 或其他默认目录；
- 不创建强制测试债务 backlog、计数器、Checker Gate 或生命周期；
- 不授权 branch、commit、push、tag、PR、merge、release、publish、部署、生产或外部写入；
- 不在 Proposal 阶段修改 runtime、模板、测试、版本文件或 installed Skill。

## 6. 核心概念

### 6.1 Repair-First Verification

`Repair-First Verification` 是以下两条既有路径中的实施顺序：

```text
bounded write
-> fresh targeted verification
-> affected existing checks
-> diff/scope/risk review
-> evidence and regression recommendation
```

它不是新的 canonical stage。它只改变何时新增测试，不改变当前结果必须被验证的要求。

### 6.2 Review Repair Fast Path

`Review Repair Fast Path` 是 Review 阶段内部的默认修复方法。它处理实现与已接受定义之间的边界内差异。

它不是 Feature 类型、Task 状态或 Auto Mode，也不创造新的执行授权。它只能使用当前已经存在的 Feature execution authorization；若当前没有目标写入授权，Agent 仍需停在原有 Human Gate。

### 6.3 Regression Test Advisory

`Regression Test Advisory` 是修复并验证后的 Agent 建议，至少说明：

- 建议覆盖的具体场景；
- 推荐放置的测试层级或位置；
- 该测试能够防止的未来回归；
- 不补测试的剩余风险；
- Agent 的优先级建议。

它是 advisory，不是新的 Gate、状态或完成阻塞器。人类可以回答“现在补”“以后补”或“不补”。Agent 记录真实决定，但不建立另一套测试债务管理系统。

### 6.4 Required Verification 与 Additional Regression Test

必须明确区分：

- `Required Verification`：这次修改当前能够被证明所必需的检查；缺失时不得声称完成。
- `Existing Test Obligation`：accepted tests.md、Gate 2、Bug Verification Matrix、Delivery Contract 或其他已接受来源已经要求的测试；不得后置成 advisory。
- `Additional Regression Test`：Review 或 Lightweight Change 后新建议的未来自动防护；默认不阻止当前完成。

## 7. Feature Review Repair 路由

### 7.1 入口条件

Review finding 同时满足以下条件时，默认进入 Review Repair Fast Path：

1. 当前 Feature、Feature Authority 和 accepted execution boundary 可靠；
2. finding 表明实现没有满足既有 Product Slice、Feature acceptance、ADR、工程规范或已接受测试意图；
3. 修复目标和预期结果明确；
4. 修改仍在 accepted Story / Product Slice / Acceptance 和实施边界内；
5. 影响文件和消费者可以枚举；
6. 存在可执行的 fresh targeted verification；
7. 修复不需要新的产品、设计、架构、接口、安全、数据或权限决定；
8. 当前执行授权允许这次目标写入。

### 7.2 默认流程

```text
Review finding
-> Agent 判断 authority、scope、risk、verification 和 authorization
-> classify: within-approved-boundary repair
-> 直接修改实现
-> 运行 failure-matched fresh verification
-> 重跑受影响的现有测试 / 构建 / 类型 / lint / API / E2E / 手工检查
-> 检查 diff、范围、回滚和无关修改
-> 记录 Review Repair evidence
-> 集中向人类提出 Regression Test Advisory
-> 回到 Review / Drift / Task Done / Feature Close
```

不为每个 finding 重复请求授权，也不要求先新增 RED。

### 7.3 允许的典型修复

- 条件分支、空值处理、默认值或错误提示与 accepted behavior 不一致；
- 局部 UI 行为、文案、样式或可访问性问题；
- 已有测试覆盖路径中的实现错误；
- 可以通过现有 API、浏览器场景、fixture、构建或脚本精确证明的遗漏；
- Reviewer 指出的局部规范、边界、资源释放或异常处理问题；
- 人类在当前 Review 中要求、且仍处于 accepted boundary 内的临时调整。

### 7.4 必须退出快速路径的情况

出现任一项时停止 Repair-First 写入并返回 owning workflow：

- 改变 Requirement、Product Slice、Feature goal、scope、out-of-scope 或 acceptance；
- 新增 Story、产品规则、角色、权限、状态、数据含义或用户结果；
- 改变公共 API、事件、schema、Delivery Contract 或外部消费者承诺；
- 需要新的 ADR、架构边界、依赖、迁移、凭据、生产或外部系统决定；
- 安全、数据、并发、恢复或权限风险无法从 accepted design 和现有证据确定；
- 影响范围、回滚或验证路径不再可枚举；
- verification 失败并显示根因比 Review finding 更广；
- 当前没有适用的执行授权；
- 人类明确要求将问题登记为 Bug 或按完整 TDD 处理。

返回点继续使用现有 Gate 1、Gate 2、Decision & Design、Delivery Contract、Bug Management、Diagnose Failure 或 Human Gate，不增加新的返回状态。

### 7.5 与 Gate 2 Drift 的关系

Review finding 导致的代码修正，只要仍映射到 Gate 2 accepted Story、Product Slice、Acceptance、风险和验证边界，就记录为 `within-approved-boundary`，无需重复 Gate 2。

修正 accepted implementation package 的事实细节不等于修改 Feature definition。若改变任务边界、接口、风险、回滚或验证义务，则按既有规则返回 Gate 2；若改变产品定义，则返回 Gate 1 或 Requirements Discussion。

## 8. Lightweight Change 路由调整

### 8.1 保留现有 eligibility

Lightweight Change Assessment 的全部准入条件和 Feature hard triggers 保持不变：

- 普通非 Bug；
- 目标和完成标准明确；
- 范围可枚举；
- 没有新产品或技术决定；
- 没有公共、数据、状态、权限、安全、依赖、迁移或架构边界；
- 存在准确 verification；
- 回滚明确；
- 不需要 Feature/Bug 长期追踪、跨会话、handoff、subagent 或长期观察。

本 Proposal 只调整 clearly eligible 后的实施和测试顺序。

### 8.2 新的默认流程

```text
Lightweight Change Assessment: clearly eligible
-> persist Lightweight Execution Card before target writes
-> execute the bounded change first
-> run exact fresh targeted verification
-> run affected existing checks when available
-> review diff, scope, rollback and memory impact
-> complete or stop the card honestly
-> present a specific Regression Test Advisory when useful
```

不再根据“修改了可隔离行为逻辑”自动要求 targeted RED / minimal GREEN。Lightweight Change Lane 不再强制加载或执行 TDD helper。

### 8.3 Plan 与 Card 调整

Lightweight Execution Card 的 Plan 仍然必须存在，但不再要求预先写 expected RED/GREEN。Plan 至少写明：

- 精确目标和范围；
- 要修改的文件、位置或行为；
- 修改后如何验证；
- 受影响的现有检查；
- diff/scope review；
- 回滚方式；
- 何种发现会触发 scope expansion。

Card 的 Result / Residuals 记录本次验证和具体 Regression Test Advisory；不新增测试债务状态、计数器或强制 Human response 字段。

### 8.4 Scope expansion 保持不变

一旦执行中发现 Feature hard trigger、明确 Bug、未知消费者、验证失败揭示更广问题、回滚失效或其他范围扩张，Agent 必须停止 Lightweight Change，在扩大写入前推荐一个 owning workflow。

Repair-First 不允许“先改了再说”跨越 scope expansion。

## 9. 验证策略

### 9.1 验证优先级

Agent 应选择最直接证明当前结果的验证组合：

1. 重跑已经覆盖该行为的现有测试；
2. 执行与 finding/修改直接匹配的 focused command；
3. 运行 build、typecheck、lint、syntax、parser、reference 或 dry-run；
4. 执行 API、integration、browser、E2E 或人工检查；
5. 检查受影响消费者和负向路径；
6. 在没有其他可靠证明时，说明必须新增测试才能完成验证。

验证必须 fresh、可追溯并真实命中风险。宽泛的全量测试不能代替针对性证明，静态 diff review 也不能单独证明运行时行为。

### 9.2 不得后置的测试

以下测试不是新的 advisory，仍须按原承诺完成：

- Gate 2 accepted tests.md 中已经要求的测试；
- Requirement / Product Slice acceptance 对应的必需验证；
- accepted ADR Design Slice 或 Delivery Contract 的验证；
- Bug Verification Matrix；
- Feature Close 前适用的集成、E2E、安全、迁移或回归检查；
- 人类明确要求本轮必须增加或执行的测试。

### 9.3 可以后置建议的测试

下列情况可以在修复后提出 Additional Regression Test 建议：

- 当前修改已由现有测试或其他 fresh verification 可靠证明；
- 新测试主要用于未来持续防回归，而非证明当前结果；
- 新测试不会填补 Gate 2 或 accepted acceptance 中已存在的空缺；
- 不补测试的剩余风险可以被清楚说明；
- 当前没有未解决的 scope、authority、safety 或 verification blocker。

### 9.4 无法可靠验证

若没有新增测试就无法可靠证明修复，流程是：

```text
修复已写入
-> available verification 不足或失败
-> 不声明 fixed / done / completed / closed
-> 保留或回滚边界内修改，说明真实状态
-> 向人类推荐新增的精确测试及原因
-> 等待“现在补 / 调整方案 / 回滚或暂停”决定
```

这不是 TDD 前置 Gate，而是完成声明所需的证据边界。

## 10. Human Review 与记录

### 10.1 Feature Review Repair 记录

Feature `notes.md` 使用现有 Review evidence 区域记录：

- finding 与来源；
- accepted authority / acceptance；
- `within-approved-boundary` 结论和理由；
- 实际修改文件；
- fresh verification 命令、结果和时间；
- 受影响现有测试结果；
- Regression Test Advisory 或 `not-needed` 理由；
- 剩余风险；
- 人类后续决定（若有）。

不创建独立 Review Repair artifact。

### 10.2 Lightweight Change 记录

Lightweight Execution Card 继续拥有 Plan、Progress、Verification、Result、Residuals、Rollback 和 Memory Review。Regression Test Advisory 写入 Result / Residuals，不增加 parser lifecycle 状态。

### 10.3 人类摘要

多个修复应集中在下一次既有 Review / completion summary 中呈现，避免每个 finding 打断人类：

| Finding | 已修改 | Fresh verification | 回归测试建议 | 剩余风险 |
|---|---|---|---|---|
| `<finding>` | `<files / behavior>` | `<command and result>` | `<specific scenario and priority>` | `<risk>` |

Agent 应给出一个总体推荐，例如：

> 当前修改均已通过针对性验证。建议补充 2 条回归测试，其中 1 条优先级高、1 条一般；是否现在补由你决定。

该提示不是新的 Human Gate。若人类没有要求立即补测试，流程可以继续到已有的 Review、Drift、Completion 或 Close Gate。

## 11. Task Done、Lightweight Completion 与 Feature Close

### 11.1 Task Done

Review Repair 后，Task 可以进入 `done`，前提是：

- accepted implementation scope 已完成；
- 原 tests.md / Gate 2 / acceptance 中要求的测试均已完成；
- 本次修复具有 fresh verification；
- Review evidence 已记录；
- Drift decision 已记录；
- evidence locator 已写入 tasks/notes。

一个尚未被人类采纳的 Additional Regression Test Advisory 本身不使 Task 保持 `review` 或 `blocked`。

### 11.2 Lightweight Change completion

Lightweight Change 可以在 targeted verification、diff/scope、rollback、Result / Residuals 和 Memory Review 完成后标记 `completed`。Regression Test Advisory 可以作为 residual 被记录，但不创建 pending test-debt lifecycle。

### 11.3 Feature Close

Feature Close Review 必须显示仍未采纳的回归测试建议和剩余风险，但只要原 accepted verification obligations 全部完成，advisory 不单独阻止 Close。

若所谓 advisory 实际是证明 acceptance、Bug fix、Contract 或安全/数据正确性所必需的验证，则它不是 advisory，必须在 Close 前完成或走现有 substitute verification Human decision。

## 12. TDD 与 Helper 路由

### 12.1 保持 TDD 默认的路径

以下路径继续把 TDD 作为默认方法，并按现有规则加载 TDD helper：

- Feature 初次 Execute Task / Story；
- 明确 Bug Management 后的 Feature 修复；
- Review/Lightweight 退出快速路径并进入新的 Feature execution；
- 人类明确要求 TDD；
- accepted Plan 已把 RED/GREEN 定义为本轮 required verification。

### 12.2 不再强制 TDD helper 的路径

- Review Repair Fast Path；
- clearly eligible Lightweight Change Lane。

这两条路径由 Agent 直接选择 failure-matched verification。若人类在修复后接受“现在补回归测试”，Agent 写测试并 fresh-run；测试写入本身不要求倒序伪造一个已经发生过的 RED。

### 12.3 不得伪造 RED

Agent 不得在实现已经存在后回滚或篡改代码，只为制造一条形式上的 RED 记录；也不得把错误命令、缺依赖、fixture 损坏或无关失败写成行为 RED。

## 13. Gate 与授权边界

### 13.1 默认启用不等于新增授权

Review Repair Fast Path 和 Lightweight Repair-First 都默认启用，但只能在已有授权内工作：

- Gate 2 / Feature Auto-Loop / Task Auto-Run 或人类当前明确指令定义 Feature 写入范围；
- Lightweight Change 的具体人类请求和已披露 Card 定义轻量写入范围；
- branch、Git、外部、生产、发布及其他独立动作继续要求原 Gate。

### 13.2 现有 Human Gates 保持

以下 Gate 不变：

- Product Human Review；
- Requirement lifecycle；
- ADR acceptance；
- Feature Gate 1 / Gate 2；
- Delivery Contract creation / acceptance / breaking change；
- Bug Resolution Path、close 和 reopen；
- Project Skill Execution；
- subagent；
- branch、commit、push、tag、PR、merge、release、publish；
- Pause / Feature Close；
- 生产、外部、凭据、破坏性和付费动作。

### 13.3 Human 回应回归测试建议

人类的三种自然语言决定为：

- `现在补`：在当前已确认范围内增加建议测试并 fresh-run；
- `以后补`：记录人类决定和风险，不创建强制 backlog；
- `不补`：记录理由和已接受剩余风险。

这些是人类沟通结果，不新增全局 lifecycle enum。若测试工作超出当前 Feature/Change 范围，Agent 应重新路由，而不是把“现在补”解释成无限授权。

## 14. 失败与恢复

### 14.1 修改后验证失败

Agent 必须：

1. 保留准确的修改和失败证据；
2. 判断是否仍是同一个局部根因；
3. 若仍在边界内，进行一次受控修正并重新验证；
4. 若根因、范围或风险扩大，停止快速路径；
5. 根据回滚可靠性和当前状态，推荐 Diagnose Failure、Feature/Bug route、回滚或 Human Review；
6. 不把失败测试降级成“建议以后补”。

### 14.2 Context loss 或跨会话

Feature Review Repair 依赖 Feature notes 中的当前 authority、finding、修改和 verification evidence。上下文丢失后必须重新加载 Feature Context 和相关 evidence。

Lightweight Change 继续使用持久 Card 的恢复规则。计划性跨会话、handoff、subagent 或复杂恢复仍触发 Feature，不因 Repair-First 改变。

### 14.3 回滚

Repair-First 不能削弱回滚：

- Lightweight Card 在写入前已有具体 rollback；
- Review Repair 使用当前 task/plan 的 rollback 或记录本次局部恢复方法；
- 验证失败后不得顺带恢复或覆盖无关 dirty work；
- 外部、生产、不可逆和迁移修改不属于本快速路径。

## 15. 跨文件工作流不变量

实施时必须保持以下一致性：

1. `references/runtime.md` 与 `references/design.md` 同步定义 Repair-First、适用范围和退出条件。
2. `SKILL.md` 继续保持简洁，只声明 TDD 默认的适用范围和两条 Repair-First 例外。
3. `references/lightweight-change-lane.md` 删除强制 targeted RED/minimal GREEN，改为 repair-first targeted verification 与回归测试建议。
4. `references/stage-guides.md` 协调 Execute、Verify、Review、Diagnose、Drift 和 Close 路由。
5. `references/workflow-checklists.md` 不再要求 Review Repair / Lightweight Change 先验证 RED。
6. `references/skill-routing.md` 与 `references/external-skill-adapters.md` 不得让 TDD helper 重新覆盖这两条路径。
7. `references/human-review-summary.md` 增加紧凑的修复、验证、测试建议和剩余风险表达。
8. `templates/lightweight-execution-card.md` 继续要求 Verification/Result/Residuals，但不增加测试债务状态。
9. `templates/notes.md` 使用现有 Review evidence 记录修复和 advisory，不新增 artifact。
10. `references/validation-scenarios.md` 和 tests 同时覆盖正向、退出、完成与反向场景。
11. `templates/root-AGENTS.md` 只保留简短 First-Hop/ownership 提醒，不写完整算法。
12. README、Usage、CHANGELOG 和版本文件在 v1.5.5 实施时一致更新，不修改历史版本事实。

## 16. 预计实施影响面

至少审查并按实际需要修改：

- `SKILL.md`
- `plugin.json`
- `references/design.md`
- `references/runtime.md`
- `references/lightweight-change-lane.md`
- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/skill-routing.md`
- `references/external-skill-adapters.md`
- `references/human-review-summary.md`
- `references/feature-completion-check.md`
- `references/validation-scenarios.md`
- `templates/lightweight-execution-card.md`
- `templates/notes.md`
- `templates/root-AGENTS.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`
- `agents/openai.yaml`（仅当 metadata 表述需要同步）
- `tests/`
- `docs/reports/`

这属于 coordinated workflow change，因为它改变 TDD 路由、Review repair、Task Done、Feature Close、Lightweight completion、helper 选择和跨文件 workflow invariant。实施后必须运行 full validation。

## 17. TDD 实施方法与 RED 基线

本 Proposal 改变下游 Agent 的默认方法，但维护 Agent Loop 源码本身仍使用 TDD 实施：

1. 先建立能够证明当前强制 TDD 缺口的 focused RED；
2. 运行并保存 RED 输出；
3. 再修改 runtime/design/reference/template/human docs；
4. 运行 focused GREEN；
5. 运行所有受影响测试和 full validation；
6. 保存中文 RED 与 full-validation 报告。

RED 至少应证明当前规则仍然：

- 要求 Review 内行为修复先 RED；
- 要求 clearly eligible Lightweight isolated behavior 先 RED；
- 把 TDD helper 设为每次 Execute 的无条件强制 helper；
- 缺少修复后 Regression Test Advisory 契约；
- 无法区分既有测试义务和新增未来回归保护。

不得通过删除测试、放宽 unrelated contract 或只增加关键词断言获得 GREEN。

## 18. 验证与压力场景

### 18.1 Feature Review Repair

1. Review 发现 accepted boundary 内的空值处理问题；Agent 先修复、运行现有 focused test，再建议新增边界回归测试。
2. Review 发现 UI 文案/样式问题；Agent 先修改并浏览器验证，记录 regression test `not-needed` 理由。
3. Review 发现已有测试覆盖的逻辑错误；Agent 修改后重跑测试，不新增重复测试，并向人类说明现有覆盖充分。
4. Review 发现局部行为问题，API/manual verification 能证明当前结果；Agent完成修复并建议未来自动化回归测试。
5. Review 发现问题实际改变 Product Slice；Agent 不进入快速路径，返回 Gate 1 / Requirements Discussion。
6. Review 发现公共接口或 Delivery Contract 改变；Agent 停止并进入 owning Gate。
7. Review finding 的修复导致更广测试失败；Agent 不把失败列为 advisory，转 Diagnose Failure 或返回 Gate 2。
8. 当前没有 Feature execution authorization；默认启用的快速路径仍不得写目标文件。

### 18.2 Lightweight Change

9. 配置、路径或文档事实修改：先修改，再执行 parser/reference/residual 检查，不制造 unit-test RED。
10. clearly eligible 的局部逻辑调整：先修改，再运行 focused verification，并建议具体回归测试。
11. 现有测试完整覆盖变更：修改后重跑，记录无需新增重复测试的理由。
12. 没有任何可靠的非测试验证路径：不得完成 Card，向人类建议现在增加精确测试。
13. 执行后发现未知消费者或公共行为变化：停止 Card，进入 scope expansion。
14. 人类明确把问题作为 Bug 管理：不得通过 Lightweight Change 绕过 Bug Resolution Path 和 Feature repair。

### 18.3 Completion 与 Human Review

15. Additional Regression Test Advisory 尚未采纳，但原 Gate 2 tests 和 fresh verification 完成：Task Done 与 Close 可继续。
16. Gate 2 已承诺的测试缺失：不得伪装成 advisory，Task 保持非终态。
17. 人类回答“现在补”：Agent 增加测试并 fresh-run，不伪造先前不存在的 RED 历史。
18. 人类回答“以后补”或“不补”：记录决定和剩余风险，不创建默认 test-debt artifact。
19. 多个 Review repairs：只在下一次既有 Review summary 中集中提示一次。
20. 回归测试建议措辞含糊为“最好补测试”：验证应失败，要求具体场景、风险和推荐层级。

### 18.4 回归保护

21. Feature 初次 Execute 仍要求 TDD。
22. 明确 Bug Management 的 Feature repair 仍要求 TDD 和 Bug Verification Matrix。
23. Product/ADR/Contract/Gate 1/Gate 2/Submit/Close/Git Human Gates 不变。
24. 不新增 canonical stage、message intent、status、Auto Mode、artifact directory 或 Checker Gate。
25. Root AGENTS 仍保留全部 managed blocks，完整算法留在 owning references。

## 19. 验收标准

Proposal 实施完成必须同时满足：

1. Feature Review 的边界内修复默认先修改、后验证，无需预先新增 RED。
2. clearly eligible Lightweight Change 默认先修改、后验证，无需 targeted RED/minimal GREEN。
3. 两条路径都保留 fresh targeted verification、diff/scope review、rollback 和真实证据。
4. Agent 在修复后向人类提出具体 Regression Test Advisory。
5. Additional Regression Test Advisory 不自动阻止 Task Done、Lightweight completion 或 Feature Close。
6. 既有 Gate 2、acceptance、ADR、Contract、Bug verification 和人类明确测试义务不得降级成 advisory。
7. 无可靠 verification 时不得声称 fixed、done、completed 或 closed。
8. Feature 初次实现、明确 Bug 修复和退出快速路径后的正式 execution 继续默认 TDD。
9. 产品、范围、接口、架构、安全、数据、权限、外部和 Git Gate 保持不变。
10. 不新增 stage、intent、status、Auto Mode、Gate、artifact tree 或 test-debt lifecycle。
11. runtime、design、stage guides、checklists、templates、root guidance、human docs 和测试保持一致。
12. v1.5.5 所有版本承载文件和 13 个 root managed block revision 在实施时同步。
13. focused RED/GREEN、全部 Shell/Python tests、机械检查和 full validation 全部通过。
14. 中文 RED baseline 与 full-validation report 保存到 `docs/reports/`。

## 20. 实施停止条件

实施过程中出现以下情况时停止并交还人类：

- 需要把 Feature 初次实现或明确 Bug 修复也改为默认 Repair-First；
- 需要取消 fresh verification、Task Done、Review、Drift 或 Close 条件；
- 需要创建 test-debt artifact、Checker Gate、生命周期或新 canonical stage；
- 需要改变 Gate 1 / Gate 2、Product、ADR、Contract、Bug 或 Git Human Gate；
- 需要让未验证修改进入完成状态；
- 需要修改本 Proposal 已确认的 `默认先修改 -> 验证 -> 建议回归测试` 顺序；
- 需要新增依赖或改变 Python 3.10+ 标准库约束；
- 工作区无关 dirty work 与实施文件发生冲突；
- focused/full validation 无法可靠通过；
- 需要 commit、push、tag、PR、merge、release、publish 或 installed Skill sync，但未获得独立授权。

## 21. 范围检查

本 Proposal 仅精进以下两处：

```text
Feature Review 内的边界内实施修正
Lightweight Change clearly eligible 后的执行与验证顺序
```

它不修改 Requirement 到 PRD、ADR technical landing、Bug lifecycle、Feature construction 两个 Human Gate、Archive、Memory Reconciliation、Project Skills、Branch Management 或发布流程。

下一步在 Human Review 接受本 Proposal 后，编写独立 Implementation Plan，逐项映射 RED、runtime/design/reference/template/human docs、版本同步和 full validation；未经确认不开始实施。
