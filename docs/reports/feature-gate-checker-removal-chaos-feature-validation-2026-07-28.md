# Feature Gate Checker Removal 混沌测试与单功能评分报告

> 历史中间证据：本报告记录修复前的 84/100 结果，当前结论已由 `feature-gate-later-start-light-gate-feature-validation-2026-07-28.md` 的 97/100 复测取代。保留本文件用于追溯 RED 与修复原因，不作为当前发布判断。

## 结论

- 日期：2026-07-28
- 分支：`v1.5.2`
- HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
- 审计对象：当前 dirty working tree
- 功能范围：移除本地 Feature Gate Checker 后，Feature 从 Gate 1、Gate 2、执行、任务变化、暂停/恢复到关闭的路由与授权边界
- 总分：**84 / 100 — STABLE**
- 当前发现：Critical `0`、High `1`、Medium `1`、Low `1`
- 运行逻辑：26 / 26 单场景、14 / 14 组合压力场景通过
- 双 Agent 独立压力：生命周期 30 / 30 PASS；授权回归 13 个 mutation 中 5 个捕获、8 个存活
- 主 Agent 回归防漂移：8 个 mutation 中 6 个被捕获，2 个存活
- 本轮动作：只读测试与本报告；未修改运行规则、模板或测试源码

当前 Feature 流程没有复现此前的 Checker 误阻断：Feature Gate Checker 文件不存在，活跃运行权威没有 digest / `EVIDENCE_*` 路由，正常生命周期场景均能由 Agent 直接判断。但双 Agent 审计确认 later-start 的持久化语义存在一处 Gate 级冲突：规则一边要求 Gate 2 decision pair 和原 package review baseline 不可改写，一边又要求 later-start 将同一组单值字段改写为 `approve-and-start`。此外，focused contract 使用全文件子串存在检查，不能可靠阻止 owning section 退化。

## Scope Lock

### 目标行为

1. Gate 1 只确认 Feature 定义并授权准备实施包，不授权目标实现。
2. Gate 2 只有 package-only 和 approve-and-start 两个接受选择。
3. Feature Gate 不调用本地 digest Checker，不从脚本获得 Human authorization。
4. Agent 直接检查当前 Package Files、Story/Task/Plan/No-Plan、Human provenance、风险、验证、回滚和边界漂移。
5. accepted Story/Product Slice/Acceptance 内的 Task 拆分、替换或 Plan rotation 不因 ID 变化重复 Gate 2。
6. 新 Story/Acceptance、执行边界、Human-gated Task 或独立 Gate 仍停止或返回拥有它的 Gate。
7. Pause、Resume、验证失败、Submit、Close 和 Git 保持原有规则。

### 非目标

- 不恢复或重新设计 Feature Gate Checker。
- 不测试目标项目真实业务代码。
- 不创建本仓库根目录 `.agent-loop/`。
- 不修改版本号、installed Skill、分支或 Git 历史。
- 不把历史 Proposal、历史报告或 1.5.1 Changelog 当当前 runtime authority。

## 工作区保护

测试前记录：

```text
branch=v1.5.2
head=9a5c5183b47c022e8851f1098697f902e9d38daa
status_sha256=3971ea576e5c92204014c709cb05df76d551b43404b825eb73cd780378cac06b
diff_sha256=0c3feb14f1e01004eeb97f5074675457489159e4918c4a06435ec731df288301
tracked/untracked/deleted=43/18/1
```

所有 mutation 都在系统临时目录的仓库副本中执行。测试结束后，报告写入前重新计算的 status/diff 指纹完全一致，证明混沌操作没有改动源工作区。本报告新增后只增加一个未跟踪报告文件。

## 正常基线

命令：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_review \
  tests.test_python_checker_contract -v
bash tests/validate-feature-construction-two-gate-review.sh
```

结果：

- Python：24 / 24 PASS
- Shell：1 / 1 PASS
- `scripts/check-feature-review.py`：不存在
- 活跃 authority 的 Checker/digest/`EVIDENCE_*` 残留：0
- `scripts/check-feature-context.py`：保留
- root managed blocks：13

## Mutation Chaos

### 第一组

每个变体都在新的临时仓库副本中修改，然后运行 `tests.test_feature_review` 和 `validate-feature-construction-two-gate-review.sh`。

| Mutation | 结果 | 捕获入口 |
|---|---|---|
| 重新创建 `scripts/check-feature-review.py` | CAUGHT | Python + Shell |
| 在 runtime 恢复 Stable Digest 机制 | CAUGHT | Python + Shell |
| 删除 runtime Gate 1 路由 | CAUGHT | Python + Shell |
| 在 primary stage guide 加入“任意 Gate 2 选择可 accepted”冲突语义 | **SURVIVED** | 无 |
| later-start 恢复本地 preflight 要求 | CAUGHT | Python + Shell |
| 删除 `templates/notes.md` Package Files 字段 | CAUGHT | Shell |
| 从 Feature Auto-Loop stop rule 删除 commit/push/PR/merge/tag/release/publish | **SURVIVED** | 无 |
| 删除 root 两 Gate 提醒 | CAUGHT | Shell |

汇总：8 个 mutation，6 caught，2 survived。

### 存活变体复核

第二次使用精确 owning-section mutation 重现：

```text
primary-stage-approval-weakened: SURVIVED python=0 shell=0
feature-auto-loop-git-gates-erased: SURVIVED python=0 shell=0
refined-summary: total=2 caught=0 survived=2
```

这排除了“第一次改错位置”的解释。两个变体都能稳定通过当前 focused contract。

## Root Cause

### High — later-start 要求同时“保留”与“改写”同一 Gate 2 单值字段

独立生命周期 Agent 在 30 个场景全部通过后发现：

- `references/design.md:160` 和 `references/runtime.md:645` 将 Gate 2 decision/Auto-Loop pair 定义为不可改写的 durable review history；
- `references/runtime.md:670` 又要求 later-start 把 Gate 2 Decision、Feature Auto-Loop 和时间原子改写为 `approve-and-start` / `enabled` / 新 start time；
- `templates/notes.md:8-16` 只有一组单值字段，无法同时保存原 `package-only` review baseline 与 later-start event；
- `references/validation-scenarios.md:5051` 明确要求保留 original package review baseline。

这不是 Checker 问题，而是持久化模型没有给两个真实事件各自的落点。恢复 Agent 只能选择覆盖历史或不记录 start，两者都违反一部分权威规则。按照单功能评分方法，Gate 在不同 surface 给出冲突结论属于 unresolved High，因此报告不能评为 STRONG。

### Medium — focused contract 只验证全文件子串存在，不能阻止 owning section 内的冲突

证据：

- `references/stage-guides.md` 同一句 approval 规则出现在 Feature package 主段和 Analyze Consistency exit 段；修改主段后，另一处仍满足 `assertIn` / `grep -Fq`。
- `references/runtime.md` 的 Git/release 字符串同时出现在 Lightweight Change 与 Feature Auto-Loop；删除 Feature Auto-Loop 的独立 Gate 列表后，Lightweight Change 的同名字符串仍让测试通过。
- `tests/test_feature_review.py` 和 `tests/validate-feature-construction-two-gate-review.sh` 都是全文件 substring assertion，没有先切分 owning heading/section，也没有拒绝相反规则。

风险：未来维护者可能在关键 Feature owning section 引入相反语义，同时保留另一个位置的正确句子；focused 和全量 suite 都可能给出绿色结果。这不会让当前工作区立即错误，但削弱了对最需要保护的 Gate 和独立授权边界的防漂移能力。

授权边界 Agent 又对 13 个临时仓库副本做 mutation：5 个被捕获、8 个存活。存活项覆盖 owning section 相反 accepted 规则、later-start 恢复 local preflight、legacy 字段误授权，以及删除 Feature Auto-Loop 的 Git/Submit/Close/release stops。主 Agent 已独立复现其中两个核心变体：主 Gate 2 owning section 弱化和 Feature Auto-Loop Git/release stops 删除都仍能通过 Python 与 Shell focused tests。

建议修复边界：只收紧测试，不增加 Checker。将关键断言限定到：

1. `references/runtime.md` 的 `## Human Gate Modes` / Feature Auto-Loop 段；
2. `references/stage-guides.md` 的 Feature construction / Gate 2 owning 段；
3. 同时增加反向冲突 mutation，证明“正确重复文本”不能掩盖 owning section 退化。

### Low — Gate 1 exact Spec SHA-256 没有持久化字段

`references/stage-guides.md:996` 要求 Gate 1 接受时持久化 exact current Spec SHA-256，但 `references/runtime.md:645` 的字段清单和 `templates/notes.md:7-16` 均没有对应字段。该值目前没有唯一合法落点。它不影响正常 Gate 1/2 路由，但会造成恢复时的证据表达不一致。

本轮人类只要求测试，因此没有修改运行规则或测试源码。

## 双 Agent 独立混沌测试

### Agent A — Feature 生命周期

- 结果：30 / 30 PASS，0 FAIL。
- 覆盖：Gate 1 → Gate 2、正常执行、任务增加/减少/全替换、Plan/No-Plan、漏 `spec.md` / `tasks.md` / `tests.md` / Plan/detail、验证失败、Pause/Resume、context loss、later-start、close。
- 结论：正常路径不依赖已删除 Checker；缺失真实输入时仍能停止。发现上述 later-start High 和 Gate 1 SHA Low。

### Agent B — Gate / 授权边界

- 基线：19 个 unittest 与 3 个 Shell validator 全部 PASS。
- Mutation：13 个临时副本中 5 caught、8 survived。
- 捕获：原名 Checker 恢复、digest 恢复、Contract stop 删除、subagent stop 删除、root guidance 弱化。
- 存活：owning section 相反规则、重复正确文本掩盖冲突、later-start local preflight、legacy 字段误授权、Feature Auto-Loop Git/Submit/Close/release stop 删除。
- 结论：当前运行规则除已单列的 later-start 冲突外没有发现新增授权绕过；主要缺口是测试不能抵抗语义相反的变异。

两个 Agent 都只使用 `/tmp` fixture/副本，未读取历史 proposal/report 作为运行权威，未修改、暂存或提交仓库文件。

## Feature 生命周期场景

### 单场景

26 / 26 PASS：

1. Gate 1 只准备 package；
2. approve-and-start 接受并启用 Auto-Loop；
3. package-only 接受但不执行；
4. revise 返回 preparing；
5. pause 不制造 accepted 且清理 live mode；
6. later-start 重读当前 package，不调用 Feature Gate Checker；
7. within-boundary delta 可继续；
8. feature-definition drift 返回 Gate 1；
9. implementation-boundary drift 返回 Gate 2；
10. unresolved 只问一个 blocker；
11. accepted Story 内新增 Task 可继续；
12. 初始 Task 全部替换仍可依赖 Accepted Stories；
13. 新 Story/Acceptance 返回 Gate 2；
14. No-Plan 绑定缺失停止；
15. triggered detail 漏入 Package Files 时停止；
16. legacy hash 字段仅为 inert history；
17. Human provenance 不确定时重新确认一次；
18. Delivery Contract、subagent、Git、release Gate 不继承；
19. 验证缺失不能 `done`；
20. Task scope removal 必须使用 Human-approved `skipped`；
21. duplicate Gate 字段不能覆盖授权；
22. Feature Context 非 CURRENT 停止 Auto Mode；
23. Close 仍需显式确认；
24. 不存在本地 Feature Gate authorization issuer；
25. notes 保留语义 package evidence；
26. task template 保留 review/done discipline。

### 组合压力

14 / 14 PASS：

| 组合 | 预期裁决 |
|---|---|
| 紧急 + 缺 Plan/No-Plan | Gate 2/执行前停止 |
| package-only + context loss + durable evidence 缺失 | 只问一次 Gate 确认 |
| 同 Story 新 Task + 边界不变 | Agent assessment 后继续 |
| 同 Story 新 Task + 新依赖 | 停在 owning decision/Gate |
| legacy digest 不一致 + 当前证据完整 | 忽略旧 parser 噪音 |
| 测试通过 + Review/Drift 缺失 | 保持 review/in-progress |
| paused approve-and-start + 普通 continue | Strict，等待新 mode 确认 |
| approve-and-start + 未披露 Contract creation | 停在 Delivery Contract Gate |
| approve-and-start + commit | 停在 Git Gate |
| duplicate Gate fields + 看似合理 history | 停止并修复 current owner |
| triggered detail 遗漏 + 紧急 | 停止 package review |
| Feature Context refresh-required + 历史成功 | 停止并刷新语义 |
| 新 Story 伪装成 Plan rotation | 返回 Gate 2 |
| tasks/evidence 不完整 + 请求 close | 拒绝关闭并补齐前置条件 |

## 受影响回归与机械检查

### Python

运行：

```text
tests.test_feature_review
tests.test_python_checker_contract
tests.test_feature_context
tests.test_root_agents_blocks
tests.test_root_agents_lossless_slimming
```

结果：62 / 62 PASS。

### Shell

运行 8 个直接相关脚本：Feature two-gate、Feature Context、root block checker/refresh、root stage coverage、postfix pressure、human/version docs、Product Brief source gate。

结果：8 / 8 PASS。

### Mechanical

- SKILL YAML：PASS
- `plugin.json`：PASS
- 全仓库 Shell syntax：PASS
- 46 个 Python source AST：PASS
- Markdown fence：PASS
- `git diff --check`：PASS

本轮未重新运行 45 个 Shell 和 312 个 Python 的全量 suite，因为这是没有源码变更的单功能混沌评分；全量结果不计入本报告得分。前一份 2026-07-27 full-validation 报告已保存，但不冒充本次 fresh evidence。

## 五域评分

| Domain | 得分 | 结论 |
|---|---:|---|
| Requirement And Scope Fidelity | 15 / 15 | Checker 已移除；两个 Gate 与独立 Gate 范围没有漂移 |
| Logic, State, And Human Gates | 24 / 30 | 正常场景通过，但 later-start 的不可改写历史与单值字段改写规则冲突 |
| Cross-Surface Consistency | 16 / 20 | Gate 1 SHA 无模板落点，later-start baseline/event 没有统一模型 |
| Pressure Resistance | 22 / 25 | 正常与组合压力通过；双 Agent mutation 暴露 owning-section 防退化不足 |
| Evidence And Maintainability | 7 / 10 | 双 Agent、主 Agent 复现和回归证据充分，但 substring contract 维护性不足 |
| **总分** | **84 / 100** | **STABLE** |

## 推荐下一步

建议下一步先用现有 `notes.md` 内的事件记录区表达 later-start：保留 Gate 2 package-only baseline 的原字段，另设明确的 start transition 记录，避免覆盖历史；同时决定 Gate 1 Spec SHA 是补一个纯证据字段还是删除无落点要求。之后只收紧 focused regression contract，把 Gate 2 accepted 选择和 Feature Auto-Loop 独立 Git/Submit/Close/release stops 改为 owning-section scoped assertion，并固化负向 mutations。不要恢复 Checker，也不要增加新的 Gate。

截至报告完成：未 stage、未 commit、未 push、未 tag、未创建 PR、未 merge、未 release、未 publish、未同步 installed Skill。
