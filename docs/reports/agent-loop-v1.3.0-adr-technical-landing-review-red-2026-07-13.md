# Agent Loop v1.3.0 ADR Technical Landing 审查 RED 报告

日期：2026-07-13

分支：`alpha/v1.3.0`

审计对象：另一个 Agent 完成但尚未提交的 ADR Requirement Model Technical Landing Trace 首轮实现。

## 结论

首轮实现方向正确，但 `98/100` 与 `0 High / Medium` 结论不成立。对 validator 做同源临时变异后，确认 10 个可绕过场景与 2 个合法输入误拒绝。修复前必须保持 RED 证据，不能把首轮 full-validation 报告当作当前验收结论。

## 可复现 RED

| 场景 | 首轮结果 | 正确结果 | 风险 |
|---|---|---|---|
| `Status: proposed` 在 Human Review 前做结构预检 | 拒绝 | 接受 preflight，但不得自动 accepted | Human Gate 顺序倒置 |
| `Status: accepted` 无 Human Review Evidence | 接受 | 拒绝 | 可伪造 acceptance |
| `not-applicable` 使用 `reason: n/a` | 接受 | 拒绝 | placeholder 冒充理由 |
| Coverage Hard Gate 被一条任意 checkbox 替换 | 接受 | 拒绝 | Hard Gate 形同虚设 |
| Accepted Requirement Model IDs 追加垃圾 token | 接受 | 拒绝 | ID parser 不完整 |
| source model 同时从 snapshot/trace 删除 | 接受 | 拒绝 | Agent 可静默缩小 scope |
| `covered-by-accepted-decision` 指向不存在 ADR | 接受 | 拒绝 | 外部 owner 未验证 |
| `feature-local` 指向不存在 Feature Spec | 接受 | 拒绝 | feature owner 未验证 |
| Design Slice 使用非法 status | 接受 | 拒绝 | coverage 生命周期不可依赖 |
| triggered operational concern 删除 detail | 接受 | 拒绝 | trigger 与落地内容脱节 |
| operational concern inventory 缺 3 项 | 接受 | 拒绝 | 部分评估冒充完整评估 |
| reasoned `concept-foundation-not-needed` 且无产品模型 | 拒绝 | 接受 trace-not-applicable branch | 诱导伪造产品模型 |

另发现上游 Requirement Role / Permission Matrix 没有稳定 `PERM-*` ID，Exception Paths 虽有 `EX-*`，但 ADR validator 未把它纳入模型集合。这会使 ADR 无法完整引用权限与异常/恢复语义。

## RED 执行摘要

初始对抗性测试输出表明：accepted fixture 可以通过；proposed preflight 与 not-needed 合法输入被拒；placeholder、任意 gate、垃圾 ID、silent omission、假 ADR、缺失 Feature Spec、非法 slice、缺失 operational detail、残缺 concern inventory 均被错误接受。

## 修复要求

1. `proposed -> structural preflight -> Human Review -> accepted + evidence -> accepted-mode validation`；
2. source-wide Requirement Model Scope Inventory 完整覆盖 `REL/PERM/CMD/EVT/FLOW/STATE/PM/EX`；
3. snapshot in-scope IDs、scope inventory 与 trace 做集合相等验证；
4. 外部 artifact 路径与状态真实可解析，未来 owner 必须显式 `planned:`；
5. Hard Gate、Design Slice、operational concern/detail 做结构化精确验证；
6. reasoned not-needed 分支不要求虚构 Concept/Model table；
7. 新增对抗性回归并重新执行全量验证，另存 `.2` 报告。

## 授权边界

本 RED 报告不授权 commit、push、tag、PR、merge、release 或 publish。
