# Agent Loop v1.5.0 Persistent Lightweight Change RED Baseline

日期：2026-07-18
分支：`alpha/v1.5.0`
基线：`200a23b85b5b0e3ebe68496f5f4a16d923d46788`
审计对象：当前工作区，RED 测试加入前后分别记录

## 设计缺口

- 当前卡片仅 response-local，任务重入后没有持久事实源。
- 当前运行面明确禁止 `.agent-loop/changes/`。
- 当前没有月份布局、状态校验、3 个 / 7 天累计扫描或记忆候选连续性。

## 既有基线

- Focused：`bash tests/validate-lightweight-change-lane.sh`，退出码 `0`，`1/1 PASS`；输出为 `PASS: Lightweight Change routing, card, Bug/Feature boundary, adaptive verification, root, version, and gate contract is complete`。
- Python：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`，退出码 `0`，`182/182 PASS`，耗时 `74.370s`。
- Shell inventory：`find tests -maxdepth 1 -type f -name '*.sh' | sort | wc -l`，输出 `39`。

## Focused RED

- 命令：`bash tests/validate-lightweight-change-lane.sh`
- 退出码：`1`
- 第一条相关失败：`FAIL: references/lightweight-change-lane.md missing Lightweight Change contract: The card file is the execution source of truth.`
- 结论：旧运行权威仍以 response-local card 为准，尚未具备批准的持久执行事实源。

## Python RED

- 命令：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_lightweight_change_scan tests.test_python_checker_contract`
- 退出码：`1`
- 实际选中：`42` 个测试；结果为 `FAILED (failures=59, errors=6)`，subtest 失败计入 failures。
- 第一条直接缺口：`scripts/scan-lightweight-changes.py: [Errno 2] No such file or directory`。
- CI 契约同时失败：`.github/workflows/cross-platform-checkers.yml` 尚未包含 `tests.test_lightweight_change_scan` 与 `scripts/scan-lightweight-changes.py`。
- 结论：当前仓库没有 scanner/support 行为，也没有跨平台原生 CI 注册，RED 能真实证明批准设计尚未实现。

## 保留边界

- Lightweight / Bug / Feature 路由和所有 Human Gate 不降低。
- 本报告不是 GREEN 或发布证据。

## 维护者最终审查 RED

开发 Agent 的首轮 GREEN/full 报告之后，维护者对运行时边界做了独立复核。原有 suite 全绿，但以下漏洞仍可稳定复现：

| RED | 修复前实际结果 | 风险 |
|---|---|---|
| changes root 无读取权限 | exit `1`、stdout 为空、stderr 为 Python traceback，并包含绝对临时路径 | 破坏确定性 JSON 与敏感路径边界 |
| completed 卡保留 `<replace with...>` | exit `0`，并进入 completed/pending 统计 | 未完成内容可成为记忆整理输入 |
| fenced evidence 含 `## Background` / `Memory Target:` | exit `1`，被误判为重复结构 | 合法代码、配置和文档证据无法记录 |
| branch 为 `feature/v1.5.0/foo@bar` | Git 接受该 branch，scanner exit `1` | 拒绝合法 Git Context |

首次 targeted 命令选择 `5` 个新增测试方法，得到 `FAILED (failures=6)`。随后 parser 自审又增加 `test_invalid_backtick_fence_cannot_hide_an_authoring_marker`，修复前得到 `FAILED (failures=1)`，证明无效 backtick fence 曾能隐藏 authoring marker。

这些 RED 只扩展 scanner 的既有合同，不改变 Proposal 的 Lightweight / Bug / Feature 路由、状态、阈值、Memory 语义或 Human Gate。GREEN 与最终全量结果记录在同日 full-validation 报告中。
