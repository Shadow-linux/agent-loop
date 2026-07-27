# AI-Led Lightweight Feature Gates 单功能混沌验证报告

> **历史报告：** 本报告中的 `67 / 100 — FRAGILE` 是修复前证据。两轮 TDD 修复与复测后的当前结果见 [ai-led-lightweight-feature-gates-feature-validation-2026-07-27.2.md](ai-led-lightweight-feature-gates-feature-validation-2026-07-27.2.md)；不要继续用本文件作为当前提交判断。

日期：2026-07-27
分支：`v1.5.2`
版本：`1.5.2`（开发中，未发布）
基线 HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
审计对象：当前未提交工作区中的 Feature 创建、Gate 1/2、Task 增减替换、Plan/No-Plan、执行流转与关闭边界

## 结论

总分：**67 / 100 — FRAGILE**
当前发现：**Critical 1 / High 3 / Medium 2 / Low 0**
提交判断：**不建议提交；先修复 Gate 授权歧义与正常流程误阻断，再复跑同一组 chaos scenarios。**

现有 focused tests 全绿并不代表混沌场景可靠。两条独立压力测试线发现：合法的同 Story 全量 Task replacement 会被脚本错误报为 `GATE_BLOCKED`；与此同时，重复 Gate 字段可把 `package-only` 覆盖成 `approve-and-start` 并得到 `GATE_VALID`。

`ASSESSMENT_REQUIRED` 是正常的 AI Semantic Review 路由，本报告没有把它计为 Gate 失败或 false positive。

## Scope Lock

本次只评估：

- Feature 从创建、Gate 1、Gate 2、执行、Verify/Review/Drift/Memory 到 Completion/Close 的路径；
- Gate 2 前后 Task 新增、减少、替换、重排、Human-gated/new Story 负控；
- `notes.md`、`spec.md`、`tasks.md`、`tests.md`、Plan 和 detail artifact 缺失/逃逸；
- package-only later start、Digest/Assessment binding、No-Plan 结构证据；
- Checker 与 AI/runtime 的职责边界。

不把 Feature Close 证据交给 Gate 1/2 Checker 检查；`GATE_VALID` 只代表当前 Gate 动作结构有效，不代表 Task 可标记 `done` 或 Feature 可关闭。未执行全仓库回归；它不是本次 feature score 的组成部分。

两名经人类明确授权的测试 Agent 使用只读 source/runtime 和系统临时 fixture 独立测试，未读取 Proposal 或既有 reports，未在仓库创建目标项目 `.agent-loop/` artifacts。

## 压力场景结果

### 生命周期与任务变动

| 场景 | 结果 | 判定 |
|---|---|---|
| 正常 Gate 2 review / approve-and-start / execute | exit 0 `GATE_VALID` | PASS |
| Gate 2 前新增、减少、替换、重排 Task | 4 / 4 valid | PASS |
| Gate 2 后同 Story 新 Task，无 Assessment | exit 3 `ASSESSMENT_REQUIRED` | PASS，AI 内部路由 |
| Gate 2 后同 Story新 Task，exact within Assessment | exit 0 | PASS |
| 删除或替换部分 initial Task，仍保留另一同 Story initial Task | exit 0 | PASS |
| 全部 initial Task 被同 Story新 Task 替换，Plan 与 exact Assessment 有效 | exit 1 `GATE_BLOCKED` | **FAIL，false positive** |
| 新 Story或 Human-gated Task | exit 1 | PASS，负控 |
| package-only 无变化 later start | exit 0 | PASS |
| package-only 变更但 Assessment stale/wrong | exit 3 | PASS |
| package-only exact current Assessment | exit 0 | PASS |
| v2 runtime-only Task/Test ledger 与 Plan rotation | exit 0 | PASS |
| Feature 永久取消/放弃 | 无明确终态与 disposition | **FAIL，设计缺口** |

生命周期 Agent 的合法自定义 Task mutation positive 中，1 / 10 被硬阻断；加入合法历史 checkpoint 场景后为 2 / 11。该统计不包含 exit 3。

### Artifact 与 Checker chaos

Artifact Agent 实跑 42 个 chaos scenarios，并对 6 个纠正配置后的场景复跑：

- 缺 `notes.md`、`spec.md`、`tasks.md`、`tests.md`、Plan：5 / 5 正确阻断；
- Plan path/symlink escape、scope mismatch、Story Plan 空 Included Tasks、Story/Task mismatch：全部正确阻断；
- 漏 `tasks/*`、`tests/*`、`plans/*`、`contracts/*` 与 symlink detail：全部正确阻断；
- Gate decision/Auto-Loop 配对、Digest algorithm/format、Feature/fingerprint/timestamp binding：正反例符合预期；
- exact Assessment 重复或分类冲突：结果由最后一行决定，**FAIL**；
- 顶层 Gate 字段重复或冲突：结果由最后一行决定，**FAIL**；
- `no-plan:*` 没有正式 No-Plan Decision 记录：仍得到 `GATE_VALID`，**FAIL**。

## Findings

### Critical-1：重复 Gate 字段可覆盖 Human authorization

`scripts/check-feature-review.py` 的 `parse_fields()` 扫描整个 `notes.md`，普通字典静默采用最后一个同名字段。原始记录是：

```text
Gate 2 Decision: package-only
Feature Auto-Loop: disabled
```

在文件末尾追加：

```text
Gate 2 Decision: approve-and-start
Feature Auto-Loop: enabled
```

再执行：

```bash
python3 scripts/check-feature-review.py --mode execute <temporary-feature-dir>
```

实际得到 exit 0：

```text
GATE_VALID: Feature Gate authorization is valid for mode=execute
```

这不是 AI 语义判断，而是 durable authorization field 的结构歧义。相同问题还会让合法历史 checkpoint 的旧值覆盖当前值，造成反向 false positive。建议所有当前 REQUIRED_FIELDS 只能存在一个无歧义的顶层值；重复/冲突值必须 fail closed，历史记录不得被解析为当前状态。

### High-1：accepted Story 边界从可变 Task ledger 反推

Checker 仅从当前仍存在的 initial Task IDs 提取 Story。唯一 initial Task 被同 Story新 Task 合法替换后，accepted Story 集合变空，脚本错误阻断新 Task。

这与 runtime 允许在 accepted Story/Product Slice/Acceptance 内 split/refine/replace Task 的规则冲突。应持久化独立的 Gate 2 accepted execution boundary，或采用等价的不可由当前 Task ledger 丢失/改写的结构证据；不能只用 mutable current rows 重建历史授权。

同一根因还有一个防御性风险：把 initial Task 的 Story 从 `US1` 改成 `US2` 后，结构检查也会跟着把 `US2` 当作已接受边界。若 AI 错误写 `within-approved-boundary`，当前 Checker 会 pass。语义分类仍由 AI 负责，但现有 Story 检查并不是独立的 accepted-boundary 结构保护。

### High-2：冲突的 exact Drift Assessments 由末行决定

同一 Feature/Gate/baseline/current binding 同时存在 `implementation-boundary-change` 与 `within-approved-boundary` 时，交换两行顺序即可改变 blocked/valid 结果。冲突证据必须 fail closed，不能由 Markdown 行顺序决定 Human Gate 路由。

### High-3：No-Plan 结构证据漏检

`Gate 2 Plan Evidence: no-plan:T001` 只校验 scope 与 Task mode，没有校验 runtime 要求的 notes-level 和 selected Task row/detail No-Plan Decision 是否存在。Task 是否命中 Plan trigger 属于 AI 语义职责；两个决定记录是否存在则属于 Checker 可确定验证的结构职责。

### Medium-1：Workflow checklist 仍把 initial Task set 写成不可变边界

`references/workflow-checklists.md` 的一处规则仍要求 Plan 只能落在 initial accepted Task set 内，与 runtime、同文件较前规则及 `templates/tasks.md` 允许同边界新 Task refinement 的规则冲突，会诱导 User Agent 重复 Gate 2 或主动误阻断。

### Medium-2：Feature 永久取消/放弃缺少明确 disposition

当前生命周期只有 `draft | active | blocked | paused | closed`。Gate 1 前后明确取消 Feature 时，没有非 resumable、非 delivered 的合法落点。是否新增 cancel/abandon 状态属于后续产品决策；本轮只记录缺口，不把 `paused` 或 `closed` 擅自解释为取消。

## Checker 与 AI/runtime 边界

Checker 应负责确定性结构：required Gate fields 唯一性、decision/action pairing、artifact inventory/path、digest/fingerprint binding、Assessment binding 与冲突、Task mode/identity/Story 结构映射、Plan/No-Plan 证据绑定。

AI/runtime 负责语义：真实产品边界、Assessment 分类、Plan trigger 判断、测试与证据真实性、Task 状态迁移、Task Done、Completion 与 Close。Checker 输出 `ASSESSMENT_REQUIRED` 时，Agent 应先自行完成 Semantic Review；不得将其包装成“Human Gate 出错”。

## 实际验证证据

```bash
python3 -m unittest -v tests.test_feature_review
# 39 / 39 PASS

bash tests/validate-feature-construction-two-gate-review.sh
# PASS

python3 -m unittest -v tests.test_python_checker_contract
# 21 / 21 PASS

ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
# PASS

git diff --check
# PASS
```

Markdown fence balance：PASS。额外 chaos fixtures 均在系统临时目录运行；主线程独立复现了 duplicate Gate field bypass、same-Story full replacement false positive 与 mutable Story boundary laundering。

## 五域评分

| Domain | 得分 | 扣分原因 |
|---|---:|---|
| Requirement And Scope Fidelity | 12 / 15 | AI/Checker 分工基本明确；取消语义与 No-Plan 结构边界不完整 |
| Logic, State, And Human Gates | 18 / 30 | 重复字段可绕过执行授权；冲突 Assessment 不 fail closed；合法 replacement 被阻断 |
| Cross-Surface Consistency | 13 / 20 | checklist 与 runtime/template 的新 Task 规则冲突；取消 disposition 未闭环 |
| Pressure Resistance | 16 / 25 | 多数路径/清单/Plan 负控可靠，但 chaos 暴露双向边界错误 |
| Evidence And Maintainability | 8 / 10 | 有真实复现、两条独立测试线和负控；现有 39 tests 未覆盖关键漏洞 |
| **总分** | **67 / 100** | **FRAGILE；Critical hard cap 生效** |

## 修复与复测建议

按 TDD 顺序修复：

1. 重复 REQUIRED_FIELDS 与重复/冲突 exact Assessment 必须 fail closed；
2. 为 Gate 2 accepted Story/Product Slice boundary 提供不依赖当前 Task rows 的持久结构证据，并保留 new Story/Human-gated/missing Plan 负控；
3. 校验 No-Plan 双处决定记录，同时保持 Plan trigger 的语义判断归 AI；
4. 同步修正 checklist 的 initial-set-only 冲突；
5. 单独向人类确认是否需要 Feature cancel/abandon lifecycle，不在修复中自行新增状态；
6. 用本报告的相同 chaos prompts 复测，并重新执行 focused/full validation。

## 工作区与发布状态

本次压力测试未修改实现代码，未清理 `.tmp/` 或 `__pycache__`，未创建目标项目 `.agent-loop/` artifacts。未执行 stage、commit、push、tag、PR、merge、release、publish 或 installed Skill 同步。
