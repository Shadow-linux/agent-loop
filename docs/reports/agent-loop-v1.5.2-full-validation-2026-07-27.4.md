# Agent Loop v1.5.2 全量验证报告（Stable Digest 单职责 Checker）

日期：2026-07-27
分支：`v1.5.2`
HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
审计对象：当前完整未提交工作区；包含此前已批准的 v1.5.2 修改及本轮 Task 13

## 总结

总分：**99 / 100 — STRONG**
当前发现：Critical 0 / High 0 / Medium 0 / Low 1。
结论：Feature Checker 已从多职责 Gate 解析器收敛为单一 Stable digest 重算器；两个 Human Gate、Agent 语义责任和全部独立授权边界保持闭环。

## RED / GREEN

- RED：`tests.test_feature_review` 共 29 tests，产生 14 个预期失败记录，证明旧 Checker 仍判断动作配对、时间、manifest coverage、Plan exclusion 与非投影 v2 UTF-8。
- GREEN：Checker focused + Python checker contract `50 / 50 PASS`。
- 单职责压力集：`7 / 7 PASS`。
- 双 Gate focused Shell contract：PASS。

## 全量回归

| 检查 | 结果 |
|---|---|
| 全部 `tests/*.sh` | `45 / 45 PASS` |
| Python unittest discovery | `338 / 338 PASS` |
| `SKILL.md` YAML | PASS |
| `plugin.json` JSON | PASS |
| Shell syntax | `46 / 46 PASS` |
| Ruby syntax | `5 / 5 PASS` |
| Python AST | `47 / 47 PASS` |
| Markdown fence | `321 / 321 PASS` |
| `git diff --check` | PASS |

## 六域语义审计

| Domain | Score | Result | 证据结论 |
|---|---:|---|---|
| Logic Correctness | 100 | PASS | Checker 单一职责；Gate 与 Agent 语义无循环授权 |
| Autonomy | 100 | PASS | Agent 可自行处理清单、任务和边界变化，不被脚本误判绑架 |
| Project Entry / Onboarding | 100 | PASS | 本轮未改变入口与 onboarding 所有权，相关全量合同通过 |
| Development / Test Workflow | 100 | PASS | Gate 1/2、Plan、TDD、Task Done、Pause/Resume/Close 保持 |
| Memory | 100 | PASS | durable Gate pair 与 live Gate Mode 分离未回退 |
| Recommendation | 94 | PASS | 唯一下一步清楚；兼容 mode 名仍有轻微误解风险 |

加权总分：99。

## 关键压力场景

- `package-only`、`approve-and-start`、矛盾 action/time 字段不会改变 Checker digest 结论；Agent 必须单独停止错误动作。
- 缺少根文件、遗漏 triggered detail、错误 Package-to-Stable closure 或把 Plan 放入 Stable 不再由 Checker判断；Agent 合同和 validation scenarios 继续硬停止这些问题。
- Stable 文件缺失、危险相对路径、symlink、same-file alias、非普通文件、非法算法或 digest 格式仍返回 `EVIDENCE_INVALID`，仅保护 Checker 自己的安全确定读取。
- Stable bytes 改变返回 `EVIDENCE_CHANGED`，由 AI Semantic Review 分类，不自动打回 Human Gate。
- legacy `review-definition-v2` 只投影 Task/Test runtime ledger，其他命名文件按原始字节哈希；非 UTF-8 二进制证据不再误报。
- `review | start | execute` 与 canonical `check` 完全同路，不产生阶段授权。

## 剩余风险

Low：三个旧 mode 名仅为兼容保留，可能让未读取新版 runtime 的旧 Agent误解其含义。没有当前 Critical、High 或 Medium。

## 范围与 Git 状态

- 未新增 canonical stage、message intent、lifecycle、Gate、artifact 或依赖。
- 未创建目标项目 `.agent-loop/`。
- 未派发新 Subagent；本轮实现与验证由主 Agent完成。
- 未 stage、commit、push、tag、PR、merge、release、publish 或同步 installed Skill。
