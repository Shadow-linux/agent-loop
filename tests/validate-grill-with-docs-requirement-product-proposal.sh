#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
proposal="$root/docs/proposal/v1.2.x/grill-with-docs-requirement-product-lane.md"

assert_contains() {
  local text=$1
  if ! grep -Fq -- "$text" "$proposal"; then
    printf 'FAIL: grill-with-docs requirement/product proposal missing required text: %s\n' "$text" >&2
    exit 1
  fi
}

assert_not_contains() {
  local text=$1
  if grep -Fq -- "$text" "$proposal"; then
    printf 'FAIL: grill-with-docs requirement/product proposal contains retired text: %s\n' "$text" >&2
    exit 1
  fi
}

if [ ! -f "$proposal" ]; then
  printf 'FAIL: missing proposal file: %s\n' "$proposal" >&2
  exit 1
fi

assert_contains "状态：讨论草案"
assert_contains "目标版本：v1.2.4"
assert_contains "grill-with-docs 是需求澄清和领域语言拷问工具，不是 PRD 生成器，也不是 ADR 生成器。"
assert_contains "grill-with-docs 早介入；to-prd 晚合成；Decision Scan 再抽取长期决策候选。"

assert_contains "## 定位"
assert_contains "grill-with-docs = 问清楚领域语言、业务场景、边界和矛盾"
assert_contains "to-prd = 将已知上下文合成为 product.md / PRD-like Product Brief"
assert_contains "Decision Scan = 从 product.md / PRD 中识别长期、跨 feature、难逆转、有 trade-off 的决策候选"

assert_contains "## 介入时机"
assert_contains "Requirements Discussion"
assert_contains "Requirement Archive"
assert_contains "Delivery Phases"
assert_contains "Product Brief If Needed"
assert_contains "Decision Scan"
assert_contains "Feature Spec"

assert_contains "## 工作流"
assert_contains "需求沟通 / 初始想法"
assert_contains "grill-with-docs 澄清"
assert_contains "requirement README / requirement.md"
assert_contains "Delivery Phases 可选"
assert_contains "to-prd / Product Brief 合成"
assert_contains "Decision Scan"
assert_contains "Feature Spec"

assert_contains "## 提问原则"
assert_contains "一次只问一个阻塞问题"
assert_contains "先查已有 project memory、requirement source、product.md、代码和文档"
assert_contains "每个问题都给出 Agent 推荐答案"
assert_contains "只问会影响 scope、用户、业务流程、数据、权限、验收、测试或长期决策的问题"
assert_contains "不要把普通闲聊升级为文档，除非人类确认要整理需求"
assert_contains '提问前先检查相关过往 feature 的 `product.md`、`spec.md`、`tests.md`、`notes.md`'
assert_contains "不做全量 feature 扫描"
assert_contains "targeted lookup"
assert_contains "关键词、领域对象、相关 requirement、相同模块/流程、active/paused/recent feature"
assert_contains "如果过往 feature 与当前说法冲突，先指出冲突"
assert_contains "沿用、覆盖、还是作为新需求处理"

assert_contains "## 输出映射"
assert_contains "CONTEXT.md"
assert_contains 'project.md Domain Language'
assert_contains 'requirement README'
assert_contains 'product.md'
assert_contains 'notes.md'
assert_contains '.agent-loop/decisions/'
assert_contains "docs/adr/"
assert_contains "不要采用 grill-with-docs 的原生输出路径"

assert_contains "## Requirement 文档生成关系"
assert_contains "Requirements Discussion 阶段"
assert_contains "grill-with-docs 负责把需求问清楚"
assert_contains "requirement.md 记录人类确认后的需求表述"
assert_contains "README.md 记录来源、状态、Delivery Phases、开放问题和术语"
assert_contains "Product Brief / product.md 不拥有 requirement lifecycle"

assert_contains "## 与 to-prd 的关系"
assert_contains '`to-prd` 不负责采访用户'
assert_contains "grill-with-docs 负责补齐 to-prd 之前缺失的上下文"
assert_contains '`to-prd` 的 `Implementation Decisions` 和 `Testing Decisions` 不能直接等同于 ADR'

assert_contains "## 与 Decision / ADR 的关系"
assert_contains "grill-with-docs 可以发现 decision point，但不直接创建 accepted decision"
assert_contains "Hard to reverse"
assert_contains "Surprising without context"
assert_contains "Real trade-off"
assert_contains "这些信号进入 Decision Scan，而不是直接写成 ADR"

assert_contains "## Human Gate"
assert_contains "开始正式 requirement 文档整理需要人类确认"
assert_contains "写入 project.md Domain Language 需要人类确认"
assert_contains "创建 product.md 需要人类确认"
assert_contains "创建 .agent-loop/decisions/*.md 需要人类确认"

assert_not_contains "默认创建 CONTEXT.md"
assert_not_contains "默认创建 docs/adr/"

printf 'PASS: grill-with-docs requirement/product proposal contract is complete\n'
