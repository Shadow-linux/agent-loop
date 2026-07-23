# Agent Loop v1.3.0 全量验证报告

日期：2026-07-13

分支：`alpha/v1.3.0`

版本：`1.3.0`

审计对象：当前未提交工作区。范围包括 Concept Foundation / Requirement Product Model 初始实现、2026-07-13 review repair、示例、validator、root guidance 与全部回归测试；历史 proposal 和旧报告不作为 runtime authority。

## 总体结论

| 项目 | 结果 |
|---|---|
| 总分 | **98 / 100** |
| 等级 | **STRONG** |
| 修复后全部 `tests/*.sh` | **31 / 31 PASS** |
| Concept Foundation 对抗用例 | **8 / 8 被拒绝** |
| Critical / High / Medium | **0 / 0 / 0** |
| Low | **1** |

结论：Concept Foundation 已能在详细流程、状态和产品数据建模前固定人类确认的概念，并把 Requirement Product Model 作为 Product Brief、Feature Spec 与后续 Decision / ADR 的产品语义输入。归档后语义变化采用 append-only follow-up 或新 requirement set，通过 README effective pointer 切换当前来源，不再要求改写已归档需求。

## 六域评分

| 审计域 | 权重 | 结果 | 评分 | 主要证据 |
|---|---:|---|---:|---|
| Logic Correctness | 20% | PASS | 99 | `references/runtime.md` 固定 hard stop、Human Gate 和归档后 reopen；validator 拒绝未确认概念、未闭合 trace 和无权限 command actor。 |
| Autonomy | 15% | PASS | 98 | Agent 先查证据、形成 candidate inventory、给出推荐与影响，再一次只问一个 blocker；非触发路径必须给具体理由。 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | PASS | 98 | canonical stage 未变化；root Stage Map 只增加 Requirements Discussion 导航和 required stop，并使用同版修订号 `1.3.0-20260713`。 |
| Development / Test Workflow | 20% | PASS | 99 | 保留 review RED 证据，新增对抗回归，修复后 focused 与全量测试均 GREEN。 |
| Memory | 15% | PASS | 98 | 历史 requirement source 不可原地重写；README 仅保存 effective/previous pointer，定义和模型留在被引用 source。 |
| Recommendation | 15% | PASS | 98 | `candidate` / `reopened` 均有明确停止与回退路径；`accepted` 前必须展示累计 Human Review Summary。 |

加权结果为 98.4，按整数记为 98。

## RED 基线与 GREEN 修复

修复前既有 `31/31` 测试为 GREEN，但人工审查证明 validator 仍可接受下列错误输入，属于真实覆盖缺口：

- downstream 使用未获人类确认的 Concept；
- 缺少 Concept Candidate Inventory；
- Blocking Ambiguity 仍为 open；
- `concept-foundation-not-needed` 使用 `n/a` 等占位理由；
- Concept-To-Product Traceability 漏掉已定义 model row；
- 重复 Concept ID；
- Product Brief / Feature Spec 没有共同的 effective source；
- Commands / Events 中 actor 对 target 没有 Role / Permission 路径。

此外，已归档 requirement 的 `reopened` 状态原本与“source immutable”发生冲突，Concept Foundation acceptance 也没有接入统一 Human Review Summary。

GREEN 后：

- `tests/validate-concept-foundation-trace-adversarial.rb` 的 8 个反例全部被拒绝；
- valid refund example 的 5 个 Concept、20 个 model row 完整通过，并补齐管理员 reconciliation permission；
- Product Brief 与 Feature Spec 必须声明同一个 `Effective Concept Source`；
- reopen 通过 Requirement Conflict Review、append-only follow-up / new requirement set 和 README pointer 完成；
- root managed-block revision 更新后，曾出现 4 个旧测试常量失败，断言同步后全量恢复为 `31/31 PASS`。

## 已通过的跨文件不变量

- `SKILL.md` 仍是简洁入口；详细规则归属 `references/`。
- `Concept Foundation` 仍是 Requirements Discussion / Requirement Product Grill 内部方法，不是 canonical stage。
- 触发后的顺序是 evidence inspection → candidate inventory → recommendation/evidence/impact → one blocking question → cumulative Human Review Summary → human acceptance。
- `candidate` 或 `reopened` 时不能进入 Business Flow、State Model、Product Data Model、Product Brief 或 Feature Spec。
- Requirement Product Model 定义产品语义；ADR 只在后续 Decision & Design Human Gate 后选择技术落地，不重定义 Concept identity、lifecycle、relationship、state、invariant 或 fact ownership。
- 已归档 source 保持不可变；README `Effective Concept Foundation` block 只维护 current/previous source 与状态。
- Product Brief、Feature Spec、examples、root guidance、stage guides、checklists 和 validation scenarios 使用同一 effective-source 规则。
- Delivery Contract、TDD、Active Feature、Pause / Resume / Close / Reopen、Submit / Integrate 和发布 Gate 的原有行为继续通过全量回归。
- 没有创建目标项目根级 `.agent-loop/` artifact，也没有引入 Design Skill、E2E Skill、Jam Kits 或 executable schema。

## 代表性压力场景

| 场景 | 结果 | 结论 |
|---|---|---|
| “退款完成”同时表示审批完成与到账完成 | PASS | 先分离 Concept 与 lifecycle，再等待人类确认 terminal meaning。 |
| User / Customer / Member / Tenant 被强制合并 | PASS | identity、ownership、membership、permission 改变下游时不可当同义词处理。 |
| 已归档退款定义被新回调证据推翻 | PASS | 保留旧 source，进入 `reopened`，确认后追加 source 并推进 README pointer。 |
| downstream 自行改名或漏引用 model row | PASS | validator 拒绝 detached / incomplete trace。 |
| command actor 没有 target permission | PASS | validator 拒绝缺失 Role / Permission pair。 |
| 简单按钮文案变更 | PASS | 使用具体的 `concept-foundation-not-needed` 理由，不强制建模或 ADR。 |
| ADR 试图重新定义产品概念和 fact owner | PASS | 回到 Requirement / Concept Foundation；技术表示留给后续 Decision & Design。 |
| 既有全流程压力集 | PASS | Product Source、Delivery Contract、TDD、Feature lifecycle、Phase 汇总、ADR drift、Follow-up、Submit、stale-memory 与 Chat 路径均由 `31/31` 回归覆盖。 |

## 当前问题

### Low：结构 validator 不证明业务证据真实性

`scripts/check-concept-foundation-trace.rb` 可以验证结构、ID、确认范围、permission、trace 和 effective source，但无法判断人类提供的业务事实是否真实。真实性仍由 evidence inspection、Human Grill 与 Human Gate 负责；将其伪装为可执行 schema 会越过本轮边界，因此不作为阻断项。

## 未采纳或降级意见

- 未把 Concept Foundation 升为 canonical stage，避免简单需求被强制建模。
- 未允许直接修改 archived requirement，避免历史语义丢失。
- 未让 ADR 承担 PRD / Concept 定义，避免产品语义在技术设计中漂移。
- 未加入 Concept-to-table/store/event/provider mapping、Design Skill、E2E Skill、Jam Kits 或 executable schema；这些不属于当前已批准实现范围。

## 机械验证

- `SKILL.md` YAML：PASS
- `plugin.json` JSON：PASS
- 全部 Shell syntax：PASS
- 全部 Ruby syntax：PASS
- Markdown fence balance：PASS
- `git diff --check`：PASS
- skill version：保持 `1.3.0`，未 bump
- root managed block：统一为 `block-version:1.3.0-20260713`

## 发布与授权

当前工作区可进入 Human Review；本报告不授权任何外部写操作。

| 操作 | 是否授权 |
|---|---|
| commit | 否 |
| push | 否 |
| PR / merge | 否 |
| tag / release / publish | 否 |

推荐的唯一下一阶段：**Human Review**。确认 Concept Foundation、append-only reopen 和 ADR ownership 边界后，再单独决定是否进入 Submit / Integrate。
