# Agent Loop v1.3.0 Cross-Platform Python Script Runtime 验证报告

日期：2026-07-13

分支：`alpha/v1.3.0`

版本：`1.3.0`，未 bump

审计对象：当前未提交工作区中的 Cross-Platform Python Script Runtime proposal、实施计划、四个 canonical checker、兼容入口、原生测试、现行文档引用和 CI matrix。

## 结论

| 项目 | 结果 |
|---|---|
| 实现状态 | 四个 canonical Python checker 已实现 |
| Python 依赖 | Python 3.10+；标准库 only |
| 原生 Python tests | `36/36 PASS` |
| 既有 Shell regressions | `32/32 PASS` |
| 旧入口兼容 | 4/4 launcher PASS；不再包含业务规则 |
| macOS | `macOS-verified`，Python 3.14.5 |
| Windows | `Windows-test-defined`，远端 CI 尚未运行 |
| Python 3.10 | CI matrix 已定义，本机未安装独立 `python3.10` |
| 当前权威旧入口推荐 | 0 |
| Critical / High / Medium | `0 / 0 / 0` |

结论：本轮代码迁移、macOS parity、fail-closed、只读和路径边界均已完成；在远端 Windows CI 实际通过前，不宣称双平台最终验收完成。唯一下一阶段是 Human Review；如人类后续授权 commit/push，再读取远端 CI 结果完成 Windows execution evidence。

## 实现范围

| 旧入口 | Canonical implementation | 当前角色 |
|---|---|---|
| `scripts/check-root-agents-blocks.sh` | `scripts/check-root-agents-blocks.py` | Root AGENTS managed-block 只读漂移检查 |
| `scripts/check-onboarding-core-flow-coverage.rb` | `scripts/check-onboarding-core-flow-coverage.py` | Onboarding Core Flow coverage |
| `scripts/check-concept-foundation-trace.rb` | `scripts/check-concept-foundation-trace.py` | Concept Foundation / Product Model trace |
| `scripts/check-adr-requirement-model-trace.rb` | `scripts/check-adr-requirement-model-trace.py` | ADR Requirement Model technical landing trace |

`scripts/checker_support.py` 统一负责 Python 3.10 guard、UTF-8 BOM/CRLF、metadata/section/table parsing 与 workspace path confinement。旧 `.sh` / `.rb` 文件只保留一周期 launcher，包含 `DEPRECATED COMPATIBILITY ENTRY` 标记并转交 canonical `.py`。

## RED 基线与修复

| RED | 修复 | GREEN evidence |
|---|---|---|
| 四个 canonical `.py` 不存在 | 建立共享支持层与四个 Python CLI | canonical inventory PASS |
| CI workflow 不存在 | 新增 macOS/Windows × Python 3.10/3.x matrix | CI contract PASS |
| Python `<3.10` 无显式 fail-closed | 四入口调用统一 runtime guard | 模拟 3.9 返回 exit 2 |
| 兼容入口未标记 deprecated | 增加标记、行数和 canonical target contract | 4/4 thin-launcher contract PASS |
| 兼容入口未发现 Windows `py -3` | 统一探测 `py -3 -> python3 -> python` | launcher discovery contract PASS |
| Root managed source 可逃逸 project root | 对 source 使用 `confined_path` | existing `../outside.md` 被拒绝 |

最初 `unittest` RED 曾先暴露测试 helper 的模块导入路径错误；修复为 `tests.checker_test_support` 后，RED 精确命中 canonical 文件缺失，没有把测试装载错误计作生产缺陷。

## 行为 parity

| Checker | Valid | Invalid / adversarial | 特殊平台文本 | 结论 |
|---|---|---|---|---|
| Root AGENTS | current template PASS | missing/stale/broken/nested/duplicate/outside source FAIL | BOM + CRLF PASS | parity PASS，越界更严格 |
| Onboarding | planned/deferred PASS | missing recovery/detached diagram FAIL | BOM + CRLF PASS | parity PASS |
| Concept Foundation | accepted/not-needed PASS | unconfirmed/open ambiguity/duplicate/missing permission 等 FAIL | BOM + CRLF PASS | parity PASS |
| ADR trace | accepted/proposed/not-needed PASS | missing review/coverage/owner/gate/operation/path 等 FAIL | BOM + CRLF PASS | parity PASS |

所有 valid checker 均重复运行两次并比较 `returncode/stdout/stderr`，输出一致；对临时 artifact tree 做运行前后 SHA-256 snapshot，确认无文件变化。

## Exit Code 与安全边界

| Exit | 含义 | 验证 |
|---:|---|---|
| 0 | PASS 或 `--help` | PASS |
| 1 | artifact contract invalid | PASS |
| 2 | usage、missing input、unsupported Python | PASS |

同时确认：

- canonical scripts 的 AST imports 只包含 Python 标准库与本地 `checker_support`；
- 不调用 Bash、Ruby、grep、sed、PowerShell cmdlet 或第三方 package；
- ADR 和 Root source reference 均拒绝 workspace/project root 越界；
- 没有 `--force`、自动安装 Python、自动修改 PATH 或手工模拟降级；
- ADR、Concept Foundation 和 Onboarding hard gate 的既有 valid/invalid 结论保持不弱化。

## 文档与历史边界

当前 authority 已切换到 `.py`：

- `SKILL.md`
- `Usage.md`
- `references/project-guidance.md`
- `references/workflow-checklists.md`
- 当前 1.3.0 `CHANGELOG.md`
- active regression runners

旧路径仍只出现在 compatibility contract、迁移 proposal/plan、历史 changelog 或历史 report 中。历史 evidence 未被改写。

## 平台证据

`.github/workflows/cross-platform-checkers.yml` 定义四组合：

```text
macos-latest  / Python 3.10
macos-latest  / Python 3.x
windows-latest / Python 3.10
windows-latest / Python 3.x
```

本地实际证据：macOS + Python 3.14.5，36/36 native tests、32/32 Shell tests、四个 compatibility launcher 和全部机械检查通过。

未执行证据：Windows runner 与独立 Python 3.10 runner。原因是当前没有 commit/push 授权，workflow 尚不能在远端执行；这不是 PASS，也不被伪装成双平台完成。

## 机械检查

- `SKILL.md` 和 workflow YAML：PASS
- repository JSON parse：PASS
- Markdown fence balance：PASS
- 全部 Shell syntax：PASS
- 全部 Ruby compatibility/test syntax：PASS
- Python compileall：PASS
- `git diff --check`：PASS

## Human Gate

| 操作 | 是否授权 |
|---|---|
| version bump | 否 |
| commit | 否 |
| push | 否 |
| tag | 否 |
| PR / merge | 否 |
| release / publish | 否 |

本报告不授权 Feature Monthly Compaction 自动进入实现；该 proposal 仍需根据当前状态和 Human Review 单独路由。
