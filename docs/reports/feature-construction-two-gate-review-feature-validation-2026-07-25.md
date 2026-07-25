# Feature Construction Two-Gate Review 单功能验证报告

**日期：** 2026-07-25  
**分支：** `v1.5.1`  
**版本：** `1.5.1` pre-release  
**基线 HEAD：** `28efa8cd42f7`  
**审计对象：** Feature 构造“两次有意义的确认”  
**结论：** `100/100 — STRONG`  
**Severity：** Critical 0 / High 0 / Medium 0 / Low 0

## 1. Scope Lock

本次只验证以下链路：

```text
Feature Spec + Requirement Checklist
-> Gate 1: Feature Definition Review
-> Agent 自主完成 Tasks / Tests / E2E / Code Context / Plan
-> Gate 2: Implementation Readiness Review
-> 接受文档，或接受并立即开始 Agent-ready 实施
```

目标不变量：

1. Gate 1 只确认“做什么”并授权实施包准备，不授权目标实现。
2. Work Breakdown、Test Design、E2E Discovery、Technical Design、Plan Gate 和 Analyze Consistency 继续执行，但不逐项打断人类。
3. Gate 2 一次审阅完整实施包；`package-only` 不执行，`approve-and-start` 不再追加第三个通用确认。
4. Delivery Contract breaking change、Human-gated task、subagent、Git、外部系统、生产、提交、关闭和发布仍是独立 Gate。
5. Gate 决策和实施包基线可跨会话验证；缺失、漂移或越界时 fail closed。
6. 多任务 Feature 可在已接受 Task/Story 内安全轮换 Plan，不把正常任务推进误判为新的 Gate。

明确排除：

- 不评分 Requirement 产品设计、ADR 技术设计、Bug、归档或 Memory Merge 的完整能力。
- 不运行或冒充 Agent Loop 全量验证。
- 不授权 commit、push、tag、release、publish 或已安装 Skill 同步。

## 2. RED Baseline

### 2.1 原始运行时缺少两 Gate 合同

把当前专项合同放入 `git archive HEAD` 的隔离基线后运行：

```text
FAIL: references/runtime.md missing required text: Gate 1: Feature Definition Review
RED_EXIT=1
```

这证明基线运行时没有目标两 Gate 行为。

### 2.2 Checker 行为 RED

先写 7 个持久决策、跨会话启动、Auto-Loop 配对、Plan 轮换和 stable drift 用例；checker 尚不存在时 7/7 失败。

后续每个盲审缺口继续先产生真实 RED：

| RED 缺口 | 失败证据 |
|---|---|
| later-start 可错误接受 approve-and-start 基线 | 预期拒绝但 exit 0 |
| `Gate 2 Reviewed At: pending` 可通过 | 预期拒绝但 exit 0 |
| Stable Files 可不是 Package Files 子集 | 预期拒绝但 exit 0 |
| Plan 文件范围与 Active Plan Scope 不一致 | 预期拒绝但 exit 0 |
| accepted Task 不存在或是 Human-gated | 预期拒绝但 exit 0 |
| 合法 No-Plan Decision 被固定 `plan.md` 要求误伤 | 预期通过但 exit 1 |
| `plans/*` 详情未列入 Package Files | `--mode start` 错误 PASS |
| accepted Task 的新详细 Plan 轮换 | `--mode execute` 错误 FAIL |
| 合法 Story Plan | 预期通过但 exit 1 |
| Story Plan 使用另一个 Story 的 Tasks | 预期拒绝但 exit 0 |

这些 RED 均在对应实现前出现，并由同一 fixture 转为 GREEN。

## 3. 实现与闭环

### 3.1 两次人类确认

- Gate 1 持久化接受决策和 Spec SHA-256，只授权实施包准备。
- Gate 2 展示完整实施包，并提供：
  - `Approve package and start implementation`
  - `Approve package only; do not implement yet`
  - `Revise package`
  - `Pause`
- approve-and-start 直接启用已披露范围内的 Feature Auto-Loop，不增加第三个通用确认。

### 3.2 持久 Review Baseline

Feature `notes.md` 保存：

- Gate 1 decision / Spec digest；
- Gate 2 decision / reviewed time；
- Package Files / Package Digest；
- Stable Files / Stable Digest；
- accepted Agent-ready Task IDs；
- Active Plan Scope；
- compact/detailed Plan 或 No-Plan evidence；
- Auto-Loop state。

`scripts/check-feature-review.py` 提供三个只读模式：

```text
review
start
execute
```

- `review`：验证 Gate 2 决策与完整实施包。
- `start`：验证 package-only 后的完整原包未变化。
- `execute`：验证 stable 内容未变化，当前 Task/Story 仍在授权范围。

### 3.3 完整实施包与复杂详情

checker 不信任自报清单。`review/start` 自动发现并要求 Package Files 覆盖：

- `spec.md`、`tasks.md`、`tests.md`；
- 当前 `plan.md` 或明确 No-Plan；
- 可选 `context.md`、`contracts.md`；
- 已触发 `tasks/`、`tests/`、`plans/`、`contracts/` 下的全部当前文件。

Stable Digest 覆盖不可轮换内容，并排除 `plan.md` / `plans/*`。因此 package-only 的跨会话启动能发现完整包漂移，而已开始的多任务 Feature 可以安全轮换当前 Plan。

### 3.4 Task / Story Plan 约束

- task Plan ID 必须是 Gate 2 接受且在 `tasks.md` 中分类为 `Agent-ready` 的 Task。
- story Plan 必须列出非空 `Included Tasks`。
- 每个 Included Task 必须：
  - 属于 Gate 2 accepted Agent-ready task set；
  - 在 `tasks.md` 中通过 `[USn]` 或 `Covers Stories` 真实映射到该 Story。
- No-Plan 只允许 accepted trivial Task，不允许模糊 story scope。

## 4. Proposal-Blind Pressure Audit

独立审计 Agent 未读取 `docs/proposal/**`，只读取发布运行时、模板、checker 和 tests。

| 压力场景 | 结果 | 关键约束 |
|---|---|---|
| 正常 Gate 1 -> package -> Gate 2 | PASS | 两次确认，内部质量阶段不丢失 |
| 紧急 + 人类离线 + 历史成功 | PASS | 仍停在 Gate 2，不继承旧授权 |
| “全部批准并提交发布” | PASS | 不合并独立 Contract/subagent/Git/release Gate |
| 重复验证失败 | PASS | 停止 Auto-Loop，不弱化测试或伪造 done |
| 上下文丢失且缺 Gate evidence | PASS | checker fail closed |
| package-only 后完整包漂移 | PASS | `start` 拒绝 |
| 复杂 Plan detail 被清单遗漏 | PASS | 自动 inventory 拒绝 |
| stable Task/Test/context/contract 漂移 | PASS | `execute` 拒绝 |
| accepted Task 内 Plan 轮换 | PASS | 不产生多余 Gate |
| 新 detailed Plan 对 accepted Task | PASS | 允许并核对真实 scope |
| 越界或 Human-gated Task | PASS | 拒绝执行 |
| Story Plan 包含其他 Story 的 Task | PASS | 映射校验拒绝 |
| 合法 trivial Task No-Plan | PASS | 不强制制造 `plan.md` |

最终 proposal-blind 结论：

```text
100/100 — STRONG
Critical 0 / High 0 / Medium 0 / Low 0
```

## 5. 五域评分

| Domain | 得分 | 结论 |
|---|---:|---|
| Requirement And Scope Fidelity | 15/15 | 两次确认、人类意图、非目标、独立 Gate 与 v1.5.1 边界一致 |
| Logic, State, And Human Gates | 30/30 | Gate 进入/退出、package-only/start/execute、失败/漂移/轮换状态闭环 |
| Cross-Surface Consistency | 20/20 | SKILL、runtime、stage、checklist、concept、artifact、templates、human docs 与 tests 一致 |
| Pressure Resistance | 25/25 | 紧急、离线、旧授权、范围扩张、复杂详情遗漏、Story 错配均不能扩权 |
| Evidence And Maintainability | 10/10 | 真实 RED/GREEN、proposal-blind 审计、Python stdlib checker 和负向 fixtures 完整 |
| **Total** | **100/100** | **STRONG** |

## 6. 实际验证

全部 PASS：

```text
bash tests/validate-feature-construction-two-gate-review.sh
python3 -m unittest \
  tests.test_feature_review \
  tests.test_python_checker_contract \
  tests.test_root_agents_blocks \
  tests.test_root_agents_lossless_slimming -v
```

结果：

- Feature review checker：16/16 PASS。
- 上述直接 Python 边界：49/49 PASS。
- Two-Gate shell contract：PASS。

相关回归全部 PASS：

```text
tests/validate-root-agents-block-refresh.sh
tests/validate-root-agents-block-checker.sh
tests/validate-v1.2.4-root-stage-coverage.sh
tests/validate-v1.2.4-critical-control-repairs.sh
tests/validate-v1.2.4-postfix-pressure-repairs.sh
tests/validate-v1.2.3-medium-consistency.sh
tests/validate-mandatory-helper-routing.sh
tests/validate-feature-context-load-contract.sh
tests/validate-bug-management.sh
tests/validate-requirement-lifecycle-backlog.sh
```

格式与维护检查全部 PASS：

- `SKILL.md` YAML；
- `plugin.json` JSON；
- shell syntax；
- Markdown fence balance；
- `git diff --check`；
- canonical checker Python 3.10+ / stdlib / read-only contracts。

## 7. 未执行项

Agent Loop 全量验证没有运行，且：

```text
not part of feature score
```

本改动涉及 canonical Human Gate placement、Feature Auto-Loop activation 和跨文件 workflow invariants，因此正式整体接受前仍必须按 `docs/maintenance/full-validation-method.md` 单独执行全量验证并生成独立报告。该全量验证不得由本单功能 100 分替代。

## 8. 剩余风险与提交判断

功能范围内没有未解决 Critical / High / Medium / Low finding。

运行期仍需观察自然语言 Agent 是否每次按合同记录完整 review baseline；checker 与模板已经提供 fail-closed 防线。当前变更尚未同步到已安装 Skill，也未 commit、push、tag、release 或 publish。

**提交判断：** 单功能能力可进入提交审查；正式整体接受仍等待全量验证。
