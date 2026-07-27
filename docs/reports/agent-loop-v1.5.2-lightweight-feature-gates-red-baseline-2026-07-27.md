# Agent Loop v1.5.2 轻量 Feature Gate RED 基线

日期：2026-07-27
分支：`v1.5.2`
基线 HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`（`stable-v1.5.1`）
审计对象：当前工作区；仅新增 Proposal、Implementation Plan、RED tests 与本报告后运行 RED，未修改生产 Checker/runtime。

## 工作区保护边界

以下内容在实施前已存在或不属于 Feature Gate 实现，本轮不恢复、不清理、不覆盖：

- `AGENTS.md` 的 stable tag 规范修改；
- `.tmp/`；
- `scripts/__pycache__/`；
- `tests/__pycache__/`。

## Task 0 现有基线

### Shell

命令：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
```

实时数量：45。

结果：43 PASS / 2 FAIL。

两项既有失败：

```text
tests/validate-lightweight-change-lane.sh
FAIL: CHANGELOG.md missing Lightweight Change contract: ## 1.5.1 — 2026-07-25

tests/validate-requirement-lifecycle-backlog.sh
FAIL: expected '## 1.5.1 — 2026-07-25' in CHANGELOG.md
```

实际 `CHANGELOG.md` 已使用 `## 1.5.1 — 2026-07-27`。这是旧测试日期硬编码，与本次 Gate 逻辑无关；v1.5.2 版本同步时单独校准，不将其伪装成本轮引入的回归。

### Python

命令：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

结果：335 tests，全部通过，耗时 84.605s。

### Focused pre-RED

命令：

```bash
python3 tests/test_feature_review.py
```

结果：27 tests，全部通过。

## Task 1 RED

先新增 8 个 focused behavior tests，使总数从 27 增加到 35；生产 Checker 未修改。

命令：

```bash
python3 tests/test_feature_review.py
```

结果：35 tests，10 failures；失败均由已批准的新行为尚不存在造成。

### RED-1：Gate 1 证据变化仍被当作普通失败

```text
expected returncode 3, got 1
FAIL: Gate 1 Spec Digest does not match spec.md
```

证明当前 Checker 无法输出 `ASSESSMENT_REQUIRED`，也不会消费 exact `within-approved-boundary` Assessment。

### RED-2：Gate 2 漂移没有 AI 评估路由

```text
expected returncode 3, got 1
FAIL: Gate 2 Stable Digest does not match current stable artifacts
```

错误 Feature ID、baseline/current fingerprint 的 Assessment 目前都无法被区分，因为 Checker 尚无 Assessment contract。

### RED-3：初始 Task ID 集仍是绝对白名单

```text
FAIL: Active Plan Scope is outside accepted Agent-ready task set
FAIL: Gate 2 Stable Digest does not match current stable artifacts
```

证明 `T003 [US1]` 即使明确 `Derived From: T001`、映射原 Story 且已有 exact Assessment，当前仍被硬阻断。

### RED-4：硬阻断与待评估变化共用 `FAIL`

```text
expected GATE_BLOCKED
got FAIL: missing field: Gate 1 Decision
```

证明 Checker 不能向 Controller 区分 Gate 授权无效与需要 AI 语义评估。

### Shell contract RED

命令：

```bash
bash tests/validate-feature-construction-two-gate-review.sh
```

结果：FAIL。

```text
FAIL: references/runtime.md missing required text: GATE_VALID
```

这证明 runtime/design/templates 尚未协调声明 typed Checker outcomes、AI boundary assessment 和“新增 Task ID 不自动重新 Gate 2”。

## RED 结论

RED 有效，且命中 Proposal 所定义的真实缺口：

1. 当前 Digest mismatch 被直接当成 Gate failure；
2. 当前 Checker 不能区分 `ASSESSMENT_REQUIRED` 与 `GATE_BLOCKED`；
3. 当前 Gate 2 把初始 Task ID 集当作不可变化白名单；
4. 当前不存在 Feature/Gate/fingerprint 绑定的 AI Assessment；
5. 现有缺口不是通过增加模板关键词即可修复，必须修改 Checker、runtime/design、Human Review、templates、scenarios 和 tests。

## GREEN Follow-up

以上 RED 原文保持不变。实现完成后的同一 focused suite 新增了边界分类、malformed Assessment、`Derived From` 越界和 digest fingerprint 输出回归，共 39 tests。

命令：

```bash
python3 tests/test_feature_review.py -v
bash tests/validate-feature-construction-two-gate-review.sh
python3 -m unittest tests.test_python_checker_contract -v
```

结果：

- Feature checker：39 / 39 PASS；
- two-gate Shell contract：1 / 1 PASS；
- Python checker contract：21 / 21 PASS。

额外 RED → GREEN：自查发现 `Derived From: T001` 可让 `T003 [US2]` 绕过 accepted Story 映射。新增 `test_derived_from_cannot_smuggle_a_new_story_boundary` 后先得到 `expected 1, got 0 / GATE_VALID`，再把 `Derived From` 收敛为追溯证据、要求独立 accepted Story 映射，单测与 39 项 focused suite 全部转绿。

最终行为：

1. 未评估变化稳定返回 exit `3` / `ASSESSMENT_REQUIRED`；
2. exact current `within-approved-boundary` 返回 `GATE_VALID`；
3. 缺 Gate、错误授权、malformed Assessment、Human-gated Task 与越界 Story 返回 `GATE_BLOCKED`；
4. `--mode digest` 保持只读并输出 Gate 1 与 Gate 2 review/start/execute baseline/current fingerprints；
5. 初始 Task IDs 不再是永久白名单，但新增 Task 仍须真实存在、Agent-ready、映射 accepted Story、通过 Plan 绑定和 exact current Assessment。
