# Agent Loop v1.5.3 轻 Gate Authority Alias RED 基线

日期：2026-07-29
分支：`v1.5.3`
基线 HEAD：`6086d7d6fc758221af2dee41ea269d0acf237795`

## 既有全量基线

- Shell：`47 / 47` 通过。
- Python：`333 / 333` 通过，耗时 `93.121s`。
- 当前工作区存在已批准但未提交的 v1.5.3 修改；本修复没有恢复、删除或覆盖无关 dirty work。

## Focused RED

命令：

```bash
python3 -m unittest \
  tests.test_feature_monthly_archive_scan.FeatureMonthlyArchiveScanTests.test_feature_entry_symlink_is_reported_but_not_planned_as_a_move \
  tests.test_feature_monthly_archive_scan.FeatureMonthlyArchiveScanTests.test_internal_memory_root_alias_keeps_logical_agent_loop_plan_paths \
  tests.test_feature_monthly_archive_apply.FeatureMonthlyArchiveCheckTests.test_apply_rejects_feature_entry_symlink_before_transaction_or_move \
  tests.test_feature_monthly_archive_apply.FeatureMonthlyArchiveCheckTests.test_internal_memory_root_alias_applies_using_logical_plan_paths \
  tests.test_feature_context.FeatureContextCheckerTests.test_internal_memory_root_alias_is_accepted \
  tests.test_lightweight_change_scan.LightweightChangeScanTests.test_internal_memory_root_alias_is_reused_with_logical_paths \
  tests.test_root_agents_blocks.RootAgentsBlocksTests.test_agent_loop_skill_body_drift_is_reported_without_becoming_a_hard_gate
```

结果：`0 / 7` 通过，七个合同均真实 RED：

1. Feature entry symlink 被旧 scanner 直接报 `path-escape`，没有形成轻量事实结果；
2. 内部 memory-root alias 的 plan 路径泄漏为 `.memory/...`；
3. Apply 未在 transaction/move 前拒绝变成 symlink 的 Feature source；
4. alias plan Apply 在写入后因 `.memory/...` locator 失败；
5. Feature Context 把安全内部 alias 一律判为 `BLOCKED`；
6. Lightweight Change 把安全内部 alias 一律判为 invalid；
7. `agent-loop-skill` block 正文被改写后仍输出 `PASS root AGENTS managed blocks are current`。

根检查器用例在修正测试夹具替换文本后单独复跑，确认是产品缺口而非测试构造错误。
