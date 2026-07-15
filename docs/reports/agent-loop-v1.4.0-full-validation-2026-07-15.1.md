# Agent Loop v1.4.0 Human-Guided Bug Management 全量验证报告

## 结论摘要

| 项目 | 结果 |
|---|---|
| 日期 | 2026-07-15 |
| 分支 | `alpha/v1.4.0` |
| 审计对象 | 基线 `85d593cf7bf57533570ac5f2aeed150450b21af7` 上的当前未提交工作区 |
| Skill 版本 | `1.4.0`，未升级 |
| Root managed block revision | `1.4.0-20260715.1`，`13/13` 一致 |
| focused validation | PASS |
| 受影响 Python | `62/62 PASS` |
| 受影响 Shell | `17/17 PASS` |
| 全量 Python | `98/98 PASS`，最终 fresh run 为 `Ran 98 tests in 21.160s` |
| 全量 Shell | `36/36 PASS`，按当前 `tests/*.sh` 实时重数，最终 fresh run 为 `6s` |
| 总分 | **99/100 — STRONG** |
| 当前严重问题 | Critical `0` / High `0` / Medium `0` / Low `0` |
| 平台证据 | `macOS-verified / Windows-test-defined` |
| Git / 发布动作 | 未 stage、commit、push、tag、PR、merge、release、publish |

结论：Human-Guided Bug Management 已按批准的 Proposal 和 Implementation Plan 落入 Agent Loop v1.4.0 开发工作区。Bug Record、Requirement 与 Feature 的权限边界清晰，Gate 无可复用绕过，90 天 Feature metadata scan 与 archive/rehydrate 边界一致。当前可进入最终 Human Review；本报告不构成提交、发布或已安装 Skill 同步授权。

## 审计环境与边界

- 系统：macOS 26.5，Darwin 25.5.0 arm64
- Python：3.14.5
- Ruby：2.6.10
- Bash：3.2.57
- 仓库视角：Agent Loop Skill 源码维护者，不是目标项目用户 Agent
- 未在源码仓库创建 `.agent-loop/`、真实 Bug workspace、分支、worktree、外部 Issue 或安装副本
- 未覆盖历史报告 `docs/reports/agent-loop-v1.4.0-full-validation-2026-07-15.md`
- Proposal / Plan 是本轮批准设计与执行依据；runtime authority 仍为 `SKILL.md`、`references/` 和 `templates/`

## 六域语义审计

| 审计域 | 分数 | 结果 | 通过证据 |
|---|---:|---|---|
| Logic Correctness | 100 | PASS | Bug Status / Resolution 双轴、唯一 Resolution Path、关闭/重开历史、duplicate/cannot-reproduce/accepted-risk fail-closed、Gate 独立性均一致 |
| Autonomy | 99 | PASS | Agent 先扫描 Bug Index 与项目证据，再给出一个路径推荐；信息不足走 `investigate-first`，真正 blocker 才交给人类 |
| Project Entry / Evidence Graph + DDD Onboarding | 100 | PASS | 无可靠 memory 时 Project Entry 优先；root 只做 routing；未改变 Onboarding stage、artifact 或现有契约 |
| Development / Test Workflow | 99 | PASS | 所有修复仍进入 Feature spec/tasks/tests/plan/TDD/Verify/Review/Drift；Feature 测试仅能推进 Bug 到 `verifying` |
| Memory | 100 | PASS | `bugs/INDEX.md` 独占 Bug inventory/backlog/locator；`project.md` 只保留 lookback 与当前工作指针；归档不改变 Feature identity/ownership |
| Recommendation | 99 | PASS | 每次只推荐一个 Resolution Path / Recovery / investigation；Bug、Feature、Requirement、Git、close/reopen 授权逐项命名且不能互相复用 |

加权评分为 99/100。扣分仅反映本机未取得 Windows 实跑证据，以及本轮按人类要求未派发独立审查 Agent；二者均不是当前逻辑缺陷。

## 关键跨文件不变量

| 不变量 | 结果 | 证据面 |
|---|---|---|
| Bug Management 只是 Feature Follow-up / Flow-back 内部方法 | PASS | `SKILL.md`、`references/runtime.md`、`references/design.md`、`references/stage-guides.md`、root Stage Map |
| 不新增 canonical stage / message intent | PASS | runtime Stage Order / intent machine check；focused contract |
| Bug Record 管身份、事实、证据、生命周期、Resolution Path、关闭/重开 | PASS | `references/bug-management.md`、Bug templates、concept/design/artifact rules |
| Requirement 只管产品目标与预期行为 | PASS | optional `0..N` relationship；不改 source、不自动改 lifecycle |
| 所有代码修复由 Feature workflow 承担 | PASS | Bug 无 tasks/tests/plan；Feature spec/tests/plan/notes 与 completion 路径完整 |
| Bug identity 无时间截止，Feature ownership 默认 90 天 metadata scan | PASS | 全 Bug Index scan；90 天非硬边界；120 天 evidence-driven extension |
| Archive 只改位置，不改 ownership | PASS | locator 只读发现无需 rehydrate；确认 flow-back 后、执行前才走 exact-hash rehydrate Gate |
| Report Origin 只是 provenance | PASS | 支持十种值与 `unknown`；不产生 Owner、Assignee、Priority、客户线或权限 |
| Human Gates 不互相复用 | PASS | Resolution Path、Feature、Requirement、Bug close/reopen、archive、branch/submit/release 均独立 |
| Root guidance 只做导航 | PASS | 原 Stage row 保留；读取顺序为 `bug-management.md` → `feature-follow-up.md`，未复制枚举/算法/Gate 表 |
| Skill 版本保持 1.4.0 | PASS | `SKILL.md`、`plugin.json`、`README.md`、`Usage.md` 一致 |

## RED → GREEN 证据

### 既有基线

实现前：

- Python：`98/98 PASS`，21.845 秒
- Shell：`35/35 PASS`
- root revision：`1.4.0-20260715`，13 个 managed blocks

### Focused RED

先新增 focused contract，再执行：

```bash
bash tests/validate-bug-management.sh
```

得到预期失败和退出码 1：

```text
FAIL: missing required file: references/bug-management.md
```

该 RED 证明原发布包没有 canonical Bug Management reference，不是测试夹具或语法错误。完整历史保存在 `docs/reports/agent-loop-v1.4.0-bug-management-red-baseline-2026-07-15.md`。

### 渐进修复与 focused GREEN

契约依次推进过 canonical reference、Bug templates、stage/branch/root/scenario 等真实缺口。Task 7 完成后，focused contract 仍只在尚未加入的 `60-Day Feature Remains Inside Default Bug Ownership Window` 场景保持 RED。补齐 20 个批准场景、9 个 Gate 对抗场景和七字段结构校验后：

```text
PASS: Human-Guided Bug Management identity, lifecycle, routing, archive, gate, artifact, and scope contract is complete
```

### 全量验证与 Human Review 中发现并关闭的回归

| 发现 | 原因 | 修复 | 当前状态 |
|---|---|---|---|
| Feature Monthly Archive exact contract 失败 | Feature Follow-up 重写时丢失 `rehydrate before reopened execution` 兼容句 | 在 `references/feature-follow-up.md` 恢复精确 invariant，同时保留 confirmed flow-back / exact-hash Gate | CLOSED，affected `17/17`、全量 `36/36` |
| Drift Check 既有 fallback exact contract 失败 | 新增 Bug authority 路由时替换了原 Project Memory / Feature Completion 逐字出口 | 把 Bug authority change 前置为独立规则，并恢复原 fallback 句 | CLOSED，全量 `36/36` |
| live human/scenario docs 残留旧 30-day 默认值 | README 与旧压力场景未随 runtime 统一到 90 天 | 更新 README、root-follow-up 场景、Day 91/120 扩展场景；只保留 Proposal/Plan 历史基线和“retired 30-day”反例 | CLOSED，语义搜索与回归通过 |
| Bug 目录出现两套当前约定 | 部分 surface 把稳定 Bug ID 误写成目录占位符 `bugs/<bug-id>/` | 当前 authority、template、human docs 与实施计划统一为 `bugs/YYYY-MM-DD-<bug-slug>/`，并增加负向回归断言 | CLOSED，focused GREEN |
| Bug intake 的 create/scan 顺序跨文件漂移 | runtime 先创建记录，stage guide 先扫描 Feature evidence | 固定为 Bug Index identity scan → Feature ownership scan → create/update/reopen；用精确顺序断言锁定 | CLOSED，focused GREEN |
| `in-progress` 可与非修复 Resolution Path 组合 | 双轴定义缺少跨轴兼容约束 | 只允许 `flow-back | linked-feature | maintenance-fix`，且必须有 Human-confirmed Fix Feature Target；新增 Requirement Path 对抗场景 | CLOSED，focused GREEN |
| `SKILL.md` 摘要保留旧顺序歧义 | 详细 authority 已统一，但 concise entrypoint 仍可读成先建 Bug 再扫 Feature | 摘要改为两层扫描完成后才 create/update/reopen，并增加 exact contract | CLOSED，focused GREEN |

## 实际测试命令与结果

### Focused / affected

```bash
bash tests/validate-bug-management.sh

PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-bug-affected-pyc \
  python3 -m unittest \
  tests.test_root_agents_blocks \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply \
  tests.test_feature_monthly_archive_restore -v

# 17 个 Feature Follow-up / Archive / Branch / Requirement / Feature /
# Human Gate / root guidance 受影响 contract，使用 set -euo pipefail 顺序执行
```

实际结果：focused `PASS`；affected Python `62/62 PASS`，`Ran 62 tests in 13.261s`；affected Shell `17/17 PASS`。

### Full executable regression

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-bug-final-pyc \
  python3 -m unittest discover -s tests -p 'test_*.py' -v

tests_count=$(find tests -maxdepth 1 -type f -name '*.sh' | wc -l)
for test_file in tests/*.sh; do
  bash "$test_file"
done
```

实际结果：

- Python：`98/98 PASS`，最终 fresh run 为 `Ran 98 tests in 21.160s`
- Shell：实时库存 `36`，`36/36 PASS`，最终 fresh run 为 `6s`

## 29 个 Bug Management 压力场景

以下 20 个是批准 Proposal 的核心场景；另有 9 个对抗扩展场景覆盖独立 Gate、非法 artifact、重复身份、归档副作用，以及 `requirement + in-progress` 非法组合。

| # | 场景 | 结果 |
|---:|---|---|
| 1 | Existing Feature Regression Flows Back | PASS |
| 2 | Narrow Internal Bug Uses Maintenance Fix | PASS |
| 3 | New Product Behavior Is Not Misclassified As Bug | PASS |
| 4 | Multiple Origins Deduplicate Into One Bug | PASS |
| 5 | Existing Bug Record Closes As Duplicate | PASS |
| 6 | Closed Bug Reopens Append-Only | PASS |
| 7 | Unknown Report Origin Does Not Block Triage | PASS |
| 8 | Cannot Reproduce Requires Attempt Evidence | PASS |
| 9 | Requirement Link Does Not Auto-Rollback Lifecycle | PASS |
| 10 | Bug May Link Multiple Requirements | PASS |
| 11 | One Feature May Resolve Multiple Bugs | PASS |
| 12 | Ordinary Chat Does Not Create Bug Artifact | PASS |
| 13 | Missing Agent Loop Memory Routes To Project Entry | PASS |
| 14 | Archived Feature Discovery Does Not Require Rehydrate | PASS |
| 15 | Sealed Release Requires New Patch Context | PASS |
| 16 | Passing Feature Tests Does Not Auto-Close Bug | PASS |
| 17 | Accepted Risk Requires Explicit Human Decision | PASS |
| 18 | Customer Origin Does Not Infer Customer Repair Line | PASS |
| 19 | 60-Day Feature Remains Inside Default Bug Ownership Window | PASS |
| 20 | 120-Day Feature Uses Evidence-Driven Extended Scan | PASS |

全部 29 个场景都由 focused contract 校验以下七个字段：`Evidence`、`Bug Record Decision`、`Expected Behavior Source`、`Resolution Path`、`Required Human Gate`、`Forbidden Action`、`Next Stage`。

## Human Gate 对抗结果

| 尝试绕过 | 结果 |
|---|---|
| 用 accepted Requirement 复用为 Feature 创建/执行授权 | BLOCKED |
| 用 critical Severity 推导 hotfix / branch / release | BLOCKED |
| 用 unknown Origin 阻止调查或修复 | BLOCKED |
| 把 `deferred` 合理化成 `closed` / accepted-risk | BLOCKED |
| 用 Feature tests 复用为 Bug Close Gate | BLOCKED |
| archive discovery 自动 rehydrate | BLOCKED |
| 标题相同自动合并或删除 Bug | BLOCKED |
| 在 Bug Record 下创建 tasks/tests/plan | BLOCKED |
| 用 commit/push approval 复用为 Bug close | BLOCKED |
| 用 `requirement` 路径把 Bug 标成 `in-progress` | BLOCKED |

## 机械检查

执行：

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md"); YAML.load_file("agents/openai.yaml")'
python3 -c 'import json; json.load(open("plugin.json", encoding="utf-8"))'
python3 -m compileall -q scripts tests
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
find . -name '*.rb' -type f -print0 | xargs -0 -n1 ruby -c
# repository Markdown fence balance checker
git diff --check
# untracked text whitespace、root .agent-loop、__pycache__ 检查
```

结果：

| 检查 | 结果 |
|---|---|
| `SKILL.md` + `agents/openai.yaml` YAML | `2/2 PASS` |
| `plugin.json` JSON | `1/1 PASS` |
| Python compileall | PASS；生成的 `__pycache__` 已清除 |
| Shell syntax | `37/37 PASS` |
| Ruby syntax | `5/5 PASS` |
| Markdown fence balance | `211/211 PASS` |
| `git diff --check` | PASS |
| untracked text trailing whitespace | `8/8 PASS` |
| root `.agent-loop/` | 不存在 |
| residual `__pycache__` | 不存在 |

部分 Shell contract 会在导入 checker 时产生 `scripts/__pycache__/` 或 `tests/__pycache__/`。这是验证副作用，不是实现文件；全量执行后已清除，并用最终 residual check 确认不存在。

## Proposal 完成标准逐项覆盖

| # | Proposal 要求 | 结果 | 落点 |
|---:|---|---|---|
| 1 | Bug 核心概念跨 surface 一致 | PASS | concepts/design/runtime/reference/templates/tests |
| 2 | `.agent-loop/bugs/` 按需创建且无 Bug 执行子系统 | PASS | artifact rules、Bug templates、root absence check |
| 3 | 所有修复经 Feature workflow | PASS | stage/checklist/spec/tests/plan/notes/completion |
| 4 | Requirement 只管产品语义，关系可选 0..N | PASS | requirement-management/template/bug reference |
| 5 | 90 天 metadata scan、证据深读、超期扩展 | PASS | feature-follow-up/runtime/scenarios |
| 6 | duplicate/cannot-reproduce/not-a-bug/accepted-risk/reopen 有证据历史 | PASS | canonical lifecycle rules + scenarios |
| 7 | Status / Resolution 双轴有效 | PASS | exact enums、transition rules、fail-closed |
| 8 | 各 Human Gate 独立保留 | PASS | runtime/reference/stops/review/adversarial cases |
| 9 | Index / README 可恢复 open/deferred/verifying | PASS | templates、memory/recovery rules |
| 10 | Project Memory 不存 Bug backlog | PASS | project-memory-mode/project template |
| 11 | Branch 只消费 confirmed Fix Feature / Target Release Context | PASS | branch-management + branch regression |
| 12 | 覆盖 20 个批准核心场景及对抗扩展 | PASS | validation-scenarios + 29-scenario structured contract |
| 13 | focused/full/mechanical/diff 全通过 | PASS | 本报告与 RED 报告 |
| 14 | 区分 Bug 记录、Feature 修复、真实 Git side effects | PASS | authority tables、scope audit、无 Git 动作 |

## 实际修改范围

新增：

- `references/bug-management.md`
- `templates/bug-index.md`
- `templates/bug-README.md`
- `tests/validate-bug-management.sh`
- `docs/reports/agent-loop-v1.4.0-bug-management-red-baseline-2026-07-15.md`
- 本报告

已批准且保留的设计输入：

- `docs/proposal/v1.4.x/bug-management.md`
- `docs/proposal/v1.4.x/bug-management-implementation-plan.md`

协调修改：

- entry/runtime/design：`SKILL.md`、`references/runtime.md`、`references/design.md`、`references/concepts.md`、`references/artifact-rules.md`、`references/feature-follow-up.md`
- workflow/gates：`references/stage-guides.md`、`references/workflow-checklists.md`、`references/requirement-management.md`、`references/implementation-planning.md`、`references/feature-completion-check.md`、`references/human-review-summary.md`、`references/branch-management.md`、`references/submit-and-integrate.md`
- memory/templates：`references/project-memory-mode.md`、`references/project-guidance.md`、`references/external-skill-adapters.md`、`references/document-templates.md`、`templates/project.md`、`templates/requirement-set-README.md`、`templates/spec.md`、`templates/tests.md`、`templates/plan.md`、`templates/notes.md`
- root/human docs/history：`templates/root-AGENTS.md`、`README.md`、`Usage.md`、`CHANGELOG.md`
- scenarios/regressions：`references/validation-scenarios.md`、`tests/test_root_agents_blocks.py`、`tests/validate-branch-management-strategy.sh`、`tests/validate-project-local-skills.sh`、`tests/validate-requirement-lifecycle-backlog.sh`、`tests/validate-root-agents-block-checker.sh`、`tests/validate-root-agents-block-refresh.sh`、`tests/validate-v1.2.4-root-stage-coverage.sh`

## 平台验证边界

- macOS：focused、affected、完整 Python/Shell、语法与格式检查均已实际执行。
- Windows：仓库 `.github/workflows/cross-platform-checkers.yml` 仍定义 `windows-latest`，`tests/test_python_checker_contract.py` 校验 macOS/Windows matrix；本轮没有远程 Windows runner 结果，因此只声明 `Windows-test-defined`，不声明 Windows 已验证。
- 本功能没有增加 Python 依赖、脚本运行时、可执行数据库或 YAML/JSON schema。

## 当前问题、风险与未采纳范围

独立 Human Review 发现的 1 个 High 与 3 个 Medium 实现问题均已补 RED、修复并回归。当前未解决 Critical/High/Medium/Low 逻辑问题：无。

剩余验证边界：

1. 未取得 Windows 实跑证据；不影响当前 Markdown/runtime contract 的 macOS 验收，但发布方如需跨平台签字，应在 Windows CI 取得真实结果。
2. 本轮遵守“不得派发子 Agent”，因此没有独立 Agent review；Task 10 由主 Agent 做逐项自审，最终仍停在 Human Review。
3. Bug 规则是文档/模板驱动的 Agent workflow contract；Proposal 明确不实现 executable schema、Bug database、Bug Archive、自动 Issue Tracker、Owner/Assignee 或第二套执行系统。

未采纳或未扩大到：新 canonical stage、message intent、Bug tasks/tests/plan、Bug archive/retention、worktree/branch memory merge、真实 branch/tag/PR/release、外部 Issue、CLI Skill 同步、版本升级。

## 范围漂移与发布判断

- Proposal / Plan 冲突：未发现。
- 版本漂移：无，仍为 `1.4.0`。
- Artifact 漂移：无；源码仓库无目标项目 `.agent-loop/`。
- Workflow 漂移：无；Feature Follow-up stage 保留，Bug Management 只作为内部方法。
- Git / 外部副作用：无。
- 当前判断：**Human Review ready**，不是 commit/release authorization。
- 推荐下一阶段：由设计/验收 Agent 对本报告、Proposal 完成标准与 diff 做 Human Review；未经新的明确授权，不进行 stage、commit、push、tag、PR、merge、release、publish 或已安装 Skill 同步。
