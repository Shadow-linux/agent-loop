# Agent Loop v1.5.2 Feature Checker 移除 RED 基线

- 日期：2026-07-27
- 分支：`v1.5.2`
- HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
- 范围：移除 Feature Gate 的 `check-feature-review.py`、Feature Gate digest 字段与 `EVIDENCE_*` 路由；保留两次 Human Review、Agent 语义检查和所有独立 Human Gates。

## RED 命令

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_feature_review -v
```

## RED 结果

```text
Ran 5 tests in 0.024s
FAILED (failures=60)
```

失败与预期缺口一致：

- `scripts/check-feature-review.py` 仍存在；
- 当前运行权威、模板和人类文档仍引用 Feature Gate digest、`EVIDENCE_MATCH | EVIDENCE_CHANGED | EVIDENCE_INVALID` 或 `review-definition-v2`；
- Gate 2 的 `Revise package` / `Pause` 尚未在所有表面明确禁止写成 readiness `accepted`；
- package-only 后的 later-start 仍强制调用本地 Feature Checker。

该 RED 基线在任何 GREEN 实现修改前保存。
