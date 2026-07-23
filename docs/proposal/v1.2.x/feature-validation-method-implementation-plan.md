# Single-Feature Validation Method Implementation Plan

> **For agentic workers:** implement inline with TDD; do not create downstream `.agent-loop/` artifacts.

**Goal:** 固化一个可复用的单功能逻辑与压力测试百分制，并用它重新评价 Project-Local Skills。

**Architecture:** 维护规则放在 `docs/maintenance/`，仓库入口放在 `AGENTS.md`，契约测试放在 `tests/`，具体评分报告放在 `docs/reports/`。该方法不进入下游运行时 `references/`，也不替代控制面变更触发的全量验证。

**Tech Stack:** Markdown、Bash contract test、隔离 Agent 压力场景。

## Tasks

- [x] RED：新增方法契约和 Local Skills 漏洞回归断言，确认因规则缺失而失败。
- [x] GREEN：新增五域评分方法、AGENTS 入口和单功能报告。
- [x] REFACTOR：修复 legacy root、helper 数量和 manifest guidance 的 review 漂移。
- [x] VERIFY：只运行 feature-validation contract、Project-Local Skills 专项及直接相关 root/routing 测试。
- [ ] SUBMIT：更新提交清单和报告证据，等待最终 commit 确认。
