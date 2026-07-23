# Agent Loop v1.4.0 Post-Merge Memory Reconciliation 全量验证报告

## 结论

当前未提交工作区通过 Post-Merge Memory Reconciliation focused validation、完整 Python/Shell 回归、六域语义审计与机械检查，最终得分 `98/100 · STRONG`。Task 10 审计中发现的恢复事务完整性、全路径 post-check 和 report identity 漏洞均先建立新 RED，再修复并完成全量重跑；当前没有未解决的 Critical、High 或 Medium。

文件名沿用已批准 Implementation Plan 冻结的 `2026-07-16`；实际执行日期为 `2026-07-17`。

## 审计对象与库存

| 项目 | 实际证据 |
|---|---|
| 分支 | `alpha/v1.4.0` |
| HEAD | `7eddf63195a266b7f107bc2d5ca0bf0095391922` |
| 审计对象 | 当前未提交工作区，不是后续 commit |
| Skill / plugin / human docs 版本 | `1.4.0`，未升级 |
| Proposal | `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md` |
| Implementation Plan | `docs/proposal/v1.4.x/post-merge-memory-reconciliation-implementation-plan.md` |
| root managed block | `1.4.0-20260716.1`，`13/13` |
| 最终 Python inventory | `180` tests |
| 最终 Shell inventory | `38` files under `tests/*.sh` |
| 平台结论 | `macOS-verified / Windows-CI-RED-repaired-locally / exact-release-CI-pending` |

本次保持 Skill source repository maintainer perspective；没有在仓库创建目标项目 `.agent-loop/`，没有创建或切换 worktree/branch，没有派发 subagent，没有同步已安装 Skill。

## 最终评分

| 审计域 | 权重 | 域评分 | 结果 | 主要证据 |
|---|---:|---:|---|---|
| Logic Correctness | 20% | 98 | PASS | 两个独立 Human Gate、Gate 顺序、exact Plan Hash、单 SHA 单报告/单次成功、动作语义、stale/replay/restore fail-closed；Task 10 与 Human Review 漏洞均已建立 RED 并修复。 |
| Autonomy | 15% | 98 | PASS | Agent 先读四快照与 authority、分类并推荐；每轮只向人类提出一个真正阻塞问题，未知目录不会要求发布 whitelist。 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | 98 | PASS | 能力只在可靠 memory 与已验证 code integration 后进入；onboarding-db 只按 evidence overlap 定向更新，不替代 project memory。 |
| Development / Test Workflow | 20% | 99 | PASS | 保存两个修复周期的 RED，scan/check/apply/finalize/restore 使用 TDD；102 个 focused Python、9 个 affected shell、180 个 full Python、38 个 full shell 全通过。 |
| Memory | 15% | 99 | PASS | Target spine 只是 traversal/output baseline；四快照全路径 ledger、immutable/accepted/append-only/derived/package owner、retained post-state 和 restore 前置验证完整。 |
| Recommendation | 15% | 97 | PASS | missing evidence、unresolved red、stale plan、apply failure、restore failure 均有唯一 Recovery/Review 下一步；扣分仅来自 Windows 修复尚需由精确 release commit 的远程 runner 复验。 |
| **加权总分** | **100%** | **98/100** | **STRONG** | 当前 `Critical 0 / High 0 / Medium 0 / Low 1`。 |

Low 风险是首个 release-candidate Windows runner 已真实失败并完成本地 RED/GREEN 修复，但修复后的精确 release commit 尚未取得远程成功证据。CI 已把 macOS/Windows、Python 3.10/3.x、5 个 memory test modules 和 4 个 CLI entrypoints 固化；不得把本地 GREEN 表述成 Windows 已复验通过。

## RED → GREEN → REFACTOR

### 原始 RED 基线

在 runtime 实现前执行：

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
```

实际退出码 `1`，输出：

```text
FAIL: missing required file: references/memory-reconciliation.md
```

证据保存在 `docs/reports/agent-loop-v1.4.0-post-merge-memory-reconciliation-red-baseline-2026-07-16.md`。

### Task 9 跨平台 RED

在 checker contract 要求新能力进入跨平台 CI 后，得到 `1 test / 9 failures`：缺少 5 个 memory test modules 和 4 个 command entrypoints。更新 `.github/workflows/cross-platform-checkers.yml` 后同一 contract 为 GREEN。

### Task 10 语义审计 RED

全量机械测试首次为 `164/164 Python PASS`、`38/38 Shell PASS`，但六域审计仍发现下列真实漏洞；这证明机械 PASS 没有替代语义审计。

| 修复前问题 | 严重级别 | RED 证据 | 修复 |
|---|---|---|---|
| restore 未重新验证 canonical Plan Hash，也未证明 journal operation 与 reviewed plan 一一对应；已完成/verified transaction 仍可被 restore | Critical（已修复） | `tests/test_memory_reconciliation_restore.py:141,158,179` | `scripts/memory_reconciliation_support.py:1239` 统一验证 plan、journal schema、operation cardinality/identity、preimage/backup、completion ledger；restore 只接受 `待确认` 和可恢复 internal states。 |
| journal 可伪造 `created_directories` 并删除非计划空目录 | High（已修复） | `tests/test_memory_reconciliation_restore.py:201` | created directory 必须唯一、路径安全、是计划 operation 的祖先，且不能在 Result snapshot 中原本存在。 |
| post-check/restore 没有直接核对所有无 operation 的 `保留` ledger 行 | High（已修复） | `tests/test_memory_reconciliation_check.py:330`、`tests/test_memory_reconciliation_restore.py:230` | scanner zero-change 和 checker/restore 直接比较 retained row 的完整 Result snapshot；restore 在第一笔 reverse mutation 前完成全 ledger 验证。 |
| collision-safe report ID 的第 13 位以后不必继续匹配 full SHA | Medium（已修复） | `tests/test_memory_reconciliation_check.py:243` | `scripts/memory_reconciliation_support.py:550` 要求整个短 ID 始终是 full Merged Code SHA 的真实前缀，长度不超过 full SHA。 |

这些 RED 均先在旧实现上复现失败；修复后新增 `7/7` regression tests 全部 GREEN。没有删除或弱化既有断言。

### Human Review 补充语义审计 RED

首次报告的 `Critical 0 / High 0 / Medium 0` 结论被重开。新的独立复现发现并修复：

| 修复前问题 | 严重级别 | RED 证据 | 修复 |
|---|---|---|---|
| 同一 full Merged Code SHA 可用不同长度前缀拥有两份报告并绕过单次成功约束 | High（已修复） | `tests/test_memory_reconciliation_check.py:262` | `memory_reconciliation_support.py:_validate_unique_merged_code_report` 在 scan/apply 前检查 sibling report 的 full SHA。 |
| action 只校验枚举值，`引入` 可覆盖、`移除过时声明` 可实际写文件 | High（已修复） | `tests/test_memory_reconciliation_check.py:297` | `_validate_operation_semantics` 绑定 Result、preimage、post-state 与 content source；`重算` 保留 absent-derived-index 合法路径。 |
| human-source / accepted-authority 可用 inline forged bytes 伪装为引入 | High（已修复） | `tests/test_memory_reconciliation_check.py:316` | immutable import 只接受同路径 recorded `100644/100755` Git blob。 |
| Merge Context 的四个文本边界可为空 | High（已修复） | `tests/test_memory_reconciliation_scan.py:138`、`tests/test_memory_reconciliation_check.py:276` | scanner 与 plan/checker 双层拒绝空白 branch/release/customer context。 |
| Source-only future directory Apply 后父目录与 Result absence 冲突，Finalize 无法收敛 | High（已修复） | `tests/test_memory_reconciliation_apply.py:383` | scanner/checker 从 planned child postimage 派生父目录 Desired post-state；Restore 允许该目录的合法事务中间态。 |
| Restore 在 journal=`restored` 后崩溃会永久失去续跑路径 | High（已修复） | `tests/test_memory_reconciliation_restore.py:267` | `_finish_restored_transaction` 重验原树，并幂等完成报告状态和 transaction cleanup。 |
| `git cat-file -p` 把 tree 输出当成文件内容 | Medium（已修复） | `tests/test_memory_reconciliation_check.py:429` | 先用 `git ls-tree` 要求 exact `100644/100755 blob`，再按 object ID 读取 bytes。 |
| CI workflow 有用但未列入已批准 file map | Medium（已修复） | Implementation Plan diff review | 将 `.github/workflows/cross-platform-checkers.yml` 明确纳入文件责任范围，不改变外部执行证据结论。 |
| 初版动作修复把 absent derived-index 的合法 `重算` 一并阻断 | Medium（已修复） | `tests/test_memory_reconciliation_check.py:361` | 在不放松 rewrite/remove/import 的前提下允许 `重算` 从 absence 或 exact preimage 生成派生文件。 |

补充 RED 全部在生产修复前或语义收窄前实际失败，之后逐项 GREEN；旧的 STRONG 分数没有直接沿用。

### Release Gate Windows CI RED

release-candidate commit `6222f3e1aca1d6df91ca477742e96eefade0f3b2` 的 run `29565218056` 中，macOS 3.10/3.x 成功，Windows 3.10/3.x 均在 native checker contract 失败。日志证明不是 workflow 配置问题，而是三个真实跨平台契约缺口：默认 Windows stderr 把中文 action 变成 `\\uXXXX`，Apply 把不可表达的 executable bit 当成 postimage drift，两个 mode 测试把 POSIX 断言错误设为 Windows 必需。

新增 `test_pre_check_emits_utf8_errors_under_ascii_host_stdio` 与 `test_regular_file_mode_matching_is_platform_aware` 后先得到 `2/2 RED`，再将 CLI 输出固定为 UTF-8，并把 `100644/100755` 等价严格限制在 native Windows 的已证明普通文件 worktree mode；POSIX、bytes、hash、kind、Git source、path、identity 和 transaction checks 未放松。本地定向 `4/4`、focused `104/104`、full `182/182` 与 shell `38/38` 已 GREEN；tag 仍等待修复 commit 的四矩阵远程 CI。

### 最终 GREEN

```text
focused Python: 104/104 PASS, 83.886s
focused affected Shell: 9/9 PASS
full Python: 182/182 PASS, 99.974s
full Shell: 38/38 PASS
```

## 六域语义审计

### 1. Logic Correctness — PASS

- Gate 顺序唯一：`Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate -> Push Gate -> Release Gate -> Source Branch Cleanup Gate`。
- Start 只授权创建报告与只读调查；Exact Rewrite Plan 只授权一个 normalized Plan Hash。
- code merge、Memory Start、Plan Hash、Memory Commit、Push、Release、Cleanup 权限不能复用。
- `待确认`、`已恢复`、unresolved transaction、stale evidence、missing report 均阻断后续 Git/发布动作；`已完成` 只允许展示下一个独立 Gate。
- Apply 只执行 bounded memory operations，报告里的 command/hook 永不执行；restore 不运行 `git reset` 或分支动作。
- completed replay、verified residual、tampered plan/journal/backup、unsafe path、preimage drift 和 retained drift 均 fail closed。
- 一个 full Merged Code SHA 只能有一个 canonical report；不同短前缀、action label 伪装、空 context 和非普通 Git blob 均不能到达 transaction 创建。

### 2. Autonomy — PASS

- Agent 使用 Target spine 建立读取顺序，再对 Base/Source/Target-before/Result 全路径记账；不会等待人类列举目录。
- Agent 先识别 stable identity、semantic role、question-specific authority、推荐 action/desired value，再请求一个 blocker。
- Source future directory 与 unknown directory 均进入 ledger；前者可按 evidence 分类，后者保持 visible/blocking，不要求修改 canonical layout 才能继续。
- scripts 只处理 inventory/hash/validation/apply/restore，不冒充产品、环境、customer 或 Human Decision 判断。

### 3. Project Entry / Onboarding — PASS

- capability 不新增 Project Entry artifact，也不会在 Init/Entry 默认创建 `memory-merges/`。
- 只有 stable verified Merged Code SHA、四个 full SHA、可靠 memory root、branch/release/customer context 完整时才进入。
- 缺证据时进入 Recovery，不猜 SHA、不隐式迁移 `.agent-loop` / legacy `agent-loop`。
- onboarding-db 只有 evidence overlap 时定向重写；不全量重建、不替代 project memory。

### 4. Development / Test Workflow — PASS

- canonical procedure、report template、四个 Python commands、support module、runtime/design/owners/root/human docs 和 scenarios 同步完成。
- Scan read-only；check 三阶段 read-only；Apply 使用 exact hash、atomic writes、report-local journal/backups；Finalize 是唯一完成状态入口；Restore 可跨进程恢复。
- Task 10 的真实漏洞都遵循新 RED -> 最小修复 -> focused GREEN -> full GREEN。
- 跨平台 checker contract 使用 Python 3.10+ standard library，没有新增第三方依赖。

### 5. Memory — PASS

- Target Canonical Memory Spine 不是事实排名或路径白名单；Target claims 仍需对应 owner 验证。
- immutable human source、accepted Requirement/ADR/Human Decision、append-only evidence、current semantic state、derived index、validated package、transaction temporary 和 unclassified 的边界明确。
- `project.md` 只保存当前 report locator/status/blocker，不复制 ledger、diff、decision 或 transaction。
- Requirement、ADR、Contract、Bug、Feature Archive、Project Skill 和 onboarding owners 保持独立 Gate 与 lifecycle。
- retained paths、absence claims、directories、future paths、case/Unicode collision、symlink parent 和 report-local scope 均有机械回归。
- Source-only future directory 的父目录由 child operation 派生 Desired post-state；Restore 对 pre-apply、transaction 中间态和 restored tree 分别验证。

### 6. Recommendation — PASS

| Blocker | 唯一安全下一步 |
|---|---|
| 四 SHA / branch / release / customer / memory root 证据缺失 | Recovery，恢复证据，不猜测 |
| unresolved 🔴 / unclassified / `暂不处理` | Agent 继续查证并推荐，再问一个阻塞 Human Decision |
| Plan Hash / preimage / context stale | 重新 Scan -> Plan -> exact hash review |
| Apply 失败且 restore 成功 | 报告 `已恢复`，进入新 Plan 或 Recovery |
| restore 失败或 transaction 不可证明 | 保留 journal，Recovery only，阻断所有后续 Git gates |
| report `已完成` | 只展示下一个独立 Memory Commit 或后续 action Gate |

## Proposal 压力场景覆盖

`references/validation-scenarios.md` 保存 `A–AJ` 共 36 个显式场景；测试与 semantic audit 按以下组验证：

| 组 | 覆盖场景 | 结果 |
|---|---|---|
| Source/Target claims | Source-only Requirement/Feature、Target-only work、compatible append-only、both memories wrong | PASS |
| Authority conflict | code vs Requirement、code vs accepted ADR、Human Decision conflict、environment unverifiable/verifiable | PASS |
| Lifecycle/owner | branch-local Current Work、Bug verifying、archive locator、original source、Project Skill manifest、onboarding overlap | PASS |
| Git context | Source branch deleted、fast-forward/squash、Target not main、customer boundary、push before memory completion | PASS |
| Plan safety | semantic error without Git conflict、dirty Result、stale Plan Hash、completed replay、zero-change integration | PASS |
| Identity/action/context | duplicate report、action mutation mismatch、immutable forged import、blank context、tree/symlink as blob | PASS |
| Recovery | Apply interruption + restore success、restore failure、tampered backup/report/journal、verified residual | PASS |
| Discovery/path | Source future directory、unclassified directory、legacy root、case/Unicode/symlink pressure | PASS |
| Human review | grouped/dependent red decisions、one blocking question、exact Plan Hash invalidation | PASS |

## 机械与跨平台检查

最终执行结果：

```text
SKILL.md YAML: PASS
plugin.json JSON: PASS
all Shell syntax: PASS
all Ruby syntax: PASS (5 files)
Python compileall scripts/tests: PASS
Markdown fences: PASS
git diff --check: PASS
repository-local __pycache__: cleaned and absent
```

`.github/workflows/cross-platform-checkers.yml` 已在 `macos-latest`、`windows-latest` 与 Python `3.10` / `3.x` matrix 中运行 native suite，并检查四个 memory command 的 `--help`。本地实际运行平台为 macOS；首个 Windows run 的真实失败与修复已保存，修复 commit 的远程复验仍为发布前置条件。

## 通过的不变量

- `SKILL.md` 保持入口简洁，详细流程由 runtime/design/reference 承载。
- root template 只新增一条 routing sentence，没有复制完整算法或状态表。
- Memory Reconciliation 是 Submit / Integrate 内部方法，不是 canonical stage 或 message intent。
- Target baseline 不等于 truth；没有 global ours/theirs precedence。
- 报告 on-demand、每 full Merged Code SHA 一份、最多一次成功 Apply；sibling prefix 不能建立第二份 canonical report。
- 原始人类来源、accepted authority 和 append-only history 不被静默改写。
- 所有路径有 ledger owner；未知路径阻断，不因目录未登记而丢弃。
- Apply/restore 只触碰计划内 memory；业务代码、HEAD、refs、branch 和外部系统保持不变。
- code verification、memory reconciliation、commit、push、tag、release、publish、cleanup 的授权完全独立。

## 未采纳或降级的建议

- 未新增 `memory-reconciliation` canonical stage 或 message intent：Proposal 明确要求内部方法。
- 未将 Target、Source、Git merge result 或“较新时间”设为全局 truth：authority 必须按问题选择。
- 未用 artifact 目录 whitelist 替代全路径发现：future/custom paths 必须可进入 ledger。
- 未让 scripts 判断产品意义、环境真相、customer policy 或 accepted decision：这些仍由 Agent + owning Human Gate 处理。
- 未将 Memory completion 视为 commit/push/release/cleanup 授权。
- 未增加 YAML/JSON executable project schema、第三方包、数据库、daemon 或 merge driver。
- 未声称修复后的远程 Windows runner 已通过；只报告首个 CI RED、本地修复 GREEN 和仍待满足的精确提交复验条件。

## 剩余风险与范围漂移

- Low：Windows CI RED 已修复并本地 GREEN，但精确修复 commit 的远程成功结果仍待取得；未满足前不创建正式 branch/tag。
- 报告中的 domain/semantic verification 由 Agent 运行并记录实际 evidence，Python 只能验证 bounded PASS record 与结构/bytes，不能证明产品语义本身。
- 没有在真实业务项目执行 memory rewrite；所有 mutation/recovery 证据来自隔离临时 Git fixtures，符合源码仓库维护边界。
- `.github/workflows/cross-platform-checkers.yml` 最初未列入 Implementation Plan file map；现已补正为已实现 cross-platform contract 的明确范围。除此之外没有新增 stage、intent、lifecycle、owner、默认目录或 Git authority；没有版本升级、installed Skill sync 或外部 side effect，当前无未解决范围漂移。

## 权限与发布判断

实现与验证已满足进入 Human Review 的条件，不代表提交或发布授权。

```text
commit: not authorized
push: not authorized
tag: not authorized
release/publish: not authorized
installed Skill sync: not authorized
```
