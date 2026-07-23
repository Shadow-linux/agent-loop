# Agent Loop v1.3.0 全量验证报告（Cross-Platform Python Script Runtime）

日期：2026-07-13

分支：`alpha/v1.3.0`

版本：`1.3.0`

审计对象：当前未提交工作区中的 Cross-Platform Python Script Runtime 实现及其对发布表面、既有 workflow contract 和 repository validation 的影响。

范围排除：共享工作区中另一个 Agent 的 `docs/proposal/v1.4.x/` 删除与 `docs/proposal/v2.0.x/` 新增，以及先前独立任务对 `onboarding-core-flow-completeness.md` 的状态修正。它们未被本轮修改、审查或视为本功能提交范围。

## 总体结论

| 项目 | 结果 |
|---|---|
| 总分 | **99 / 100** |
| 等级 | **STRONG** |
| 全部 `tests/*.sh` | `32/32 PASS` |
| Native Python suite | `36/36 PASS` |
| Compatibility launchers | 4/4 PASS |
| Current authority legacy recommendations | 0 |
| Critical / High / Medium | `0 / 0 / 0` |
| 平台证据 | `macOS-verified / Windows-test-defined` |

结论：脚本 runtime 迁移没有改变 canonical stage、routing、Human Gate、artifact ownership 或 lifecycle。四个 checker 的 hard gate 保持等价或更严格，当前权威入口与测试已切换，repository full suite 全绿。Windows execution evidence 仍需 commit/push 后的远端 CI；因此本报告支持进入 Human Review，不支持声称双平台最终验收或直接发布。

## 六域评分

| 审计域 | 权重 | 结果 | 评分 | 主要证据 |
|---|---:|---|---:|---|
| Logic Correctness | 20% | PASS | 99 | valid/invalid parity、exit code、runtime guard、workspace confinement 与 hard gate regression 全部闭合。 |
| Autonomy | 15% | PASS | 99 | Agent 有明确 canonical entry、capability failure 和唯一后续动作；缺 Python 时 fail closed，不手工模拟。 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | PASS | 99 | Root checker 与 Onboarding checker 语义保持；root Stage Map 和 onboarding Human Gates 未改变。 |
| Development / Test Workflow | 20% | PASS | 100 | TDD RED/GREEN、36 native tests、32 shell tests、兼容入口、机械检查与 review RED 全部有证据。 |
| Memory | 15% | PASS | 99 | requirement pointer、ADR snapshot/scope/trace、Active Feature、Delivery Phase 与 root guidance ownership 均未改变。 |
| Recommendation | 15% | PASS | 99 | 当前唯一下一阶段为 Human Review；commit/push/Windows CI evidence 仍保持独立 Human Gate。 |

加权分为 99.2，按整数记为 99。

## 当前问题

没有 Critical、High 或 Medium 逻辑问题。

### 验证边界：Windows execution evidence 待远端 CI

CI 已定义 `windows-latest` × Python 3.10/3.x，但当前未 commit/push，未产生真实 Windows runner 结果。报告使用 `Windows-test-defined`，不把 matrix configuration 等同于 execution PASS。

处理：Human Review 后若另行授权 commit/push，读取远端 CI；任何 Windows failure 返回 Diagnose Failure，不得将 proposal 标记为双平台最终完成。

### Review helper 边界

`requesting-code-review` helper 建议派发 reviewer subagent，但批准实施计划明确写明 Subagent execution 未授权。本轮没有越权派发，改由主 Agent 对完整 diff、旧规则、proposal contract、路径边界和回归结果进行自审。

处理：该降级不改变实现结论；若人类需要独立 reviewer，可单独授权 subagent review。

## RED 基线

实施前四个旧 checker focused suites 全部 PASS，证明迁移基线有效：

- Root AGENTS checker：PASS
- Onboarding Core Flow：PASS
- Concept Foundation：PASS
- ADR Technical Landing：PASS

新增 RED 依次证明：

- canonical `.py` inventory 缺失；
- cross-platform workflow 缺失；
- unsupported Python guard 缺失；
- deprecated/thin compatibility contract 缺失；
- Windows `py -3` launcher discovery 缺失；
- Root source 可在外部文件存在时逃逸 project root。

所有 RED 均先失败于目标缺口，随后才修改生产实现。

## GREEN 结果

### Native checker contracts

36 项 `unittest` 覆盖：

- canonical inventory 与 standard-library-only imports；
- usage/missing input/unsupported runtime exit 2；
- deprecated thin launcher 与 `py -3` discovery；
- valid runs 的只读 SHA-256 snapshot 与 deterministic output；
- Root missing/stale/broken/nested/duplicate/source escape；
- Onboarding planned/deferred/recovery/diagram；
- Concept accepted/not-needed/unconfirmed/ambiguity/permission/trace；
- ADR proposed/accepted/Human Review/scope/trace/owner/operational/path；
- 全部 checker 的 BOM/CRLF 行为；
- macOS/Windows CI matrix contract。

### Repository regressions

全部 32 个 `tests/*.sh` PASS，包括 requirement/chat、Decision & Design、Product Brief Source Gate、Delivery Contract、Project Entry、project-local skill gates、routing/lifecycle、root Stage Map、full-validation guidance 和 monthly compaction proposal contract。

## 六域语义审计

### Logic Correctness

- Requirement 仍拥有产品语义；ADR 只消费 accepted meaning 并负责技术落地。
- Decision / ADR 仍 globally optional、conditionally required，创建与接受保持 Human-gated。
- ADR proposed/accepted/not-needed、Coverage Hard Gate、Operational Landing 和 Design Slice 结论未弱化。
- Root source 与 ADR owner/reference 路径均限制在声明 root 内。
- 没有新增 canonical stage、status 或自动 acceptance。

### Autonomy

- `SKILL.md` 发布四个 canonical `.py` 路径和共享支持层。
- macOS/Windows 有明确 native invocation；兼容入口不再拥有规则。
- Python 不可用或版本不足时 exit 2，并报告 capability gap。
- Agent 不自动安装 Python、不改 PATH、不手工模拟 checker。

### Project Entry / Evidence Graph + DDD Onboarding

- Root AGENTS checker 继续只读，并增加 source confinement。
- Onboarding valid planned/deferred fixtures 和缺 recovery/detached diagram 反例保持原结论。
- Project Entry 与 Evidence Graph + DDD Onboarding 的阶段边界、Spec/Tasks gate 和 exactly two Human Gates 未改变。

### Development / Test Workflow

- 行为改动遵循 test-first RED/GREEN。
- Active shell tests 已调用 canonical Python；旧 Ruby adversarial 文件保留为 compatibility evidence，但不再是 active主路径。
- full validation、review、drift 与 Submit / Integrate gate 未改变。
- `requesting-code-review` 的 subagent 默认未覆盖实施计划中的 no-subagent Human Gate。

### Memory

- Requirement lifecycle、Delivery Phase、Feature Mapping、Active Feature 与 project memory 无 schema/routing 修改。
- Effective Concept Foundation pointer、ADR Effective Requirement Snapshot、scope inventory 与 technical landing trace 保持既有 ownership。
- 历史 report/proposal 命令保持原样，避免把当前 runtime 反写为过去证据。

### Recommendation

- 当前 authority 只推荐 canonical `.py`。
- 缺 Python、Windows CI failure 或 checker failure 都有明确 Diagnose/Capability stop。
- Human Review 之后仍需独立 commit/push 授权；远端 CI 结果不能预先假定。

## 代表性压力场景

| 场景 | 结果 |
|---|---|
| 复杂 Requirement -> Decision Scan -> ADR -> Feature Spec | PASS；既有 scope/trace/Human Review contract 保持。 |
| 无需 ADR 的简单需求 | PASS；ADR 仍 globally optional。 |
| Product Brief Source Gate | PASS。 |
| Delivery Contract Human Gate | PASS。 |
| TDD RED / 非行为型 N/A | PASS。 |
| Active Feature / Pause / Resume / Close / Reopen | PASS。 |
| 多 Phase `partially-implemented` | PASS。 |
| accepted ADR 与实现 drift | PASS；仍回 Drift Check / Decision & Design。 |
| Follow-up investigate-first | PASS。 |
| Submit / Integrate blocker 与顺序 | PASS。 |
| stale-memory / root guidance / Project Entry | PASS。 |
| 普通 Chat | PASS；不创建 workflow artifacts。 |
| Python 3.9 | 正确 exit 2。 |
| Root source 指向已存在的 `../outside.md` | 正确拒绝。 |
| Windows runner 尚未执行 | 不误报 PASS，保持 CI pending。 |

## 机械检查

- `SKILL.md` YAML：PASS
- `.github/workflows/cross-platform-checkers.yml` YAML：PASS
- repository JSON：PASS
- Python compileall：PASS
- 全部 Shell syntax：PASS
- 全部 Ruby syntax：PASS
- Markdown fence balance：PASS
- `git diff --check`：PASS
- target-project `.agent-loop/` guard：PASS
- version：保持 `1.3.0`

## 未采纳或降级意见

- 未把全部 `tests/*.sh` 改写为 Python：不在批准范围，维护侧 shell tests 继续作为 repository regression。
- 未改写历史报告和已完成实施计划中的 `.rb/.sh`：历史证据必须保留时间点语义。
- 未引入 PyYAML 或通用 YAML parser：Python 标准库边界不支持，且本轮四个 checker 只解析 Markdown。
- 未自动安装 Python 或提供 `--force`：与 fail-closed 决策冲突。
- 未执行 reviewer subagent：实施计划未授权 subagent。

## 发布与授权判断

当前可进入 Human Review；在 Windows CI 实际通过前，不建议宣称跨平台最终验收或发布 Feature Monthly Compaction 的 mutation runtime。

| 操作 | 是否授权 |
|---|---|
| version bump | 否 |
| commit | 否 |
| push | 否 |
| tag | 否 |
| PR / merge | 否 |
| release / publish | 否 |
