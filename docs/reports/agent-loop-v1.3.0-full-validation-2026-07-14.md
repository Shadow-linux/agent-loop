# Agent Loop v1.3.0 发布前全量验证报告

验证日期：2026-07-14
验证分支：`codex/v1.3.0-pre-release-validation`
版本：`1.3.0`
审计对象：v1.3.0 release candidate，行为基线 commit `7253461`，以及隔离 worktree 中仅用于刷新发布证据的文档/contract 变更
比较基线：`stable-v1.2.4`（`a3c8408`）
平台状态：`macOS-verified / Windows-verified`
远端 CI：<https://github.com/Shadow-linux/agent-loop/actions/runs/29320389912>

## 1. 发布判断

总分：**99/100**
等级：**STRONG**
最终测试：**98/98 Python tests PASS；34/34 `tests/*.sh` PASS**
当前严重度：**Critical 0 / High 0 / Medium 0 / Low 0**

v1.3.0 的累计行为已经形成一致、可执行、可恢复的闭环，并已通过正式 Release Human Gate。发布范围包括：Onboarding Core Flow Completeness、Concept Foundation / Requirement Product Model、ADR Requirement Model Technical Landing、Cross-Platform Python Script Runtime、Feature Monthly Archive。

Release Human Gate：**已批准**。授权动作：提交并推送 release-evidence commit、推进两个 `v1.3.0` branch、创建并推送 `stable-v1.3.0` tag。为保证 tag 与验证证据绑定，只有精确 release-evidence commit 的 Windows/macOS CI 全部成功后才执行 branch/tag 发布。

## 2. 版本范围与提交边界

`stable-v1.2.4..7253461` 共五个行为提交：

| Commit | 能力 | 发布前结论 |
|---|---|---|
| `27f4f18` | Onboarding Core Flow Completeness | Critical flow、slice、terminal、recovery、diagram/evidence trace 完整；仍保持两个 Onboarding Human Gates |
| `e43f745` | Concept Foundation / Requirement Product Model | 复杂需求先固化 Concept IDs，再推导 flow/state/product facts；简单需求有 reasoned not-needed 分支 |
| `81b55c7` | ADR Requirement Model Technical Landing | accepted product meaning 全量进入 scope inventory、landing trace、Design Slice 和 verification；ADR 不重定义 PRD 语义 |
| `e49673c` | Cross-Platform Python Script Runtime | 四个 canonical checker 使用 Python 3.10+ 标准库；旧 Bash/Ruby 入口仅兼容一周期 |
| `7253461` | Feature Monthly Archive | 只读 scan、确定性 plan、Human Gate、事务 apply/post-check/restore、rehydrate 和 locator 闭环 |

发布证据刷新不改变 runtime、stage order、Human Gate、artifact schema 或 feature behavior。

## 3. 六域语义审计

| 审计域 | 结果 | 分数 | 已通过的不变量 |
|---|---|---:|---|
| Logic Correctness | PASS | 99 | first-match precedence 唯一；Concept/Requirement/ADR/Feature 所有权不冲突；archive state 不混入 lifecycle；无 Gate 绕过 |
| Autonomy | PASS | 99 | Agent 负责调查、分类和唯一下一阶段；blocked matrix 可执行；helper fallback 不接管 task/memory/gate authority |
| Project Entry / Onboarding | PASS | 99 | remote-entry 优先；stale memory 先恢复；Onboarding 仍只有 Spec Acceptance 与 Tasks Full Execution 两个 Human Gates |
| Development / Test Workflow | PASS | 99 | Plan Gate、Analyze Consistency、TDD、Verify、Review、Drift、Task Done、Completion 和 Follow-up 顺序闭合 |
| Memory | PASS | 99 | 单 Active Feature、Delivery Phase roll-up、Effective Concept pointer、ADR compatibility、archive locator 与 code-reality-wins 一致 |
| Recommendation | PASS | 99 | Chat 不创建产物；阻塞只推荐一个 unblock stage；Submit/Close/Release/Publish 分别保留 Human Gate |

加权结果为 99。没有未解释的 Critical、High 或 Medium。

## 4. RED 基线

### 4.1 可执行与机械基线

在干净 worktree、精确 HEAD `7253461` 上先运行既有验证：

- `python3 -m unittest discover -s tests -p 'test_*.py' -v`：98/98 PASS；
- `for test_file in tests/*.sh; do bash "$test_file"; done`：33/33 PASS；
- YAML、JSON、Python compile、Shell/Ruby syntax、Markdown fence、`git diff --check`：PASS。

因此本轮没有把既有失败混入 release 修复。

### 4.2 发布证据状态 RED

语义审计发现一个 Medium 级发布证据漂移，不是 runtime 逻辑缺陷：代码、commit/push 和 Windows/macOS CI 已完成，但五组 Proposal、Archive 实施计划和 7 月 14 日报告仍声明 `Windows-test-defined`、未 commit/push 或等待旧 Human Review。

新增 `tests/validate-v1.3.0-release-readiness.sh`，并先更新 Archive proposal contract 的期望状态。修复前两个 contract 都真实退出 1：

```text
FAIL: docs/proposal/v1.3.x/onboarding-core-flow-completeness.md missing release evidence: 状态：已实现并通过发布前全量验证；待 v1.3.0 Release Human Gate
FAIL: feature monthly archive proposal missing required text: 状态：已实现并通过发布前全量验证；待 v1.3.0 Release Human Gate
release-evidence exit=1 archive-proposal exit=1
```

该 RED 证明最终 GREEN 不是通过保留旧状态或弱化断言获得。

## 5. GREEN 结果

发布证据修复包括：

- 五组 v1.3.0 Proposal 统一进入 `待 v1.3.0 Release Human Gate`；
- Cross-Platform Runtime 与 Feature Monthly Archive 记录具体 commit `7253461` 和 workflow run `29320389912`；
- Archive 实施计划记录 implementation/review/commit/push 已完成，同时保留 tag/release/publish 未授权；
- Archive focused report 更新为 Windows/macOS verified；
- 本报告从单一 Archive 审计扩展为 `stable-v1.2.4..7253461` 的累计 release-candidate 审计；
- 新增持久 release-evidence contract，防止同一版本再次退回旧发布状态。

最终复跑结果：

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
Ran 98 tests
OK

for test_file in tests/*.sh; do bash "$test_file"; done
34/34 PASS
```

## 6. 关键压力场景

### Requirement、Product 与 ADR

- 复杂 Requirement：Concept Foundation accepted 后才能推导 Requirement Product Model；Design Readiness 触发 Decision & Design；每个 accepted model ID 必须有 scope/landing/Design Slice/verification disposition。
- 简单 Requirement：使用有具体理由的 `concept-foundation-not-needed`，不伪造概念、状态机或 ADR。
- Product Brief / Feature Spec：必须引用有效 requirement source 或明确 feature-start evidence，不重新定义 accepted Concept/Product Model。
- accepted ADR 与上游或实现 drift：进入 compatibility review / Decision Scan / Drift Check；旧 accepted ADR 被 supersede，不原地改写。

### Human Gate、执行与完成

- Delivery Contract：不是默认产物；创建、接受和 breaking change 都必须单独 Human Gate。
- 行为变更：不能因人类催促跳过 TDD RED；非行为工作只允许带理由的 `not-applicable`。
- Task 完成：测试通过或 review approval 单独都不能标记 `done`；必须满足 evidence、review、drift 和 Task Done Gate。
- Submit / Release：`commit this`、`publish release` 只进入 Submit / Integrate 检查；真正 commit、tag、release、publish 仍需后续明确确认。

### 状态、记忆与恢复

- 同一时间只允许一个 Active Feature；新 feature 前必须 close 或 pause 当前 feature并记录 resume point。
- 多 Delivery Phase：一部分实现时 requirement 只能是 `partially-implemented`，不能由单个 feature 错误关闭整体。
- stale-memory / outside-loop：先 Reconcile / Recovery，code reality 是 agent-maintained facts 的当前基线，human requirement source 保持不可变。
- Feature Follow-up：先 investigate owner；archived owner 必须先独立 rehydrate Gate，再决定 `closed -> active`。

### Feature Monthly Archive

- stale plan、flat/month collision、symlink/path escape、broken/ambiguous reference、stranded transaction 全部 fail closed；
- journal scope、backup bytes、post-crash human edits在任何恢复写入前校验；
- scan/check 只读，apply 只执行 Human-reviewed SHA-256 plan；
- 归档只移动完整目录并维护 locator，不删除、压缩、summary-only 或创建 `historical/`。

### Project Entry 与 Onboarding

- remote-entry 在 existing-project 之前；普通 Chat 不创建 requirement/feature/onboarding 产物；
- Project Entry 只建立安全接管记忆，不偷跑 Evidence-Graph onboarding；
- Critical/Important flow 缺 slice、terminal、recovery 或 detached diagram 时 Completeness Hard Gate 失败；
- Completeness 是 Agent quality gate，不增加第三个 Onboarding Human Gate。

## 7. 关键跨文件不变量

- `SKILL.md` 保持简洁 controller；`references/design.md` 与 `references/runtime.md` 分别拥有模型/约束和可执行路由。
- root `templates/root-AGENTS.md` 只做导航；13 个 managed block 均为 `1.3.0-20260714.1`。
- runtime 与 root Stage Map 的 first-match 顺序一致：Safety Stop -> Remote Discovery -> Memory Recovery -> Feature Archive Maintenance -> Active Feature Guard -> Blocker Resolution -> Intent Routing -> Normal Stage Continuation。
- Requirement 拥有产品目标/语义；ADR 是可选技术落地桥梁；Feature Spec 消费已接受输入。
- Delivery Contract、Task Done、Submit、Close、Release、Publish 和 Tag Gate 没有被 Auto Mode、external skill 或 subagent 绕过。
- `features/archive.md` 只是 locator/ledger，不替代 requirement、ADR、feature artifacts 或 lifecycle authority。

## 8. 版本、平台与机械证据

版本同步：

- `SKILL.md`: `Version: 1.3.0`；
- `plugin.json`: `1.3.0`；
- `README.md`: Current version `1.3.0`；
- `Usage.md`: `1.3.0`；
- `CHANGELOG.md`: `1.3.0` section；
- `templates/root-AGENTS.md`: 13/13 managed blocks 使用 `1.3.0-20260714.1`。

跨平台 CI：

| Job | 结果 |
|---|---|
| `windows-latest / Python 3.10` | success |
| `windows-latest / Python 3.x` | success |
| `macos-latest / Python 3.10` | success |
| `macos-latest / Python 3.x` | success |

四个 job 都属于 commit `7253461` 的 run `29320389912`。

机械检查：

| 检查 | 结果 |
|---|---|
| `SKILL.md` + repository YAML parse | PASS（2 YAML files） |
| repository JSON parse | PASS（1 file） |
| `python3 -m compileall -q scripts tests` | PASS |
| Shell `bash -n` | PASS（35 files） |
| Ruby `ruby -c` | PASS（5 files） |
| Markdown fence balance | PASS（199 files） |
| `git diff --check` | PASS |

## 9. Review 与未采纳意见

主 Agent 逐项完成 Spec/Standards Review、六域交叉取证和 release diff 审计。当前协作约束未授权 reviewer subagent，因此没有把主 Agent review 冒充独立 reviewer 证据；这一限制不构成 runtime 缺陷。

未采纳：

- 不新增 canonical stage、Human Gate、Delivery Contract 默认产物或 executable schema；
- 不为发布证据更新修改 skill version 或 root block revision；
- 不把历史 `.1` 等报告改写成当前权威；其中已标记 superseded 的报告继续保留 RED/审查历史；
- 不在发布前验证中创建 tag、GitHub/GitLab Release 或执行 publish。

## 10. 工作区隔离与授权

验证 worktree：`/Users/shaodowyd/.config/superpowers/worktrees/agent-loop/v1.3.0-pre-release-validation`

主工作区原有以下无关改动未被读取为发布内容、未被复制、暂存或修改：

- `docs/proposal/v1.3.x/onboarding-core-flow-completeness.md` 的主工作区未提交版本；
- 删除中的两个 v1.4 proposal；
- `docs/proposal/v2.0.x/`。

行为提交 `7253461` 已推送到两个经授权远端的 `alpha/v1.3.0`。两个远端的 `v1.3.0` branch 在审计开始时也指向 `7253461`。本轮 release-evidence 变更尚未 commit 或 push。

## 11. 下一阶段

当前推荐下一阶段：**执行已批准的 v1.3.0 正式发布**。

顺序固定为：提交 release-evidence commit；推送到两个 `alpha/v1.3.0`；等待该精确 commit 的 Windows/macOS CI；CI 全绿后推进两个 `v1.3.0` branch，并创建、推送 `stable-v1.3.0` tag。任何 CI 失败都必须停止 branch/tag 发布。
