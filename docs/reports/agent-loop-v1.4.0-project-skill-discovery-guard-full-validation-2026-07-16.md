# Agent Loop v1.4.0 Project Skill Discovery Guard 全量验证报告

## 1. 验证摘要

| 项目 | 结果 |
|---|---|
| 日期 | 2026-07-16 |
| 分支 | `alpha/v1.4.0` |
| 基线提交 | `c0221694734b25e053efb4b490c7efdd5468a203` |
| 审计对象 | 当前未提交工作区 |
| Skill 版本 | `1.4.0`，未修改 |
| focused RED | PASS：修复前按预期失败并保存证据 |
| focused GREEN | PASS |
| 全部 shell tests | `37/37 PASS`，实时重新统计 |
| Python root checker unit tests | `8/8 PASS` |
| 机械检查 | YAML / JSON / Shell / Ruby / Markdown fence / diff 全部 PASS |
| Critical / High / Medium | `0 / 0 / 0` |
| 总分 | `98.5 / 100` |
| 等级 | `STRONG` |
| Git / 发布动作 | 未 commit、未 push、未 tag、未 PR、未 merge、未 release、未 publish、未同步安装副本 |

结论：Project Skill Discovery Guard 已在 Agent Loop 源码权威、下游运行 reference、root bootstrap、人类文档、压力场景和回归测试中协调落地。当前工作区满足 Proposal 的实现与验证条件，可以进入 Human Review；该结论不构成 Submit / Integrate、发布或安装同步授权。

## 2. 范围与工作区保护

### 2.1 维护视角

本轮始终维护 Agent Loop Skill source repository，没有在源码仓库创建目标项目 `.agent-loop/skills/` 或其他目标项目 artifact。

### 2.2 无关 dirty work

人类已有未跟踪文件：

```text
docs/proposal/v1.4.x/post-merge-memory-reconciliation.md
```

Task 0 与 focused/full validation 后 SHA-256 均为：

```text
612df36b0c3b2954cd1ba0d02ab19ca1ba967cf4361720b585079bd867bb8b7e
```

该文件未被修改、覆盖、恢复、暂存或提交。

### 2.3 明确未进入的范围

- 没有新增 canonical stage 或 message intent；
- 没有新增 Project Skill lifecycle status；
- 没有新增 discovery cache、数据库、守护进程或 executable schema；
- 没有全局安装、兼容复制或原生 Skill chip 集成；
- 没有削弱 Gate 1、Execution Gate 或其他 Human Gate；
- 没有修改 `plugin.json` 或 Skill 版本；
- 没有派发 subagent；
- 没有创建 branch/worktree/tag/PR/release。

## 3. 实际修改文件

### 3.1 新增

- `docs/proposal/v1.4.x/project-skill-discovery-guard.md`
- `docs/proposal/v1.4.x/project-skill-discovery-guard-implementation-plan.md`
- `tests/validate-project-skill-discovery-guard.sh`
- `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-red-baseline-2026-07-16.md`
- `docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-full-validation-2026-07-16.md`

### 3.2 核心权威

- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
- `references/project-skills.md`

### 3.3 派生 workflow 与人类 surface

- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/project-guidance.md`
- `templates/root-AGENTS.md`
- `references/validation-scenarios.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

### 3.4 root revision 耦合回归

- `tests/test_root_agents_blocks.py`
- `tests/validate-branch-management-strategy.sh`
- `tests/validate-bug-management.sh`
- `tests/validate-project-local-skills.sh`
- `tests/validate-requirement-lifecycle-backlog.sh`
- `tests/validate-root-agents-block-checker.sh`
- `tests/validate-root-agents-block-refresh.sh`
- `tests/validate-v1.2.4-root-stage-coverage.sh`

## 4. RED 基线

修复前先确认既有机械基线：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
```

结果：修改前已有 `36/36` shell tests PASS，YAML、Shell syntax 和 diff PASS。

随后新增 focused contract，但尚未修改运行规则：

```bash
bash tests/validate-project-skill-discovery-guard.sh
```

实际退出码：`1`。

```text
FAIL: SKILL.md missing required text: Project Skill Discovery Guard
```

该失败证明：测试脚本本身可以正常执行，并在第一个缺失的 controller contract 上失败。完整证据见：

`docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-red-baseline-2026-07-16.md`

## 5. GREEN 结果

实现协调规则、root reminder、人类文档和压力场景后执行：

```bash
bash tests/validate-project-skill-discovery-guard.sh
```

实际结果：

```text
PASS: Project Skill Discovery Guard ordering, fallback, drift, root, and gate contract is complete
```

该 contract 不只检查关键词：

- 从 runtime 的 `Project Skill Discovery Guard` section 提取 canonical flow；
- 验证 INDEX inspect → active match → row/path/manifest verification → read-only load → Execution Gate → stage action 的顺序；
- 验证只有 `index-absent | no-active-match` 允许 fallback；
- 验证 `project-skill-drift` fail closed；
- 验证 design/project-skills 拥有同一核心 contract；
- 验证 root reminder 精确短句只出现一次且不包含详细 result vocabulary；
- 验证 13 个 root managed blocks 全部使用 `1.4.0-20260716`；
- 验证十个压力场景存在；
- 验证源码仓库没有 `.agent-loop/skills/`。

## 6. Focused Validation

执行命令：

```bash
bash tests/validate-project-skill-discovery-guard.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-operational-support-guard.sh
bash tests/validate-mandatory-helper-routing.sh
bash tests/validate-skill-reentry-guidance.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-branch-management-strategy.sh
bash tests/validate-bug-management.sh
bash tests/validate-human-help-version-docs.sh
python3 -m unittest tests.test_root_agents_blocks
```

结果：全部退出码为 0；Python root checker unit tests 为 `8/8 PASS`。

覆盖边界：

- Project-Local Skills lifecycle、manifest、Execution Gate；
- Code-Guided Operational Support；
- mandatory helper routing；
- controller bootstrap/re-entry；
- root block checker / refresh / stage coverage；
- Requirement、Branch、Bug 等共享 root revision contract；
- 人类帮助与版本文档。

## 7. Full Validation

### 7.1 全部 shell tests

实时统计与执行：

```bash
test_count=$(find tests -maxdepth 1 -type f -name '*.sh' | wc -l | tr -d ' ')
passed=0
for test_file in tests/*.sh; do
  bash "$test_file"
  passed=$((passed + 1))
done
printf 'shell tests passed: %s/%s\n' "$passed" "$test_count"
```

实际结果：

```text
shell test count: 37
shell tests passed: 37/37
```

没有沿用旧报告中的测试数量。

### 7.2 机械检查

| 检查 | 命令摘要 | 结果 |
|---|---|---|
| SKILL YAML | Ruby YAML load | PASS |
| JSON | Ruby JSON parse all `*.json` | PASS |
| Shell syntax | `bash -n` all `*.sh` | PASS |
| Ruby syntax | `ruby -c` all `*.rb` | PASS |
| Markdown fence | all Markdown fence balance scan | PASS |
| Tracked diff whitespace | `git diff --check` | PASS |
| 新增未跟踪文件 whitespace | `rg '[[:blank:]]+$'` negative check | PASS |
| Source artifact boundary | `.agent-loop/skills` absence | PASS |

Python tests生成的 `scripts/__pycache__/` 和 `tests/__pycache__/` 被识别为本轮验证临时产物；最终 hygiene 只删除这些新生成缓存，不触碰用户文件。

## 8. 六域语义审计

| 审计域 | 权重 | 得分 | 结果 | 核心证据 |
|---|---:|---:|---|---|
| Logic Correctness | 20% | 99 | PASS | runtime canonical order、两种 fallback 许可、drift fail-closed、Execution Gate 不变 |
| Autonomy | 15% | 99 | PASS | Agent 主动查 INDEX，不再等待人类提醒或点名 Project Skill |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | 98 | PASS | entry/re-entry 保留，actionable intent 增量匹配，chat 不全量扫描；Onboarding 无改动 |
| Development / Test Workflow | 20% | 98 | PASS | Operational Support 与 mandatory helper 兼容，focused RED/GREEN 和全量回归完整 |
| Memory | 15% | 99 | PASS | INDEX 仍是唯一发现索引，无 cache/status/artifact；context loss 强制重建发现状态 |
| Recommendation | 15% | 98 | PASS | matched、absent/no-match、drift 分支分别导向 Gate、fallback、Recovery，下一动作唯一 |

加权得分：

```text
99*0.20 + 99*0.15 + 98*0.15 + 98*0.20 + 99*0.15 + 98*0.15 = 98.5
```

最终等级：`STRONG`。

### 8.1 已通过的不变量

- Agent Loop controller / Human Gates 高于 Project Skill；
- valid active Project Skill match 高于 runtime/global helper 和 built-in/generic fallback；
- runtime/global Skill inventory 不能证明项目 Skill 不存在；
- Project Skill negative claim 需要当前项目的 `index-absent | no-active-match` 证据；
- drift 不能通过临时资源或等价通用动作绕过；
- 发现和只读加载不等于 Execution Gate；
- `proposed | disabled | deprecated` 不进入正常路由；
- 只加载匹配 body，不全量加载所有 Skill；
- chat 不创建 artifact 或 discovery cache；
- root AGENTS 只增加一句短提醒，完整规则留在 runtime/design/reference；
- Skill 版本保持 1.4.0。

## 9. 压力场景

| 场景 | 结果 | 关键判断 |
|---|---|---|
| Active On-Demand Match Before Operational Fallback | PASS | active match 先于通用动作并停在 Execution Gate |
| Runtime Inventory Is Not Project Skill Inventory | PASS | 原生 inventory 不支持 negative claim |
| Index Absent Allows Generic Method | PASS | `index-absent` 允许只读通用方法，不建空目录 |
| No Active Match Avoids Full Body Scan | PASS | metadata-only，`no-active-match` 后 fallback |
| Inactive Skill Cannot Route | PASS | proposed/disabled/deprecated 被排除 |
| Manifest Drift Blocks Equivalent Fallback | PASS | drift 停止，不能借临时资源绕过 |
| Execution Gate Still Blocks Side Effects | PASS | discovery question 不授权命令/工具/外部动作 |
| Context Re-entry Rechecks Discovery | PASS | context loss 后重读 INDEX/manifest，不复用旧 grant |
| Same-Name Ownership Is Explicit | PASS | owner/path 必须显式，冲突视为 drift |
| Chat Remains Lightweight | PASS | 规则问答不全量扫描或写 artifact |

全量回归还重新覆盖 Requirement → ADR → Feature、简单需求、Product Brief Source Gate、Delivery Contract Gate、TDD、Active/Pause/Close/Reopen、Requirement lifecycle、Follow-up、Submit、stale-memory/root guidance 和普通 Chat 等既有代表性场景；37/37 shell tests 全部通过。

## 10. Proposal 验收映射

| Proposal 条目 | 实现/证据 | 结论 |
|---|---|---|
| actionable intent 在 fallback 前检查 INDEX | `SKILL.md`、runtime canonical sequence、stage guide | 符合 |
| runtime/global inventory 与 Project INDEX 分离 | runtime/design/project-skills/README/Usage | 符合 |
| negative claim 需要项目证据 | runtime/project-skills/root reminder | 符合 |
| metadata-first、matched-body-only | runtime/design/project-skills/checklist | 符合 |
| matched active 保留 Execution Gate | 所有核心 surface + focused test | 符合 |
| drift fail closed | runtime/design/project-skills/stage scenarios | 符合 |
| chat 保持轻量 | runtime/design/project-skills/scenario | 符合 |
| context re-entry 重建 discovery | runtime/design/project-skills/scenario | 符合 |
| coordinated workflow surfaces | 20 个 tracked files + focused test/docs/reports | 符合 |
| 不新增 stage/intent/status/cache/schema | diff/semantic audit | 符合 |
| root guidance 只保留短提醒 | exact-once + forbidden-detail assertions | 符合 |
| focused RED/GREEN | RED 报告 + GREEN output | 符合 |
| full validation + 中文报告 | 37/37 + 本报告 | 符合 |
| 版本/Git/安装边界 | version checks + status review | 符合 |

## 11. 实施偏差与修正

没有设计范围漂移。有两项仅涉及测试/计划命令的机械修正：

1. Implementation Plan 的 Task 2 临时检查最初在整个 `runtime.md` 搜索第一个 `Execution Gate`，错误命中了新 section 之前的既有文本。已把计划命令修正为先提取 `## Project Skill Discovery Guard` section 再比较顺序；focused contract 从一开始就使用 section 提取，不受影响。
2. focused test 最初用整行匹配 root reminder，但模板提醒位于编号列表并带 `9b.` 前缀。已改为对完整提醒短句做文件内精确子串计数并要求恰好一次；仍然同时禁止 root 出现四个详细 result 名称，约束没有降低。

## 12. 剩余风险

### Low 1：语义 trigger 匹配仍依赖 Agent 判断

本轮明确不建设 executable schema 或确定性 trigger engine。INDEX Triggers/Scope 的语义匹配仍依赖 Agent；风险由 progressive metadata、exact manifest、pressure scenarios 和 Execution Gate 限制。

### Low 2：没有独立 live LLM E2E harness

当前证据是 ordering-aware structural contract、跨文件语义审计和压力场景，并非多个真实运行时 Agent 的在线行为对比。仓库当前没有已发布的通用 self-test harness；本轮不扩大范围建设它。

### Low 3：下游 root guidance 需要人类确认刷新

源码模板 revision 已更新为 `1.4.0-20260716`。使用旧模板的下游项目会被 checker 判为 stale，但实际刷新仍须遵守 root guidance Human Review，不会自动覆盖项目内容。

未发现 Critical、High 或 Medium 问题。

## 13. 发布与提交判断

当前判断：

- 功能实现和验证：`Human Review ready`；
- Skill 版本：仍为 `1.4.0`；
- commit/push/tag/PR/merge/release/publish：均未获本轮授权，也未执行；
- installed Skill sync：未获授权，也未执行；
- 推荐下一阶段：人类审查修改文件、RED/GREEN、全量报告和剩余 Low 风险，然后决定是否授权 Submit / Integrate 检查。
