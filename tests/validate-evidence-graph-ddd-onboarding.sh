#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

require_file() {
  local path="$1"
  if [[ ! -f "$ROOT/$path" ]]; then
    echo "missing file: $path" >&2
    exit 1
  fi
}

require_text() {
  local path="$1"
  local pattern="$2"
  if ! grep -Fq "$pattern" "$ROOT/$path"; then
    echo "missing text in $path: $pattern" >&2
    exit 1
  fi
}

require_absent_text() {
  local path="$1"
  local pattern="$2"
  if grep -Fq "$pattern" "$ROOT/$path"; then
    echo "forbidden text in $path: $pattern" >&2
    exit 1
  fi
}

require_order() {
  local path="$1"
  shift
  local previous=0
  local pattern line
  for pattern in "$@"; do
    line="$(grep -nF "$pattern" "$ROOT/$path" | head -n 1 | cut -d: -f1 || true)"
    if [[ -z "$line" ]]; then
      echo "missing ordered text in $path: $pattern" >&2
      exit 1
    fi
    if (( line <= previous )); then
      echo "out-of-order text in $path: $pattern" >&2
      exit 1
    fi
    previous="$line"
  done
}

require_file "references/onboarding-knowledge-base.md"
require_file "references/stage-guides.md"
require_file "references/workflow-checklists.md"
require_file "references/validation-scenarios.md"
require_file "templates/onboarding-db/module.md"
require_file "templates/onboarding-db/flow.md"
require_file "templates/onboarding-db/evidence-graph.md"
require_file "templates/onboarding-db/onboarding-spec.md"
require_file "templates/onboarding-db/onboarding-tasks.md"
require_file "templates/onboarding-db/coverage-matrix.md"
require_file "templates/onboarding-db/batch-review.md"

require_text "references/onboarding-knowledge-base.md" "Evidence Graph"
require_text "references/onboarding-knowledge-base.md" "Onboarding Spec"
require_text "references/onboarding-knowledge-base.md" "Onboarding Tasks"
require_text "references/onboarding-knowledge-base.md" "02-modules/<module-name>.md"
require_text "references/onboarding-knowledge-base.md" "03-flows/<flow-name>.md"
require_text "references/onboarding-knowledge-base.md" "single long file"
require_text "references/onboarding-knowledge-base.md" "ASCII wireframe"
require_text "references/onboarding-knowledge-base.md" "ASCII 文本图"
require_text "references/onboarding-knowledge-base.md" "ASCII 状态机图"
require_text "references/onboarding-knowledge-base.md" "ASCII 架构图"
require_text "references/onboarding-knowledge-base.md" "Architecture / Boundary Diagram"
require_text "references/onboarding-knowledge-base.md" "架构/边界图"
require_text "references/onboarding-knowledge-base.md" "Mermaid flowchart"
require_text "references/onboarding-knowledge-base.md" "Mermaid sequenceDiagram"
require_text "references/onboarding-knowledge-base.md" "Timeline Diagram"
require_text "references/onboarding-knowledge-base.md" "状态图优先"
require_text "references/onboarding-knowledge-base.md" "模块文档默认必须包含架构/边界图、ASCII 状态图、Timeline / 时序图"
require_text "references/onboarding-knowledge-base.md" "流程文档默认必须包含架构/边界图、ASCII 状态图、Timeline / 时序图"
require_text "references/onboarding-knowledge-base.md" "content-bearing onboarding-db document"
require_text "references/onboarding-knowledge-base.md" "must include the required diagram set"
require_text "references/onboarding-knowledge-base.md" "Explicitly exempted docs"
require_text "references/onboarding-knowledge-base.md" "coverage-matrix.md"
require_text "references/onboarding-knowledge-base.md" "batch-review.md"
require_text "references/onboarding-knowledge-base.md" "open-questions.md"
require_text "references/onboarding-knowledge-base.md" "Timeline / 时序图 is required by default for module and flow docs"
require_text "references/onboarding-knowledge-base.md" "List state diagrams and timeline/sequence diagrams before optional supporting diagrams"
require_text "references/onboarding-knowledge-base.md" "Sequence and flow diagrams may use Mermaid"
require_text "references/onboarding-knowledge-base.md" "State machine diagrams and complex example diagrams should use ASCII"
require_text "references/onboarding-knowledge-base.md" "核心原理"
require_text "references/onboarding-knowledge-base.md" "示例图"
require_text "references/onboarding-knowledge-base.md" "流程讲解时顺带解释涉及的数据模型"
require_text "references/onboarding-knowledge-base.md" "## 2. 图解"
require_text "references/onboarding-knowledge-base.md" "## 11. 工作原理与示例"
require_text "references/onboarding-knowledge-base.md" "每张图必须带讲解"
require_text "references/onboarding-knowledge-base.md" "key 生成、hash/加密存储、脱敏展示、权限 scope、过期/轮换/吊销、泄露处置、审计日志"
require_text "references/onboarding-knowledge-base.md" "状态机/决策图"
require_text "references/onboarding-knowledge-base.md" "stacked box diagram"
require_absent_text "references/onboarding-knowledge-base.md" "复杂流程默认先用泳道时序图"
require_absent_text "references/onboarding-knowledge-base.md" "Sequence/swimlane diagrams are optional supporting diagrams."
require_text "references/onboarding-knowledge-base.md" "普通 flowchart"
require_text "references/onboarding-knowledge-base.md" "low score"
require_text "references/onboarding-knowledge-base.md" "newcomer-ready"
require_text "references/onboarding-knowledge-base.md" "Human examples are quality/detail references only"
require_text "references/onboarding-knowledge-base.md" "Relationship Wireframe"
require_text "references/onboarding-knowledge-base.md" "claims without concrete evidence stay in"
require_text "references/onboarding-knowledge-base.md" "Full Execution Gate 确认后 Agent 可以全盘执行"
require_text "references/onboarding-knowledge-base.md" "batch 是 Agent 的组织和 review 单位，不是人类闸门"
require_text "references/onboarding-knowledge-base.md" "可以一次性创建计划内的完整 onboarding-db"
require_text "references/onboarding-knowledge-base.md" "consistency / idempotency / compensation"
require_text "references/onboarding-knowledge-base.md" "Nginx, OpenResty"
require_text "references/onboarding-knowledge-base.md" "no unresolved placeholders"
require_text "references/onboarding-knowledge-base.md" "全部正式文档默认使用中文"
require_text "references/onboarding-knowledge-base.md" "推断"
require_absent_text "references/onboarding-knowledge-base.md" "Create files only when the accepted spec and current batch require them."
require_absent_text "references/onboarding-knowledge-base.md" "current batch must be explicitly accepted before module / flow docs"
require_absent_text "references/onboarding-knowledge-base.md" "accepted current batch scope"

require_text "references/stage-guides.md" "Evidence Graph"
require_text "references/stage-guides.md" "Onboarding Spec"
require_text "references/stage-guides.md" "Onboarding Tasks"
require_text "references/stage-guides.md" "Full Execution Gate 确认后 Agent 可以全盘执行"
require_text "references/stage-guides.md" "状态图优先"
require_text "references/stage-guides.md" "状态机/决策图"
require_text "references/workflow-checklists.md" "default to single long files"
require_text "references/workflow-checklists.md" "wireframe"
require_text "references/workflow-checklists.md" "batch is not a human gate"
require_text "references/workflow-checklists.md" "diagram type"
require_text "references/workflow-checklists.md" "state diagram first"
require_text "references/workflow-checklists.md" "module docs require architecture/boundary + state + timeline/sequence"
require_text "references/workflow-checklists.md" "flow docs require architecture/boundary + state + timeline/sequence"
require_text "references/workflow-checklists.md" "content-bearing onboarding-db document"
require_text "references/workflow-checklists.md" "explicit exemption"
require_text "references/validation-scenarios.md" "Prevent outline-only module docs"
require_text "references/validation-scenarios.md" "Module default single-file"
require_text "references/validation-scenarios.md" "Flow default single-file"
require_text "references/validation-scenarios.md" "Diagram Plan covers every planned content doc"
require_text "references/validation-scenarios.md" "Required diagram set"
require_text "references/validation-scenarios.md" "Mermaid flowchart / sequenceDiagram is allowed and preferred"
require_text "references/validation-scenarios.md" "ASCII remains preferred for state-machine / decision diagrams"
require_text "references/validation-scenarios.md" "module docs include architecture/boundary, state, and timeline/sequence diagrams"
require_text "references/validation-scenarios.md" "flow docs include architecture/boundary, state, and timeline/sequence diagrams"
require_text "references/design.md" "Evidence-Graph + DDD Onboarding Docs"
require_text "references/project-entry-scan.md" "Evidence-Graph + DDD Onboarding lives in"
require_text "examples/ai-meeting-minutes-backend/README.md" "Evidence-Graph + DDD Onboarding"

require_text "templates/onboarding-db/module.md" "## 2. 图解"
require_text "templates/onboarding-db/module.md" "每张图必须带讲解"
require_text "templates/onboarding-db/module.md" "架构/边界图"
require_text "templates/onboarding-db/module.md" "ASCII 架构图"
require_text "templates/onboarding-db/module.md" "ASCII 状态机图"
require_text "templates/onboarding-db/module.md" "Timeline / 时序图（必填）"
require_text "templates/onboarding-db/module.md" "Mermaid sequenceDiagram"
require_text "templates/onboarding-db/module.md" "Mermaid flowchart"
require_text "templates/onboarding-db/module.md" "## 11. 工作原理与示例"
require_text "templates/onboarding-db/module.md" "### 11.1 关键机制"
require_text "templates/onboarding-db/module.md" "### 11.2 示例 1"
require_text "templates/onboarding-db/module.md" "### 11.3 示例 2"
require_text "templates/onboarding-db/module.md" "示例 1 和示例 2 均有证据"
require_text "templates/onboarding-db/module.md" "每个示例都带示例图"
require_text "templates/onboarding-db/module.md" "key 生成、hash/加密存储、脱敏展示、权限 scope、过期/轮换/吊销、泄露处置、审计日志"
require_text "templates/onboarding-db/module.md" "原理机制图 / 示例图"
require_text "templates/onboarding-db/module.md" "流程讲解时顺带解释涉及的数据模型"
require_absent_text "templates/onboarding-db/module.md" "ASCII 泳道时序图为可选项"
require_text "templates/onboarding-db/module.md" "核心用例"
require_text "templates/onboarding-db/module.md" "数据对象"
require_text "templates/onboarding-db/module.md" "失败模式"
require_text "templates/onboarding-db/module.md" "关键代码索引"
require_text "templates/onboarding-db/module.md" "不要只写"
require_text "templates/onboarding-db/module.md" "## 15. 自检"
require_text "templates/onboarding-db/module.md" "一致性、幂等、事务边界、补偿和对账"
require_text "templates/onboarding-db/module.md" "route matching"
require_order "templates/onboarding-db/module.md" \
  "# Module: <module-name>" \
  "## 1. 模块定位" \
  "## 2. 图解" \
  "### 2.1 模块图 / 架构/边界图" \
  "### 2.2 ASCII 状态机图" \
  "### 2.3 Timeline / 时序图（必填）" \
  "### 2.4 流程图（按需）" \
  "### 2.5 图解说明" \
  "## 3. Bounded Context / DDD 视角" \
  "## 4. 核心用例" \
  "## 5. 领域模型" \
  "## 6. 数据对象" \
  "## 7. 信息传递" \
  "### Inbound" \
  "### Outbound" \
  "## 8. API / Events / Jobs" \
  "## 9. 状态流转" \
  "## 10. 失败模式" \
  "## 11. 工作原理与示例" \
  "### 11.1 关键机制" \
  "### 11.2 示例 1" \
  "### 11.3 示例 2" \
  "## 12. 验证和排障" \
  "## 13. 关键代码索引" \
  "## 14. 变更指南" \
  "## 15. 自检"

require_text "templates/onboarding-db/flow.md" "线框流程图"
require_text "templates/onboarding-db/flow.md" "架构/边界图"
require_text "templates/onboarding-db/flow.md" "ASCII 架构图"
require_text "templates/onboarding-db/flow.md" "状态图优先"
require_text "templates/onboarding-db/flow.md" "ASCII 状态机/决策图"
require_text "templates/onboarding-db/flow.md" "Timeline / 时序图（必填）"
require_text "templates/onboarding-db/flow.md" "Mermaid sequenceDiagram"
require_text "templates/onboarding-db/flow.md" "Mermaid flowchart"
require_absent_text "templates/onboarding-db/flow.md" "时序图为可选项"
require_text "templates/onboarding-db/flow.md" "Timeline Diagram"
require_text "templates/onboarding-db/flow.md" "数据流转"
require_text "templates/onboarding-db/flow.md" "状态变化"
require_text "templates/onboarding-db/flow.md" "失败路径"
require_text "templates/onboarding-db/flow.md" "代码证据"
require_text "templates/onboarding-db/flow.md" "## 15. 自检"
require_text "templates/onboarding-db/flow.md" "真实测试、fixture、API contract"

require_text "templates/onboarding-db/evidence-graph.md" "Relationship Wireframe"
require_text "templates/onboarding-db/evidence-graph.md" "Gateway / Runtime Inventory"
require_text "templates/onboarding-db/evidence-graph.md" "Evidence Readiness Gate"
require_text "templates/onboarding-db/onboarding-spec.md" "Gateway / Runtime Plan"
require_text "templates/onboarding-db/onboarding-spec.md" "Diagram Plan"
require_text "templates/onboarding-db/onboarding-spec.md" "状态图优先"
require_text "templates/onboarding-db/onboarding-spec.md" "模块文档默认必须规划架构/边界图、ASCII 状态图、Timeline / 时序图"
require_text "templates/onboarding-db/onboarding-spec.md" "流程文档默认必须规划架构/边界图、ASCII 状态图、Timeline / 时序图"
require_text "templates/onboarding-db/onboarding-spec.md" "Every planned module/flow doc must have Required Architecture/Boundary Diagram, Required ASCII State Diagram, and Required Timeline/Sequence Diagram"
require_text "templates/onboarding-db/onboarding-spec.md" "Mermaid flowchart / sequenceDiagram"
require_text "templates/onboarding-db/onboarding-spec.md" "Exemptions"
require_text "templates/onboarding-db/onboarding-spec.md" "Required Timeline / Sequence"
require_text "templates/onboarding-db/onboarding-spec.md" "ASCII 状态机/决策图"
require_text "templates/onboarding-db/onboarding-spec.md" "key 生成、hash/加密存储、脱敏展示、权限 scope、过期/轮换/吊销、泄露处置、审计日志"
require_text "templates/onboarding-db/onboarding-spec.md" "Spec Acceptance Gate"
require_text "templates/onboarding-db/onboarding-spec.md" "Full Execution Gate 另行确认后"
require_text "templates/onboarding-db/onboarding-tasks.md" "batch 是 Agent 的组织和 review 单位"
require_text "templates/onboarding-db/onboarding-tasks.md" "Full Execution Gate"
require_text "templates/onboarding-db/onboarding-tasks.md" "架构/边界图、ASCII 状态图、Timeline / 时序图"
require_text "templates/onboarding-db/onboarding-tasks.md" "Mermaid flowchart / sequenceDiagram"
require_text "templates/onboarding-db/README.md" "架构/边界图、ASCII 状态图、Timeline / 时序图"
require_text "templates/onboarding-db/README.md" "Mermaid flowchart / sequenceDiagram"
require_text "Usage.md" "架构/边界图、ASCII 状态图、Timeline / 时序图"
require_text "Usage.md" "Mermaid flowchart / sequenceDiagram"
require_absent_text "templates/onboarding-db/onboarding-spec.md" "没有 accepted spec + accepted current batch scope"
require_absent_text "templates/onboarding-db/onboarding-tasks.md" "没有 accepted spec + accepted current batch scope"
require_absent_text "templates/onboarding-db/onboarding-tasks.md" "Current Batch Acceptance Gate"

require_text "templates/onboarding-db/coverage-matrix.md" "Score"
require_text "templates/onboarding-db/coverage-matrix.md" "newcomer-ready"
require_text "templates/onboarding-db/coverage-matrix.md" "Required diagram set present"
require_text "templates/onboarding-db/coverage-matrix.md" "Architecture diagram clarity"
require_text "templates/onboarding-db/coverage-matrix.md" "State diagram clarity"
require_text "templates/onboarding-db/coverage-matrix.md" "Timeline / sequence clarity"
require_text "templates/onboarding-db/batch-review.md" "Score"
require_text "templates/onboarding-db/batch-review.md" "Gaps / Unknowns"

require_absent_text "references/onboarding-knowledge-base.md" "Build Learning Skeleton"
require_absent_text "references/onboarding-knowledge-base.md" "stable skeleton"
require_absent_text "references/project-entry-scan.md" "Learning-path-first"

echo "evidence-graph DDD onboarding validation passed"
