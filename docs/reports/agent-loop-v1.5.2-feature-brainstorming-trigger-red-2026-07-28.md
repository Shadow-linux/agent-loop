# Agent Loop v1.5.2 Feature Brainstorming 条件触发 RED 基线

## 审计对象

- 日期：2026-07-28
- 分支：`v1.5.2`
- 基线提交：`a9b10f707f42ec37f68b74b6867fea5af88c458d`
- 问题：runtime/design 将 Brainstorm / Clarify 定义为 Feature-local uncertainty 的按需方法，但 external adapter、stage guide 和 checklist 容易让 Agent 把 brainstorming 当作所有 Feature Spec 的默认前置步骤。

## RED

新增 `tests/validate-feature-brainstorming-trigger.sh` 后首次执行：

```text
FAIL: references/runtime.md missing Feature brainstorming contract:
Feature Spec enters Brainstorm / Clarify only when concrete feature-local scope,
acceptance, or implementation-boundary uncertainty remains after loading the
accepted Product Slice and applicable ADRs.
EXPECTED_RED_EXIT=1
```

该失败证明旧规则没有明确保护“清晰 Feature 直接进入 Feature Spec”的路径。

## 目标不变量

- helper 可用不构成 Brainstorm / Clarify 触发条件。
- Product Slice、适用 ADR Design Slice、scope、exclusions 和 measurable acceptance 已清楚时，直接进入 Feature Spec。
- brainstorming 只处理一个真实的 Feature-local scope、acceptance 或 implementation-boundary uncertainty。
- brainstorming 不得重定义 Requirement 产品语义、改写 accepted ADR 或新增 Feature scope。
- product ambiguity 返回 Requirements Discussion；ADR incompatibility 返回 Decision & Design Human Review。
