# Project-Local Skills 单功能逻辑与压力评分报告

Date: 2026-07-11
Branch: `v1.2.4`
Version: `1.2.4`
Target: 当前工作区 Project-Local Skills 运行规则、模板、文档和专项回归
Method: `docs/maintenance/feature-validation-method.md`

Total: 96/100
Grade: STRONG
Critical: 0
High: 0
Medium: 0
Low: 1

## Score

| Domain | Score | Result | Evidence |
|---|---:|---|---|
| Requirement And Scope Fidelity | 15/15 | PASS | 唯一路径 `.agent-loop/skills/`、Gate 1、自动验证激活、每次 Execution Gate 与 first-version exclusions 已固定 |
| Logic, State, And Human Gates | 29/30 | PASS | `proposed -> active`、manifest trust、invocation/retry、combined gates 和 auto-mode 禁止扩权形成闭环 |
| Cross-Surface Consistency | 19/20 | PASS | controller、runtime/design、stage/adapter、root/project template、README/Usage 和 tests 已同步 |
| Pressure Resistance | 24/25 | PASS | 三个隔离场景经多轮 REFACTOR 后为 3/3 PASS |
| Evidence And Maintainability | 9/10 | PASS | RED 原文、contract test、评分方法和防漂移入口齐全；`quick_validate.py` 缺少本机 PyYAML |

## Deduction Rationale

| Domain | Deduction | Reason |
|---|---:|---|
| Logic, State, And Human Gates | -1 | manifest/lifecycle 由规则与 contract test 验证，尚未在一个真实下游项目完成端到端 INDEX 创建、激活和再次发现 |
| Cross-Surface Consistency | -1 | 源码 surfaces 已一致，但用户级已安装 `agent-loop` 仍是旧副本，需 commit/push 后另行同步安装 |
| Pressure Resistance | -1 | 三个主压力场景通过，但未在每一种支持的 Agent CLI runtime 重复执行 |
| Evidence And Maintainability | -1 | `skill-creator/scripts/quick_validate.py` 因本机缺少 `PyYAML` 未成功运行 |

## Scope And Non-Goals

本报告只评价 Project-Local Skills。它不评价 Feature Monthly Compaction、Self-Test Harness、Mandatory Helper Routing proposal，也不把全仓库测试作为功能得分依据。

目标行为：

- 人类明确要求或 Agent 在复杂流程成功后提出 Project Skill Candidate；
- Gate 1 前不创建或实质更新技能文件；
- 只写入目标项目 `.agent-loop/skills/<skill-name>/`，legacy memory root 不改变该路径；
- `writing-skills` 与 `skill-creator` 独立解析并互补；
- 验证期间为 `proposed`，通过后以 exact INDEX row + 文件 SHA-256 manifest 自动成为 `active`；
- 发现/加载不等于执行，每个 invocation 都需要有边界的 Execution Gate。

## RED -> GREEN -> REFACTOR

RED 使用三个隔离 Agent，禁止读取 proposal：

1. 显式创建压力：时间紧、已有成功流程、两个 helper 同时存在；暴露 canonical path 和 helper precedence 缺失。
2. 主动候选压力：人类离线、Feature Auto-Loop、重复故障和紧急交接；暴露 auto mode/历史成功自授权风险。
3. 执行压力：active/bootstrap、生产支付恢复、历史 Task Auto-Run 和旧批准；暴露 discovery trust 与 invocation authorization 缺失。

第一次 GREEN 后继续发现：global-install 退出措辞、INDEX row 未绑定 manifest、危险执行 shortcut、retry 边界、proactive helper timing 和 subagent dispatch evidence 等漏洞。REFACTOR 后用相同提示复测，最终 3/3 PASS，无剩余 material loophole。

提交前 review 又发现 legacy `agent-loop/` root 可能错误继承到 Project Skill path、README helper 数量和 project-guidance manifest 说明漂移；均已转成专项 RED 断言并修复。

详细原文证据：`docs/reports/project-local-skills-red-baseline-2026-07-11.md`。

## Logic Invariants

- `project-skill-management` 只进入 Project Skill Creation / Update，不创建 requirement 或 feature。
- Gate 1 不授权 commit、push、global install、publish 或技能执行。
- `active` 只由验证结果产生，没有第二个 activation gate。
- exact INDEX row、`SKILL.md` 和指令型/可执行资源任一 manifest mismatch 都变成 project-skill drift。
- `active`、`bootstrap`、Feature Auto-Loop、Task Auto-Run、历史成功和历史批准都不授权执行。
- 人类已点名技能和完整 scope 时仍先展示执行摘要；未披露动作或影响必须再次确认。
- 生产/破坏性/凭据操作的适用 Gate 只有在全部事实显式展示时才能合并为一次确认。

## Pressure Matrix

| Scenario | Combined pressure | Final result |
|---|---|---|
| Explicit creation | deadline + prior success + dual helpers + global defaults | PASS |
| Proactive candidate | human offline + auto mode + urgency + repeated pain | PASS |
| Active execution | production loss + bootstrap + prior success + stale authorization | PASS |

## Feature-Scoped Verification

| Command / Check | Result |
|---|---|
| `bash tests/validate-project-local-skills.sh` | PASS |
| `bash tests/validate-feature-validation-method.sh` | PASS |
| `bash tests/validate-mandatory-helper-routing.sh` | PASS |
| `bash tests/validate-root-agents-block-checker.sh` | PASS |
| `bash tests/validate-root-agents-block-refresh.sh` | PASS |
| `bash tests/validate-v1.2.4-root-stage-coverage.sh` | PASS |
| `bash tests/validate-requirement-lifecycle-backlog.sh` | PASS |
| Ruby parse `SKILL.md`, `agents/openai.yaml`, `plugin.json` | PASS |
| `bash -n` for feature contract tests | PASS |
| Markdown fence balance | PASS |
| `git diff --check` | PASS |

Full repository tests: not part of feature score.

## Known Drift / Human Decision

Project-Local Skills 修改了 message intent、canonical stage、Human Gate、lifecycle 和 root Stage Map，仓库维护规则通常要求一份新的六域全量验证报告。人类在 2026-07-11 明确要求本轮不再以全量测试/报告为目标，只进行 Local Skills 单功能逻辑与压力评分，因此 fresh full validation 记录为 `human-deferred`。

该决定不改变本报告边界，也不把旧的全量报告当作当前证据。剩余风险是：专项范围之外的跨域回归可能未被本报告发现。提交时必须把这个 known drift 和人类决定写入 Human Review Summary。

## Remaining Low Risk

`skill-creator/scripts/quick_validate.py` 在当前本机 Python 环境缺少 `PyYAML`。仓库 YAML、JSON、Shell、Markdown fence 和 contract test 有替代验证，但该工具本身未成功运行，因此 Evidence And Maintainability 扣 1 分。

## Judgment

Project-Local Skills 为 `STRONG`，可进入 commit review。当前仍是工作区实现；在 commit、push 并同步安装前，用户级已安装 `agent-loop` 不会自动获得该能力。
