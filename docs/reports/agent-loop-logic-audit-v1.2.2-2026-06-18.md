# Agent Loop v1.2.2 全量逻辑审查报告

**审查日期**: 2026-06-18

**审查版本**: alpha-v1.2.2 (commit 75ebb9e)

**审查方法**: 5 个并行子 agent 分域审查，覆盖全部 48+ 验证场景
**审查范围**: 全部 references、templates、SKILL.md、AGENTS.md

---

## 总览

| 审查域 | 高 | 中 | 低 | 通过 |
|--------|-----|-----|-----|------|
| Project Entry & Onboarding | 3 | 4 | 1 | 29 |
| Feature Lifecycle & Flow-back | 0 | 2 | 2 | 15 |
| Task Execution & Auto Modes | 0 | 0 | 3 | 6 |
| Project Memory & Guidance | 0 | 1 | 4 | 9 |
| External Skills & Contracts | 2 | 2 | 2 | 12 |
| **合计** | **5** | **9** | **12** | **71** |

---

## 高严重度问题 (5)

### H1. 验证场景 2h-18 与 project-onboarding-scan.md 在 sequenceDiagram 定位上直接矛盾

- **位置**: `references/project-onboarding-scan.md:178` vs `references/validation-scenarios.md:499-501`
- **描述**: 场景 2h-18 要求 "reject `sequenceDiagram` as the first or only onboarding diagram"（含 Celery workers、object storage、ASR service 等异步/外部交互）。但 `project-onboarding-scan.md:178` 规定核心模块涉及异步 jobs、外部服务调用时，sequenceDiagram 是**强制要求**。场景中的 flow 完全命中强制条件。
- **影响**: Agent 执行 Deep Scan 时面临矛盾指令，图表选择行为不可预测。
- **建议**: 修改 `project-onboarding-scan.md:178`，将 sequenceDiagram 定位为详细交互图而非首选概览图。先 flowchart TB 概览，再 sequenceDiagram 详细交互。

### H2. SKILL.md Required Runtime Behavior 缺少 stale-memory onboarding-db 检测触发条件

- **位置**: `SKILL.md:97-132`
- **描述**: `runtime.md:59` 规定了当 project.md 声称 onboarding-db 存在但实际缺失时应分类为 stale-memory。SKILL.md:36 在 Non-Negotiable Rule 提到了此规则，但 Required Runtime Behavior（agent 主执行清单）中未列出。
- **影响**: Agent 在 Project Entry 时可能信任 project.md 中声称存在但实际缺失的 onboarding-db。
- **建议**: 在 Required Runtime Behavior 中添加条目，覆盖 onboarding-db 完整性检查。

### H3. 验证场景 2b 的 remote-entry Status 字段在 runtime.md Inspection Order 中路由时机偏晚

- **位置**: `references/runtime.md:38-53` vs `references/validation-scenarios.md:59`
- **描述**: 场景 2b 期望 project.md Status: remote-entry 能被立即检测并路由。但 runtime.md Inspection Order 步骤 2 读取 project.md 后，直到步骤 4 才检查 remote-entry，中间步骤可能已做其他决策。
- **影响**: Agent 可能在步骤 4 之前进入错误路由。
- **建议**: 在 Inspection Order 步骤 2 添加明确指令：检测 Status: remote-entry 时立即路由到步骤 4。

### H4. 验证场景 18b 和 23 遗漏子 agent "不能直接更新 project memory" 和 "不能批准破坏性变更" 限制

- **位置**: `references/validation-scenarios.md:1629,1731`
- **描述**: 场景 18b 和 23 的 Expected 列出了子 agent 的 6 项禁止行为，但遗漏了 "update project memory directly" 和 "approve breaking changes"。而 `stage-guides.md:712`、`external-skill-adapters.md:182`、`templates/subagent-brief.md:49-50`、`workflow-checklists.md:337` 都明确包含了这两项。
- **影响**: Agent 通过场景验证后可能允许子 agent 直接更新 project memory 或批准破坏性变更。
- **建议**: 在场景 18b 和 23 的 Expected 中补充这两项限制。

### H5. Stage Helper Capability Scan 在 stage-guides.md 中遗漏 4 个 helper-friendly 阶段

- **位置**: `references/stage-guides.md` (Work Breakdown ~482, Test Design ~554, E2E Discovery, Technical Design ~590)
- **描述**: `skill-routing.md:36-54` 将 Work Breakdown、Test Design、E2E Discovery、Technical Design 列为 helper-friendly stages，但 stage-guides.md 这 4 个阶段缺少 Stage Helper Capability Scan 步骤。Plan Gate、Execute、Diagnose、Verify、Review、Submit、Feature Completion Check 都已有。
- **影响**: 外部 issue/task splitter、test matrix builder、codebase scan helper 可用时，agent 会跳过检测直接用 fallback。
- **建议**: 在 stage-guides.md 的 Work Breakdown、Test Design、Technical Design 部分添加 Stage Helper Capability Scan。

---

## 中严重度问题 (9)

### M1. SKILL.md Required Runtime Behavior 未覆盖 Quick Onboarding 不创建 onboarding-db 的约束

- **位置**: `SKILL.md:190-192`
- **描述**: SKILL.md 提到 "offer Quick Onboarding by default"，但没有明确说明 Quick 不创建 onboarding-db 或 diagrams。`existing-project-onboarding.md:39` 有此规则但未同步到 SKILL.md。
- **建议**: 在 Required Runtime Behavior 中明确 Quick Onboarding 的输出范围限制。

### M2. runtime.md Inspection Order 缺少 Targeted Onboarding Scan 路由触发条件

- **位置**: `references/runtime.md:38-53`
- **描述**: runtime.md 主路由逻辑中未明确覆盖 Targeted Onboarding Scan 的入口。当 human 有 onboarding-db 但提出特定模块/流程问题时，agent 不确定应路由到 Targeted Scan。
- **建议**: 在 Entry Classification 表中添加 Targeted Onboarding Scan 路由条件。

### M3. onboarding-db-templates.md README Requirements 缺少 role-based reading paths 强制条件

- **位置**: `references/onboarding-db-templates.md:192-210`
- **描述**: 验证场景 2n 期望 role-based reading paths 为完成度检查项，但模板 README Requirements 中未列出。
- **建议**: 在 README Requirements 中添加 role-based reading paths 条件。

### M4. Feature Follow-up Trigger Phrases 缺少 "behavior tweak"、"small tweak" 和需求变更表述

- **位置**: `references/feature-follow-up.md:11-20`
- **描述**: runtime.md 和 SKILL.md 都列出了这些触发条件，但 feature-follow-up.md 的 Trigger Phrases 部分未列出。
- **建议**: 在 Trigger Phrases 中补充 "behavior tweak"、"small tweak"、"需要改一下" 等表述。

### M5. 验证场景 19b 缺少破坏性变更前的 mandatory affected-consumer 影响分析

- **位置**: `references/validation-scenarios.md:1660-1665`
- **描述**: 场景 19b 的 Expected 只要求 "list affected consumers" 和 "ask human confirmation"，但 `delivery-contracts.md:91-93` 要求先展示 impact table、compatibility options、migration risk，然后才能请求确认。
- **建议**: 在场景 19b 的 Expected 中补充影响分析步骤。

### M6. Version Sync Checklist 描述精确性不足

- **位置**: `AGENTS.md:47`
- **描述**: checklist 说 "section:meta managed block version:<x.y.z> and the visible synced-version text"，但可见文本使用自然语言格式（"version `1.2.2`"），非 `version:<x.y.z>` 格式。Agent 可能只搜索 `version:` 模式而遗漏可见文本更新。
- **建议**: 明确指出需要同时更新 managed block 的 `version:` 属性和第 20 行的自然语言版本文本。

### M7. stage-guides.md Existing Project Onboarding 引用 project-architecture-init.md 但 SKILL.md 未显式覆盖

- **位置**: `references/stage-guides.md:130` vs `SKILL.md:97-132`
- **描述**: stage-guides 在 Existing Project Onboarding 中加载 project-architecture-init.md，但 SKILL.md Required Runtime Behavior 只说 "during init/onboarding"，与其他文件的显式列出方式不一致。
- **建议**: 在 SKILL.md 中明确列出 "during Existing Project Onboarding"。

### M8. workflow-checklists.md stale 检查遗漏 Submit And Commit Rules 和 Feature Follow-up 条件

- **位置**: `references/workflow-checklists.md:42`
- **描述**: checklist 只检查 Bootstrap Protocol、Agent Ownership、Gate Modes、Required Stops、Completion Rules，遗漏了 Submit And Commit Rules 和 Feature Follow-up / Flow-back 两个 stale 条件。
- **建议**: 与 `project-guidance.md:39-52` 对齐，补充完整 stale 条件列表。

### M9. templates/root-AGENTS.md 缺少 Stage Helper Capability Scan 的 managed block

- **位置**: `templates/root-AGENTS.md`
- **描述**: `project-guidance.md:44` 将 Stage Helper Capability Scan 列为 stale 条件之一，但模板中没有对应的 managed block section 承载此规则。
- **建议**: 考虑添加 section:stage-scan managed block，或合并到 section:bootstrap/ownership 中。

---

## 低严重度问题 (12)

| # | 位置 | 描述 |
|---|------|------|
| L1 | `stage-guides.md:31-35` | Project Entry exit condition 不要求 AGENTS.md/CLAUDE.md 状态检查（路由阶段，实际检查在 Init/Onboarding 中） |
| L2 | `feature-follow-up.md:11-20` vs `:77` | Trigger Phrases 与 Requirement-change Ambiguity 措辞不完全一致 |
| L3 | `feature-follow-up.md:150` vs `validation-scenarios.md:2032` | maintenance-fix spec.md 内容要求措辞微差（"regression risk" vs "regression/safety risk"） |
| L4 | `runtime.md:168-174` | Feature Auto-Loop 段落未显式写 "stop at Human-gated tasks"，仅通过 "Agent-ready" 隐含 |
| L5 | `runtime.md:200` vs `stage-guides.md:837` | Standards Review 触发条件措辞微差 |
| L6 | `stage-guides.md:840` | 缺少显式声明 "review approval alone is insufficient to mark done" |
| L7 | `validation-scenarios.md:2157-2170` | 场景 48 未验证 Work Breakdown/Test Design/E2E Discovery/Technical Design 的 Stage Helper Scan |
| L8 | `validation-scenarios.md:1268-1281` | 场景 12b existing-project 分支缺少 Architecture Profile recording 步骤 |
| L9 | `project-memory-mode.md:52-63` vs `validation-scenarios.md:1226` | Enterprise 模式文件列表在场景中不完整（仅示例，非错误） |
| L10 | `workflow-checklists.md:42` | 与 L8 同源，stale 条件列表遗漏 |
| L11 | `AGENTS.md:47` | 与 M6 同源，checklist 描述精确性 |
| L12 | `templates/root-AGENTS.md` | 与 M9 同源，缺少 stage-scan managed block |

---

## 已通过的关键验证点 (71)

### Project Entry & Onboarding (29)
- [x] 场景 1 New Project 的 Expected 与 stage-guides.md Init Project 一致
- [x] 场景 2 Existing Codebase 与 existing-project-onboarding.md scan layers 一致
- [x] 场景 2d Quick/Deep 模式门控逻辑正确
- [x] 场景 2f Deep Scan P0/P1/P2 优先级正确
- [x] 场景 2g Targeted Scan 定义正确
- [x] 场景 2h-2 Standard layout derivation 正确
- [x] 场景 2h-3 Expanded layout 正确
- [x] 场景 2h-4 Default to Expanded 正确
- [x] 场景 2h-7 Human Layout Override 正确
- [x] 场景 2h-10 Module Map stays index 正确
- [x] 场景 2h-14 Data Model 规则正确
- [x] 场景 2h-17 Chinese default 正确
- [x] 场景 2h-19 Step-by-Step Walkthrough 要求正确
- [x] 场景 2i Subagent conflict synthesis 正确
- [x] 场景 2j Deployment split 正确
- [x] 场景 2k Batch Human Review 正确
- [x] 场景 2l Guided Newcomer 正确
- [x] 场景 2m Call path question 正确
- [x] 场景 2o Startup failure diagnosis 正确
- [x] 场景 2p Design decision routing 正确
- [x] 场景 2q State change trace 正确
- [x] 场景 2r Change impact analysis 正确
- [x] runtime.md Entry Classification 覆盖所有场景分类
- [x] remote-project-discovery.md trigger conditions 正确
- [x] project-guidance.md managed block version detection 链路完整
- [x] onboarding-db.md Integrity Check 覆盖 stale-memory
- [x] workflow-checklists.md Existing Project Onboarding 清单完整
- [x] Quick/Deep/Targeted 模式路由一致
- [x] Expanded/Standard/Compact 布局模式一致

### Feature Lifecycle & Flow-back (15)
- [x] 30 天窗口规则清晰，非硬边界
- [x] Candidate Match Matrix 结构完整
- [x] flow-back vs linked-new-feature vs maintenance-fix 路由清晰
- [x] maintenance-fix 要求完整（spec/tasks/tests/plan）
- [x] Feature Close 流程顺序正确（verify → review → drift → memory → confirm）
- [x] Feature Auto-Loop 停止条件完整
- [x] maintenance-fix 正确区分于普通 feature
- [x] bug 报告路由正确（场景 35, 37, 43）
- [x] 截图路由正确（场景 38）
- [x] "小改动"路由正确（场景 45）
- [x] QA 反馈路由正确
- [x] 需求变更路由正确（场景 39）
- [x] 拒绝 flow-back 处理正确（场景 41）
- [x] 拒绝重开连续性保持正确（场景 46）
- [x] runtime/stage-guides/SKILL.md 核心描述一致

### Task Execution & Auto Modes (6)
- [x] Plan Gate 正确阻止直接执行（场景 6a-1）
- [x] Analyze Consistency 在执行前运行（场景 6a-2）
- [x] Task Auto-Run 需要 accepted plan（非 No-Plan Decision）
- [x] 构造级 Plan 要求完整（exact paths/code/test/commands）
- [x] 子 agent 返回需要 main-agent review（场景 31）
- [x] Web E2E Discovery 触发条件正确（场景 6f）

### Project Memory & Guidance (9)
- [x] Managed Block 机制完整（start/end 标记、检测清单）
- [x] 版本自检 semver 比较规则正确
- [x] Stale 检测条件覆盖（missing + version older + broken）
- [x] CLAUDE.md 指向要求正确
- [x] Bug 报告路由到 Feature Follow-up
- [x] Re-adoption 最小安全协调完整
- [x] Enterprise 模式触发条件正确
- [x] Version Sync Checklist 覆盖 6 个文件
- [x] 跨文件一致性良好

### External Skills & Contracts (12)
- [x] Superpowers path overrides 全部 6 个适配器正确
- [x] Superpowers gate overrides 所有限制完整
- [x] Delivery Contract human gates 规则完整
- [x] Submit 流程顺序正确（verify → drift → diff → confirm）
- [x] Commit 消息格式区分正确（agent-loop vs 通用）
- [x] DDD Architecture Init 触发条件和输出正确
- [x] Subagent Brief 模板禁止行为完整
- [x] Superpowers 不能直接 commit/close/update memory
- [x] Superpowers 不能 accept contract/release/publish
- [x] Review 不能自行标记 done（场景 30）
- [x] Feature Auto-Loop 在 Delivery Contract 处停止（场景 33）
- [x] Feature Auto-Loop 在 submit/close/release 处停止（场景 34）

---

## 评估

**整体结论**: agent-loop v1.2.2 的规则体系设计优秀，逻辑一致性在 71/96 (74%) 的验证点上完全通过。5 个高严重度问题中，1 个是规则矛盾（sequenceDiagram），2 个是验证场景不完整（子 agent 限制），1 个是 SKILL.md 与 runtime.md 同步缺口，1 个是 stage-guides.md 阶段覆盖遗漏。所有高严重度问题均有明确的修复路径，不影响核心架构。

**优先修复建议**:
1. H1 (sequenceDiagram 矛盾) — 影响 Deep Scan 图表质量
2. H4 (子 agent 限制遗漏) — 影响子 agent 安全边界
3. H5 (Stage Helper Scan 遗漏) — 影响外部技能集成
4. H2 (SKILL.md stale-memory 触发) — 影响 onboarding 完整性
5. H3 (remote-entry 路由时机) — 影响远程项目识别
