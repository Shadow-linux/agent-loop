# Agent Loop v1.3.0 Feature Monthly Archive 专项验证报告

验证日期：2026-07-14
验证范围：Feature Monthly Archive（目录归档、locator、Reader Compatibility、scan/check/apply/restore/rehydrate）
平台结论：`macOS-verified / Windows-test-defined`
版本结论：沿用 v1.3.0 开发线，未修改版本号

## 1. 结论

Feature Monthly Archive 的本地专项实现通过。归档只把经过人类确认的完整 closed Feature 目录移动到 `.agent-loop/features/YYYY-MM/<feature-id>/`，并维护根级 `.agent-loop/features/archive.md`；没有内容压缩、per-feature summary、`historical/`、Deep Archive、删除或自动调度能力。

本地最终 focused 回归为 79/79 个 Python 测试通过、2/2 个专项 shell contract 通过。由于当前环境没有可用的远程 Windows run 证据，跨平台结论不能写成已验收，只能保持 `macOS-verified / Windows-test-defined`。

## 2. RED 基线

| RED 阶段 | 真实结果 | 证明的缺口 |
|---|---:|---|
| 初始 archive contract | 27 个测试方法运行，产生 28 个预期失败 | support module、archive template、四个 CLI 与 Reader Compatibility 尚不存在 |
| Runtime coordinated contract | 1 个 shell contract 失败 | `SKILL.md` 尚无 Feature Monthly Archive runtime authority |
| Cross-platform CI contract | 1 个测试方法产生 8 个失败 | 四个 archive 测试模块和四个 CLI 路径尚未进入 Windows/macOS workflow |
| Proposal implementation status contract | 1 个 shell contract 失败 | proposal 仍停留在设计/计划状态，没有标记为“已实现；待最终 Human Review” |
| Responsibility-map contract | 1 个 shell contract 失败 | project decision、requirement mapping、project memory、project guidance 与 execution-path negative assertion 尚未同步 |
| Restore check contract | 1 个 Python 测试失败 | `check --operation restore` 虽出现在 CLI contract 中，但没有可到达的成功语义 |
| Journal path escape | 1 个 Python 测试失败，错误返回 0 | 篡改 journal 的 `../` move path 可以把目录移出 workspace；该 Critical 已用统一 confinement 修复 |
| Rename/journal crash window | 1 个 Python 测试失败 | rename 完成但 completion record 尚未写入时，新进程无法恢复；现按 source/target 实际状态恢复 |
| Whole-directory hash coverage | 1 个 Python 测试失败 | 大于 2 MiB 的 feature payload 未进入 snapshots；现仅 Markdown reference scan 保留 2 MiB 限制 |
| BOM/CRLF preservation | 1 个 Python 测试失败 | 引用更新会移除 UTF-8 BOM 并规范化换行；现逐字节保留编码标记和 CRLF |
| Broken relative link | 1 个 Python 测试失败 | 不存在的跨边界相对链接仍会被重写；现分类为 `unsupported` 并阻断 apply |
| Journal scope tampering | 1 个 Python 测试错误返回 0，并删除不在原计划内的 `README.md` | 外层 journal 与内嵌 plan 被一起篡改并重算自哈希时，`missing-before` 可越权；现要求 reference-edit 哈希链从原 snapshots 起步，并在任何目录移动前校验 backup bytes |
| Post-crash human drift | 1 个 Python 测试错误返回 0 | restore 会覆盖进程中断后的人类修改；现对 source/target 实际位置和全部当前字节做 preflight，发现 drift 后保留 journal 并停止 |
| Stranded transaction bypass | 2 个 Python 测试错误返回 0 | 已存在 `.archive-txn/<id>` 时仍可生成新 plan 或开始 apply；现 scan 与 apply 都要求先按显式 transaction ID 恢复 |
| Inbound relative link blind spot | 2 个 Python 测试失败 | `.agent-loop/project.md` 中 `features/<id>/spec.md` 这类指向待移动 feature 的相对链接未进入 plan，apply 后可留下 broken link；现双向计算跨移动边界的链接目标 |

这些 RED 都发生在对应实现或 authority 更新之前；没有通过弱化断言把失败改成 GREEN。

## 3. GREEN 证据

执行命令：

```text
python3 -m unittest \
  tests.test_python_checker_contract \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply \
  tests.test_feature_monthly_archive_restore \
  tests.test_adr_requirement_model_trace -v
```

Task 6 首次运行结果为 `Ran 64 tests`，`OK`。首轮 Standards Review 后为 `Ran 72 tests`，`OK`；本轮 Human Review 针对四个问题补强 7 条回归并完成修复后，最终为 `Ran 79 tests`，`OK`。

执行命令：

```text
bash tests/validate-feature-monthly-archive-runtime.sh
bash tests/validate-feature-monthly-compaction-proposal.sh
```

结果：2/2 PASS。

## 4. 逻辑与压力场景

### Eligibility 与阻断

- 两个月 fixture 中，`2026-05-08-login` 与 `2026-06-12-payment` eligible；同批 `2026-05-22-import` 为 paused，保留在 flat path。
- active、blocked、paused、current-month、incomplete close、缺少 Archive Readiness、非终态 readiness、placeholder summary、open follow-up、project memory active/paused 均被阻断。
- flat/month collision、symlink escape、大于 2 MiB 且含旧路径的 Markdown、不确定旧路径引用均 fail closed。
- 原始 requirement source 被分类为 `immutable-requirement-source`，不被重写；历史报告只作为可见 preserved evidence。

### Read-only 与哈希证据

- `scan`、pre-check、post-check、current-month blocker、collision 与 stale-plan 场景都在操作前后比较完整文件树 SHA-256 map；结果完全相等，没有新增、删除或字节漂移。
- deterministic plan 测试在两个不同绝对根目录生成相同 canonical JSON SHA-256，绝对路径不进入 plan hash。
- valid-but-different `expected-plan-sha256` 与 scan 后状态漂移均以 `stale-plan` 拒绝，且完整 SHA-256 map 保持不变；状态漂移拒绝时不会创建 transaction journal。

### Apply、恢复与 rehydrate

- 两个 closed Feature 被整目录移动到各自月份；移动前后的完整文件 SHA-256 map 相同，binary payload 字节保持不变，archive locator 按 Feature ID 排序。
- 只执行 plan 中预计算的 project、requirement README 与 ADR 引用更新；人类原始 requirement source 和无关 Markdown 字节保持不变。
- 重复 apply 不创建 `YYYY-MM/YYYY-MM/<feature-id>`，无 move 的重复计划保持幂等。
- test-only 注入引用写失败后，目录、引用和 locator 由 transaction journal 恢复到完整的事前 SHA-256 map；非 test mode 使用注入变量会被拒绝。
- 新进程可以从显式 transaction ID 恢复中断事务；发生源路径碰撞时 fail closed，并保留 `restoring` journal 供人工处理。
- restore 在任何 feature move 或引用回写前校验 journal/plan/snapshot scope、reference-edit 哈希链、备份字节和当前工作区字节；整体篡改 journal、损坏 backup 或崩溃后出现人类修改时都不会覆盖项目内容。
- 任一 stranded `.archive-txn/<id>` 会同时阻断新 scan 和 apply；项目记忆中指向待移动 feature 的相对 Markdown link 会进入确定性 plan 并随 apply 更新。
- rehydrate 把完整目录移回 flat path，将 locator 标记为 `rehydrated`，但 `spec.md` 仍保持 `closed`；后续 reopen 仍需独立 Feature Follow-up Human Gate。

## 5. 平台证据

| 平台 | 状态 | 证据 |
|---|---|---|
| macOS | verified | Python 3.10+ 本地 79/79 focused tests 与 2/2 shell contracts 通过 |
| Windows | test-defined | GitHub Actions 保留 `windows-latest` × Python `3.10`/`3.x`，已加入四个模块和四个 CLI `--help`；本轮没有取得成功 run |

实现只使用 Python 3.10+ 标准库。文档同时给出 macOS `python3` 与 Windows PowerShell `py -3` 调用方式。

## 6. 严重度审计

| 严重度 | 数量 | 结论 |
|---|---:|---|
| Critical | 0 | 未发现删除历史内容、绕过 Human Gate、跳过 expected hash 或越界写入能力 |
| High | 0 | 未发现 stale-plan、恢复、locator 或 lifecycle/archive-state 混淆缺口 |
| Medium | 1 | Windows workflow 已定义但未取得实际成功 run；因此不能完成跨平台验收 |

专项评分：96/100。扣分仅来自 Windows 远程执行证据缺失，不将“测试已定义”冒充“跨平台已通过”。

## 7. 明确排除范围

- 不创建 per-feature archive summary 或 per-month index；
- 不创建 `historical/`、Deep Archive、Summary Only；
- 不删除、打包、压缩、外移或替代历史 feature 内容；
- 不自动定时归档，不自动归档当前月；
- 不移动 active、blocked、paused 或证据不完整的 feature；
- 不改写原始人类需求文件或 accepted ADR 产品语义；
- 不提供 `--force`；
- 不在技能源码仓库创建真实目标项目 `.agent-loop/features/`。

## 8. 授权与边界

本报告只覆盖实现与 focused validation。commit、push、tag、PR、merge、release、publish 均未获得本轮授权，也未执行。工作区原有 onboarding proposal 修改、v1.4 proposal 删除与 `docs/proposal/v2.0.x/` 内容不属于本功能，没有被恢复、覆盖、暂存或纳入本报告结论。
