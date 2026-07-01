#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
proposal="$root/docs/proposal/v1.2.x/project-decisions-adr-lane.md"

assert_contains() {
  local text=$1
  if ! grep -Fq -- "$text" "$proposal"; then
    printf 'FAIL: project decisions ADR proposal missing required text: %s\n' "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local text=$1
  if grep -Fq -- "$text" "$proposal"; then
    printf 'FAIL: project decisions ADR proposal contains retired text: %s\n' "$text" >&2
    exit 1
  fi
}

assert_contains "状态：轻量版已实施"
assert_contains "目标版本：v1.2.4"
assert_contains 'v1.2.4 已将轻量 Decision / ADR Lane 落到 `references/project-decisions.md`'
assert_contains "Decision Scan 早介入，Decision File 晚创建。"
assert_contains "Decision Scan 是必选检查；Decision File / ADR 是可选产物。"
assert_contains "Requirement -> Decision / ADR -> Feature"
assert_contains "first-version exclusion 仍然禁止 complex ADR system"
assert_contains '`.agent-loop/decisions/` 是 simple 和 enterprise memory mode 都可使用的一等长期 artifact'
assert_contains "第一版只正式支持两类决策记录"
assert_contains 'feature-local 小决策写入 `features/<feature>/spec.md` 的 `Design Decisions`'
assert_contains 'project / cross-feature 长期决策写入 `.agent-loop/decisions/*.md`'
assert_not_contains 'features/<feature>/decisions/`，需另行讨论是否支持'
assert_not_contains "Scope: project | cross-feature | feature"

assert_contains "## Decision / ADR 介入时机"
assert_contains "需求沟通 / 产品目标成形"
assert_contains "产品文档 / requirement README / product.md 明确"
assert_contains "Feature Spec 前"
assert_contains "Technical Design / Code Context"
assert_contains "Plan Gate 前"
assert_contains "Drift Check / Close Feature"

assert_contains "## Decision Scan Inputs"
assert_contains "requirement README"
assert_contains "product.md / PRD"
assert_contains 'to-prd `Implementation Decisions`'
assert_contains 'to-prd `Testing Decisions`'
assert_contains "current project memory"
assert_contains "existing decisions"

assert_contains "## Decision Candidate Routing"
assert_contains "Product-level decision"
assert_contains "Feature-local implementation decision"
assert_contains "Cross-feature or long-term architecture decision"
assert_contains "Testing decision"
assert_contains "Human-gated question"

assert_contains "## 技术设计部分"
assert_contains "技术选型"
assert_contains "架构组件"
assert_contains "数据模型"
assert_contains "接口 / 协议"
assert_contains "事务边界"
assert_contains "一致性模型"
assert_contains "并发控制"
assert_contains "幂等设计"
assert_contains "失败恢复"
assert_contains "性能设计"
assert_contains "高可用设计"
assert_contains "安全 / 风控"
assert_contains "可观测性"
assert_contains "验证计划"

assert_contains "### 6.1 Technology Choices"
assert_contains "### 6.2 Component Responsibilities"
assert_contains "### 6.3 Data Model And Source Of Truth"
assert_contains "### 6.4 Interfaces And Protocols"
assert_contains "### 6.5 Transaction And Consistency Boundaries"
assert_contains "### 6.6 Idempotency And Concurrency"
assert_contains "### 6.7 Failure Recovery And Compensation"

assert_contains "## 与 grill-with-docs / to-prd 的关系"
assert_contains "grill-with-docs = 问清楚领域语言、业务场景和边界"
assert_contains "to-prd = 将已知上下文合成为 product.md / PRD-like Product Brief"
assert_contains "Decision / ADR = 从产品上下文和技术设计中抽取长期、跨 feature、难逆转、有真实 trade-off 的决策"

assert_contains "## 待讨论问题"
assert_contains '独立 `references/project-decisions.md` 已实施。'

printf 'PASS: project decisions ADR proposal contract is complete\n'
