# Agent Loop v1.5.0 Root AGENTS Lossless Slimming RED Baseline

- 日期：2026-07-21
- 分支：`alpha/v1.5.0`
- HEAD：`3063201a3fee0adad9846fa33e977df30405d295`
- 审计对象：当前工作区
- Production template：224 行、3434 words、27370 bytes、13 managed blocks、revision `.1`
- 既有 dirty work：保留已批准的 root-routing / ownership 修改；历史 Proposal 和 Report 继续作为仓库内历史证据，不纳入本功能改写

## 实施前机械基线

保留历史报告及其原有路径，两个旧维护测试继续直接验证当前源码树中的历史证据，不依赖固定 Git commit 或仓库历史可达性。随后重新执行完整基线：

| 检查 | 结果 |
|---|---|
| Existing `tests/*.sh` | 39/39 PASS |
| Existing Python tests | 215/215 PASS |
| YAML / JSON / Shell syntax / Markdown fences / `git diff --check` | PASS |
| 冲突、目标项目 `.agent-loop/`、`__pycache__` | none |

## Focused RED

执行：

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_root_agents_lossless_slimming
```

真实结果：`Ran 6 tests`，`FAILED (failures=1, errors=1)`。

Production contract 报告以下目标缺口：

```text
line-count:224
canonical-template-has-cjk
managed-revision
gateway-contract
missing-contract:Inspect -> Classify Intent And P
missing-contract:Requirements / Concept -> Decisi
missing-contract:Requirement owns human source an
missing-gate:Semantic Gate
missing-gate:Scope And Risk Gate
missing-gate:Evidence Gate
missing-gate:External Mutation Gate
missing-gate:Git And Lifecycle Gate
auto-mode-gate-bypass
missing-completion:Code changes alone never make a task or Feature done.
missing-completion:Fresh verification, Review, Drift Check, and required Project Memory evidence precede completion.
missing-independent-lifecycle-gates
root-duplicates-detail:Requirement Model Scope Inventory
root-duplicates-detail:Requirement Model Technical Landing Trace
root-duplicates-detail:.archive-txn
```

`test_removing_gateway_is_rejected` 在旧 leaf-stage 表尚无 `No reliable memory` Gateway 行时产生预期 `StopIteration`；Implementation Plan 明确允许 mutation tests 在 Gateway 尚未安装时处于 RED。

## Harness 健康证据

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_root_agents_blocks
Ran 8 tests in 0.373s
OK

bash tests/validate-root-agents-block-checker.sh
PASS: root AGENTS block checker contract is complete
```

旧 `.1` managed-block 结构仍然有效；失败仅来自新的 `.2` lossless-slimming contract。

## RED 结论

Existing behavior baseline is green; the new lossless-slimming contract is red for the intended production gap. Production edits may begin.

## GREEN Closure

Task 2–5 已在保留上述 RED 原文的前提下完成 GREEN：

- canonical Root AGENTS：`170 lines / 1883 words / 15357 bytes`；13/13 managed blocks 使用 `.2`。
- `tests.test_root_agents_lossless_slimming + tests.test_root_agents_blocks + tests.test_python_checker_contract`：`33/33 PASS`。
- 23 个 Root 消费 Shell contracts：`23/23 PASS`。
- 两个读取历史验证证据的维护测试在无 `.git` 历史源码快照中：`2/2 PASS`；验证不依赖固定 Git object。
- 四个 mutation：删除 Gateway、交换 Gateway reference、删除 project-outcome ownership、删除 Gate class，全部被拒绝。
- `git diff --check`：PASS。

## 语义压力闭环

| 场景 | 结果 | 当前证据 |
|---|---|---|
| context compaction 后 controller unavailable | PASS | `templates/root-AGENTS.md:15-16`; `references/runtime.md:17` |
| new project / meaningful existing project | PASS | `references/runtime.md:264-276` |
| remote source / local mirror | PASS | `templates/root-AGENTS.md:70`; `references/runtime.md:306-315` |
| stale / outside-loop memory | PASS | `templates/root-AGENTS.md:71`; `references/runtime.md:337-346` |
| requirements shaping / defined Lightweight change | PASS | `templates/root-AGENTS.md:74-75`; `references/project-guidance.md:29` |
| explicit Bug / generic fix wording | PASS | `templates/root-AGENTS.md:51,73-74`; `references/runtime.md:374-376` |
| accepted Requirement needs ADR / simple no-ADR Feature | PASS | `templates/root-AGENTS.md:78-79`; `references/project-decisions.md:54-82` |
| Feature continuation at Product Brief, Checklist, Plan, Verify, Drift leaves | PASS | `templates/root-AGENTS.md:79,86`; `references/runtime.md:470-527` |
| Operational diagnosis / implementation | PASS | `templates/root-AGENTS.md:80`; `references/runtime.md:362` |
| Project Skill discovery/loading / Execution Gate | PASS | `templates/root-AGENTS.md:19,81,105`; `references/runtime.md:368-421` |
| Archive scan / apply and rehydrate | PASS | `templates/root-AGENTS.md:72,105`; `references/runtime.md:48,627` |
| post-code-merge reconciliation / later Git gates | PASS | `templates/root-AGENTS.md:82,124-129`; `references/runtime.md:459` |
| Auto Mode versus six Gate classes | PASS | `templates/root-AGENTS.md:92-109` |
| tests pass but Review/Drift/Memory absent | PASS | `templates/root-AGENTS.md:112-119` |
| commit request with unrelated dirty work | PASS | `templates/root-AGENTS.md:122-129` |
| ordinary Chat without artifact/action intent | PASS | `templates/root-AGENTS.md:84`; `references/runtime.md:54-56` |

本轮压力检查未发现新的语义缺口，因此没有伪造额外 RED 或加入未验证 prose。Task 6 将执行全量回归和六域审计。
