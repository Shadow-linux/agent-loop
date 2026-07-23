# Agent Loop v1.5.0 Optional Visual Communication Adapter RED Baseline

日期：2026-07-23
分支：`alpha/v1.5.0`
基线 HEAD：`7a74667bc3ce6acd99b34fc867115fbc8455b7f3`
审计对象：当前工作区；Proposal、Implementation Plan 与本 RED 测试属于本能力，无关 `.tmp/` 和既有 cache 不在范围内

## 既有基线

| 检查 | 结果 |
|---|---|
| `tests/*.sh` | 40 / 40 PASS |
| `python3 -m unittest discover -s tests -p 'test_*.py'` | 258 / 258 PASS，104.110s |
| `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'` | PASS |

## RED 证据

### Cross-file contract

Command:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
```

Result：exit 1

```text
FAIL: references/external-skill-adapters.md missing: Optional Visual Communication Adapter
```

该失败证明当前 runtime adapter 尚未定义 Proposal 要求的 Optional Visual Communication Adapter，而不是测试语法错误。

### Durable source/render validator

Command:

```bash
python3 -m unittest tests.test_optional_visual_communication_adapter -v
```

Result：exit 1

```text
ModuleNotFoundError: No module named 'scripts.visual_artifact_support'
Ran 1 test in 0.000s
FAILED (errors=1)
```

该失败证明共享 durable source/render validator 尚不存在。后续 GREEN 必须通过真实文件、JSON identity、路径、hash、generator 和 validation evidence 验证，而不是把测试改成只检查字符串。

### Task 13：Archify-first recommendation follow-up RED

人类进一步确认：决定画图后，应按“匹配的项目本地专用 Visual Skill → Archify → Mermaid/ASCII”路由；Archify 缺失但确实有价值时，必须先给出精确、可拒绝的安装/使用建议，而不是先画 Mermaid。

在修改运行规则前，扩展 focused contract 并执行：

```bash
bash tests/validate-optional-visual-communication-adapter.sh
```

Result：exit 1

```text
FAIL: references/external-skill-adapters.md missing: Do not offer Markdown / table / Mermaid / ASCII as the first drawing path merely because Archify is absent.
```

该失败证明原实现虽然允许推荐 Archify，但没有封闭“先 fallback、再考虑推荐”的解释路径。

## 预期 GREEN 边界

- Archify 只在 Visual Trigger 有价值时 preferred，不进入 mandatory helper table；
- 未授权不得安装，授权只覆盖精确披露的安装、doctor 和已披露当前 Visual Scope；
- unavailable、declined 和 install-failed 均有非阻塞 fallback；
- 新 durable diagram 使用 typed source + validated render；
- Requirement 保留 legacy render-only reader；
- ADR acceptance、Product Review、Onboarding Gates、Feature/Git/release Gates 保持独立；
- focused GREEN 后仍需 mutation pressure 和 full validation。

本报告不证明能力已实现，也不授权安装 Archify、commit、push、tag、release、publish 或 installed-skill sync。
