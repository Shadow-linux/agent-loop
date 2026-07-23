# Agent Loop v1.3.0 全量验证报告

日期：2026-07-12

分支：`alpha/v1.3.0`

版本：`1.3.0`

审计对象：当前未提交工作区，包含已批准 proposal、Phase 1 / Phase 2 实现、回归测试、行为示例与验证证据。不将历史报告当作 runtime authority。

## 总体结论

| 项目 | 结果 |
|---|---|
| 总分 | **97 / 100** |
| 等级 | **STRONG** |
| 修复前仓库基线 | `30/30 PASS` |
| Focused Concept Foundation contract | `PASS` |
| 修复后全部 `tests/*.sh` | `31/31 PASS` |
| Critical / High / Medium | `0 / 0 / 0` |
| 当前风险 | 2 项 Low，均不绕过 Gate |

结论：Phase 1 Requirement Concept Foundation 和 Phase 2 Product Model Derivation 已形成跨 runtime、design、requirement、product/spec、root guidance、example 和测试的一致闭环。`Concept Foundation` 仍为 Requirements Discussion / Requirement Product Grill 内部方法，未新增 canonical stage。

## 六域评分

| 审计域 | 权重 | 结果 | 评分 | 主要证据 |
|---|---:|---|---:|---|
| Logic Correctness | 20% | PASS | 97 | `references/runtime.md:59-88` 定义路由、状态、hard stop 和 Human Grill Contract；`references/requirement-product-grill.md:22-113` 定义 Gate 与推导。 |
| Autonomy | 15% | PASS | 96 | Agent 先查证据、提取候选、推荐定义与影响，再仅询问一个 downstream-blocking 问题；简单路径可记录 not-needed 理由。 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | PASS | 97 | 未修改这些阶段的语义或顺序；root Stage Map 仅在 Requirements Discussion 行增加导航，全量回归保持 GREEN。 |
| Development / Test Workflow | 20% | PASS | 99 | 保留 RED，新增 focused contract、真实 Markdown artifact parser、无效 fixtures、同场景 GREEN 压测，并重跑全量测试。 |
| Memory | 15% | PASS | 96 | 原始人类需求保持不可篡改；accepted Concept Foundation 和 Requirement Product Model 归属 human-reviewed requirement document，root guidance 与下游引用一致。 |
| Recommendation | 15% | PASS | 98 | `candidate` / `reopened` 有唯一回退路径；`accepted` / `concept-foundation-not-needed` 后才继续；Human Gate 的问题粒度和停止条件明确。 |

加权得分为 97.25，按报告精度记为 97。

## RED 基线与 GREEN 证据

修复前，全部已有测试为 `30/30 PASS`，说明仓库健康但现有测试未覆盖本漏洞。新增 `tests/validate-concept-foundation-requirement-modeling.sh` 后，在修改 runtime/template 之前产生预期 RED：

```text
FAIL: SKILL.md missing required text: Concept Foundation
```

三组修复前语义压测暴露了真实合理化路径：退款终态被压缩，Approval 动作/实例在下游漂移，ADR 重新拥有产品语义。完整证据保存于 `docs/reports/agent-loop-v1.3.0-concept-foundation-red-baseline-2026-07-12.md`。

修复后，同一组授权场景复测为：

```text
Refund Human Grill Contract: PASS
Approval Concept -> Product/Spec trace: PASS
Simple copy not-needed route: PASS
Historical overdraft / PRD-ADR ownership: PASS
```

Focused contract 还通过 Ruby validator 实际解析示例与无效 fixture，证明：

- accepted 示例的 5 个 Concept 和 20 个 Product Model row 可追踪；
- `candidate` 需求不能继续模型化；
- 未定义 Concept ID 或脱离上游的 downstream reference 会被拒绝；
- Product Brief / Feature Spec 不能在本地重新定义 accepted 产品语义。

## 已通过的核心不变量

- `SKILL.md` 保持简洁入口，详细方法仍属于 `references/`。
- `Concept Foundation` 没有进入 `references/runtime.md` canonical Stage Order。
- Human Grill Contract 固定为 evidence inspection → candidate extraction → recommendation/evidence/impact → exactly one blocking question。
- `candidate` 和 `reopened` 会阻止 Business Flow、State Model 和 Product Data Model。
- 简单文案/样式/配置变更可使用带具体理由的 `concept-foundation-not-needed`。
- accepted Concept Foundation 与 Requirement Product Model 只由 human-reviewed requirement document 拥有。
- Product Brief 和 Feature Spec 只引用 accepted Concept / Model ID，不重新定义产品语义。
- ADR 仅消费 accepted PRD 语义；本轮未建立 Concept-ID-to-table/store/event/provider 映射。
- Delivery Contract、TDD、Active Feature、Pause/Resume/Close/Reopen、Submit/Integrate 和 Tag 的原有 Gate 继续由全量回归保护。
- 没有在技能源仓库中创建目标项目 `.agent-loop/` artifact。

## 代表性压力场景

| 场景 | 结果 | 结论 |
|---|---|---|
| 退款审核完成与资金到账完成被要求合并 | PASS | Agent 先展示候选概念和推荐定义，再只问一个阻断问题。 |
| User / Customer / Member / Tenant 边界 | PASS | 候选库要求 identity、owner、lifecycle 和 relationship，不得仅做同义词表。 |
| Approval action / instance 冲突 | PASS | stable Concept IDs 追踪到 Product Brief 和 Feature Spec。 |
| 历史允许透支与新规则冲突 | PASS | PRD 负责产品定义，ADR 无权用技术结构重新定义。 |
| 按钮文案变更 | PASS | 记录 `concept-foundation-not-needed` 理由，不强制建模或 ADR。 |
| 复杂 Requirement 后续 Decision Scan | PASS | accepted PRD 语义可被后续技术决策消费，本轮未提前实现 Phase 3。 |
| 既有全流程压力集 | PASS | Product Source、Delivery Contract Gate、TDD、Active Feature、Phase 汇总、ADR drift、Follow-up、Submit、stale-memory、Chat 路径由 `31/31` 全量回归保持通过。 |

## 当前问题

### Low-1：触发分类仍需 Agent 语义判断

证据：`references/runtime.md:61-71`、`references/requirement-product-grill.md:28-41`。

风险：边界案例中，Agent 可能需要在“复用已接受概念”和“新关系已改变产品语义”之间做判断。

处理：已有正/反触发信号、具体 not-needed 理由和 human stop；不会绕过 Gate，故为 Low。

### Low-2：Markdown validator 证明结构引用，不证明业务证据为真

证据：`scripts/check-concept-foundation-trace.rb`。

风险：自动验证可拒绝未接受状态、未定义 ID、脱钩 model row 与下游重定义，但无法自动判断人类提供的业务事实是否真实。

处理：这是 Human Grill Contract 与 Human Gate 的职责，不应在本轮用可执行 schema 伪造业务真实性，故为 Low。

## 未采纳或降级意见

- 未把 Concept Foundation 升级为 canonical stage：proposal 明确否定，且会与轻量需求路径冲突。
- 未强制所有需求建立概念模型：保留带理由的 `concept-foundation-not-needed`。
- 未让 ADR 拥有 Domain Concept 定义：ADR 仅保留 accepted PRD 引用与技术决策职责。
- 未增加 Concept-to-technical mapping、Design Skill、E2E Skill、Jam Kits 或 YAML/JSON 可执行 schema：均属 Phase 3/4 或明确排除范围。

## 范围漂移检查

- Phase 1：已实现 trigger、not-needed、status lifecycle、evidence-first candidate extraction、recommended definition/evidence/impact、单一 blocking question 和 hard stop。
- Phase 2：已实现 Concept Relationships、Role/Permission、Commands/Events、Business Flow、State Model、Product Data/Fact/Invariant、Exception/Recovery 和 Concept-to-Product trace。
- 未实现 Phase 3 / Phase 4，未新增 Design Skill、E2E Skill、Jam Kits 或 executable schema。
- 未修改技能版本；`SKILL.md`、`plugin.json`、`README.md` 与 `Usage.md` 仍为 `1.3.0`，root managed block 仅做同版修订号更新。
- 未在仓库根目录创建 `.agent-loop/`；下游 artifact 只存在于 `templates/`、`examples/` 和 tests fixtures。

## 结构与机械检查

- `SKILL.md` YAML：PASS
- `plugin.json` JSON：PASS
- `scripts/check-concept-foundation-trace.rb` Ruby 语法：PASS
- 全部 Shell 语法：PASS
- Markdown fence 平衡：PASS
- 本轮 diff 新增/修改行尾随空白：PASS；被触及模板内仍有历史 `- ` 占位行，不在本轮 diff 中，未做无关格式清理
- `git diff --check`：PASS

## 发布与授权判断

当前实现可进入人类审查，但本报告不构成提交或发布授权。

| 操作 | 是否授权 |
|---|---|
| commit | 否 |
| push | 否 |
| PR / merge | 否 |
| tag / release / publish | 否 |

推荐的唯一下一阶段：**Human Review**。人类确认本报告与 Phase 1 / Phase 2 范围后，再单独决定是否进入 Submit / Integrate。
