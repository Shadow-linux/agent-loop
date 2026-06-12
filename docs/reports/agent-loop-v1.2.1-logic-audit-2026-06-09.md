# Agent Loop v1.2.1 全量逻辑检查报告

**检查日期：** 2026-06-09  
**检查范围：** SKILL.md、CHANGELOG.md、references/*.md（31 份）、templates/*.md（22 份 onboarding-db + 核心模板）、Usage.md、examples/、validation-scenarios.md、plugin.json  
**检查方法：** 交叉引用验证、stage order 对齐、entry classification 映射、artifact 定义一致性、stop condition 完整性、validation scenario 覆盖度、模板与规则对照  
**检查人：** Kimi Code CLI

---

## 执行摘要

本次逻辑检查共发现 **2 项严重缺陷（🔴）**、**4 项中等风险（🟡）** 和 **3 项低风险观察（🟢）**。

最严重的问题是 `references/design.md` 作为设计来源的浓缩提取，其 **Main Flow 遗漏了 4 个已在 runtime 和 stage-guides 中正式定义的关键阶段**，且 **Entry Scenarios 仅覆盖 50% 的 runtime entry states**。这直接违反了 SKILL.md 的 Design Source Rule（"references are operational extracts from design sources"），会导致 Agent 在加载 design.md 时获得不完整的流程图和入口分类视图。

其余问题多为边界条件覆盖不足、验证场景缺失、以及跨文件 stop condition 的细微差异，不影响核心流程但可能在实战中成为 Agent 理性化绕过的漏洞。

---

## 🔴 严重缺陷

### 1. design.md Main Flow 遗漏 4 个关键阶段

**位置：** `references/design.md` 第 207–235 行（Main Flow）  
**现象：**

`runtime.md` Stage Order（第 102–134 行）和 `stage-guides.md` 均包含以下阶段，但 `design.md` 的 Main Flow 中**完全缺失**：

| 缺失阶段 | 在 runtime.md 的位置 | 在 stage-guides.md 的位置 | 功能重要性 |
|---|---|---|---|
| **Project Onboarding Scan if Needed** | Stage Order #4 | Existing Project Onboarding 入口 | 旧项目接管的正式扫描阶段 |
| **Feature Follow-up And Flow-back if Needed** | Stage Order #8 | 独立 Stage Guide | v1.2.1 核心新增能力 |
| **Analyze Consistency** | Stage Order #18 | 独立 Stage Guide | Plan Gate 后的一致性校验 |
| **Subagent Execution If Approved** | Stage Order #19 | 独立 Stage Guide | 子代理执行的正式阶段 |

**影响：**

- `design.md` 被 SKILL.md 声明为 "condensed operational extract of design sources"，是 Agent 加载的第二份强制文件（Non-Negotiable Rule）。Agent 可能优先依赖 design.md 的 Main Flow 来理解阶段顺序，从而**遗漏 onboarding 扫描、bug 回流、一致性分析、子代理执行**等关键阶段。
- `design.md` Core Model（第 44–54 行）虽然提到了 "Feature Follow-up / Flow-back when post-close bug/change appears"，但 Main Flow 中没有对应的阶段节点，形成**概念-流程断裂**。

**建议修复：**

在 `design.md` Main Flow 中补充以下 4 个阶段，顺序与 `runtime.md` Stage Order 完全一致：

```text
Project Entry
→ Remote Project Discovery if Needed
→ Re-Adopt Agent Loop Project if Needed
→ Project Onboarding Scan if Needed          <-- 补充
→ Requirement Archive
→ Product Brief if Needed
→ Brainstorm / Clarify if Needed
→ Feature Follow-up And Flow-back if Needed  <-- 补充
→ Targeted Feature Scan if Needed
→ Feature Spec
→ Requirement Checklist
→ Work Breakdown
→ Delivery Contract if Needed
→ Test Design
→ E2E Discovery if Web
→ Technical Design / Code Context
→ Plan Gate / Plan if Needed
→ Analyze Consistency                        <-- 补充
→ Subagent Execution If Approved             <-- 补充
→ Execute Task / Story
→ Verify
→ Review
→ Drift Check
→ Project Memory Update
→ Feature Completion Check
→ Submit / Integrate
→ Pause / Close
```

---

### 2. design.md Entry Scenarios 仅覆盖 50% 的 Runtime Entry States

**位置：** `references/design.md` 第 104–205 行（Entry Scenarios）vs `references/runtime.md` 第 21–36 行（Entry Classification）  
**现象：**

`runtime.md` 定义了 10 个 entry states：

```text
new-project, remote-entry, existing-project, resume, re-adopt, stale-memory,
guided-onboarding, feature-follow-up, active-feature, blocked
```

`design.md` 只定义了 5 个 entry scenarios：

```text
New Project, Remote Project Entry, Existing Project Onboarding,
Resume Existing Agent Loop, Reconcile Project Context
```

**缺失映射：**

| runtime.md Entry State | design.md 对应项 | 状态 |
|---|---|---|
| `guided-onboarding` | 无 | ❌ 缺失 |
| `feature-follow-up` | 无 | ❌ 缺失 |
| `active-feature` | 无（隐含在 Resume 中） | ⚠️ 未明确 |
| `blocked` | 无 | ❌ 缺失 |
| `re-adopt` + `stale-memory` | 合并为 "Reconcile Project Context" | ⚠️ 未拆分 |

**影响：**

- Agent 在加载 `design.md` 时无法获得 `guided-onboarding`（onboarding-db 存在后的人类引导流程）和 `feature-follow-up`（bug/改动回流）的入口定义。这两个都是 v1.2.1 的核心新增能力。
- `re-adopt` 和 `stale-memory` 在 `runtime.md` 中是两个独立状态（re-adopt = 近期开发 bypassed；stale-memory = 文档与代码冲突），但在 `design.md` 中被合并为 "Reconcile Project Context"。这可能导致 Agent 在分类时混淆 "需要重新托管" 和 "需要回补文档" 的区别。

**建议修复：**

在 `design.md` Entry Scenarios 中补充以下 4 个独立场景：

```markdown
### Guided Newcomer Onboarding
Condition: `.agent-loop/onboarding-db/` exists and human asks to be guided.
Action: Load `onboarding-db.md`, run Guided Newcomer Onboarding, recommend next reading path.

### Feature Follow-up And Flow-back
Condition: human reports bug/regression/post-close correction/field change/API mismatch/test failure.
Action: Classify as `feature-follow-up`, load `feature-follow-up.md`, inspect 30-day lookback, present Candidate Match Matrix.

### Active Feature Continuation
Condition: `.agent-loop/` exists, project.md has Active Feature, next action is clear.
Action: Read active feature docs, continue current stage.

### Blocked
Condition: blocker or missing decision prevents next stage.
Action: Ask human or diagnose.
```

同时，将 "Reconcile Project Context" 拆分为两个明确场景，或保留合并但注明涵盖 `re-adopt` 和 `stale-memory` 两种条件。

---

## 🟡 中等风险

### 3. validation-scenarios.md 缺少 "Analyze Consistency" 独立验证场景

**位置：** `references/validation-scenarios.md`  
**现象：** `stage-guides.md` 明确定义了 "Analyze Consistency" 阶段（Plan Gate 之后、Subagent/Execute 之前），要求检查 "each accepted requirement has task coverage", "each task maps to spec", "tests cover acceptance", "plan scope matches selected task"。但 validation scenarios 中没有对应的独立压测场景。

**影响：** Agent 在实战中可能跳过 Analyze Consistency，或在 Feature Auto-Loop 中从 Plan Gate 直接进入 Execute 而不做一致性检查。

**建议修复：** 新增场景编号（如 6g），测试 Agent 在 Plan Gate 后是否执行一致性检查：

```text
Prompt: "Plan 已确认。开始执行 T003。"
Expected: Agent 先运行 Analyze Consistency（检查 spec→tasks→tests→plan 的映射），确认无缺口后才进入 Execute。
```

---

### 4. Stop And Ask 条件在 SKILL.md、runtime.md、project-guidance.md 中存在细微差异

**位置：**
- `SKILL.md` 第 238–255 行（Stop And Ask）
- `runtime.md` 第 231–244 行（Auto Mode Stop Conditions）
- `project-guidance.md` 第 56–72 行（Required Stops）

**现象：** `SKILL.md` 额外包含两个条件：
- "a stage would modify human original requirements"
- "the work would require first-version exclusions"

这两个条件在 `runtime.md` Auto Mode Stop Conditions 和 `project-guidance.md` Required Stops 中**均未出现**。

**影响：** 当 Agent 处于 Feature Auto-Loop 或 Task Auto-Run 时，可能因 runtime.md 未明确列出 "修改人类原始需求" 和 "触及 first-version exclusions" 作为 stop 条件而继续执行。

**建议修复：** 在 `runtime.md` Auto Mode Stop Conditions 中补充：

```text
- a stage would modify human original requirements
- the work would require first-version exclusions
```

---

### 5. First-Version Exclusions 在三份文件中定义不一致

**位置：**
- `references/design.md` 第 237–250 行
- `references/concepts.md` 第 7–15 行
- `SKILL.md` 第 50 行

**现象：**

| 排除项 | design.md | concepts.md | SKILL.md |
|---|---|---|---|
| multiplayer workflow | ✅ | ✅ | ✅ (as "single-person only") |
| roadmap graph | ✅ | ✅ | ✅ |
| roadmap adapter | ✅ | ✅ | ✅ |
| tdd-guard | ✅ | ✅ | ✅ |
| complex ADR system | ✅ | ✅ | ❌ 未提及 |
| global skill installation | ✅ | ✅ | ❌ 未提及 |
| automatic directory-level AGENTS.md | ✅ | ✅ | ❌ 未提及 |
| automatic commit/PR/merge/release/publish | ✅ | ❌ 未提及 | ❌ 未提及 |

**影响：** 不大，但增加了 Agent 的困惑——如果人类要求 "自动提交"，Agent 从 SKILL.md 中找不到明确的 first-version exclusion，可能认为可以通过 Auto Mode 绕过。

**建议修复：** 在 `SKILL.md` 的 "First version is single-person only..." 段落后补充一个简明的 first-version exclusion 列表，或明确引用 `design.md`/`concepts.md`。

---

### 6. examples/ai-meeting-minutes-backend/ 缺少 onboarding-db 参考实现

**位置：** `examples/ai-meeting-minutes-backend/`  
**现象：** 该目录下仅有 `README.md`，没有展示 Expanded onboarding-db 在多模块、多流程、async、部署拓扑下的实际产出。

**影响：** 这不是逻辑错误，但导致 Agent 和人类缺少"复杂项目 onboarding-db 应该长什么样"的标杆。v1.2.1 规则要求 Deep Scan 产出大量图解和 Walkthrough，但没有示例可供对标。

**建议修复：** 按 `CHANGELOG.md` v1.2.1 的描述，在该目录下构建完整的 onboarding-db 参考实现。

---

## 🟢 低风险观察

### 7. SKILL.md Required Runtime Behavior 编号使用 #17/#17a 和 #21/#21a

**位置：** `SKILL.md` 第 110–129 行  
**现象：** 正常编号到 #17 后，用 #17a 表示 onboarding-diagnostics，#17a 后又回到 #18；#21 后使用 #21a 表示 onboarding-db + recovery-and-backfill。

**评估：** 这种编号方式在 Markdown 中常见，用于规则扩展，**不构成逻辑错误**。但如果未来有自动化解析工具扫描 SKILL.md，可能需要处理非数字编号。

---

### 8. templates/root-AGENTS.md 的 `section:architecture` 为占位符说明

**位置：** `templates/root-AGENTS.md` 第 97–101 行  
**现象：** `section:architecture` 的内容是 "Add only startup-critical architecture boundaries... Keep details in ARCHITECTURE.md..."，这是指导性文字而非实际内容。

**评估：** 这是模板设计，让项目初始化时知道该填什么。**不构成错误。**

---

### 9. plugin.json 的 description 与 SKILL.md 的 description 字段语义不同

**位置：** `plugin.json` 第 4 行 vs `SKILL.md` frontmatter 第 3 行  
**现象：**
- `plugin.json`: "Agent-guided single-human development loop..."
- `SKILL.md`: "Use when starting, continuing, resuming..."

**评估：** plugin.json 的 description 是项目/插件描述，SKILL.md 的 description 是 skill 触发条件（per writing-skills 的 CSO 规则）。**不构成错误。**

---

## 一致性检查汇总表

| 检查维度 | 涉及文件 | 状态 | 备注 |
|---|---|---|---|
| **Stage Order** | runtime.md ↔ design.md ↔ stage-guides.md | ❌ 不一致 | design.md 遗漏 4 个阶段 |
| **Entry Classification** | runtime.md ↔ design.md | ❌ 不一致 | design.md 仅覆盖 50% |
| **Artifact Layout** | SKILL.md ↔ artifact-rules.md ↔ design.md ↔ concepts.md | ✅ 一致 | 无矛盾 |
| **Task Done Gate** | runtime.md ↔ artifact-rules.md ↔ stage-guides.md | ✅ 一致 | 6 项条件完全对齐 |
| **Feature Close Gate** | runtime.md ↔ feature-completion-check.md ↔ stage-guides.md | ✅ 一致 | 条件完整对齐 |
| **Contract Status** | artifact-rules.md ↔ delivery-contracts.md | ✅ 一致 | draft→accepted→implemented→verified→superseded |
| **Drift Rules** | artifact-rules.md ↔ stage-guides.md ↔ large-projects.md | ✅ 一致 | 路由规则完整对齐 |
| **Status Values** | artifact-rules.md ↔ runtime.md ↔ stage-guides.md | ✅ 一致 | feature/task/contract 状态无矛盾 |
| **Gate Modes** | runtime.md ↔ artifact-rules.md ↔ project-guidance.md | ✅ 一致 | Strict/Feature Auto-Loop/Task Auto-Run 定义一致 |
| **Human Gate Stop Conditions** | SKILL.md ↔ runtime.md ↔ project-guidance.md | ⚠️ 细微差异 | SKILL.md 多 2 项条件 |
| **First-Version Exclusions** | design.md ↔ concepts.md ↔ SKILL.md | ⚠️ 细微差异 | SKILL.md 缺少 4 项 |
| **Onboarding Modes** | existing-project-onboarding.md ↔ project-onboarding-scan.md | ✅ 一致 | Quick/Deep/Targeted 定义一致 |
| **Onboarding DB Layout** | onboarding-db-templates.md ↔ project-onboarding-scan.md | ✅ 一致 | Compact/Standard/Expanded 定义一致 |
| **Complex Artifact Mode** | complex-artifacts.md ↔ stage-guides.md ↔ examples/complex-saas-project/ | ✅ 一致 | 触发条件和目录布局一致 |
| **E2E Discovery** | e2e-discovery.md ↔ stage-guides.md ↔ project.md 模板 | ✅ 一致 | 记录位置和分类一致 |
| **Project Memory Mode** | project-memory-mode.md ↔ design.md ↔ project.md 模板 | ✅ 一致 | simple/enterprise 定义一致 |
| **Root AGENTS.md Template** | templates/root-AGENTS.md ↔ project-guidance.md | ✅ 一致 | managed block sections 完全对齐 |
| **External Skill Adapters** | external-skill-adapters.md ↔ skill-routing.md ↔ stage-guides.md | ✅ 一致 | path override + gate override 一致 |
| **Feature Follow-up Rules** | feature-follow-up.md ↔ runtime.md ↔ stage-guides.md ↔ Usage.md | ✅ 一致 | 30 天窗口、Candidate Match Matrix、reopen 流程一致 |
| **Validation Scenarios 覆盖** | validation-scenarios.md ↔ 全部 rules | ⚠️ 轻微缺口 | 缺少 Analyze Consistency 场景 |
| **CHANGELOG 落地** | CHANGELOG.md ↔ 全部 rules/templates | ✅ 一致 | v1.2.1 变更均可在文件中找到对应 |

---

## 结论与修复优先级

| 优先级 | 问题 | 文件 | 修复动作 |
|---|---|---|---|
| **P0** | Main Flow 遗漏 4 个阶段 | `references/design.md` | 补充 Project Onboarding Scan、Feature Follow-up、Analyze Consistency、Subagent Execution |
| **P0** | Entry Scenarios 覆盖不足 | `references/design.md` | 补充 Guided Onboarding、Feature Follow-up、Active Feature、Blocked；拆分 Reconcile/Re-adopt |
| **P1** | Auto Mode Stop 缺少 2 项 | `references/runtime.md` | 补充 "modify human original requirements" 和 "first-version exclusions" |
| **P1** | First-Version Exclusions 不完整 | `SKILL.md` | 补充或引用完整的 exclusion 列表 |
| **P1** | 缺少 Analyze Consistency 验证场景 | `references/validation-scenarios.md` | 新增场景 6g |
| **P2** | 缺少 onboarding-db 参考实现 | `examples/ai-meeting-minutes-backend/` | 构建完整 Expanded onboarding-db |
| **P2** | 编号使用 #17/#17a | `SKILL.md` | 可选：改为连续数字或明确说明扩展编号规则 |

---

## 附录：检查文件清单

**核心规则（全部逐行审查）：**
- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
- `references/stage-guides.md`
- `references/artifact-rules.md`
- `references/validation-scenarios.md`（编号和场景主题全覆盖）

**专项规则（关键段落审查）：**
- `references/feature-follow-up.md`
- `references/feature-completion-check.md`
- `references/project-onboarding-scan.md`
- `references/onboarding-db.md`
- `references/onboarding-db-templates.md`
- `references/complex-artifacts.md`
- `references/recovery-and-backfill.md`
- `references/existing-project-onboarding.md`
- `references/human-review-summary.md`
- `references/submit-and-integrate.md`
- `references/implementation-planning.md`
- `references/project-memory-mode.md`
- `references/project-guidance.md`
- `references/external-skill-adapters.md`
- `references/skill-routing.md`
- `references/large-projects.md`
- `references/e2e-discovery.md`
- `references/delivery-contracts.md`
- `references/concepts.md`

**模板与示例（结构审查）：**
- `templates/root-AGENTS.md`
- `templates/project.md`
- `templates/onboarding-db/*.md`（22 份）
- `examples/complex-saas-project/`
- `examples/login-feature/`
- `examples/ai-meeting-minutes-backend/`

**元数据：**
- `CHANGELOG.md`
- `Usage.md`
- `plugin.json`
