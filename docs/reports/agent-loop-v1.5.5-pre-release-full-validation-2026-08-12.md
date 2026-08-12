# Agent Loop v1.5.5 发布前全量验证报告

## 审计对象与边界

| 项目 | 结果 |
|---|---|
| 日期 / 平台 | 2026-08-12；macOS live validation |
| 分支 | `v1.5.5` |
| 基线 HEAD | `f9c5569d93f6e42457b12fa2925a95373bea0cb9` |
| 审计对象 | 当前未提交工作区：v1.5.5 Repair-First 实现与发布前跨路径审计修复 |
| RED 证据 | `docs/reports/agent-loop-v1.5.5-pre-release-red-baseline-2026-08-12.md` |
| root managed revision | `1.5.5-20260812.2`，13/13 blocks，177 行 |

本轮保持 Agent Loop Skill 源码仓库维护者视角，没有创建目标项目 `.agent-loop/`。已知 `.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/` 被保留。报告完成后的定向复核又发现 2 个当前 High、1 个 legacy High、1 个测试覆盖 Medium 和 1 个报告 Low；人类已明确决定不在本版修复并授权发布。

## 总结论

**定向复核后的真实结论：`89.25/100 — STABLE WITH ACCEPTED RISKS`。**

当前 finding 为 `Critical=0`、`High=3`、`Medium=1`、`Low=1`。High 分别是普通业务目录 `agent-loop/` 被误判为 memory root、legacy Project Skill 创建 `.agent-loop/skills/` 后产生 dual root，以及 Post-Merge 主序列遗漏 Tag/Publish/Seal；Medium 是组合回归未覆盖这些矛盾；Low 是本报告原先把 `97.05` 误写为 `97.20`。这些 finding 均已向人类披露；人类明确决定先不修并以当前状态发布 v1.5.5，因此这是 accepted-risk release，而不是零风险发布。

## 六域评分

| 审计域 | 权重 | 结果 | 域分 | 加权分 | 结论 |
|---|---:|---|---:|---:|---|
| Logic Correctness | 20% | PASS WITH ACCEPTED RISK | 90 | 18.00 | closed Bug 顺序已修；但 Post-Merge 的 executable summary 仍遗漏 Tag/Publish/Seal。 |
| Autonomy | 15% | PASS | 99 | 14.85 | Agent 可在既有授权内 Repair-First、做自主验证与建议；只在真实 owner/Gate 阻塞时停下。 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | PASS WITH ACCEPTED RISK | 70 | 10.50 | 名为 `agent-loop/` 的普通业务目录可被误认成 legacy memory；legacy Project Skill 也可制造 dual root。 |
| Development / Test Workflow | 20% | PASS | 99 | 19.80 | 初始 Feature/显式 Bug TDD、Review/Lightweight Repair-First、Task Done、Review/Drift/Memory 均通过回归。 |
| Memory | 15% | PASS WITH ACCEPTED RISK | 82 | 12.30 | Archive/restore 正常，但 Post-Merge 摘要和 memory reference 未完整投影五个独立 release actions。 |
| Recommendation | 15% | PASS WITH ACCEPTED RISK | 92 | 13.80 | Human Review 表本身逐行授权正确；另有运行摘要可能跳过未列出的 Gate。 |
| **总计** | **100%** | **HUMAN-ACCEPTED RELEASE RISK** |  | **89.25** | **STABLE** |

## 定向复核新增的未解决 Findings

### High：普通 `agent-loop/` 业务目录被误判为 legacy memory

`scripts/checker_support.py` 只按顶层名称存在判断 `.agent-loop/` / `agent-loop/`，不检查后者是否包含 Agent Loop memory。临时 fixture 证明：只有普通 `agent-loop/src/` 时会被当作 legacy root；真实 `.agent-loop/` 加普通 `agent-loop/src/` 时会误报 dual root。该问题影响默认路径，不是 legacy-only。

### High：legacy Project Skill 创建可制造 dual root

legacy `agent-loop/` 可作为 accepted root，但 Project Skill 固定写入 `.agent-loop/skills/`；Gate 1 后会同时出现两个根，并在下一次入口先于 Discovery/Execution Gate 进入 Recovery。人类仍决定本版不修。

### High：Post-Merge 主序列遗漏 Tag / Publish / Seal

`references/submit-and-integrate.md` 已有完整 `Tag -> Push -> Release -> Publish -> Seal` owning sequence，但 `references/runtime.md`、`references/design.md` 和 `references/memory-reconciliation.md` 的摘要仍保留旧链，只列 Push/Release。现有 post-merge focused test 也只保护旧链，因此 Tag 失败或 Seal 未批准的组合没有得到完整 executable-order 保护。

### Medium：组合回归缺失

现有测试分别保护路径命名、dual-root fail-closed 和独立 Gate 关键词，却没有覆盖普通业务 `agent-loop/`、legacy Project Skill 创建后的下一次入口，以及完整五 Gate 的失败前置顺序。

### Low：原评分算术错误

原表域分加权应为 `97.05` 而非 `97.20`，且 Autonomy 行缺一个加权分单元格。定向复核后已重新评分为 `89.25`。

## 已解决的发布前 Findings

### Critical：Bug Reopen Gate 顺序

旧规则可能在 Human Gate 前把 matched closed Bug 改回活动状态。当前顺序为：

```text
matched closed Bug remains closed
-> prepare named reopen candidate without lifecycle write
-> Bug Reopen Gate
-> after acceptance append Reopen Record and restore unresolved
-> new Resolution Path recommendation and Gate
```

证据：`references/runtime.md:70`、`references/stage-guides.md:806`、`references/bug-management.md`、`references/workflow-checklists.md`、`tests/validate-bug-management.sh`。

### High：合并的 Release Gate

旧 `Release Gate` 同时表达 tag、push、release、publish 和 sealed transition，可能让一个决定被复用到多个外部动作。当前拥有面明确区分：

- `Tag Gate`：精确 tag + 精确 commit；
- `Push Gate`：精确 refs + 精确 remote；
- `Release Gate`：精确 version 的 release record；
- `Publish Gate`：精确 artifact + channel/destination；
- `Seal Gate`：精确 version 的 `released / sealed` transition。

一张 Batch Human Review 可以展示这些行，但一行的授权不能供应另一行；前置动作失败会停止依赖行。证据：`references/branch-management.md:336`、`references/runtime.md:265`、`references/submit-and-integrate.md:97`、`references/human-review-summary.md:456`、`templates/root-AGENTS.md:129`、`tests/validate-branch-management-strategy.sh`。

### Low：Archive 测试名称与行为相反

只把测试名改为 `test_ambiguous_old_path_reference_is_reported_as_advisory`，与当前“Scanner 报告事实、Agent 判断”的轻 Gate 语义一致。Scanner、Apply、plan hash、transaction journal 和 rollback 行为未改变。证据：`tests/test_feature_monthly_archive_scan.py:739`。

### 同步修正：Lightweight stale assertion

一个 Lightweight contract 仍期待 Gate 前 create/update/reopen closed Bug 的旧句子。它已改为当前 gate-correct 顺序；这只是回归期望同步，不改变 Lightweight 路由。

## RED -> GREEN

真实 RED 包括：

```text
FAIL: references/runtime.md does not keep a matched closed Bug unchanged until the Bug Reopen Gate
FAIL: references/branch-management.md missing branch-management contract: | Tag Gate | creation of one exact tag at one exact commit |
FAIL: references/human-review-summary.md missing branch-management contract: | Tag Gate / Tag | exact tag + exact commit |
FAIL: references/branch-management.md missing branch-management contract: Recommendation and adoption do not authorize branch creation, switching, merge, deletion, push, tag, release, publish, or seal.
FAIL: references/design.md missing Lightweight Change contract: For explicit Bug management, create/update/reopen the Bug Record, verify Expected Behavior, and recommend exactly one Resolution Path.
```

修复后同一 focused contracts：

- `tests/validate-bug-management.sh`：PASS；
- `tests/validate-branch-management-strategy.sh`：PASS；
- `tests/validate-lightweight-change-lane.sh`：PASS，内嵌 Python 37/37；
- `tests/validate-feature-construction-two-gate-review.sh`：PASS；
- `tests/validate-repair-first-verification.sh`：PASS；
- `tests/test_feature_monthly_archive_scan.py`：28/28；
- `tests/test_feature_review.py` + root lossless：22/22。

## 全量执行结果

最终 live recount：

```text
tests/*.sh: 50/50 PASS
python3 -m unittest discover -s tests -p 'test_*.py' -v: 416/416 PASS
Python wall time: 91.401s
```

无失败后重试或测试放宽。最初从仓库根运行没有指定 `-s tests` 的 discovery 发现 0 tests（exit 5），因此没有把它计入测试结果；随后使用仓库真实测试目录执行并得到上述 416/416。

机械检查：

| 检查 | 结果 |
|---|---|
| `SKILL.md` + `agents/openai.yaml` YAML | 2/2 PASS |
| JSON parse | 3/3 PASS |
| Shell syntax | 51/51 PASS |
| Python AST | 48/48 PASS |
| Ruby syntax | 5/5 PASS |
| Markdown fence | 343/343 PASS |
| `git diff --check` | PASS |
| untracked text whitespace | 7/7 PASS |
| root template | 177 行；13/13 blocks；`.2` revision 13/13；当前权威 `.1` 为 0 |

## 代表性压力路径

| 路径 | 结果 |
|---|---|
| Standard Product Definition -> ADR -> Feature Product Slice | PASS；产品语义、技术落地与 Feature ownership 未被发布前修复改写。 |
| Brief Product Definition -> Feature Product Slice | PASS；无需 ADR 的简单路径仍可达。 |
| initial Feature / explicit Bug | PASS；TDD 仍必需，Bug reopen 不越过独立 Gate。 |
| Review repair / Lightweight | PASS；Repair-First 不替代 Required Verification 或 Existing Test Obligation。 |
| Active Feature / Pause / Resume / Close / Reopen | PASS；生命周期与项目记忆同步。 |
| Archive/Rehydrate | PASS；ambiguous reference 是 advisory，exact plan/apply 物理边界仍保留。 |
| Branch/release batch | Human Review 表逐行授权正确；Post-Merge 摘要的完整顺序风险已披露并由人类接受。 |
| Post-Merge Memory Reconciliation | conflict/no-conflict 行为与 restore 正常；Tag/Publish/Seal 摘要遗漏作为 accepted High 保留。 |
| ordinary Chat | PASS；不创建 Requirement、Feature、Bug 或 Change artifact。 |

## 保持的跨文件不变量

- 未新增 canonical stage、message intent、artifact tree 或 Checker outcome。
- `Seal Gate` 是把已经存在的 sealed transition 从错误的合并 Release 授权中分离，不改变版本 lifecycle 状态集合。
- Product Human Review、Requirement、ADR、Delivery Contract、Feature Gate 1/2、Task Done、Project Skill、Subagent、Archive/Rehydrate、Bug Resolution/Close/Reopen、Submit、Commit、PR、Merge、Tag、Push、Release、Publish、Seal、Pause 和 Feature Close 均保持独立 Human Gate。
- root `AGENTS.md` 仍为 177 行、13 个 First-Hop managed blocks，不承载完整 leaf-stage 流程。
- 当前版本已获准作为 `1.5.5` 正式稳定版发布，稳定 tag 为 `stable-v1.5.5`；`main` 同步仍是独立 Human Gate。

## 未解决问题与人类决定

### High（legacy-only，已接受延后）：Project Skill 双 root

`references/design.md:17` 仍允许读取 legacy `agent-loop/` 并在确认后迁移，同时规定双 root fail-closed；`references/project-skills.md:92` 固定把 Project Skill 写到 `.agent-loop/skills/`。如果一个仍以 legacy root 工作的项目直接创建 Project Skill，可能同时出现 `agent-loop/` 与 `.agent-loop/`，下次入口会进入 Recovery。

人类决定：本版不修。该风险本身仍是 legacy-only；但另一个普通业务目录 `agent-loop/` 名称碰撞 High 会影响默认 `.agent-loop/` 路径，已在上文单独披露。若未来继续承诺 legacy Project Skill 创建兼容，应另建变更迁移或移除该兼容声明。

其他当前未解决 finding 已在“定向复核新增的未解决 Findings”列出。Windows 为 `test-defined`，未进行 live Windows host 验证。

## 范围与发布判断

本轮没有实现 Bug Management 新阶段、Memory Merge、worktree、目标项目 artifact 或新 Checker。Bug 修复属于状态/Gate 顺序修正；Branch 修复属于已有人类动作授权拆分；Archive 仅修改误导性测试名。

结论：技术建议原本应 HOLD 并先修两个默认/执行顺序 High；人类在阅读汇总后明确决定“先不修，就这样发布”。因此 v1.5.5 按 Human-accepted risk 发布。这一决定不表示 finding 已关闭，也不得作为后续版本忽略它们的证据。

## Git 动作声明

人类已授权本报告所对应的 release commit、`v1.5.5` branch push 与 `stable-v1.5.5` tag 发布。PR、merge、`main` 同步、installed Skill 同步和其他发布动作不在本次授权内。
