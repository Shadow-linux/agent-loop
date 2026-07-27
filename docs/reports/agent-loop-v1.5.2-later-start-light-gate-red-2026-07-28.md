# Agent Loop v1.5.2 Later Start 轻量 Gate RED 基线

## 审计对象

- 日期：2026-07-28
- 分支：`v1.5.2`
- HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
- 对象：当前 dirty working tree
- 目标：保留 Gate 2 原始评审基线，以独立轻量 transition 记录 package-only 后的 later-start；移除无落点的 Gate 1 Spec SHA；让 focused tests 按 owning section 防止规则掩盖。

## 修复前全量基线

```text
tests/*.sh: 45 / 45 PASS
Python unittest discovery: 312 / 312 PASS
```

上述绿色基线未覆盖本次已确认的跨文件冲突。

## Focused RED

命令：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_feature_review -v
bash tests/validate-feature-construction-two-gate-review.sh
```

结果：

```text
Python: 8 tests, 6 PASS, 2 expected FAIL
- FAIL: later-start 缺少独立 Later Start Decision / Authorized At / Evidence，且 runtime 要求覆盖 Gate 2 baseline
- FAIL: Requirement Checklist 要求 exact current Spec SHA-256，但 notes/runtime 没有落点

Shell: expected FAIL
- Human Gate Modes 缺少 Later Start Decision
```

额外 mutation contract 已在 RED 阶段证明：测试可按 owning H2 section 定位关键规则，删除 Feature Auto-Loop Git/release stop 或在 Analyze Consistency 引入相反 accepted 规则时会失败，不再由其他章节的重复正确文本掩盖。

## 约束

- 不恢复 `scripts/check-feature-review.py`。
- 不增加 digest、Stable Digest、`EVIDENCE_*` 或本地 Feature Gate preflight。
- 不增加 canonical stage、Human Gate 或新 artifact。
- Gate 2 原始决定保持 durable review baseline；live mode 继续由 project `Gate Mode` 管理。
- 本报告是维护验证证据，不是下游运行权威。
