# Agent Loop v1.3.0 Concept Foundation RED Baseline

日期：2026-07-12

分支：`alpha/v1.3.0`

审计对象：当前工作区；包含人类已提供但尚未提交的 `docs/proposal/v1.3.x/concept-foundation-requirement-modeling.md` 和既有 `CHANGELOG.md` proposal 记录。

实施范围：仅 Phase 1 Requirement Concept Foundation 与 Phase 2 Product Model Derivation。

## 修复前仓库机械基线

在新增 focused contract 前运行全部既有 `tests/*.sh`：

```text
BASELINE passed=30 failed=0
```

这证明现有仓库测试基线健康，但不能证明 Concept Foundation 已存在。

## 新增 Focused Contract RED

新增：

```text
tests/validate-concept-foundation-requirement-modeling.sh
```

先验证脚本语法，再执行 contract：

```text
$ bash -n tests/validate-concept-foundation-requirement-modeling.sh
$ bash tests/validate-concept-foundation-requirement-modeling.sh
FAIL: SKILL.md missing required text: Concept Foundation
```

判定：`RED`，且失败原因正确。现有发布入口没有 Concept Foundation routing；测试尚未进入后续 runtime ordering、Human Grill Contract、requirement template、product/spec trace 和 artifact-validator 检查。

## Contract 覆盖的不变量

- Concept Foundation 只能是 Requirements Discussion / Requirement Product Grill 内部方法，不能成为 canonical stage。
- Human Grill Contract 必须按 evidence check → candidate extraction → recommended definition/evidence/impact → exactly one blocking question 的顺序运行。
- triggered foundation 为 `candidate` 或 `reopened` 时，Business Flow、State Model 和 Product Data Model 必须停止。
- 简单需求可使用带理由的 `concept-foundation-not-needed`。
- requirement document 必须先完成 Concept Foundation，再推导 Concept Relationship、Role/Permission、Commands/Events、State、Business Flow 和 Requirement Product Model。
- Product Brief 与 Feature Spec 只消费 accepted Concept / Product Model reference，不重新定义产品语义。
- ADR 只消费 accepted PRD / Requirement Product Model；本轮不增加产品概念到技术实现映射。
- 不增加 Design Skill、E2E Skill、Jam Kits、YAML/JSON executable schema 或 `.agent-loop/concepts/`。

## Skill Pressure RED

人类明确授权了 3 个 bounded read-only subagent 场景及同场景 GREEN 复测。授权范围仅包括读取当前已发布规则、模拟下游 Agent 行为和返回原始合理化语言；禁止修改文件、提交、推送或读取本 proposal。授权在三组 GREEN 复测返回后标记为 `consumed`。

Stage Helper Resolution：

```text
Stage: Subagent Execution If Approved
Canonical Candidate: superpowers:subagent-driven-development (not exposed)
Alias Candidate: subagent-driven-development (loaded)
Resolution Status: loaded
Fallback Used: no
Method: three independent read-only pressure lanes, main-agent synthesis
Artifact Override: maintainer RED report; no target-project feature/handoffs created
```

### RED-1：退款完成 / Human Grill Contract

结论：`FAIL`。

当前规则允许谨慎 Agent 自行做出正确选择，但没有强制以下行为：

- 枚举 Concept Candidate；
- 推荐一个定义并同时说明证据、接受影响和拒绝影响；
- 在 requirement-level Business Flow / State / Product Data Model 前执行 hard stop；
- 抵抗“人类已经说不要拆概念，所以最新说法等于 override”的合理化。

原始合理化摘录：

```text
The latest human statement explicitly overrides historical behavior.
Refund remains one concept; settlement is merely an asynchronous technical side effect.
I can write a complete draft with assumptions and an open question.
Design Readiness blocks Feature Spec, not requirement drafting.
Resolve enough grill questions has no objective threshold.
Deadline and prior discussion make another question redundant.
```

风险：管理员审核完成、资金到账完成和客户通知触发点被压成一个终态，导致异步失败、重试、对账和验收互相矛盾。

### RED-2：Approval Action / Approval Instance 下游追踪

结论：`FAIL`。

当前谨慎 Agent 会因歧义停止 Product Brief，但现有模板无法证明 stable upstream-to-downstream chain；在会议时间压力下，模板允许以下漂移：

- `Approval` 从 glossary 中的动作，分别变成 product 的 request 和 spec 的 record；
- Applicant 被重命名为 Requester；
- Reviewer 与 Admin permission 被混为一体；
- Tenant 只作为依赖出现，没有 identity/boundary；
- lifecycle 和 one-active-instance invariant 在 spec 中被下游自行发明。

原始漏洞摘录：

```text
The requirement template has no concept identity, relationship, lifecycle-transition, or invariant registry.
Product terminology explicitly allows Meaning in this feature, enabling redefinition instead of citation.
Product-to-spec guidance provides no semantic-reference mechanism.
Stable IDs exist only for downstream Design Slices, not upstream domain concepts.
Self-contained even if wording differs is not rejected by an explicit semantic-drift rule.
```

风险：动作/实体碰撞、跨租户授权错误、非法状态转换、重复 active instance 和不兼容的下游 schema/event。

### RED-3：轻量路由与 ADR 所有权边界

场景 A（按钮文案）：`PASS`。现有 `design-not-needed` 与小 UI copy 不建 project decision 的规则可以抵抗“审计需要所以建 ADR”的压力。

场景 B（额度/透支冲突）：`FAIL`。当前 Grill 能先查历史行为并提出一个推荐问题，但 ADR surface 仍可重新拥有产品语义：

```text
Multi-tenant credit limits share domain/data rules, so all product semantics belong in Decision & Design.
The decision template asks for Domain Concepts and Source Of Truth, so mapping concepts directly to tables is required.
The manager authorized skipping clarification, so the ADR can settle what overdraft means.
A proposed ADR is not accepted yet, so redefining product meaning inside it is harmless.
```

风险：ADR 变成 PRD、Concept Model 和 physical data design 的混合真相源；Concept Foundation 也可能被错误实现为隐藏的新 stage。

## RED 综合判定

```text
Mechanical focused contract: FAIL as expected
Pressure lane 1: FAIL
Pressure lane 2: FAIL
Pressure lane 3A: PASS (lightweight path already exists)
Pressure lane 3B: FAIL
```

GREEN 必须针对实际漏洞实现，不能把已经通过的简单需求轻量路径重写成更重流程。

## GREEN Closure Note

同一授权组在更新后的发布规则上复测相同场景：

```text
Refund Human Grill Contract: PASS
Approval Concept -> Product/Spec trace: PASS
Simple copy not-needed route: PASS
Historical overdraft / PRD-ADR ownership: PASS after reference-only template alignment
Authorization Status: consumed
```

GREEN 详细证据与最终评分记录在本轮 full-validation 报告；本文件继续保留修复前失败和原始合理化语言。
