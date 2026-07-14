# Onboarding Core Flow Completeness 单功能验证报告

**日期：** 2026-07-11
**分支：** `alpha/v1.3.0`
**版本：** 1.3.0
**审计对象：** 当前工作区中的 Onboarding Core Flow Completeness 功能改动
**验证方法：** `docs/maintenance/feature-validation-method.md`
**全量验证状态：** 未在最终 Scope Lock 后执行；人类明确要求默认只做单功能全量验证，全仓库/全技能验证不计入本报告得分

## 结论

| 项目 | 结果 |
|---|---|
| 总分 | 96 / 100 |
| 等级 | `STRONG` |
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 2 |
| GREEN 压力场景 | 3 / 3 PASS |
| 功能边界测试 | 7 / 7 PASS |
| 提交状态 | 未 commit、未 push、未 tag |

功能在已确认范围内形成闭环，可以进入提交前的人类审查。该结论只覆盖 onboarding-core-flow 功能，不代表整个 Agent Loop 已完成全量验证或发布验收。

## Scope Lock

### 目标行为

- Evidence Graph 在正式文档前发现 `critical` / `important` 核心流程、业务终态、变体、owner、副作用、恢复责任和 Evidence Chain。
- 核心流程不能停在 `accepted` / `pending` / `processing` 等非终态响应。
- callback、consumer、retry、DLQ、compensation、reconciliation 和 job 只要承担核心状态、副作用或恢复责任，就不能被拆成 future topic 来逃避闭环。
- critical/important flow 使用 Flow Slice Coverage，把关键行为映射到代码 evidence、Diagram IDs 和正文 section。
- Completeness Hard Gate 先于质量评分；missing/blocked critical slice 不能被平均掉。
- 核心流程默认使用 Overview/Boundary、Timeline/Sequence、ASCII State Machine；额外图由真实 complexity signal 触发。
- supporting flow 保持轻量，除非承担核心状态、副作用或恢复责任。
- stateless glossary、静态配置清单和纯索引不强制状态图。
- 仍只有 Onboarding Spec Acceptance 和 Onboarding Tasks Full Execution Gate 两个人类 Gate。

### 非目标

- 不改变 Project Entry Scan 边界或 onboarding 阶段顺序。
- 不增加 batch、diagram、slice 或 newcomer-ready Human Gate。
- 不以固定文件数、图数量或文档长度证明完整。
- validator 不宣称自动证明业务事实正确，只验证 artifact trace 和明确的结构不变量。
- 本报告不审计 Agent Loop 的无关 feature、submit、memory、ADR、contracts 或 project-local skills。

## 五域评分

| Domain | Weight | Score | Result | 扣分原因 |
|---|---:|---:|---|---|
| Requirement And Scope Fidelity | 15 | 15 | PASS | 无 |
| Logic, State, And Human Gates | 30 | 29 | PASS | critical/supporting 初始分类仍需要 evidence-based Agent judgment |
| Cross-Surface Consistency | 20 | 20 | PASS | 无 |
| Pressure Resistance | 25 | 24 | PASS | 合理 focused scope 与错误缩窄仍需语义审查区分 |
| Evidence And Maintainability | 10 | 8 | PASS | validator 只能证明 trace 结构；全仓库验证未获授权且不计入功能得分 |
| **Total** | **100** | **96** | **STRONG** | 0 Critical / 0 High / 0 Medium |

## RED Baseline

详细原话和证据见：

```text
docs/reports/agent-loop-v1.3.0-onboarding-core-flow-red-baseline-2026-07-11.md
```

修复前机械基线：原有测试通过，但新专项 contract 因缺少 `Core Flow Inventory` 失败。

三个只读 RED 场景全部 FAIL：

| Scenario | RED 行为 | 根因 |
|---|---|---|
| RED-1 | 把订单支付缩窄到同步 `PROCESSING`，callback/retry/reconcile/cancel 延期 | 没有业务终态闭合和关键 slice hard gate |
| RED-2 | 三图和章节齐全即可主观自评 4/5 | 缺少不可平均的 evidence/diagram/section trace |
| RED-3 | focused scope 可冒充 whole-project 完成；所有正式文档被迫画状态图 | scope claim 和 diagram relevance 规则不足 |

## GREEN 压力复测

| Scenario | Result | 修复后行为 |
|---|---|---|
| GREEN-1：同步 `PROCESSING` 截断 | PASS | `PROCESSING` 明确为非终态；webhook、retry、DLQ、reconcile、cancel 保留在同一核心闭环；缺失 slice 直接 FAIL |
| GREEN-2：三图齐但图文脱节 | PASS | Hard Gate 先于评分；目录级 evidence、缺 Diagram/Section 映射和缺 recovery slice 均不能 newcomer-ready |
| GREEN-3：8 服务复杂项目时间压力 | PASS | focused scope 不得冒充全项目；transaction/async/recovery/decision/runtime 图按信号触发；stateless 文档不编造状态图 |

三个 Agent 均只读修复后的发布规则，没有把 proposal 当运行时权威，也没有修改文件。

## Review Findings And Closure

最终只读 reviewer 首轮给出 `NOT READY`：1 High、4 Medium、1 Low。主 Agent 逐项验证并通过专项 RED/GREEN 关闭：

| Severity | Finding | Closure |
|---|---|---|
| High | validator 只验证任意 `D-*` / `§N` / 路径字符串，缺条件图和图文脱节仍可能通过 | 新增 detached-trace invalid fixture；validator 验证 Diagram 定义、真实 section、symbol/config evidence、call/data direction、placeholder、Hard Gate 顺序 |
| Medium | validator 错误拒绝合法 deferred core flow | 新增 valid-deferred fixture；planned 与 deferred 分支分别验证，deferred 要求 impact/missing/next |
| Medium | supporting flow 仍被 Flow 模板强制完整图组 | flow/spec/checklist 明确 critical/important 与 supporting 边界，supporting 承担核心责任时才升级 |
| Medium | Flow 模板缺 ERD、独立 runtime 和 troubleshooting 图 | 补齐 ERD / Model Relationship、Runtime / Deployment Topology、Observability / Troubleshooting Map 及自检 |
| Medium | reference 与 coverage/batch 评分维度漂移 | 统一 Failure / recovery、Troubleshooting、Evidence granularity、Consistency / gateway risk 等维度 |
| Low | `Review Gate`、`Human Review Status` 可能暗示额外 Gate | 改为 `Agent Review Check` 和 `Optional Human Review Notes` |

关闭这些 finding 后，专项 contract、相关回归和结构检查重新运行通过。

## Feature-Scoped Test Evidence

实际执行并通过：

```text
PASS tests/validate-onboarding-core-flow-completeness.sh
PASS tests/validate-evidence-graph-ddd-onboarding.sh
PASS tests/validate-project-entry-onboarding-reset.sh
PASS tests/validate-v1.2.4-state-lifecycle-repairs.sh
PASS tests/validate-v1.2.4-postfix-pressure-repairs.sh
PASS tests/validate-v1.2.3-routing-fixes.sh
PASS tests/validate-v1.2.3-medium-consistency.sh
feature tests: passed=7 failed=0
```

结构检查：

```text
SKILL YAML: PASS
plugin JSON: PASS
Ruby validator syntax: PASS
Focused Shell syntax: PASS
Changed Markdown fence balance: PASS
git diff --check: PASS
```

Artifact validator evidence：

```text
valid reference: PASS (1 planned, 0 deferred)
valid deferred fixture: PASS (0 planned, 1 deferred)
invalid missing recovery slice: expected FAIL
invalid detached diagram/section/evidence trace: expected FAIL
```

## Unexecuted Validation

- 最终 Scope Lock 后未运行 `for test_file in tests/*.sh` 全仓库测试。
- 未运行 `docs/maintenance/full-validation-method.md` 的六域全技能验证。
- 人类已明确规定：默认执行单功能全量验证；全仓库/全技能验证只有在明确允许后才执行。
- 本轮早期在该规则提出前曾运行过仓库测试基线；该历史输出不计入本报告得分，也不作为已授权的 full validation。

## Remaining Risks

### Low-1: Core-flow classification remains judgment-based

`critical` / `important` / `supporting` 初始分类仍依赖 Agent 阅读业务结果、state owner、副作用和恢复证据。规则通过“承担核心责任必须升级”缩小了空隙，但无法完全机械替代语义判断。

### Low-2: Validator proves trace, not truth

validator 可以拒绝缺 Slice、缺 Diagram 定义、悬空 section、泛化 evidence 和错误 Hard Gate 顺序，但不能证明代码路径陈述与真实业务绝对一致。真实正确性仍需 Evidence Graph 调查和 reviewer 审计。

## Submission Judgment

在 onboarding-core-flow 单功能范围内，当前结果为 `STRONG`，可进入提交前人类审查。

当前没有 commit、push、tag、release 或 publish 授权。全仓库/全技能验证也没有授权，不应把本报告描述为 release acceptance。
