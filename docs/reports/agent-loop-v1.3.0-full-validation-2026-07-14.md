# Agent Loop v1.3.0 全量验证报告（Feature Monthly Archive）

验证日期：2026-07-14
分支：`alpha/v1.3.0`
基线 HEAD：`e49673c`
审计对象：当前未提交工作区中的 Feature Monthly Archive 实现及其协调 authority 变更
平台状态：`macOS-verified / Windows-test-defined`

## 1. 总结

总分：**98/100**
等级：**STRONG**
最终测试：**98/98 Python tests PASS；33/33 `tests/*.sh` PASS**
当前严重度：**Critical 0 / High 0 / Medium 1 / Low 0**

Feature Monthly Archive 已形成从只读 scan、确定性 plan、精确 SHA-256 Human Gate、事务 apply、post-check、失败 restore 到独立 rehydrate Gate 的闭环。目录归档只改变位置与 locator，不压缩、摘要替代或删除 feature 内容。当前唯一 Medium 是没有取得 Windows 远程成功 run，因此本轮不能声称跨平台验收完成。

## 2. 六域语义审计

| 审计域 | 结果 | 分数 | 通过的不变量 |
|---|---|---:|---|
| Logic Correctness | PASS | 99 | `feature-archive-maintenance` 位于 Memory Recovery 后、Active Feature Guard 前；archive state 不混入 lifecycle；stale plan、collision、unsafe reference、path escape 均 fail closed |
| Autonomy | PASS | 98 | Agent 可先做只读 evidence/eligibility/reference scan，输出唯一推荐；apply/rehydrate 必须停在精确 plan SHA-256 Gate |
| Project Entry / Onboarding | PASS | 98 | 先要求可靠 project memory；不把 archive 变成 onboarding 或新 canonical stage；源码仓库没有创建目标项目 `.agent-loop/` |
| Development / Test Workflow | PASS | 99 | Reader Compatibility 先行；RED/GREEN、整目录哈希、post-check、transaction restore、rehydrate-before-execution 闭环完整 |
| Memory | PASS | 98 | Feature ID 稳定；`features/archive.md` 仅为 locator；project/requirement/ADR authority 不被替代；stale locator/journal 路由 Recovery |
| Recommendation | PASS | 98 | 完成、stale-plan、restore failure、rehydrate 与 Follow-up 都有唯一下一阶段；auto mode 不能授权归档 |

加权结果为 98，且不存在未解释的 Critical/High。

## 3. RED 基线与修复证据

### 初始 TDD RED

- 初始 archive contract：27 个测试方法产生 28 个预期失败，证明 support/template/CLI/Reader Compatibility 缺失。
- Runtime contract：首先因 `SKILL.md` 缺少 Feature Monthly Archive authority 失败。
- CI contract：四个测试模块和四个 CLI 路径产生 8 个明确失败。
- Proposal status contract：先因缺少“已实现；待最终 Human Review”失败。

### Full Review 中发现并修复的 RED

| 发现 | 修复前证据 | 修复 |
|---|---|---|
| root block stale fixture 未随新 revision 更新 | 全量 shell 第 24 项失败 | 更新 stale fixture 的 source revision，保持 checker 真正验证 stale 状态 |
| 两个旧 precedence regression 仍要求 Archive 前的顺序 | 全量 shell 第 30 项失败 | 与新 `Feature Archive Maintenance` first-match order 同步 |
| 四个 responsibility-map authority surface 遗漏 | 新 runtime contract RED | 补 project decisions、requirement mapping、project memory、project guidance |
| `check --operation restore` 不可成功 | focused Python RED | 定义只读 `restore-check`，只接受精确 pre-transaction state |
| 篡改 journal 可用 `../` 把 feature 移出 workspace | 测试错误返回 0 并真实触发越界 move | 对 plan、apply、journal、backup、snapshot、created-directory 全部统一 workspace confinement |
| rename 后、completion record 前崩溃无法恢复 | 新进程 restore RED | 恢复时按 journal move 的实际 source/target 状态协调，不依赖 completion record 单点 |
| 大于 2 MiB 的 feature payload 未纳入 snapshots | large payload RED | 2 MiB 限制只用于 Markdown reference scan；整目录所有文件均进入哈希 |
| 引用更新移除 UTF-8 BOM 并把 CRLF 改为 LF | BOM/CRLF RED | 引用替换按原始字节哈希并保留 BOM/换行 |
| broken relative link 被计算新路径而未阻断 | broken-link RED | 不存在的跨边界链接分类为 `unsupported` 并阻断 apply |
| 同时篡改 journal 与内嵌 plan 并重算自哈希后，可用 `missing-before` 删除计划外文件 | 新 restore RED 错误返回 0，并实际删除 `README.md` | reference-edit 链必须从原 snapshots 起步；backup scope、状态、路径、哈希和字节在任何目录移动前完成预检 |
| restore 会覆盖崩溃后的人类修改 | 新 restore RED 错误返回 0 | source/target 状态和当前字节只允许事前或本事务中间状态；其他字节作为 `drift` 停止且保留 journal |
| stranded `.archive-txn` 不阻断新 scan/apply | 2 个新 RED 错误返回 0 | scan 与 apply 都先检查残留事务，并要求按显式 transaction ID 进入 Recovery |
| 项目记忆指向待移动 feature 的相对链接未被发现 | scan 无 edit，apply 后链接断裂 | reference impact 同时处理从 moving file 指向外部和从外部指向 moving target 的相对链接 |

所有修复都先保存失败证据，再运行对应 GREEN；当前没有保留的 Critical/High。

## 4. 最终可执行验证

### Python

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

结果：`Ran 98 tests`，`OK`。

专项复验：

```text
python3 -m unittest \
  tests.test_python_checker_contract \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply \
  tests.test_feature_monthly_archive_restore \
  tests.test_adr_requirement_model_trace
```

结果：`Ran 79 tests`，`OK`。

### Shell contracts

```text
for test_file in tests/*.sh; do bash "$test_file"; done
```

结果：33/33 PASS。两个 shell contract 内部还分别运行了 13 与 6 个 Python case；这些嵌套 case 未重复计入 98。

### 机械检查

| 检查 | 结果 |
|---|---|
| `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'` | PASS |
| repository `.yml` / `.yaml` parse | PASS |
| repository JSON parse | PASS（1 file） |
| `python3 -m compileall -q scripts tests` | PASS；随后删除生成的 `__pycache__` |
| Shell `bash -n` | PASS（34 files） |
| Ruby `ruby -c` | PASS（5 files） |
| Markdown fence balance | PASS（199 files） |
| tracked `git diff --check` + untracked `git diff --no-index --check` | PASS |

## 5. Proposal 验收条件逐项核对

| # | 验收条件 | 结果与证据 |
|---:|---|---|
| 1 | 5/6 月多个 closed feature 分月移动 | PASS：双月 apply fixture |
| 2 | 同月 paused 保持 flat，eligible 可归档 | PASS：mixed candidate scan |
| 3 | current/active/blocked/paused/open follow-up/incomplete close 拒绝 | PASS：逐项 eligibility tests |
| 4 | 移动前后文件清单和哈希一致 | PASS：完整 tree SHA-256；含 >2 MiB payload |
| 5 | 跨边界相对链接和 old flat path 更新 | PASS：precomputed exact edits；BOM/CRLF preserved |
| 6 | archive locator 解析全部 archived Feature ID | PASS：parser/resolver/ADR reader tests |
| 7 | ADR、Requirement Mapping、Project Memory、Follow-up 支持 month path | PASS：validator tests + coordinated authority contract |
| 8 | collision、case、Unicode、symlink、stale-plan、broken link 拒绝 | PASS：显式 regression；全部 fail closed |
| 9 | 中途失败恢复目录和引用 | PASS：test-only injected failure，完整事前 SHA-256 map 恢复 |
| 10 | 重复 apply 不产生嵌套 month | PASS：idempotency regression |
| 11 | rehydrate 整目录回 flat，Feature ID/内容不变 | PASS：locator 为 `rehydrated`，`spec.md` 仍 `closed` |
| 12 | Windows/macOS 相同 fixture 输出 | **未完成跨平台实跑**：workflow 已定义，状态保持 `Windows-test-defined` |
| 13 | scan/check 不修改文件 | PASS：全树 SHA-256 before/after equality |
| 14 | 无删除历史内容或 `--force` | PASS：runtime negative contract、CLI review、mutation review |

结论：除必须诚实保留的 Windows 远程运行证据外，Proposal 的本地行为验收条件均已落地。不能把第 12 项标记为跨平台已验收。

## 6. 关键压力场景

- Archive intent 与 Active Feature 同时存在：first-match 先进入 archive maintenance，但 active/paused candidate 在 eligibility 内阻断，不切换 active work。
- 旧 hash 重放：valid-but-different hash 返回 `stale-plan`，没有 journal 或写入。
- 原始需求出现 old path：记录 `immutable-requirement-source`，保持字节不变；无法确定的普通引用为 `unsupported`。
- Apply 在引用写入中断：journal 恢复目录、locator 和全部 backup bytes。
- Apply 在 rename 与 completion record 之间中断：新进程仍可根据 source/target 恢复。
- 恶意/损坏 plan 或 journal 使用 `../`：`path-escape`，不移动或读取 workspace 外路径。
- 外层 journal 与内嵌 plan 一起被重写并重算自哈希：reference-edit/snapshot 链不成立时在任何项目写入前拒绝；损坏 backup 同样在 move 前拒绝。
- 崩溃后人类修改了待恢复引用：当前字节不属于 pre/intermediate/post 允许集合，返回 `drift`，不覆盖人类内容。
- 残留 transaction 存在时再次 scan/apply：返回 `stranded-transaction`，不生成竞争 plan 或第二个 journal。
- Project Memory 以相对链接指向待移动 feature：scan 生成精确 edit，apply 更新到 month path，post-check 通过。
- Restore 碰撞：保留 `restoring` journal，不猜测、不覆盖。
- Archived follow-up：先独立 rehydrate Gate；rehydrate 不自动 reopen lifecycle。
- “为了省空间删除历史内容”或“手工移动绕过 scan”：超出能力范围并停止。
- Chat、Requirement、ADR、Delivery Contract、TDD、Submit、Pause/Close 等既有流程没有被 archive 自动模式旁路。

## 7. Code Review

已按 `requesting-code-review` 的 Spec Review / Standards Review 检查 plan alignment、错误处理、filesystem mutation、cross-platform bytes、测试真实性、runtime authority 与 production readiness。由于本轮没有获得 subagent dispatch 授权，未派发 reviewer subagent；由主 Agent 逐文件执行相同审查清单。首轮修复了 path escape；本轮又用 7 条 RED 封闭 journal scope/backup preflight、post-crash drift、stranded transaction 和 inbound relative-link 四类缺口。

Review 结论：本地实现可进入 Human Review；在 Windows job 成功证据出现前，不得宣称跨平台 acceptance 完成。

## 8. 当前问题与未采纳意见

### Medium

1. `.github/workflows/cross-platform-checkers.yml` 已定义 `windows-latest` × Python 3.10/3.x，但本轮环境没有 `gh` 或其他远程 run 证据。影响是跨平台结论只能为 `Windows-test-defined`，不影响 macOS 本地逻辑结论。

### 未采纳/未执行

- 未新增 third-party Python dependency、executable schema、canonical stage、default mapping artifact、per-feature summary、`historical/`、Deep Archive、删除或定时任务，因为均超出批准范围。
- 未派发 subagent code reviewer，因为 subagent dispatch 未获单独授权；使用本地主 Agent review，不把它伪装成独立 reviewer 证据。
- 未执行真实目标项目 archive/rehydrate；源码仓库只使用临时 fixture。

## 9. 实际变更面

### 实现、模板与 CI

- `scripts/feature_archive_support.py`
- `scripts/scan-feature-monthly-archive.py`
- `scripts/check-feature-monthly-archive.py`
- `scripts/apply-feature-monthly-archive.py`
- `scripts/restore-feature-monthly-archive.py`
- `scripts/checker_support.py`
- `scripts/check-adr-requirement-model-trace.py`
- `templates/feature-archive.md`
- `templates/notes.md`
- `templates/root-AGENTS.md`
- `.github/workflows/cross-platform-checkers.yml`

### Runtime / design authority

- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
- `references/concepts.md`
- `references/artifact-rules.md`
- `references/feature-follow-up.md`
- `references/feature-completion-check.md`
- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/human-review-summary.md`
- `references/recovery-and-backfill.md`
- `references/project-decisions.md`
- `references/requirement-management.md`
- `references/project-memory-mode.md`
- `references/project-guidance.md`
- `references/document-templates.md`
- `references/validation-scenarios.md`
- `examples/login-feature/notes.md`

### Tests、human docs 与证据

- `tests/feature_archive_test_support.py`
- `tests/test_feature_archive_support.py`
- `tests/test_feature_monthly_archive_scan.py`
- `tests/test_feature_monthly_archive_apply.py`
- `tests/test_feature_monthly_archive_restore.py`
- `tests/test_adr_requirement_model_trace.py`
- `tests/test_python_checker_contract.py`
- `tests/validate-feature-monthly-archive-runtime.sh`
- proposal/root revision/precedence 相关既有 regression tests
- `README.md`、`Usage.md`、`CHANGELOG.md`
- proposal、implementation plan、专项报告与本报告

## 10. 工作区隔离与范围漂移

以下既有工作不属于 Feature Monthly Archive，已保持原状且未纳入实现结论：

- `docs/proposal/v1.3.x/onboarding-core-flow-completeness.md`
- 删除中的 `docs/proposal/v1.4.x/mandatory-stage-helper-routing-plan.md`
- 删除中的 `docs/proposal/v1.4.x/project-group-feature-routing.md`
- `docs/proposal/v2.0.x/`

没有在仓库根创建目标项目 `.agent-loop/`，没有修改 skill version，没有创建真实 feature archive。

## 11. 发布与授权判断

当前推荐下一阶段：**Human Review**。

本轮未获得并未执行 commit、push、tag、PR、merge、release 或 publish。Windows 成功 run 和 Human Review 是后续验收证据；它们不应由本报告自动推导或替代。
