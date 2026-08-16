# Agent Loop v1.5.7 Progressive Verification + Proof First RED 基线

日期：2026-08-16
分支：alpha/v1.5.7
基线提交（实施前父提交）：e043d69 `docs(v1.5.7): 新增 Progressive Verification + Proof First 提案`

## 目标

证明 `tests/validate-progressive-verification.sh` 契约测试在 v1.5.7 实施前的源码上真实失败（非恒真断言），从而保证 GREEN 结果由本次实施产生，而不是测试本身失效。

## RED 命令

```text
git worktree add /tmp/al-red-e043d69 e043d69
cp tests/validate-progressive-verification.sh /tmp/al-red-e043d69/tests/
cd /tmp/al-red-e043d69 && bash tests/validate-progressive-verification.sh
```

## RED 输出（存档）

```text
FAIL: references/runtime.md missing Progressive Verification contract: focused | full | high-assurance
exit=1
```

测试在第一条核心断言（runtime.md 必须存在三档契约）即失败并停止——实施前源码不包含任何 Profile 契约，符合预期 RED。

## GREEN 对照

当前 alpha/v1.5.7 HEAD 上同一测试通过：

```text
PASS: Progressive Verification + Proof First contract is complete
（含沙箱对照组 + 15 个语义变异全部被捕获）
```

## 历史说明

本基线为实施后补建（测试编写于实现之后，属 GREEN-first 流程偏差，已在全量验证报告中记录）；补建方式为标准 worktree 回放，证据等价。本轮及后续新增断言（升档重绑、legacy 兼容、跨面锚点、反语义）均在变异段有对应 RED 证明：每个变异在沙箱中真实制造了测试失败后才被接受。

## 结论

RED 基线成立：契约测试对实施前源码失败、对实施后源码通过，且 15 个语义变异全部可被捕获。
