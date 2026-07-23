# Agent Loop v1.4.0 Human-Guided Bug Management RED 基线报告

## 审计边界

- 日期：2026-07-15
- 分支：`alpha/v1.4.0`
- 基线提交：`85d593cf7bf57533570ac5f2aeed150450b21af7`
- Skill 版本：`1.4.0`
- Root managed block 基线 revision：`1.4.0-20260715`，共 `13` 个 block
- 实施前 Shell 测试库存：`35` 个 `tests/*.sh`
- 实施前工作区：只有已批准的 `docs/proposal/v1.4.x/bug-management.md` 与 `docs/proposal/v1.4.x/bug-management-implementation-plan.md` 两个未跟踪文件
- 视角：Agent Loop Skill 源码仓库维护者；没有创建目标项目 `.agent-loop/`

## 既有 GREEN 基线

执行命令：

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/agent-loop-bug-baseline-pyc \
  python3 -m unittest discover -s tests -p 'test_*.py' -v

for test_file in tests/*.sh; do
  bash "$test_file"
done
```

实际结果：

- Python：`98/98 PASS`，`Ran 98 tests in 21.845s`，退出码 `0`
- Shell：`35/35 PASS`，退出码 `0`
- 既有 Branch Management、Feature Monthly Archive、Requirement、Feature Follow-up、Human Gate、root guidance 等契约均为 GREEN

## Focused RED

先新增 `tests/validate-bug-management.sh`，在没有修改 runtime、reference 或 template 的情况下执行：

```bash
bash tests/validate-bug-management.sh
```

实际结果：

```text
FAIL: missing required file: references/bug-management.md
```

退出码：`1`

该失败是预期 RED：当前发布包缺少 Human-Guided Bug Management 的 canonical reference，focused contract 因真实能力缺口失败，而不是命令、语法或测试夹具错误。

## RED Contract 覆盖

focused contract 已固定以下已批准约束，后续不得为转绿而削弱：

- Bug Report 与稳定 Bug Record 身份分离；
- `Status` 与 `Resolution` 双轴生命周期；
- Report Origin 完整枚举且不引入 Owner / Assignee；
- 一个当前 Resolution Path，所有代码修复由 Feature workflow 承担；
- Requirement 只建立可选 `0..N` 关系，不自动修改 lifecycle；
- Bug Index metadata 去重 / reopen 无时间 cutoff；
- Feature ownership 默认 90 天 metadata scan，并允许证据驱动的超期扩展；
- Archive 只改变 Feature 位置，不改变 identity / ownership；发现和 Human Review 不要求 rehydrate；
- Bug close、reopen、Feature create/reopen、Requirement change 与 Git actions 保持独立 Human Gate；
- Bug Management 不成为 canonical stage 或新的 message intent；
- 源码仓库不创建目标项目 `.agent-loop/`，也不创建 Bug tasks/tests/plan 模板。

## 授权与副作用边界

截至 RED 固化时：

- 未修改任何 runtime authority、target-project artifact 或 Skill 安装副本；
- 未创建或切换 branch/worktree；
- 未 stage、commit、push、tag、创建 PR、merge、release、publish；
- 未调用外部 Issue Tracker；
- 未派发子 Agent。

后续 GREEN 只能按已批准 Proposal 与 Implementation Plan 的 Task 1–10 实施，并保留本 RED 历史。

## GREEN 修复过程

按 Task 1–8 依次补齐并协调：

- canonical runtime authority：`references/bug-management.md`；
- Bug Index / Bug README 模板及 `document-templates.md` 同步副本；
- runtime / design / concepts / artifact ownership 与 Feature Follow-up 90 天 ownership scan；
- Requirement、Feature spec/tests/plan/notes、completion、Human Review、submit、branch、archive 与 project memory 边界；
- root Stage Map routing-only 更新，以及 13 个 managed blocks 的 `block-version:1.4.0-20260715.1` 同步；
- README、Usage、CHANGELOG 与 20 个批准场景、9 个 Human Gate 对抗场景；
- Branch Management 等既有契约对 Bug ownership 边界的协调更新。

Task 7 root/version/human-doc 回归实际执行并通过：

```bash
python3 -m unittest tests/test_root_agents_blocks.py -v
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-requirement-lifecycle-backlog.sh
bash tests/validate-human-help-version-docs.sh
bash tests/validate-branch-management-strategy.sh
```

实际结果：Python root checker `8/8 PASS`；上述 7 个 shell contract 均 `PASS`。随后 focused contract 仍只在 Task 8 尚未加入的 `60-Day Feature Remains Inside Default Bug Ownership Window` 场景上保持 RED，证明 Task 7 没有通过削弱断言提前转绿。

## 最终 Focused GREEN

补齐 20 个批准的核心压力场景、9 个对抗扩展场景，以及逐场景七字段结构校验后执行：

```bash
bash tests/validate-bug-management.sh
```

实际结果（退出码 `0`）：

```text
PASS: Human-Guided Bug Management identity, lifecycle, routing, archive, gate, artifact, and scope contract is complete
```

focused GREEN 保持了最初 RED contract 的全部断言，没有移除或放宽缺口检测。

## 独立 Human Review RED → GREEN

首次 focused GREEN 后，主 Agent 以 Proposal、canonical runtime、模板和 focused contract 为证据重新审查实现，发现 4 个跨文件漏洞。每个漏洞先加入可复现的负向断言，再修复 runtime / template / human docs：

| 严重度 | Review RED | 实际失败 | 修复 | 当前结果 |
|---|---|---|---|---|
| High | Bug 目录同时出现 canonical `bugs/YYYY-MM-DD-<bug-slug>/` 与简写 `bugs/<bug-id>/` | `FAIL: README.md missing Bug Management contract: bugs/YYYY-MM-DD-<bug-slug>/` | 所有当前 authority、template、human docs 与实施计划统一为日期加 slug 的稳定目录；focused contract 禁止旧简写回流 | GREEN |
| Medium | `runtime.md` 与 `stage-guides.md` 的 Bug intake 顺序不一致 | `FAIL: references/runtime.md missing canonical Bug intake sequence token` | 固定为完整 Bug Index metadata scan → 90-day Feature metadata scan → evidence-ranked deep/extended scan → create/update/reopen Bug Record | GREEN |
| Medium | `Status: in-progress` 可与 `requirement`、`investigate-first`、`no-fix` 等非修复路径组合 | authority/template compatibility RED，且 `SKILL.md` 缺少对应 fail-closed contract | `in-progress` 只允许 `flow-back | linked-feature | maintenance-fix`，并要求一个 Human-confirmed Fix Feature Target；新增 Requirement Path 对抗场景 | GREEN |
| Medium | `SKILL.md` 的摘要句仍可解释为 Bug Index 扫描后先建记录、再扫描 Feature | `FAIL: SKILL.md missing Bug Management contract: Before creating, updating, or reopening ...` | 入口摘要明确要求 Bug Index 与 Feature ownership 两层扫描都完成后才 create/update/reopen | GREEN |

修复后再次执行：

```bash
bash tests/validate-bug-management.sh
```

实际结果（退出码 `0`）：

```text
PASS: Human-Guided Bug Management identity, lifecycle, routing, archive, gate, artifact, and scope contract is complete
```

该轮没有改变 Proposal 的产品模型；它关闭的是实现中的目录、排序、入口摘要与状态组合漂移。

## GREEN 时点的实际文件范围

新增：

- `references/bug-management.md`
- `templates/bug-index.md`
- `templates/bug-README.md`
- `tests/validate-bug-management.sh`
- 本 RED/GREEN 报告

协调修改：

- 入口与运行模型：`SKILL.md`、`references/runtime.md`、`references/design.md`、`references/concepts.md`、`references/artifact-rules.md`、`references/feature-follow-up.md`
- 工作流与边界：`references/stage-guides.md`、`references/workflow-checklists.md`、`references/requirement-management.md`、`references/implementation-planning.md`、`references/feature-completion-check.md`、`references/human-review-summary.md`、`references/branch-management.md`、`references/submit-and-integrate.md`
- memory / template 同步：`references/project-memory-mode.md`、`references/project-guidance.md`、`references/external-skill-adapters.md`、`references/document-templates.md`、`templates/project.md`、`templates/spec.md`、`templates/tests.md`、`templates/plan.md`、`templates/notes.md`、`templates/requirement-set-README.md`
- root / human docs / history：`templates/root-AGENTS.md`、`README.md`、`Usage.md`、`CHANGELOG.md`
- 场景与既有回归：`references/validation-scenarios.md`、root revision tests、Branch Management contract
- 设计证据：已批准 Proposal 与 Implementation Plan 只更新实施状态，不改已确认模型

最终完整文件清单与 full validation 结果由独立的 `.1` 全量验证报告记录。

## 当前授权与副作用边界

截至 focused GREEN：

- Skill 版本仍为 `1.4.0`；
- 源码仓库根目录没有目标项目 `.agent-loop/`；
- 没有创建真实 branch、worktree、tag、PR、release 或外部 Issue；
- 没有同步 Codex、Kimi Code 或 OpenCode 已安装 Skill；
- 没有 stage、commit、push、merge、release、publish 或 tag；
- 没有派发子 Agent；
- Task 9 完整验证与 Task 10 主 Agent 自审均已完成；当前停在最终 Human Review，不构成提交或发布授权。
