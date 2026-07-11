# Agent Loop 全量验证与压力测试方法

本文面向维护和开发 Agent Loop 仓库的 Agent。它不是目标项目中用户 Agent 的运行规则，也不属于技能运行时 `references/`。

## 目标

验证 Agent Loop 的规则能否形成一致、可执行、可恢复的闭环。重点检查跨文件逻辑、阶段路由、Human Gate、状态迁移和项目记忆，而不是评价文档是否足够冗长。

**机械检查通过不等于逻辑验证通过。** YAML、Shell、Markdown 和测试脚本全部通过时，仍可能存在互相冲突的规则、无法到达的阶段或可以绕过的 Gate。

## 触发条件

出现以下任一情况时，开发 Agent 必须读取本文并执行对应验证：

- 人类要求“全面压测”“完整验证”“逻辑测试”“形成评分报告”或发布前验收。
- canonical stage order、routing axes、routing precedence 或 controller fallback 改变。
- Human Gate、Stop And Ask、Auto Mode、TDD、Submit、Pause、Close 或 Reopen 规则改变。
- Requirement、Product Brief、Decision / ADR、Feature Spec 或 Delivery Contract 的依赖关系改变。
- Active Feature、Requirement lifecycle、Delivery Phase、项目记忆或 root guidance 更新规则改变。
- Project Entry、Recovery / Backfill、Evidence Graph + DDD Onboarding 或 Feature Follow-up 改变。
- root Stage Map 的 signal、next stage、Read Next 或 managed block revision 改变。
- 修复了 Critical、High 或跨多个控制文件的 Medium 逻辑问题。

只有局部措辞、拼写或不改变行为的示例修正，可以只运行仓库最小检查与受影响测试。

如果人类只要求某个独立功能的评分、逻辑测试或专项压测，使用 `docs/maintenance/feature-validation-method.md`。单功能方法使用独立五域权重和 feature-scoped tests，但不替代本节触发条件已经要求的全量验证。

## 验证原则

1. 先确定审计对象是 Git `HEAD`、某个 commit，还是当前工作区；报告中必须写明。
2. 先跑现有测试建立机械基线，再做语义审计和压力场景。
3. 只报告真实逻辑问题：规则冲突、死锁、Gate 绕过、状态不一致、记忆丢失或路由不唯一。
4. 不把“希望写得更详细”当作缺陷。Agent Loop 提供原则、约束和判断框架，不追求把 Agent 降级成固定 SOP 执行器。
5. 发现问题后遵循 RED -> GREEN -> REFACTOR：保留修复前证据，添加回归断言，修复规则，再重新运行完整验证。
6. 修复前基线和修复后结果必须分区呈现，不能让历史缺陷看起来像当前问题。
7. 验证必须覆盖跨文件一致性，不能只检查被修改的单个文件。

## 六个审计域

| 审计域 | 权重 | 核心检查 |
|---|---:|---|
| Logic Correctness | 20% | 规则冲突、循环依赖、路由优先级、状态机、Auto Mode 与 Stop And Ask、Gate 绕过 |
| Autonomy | 15% | Agent Ownership、唯一下一阶段、主动调查、Helper fallback、阻塞时的可执行建议 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | Project Entry 边界、可靠记忆前置条件、Spec/Tasks Gate、legacy evidence、跨文件一致性 |
| Development / Test Workflow | 20% | Plan Gate、TDD RED/GREEN、Task Done、Review/Drift/Memory 闭环、Completion 与 Follow-up |
| Memory | 15% | Simple/Enterprise、stale-memory、Active Feature、Phase 汇总、root guidance、code reality wins |
| Recommendation | 15% | 阶段退出完整性、模糊目标处理、blocked 处理、推荐唯一性、Human Gate 表达 |

每个域输出：

- 结果：`PASS`、`CONFLICT`、`DEADLOCK`、`GAP` 或 `WEAK`
- 评分：0-100
- 发现：文件路径、行号、严重级别、冲突规则和实际风险
- 已通过的不变量
- 需要补充的回归测试

## 严重级别

| 级别 | 定义 |
|---|---|
| Critical | 会造成不可预测行为，或允许绕过安全、提交、状态及 Human Gate |
| High | 会让 Agent 对下一阶段作出不一致判断，或产生状态/项目记忆冲突 |
| Medium | 跨文件规则或迁移不完整，Agent 可能绕开，但容易造成误解或漂移 |
| Low | 不影响主流程的轻微措辞、索引或边缘场景问题 |

最终等级：

| 得分 | 等级 | 判断 |
|---:|---|---|
| 90-100 | STRONG | 主流程闭环，可进入发布候选验证 |
| 75-89 | STABLE | 可运行，但应处理剩余 High/Medium 风险 |
| 60-74 | FRAGILE | 机械上可运行，语义上仍容易漂移 |
| 0-59 | BROKEN | 存在阻断主流程或绕过关键 Gate 的问题 |

只要仍有 Critical，最终等级不得高于 `FRAGILE`；存在未解释的 High 时，不得判定为 `STRONG`。

## 审计准备

1. 读取 `AGENTS.md`、`SKILL.md`、`references/runtime.md` 和 `references/design.md`。
2. 根据改动范围读取相关 `references/`、`templates/`、`examples/` 与 `tests/`。
3. 检查 `git status --short --branch` 和 `git diff --stat`，记录审计边界。
4. 列出受影响的不变量与跨文件入口，避免只跟随 diff 阅读。
5. 运行现有 `tests/*.sh` 及基础语法检查，记录失败项，不要先修改后补基线。

## RED：记录修复前基线

在修复前完成以下工作：

1. 运行机械检查，记录通过数、失败数和失败输出。
2. 为六个审计域分别设计压力场景。
3. 对同一事实在 `SKILL.md`、runtime、design、stage guides、checklists、templates、root Stage Map 和 validation scenarios 中交叉取证。
4. 记录 Agent 可能采用的错误路径、合理化理由和最终风险。
5. 对可机械断言的问题先添加失败的回归测试，并确认测试因目标漏洞失败。

可并行时，将六个审计域分配给独立子 Agent。每个子 Agent必须获得明确范围，并按统一结构返回结果；主 Agent负责去重、验证跨域冲突和最终评分。不得用子 Agent 的意见替代主 Agent 对证据的核对。

## GREEN：修复后重新验证

修复后必须：

1. 运行新增专项测试，确认原 RED 场景转为 PASS。
2. 运行全部 `tests/*.sh`，不能只运行新增测试。
3. 重新执行六域语义审计，检查修复是否在另一个入口产生冲突。
4. 重新执行代表性压力场景，至少覆盖：
   - 复杂 Requirement -> Decision Scan -> ADR -> Feature Spec
   - 无需 ADR 的简单需求路径
   - Product Brief Source Gate
   - Delivery Contract Human Gate
   - TDD RED 与非行为型 `N/A`
   - Active Feature、Pause、Resume、Close、Reopen
   - 多 Phase requirement 的 `partially-implemented` 汇总
   - accepted ADR 与实现 drift
   - Follow-up investigate-first
   - Submit / Integrate 的 blocker 与验证顺序
   - stale-memory、root guidance 和 Project Entry
   - 普通 Chat 不创建工作流产物
5. 运行 YAML、JSON、Markdown 围栏、Shell 语法和 `git diff --check`。
6. 确认没有仍在运行、且属于本轮验证的命令或子 Agent。

## 关键跨文件不变量

每次全量验证至少确认：

- `SKILL.md` 是简洁入口，详细运行规则由发布包内的 design/runtime/reference 承载。
- root `AGENTS.md` Stage Map 只负责用户 Agent 导航，不替代详细阶段过程。
- Requirement 是业务目标与验收方向的 source of truth。
- Decision / ADR 是复杂需求落地前的可选决策桥梁，不是所有 Feature 的强制产物。
- Product Brief 和 Feature Spec 必须具有 requirement source 或明确 Feature-start 证据。
- accepted ADR、Decision Candidate 与实现不一致时，必须回到 Drift Check / Decision Scan。
- Delivery Contract 不能在 Human Gate 之前创建、接受或发生 breaking change。
- 行为变更不能跳过 TDD RED；非行为变更的 `N/A` 必须有理由。
- 同一时刻只允许一个 Active Feature，生命周期变化同步更新项目记忆。
- 部分 Feature 或 Phase 完成不能错误关闭整个 Requirement。
- Agent 先调查可获得的事实，再请求人类裁决真正的 blocker。
- Feature Completion、Submit、Commit、PR、Merge、Release、Publish 和 Tag 保持各自的人类 Gate。

## Commit 压力测试

当人类要求针对一个或多个 commit 压测时：

1. 使用 `git show --stat <hash>` 和 `git show <hash> -- <files>` 确定每个 commit 的行为边界。
2. 每个 commit 单独建立预期、不变量和反例，不把多个 commit 的结果混为一体。
3. 可在获得子 Agent 授权时为每个 commit 分配独立压力测试，再由主 Agent做跨 commit 集成判断。
4. 运行已有 contract/regression tests，并补充能复现漏洞的场景。
5. 分别给出稳定性 `STABLE / FRAGILE / BROKEN` 和有效性 `EFFECTIVE / WEAK / INEFFECTIVE`。

## 报告规范

验证报告保存到：

```text
docs/reports/agent-loop-<version>-full-validation-<YYYY-MM-DD>.md
```

报告正文使用中文；稳定的阶段名、状态值、命令和文件路径保留英文或代码格式。报告至少包含：

1. 日期、分支、版本和审计对象。
2. 总分、等级、测试通过数和是否存在 Critical/High/Medium。
3. 六域评分表。
4. 当前问题，按严重级别排序，并提供路径和行号。
5. 通过的不变量和压力场景。
6. RED 基线、GREEN 结果及新增回归测试。
7. 未采纳或降级意见及原因。
8. 发布判断，以及 `commit`、`push`、`tag` 是否获得人类授权。

禁止用“所有脚本通过”代替语义结论，也禁止在没有重新执行验证时沿用旧报告的分数。

## 最小命令集

根据仓库实际文件调整命令，但至少执行：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

若仓库含 JSON 元数据，再使用结构化 JSON 解析器检查；若修改 Markdown，执行围栏平衡检查。任何未执行项都必须在报告中说明原因。

## 防漂移维护

- 修改本文定义的触发面时，同步检查 `AGENTS.md` 入口和 `tests/validate-maintainer-full-validation-guidance.sh`。
- 新增 canonical stage、状态或 Human Gate 时，更新相应审计域、压力场景和跨文件不变量。
- 不要把仓库维护规则复制到 `references/`、`templates/root-AGENTS.md` 或目标项目 `.agent-loop/`。
- 历史报告只保存证据，不作为当前规则的 source of truth；方法变化以本文为准。
