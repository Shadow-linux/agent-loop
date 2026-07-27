# Agent Loop v1.5.2 Feature Gate 混沌修复 RED 基线

日期：2026-07-27
分支：`v1.5.2`
基线 HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
范围：重复当前 Gate 字段、重复/冲突 exact Assessment、全部初始 Task 同 Story 替换、accepted Story snapshot、No-Plan 双处结构记录、旧 Feature 迁移、Task history 污染、Gate 2 durable-field 绑定、路径与列表歧义

## RED 命令

```bash
python3 -m unittest -v \
  tests.test_feature_review.FeatureReviewCheckerTests.test_duplicate_current_gate_field_is_gate_blocked \
  tests.test_feature_review.FeatureReviewCheckerTests.test_same_value_duplicate_current_field_is_gate_blocked \
  tests.test_feature_review.FeatureReviewCheckerTests.test_historical_gate_field_does_not_override_current_authorization \
  tests.test_feature_review.FeatureReviewCheckerTests.test_duplicate_exact_assessment_binding_is_gate_blocked \
  tests.test_feature_review.FeatureReviewCheckerTests.test_conflicting_exact_assessment_binding_is_gate_blocked \
  tests.test_feature_review.FeatureReviewCheckerTests.test_all_initial_tasks_may_be_replaced_inside_accepted_story \
  tests.test_feature_review.FeatureReviewCheckerTests.test_review_rejects_accepted_story_snapshot_not_derived_from_reviewed_tasks \
  tests.test_feature_review.FeatureReviewCheckerTests.test_no_plan_requires_notes_and_task_decision_records \
  tests.test_feature_review.FeatureReviewCheckerTests.test_no_plan_with_both_structural_decisions_is_valid
```

实际结果：**9 tests / 9 failures**，exit 1。

## 真实缺口

| RED | 修复前实际行为 |
|---|---|
| 冲突 Gate 2 Decision | 末值覆盖，只因 Auto-Loop 配对不符才阻断，没有识别重复字段 |
| 同值 Gate 2 Reviewed At 重复 | exit 0 `GATE_VALID` |
| history section 包含旧 Gate 2 Decision | 历史值覆盖当前值并误阻断 execute |
| 相同 exact Assessment 重复 | exit 0 `GATE_VALID` |
| 相同 binding 分类冲突 | 最后一行 `within-approved-boundary` 使 exit 0 |
| 全部 initial Task 被同 Story新 Task 替换 | exit 1，错误报告无法映射 accepted Story |
| Gate 2 Accepted Stories 与 review Task 映射不一致 | exit 0，没有 snapshot 契约 |
| `no-plan:T001` 缺 notes/Task决定记录 | exit 0 `GATE_VALID` |
| 完整 No-Plan 正控 | 因测试后置写入触发真实 Stable Drift，证明 fixture 必须在 Gate 2 baseline 前建立；纠正 fixture 后作为 GREEN 正控 |

## RED 有效性

- 所有 fixture 位于系统临时目录；未创建目标项目 `.agent-loop/` artifacts。
- 失败来自已知缺失行为，不是 Python、路径、导入或语法错误。
- 正控 fixture 的 No-Plan 记录改为在 baseline 计算前建立，避免把真实定义漂移误当目标缺陷。
- 本报告记录实现前证据；后续 GREEN 不覆盖此基线。

## 补充 RED：旧 Feature 迁移兼容

新增：

```text
test_legacy_missing_story_snapshot_routes_to_ai_backfill_when_intact
test_legacy_missing_story_snapshot_cannot_be_guessed_after_task_drift
```

实际结果：**2 tests / 2 failures**。旧 Feature 缺少新 snapshot 时，Checker 不能区分“证据完整、可事实回填”和“已经漂移、不可安全推断”，会制造不必要阻断或失去保守边界。该 RED 推动 `ASSESSMENT_REQUIRED` 事实回填与 drift 后 `GATE_BLOCKED` 两条迁移路径分离。

## 第二轮 RED：修复后双子 Agent 混沌复测

主 Agent 独立复现两个只读子 Agent 的发现后，新增以下 10 个 focused tests：

```text
test_duplicate_task_mode_cannot_upgrade_human_gated_task
test_historical_task_mode_cannot_override_current_human_gate
test_historical_story_mapping_cannot_attach_to_current_task
test_historical_no_plan_decision_cannot_satisfy_current_task
test_authorization_digest_blocks_manual_package_only_upgrade
test_authorization_digest_binds_accepted_story_snapshot
test_authorization_digest_binds_initial_agent_ready_tasks
test_notes_symlink_outside_feature_is_gate_blocked
test_normalized_duplicate_package_path_is_gate_blocked
test_duplicate_initial_task_id_in_gate_field_is_gate_blocked
```

组合命令第一次实际结果为 **10 tests / 9 failures**；唯一未失败的 No-Plan 场景经检查发现 fixture 中仍有后续 `T002`，历史字段附着到了错误 Task。纠正为单 Task fixture 后单独运行，实际 **1 test / 1 failure**。因此第二轮是 **10 个真实 RED / 10 个缺口**，不是测试装配错误。

修复前行为：

| 缺口 | 修复前实际行为 |
|---|---|
| 当前 `Human-gated` 后重复 `Mode: Agent-ready` | exit 0，Human Gate 被 last-write-wins 绕过 |
| 后续 history section 的 Mode/Story/No-Plan | 被附着到前一 Task 并参与当前授权 |
| package-only 手改为 approve-and-start/enabled | exit 0，没有 durable-field 绑定 |
| 改写 Accepted Stories 或初始 Task 列表 | 可配合当前 Plan/Assessment 绕过原 snapshot |
| 外部 `notes.md` symlink | 被作为 Gate 授权源读取 |
| `spec.md` 与 `./spec.md`、重复 Task ID | 被静默集合化或按不同字符串接受 |

累计保存 RED：第一轮 9 + 迁移 2 + 第二轮 10 = **21 个真实缺口测试**。

## 第三轮 RED：本地 Human provenance 不可判定

最终制品 chaos 证明：同一 Agent 同时可写 `notes.md` 并调用本地授权摘要计算器时，可以把 accepted package-only 状态回拨成 `review-ready + pending`，再由 `authorize-review` 生成新的候选。该结果不是摘要算法实现错误，而是“声明者、证据写入者与本地发行器为同一主体”的信任边界冲突。

人类明确选择轻量方案后，新增两个 focused RED：

```text
test_lightweight_gate_accepts_human_recorded_start_without_local_authorization_digest
test_lightweight_gate_checker_exposes_no_local_authorization_issuer
```

修复前实际结果：**2 tests / 2 failures**。

```text
expected returncode 0, got 3:
ASSESSMENT_REQUIRED: legacy Gate 2 evidence may backfill Gate 2 Authorization Digest ...

expected returncode 2, got 1:
GATE_BLOCKED: authorize-review requires Implementation Readiness review-ready
GATE_BLOCKED: authorize-review requires Gate 2 Authorization Digest pending
```

这两个 RED 分别证明：正常守规 Agent 会被缺少本地摘要误阻断，以及 Checker 暴露了可由同一 Agent 调用的授权发行入口。

## 第三轮 GREEN

- 移除 `gate2-authorization-v1`、`authorize-review`、`authorize-start` 和模板授权摘要字段；
- Agent 从可靠会话或保留的人类决定证据判断 Human provenance；
- Checker 只保留 `digest | review | start | execute`，其中 `start` 是 package-only 的只读结构/漂移预检；
- later-start 在可靠 Human 指令后记录 approve-and-start/enabled/time，再要求 `execute`；
- focused RED 转为 **2 / 2 PASS**；完整 Feature checker 为 **62 / 62 PASS**；双 Gate Shell contract 与 Python checker contract 均 PASS。

历史 21 个 RED 的授权摘要专用断言按维护者确认的轻量信任边界被替换，不把已明确接受的“恶意 AI 可改全部本地字段”重新定义为 Checker 缺陷。重复字段、历史污染、Story/Task/Plan/No-Plan、路径与列表歧义的结构回归继续保留。

## 第四轮 RED：第二轮 chaos 后收敛 Checker 职责

第二组只读 chaos 测试进一步证明：即使移除本地授权发行器，只要 Checker 继续解析 Task、Plan、Assessment 和 Markdown table，就会不断出现与真实 Gate 无关的假阳性/假阴性。主 Agent 独立复现后先新增 6 个 focused RED：

```text
test_valid_review_reports_evidence_match_not_gate_authorization
test_digest_drift_reports_evidence_changed_for_agent_review
test_checker_does_not_interpret_task_plan_or_assessment_semantics
test_digest_rejects_manifest_that_omits_triggered_detail
test_parent_symlink_and_resolved_alias_are_evidence_invalid
test_fenced_gate_fields_do_not_count_as_current_evidence
```

实际命令结果：**6 tests / 6 failures**，exit 1。失败证据分别为：

- 正常路径输出 `GATE_VALID`，错误暗示 Checker 可以判断授权；
- digest 变化输出 `ASSESSMENT_REQUIRED` 而不是纯证据状态；
- escaped-pipe Assessment table 被解析并硬阻断；
- `--mode digest` 在漏掉已触发 Task detail 时仍输出摘要；
- 父目录 symlink 与同一 resolved target 的两个路径仍能生成摘要；
- fenced example 中的 Gate fields 被当作当前字段。

随后补充 `digest` 必须输出可复制 `Gate 1 Spec Digest` 的第 7 个 RED；修复前为 **1 test / 1 failure**。

## 第四轮 GREEN

- Checker 结果收敛为 `EVIDENCE_MATCH | EVIDENCE_CHANGED | EVIDENCE_INVALID`；
- 移除 Task/Story/Plan/No-Plan/Assessment 语义解析，保留为 Agent-owned workflow evidence；
- `digest | review | start | execute` 统一验证完整 manifest、必需根文件、触发明细覆盖、规范路径、重复、symlink component、resolved-target alias、常规文件与 Feature-root containment；
- 新 evidence 默认 `raw-v1`，显式 legacy `review-definition-v2` 只保留 reader compatibility；
- `digest` 只读输出 Gate 1、Gate 2 Package 与 Stable 三个当前摘要；
- focused Feature checker：**24 / 24 PASS**；相关 Python checker contract：**21 / 21 PASS**；双 Gate Shell contract：PASS；
- 全量 Shell：**45 / 45 PASS**；全量 Python：**333 / 333 PASS**。

第四轮不再把恶意 AI 改写 accepted evidence 视为脚本可解决的问题，也不让 Checker 通过解析更多 Markdown 假装拥有产品语义判断能力。

## 第五轮 RED：第三轮 chaos 的确定性证据边界

人类再次授权两个只读子 Agent 后，主 Agent 对第三轮发现逐条复现，并在修改 Checker 前新增 6 个 focused regression：

```text
test_stable_manifest_covers_every_non_plan_package_file
test_non_utf8_notes_are_reported_as_invalid_evidence
test_empty_manifest_items_are_invalid_instead_of_silently_removed
test_same_file_alias_is_invalid_even_when_path_spelling_differs
test_invalid_fence_closing_line_cannot_expose_current_fields
test_windows_drive_absolute_path_is_invalid_on_every_host
```

实际命令：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_feature_review
PYTHONDONTWRITEBYTECODE=1 bash tests/validate-feature-construction-two-gate-review.sh
```

实际结果：Python **30 tests / 6 failures**；Shell contract 在 `raw-v1` legacy 冲突断言处失败。六个 Python failure 均来自目标缺口：Stable 漏 `extra.md` 仍输出 digest、非法 UTF-8 traceback、空 manifest item 被删除、同 inode/大小写别名通过、非法 fence closing 暴露字段、macOS 将 `C:/spec.md` 当相对路径。

文档 RED 同时覆盖：

- `references/artifact-rules.md` 把当前默认 `raw-v1` 又称作 legacy；
- Pause 要清除 Auto-Loop grant，但没有说明 durable Gate 2 pair 与 live project `Gate Mode` 的分工；
- `references/document-templates.md` 的 inline notes 模板缺少 `Gate Drift Assessments`。

GREEN 后，focused Feature checker + Python checker contract 为 **51 / 51 PASS**，Two-Gate Shell contract PASS；证据 chaos **79 / 79 PASS**，生命周期 executable chaos **31 / 31 PASS**。

GREEN 日志又暴露非法 UTF-8 会附带 11 条缺字段噪音，因此先收紧一个回归断言，实际 **1 / 1 RED**（12 条 `EVIDENCE_INVALID`，期望 1 条），再让解析错误短路为单条确定性诊断。该微循环未扩大 Checker 职责。
