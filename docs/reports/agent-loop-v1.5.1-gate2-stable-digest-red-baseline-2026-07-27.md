# Agent Loop v1.5.1 Gate 2 Stable Digest RED 基线

日期：2026-07-27
分支：`v1.5.1`
基线提交：`32a1d2ae94071e39966c48ff2feec28abdc34b3c`

## 结论

当前 `scripts/check-feature-review.py` 把 Stable Digest 的所有文件按原始字节计算。`tasks.md`、任务详情、`tests.md` 和测试详情在正常执行中更新运行态字段后，`execute` 会错误阻断；当前实现也不要求算法字段，且没有只读 `digest` 模式。

## 真实复现

对目标项目 Feature 只回退 T001 的以下四类运行态字段后重算原始摘要：

- 任务复选框 `[x]` → `[ ]`
- `Status: done` → `Status: todo`
- `Review: pass` → `Review: pending`
- `Drift: no drift` → `Drift: pending`

重算结果与 Gate 2 保存值完全一致：

```text
sha256:89886dad8b1e140dc0b4d6167b0a1b9c0e27ce7b1d043ad8cafe9b16373ebd66
```

这证明误报由任务完成时必须发生的运行态更新触发，不是审核包的产品/实施定义发生漂移。

## RED 命令

```text
python3 tests/test_feature_review.py
```

结果：共 25 个测试，18 通过，7 失败，退出码 1。

预期失败覆盖：

1. v2 根任务账本完成与 Active Plan 轮转；
2. v2 任务详情 Task Done Gate 运行态更新；
3. v2 根测试矩阵结果更新；
4. v2 测试详情状态更新；
5. 缺失 Stable Digest Algorithm 未 fail closed；
6. 未知 Stable Digest Algorithm 未 fail closed；
7. `digest` 只读模式不存在。

关键输出：

```text
FAIL: Gate 2 Stable Digest does not match current stable artifacts
argument --mode: invalid choice: 'digest'
PASS: Feature review evidence is valid for mode=review
```

最后一行分别出现在缺失/未知算法的负向用例中，证明旧 checker 会忽略算法契约。

## 阴性控制

以下契约仍通过：

- 显式 `raw-v1` legacy 基线；
- 任务 ID、Mode、Story 映射、标题变化被阻断；
- 测试定义变化被阻断；
- 既有 package-only / approve-and-start、Plan Scope、Stable Files、Agent-ready 规则。

## GREEN 判定标准

- 25 个 focused 测试全部通过；
- v2 只忽略精确白名单运行态字段，任何定义变化继续阻断；
- 缺失/未知算法 fail closed；
- `digest` 使用同一实现计算且不写文件；
- 不增加 force/bypass 或自动迁移。
