# Inline Task Review、Final Review Subagent 与 Agent-Owned Delegation 单功能验证报告

**日期：** 2026-08-30
**分支：** `alpha/v1.5.9`
**版本：** 当前源码仍为 `1.5.8`；本 Feature 目标版本为 `1.5.9`，Phase 2 版本同步尚未授权
**基线 HEAD：** `eee51f0dd72568ec5711567d6c7bc66d9b61797e`
**审计对象：** Task Completion Review、Feature-wide Final Review Subagent、Agent-Owned Subagent Delegation、Completion / Submit / Close 衔接与旧版归档兼容
**审阅输入：** Phase 1 的 42 个 tracked 修改与 4 个原有 untracked 文件；本报告是审阅输出，不属于被评分实现输入
**结论：** `77/100 — STABLE`
**Severity：** Critical 0 / High 4 / Medium 3 / Low 2

## 1. Scope Lock

本次只验证以下 Feature 流程：

```text
Execute Task / Story
-> Verify
-> Task Done Gate 内部 Task Completion Review
-> 全部 Task 与 Feature-wide Required Verification 完成
-> 自动只读 Final Review Subagent
-> owning Agent 校验 finding / repair / route / freshness
-> Drift Check
-> Project Memory Update
-> Feature Completion Check
-> Normal Submit（按输入新鲜度复用 Final Review）或 Human Close Gate
```

目标不变量：

1. Task review 是 Task Done Gate 内部的快速、强制审阅，不再是独立 Stage。
2. 全部 Task 和 Feature-wide verification 当前时，自动派发一次只读 Final Review Subagent。
3. reviewer 只报告；owning Agent 负责 finding 判断、修复、验证、路由、状态和人类声明。
4. 普通边界内修复不机械重复 reviewer；review boundary、integration、consumer、risk、rollback 或 coverage 实质变化时重新审阅。
5. Subagent dispatch 本身不是 Human Gate；每个委派动作只继承已有 stage、write grant 和 assignment boundary 的交集。
6. Feature Close 不再运行 Feature Close Review；Final Review 是完成证据，Human Close Gate 仍是唯一关闭授权。
7. Normal Submit 仅在 reviewed inputs 未变化时复用 Final Review；Full-Worktree Git Fast Path 不因 Git 请求制造 Review 或测试。
8. pre-1.5.9 历史记录可读，但不得成为当前 execution、completion、close、Git 或 release 授权。

明确排除：

- 不评分 Agent Loop 其他功能域的完整能力。
- 不进行 Phase 2 版本同步、13 个 root managed block revision 更新或 CHANGELOG 发布记录。
- 不运行或冒充全仓库 / 六域 full validation。
- 不授权 installed Skill 同步、stage、commit、push、tag、PR、merge、release、publish 或 seal。

## 2. 审阅方法

本轮使用三个互不写文件的 Subagent 并行审阅，并由 owning Agent 逐项对照源码复核：

| Reviewer | 边界 | 原始结论 |
|---|---|---|
| Logic / Gate reviewer | Proposal、Plan、runtime/design/stage/completion/submit | `35/45`；High 2 / Medium 3 / Low 1 |
| Cross-surface / Evidence reviewer | owning source、templates、docs、examples、scripts、tests；执行限定 focused checks | `29/30`；Low 1 |
| Proposal-blind pressure reviewer | 不读 `docs/proposal/`，只从当前运行时推演下游行为 | `16/25`；High 3 / Medium 2 / Low 1 |

Owning Agent 没有直接相加 reviewer 的问题数，而是合并同一根因、核实代码行和 Proposal 约束，并重新评估五域分数。Cross-surface reviewer 的机械 GREEN 真实有效，但其 `20/20` 一致性原始分被后续语义审阅发现的 adapter/runtime/scenario 冲突下调。

## 3. RED / GREEN / REFACTOR

### 3.1 RED

Implementation Plan 保存了 Phase 1 的真实 focused RED：新 contract 在 v1.5.8 owners 上首次运行产生 `14/14` 失败，覆盖 standalone Review、approval-gated Subagent dispatch、mandatory Feature Close Review、template/root/archive 和 human-doc gaps。

本次评分没有回退当前源码重跑 RED，也没有声称存在全仓库 pre-change baseline。可复现 RED 仍受 Plan 中已保存的命令和失败摘要约束。

### 3.2 GREEN

本次 Cross-surface reviewer 新鲜执行：

- 5 个直接相关 unittest 模块：`52/52 PASS`；
- `test_*archive*.py` discovery：`80/80 PASS`；
- focused wrapper：`56/56 PASS`，其中 review/delegation `18`、monthly archive scan `38`；
- wrapper 中的附加 contract assertions：PASS；
- `SKILL.md` YAML：PASS；
- `plugin.json` JSON：PASS；
- focused Shell syntax：PASS；
- `git diff --check`：PASS。

Owning Agent 另外新鲜执行：

- changed Python `py_compile`：PASS；
- 全仓库 Markdown fence balance：PASS；
- `git diff --check`：PASS。

52-test 与 80-test 集合是 132 个不重复 Python tests；focused wrapper 是其中 56 个测试的重复聚合，不重复计数为 188。

### 3.3 REFACTOR

Phase 1 记录显示，上一轮独立 reviewer 发现的 archive bypass、dispatch approval 残留、rollback entry evidence 和 mutation-test gaps 已经修复并通过 targeted re-review。本轮新增 findings 位于更深的状态衔接与压力边界，尚未修复，因此 GREEN 不能解释为 Phase 1 已接受。

## 4. Consolidated Findings

### Critical

无。

### High

#### H1. Task Completion Review 的当前性没有贯穿 Final Review 与 Review Repair

- `references/runtime.md:907-919` 要求 Task `done` 前审阅 current implementation/current diff，并由 Task row/detail 指向证据。
- Proposal `5.1` 明确要求 Final Review entry 验证 Task Done evidence 指向 current Task Completion Review。
- `references/stage-guides.md:1484` 只检查 Task 状态、Feature-wide verification、authority、dirty-work 和 rollback，没有检查每个 `done` Task 的当前 review evidence。
- `references/stage-guides.md:1494` 允许 Final Review 后修复 implementation，但没有说明如何刷新受影响 Task 的 Task Completion Review currentness，状态机也没有 `done -> review` 迁移。
- `references/feature-completion-check.md:38-47` 与 `references/runtime.md:1028-1038` 同样没有把该证据链重新锁定。

影响：开放中的 legacy Feature、错误手工状态、Task 后续漂移或 Final Review repair 可能保留 `done`，却没有与当前实现匹配的 Task Completion Review 证据，削弱“每个 Task 都快速审阅”的核心承诺。

建议：Final Review entry、Completion Check 和 Completion Gate 显式验证每个 `done` Task 的 evidence pointer/currentness；普通 Final Review repair 不必制造第二个 formal review，但必须明确刷新受影响 Task 的 completion-review evidence，或定义等价的 post-repair currentness contract。

#### H2. Task Auto-Run 最后一个 Task 与自动 Final Review 的退出顺序冲突

- `references/runtime.md:864,880-886` 要求 Task Auto-Run 在 selected Task/Story evidence、review notes、drift notes 和 status 更新后停止。
- `references/runtime.md:773-774` 与 `references/stage-guides.md:1478-1484` 又要求全部 Task 与 Feature-wide verification 当前后自动 Final Review。

影响：当 Task Auto-Run 完成最后一个 Task，且 Final Review 的其他条件已满足时，Agent 同时收到“必须停止”和“自动 dispatch”两个结论。人类离线时可以合理化为停止，从而使自动 Final Review 永远不发生；也可能反向合理化为越过 Task Auto-Run 的单任务边界。

建议：明确唯一顺序。推荐 Task Auto-Run 仍不开始新的实现 Task，但在最后一个 Task 完成且 Feature-wide review prerequisites 已经 current 时，允许其执行无写入的 Final Review dispatch；若 Feature-wide verification 尚未完成，则停在唯一明确的 Verify next action，而不是模糊地等待人类再次授权 review dispatch。

#### H3. helper fallback 与真正缺少 Subagent runtime 被混为一谈

- Proposal `5.5` 只允许“active runtime genuinely exposes no Subagent mechanism”时使用 `Final Reviewer: controller-fallback`。
- `references/stage-guides.md:1500` 保留了该正确边界。
- `references/external-skill-adapters.md:310` 却写成 “Subagent coordination capability is unavailable” 即可进入 controller fallback，没有区分 coordination helper 缺失和 dispatcher 机制缺失。

影响：环境有可用 Subagent dispatch、但缺少 `subagent-driven-development` helper 时，Agent 可合理化为同一 controller 自审，跳过强制独立 reviewer。

建议：拆成两个分支：helper unavailable/load-failed 只记录 helper fallback、仍 dispatch；只有 runtime 无 dispatcher 才使用 controller fallback。同步 README/scenario/test wording。

#### H4. 同一可写文件的并发 Subagent assignment 没有在 owning rule 中 fail closed

- `references/validation-scenarios.md:5875-5879` 要求 overlapping writes serialized。
- `references/stage-guides.md:1349-1356` 和 `references/external-skill-adapters.md:304-310` 允许“explicitly coordinates shared paths”，并把 overlap reconciliation 放到返回后。

影响：共享 worktree 中两个 Subagent 可并发读旧内容并覆盖同一文件。事后 diff/reconcile 不一定能恢复已经丢失的中间修改；“已协调”也可成为并发写合理化。

建议：同一可写路径必须串行或使用真实隔离 worktree；仅当 write sets 机械不重叠时才并发。事后 reconcile 只处理意外 overlap，不能把预知 overlap 变成允许并发的策略。

### Medium

#### M1. Finding 类型与合法 disposition 缺少约束矩阵

- `references/stage-guides.md:1488-1490` 区分 blocking defect、semantic/boundary conflict、verification gap、non-blocking improvement。
- `references/feature-completion-check.md:47` 却允许通用 `accepted residual`，没有限定 severity、类型、接受者和 Human evidence。

影响：blocking defect 或 unresolved verification gap 可被写成 accepted residual 后进入 Close Summary；Human Close Gate 虽仍存在，但收到的是被过早降级的证据。

建议：blocking defect 与 unresolved verification gap 不可 residual-close；semantic/boundary conflict 必须返回 owner 并刷新 review；只有 non-blocking improvement/明确残余风险可由对应 Human Gate 接受，且记录 provenance。

#### M2. 已退休 standalone Review 仍出现在 active routing

- `references/external-skill-adapters.md:176` 的 Diagnose Failure 仍返回 `Execute / Verify / Review`。
- `references/stage-guides.md:1600` 的 Submit entry 仍写 `after Verify, Review...`。
- `references/stage-guides.md:1665,1680` 在 Feature Completion Check 仍加载和使用 review helper，存在完成阶段重新做 code review 的合理化空间。

建议：替换为 owning Task Done / Final Review / finding-disposition route；Completion helper 只用于 evidence discipline 与 close-decision support，并明确禁止再次运行 code review。

#### M3. Normal Submit 的 review freshness 枚举遗漏 coverage 与 residuals

- Implementation Plan Task 5 要求 authority、diff、verification、risk、coverage、residuals 全部未变化才复用。
- `references/submit-and-integrate.md:89` 明列 authority、diff、verification、risk/rollback、consumer boundary，但未显式列 review coverage 与 residuals，也没有完整枚举 merge resolution、generated output、packaging 和 late edits。

影响：coverage/residual 改变可能没有使 Final Review 过期。

建议：把 coverage、residuals 和 Proposal 的 delta triggers 加入 owning rule 与 focused negative tests。

### Low

#### L1. Legacy cutoff 当日缺少精确回归

`scripts/feature_archive_support.py` 使用严格 `< 2026-08-29`，当前行为正确；现有测试覆盖 2026-08-30，但没有直接锁定 `Created == 2026-08-29` 或 `Closed At == 2026-08-29`。若未来误改为 `<=`，当前用例未必发现。

#### L2. Implementation Plan 的执行状态表达不一致

Plan 顶部和 progress 声明 Phase 1 已实现，但 Tasks 0-6 checkbox 仍全部为 `[ ]`，末尾仍写“repository is stopped before implementation”。这不改变 runtime，却降低 Human Review 的可审计性。

## 5. Proposal-Blind Pressure Matrix

| 场景 | 结果 | 说明 |
|---|---|---|
| 正常多 Task 完成 | PASS | Task Completion Review、Feature-wide verification、Final Review 的主顺序存在 |
| 人类离线、Final Review 自动 dispatch | PASS | dispatch 无 Human Gate；runtime 无机制时有 fallback |
| Feature Auto-Loop | PASS | 明确覆盖 Final Review、Drift、Memory，且保留 stop conditions |
| Task Auto-Run 完成最后一个 Task | FAIL | 单 Task stop 与自动 Final Review 冲突，见 H2 |
| 紧急 + 历史成功 + 旧授权 | PASS | 不会扩权或替代 current Gate |
| 普通 finding 修复 | PARTIAL | fresh verification/post-repair assessment 存在，但 Task review currentness 未闭环，见 H1 |
| Material repair | PASS | 旧 Final Review 失效并要求新 reviewer |
| verification failed / stale inputs | PASS | 进入 Diagnose/Verify 或 fresh Final Review |
| 高风险安全/数据/Contract/外部/Git 多 Gate | PASS | dispatch 不创造 action authorization |
| controller fallback | PARTIAL | stage guide 正确，adapter 条件过宽，见 H3 |
| legacy pre-cutoff/current post-cutoff archive | PASS | 双日期、旧 readiness key、current heading 共同隔离 |
| overlapping Subagent writes | FAIL | scenario 要求串行，owning rule 允许模糊协调，见 H4 |

## 6. 五域评分

| Domain | 得分 | 结论与扣分 |
|---|---:|---|
| Requirement And Scope Fidelity | 13/15 | 核心意图、非目标、版本/Phase 和 legacy 方向正确；扣分在 Task evidence entry 与 fallback 边界偏离 accepted Proposal |
| Logic, State, And Human Gates | 22/30 | Human Gates、Task Done 本体、material re-review、Close/Git 边界较强；扣分在 H1/H2/H3 和 finding disposition |
| Cross-Surface Consistency | 17/20 | 大多数 owner/template/doc/test 同步；扣分在 adapter fallback、retired Review 残留、runtime/scenario overlapping-write 冲突 |
| Pressure Resistance | 16/25 | 正常、紧急、旧授权、高风险、Git/Close、legacy 均可守住；最后 Task、repair currentness 和并发写压力失败 |
| Evidence And Maintainability | 9/10 | 真实 RED 记录、新鲜 focused GREEN、独立 proposal-blind review 和机械检查完整；扣分在 cutoff 边界与关键状态 mutation tests 缺口 |
| **Total** | **77/100** | **STABLE；存在 unresolved High，不能评为 STRONG** |

## 7. 未执行项

以下没有运行，不得写成 PASS，且 `not part of feature score`：

- 全仓库 Shell/Python tests；
- 六域 full validation 与 full validation 中文报告；
- Phase 2 版本/root revision contracts；
- macOS 之外的 native execution；Windows 仅保留 test-defined boundary，未实机运行；
- CI、commit、push、tag、PR、merge、release、publish；
- installed Skill synchronization。

该 Feature 修改 canonical Stage Order、Subagent authorization semantics、Task Done evidence、completion/close 和 root projection，因此正式 completion/release 仍强制需要另行 Human-confirmed full validation。本报告不能替代它。

## 8. 风险与判断

主方向和多数 safety Gate 正确，focused tests 也稳定；问题集中在“最后一个 Task 后自动收尾”与“修复/委派后证据是否仍 current”。这些是 Feature 核心路径，不适合只作为未来优化。

**Phase 1 判断：** 可以把本报告作为 Phase 1 Human Review 的问题输入，但当前不建议接受 Phase 1。先关闭 4 个 High 与 3 个 Medium，补对应 RED/mutation cases，再重跑同一 focused boundary 和一次新的 proposal-blind pressure review。

**Git / release 判断：** 尚未达到 commit 或 release-readiness。当前未同步 installed Skill，未 stage、未 commit、未 push、未 tag、未 release、未 publish。
