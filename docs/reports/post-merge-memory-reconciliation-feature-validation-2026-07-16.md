# Post-Merge Memory Reconciliation 单功能验证报告

## 结论

Post-Merge Memory Reconciliation 在已批准范围内达到 `99/100 · STRONG`。专项逻辑、Gate、事务恢复、跨 surface 和压力回归均通过。后续 full validation 已作为独立审计完成；本报告仍只按 feature-scoped boundary 计分，不用全仓库结果替代专项结论。

文件名沿用 Implementation Plan 冻结的 `2026-07-16`，实际执行日期为 `2026-07-17`。

## Scope Lock

| 项目 | 证据 |
|---|---|
| 分支 | `alpha/v1.4.0` |
| HEAD | `7eddf63195a266b7f107bc2d5ca0bf0095391922` |
| Skill 版本 | `1.4.0`，未升级 |
| 审计对象 | 当前未提交工作区中的 Post-Merge Memory Reconciliation 实现 |
| 设计来源 | `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md` |
| 实施来源 | `docs/proposal/v1.4.x/post-merge-memory-reconciliation-implementation-plan.md` |
| 目标行为 | 代码合并后，以 Target 为 baseline、以四快照与领域 authority 为证据，生成单一报告并经 Start/Plan Human Gate 后安全 Apply、post-check、finalize 或 restore |
| 明确非目标 | 不新增 canonical stage/message intent，不执行 Git merge/commit/push/tag/release，不新增数据库/服务/依赖，不迁移 memory root，不同步已安装 Skill |
| root guidance | `1.4.0-20260716.1`，`13/13` managed blocks |

## 评分

| Domain | 得分 | 结论与扣分 |
|---|---:|---|
| Requirement And Scope Fidelity | 15/15 | Proposal 的角色、动作、状态、四 SHA、Target baseline、领域 authority 与非目标均有 owning source 和回归约束。 |
| Logic, State, And Human Gates | 30/30 | Start Gate、exact Plan Hash Gate、Memory Commit/Push/Release/Cleanup 独立；stale plan、replay、脏状态、失败恢复和 restore blocker 均 fail closed。 |
| Cross-Surface Consistency | 20/20 | `SKILL.md`、runtime/design、owners、templates、root routing、README/Usage、scenario 和 tests 已协调；没有新增 stage 或 intent。 |
| Pressure Resistance | 24/25 | 36 个显式压力场景与 79 个 memory command/support 单测覆盖关键组合；macOS 本地通过，Windows 由 CI matrix 定义但本次未取得远程运行结果。 |
| Evidence And Maintainability | 10/10 | 有保存的原始 RED、各命令 TDD RED/GREEN、Task 10 与 Human Review 语义审计的补充 RED、102 个专项 Python、9 个 shell 和跨平台 CI contract。 |
| **总分** | **99/100** | **STRONG** |

Severity：`Critical 0 / High 0 / Medium 0 / Low 1`。Low 为本次没有远程 Windows runner 的实际执行证据；它不影响本地逻辑闭环，但不得宣称 Windows 已实跑通过。

## RED → GREEN → REFACTOR 证据

### RED

原始 focused contract 首次运行退出码 `1`：

```text
FAIL: missing required file: references/memory-reconciliation.md
```

证据保存于 `docs/reports/agent-loop-v1.4.0-post-merge-memory-reconciliation-red-baseline-2026-07-16.md`。

随后分别确认 support/scan/check/apply/restore 命令不存在或契约缺失时对应测试为 RED。Task 9 还新增跨平台 CI 契约并得到 `1 test / 9 failures`：缺少 5 个 memory 测试模块和 4 个命令入口。

首次 Human Review 又复现同 SHA 双报告、动作伪装、人类来源伪引入、空 Merge Context、Source-only 父目录不收敛、`restored` journal 无法续跑、Git tree 伪 blob 共 7 类漏洞。修复后语义复核还用一个 RED 证明不能把合法的 absent derived-index `重算` 一并封死。

### GREEN

- focused contract：`PASS: Post-Merge Memory Reconciliation contract is complete`。
- feature-scoped Python：`102/102 PASS`，耗时 `89.283s`。
- affected shell：`9/9 PASS`。
- cross-platform CI contract：`1/1 PASS`；CI matrix 已包含 macOS/Windows、Python 3.10/3.x、5 个测试模块和 4 个命令 `--help`。
- YAML、JSON、focused shell syntax、feature Python syntax、Markdown fence、`git diff --check`：全部 PASS。

### REFACTOR

- full Git SHA 同时支持 Git SHA-1 的 40 位和 SHA-256 的 64 位；Plan Hash 始终固定为 64 位 SHA-256。
- scanner 只排除当前报告/事务 scope；若 `memory-merges/` 下仍有历史报告，父目录继续纳入 ledger。
- casefold 与 Unicode normalization collision 使用跨快照合成 inventory 验证，避免依赖当前文件系统是否能同时创建碰撞路径。
- 测试故障注入仅在 `AGENT_LOOP_TEST_FAILURE` 与 `AGENT_LOOP_ALLOW_TEST_HOOKS=1` 同时存在时有效，生产路径遇到单独注入变量会 fail closed。
- Task 10 进一步固化 reviewed plan/journal operation 绑定、verified/completed restore 阻断、created-directory ledger、retained-path 全局 post-check/restore 和 full-SHA report ID prefix；7 个新增 RED 均已转 GREEN。
- Human Review 修复增加 one-full-SHA/one-report 全局检查、action/preimage/post-state 绑定、immutable same-path regular-blob import、非空 Merge Context、派生目录 post-state、`restored` journal 幂等收尾和 tree/symlink 拒绝；随后收窄 `重算` 约束以允许从 absence 重建 derived index。

## Logic / Gate 不变量

- Target memory 是 primary spine/baseline，不自动成为真相；Requirement、accepted ADR、Delivery Contract、Bug、Feature Archive、Project Skill 和 onboarding-db 的 authority 不被覆盖。
- 四快照 union 中每条路径都必须被 ledger 精确归类；未知目录、Source future directory、target-only 内容和 absence claim 不得静默丢弃。
- Agent 先读取证据、分类和推荐，只有 Start Gate 与 exact Plan Hash review 向人类提出阻塞确认。
- `待确认`、`已恢复`、未恢复 transaction、stale Plan Hash、unresolved red row 均阻断后续 Memory Commit、push、release 和 source cleanup。
- Apply 只写计划内 memory path，不执行报告中的 command/hook，不修改业务代码、HEAD 或 refs；事务失败自动尝试同一 restore primitive。
- `已完成` 只由 post-check + zero-change + semantic evidence 后的 finalizer 写入；重复 Apply 被拒绝，verified residual 只允许幂等 finalize cleanup。
- 代码 merge 授权不能复用为 Start、Plan Hash、Memory Commit、Push、Release 或 Cleanup 授权。

## 压力场景矩阵

| 场景组 | 代表场景 | 结果 |
|---|---|---|
| 四快照与路径覆盖 | Source-only Requirement/Feature、Target-only work、Source future directory、unclassified directory、legacy root | PASS：全部进入 union/ledger；双 memory root 或隐式迁移 fail closed。 |
| 语义冲突 | conflicting current state、both memories wrong、code vs Requirement、code vs accepted ADR、Human Decision conflict | PASS：Target 不自动胜出；回到对应 owner/Human Gate。 |
| 历史与派生内容 | append-only Feature、Bug verifying、archive locator、onboarding、Project Skill manifest | PASS：保留 owner 规则；不借 reconciliation 改生命周期、移动 archive 或授权 skill execution。 |
| Git 与分支压力 | source branch deleted、fast-forward/squash、Target not main、customer boundary、push-before-memory | PASS：要求 recorded SHA/context；memory completion 不是任何 Git 动作授权。 |
| Plan/Apply 压力 | dirty result、stale hash、semantic-only conflict、completed replay、zero-change | PASS：preimage/hash/ledger/post-check 约束阻断漂移和 replay。 |
| 计划语义与身份压力 | 同 SHA sibling report、动作/实际 mutation 不一致、human-source forged import、blank context、Git tree 伪 blob | PASS：均在 transaction 创建前 fail closed，并指向 Recovery 或新 exact plan。 |
| 故障恢复 | mid-apply interruption、process restart、backup tamper、restore failure、unrelated drift | PASS：恢复前全量校验；失败保留 journal 并只允许 Recovery。 |
| 路径安全 | path escape、case/Unicode collision、symlink parent | PASS：写入前阻断，无计划外 mutation。 |
| 人类决策组合 | grouped/dependent red decisions、旧授权、离线/紧急隐含扩权 | PASS：依赖决策保持阻塞且逐项绑定 exact plan；不复用旧授权。 |

`references/validation-scenarios.md` 中保存 `A–AJ` 共 36 个显式场景；focused contract 对高风险场景名和 canonical invariants 做防漂移断言。

## 实际执行命令与结果

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
# PASS

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-memory-focused-pyc \
  python3 -m unittest \
    tests.test_memory_reconciliation_support \
    tests.test_memory_reconciliation_scan \
    tests.test_memory_reconciliation_check \
    tests.test_memory_reconciliation_apply \
    tests.test_memory_reconciliation_restore \
    tests.test_python_checker_contract \
    tests.test_root_agents_blocks -v
# Ran 102 tests in 89.283s ... OK

# Implementation Plan 指定的 9 个 affected shell tests
# focused shell tests passed: 9
```

格式和 hygiene 检查：`SKILL.md` YAML、`plugin.json` JSON、focused shell syntax、feature Python syntax、Markdown fence、`git diff --check` 全部 PASS。

## 独立全量验证与剩余风险

- 独立 full validation 已完成 `180/180` Python、`38/38` shell、六域语义审计和机械检查；详见 `docs/reports/agent-loop-v1.4.0-post-merge-memory-reconciliation-full-validation-2026-07-16.md`。这些结果用于整体验收证据，但 `not part of feature score`。
- 本机 macOS 已执行；Windows 兼容性通过 stdlib/path-safe 设计和 GitHub Actions matrix 固化，但本次没有远程 Windows runner 结果。因此当前证据为 `macOS-verified / Windows-test-defined`。
- 没有真实目标项目 `.agent-loop/`、真实 merge、push 或 release；测试全部使用隔离临时仓库和 synthetic fixtures，符合源码仓库维护边界。

## 权限与提交判断

专项与独立 full-validation 证据支持进入 Human Review，不等于提交或外部操作授权。

```text
commit: not authorized
push: not authorized
tag: not authorized
release/publish: not authorized
installed Skill sync: not authorized
```
