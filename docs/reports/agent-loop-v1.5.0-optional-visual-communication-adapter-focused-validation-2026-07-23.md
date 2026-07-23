# Optional Visual Communication Adapter Focused Validation

日期：2026-07-23
分支：`alpha/v1.5.0`
版本：v1.5.0（未升级）
审计对象：基线 `7a74667bc3ce6acd99b34fc867115fbc8455b7f3` 之上的当前工作区实现
上游能力：<https://github.com/tt-a1i/archify>

## 结论

Focused validation 为 **PASS**。Optional Visual Communication Adapter 已形成可执行闭环：Visual Trigger 成立时优先匹配 active project-local visual skill，再使用 installed Archify；Archify 缺失但对审核有实质价值时，先提出精确安装/使用建议，只有不值得安装、人类拒绝、环境不支持或安装/使用失败时才降级 Markdown/Mermaid/ASCII。安装、Visual Scope、durable record、语义接受、Feature 与 Git/release 保持独立 Human Gate。

新的 durable writer 使用 `source-render-v1`，同时验证 typed JSON source、render、两份 SHA-256、Type、`meta.output`、`archify@version` 和 `validate=pass; check=pass`。Requirement 保留历史六列表 reader；ADR 和 Onboarding 的 HTML-only 输出不能充当长期证据。

## RED 基线

实施前真实证据见 `docs/reports/agent-loop-v1.5.0-optional-visual-communication-adapter-red-baseline-2026-07-23.md`：

- focused Shell 因运行时/路由/模板合同不存在而失败；
- focused Python 因 `scripts.visual_artifact_support` 不存在而失败；
- 旧仓库基线为 40/40 Shell、258/258 Python，证明 RED 来自新增合同而非旧故障。
- Task 13 follow-up RED 因 `references/external-skill-adapters.md` 缺少“不得仅因 Archify 缺失就先给 Mermaid”的约束而 exit 1，证明原优先级仍存在 fallback-first 歧义。

## GREEN 结果

```text
bash tests/validate-optional-visual-communication-adapter.sh
PASS

python3 -m unittest tests.test_optional_visual_communication_adapter -v
Ran 19 tests in 0.440s
OK
```

覆盖结果：

| 范围 | 结果 |
|---|---|
| Shared source/render envelope | PASS |
| Requirement new writer | PASS |
| Requirement legacy reader | PASS |
| ADR optional evidence | PASS |
| ADR proposed/accepted independence | PASS |
| Onboarding durable Diagram ID | PASS |
| Onboarding embedded Mermaid/ASCII fallback | PASS |
| BOM / CRLF / Windows-style path | PASS |

## Mutation Pressure

13 个负向变体均被拒绝，包括：fallback-first 路由、path escape、render-only、source/render type mismatch、`meta.output` mismatch、source hash drift、render hash drift、无版本 generator、缺失 validate/check、错误 Product columns、ADR missing source、视觉绕过 ADR Human Review、Onboarding HTML-only required diagram。

正向兼容性覆盖包括：valid Archify pair、Requirement `source-render-v1`、legacy Requirement 六列表、proposed ADR visual、accepted ADR visual、durable Onboarding Diagram ID、embedded Mermaid/ASCII 和 BOM/CRLF/backslash paths。

## 当前问题与残余边界

无 Critical / High / Medium / Low 逻辑问题。

Archify 已在本轮获得人类明确授权后通过 `npx skills add tt-a1i/archify -g` 更新，并将 active Codex copy 做 checksum 同步；`doctor` PASS。README capability map 进一步通过 `workflow` showcase validate、deliver、check、SVG 导出和像素审阅。真实目标项目仍必须在当时披露 exact source/revision/command/target/effects/doctor/fallback，不能复用本次授权。

## Git 与外部动作

- 已按本轮精确授权升级并验证 Archify；该授权不覆盖未来安装或目标项目动作；
- 未同步 installed Agent Loop；
- 未 stage、commit、push、tag、PR、merge、release 或 publish。
