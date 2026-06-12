# Agent Loop v1.2.1 深度测试报告

**测试日期：** 2026-06-09  
**测试范围：** SKILL.md、CHANGELOG.md、全部 31 份 references、22 份 onboarding-db 模板、validation-scenarios.md、examples/ 实际产物  
**测试方法：** 规则审查 + 模板落地审查 + 验证场景审查 + 示例产物审查  
**测试人：** Kimi Code CLI

---

## 执行摘要

v1.2.1 在三个测试维度上的**规则设计均达到优秀水平**：

1. **Onboarding 图解扩展**：通过 Diagram Expansion Matrix、Discovery Coverage Matrix 和强制 Walkthrough 要求，建立了"复杂度→图解数量/质量"的正向映射。
2. **下一步动作引导**：Runtime Response Frame、Stage Steering Rule 和 Guided Newcomer Onboarding 7 步流程，几乎覆盖了所有关键节点的引导义务。
3. **Bug/改动关联 30 天 Feature**：Feature Follow-up / Flow-back 机制完整，从入口拦截、证据提取、候选匹配到 reopen 闭环，规则无显著遗漏。

**但规则完备 ≠ 实战落地。** 当前最大的结构性缺口是 **"缺少复杂项目的实战参考实现"** 和 **"缺少端到端验证 harness"**。Agent 在实际执行中是否遵守规则，目前只能依赖 Agent 的 self-policing，缺乏可复现的实战对标样本。

---

## 一、Deep Onboarding 图解丰富度测试

### 1.1 规则审查

| 机制 | 状态 | 说明 |
|---|---|---|
| Diagram Expansion Matrix | ✅ 完备 | `project-onboarding-scan.md` 明确列出复杂度信号与强制图解的映射关系 |
| Discovery Coverage Matrix | ✅ 完备 | 要求每个发现的核心模块/流程/实体/async/部署必须有文档或证据级跳过理由 |
| Expanded Minimum Required Set | ✅ 完备 | 10 份强制文件只是 floor，不是 cap；明确禁止"有 10 个文件就停" |
| How To Read + Step-by-Step Walkthrough | ✅ 完备 | 所有带图模板均含双重说明；validation scenario `2h-19` 压测缺失即拒绝 complete |
| Sequence Diagram 强制要求 | ✅ 完备 | async/job/external/callback/WebSocket 场景下 sequence diagram 是 mandatory，非 optional |
| Model Usage Flow Map | ✅ 完备 | `data-model.md` 模板强制要求，展示"哪些流程/API/job 使用哪些实体" |
| Entity Lifecycle Flow Map | ✅ 完备 | `entity-template.md` 新增，追踪实体的 CRUD 责任方 |

### 1.2 模板落地审查

对 `templates/onboarding-db/` 下 22 份模板进行审查：

- **module-template.md**：包含 Call Chain Flowchart + Sequence Diagram，各配 How To Read + Step-by-Step Walkthrough ✅
- **flow-template.md**：包含 Layered Flowchart + How To Read + Step-by-Step Walkthrough ✅
- **data-model.md**：包含 ERD + Model Usage Flow Map + 双重 Walkthrough ✅
- **entity-template.md**：包含 Entity Lifecycle Flow Map 字段 ✅
- **state-flow-template.md / state-trace-template.md**：状态流转和状态写入追踪图 ✅
- **diagram.md**：统一图例风格指南（颜色、节点形状、箭头含义） ✅

### 1.3 发现的风险与缺口

| 缺口 | 严重程度 | 说明 |
|---|---|---|
| **缺少复杂项目完整参考实现** | 🔴 高 | `examples/ai-meeting-minutes-backend/` 下仅有 `README.md`，没有展示 Expanded onboarding-db 在多模块、多流程、多实体、async/job、部署拓扑下的实际产出形态。Agent 和人类都缺少"对标样本" |
| **"图尽可能完整"的主观性** | 🟡 中 | 规则虽强，但"完整"的标准依赖 Agent 判断。复杂项目中 Agent 可能以"一张概览已足够"为由减少图解 |
| **Batch Human Review 过载** | 🟡 中 | 复杂项目可能产生 20+ 张图和 15+ 份文档，Batch Review 表格会非常冗长，人类可能疲劳通过 |
| **Mermaid 渲染天花板** | 🟡 中 | 规则建议 >80 行的 Mermaid 拆分为 standalone `diagrams/<name>.md`，但"80 行"是经验值，在大型 ERD 中仍可能不可读 |
| **无自动化完整性校验** | 🟡 中 | 没有脚本或 checklist 能自动验证"每个核心模块是否都有图"。validation scenarios 依赖人工审阅 |

### 1.4 实战增强建议

1. **在 `examples/ai-meeting-minutes-backend/` 下构建完整 Expanded onboarding-db 参考实现**
   - 假设该项目有 5+ 核心模块、3+ 复杂流程、异步 ASR/生成任务、多实体关系
   - 产出应包含：`modules/*.md`（每模块调用链图+时序图）、`flows/*.md`（流程图+状态追踪）、`domain/data-model.md`（完整 ERD + Model Usage Flow Map）、`runtime/async-and-events.md`、`runtime/deployment-and-operations.md`
   - 目的：让 Agent 和人类有一个可复制的"复杂项目 onboarding 应该长什么样"的标杆

2. **增加 Diagram Coverage Checklist 脚本**
   - 一个可运行的校验清单（如 Ruby/Python 脚本或 Markdown checklist），自动检查 onboarding-db 中是否每个 `modules/<module>.md` 都包含 `## Core Call Chain Diagram`、`## How To Read`、`## Step-by-Step Walkthrough`
   - 可在 `references/onboarding-db-templates.md` 中引用该脚本

3. **增加"图解数量压力测试"验证场景**
   - 当前 validation scenarios 验证了"有图必须有 Walkthrough"，但未验证"复杂项目是否产出了足够数量的图"
   - 建议新增场景：模拟一个 8 模块 + 4 流程 + 异步队列 + 多环境部署的项目，要求 Agent 产出的 onboarding-db 必须通过 Discovery Coverage Matrix 审查

---

## 二、事事引导人类下一步动作测试

### 2.1 规则审查

| 机制 | 状态 | 说明 |
|---|---|---|
| Runtime Response Frame | ✅ 完备 | `runtime.md` 强制要求每次响应含 `Recommended next stage` |
| "禁止只回 done" | ✅ 完备 | `runtime.md` 明确要求 "Do not end an action report with only 'done'. Always include the next recommended stage or a concrete stop reason." |
| Stage Steering Rule | ✅ 完备 | `stage-guides.md` 要求每个阶段后输出 `Current Stage / Result / Recommended Next Stage / Why / Human Gate` 表格 |
| Guided Newcomer Onboarding | ✅ 完备 | `onboarding-db.md` 7 步流程，步骤 7 强制要求 "recommend exactly one next action" |
| Onboarding Next-Action Format | ✅ 完备 | 标准化表格：`Current Understanding / Recommended Next Step / Why / Artifact / Human Gate` |
| On-Demand Explanation | ✅ 完备 | 回答后若文档过薄，推荐下一步应为"补一张聚焦图"而非空泛的"还有问题吗" |
| Feature 阶段引导 | ✅ 完备 | Spec → Tasks → Tests → Plan → Execute → Verify → Review → Drift → Memory → Completion Check → Close，每阶段均有 exit/next 规则 |
| Auto Mode 边界 | ✅ 完备 | Feature Auto-Loop / Task Auto-Run 虽可自动推进，但必须在 Human-gated decisions、risky changes、failed verification 等节点停下 |

### 2.2 发现的风险与缺口

| 缺口 | 严重程度 | 说明 |
|---|---|---|
| **"给选项" vs "给唯一推荐" 的张力** | 🟡 中 | `onboarding-db.md` 步骤 4 要求 "Ask the human what they want to understand next, with 2-4 concrete options"，步骤 7 又要求 "recommend exactly one next action"。Agent 可能在实践中变成"这里有 A/B/C/D，你选哪个"，弱化了引导感 |
| **Auto 模式下的引导感稀释** | 🟡 中 | 一旦人类开启 Feature Auto-Loop 或 Task Auto-Run，Agent 可以连续推进多个阶段。虽然规则要求在某些节点停下，但人类在 Auto 模式中的"被引导感"会显著下降，甚至可能感觉 Agent 在"黑箱执行" |
| **TDD 循环内的 micro-step 引导** | 🟡 中 | 规则要求 Plan Gate 后才能执行，但 RED→GREEN→Refactor 的 TDD 循环内，Agent 是否每个小步骤都会告知人类"现在在 RED，下一步写最少实现"？文档未明确规定 micro-step 的汇报频率 |
| **开放性问题回退** | 🟡 中 | 若人类问"你觉得这个设计怎么样"，Agent 是否能抵御泛泛而谈的诱惑，而是给出一个具体下一步（如"我建议你先读 modules/auth.md 的调用链图，确认权限校验顺序是否满足需求"）？依赖 Agent 推理质量 |

### 2.3 实战增强建议

1. **在 `Usage.md` 中增加"引导感"示例对话**
   - 当前 `Usage.md` 告诉人类"Agent 会推荐下一步"，但没有展示一段完整的 onboarding 引导对话实录
   - 建议增加一个对话示例：从 "带我理解这个项目" 开始，展示 Agent 如何一步步推荐阅读路径、推荐补图、推荐运行命令

2. **增加"弱引导"检测验证场景**
   - 新增 validation scenario：当 Agent 在 onboarding 回答后只说了"还有其他问题吗"而没有给出具体下一步时，判定为失败
   - 新增 validation scenario：当 Agent 在 feature 执行阶段连续推进 3 个阶段而未向人类汇报中间状态时，判定为失败（Auto 模式除外）

3. **为 Auto 模式增加"阶段摘要"义务**
   - 当前规则允许 Auto 模式跳过阶段间的人类确认，但建议增加一条：即使在 Auto 模式下，每完成一个阶段（如 Verify、Review），Agent 必须在内部 notes 中记录摘要，并在下一个 Human-gated 停止点向人类展示"自从你上次确认后，我已完成了 X、Y、Z"

---

## 三、Flow Feature — Bug/改动关联最近 30 天 Feature 测试

### 3.1 规则审查

| 机制 | 状态 | 说明 |
|---|---|---|
| 30 天默认回溯窗口 | ✅ 完备 | `feature-follow-up.md` 明确 "Default recent window: 30 calendar days" |
| 入口拦截 | ✅ 完备 | `runtime.md` Entry Classification 设有 `feature-follow-up` 状态；Bug/改动必须先匹配再决定 |
| 触发词覆盖 | ✅ 完备 | 覆盖 bug、回归、字段/算法/API 调整、截图、日志、堆栈、测试失败、QA/用户反馈 |
| 截图证据提取 | ✅ 完备 | 明确要求提取 "screenshot-visible text, visible UI labels, error messages, stack traces, request/response samples, logs, test names" 作为匹配证据 |
| Candidate Match Matrix | ✅ 完备 | 强制表格呈现候选 Feature、状态、最后更新/关闭时间、匹配证据、匹配强度、推荐处理流 |
| 六类分类 | ✅ 完备 | `same-feature-bug`、`same-feature-adjustment`、`regression-from-feature`、`new-feature`、`maintenance-fix`、`unclear` |
| Reopen 规范 | ✅ 完备 | 不覆盖原 Close Record；新增 Follow-up Intake；更新 spec/tasks/tests/plan；重新走完整流程；最终 human confirm close |
| Maintenance Fix 兜底 | ✅ 完备 | 无归属 bug 不得裸改，必须创建 `Feature Type: maintenance-fix` workspace，含完整 spec/tasks/tests/plan |
| Validation Scenarios | ✅ 完备 | 6+ 个独立场景覆盖：bug 报告、字段更改、错误截图、测试失败、无归属 bug、人类拒绝 flow-back |

### 3.2 发现的风险与缺口

| 缺口 | 严重程度 | 说明 |
|---|---|---|
| **缺少端到端实战示例** | 🔴 高 | `examples/` 下没有任何一个 feature-follow-up 的完整产物示例。人类和 Agent 都看不到"一个 reopened feature 的 notes.md 应该长什么样"、"Follow-up Intake 的完整格式" |
| **通用错误的证据贫乏** | 🟡 中 | 若截图仅为 "500 Internal Server Error" 或空白页面，可提取的匹配文本极少。Agent 可能因证据不足而误判为 `unclear` 或错误匹配到不相关的最近 Feature |
| **31 天边界陷阱** | 🟡 中 | 30 天是默认窗口。第 31 天报告的 bug，若 Agent 没有触发 extended scan，可能错误地默认创建新 Feature，导致历史割裂。`outside-default-window` 标记存在，但依赖 Agent 主动使用 |
| **"需求改动" vs "新需求" 的模糊性** | 🟡 中 | 人类说"这个字段要改一下"在规则中属于 `same-feature-adjustment`，但如果人类坚持"这是全新的业务要求"，Agent 是否能坚持走 follow-up 流程？ |
| **Reopen 的心理阻力** | 🟡 低 | 规则要求人类确认 reopen，但部分团队文化上不喜欢重开已关闭的 ticket。规则无法解决人类心理因素，只能记录拒绝决定并引导至 linked new/maintenance-fix |

### 3.3 实战增强建议

1. **在 `examples/` 下新增 `feature-follow-up-demo/` 完整示例**
   - 构造一个场景：某 SaaS 项目在 2026-05-20 关闭了 "会议音频上传" Feature，2026-06-05（15 天后）人类报告"上传大文件时截图显示 504 错误"
   - 产出应包含：
     - 原始 Feature 的 `spec.md`、`tasks.md`、`notes.md`（含原始 Close Record）
     - `notes.md` 中的 **Follow-up Intake** 完整记录
     - **Candidate Match Matrix** 示例
     - 更新后的 `spec.md`、`tasks.md`、`tests.md`、`plan.md`
     - 修复后的 **新的 Close Record**
   - 目的：提供可复制的"bug → follow-up → reopen → 修复 → 重新关闭"全链路样本

2. **增加"截图证据贫乏"的验证场景**
   - 当前 validation scenarios 中的截图场景（约 1897 行）假设截图包含可识别的 UI 标签或错误文本
   - 建议新增场景：人类提供一个仅含 "500 Internal Server Error" 的截图，要求 Agent 正确分类为 `unclear` → `investigate-first`，而非强行匹配最近 Feature

3. **增加"31 天边界"验证场景**
   - 模拟一个在第 32 天报告、但代码路径和测试名与 32 天前 Feature 高度重合的 bug
   - 要求 Agent 识别 `outside-default-window` 并仍推荐 reopen-for-follow-up

4. **增加 Feature Follow-up 的自动化检查清单**
   - 一个可运行脚本，检查 `.agent-loop/features/` 下是否存在 reopened feature 的规范结构：Follow-up Intake 是否存在于 `notes.md`、原 Close Record 是否被保留、是否新增了新 Close Record

---

## 四、综合评估矩阵

| 维度 | 规则设计 | 模板落地 | 验证场景 | 实战示例 | 总体 |
|---|---|---|---|---|---|
| Onboarding 图解扩展 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐☆ | ⭐⭐⭐⭐⭐ | ⭐⭐☆☆☆ | **4.0 / 5** |
| 下一步动作引导 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐☆ | ⭐⭐⭐⭐☆ | ⭐⭐⭐☆☆ | **4.0 / 5** |
| Bug/改动关联 30 天 Feature | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐☆☆☆ | **4.2 / 5** |

**共同短板：实战示例缺失。** 三个维度的规则、模板、验证场景都非常扎实，但 `examples/` 目录未能提供对应复杂度的真实参考实现。这导致：
- Agent 在执行时缺少"对标样本"，容易低估产出要求
- 人类在验收时缺少"应该长什么样"的参照
- 无法做端到端的回归测试（regression test）

---

## 五、优先级行动建议

按优先级排序的实战补强项：

| 优先级 | 行动 | 目标文件/目录 | 预计工作量 |
|---|---|---|---|
| P0 | 构建 `examples/ai-meeting-minutes-backend/onboarding-db/` 完整 Expanded 参考实现 | `examples/ai-meeting-minutes-backend/onboarding-db/` | 大 |
| P0 | 构建 `examples/feature-follow-up-demo/` 完整回流示例 | `examples/feature-follow-up-demo/` | 中 |
| P1 | 新增"弱引导"和"图解数量"验证场景 | `references/validation-scenarios.md` | 小 |
| P1 | 新增 onboarding-db 完整性检查脚本（可选） | `scripts/check-onboarding-coverage.rb` 或类似 | 小 |
| P2 | 在 `Usage.md` 中增加 onboarding 引导对话示例 | `Usage.md` | 小 |
| P2 | 为 Auto 模式增加"阶段摘要"义务规则 | `references/runtime.md`、`references/stage-guides.md` | 小 |

---

## 附录：审查文件清单

**核心规则文件：**
- `SKILL.md`
- `CHANGELOG.md`
- `references/runtime.md`
- `references/stage-guides.md`
- `references/project-onboarding-scan.md`
- `references/onboarding-db.md`
- `references/onboarding-db-templates.md`
- `references/feature-follow-up.md`
- `references/validation-scenarios.md`

**模板文件（22 份 onboarding-db 模板）：**
- `templates/onboarding-db/README.md`
- `templates/onboarding-db/module-template.md`
- `templates/onboarding-db/flow-template.md`
- `templates/onboarding-db/data-model.md`
- `templates/onboarding-db/entity-template.md`
- `templates/onboarding-db/state-flow-template.md`
- `templates/onboarding-db/state-trace-template.md`
- `templates/onboarding-db/diagram.md`
- 及其他 14 份辅助模板

**示例文件：**
- `examples/ai-meeting-minutes-backend/README.md`
- `examples/complex-saas-project/`
- `examples/login-feature/`
- `examples/remote-entry/`

**人类指南：**
- `Usage.md`
- `AGENTS.md`
