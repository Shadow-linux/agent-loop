# Agent Loop v1.4.0 Post-Merge Memory Reconciliation RED 基线

## 基线信息

| 项目 | 证据 |
|---|---|
| 实际执行日期 | 2026-07-17 |
| 分支 | `alpha/v1.4.0` |
| HEAD | `7eddf63195a266b7f107bc2d5ca0bf0095391922` |
| Skill / plugin / human docs 版本 | `1.4.0` |
| root managed block revision | `1.4.0-20260716`，`13/13` |
| 修改前 Python baseline | `98/98 PASS` |
| 修改前 Shell baseline | `37/37 PASS` |
| 审计对象 | 当前未提交工作区 |

文件名沿用已批准 Implementation Plan 冻结的 `2026-07-16`；本报告正文记录实际执行日期。

## 已确认范围

本轮只在 Agent Loop Skill source repository 内实现已批准的 Post-Merge Memory Reconciliation。没有创建目标项目 `.agent-loop/`，没有创建或切换 branch/worktree，没有派发 subagent，没有修改版本，没有同步已安装 Skill，也没有执行 commit、push、tag、PR、merge、release 或 publish。

Proposal 与 Implementation Plan 在 RED 前是唯一 dirty scope：

```text
docs/proposal/v1.4.x/post-merge-memory-reconciliation.md
docs/proposal/v1.4.x/post-merge-memory-reconciliation-implementation-plan.md
```

## RED Contract

先新增：

```text
tests/validate-post-merge-memory-reconciliation.sh
```

该 contract 要求 canonical reference、report template、四个 Python command、runtime/design/Submit/Branch/root routing 以及明确的 Gate 顺序同时存在，并禁止以下行为：

- Memory Reconciliation 自动执行代码 merge；
- Target memory 无条件胜出；
- 忽略未知目录；
- completed report 重复 Apply；
- Memory merge 自动授权 push。

## 实际 RED 证据

执行：

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
```

实际退出码：`1`。

实际输出：

```text
FAIL: missing required file: references/memory-reconciliation.md
```

这证明当前发布 Skill 尚未具备 Proposal 要求的 canonical Memory Reconciliation capability，测试因第一个真实缺口失败，而不是因 shell syntax、既有回归或无关工作区问题失败。

首次用于捕获退出码的 zsh 包装命令误用了只读变量名 `status`；该包装器问题没有修改仓库内容。改为 `exit_code` 后重新运行并得到上述真实 RED。

## Human Review 重开后的补充 RED

主 Agent 在首次 Human Review 中没有沿用机械 GREEN，而是重新构造边界场景。下列实现后漏洞均在修复前稳定复现：

| RED 场景 | 修复前实际结果 |
|---|---|
| 同一 full Merged Code SHA 使用 12/13 位前缀创建两个报告 | 第二个报告没有命中 one-report invariant，只在后续报普通 ledger drift；独立复现中两份报告均可 Apply/Finalize。 |
| 空 Source/Target Branch、Target Release Context、Customer Boundary | Scan 返回 `0`；pre-check 直到 stale scan hash 才失败，未识别缺失上下文。 |
| `引入` 覆盖现有文件、`移除过时声明` 实际写文件 | `validate_plan_contract` 均未抛错。 |
| human-source 用 inline forged bytes 伪装为 `引入` | `validate_plan_contract` 未抛错。 |
| Git tree 伪装为 `git-blob` | pre-check 返回 `0`。 |
| Source-only future directory | Apply 返回 `0`，Finalize 返回 `1: retained postimage mismatch: domain-snapshots`。 |
| journal 已写成 internal `restored` 后进程退出 | Restore 返回 `1: restore transaction state: restored`；若报告已更新又返回 report-status 错误。 |
| 初版修复把 absent derived index 的合法 `重算` 一并阻断 | 新兼容性测试返回 `operation semantics: 重算`，证明修复范围过宽。 |

对应 RED 位于 `tests/test_memory_reconciliation_check.py:262`、`:276`、`:297`、`:316`、`:361`、`:429`，`tests/test_memory_reconciliation_scan.py:138`，`tests/test_memory_reconciliation_apply.py:383` 和 `tests/test_memory_reconciliation_restore.py:267`。GREEN 与最终全量结果只记录在 focused/full 报告，本 RED 报告仍不把历史失败表述为当前问题。

## 后续 GREEN 目标

后续实现必须让同一 contract 在不削弱断言的前提下转为 PASS，并继续完成：

- runtime/design/reference/template 协调更新；
- Python 3.10+ stdlib scan/check/apply/finalize/restore TDD；
- focused validation 与五域评分；
- full validation、六域审计和中文报告；
- Proposal/Implementation Plan evidence refresh；
- 最终停在 Human Review。

本 RED 报告只保存两个修复周期的失败证据；不以自身声称当前 GREEN、focused 或 full validation 已通过。
