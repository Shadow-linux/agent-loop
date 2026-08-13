# Agent Loop v1.5.5 Nested Product Definition RED 基线

- 日期：2026-08-13
- 分支：`v1.5.5`
- 基线 HEAD：`aad3bd8ceadfa0980439e64d4057b779801ad022`
- 原始 `scripts/check-feature-context.py` SHA-256：`a98018fa127713bb810be01033364eb835d0ccc75202ce628fcae2a9b1c67898`
- 视角：Agent Loop Skill 源码仓库维护者；临时目标项目 fixture 仅位于 `/tmp/`

## 复现

Requirement README 指向 Requirement 内嵌套的 `design-package/product.md`。Feature 的 `Product Requirement Source` 按 Product Definition Checker 的既有契约记录 basename `product.md`，Feature Context Snapshot 记录完整 resolved path。

```text
.agent-loop/requirements/<id>/README.md
.agent-loop/requirements/<id>/design-package/product.md
.agent-loop/features/<id>/spec.md
```

两个官方 Checker 在相同事实上的结果：

```text
PASS: confirmed standard product definition is valid
CHANGED: Product Requirement Source Effective Product Definition is invalid cached evidence: Product Requirement Source Product Definition escapes accepted boundary
```

根因是 `check-feature-context.py` 把 `Effective Product Definition: product.md` 先按项目根解析为 `<project-root>/product.md`，再检查它是否位于 Requirement boundary。它没有复用已经通过 Requirement README 解析、约束并确认的 `source.path`。

## Focused RED

命令：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_feature_context.FeatureContextCheckerTests.test_nested_effective_product_basename_is_current \
  tests.test_feature_context.FeatureContextCheckerTests.test_nested_effective_product_wrong_basename_is_advisory \
  tests.test_feature_context.FeatureContextCheckerTests.test_nested_effective_product_escape_is_advisory -v
```

结果：`3` 个测试中 `1` 个按预期失败，两个负向控制通过。

```text
FAIL: test_nested_effective_product_basename_is_current
AssertionError: 'CURRENT:' not found in
'CHANGED: Product Requirement Source Effective Product Definition is invalid cached evidence: Product Requirement Source Product Definition escapes accepted boundary'
```

完整 `tests.test_feature_context` 为 `37` 个测试，其中只有新增的合法嵌套 basename 场景失败。错误 basename 和 `../../outside/product.md` 仍返回 `CHANGED / 0`。

## 目标修复边界

- 纯 basename 且等于已确认 `source.path.name` 时，复用 `source.path`。
- 错误 basename 继续 `CHANGED`。
- 显式项目相对路径继续按原路径规则解析并执行 Requirement/project boundary 检查。
- 越界路径继续 `CHANGED`，不放宽物理 authority、memory-root、Requirement 或 Product Definition 安全检查。
