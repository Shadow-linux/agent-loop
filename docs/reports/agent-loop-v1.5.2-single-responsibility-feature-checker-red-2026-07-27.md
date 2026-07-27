# Agent Loop v1.5.2 Feature Checker 单职责 RED

日期：2026-07-27
分支：`v1.5.2`
审计对象：当前未提交工作区
目标：证明旧 Checker 仍把 Stable digest 以外的 Gate、时间、清单完整性和 v2 解码规则当作脚本职责。

## RED 命令

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_feature_review
```

实际结果：`Ran 29 tests`，`FAILED (failures=14)`。

代表性失败：

- `--mode check` 不存在；
- package-only baseline 在 `execute` 被 Checker 判为 invalid；
- Gate decision / Auto-Loop / review time 会改变 Checker 结论；
- 缺少必需根、triggered detail、Package-to-Stable closure 或 Plan exclusion 会由 Checker 阻断；
- `review-definition-v2` 会把非 Task/Test 文件错误按 UTF-8 解码。

这些失败证明现有实现没有满足人类确认的单一职责边界。完整终端输出保留在本次会话证据中。

## GREEN 目标

Checker 只读取 `Gate 2 Stable Files`、`Gate 2 Stable Digest Algorithm` 和 `Gate 2 Stable Digest`，安全重算该摘要。其他全部由 Agent 核对。`review | start | execute` 只能是 `check` 的兼容别名，不能含不同 Gate 逻辑。
