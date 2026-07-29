# Agent Loop v1.5.3 Feature Context 事实扫描软 Gate RED 基线

## 审计对象

- 日期：2026-07-28
- 分支：`v1.5.3`
- HEAD：`6086d7d6fc758221af2dee41ea269d0acf237795`
- 对象：包含已批准但未提交的 Feature Archive soft-gate 工作区，尚未修改 Feature Context checker 实现
- Proposal：`docs/proposal/v1.5.x/feature-context-fact-scan-soft-gate.md`
- Implementation Plan：`docs/proposal/v1.5.x/feature-context-fact-scan-soft-gate-implementation-plan.md`

## 既有全量机械基线

命令：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
```

结果：

- Shell：`47 / 47 PASS`
- Python：`327 / 327 PASS`
- 结论：本轮 RED 之前的组合工作区机械基线为 GREEN。

第一次 Shell 汇总命令使用了 zsh 只读变量名 `status`，命令在测试执行前退出；改用 `rc` 后完整重跑并获得以上基线。该命令错误不是仓库测试失败。

## Focused RED

命令：

```bash
python3 -m unittest tests.test_feature_context
bash tests/validate-feature-context-load-contract.sh
```

结果：

- Python Feature Context：`27` 项，`15` 项按新契约失败，`12` 项通过；退出 `1`。
- Shell contract：失败；`templates/spec.md` 仍缺少 `Freshness: current | changed | blocked`。

代表性 RED：

| 场景 | 期望 | 当前结果 |
|---|---|---|
| Product 仅追加 editorial 内容 | `CHANGED / 0` | `REFRESH_REQUIRED / 3` |
| ADR 仅追加 editorial 内容 | `CHANGED / 0` | `REFRESH_REQUIRED / 3` |
| Snapshot 缺失或字段不全 | `CHANGED / 0` | `REFRESH_REQUIRED / 3` |
| `Verified At` 缓存格式异常 | `CHANGED / 0` | `REFRESH_REQUIRED / 3` |
| Requirement lifecycle 为 `deferred` | `CHANGED / 0`，由 Agent 路由 | `BLOCKED / 1` |
| Product Review 未确认 | `CHANGED / 0`，由 Agent 路由 | `BLOCKED / 1` |
| Product Slice ID/anchor 未解析 | `CHANGED / 0`，由 Agent 判断影响 | `BLOCKED / 1` |
| ADR `review-required` | `CHANGED / 0`，由 Agent 返回 Decision & Design | `BLOCKED / 1` |
| Feature 缓存指针/profile/decision 集合不一致 | `CHANGED / 0` | `BLOCKED / 1` |

完整失败摘要：

```text
Ran 27 tests in 1.293s
FAILED (failures=15)
FAIL: templates/spec.md missing required text: Freshness: current | changed | blocked
```

## 已通过的物理负例

RED 运行中，下列旧有/新增物理边界继续通过：

- Requirement/Feature 路径逃逸仍被拒绝；
- Requirement README 缺失仍被拒绝；
- Requirement README 同时存在两个 effective pointer 仍被拒绝；
- ADR 文件缺失仍被拒绝；
- ADR 路径逃逸仍被拒绝；
- memory root symlink 仍被拒绝；
- checker 运行前后目标文件快照一致，保持只读。

## RED 结论

当前缺口已被真实证明：Checker 同时承担事实采集和工作流裁决，导致可由 Agent 评估的 changed facts 直接形成非零硬停止。下一步只修改 checker 分类/退出契约及协调运行规则，不放松项目边界、唯一 authority、文件存在性或现有 Human Gates。
