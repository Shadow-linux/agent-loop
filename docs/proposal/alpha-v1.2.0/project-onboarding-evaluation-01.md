# 🔍 Project Onboarding 提案双文档深度分析报告

> 分析对象：`project-onboarding-scan.md`（扫描流程）+ `project-onboarding-templates.md`（模板规范）
> 分析视角：**人类接管项目的可理解性**作为首要评判标准
> 分析日期：2026-06-07（V1 / V2 / V3）

---

## ⚡ V1 → V2 → V3 变更时间线

| 版本 | 核心主题 | 关键新增 |
|---|---|---|
| **V1** | 设计框架搭建 | 三层分离、反目标、17文档+14图、逐文件确认、线性10步扫描 |
| **V2** | 落地可行性 | Layout Mode三级、批量确认模式、决策和历史、元信息分层、模板31→10 |
| **V3** | 执行完备性 | 扫描P0/P1/P2优先级、Subagent冲突处理流程、模块阅读路径、部署运维分层、批量确认为通用模式 |

### V2 → V3 新增清单

**scan.md V3 新增（对比 V2）：**

| 新增模块 | 说明 | 回补了 V2 哪个问题 |
|---|---|---|
| **扫描优先级 P0/P1/P2** (行623-641) | 扫描不再是线性10步，先拿安全接管事实(P0)，再补人类理解(P1)，最后补齐复杂项目(P2) | ✅ "扫描流程无优先级" |
| **Subagent 冲突处理流程** (行1023-1061) | 完整的冲突合并→证据归一→可信度标注→冲突表→主Agent裁决→批量确认流水线，含6条处理规则 | ✅ "Subagent 协调机制不清晰" |
| **模块阅读路径** (行385-397) | README 增加"按模块"的阅读路径表，支持"理解支付模块：先读A→B→C"，Compact下指向合并文档章节 | ✅ "缺少按模块阅读路径" |
| **部署和运维分层** (行423-469) | 本地启动/环境配置/生产部署三级分离，独立 deployment-and-operations.md，含触发信号和Layout Mode适配 | 🆕 新能力 |
| **Batch Human Review 升级为通用模式** (行250-306) | 从 onboarding-db 专用升级为 agent-loop 通用确认方式：含适用范围表（onboarding-db/backfill/AGENTS/drift/close/spec 全覆盖） | 🆕 扩展能力 |

**templates.md V3 新增（对比 V2）：**

| 新增模块 | 说明 |
|---|---|
| **deployment-and-operations.md 模板** (行541-604) | 完整模板：部署概览/环境/发布流水线/运行拓扑/回滚/迁移/健康检查/日志/运维入口，3张表格，Layout Mode 适配 |
| **Batch Human Review 通用模板** (行303-361) | 分离为"通用批量确认模板"和"Onboarding DB 批次摘要模板"两个层级，适用范围从 4 场景扩展到 6 场景 |

两份提案在 V1 的基础上做了大量针对性改进，**恰好解决了 V1 报告中指出的两个 P0 级问题**。

| V1 提出的 P0 问题 | V2 解决方案 | 落地位置 |
|---|---|---|
| 🔴 人类审批疲劳，30+ 文件逐文件确认 | **批量确认模式**：4 批次审批，支持 approve all / selected / revise / defer / skip | scan.md §批量确认模式, templates.md §批量确认模板 |
| 🔴 小项目被 31 个文件压垮 | **Onboarding DB Layout Mode**：Compact(5-7文件) / Standard(8-12) / Expanded(12-18) 三级 | scan.md §Onboarding DB Layout Mode, templates.md §Layout Mode 与模板颗粒度 |

同时新增了以下能力：

| V2 新增 | 解决什么问题 |
|---|---|
| **决策和历史** (`decisions-and-history.md`) | 新人理解"为什么这样设计"，不仅是"现在是什么" |
| **元信息三层分级** (Core Required / Optional / Expanded Only) | 小项目不用填满 12 个元信息字段，减少格式噪音 |
| **模块卡片字段分层** | Agent 不为了填满卡片而编造信息 |
| **模板数从 31 → 10 核心模板** | 用 `diagram.md` 通用图模板替代 14 个独立图模板 |

---

## 一、总体评分（V3 更新）

| 评估维度 | 权重 | scan.md 得分 | templates.md 得分 | 加权综合 |
|---|---|---|---|---|
| 设计完整性与一致性 | 25% | 29/30 | 29/30 | **29.0** |
| **人类可读性与可理解性** | **30%** | **25/25** | **25/25** | **30.0** |
| 实用性与可落地性 | 20% | 20/20 ↑ | 19/20 | **19.5** |
| Agent 友好度与约束力 | 15% | 15/15 ↑ | 14/15 | **7.3** |
| 创新性与前瞻性 | 10% | 9/10 | 8/10 | **8.5** |
| **综合总分** | **100%** | **98/100** ↑ | **95/100** | **94.3/100** ↑ |

### 分数变化轨迹

| 版本 | scan.md | templates.md | 综合 | 关键驱动 |
|---|---|---|---|---|
| V1 | 92 | 90 | 91.1 | 设计框架完整但落地有瓶颈 |
| V2 | 96 | 95 | 93.5 | Layout Mode + 批量确认切掉两大 P0 障碍 |
| **V3** | **98** | **95** | **94.3** | 扫描优先级 + Subagent 冲突 + 模块路径 + 部署分层，**四个 P1 问题解决三个** |

---

## 二、V3 新增亮点分析

### 2.6 扫描优先级 P0/P1/P2 — 解决了"线性扫描无脑跑" ⭐V3新增⭐

| 优先级 | 目标 | 包含扫描 | 典型产出 |
|---|---|---|---|
| **P0** | 让 Agent 能判断项目形态、运行入口和风险 | Project Shape、Existing Docs、Shallow Repo、Tooling、Entrypoints | Quick Onboarding、project.md 草案、风险标记 |
| **P1** | 让人类能理解主要模块、边界和核心流程 | Module Map、Boundary、Core Flow、Commands/Tests | onboarding-db 主阅读路径、模块/边界/核心流程图 |
| **P2** | 补齐复杂项目长期维护资料 | Async/Events、Jobs、Data Model、Deployment、Integrations、Decisions、Change Impact | 细分文档、专题图、project memory backfill |

**关键执行规则**：

| 情况 | 行为 |
|---|---|
| 人类选 Quick | 只做 P0 |
| 人类选 Deep | P0 → P1 → 按项目选 P2 |
| 项目很大 | 不直接全量 P2，先用 P0/P1 形成边界 |
| 发现高风险未知 | 暂停，让人类确认 |
| 只关心某个模块 | Targeted Scan，不跑完整 P2 |

> 这个设计完美回应了 V2 的"扫描流程无优先级"问题，而且把 P0 和 Quick Onboarding 绑定、P1 和 Deep 的核心价值绑定，逻辑自洽。

### 2.7 Subagent 冲突处理流水线 — 解决了"子代理只管扫不管合" ⭐V3新增⭐

完整的冲突处理流程：

```
Subagent Returns
→ Normalize Findings（证据归一）
→ Deduplicate Facts（去重）
→ Detect Conflicts（发现冲突）
→ Check Evidence Quality（证据质量检查）
→ Assign Confidence（可信度标注）
→ Produce Conflict Table（冲突表）
→ Main Agent Decision / Human Question（主Agent裁决或问人类）
→ Batch Human Review（批量确认）
→ Confirmed Write（写入）
```

**6 条冲突处理规则**：结论一致→合并提可信度；代码证据更强→以代码为准；证据都弱→进 risks-and-unknowns；涉及业务意图→问人类；涉及长期记忆→放入 Memory Backfill 批次；涉及安全/数据/生产→降低自动化。

> V2 的"Subagent 协调机制不清晰"被彻底解决。

### 2.8 模块阅读路径 — 解决了"知道有哪些文件但不知道怎么串" ⭐V3新增⭐

```markdown
| 模块 | 先读 | 再读 | 相关图 | 适合的问题 |
|---|---|---|---|---|
| <module> | module-map.md#<module> | core-flows.md#<flow> | diagrams/<flow>.md | 这个模块做什么、入口在哪、改它影响谁 |
```

Compact 模式下指向合并文档的章节。这恰好是 V2 报告中指出的"缺少按模块阅读路径"。

### 2.9 部署和运维分层 — 解决了"部署信息散落各处" ⭐V3新增⭐

| 内容 | 放置位置 |
|---|---|
| 本地启动、端口、依赖服务 | `setup-and-run.md` |
| 环境变量、dev/test/prod 差异、CI | `environment.md` |
| 生产部署、发布、回滚、运维入口 | `deployment-and-operations.md` |
| 部署拓扑 | `diagrams/deployment-map.md` |

独立 `deployment-and-operations.md` 的触发信号：多环境发布、容器编排、CI/CD 发布流程、回滚流程、运维入口。所有 Layout Mode 都有对应处理方式。

### 2.10 Batch Human Review 升级为通用模式 ⭐V3扩展⭐

原来 scope 仅限于 onboarding-db，现在扩展到：

| 场景 | 是否必须 | 原因 |
|---|---|---|
| onboarding-db 文档 | 必须 | 面向人类接管 |
| project memory backfill | 必须 | 影响长期 Agent 行为 |
| AGENTS.md / CLAUDE.md 更新 | 必须 | 影响后续 Agent 工作方式 |
| drift check 后回补 | 必须 | 需明确代码现实和文档差异 |
| close feature 前文档同步 | 必须 | 避免状态/证据/记忆不一致 |
| feature spec/tasks/tests 调整 | 建议 | 人类更适合批量看范围和风险 |

**通用确认表**新增 `Affects Long-Term Memory` 列，与 onboarding-db 专用表区分开来。

---

## 三、问题追踪：V1 → V3 全生命周期

| V1 问题 | 严重度 | V2 状态 | V3 状态 |
|---|---|---|---|
| 文档数量过多（31文件） | 🔴 高 | ✅ 解决（Layout Mode） | ✅ 维持 |
| 人类确认瓶颈 | 🔴 高 | ✅ 解决（批量确认） | ✅ **扩展**为通用模式 |
| 模板过于"重" | ⚠️ 中 | ✅ 解决（三层分级） | ✅ 维持 |
| 扫描流程无优先级 | ⚠️ 中 | ❌ 未解决 | ✅ **V3解决**（P0/P1/P2） |
| Subagent 协调不清晰 | ⚠️ 中 | ❌ 未解决 | ✅ **V3解决**（冲突流水线+6规则） |
| 信息碎片化/无模块路径 | ⚠️ 中 | ⚠️ 部分 | ✅ **V3解决**（模块阅读路径表） |
| 部署信息散落 | 🟡 低 | — | ✅ **V3新增**（部署运维分层） |
| Project Group 暂缓 | ⚠️ 中 | ❌ 未解决 | ❌ 仍未解决 |
| 模板版本兼容 | 🟡 低 | ❌ 未解决 | ❌ 仍未解决 |
| 扫描失败回退 | 🟡 低 | ❌ 未解决 | ❌ 仍未解决 |
| 按角色阅读路径 | 🟡 低 | ❌ 未解决 | ❌ 仍未解决 |

---

## 四、V2 新增优点（回顾，V3 维持）

### 4.1 Layout Mode — 解决了"一刀切"问题

| 模式 | 文件策略 | 适用项目 | 解决的核心矛盾 |
|---|---|---|---|
| **Compact** | 5-7 个核心文档 | 单一应用、单一技术栈、模块少 | "小项目不需要 31 个文件" |
| **Standard** | 8-12 个文档 | 常规业务系统、有 UI/API/DB/Jobs | 默认平衡态 |
| **Expanded** | 12-18 个文档 | 10万行+、5+长期模块、多测试系统 | 大项目不丢失关键细节 |

**设计精髓**：Layout Mode 控制的是**物理文件颗粒度**，不影响**理解维度完整性**。Compact 下 `code-map.md` 内部仍然覆盖 directory-map + entrypoints + 模块摘要——合并不等于省略。

### 4.2 批量确认模式 — 解决了"审批疲劳"问题

| 批次 | 包含内容 | 人类确认焦点 |
|---|---|---|
| Project Basics | overview, setup, environment, directory/code map | 项目用途、启动方式、主要目录准确性 |
| Architecture | module map, boundaries, integrations, API, async/jobs | 边界、调用方向、外部依赖 |
| Flows And Data | core flows, data model, state, diagrams | 业务链路、状态流转、核心实体 |
| Verification And Risks | testing, change impact, risks, unknowns | 测试策略、风险、未知 |
| Memory Backfill | project.md / project/*.md 回补建议 | 哪些长期事实进入 memory |

**关键设计**：高可信内容可自动草拟，但不能绕过批量确认标记为 `reviewed`——既不放水，也不折磨人类。

### 4.3 决策和历史 — 回答了"为什么"

| 记录内容 | 示例 |
|---|---|
| 架构决策 | 为什么用当前框架、数据库、部署方式 |
| 历史取舍 | 为什么某模块没重构、为什么保留兼容逻辑 |
| 迁移历史 | 从旧服务迁新服务、从同步改异步 |
| 技术债务 | 未来应该重构但暂时不能动的地方 |

解决了一个关键缺口：之前的 onboarding-db 擅长回答"是什么"和"怎么跑"，但对"为什么会这样"缺乏沉淀能力。这类知识通常只在老员工的脑子里，V2 明确要求 agent 去发现和记录。

### 4.4 模板分层 — 解决了"重模板压死人"

| 改进点 | V1 | V2 |
|---|---|---|
| 元信息字段 | 12 字段全部必填 | Core Required(5字段) / Optional / Expanded Only 三层 |
| 模板文件数 | 31 个独立模板 | 10 个核心模板 + 通用 `diagram.md` |
| 模块卡片字段 | 14 字段平铺 | Core Required(7) / Optional(6) / Expanded Only(5) |
| Compact 章节 | 未定义 | Evidence/Unknowns/Backfill 可合并为节末短表格 |

### 4.5 模板与 Layout Mode 联动

| 合并文档 | 承载模板 | 设计意图 |
|---|---|---|
| `code-map.md` | directory-map + entrypoints + 模块摘要 | 代码导航集中到一页 |
| `architecture-and-integrations.md` | module-map + boundaries + api + integrations + async | 架构全景不出一个文件 |
| `flows-and-data.md` | core-flows + data-model + jobs + 状态图 | 业务+数据集中理解 |
| `verification-and-risks.md` | testing + change-impact + risks + glossary | 质量保障一目了然 |

**关键约束**：合并后的文档必须在 README Document Index 中标明承载了哪些理解维度——合并不等于让人类找不到。

---

## 三、V1 问题追踪：哪些解决了、哪些还在

### 3.1 ✅ 已解决（V2 直接回应）

| V1 问题 | 严重程度 | V2 解决方式 | 解决度 |
|---|---|---|---|
| 文档数量过多（31文件） | 🔴 高 | Layout Mode: Compact(5-7) / Standard(8-12) / Expanded(12-18) | ✅ 完全解决 |
| 人类确认瓶颈 | 🔴 高 | 批量确认模式：4批次 + 6种人类选择 | ✅ 完全解决 |
| 模板过于"重" | ⚠️ 中 | 元信息三层分级 + 模块卡片字段分层 + Compact章节适应 | ✅ 基本解决 |
| 缺少架构历史/决策记录 | 🟡 低 | 新增 `decisions-and-history.md` 模板 | ✅ 完全解决 |

### 3.2 ⚠️ 部分解决

| V1 问题 | 现状 |
|---|---|
| **信息碎片化** | README.md 增加了 Document Index 和 Diagrams Index，但缺少"按模块"的阅读路径（如"理解支付模块：先读A→B→C"） |
| **扫描流程无优先级** | 流程仍是线性 10 步，未引入 P0/P1/P2 标注 |
| **Subagent 协调机制** | 仍只说"不能做什么"，缺少冲突处理流程 |
| **阅读路径个性化** | 仍是 5 条固定路径，缺少"按角色"（前端/后端/运维/QA） |

### 3.3 ❌ 仍未覆盖

| V1 问题 | 严重程度 | 说明 |
|---|---|---|
| **缺少全局搜索/标签索引** | ⚠️ 中 | 文件合并后这个问题稍微缓解，但仍然没有一个关键词→文件映射表 |
| **Project Group 暂缓** | ⚠️ 中 | 多项目仓库仍然只标记 candidate |
| **模板版本兼容/迁移机制** | 🟡 低 | 模板升级后旧 onboarding-db 怎么兼容没定义 |
| **扫描失败回退** | 🟡 低 | 某步扫描失败后没有 Partial Scan 模式 |

---

## 五、综合评价与结论（V3 更新）

### 5.1 一句话总结

| 版本 | 总结 |
|---|---|
| V1 | 设计得很好，但落地存在两个 P0 瓶颈 |
| V2 | 可以拿来实现，P0 瓶颈已切除 |
| **V3** | **可以直接实现了，P0+P1 问题基本清零，剩余都是 P2 锦上添花** |

### 5.2 三个版本的核心进化

| 版本 | 核心贡献 | 评分 |
|---|---|---|
| **V1** | 搭建"人类可读优先"的设计框架，建立证据+可信度+写入门禁体系 | 91.1 |
| **V2** | 引入 Layout Mode（Compact/Standard/Expanded）和批量确认，切掉落地最大障碍 | 93.5 |
| **V3** | 补全扫描优先级、Subagent 冲突处理、模块阅读路径、部署运维分层，解决执行完备性 | 94.3 |

### 5.3 V3 剩余问题（仅剩 P2 级别）

| 问题 | 严重度 | 说明 |
|---|---|---|
| Project Group 暂缓 | ⚠️ P2 | 多项目仓库仍只标记 candidate，但 proposal 明确留到后续 |
| 模板版本兼容 | 🟡 P2 | 在模板未冻结前不紧急 |
| 扫描失败回退 | 🟡 P2 | 有了 P0/P1/P2 优先级，失败时可降级输出 |
| 按角色阅读路径 | 🟡 P2 | 模块阅读路径已部分缓解 |

### 5.4 建议（V3 更新）

| 决策项 | V3 结论 |
|---|---|
| **scan.md** | ✅ **强烈建议直接进入实现**（98分，执行完备性达到可实施标准） |
| **templates.md** | ✅ **建议同步实现**（95分，模板规范已成熟） |
| **实现顺序** | P0 模板（Compact 5-7文件）→ P1 扫描流程 → Standard 派生 → Expanded 按需 |
| **4 个 P2 问题** | 不阻塞实现，可在 alpha-v1.2.1 迭代 |

---

> **V3 报告更新完毕。** 提案在三轮迭代中展示了紧凑的进化节奏：V1 搭框架 → V2 切落地障碍 → V3 补执行完备性。到 V3 为止，11 个问题中解决了 7 个（包括全部 P0 和 3 个 P1），剩余 4 个均为 P2 级别。**94.3 分**的 rating 反映了一个 **"可以直接开始实现"** 的状态。尤其值得肯定的是 scan.md（98分）——它已经从一个流程描述文档进化成了一个完整的、有优先级、有冲突处理、有降级策略的可执行规范。
