# Agent Loop v1.5.3 Feature Archive Soft Gate RED 基线

## 审计边界

- 日期：2026-07-28
- 分支：v1.5.3
- 基线 HEAD：6086d7d6fc758221af2dee41ea269d0acf237795
- 审计对象：Feature Monthly Archive / Rehydrate Scanner、Check、Apply 的 reference finding 授权边界
- 目标设计：Scanner 只收集事实和生成 exact plan；Agent 判断是否继续；人类授权最终计划；执行器保持 transaction、rollback 和项目写边界。

## 修改前全量基线

- Shell：46 / 46 PASS，9 秒
- Python：320 / 320 PASS，85.399 秒（外层计时 86 秒）
- 修改前业务代码：无 tracked diff
- 既有未跟踪缓存：.tmp/、scripts/__pycache__/、tests/__pycache__/
- 本轮新增但尚未实现：Proposal 与 Implementation Plan

## 当前缺口

当前 scripts/feature_archive_support.py 在全仓 Markdown 引用扫描时：

1. 发现任何 symlinked directory 就抛出 path-escape；
2. 发现 symlinked Markdown 就抛出 path-escape；
3. validate_archive_plan_state 发现 classification 为 unsupported 的 skipped reference 就抛出 reference-impact。

因此 Scanner/Checker 会替 Agent决定 Archive/Rehydrate 不能继续，无法形成包含客观 finding 的可审查计划。

## 预期 RED

专项测试必须证明：

- .claude -> .agents 使当前 Scanner 以 path-escape 失败；
- unsupported reference 使当前 Check/Apply 以 reference-impact 失败；
- runtime/design/Human Review 尚未声明“finding 是证据而非 Checker 授权”。

完成专项测试后追加实际命令、失败测试名和失败输出摘要。

## 实际 RED 证据

执行：

```bash
python3 -m unittest tests.test_feature_monthly_archive_scan.FeatureMonthlyArchiveScanTests.test_internal_directory_symlink_is_reported_without_blocking_or_traversal
python3 -m unittest tests.test_feature_monthly_archive_apply.FeatureMonthlyArchiveCheckTests.test_unsupported_reference_is_advisory_for_exact_plan_apply
bash tests/validate-feature-archive-soft-gate.sh
```

结果：3 / 3 按目标原因失败。

- symlink RED：exit 1，`path-escape: symlinked directory cannot be reference-scanned: .claude`；
- advisory apply RED：exit 1，`reference-impact: unsupported references block apply: docs/ambiguous.md`；
- cross-surface RED：exit 1，`references/design.md` 缺少 `reference findings are evidence, not Checker authorization`。

这三个失败分别证明 Scanner、Check/Apply 授权路径和发布规则面都尚未实现目标能力，不是测试拼写、环境或 fixture 错误。

## GREEN 闭环

实现后相同场景均已转为 PASS，并扩展为 internal/external/broken/cyclic/file symlink、advisory apply、symlink retarget stale-plan 和 project-boundary negative control。

- Focused：61 / 61 Python PASS，soft-gate Shell contract PASS；
- Mutation：旧 symlink exception、`unsupported` rejection、移除 project confinement 三项 mutation 均使对应测试重新转 RED；
- Full：47 / 47 Shell PASS，327 / 327 Python PASS；
- 完整结论：`docs/reports/agent-loop-v1.5.3-full-validation-2026-07-28.md`。
