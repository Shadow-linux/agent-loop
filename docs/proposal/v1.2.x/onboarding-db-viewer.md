# Proposal: Onboarding DB Viewer

状态：讨论草案
目标版本：未定
创建时间：2026-06-08

## 目的

`Onboarding DB Viewer` 是 `.agent-loop/onboarding-db/` 的可视化阅读层。

它的目标不是替代 Markdown，也不是生成全量代码知识图谱，而是把 onboarding-db 中已经沉淀的项目理解资料，以更适合人类接管项目的方式展示出来：

- 一页看懂项目是什么；
- 快速知道项目怎么启动、怎么验证；
- 看到模块、边界、核心流程、异步任务、部署路径之间的关系；
- 点击模块能看到关键文件路径、文件解释、相关流程和测试；
- 在需要时查看关键代码片段或打开本地文件；
- 通过阅读路径引导新人从“完全不懂”到“可以开始开发”。

## 核心观点

```text
Markdown 是事实源。
Viewer 是阅读层。
代码是最终现实。
Agent 负责维护 onboarding-db，Viewer 负责帮助人类理解。
```

三者的职责不能混淆：

| 对象 | 作用 | 是否事实源 |
|---|---|---|
| `.agent-loop/onboarding-db/*.md` | 人类可读项目理解资料，支持 review 和 diff | 是 |
| `onboarding-db-viewer` | 前端交互展示，帮助理解模块、流程、影响面 | 否 |
| 源代码 | 当前实现现实 | 是，优先级最高 |
| `viewer-data.json` / `viewer-manifest.json` | 从 Markdown 和扫描结果派生的前端索引 | 否，派生数据 |

Viewer 不应该直接成为新的项目记忆系统。它应该能从 onboarding-db 重新生成。

## 反目标

| 不做什么 | 原因 |
|---|---|
| 不默认展示完整仓库文件树 | 信息太多，接管效率低 |
| 不默认展示完整原始代码 | 容易把新人淹没，违背 onboarding 目标 |
| 不生成全量函数调用图 | 人类很难消费，维护成本高 |
| 不让 Viewer 修改 onboarding-db | 写入仍由 Agent 走 Batch Human Review |
| 不把 Viewer 当成任务状态系统 | feature/task/plan/notes 仍属于 agent-loop artifacts |
| 不上传源码或敏感信息到外部服务 | 本地优先，保护代码和配置 |

## 产品定位

推荐名称：

```text
Onboarding DB Viewer
```

它是 agent-loop 的可选增强能力：

```text
Project Onboarding Scan
-> onboarding-db markdown
-> viewer data index
-> local web viewer
```

第一版建议做成本地静态站或本地开发服务，优先支持：

- 打开本地 `.agent-loop/onboarding-db/`；
- 读取 Markdown 和派生 JSON；
- 展示项目地图；
- 不要求后端数据库；
- 不要求账号系统。

## 页面信息架构

### 1. Overview

回答：“这个项目是什么？”

展示内容：

| 区块 | 数据来源 |
|---|---|
| 项目用途 / 用户 / 核心能力 | `overview.md` |
| 技术栈 | `overview.md`, `setup-and-run.md`, manifest evidence |
| 启动命令 | `setup-and-run.md` |
| 测试命令 | `verification-and-risks.md` 或 `testing-and-verification.md` |
| 核心模块 | `code-map.md`, `module-map.md`, `module-*.md` |
| 核心流程 | `flows-and-data.md`, `core-flows.md`, `flow-*.md` |
| 当前 unknowns / risks | `verification-and-risks.md`, `risks-and-unknowns.md` |

页面形态：

- 顶部 summary cards；
- 中部 “10 分钟阅读路径”；
- 下方模块 / 流程 / 风险入口。

### 2. Module Explorer

回答：“这个模块做什么？从哪些文件开始看？”

模块页默认展示：

| 信息 | 说明 |
|---|---|
| Module Purpose | 模块职责，一两段即可 |
| Boundary | 该模块负责什么，不负责什么 |
| Core Call Chain | 模块级调用链图 |
| Entrypoints | 入口文件、路由、job、handler、component |
| Key Files | 关键文件路径、角色、是否优先阅读 |
| Related Flows | 相关业务流程 |
| Dependencies | 上游/下游模块或外部服务 |
| Tests | 覆盖该模块的测试文件或命令 |
| Risks / Unknowns | 不确定项 |
| Evidence / Confidence | 事实依据和可信度 |

关键文件表建议字段：

| 字段 | 含义 |
|---|---|
| `path` | 文件路径 |
| `role` | 文件角色，例如 route / service / domain / model / test |
| `why_it_matters` | 为什么新人需要看它 |
| `summary` | 文件大意 |
| `important_symbols` | 关键函数、类、组件、类型 |
| `related_flows` | 参与哪些流程 |
| `related_tests` | 哪些测试覆盖 |
| `confidence` | 高 / 中 / 低 |
| `evidence` | 来源 Markdown 或代码路径 |

默认不展开完整代码。

推荐交互：

```text
模块卡片
-> 关键文件表
-> 点击文件
   -> 文件解释
   -> 关键符号
   -> 相关流程 / 测试
   -> 关键代码片段
   -> 打开完整文件 / 展开完整代码
```

### 3. Flow Explorer

回答：“这条业务链路怎么走？”

展示内容：

| 信息 | 说明 |
|---|---|
| Flow Summary | 起点、参与者、终点、业务结果 |
| Flow Diagram | 小图，展示模块/系统级步骤 |
| Steps | 每一步的 actor/module/action/data/failure path |
| Entrypoints / Exits | 入口和出口 |
| Data / State Changes | 数据和状态变化 |
| Async / Job / External Behavior | 队列、订阅、回调、worker、外部服务 |
| Verification | 如何验证该流程 |
| Related Modules / Files | 关联模块和关键文件 |

Viewer 应优先展示“小图 + 步骤表”，而不是全量调用图。

### 4. Architecture Map

回答：“系统边界在哪里？谁调用谁？”

展示内容：

- UI / API / Domain / DB / Jobs / External Services 边界；
- 模块关系图；
- 外部服务 / SDK / queue / cache / storage；
- contract 或 public interface；
- 方向性依赖。

图的原则：

```text
边界图 > 全仓库依赖图
模块图 > 文件图
业务流程图 > 函数调用图
```

### 5. Change Impact Map

回答：“我要改一个需求，会影响哪里？”

展示内容：

| 输入 | 输出 |
|---|---|
| 选择一个模块 | 影响的 flows、files、tests、contracts、risks |
| 选择一个 flow | 影响的 modules、data、API、jobs、E2E |
| 选择一个文件 | 文件角色、所属模块、相关流程、测试 |
| 输入需求关键词 | 推荐相关模块和阅读路径 |

第一版可以先做静态筛选，不做复杂搜索。

### 6. Code File View

回答：“这个文件大概做什么？我是否需要读源码？”

建议三层展示：

| 层级 | 内容 | 默认 |
|---|---|---|
| 文件路径 | path、role、所属模块、相关流程 | 展示 |
| 文件解释 | summary、responsibilities、important symbols、call relations、tests | 展示 |
| 原始代码 | 关键片段或完整文件 | 按需展开 |

不建议默认展示完整代码。

原因：

- 完整代码会打断新人阅读路径；
- 大文件会让页面噪音过高；
- onboarding 的目标是理解项目，不是替代 IDE；
- 原始代码应该作为证据层或深挖层。

推荐能力：

| 能力 | 说明 |
|---|---|
| Open local file | 用本地编辑器打开文件 |
| Show snippet | 展示 Agent 提取的关键代码片段 |
| Show full file | 高级展开，默认折叠 |
| Explain stale risk | 如果文件解释不是最新，显示 stale / unknown |

## Viewer 需要的数据

这是最容易复杂化的地方。建议分成三类数据。

### A. 已有 Markdown 可直接提供的数据

这些来自 onboarding-db 当前模板：

| 数据 | 来源 |
|---|---|
| 项目总览 | `overview.md` |
| 阅读路径 | `README.md` |
| 文档索引 | `README.md` |
| 图索引 | `README.md` |
| 模块列表 | `code-map.md`, `module-map.md`, `module-*.md` |
| 模块职责 | `module-template.md` 字段 |
| 模块入口 | `Entrypoints` 表 |
| 关键文件路径 | `Key Files` 表 |
| 业务流程 | `flows-and-data.md`, `flow-*.md` |
| 流程步骤 | `flow-template.md` 字段 |
| 异步/任务/外部行为 | `flow-template.md`, `architecture-and-integrations.md` |
| 测试和验证 | `verification-and-risks.md`, `testing-and-verification.md` |
| 风险 unknowns | 各文档 `Risks And Unknowns` |
| 证据和 confidence | 每个文档 metadata 和表格字段 |

这些足以做第一版 Viewer。

### B. 需要派生索引的数据

Markdown 适合人读，但前端需要统一索引。

建议生成：

```text
.agent-loop/onboarding-db/.viewer/
  manifest.json
  modules.json
  flows.json
  files.json
  diagrams.json
  search-index.json
```

派生数据不是事实源，可以删除后重新生成。

核心 JSON 形状示意：

```json
{
  "project": {
    "name": "",
    "summary": "",
    "lastVerified": "",
    "confidence": "",
    "sourceDocs": []
  },
  "modules": [
    {
      "id": "billing",
      "name": "Billing",
      "purpose": "",
      "boundary": "",
      "entrypoints": [],
      "keyFiles": [],
      "relatedFlows": [],
      "relatedTests": [],
      "diagrams": [],
      "confidence": "medium",
      "sourceDocs": []
    }
  ]
}
```

### C. 需要额外扫描才能更好的数据

这些不是第一版必须，但会显著提升体验：

| 数据 | 价值 | 风险 |
|---|---|---|
| 文件摘要 | 模块页更易读 | 需要 Agent 额外扫描，可能 stale |
| important symbols | 快速知道读哪些函数/类 | 需要语言解析或 LSP/AST |
| call relations | 文件/模块关系更清楚 | 容易变成全量调用图 |
| code snippets | 直接看到关键实现 | 可能太长或泄露敏感逻辑 |
| test coverage relation | 知道改哪跑哪 | 需要测试结构分析 |

建议第一版只做：

```text
文件路径 + 文件角色 + 文件解释 + 关键符号（可选） + 相关测试
```

不做全量 call graph。

## Agent 需要如何生成数据

推荐在 Deep / Targeted Onboarding Scan 后增加一个可选步骤：

```text
Generate Viewer Index
```

流程：

```text
Read onboarding-db markdown
-> Extract metadata tables
-> Normalize modules / flows / files / diagrams
-> Detect missing required fields
-> Draft .viewer/*.json
-> Batch Human Review if generated summaries add new interpretation
-> Write derived index
```

派生规则：

| 情况 | 是否需要人类确认 |
|---|---|
| 只从已 reviewed Markdown 复制结构化字段 | 不需要单独确认，可生成 |
| Agent 新增文件解释、符号解释、关系判断 | 需要 Batch Human Review |
| 发现 Markdown 缺字段 | 不直接补，提出 onboarding-db 更新建议 |
| 发现 code reality 与 docs 冲突 | 标记 stale / conflict，走 Targeted Scan |

## 技术实现建议

第一版推荐静态 Viewer：

| 方案 | 说明 | 推荐度 |
|---|---|---|
| 静态站 + JSON index | 读取 `.viewer/*.json` 展示 | 推荐 |
| Vite/React 本地 app | 开发体验好，适合交互图 | 推荐 |
| Next.js 全功能站 | 偏重，需要后端时再考虑 | 暂不推荐 |
| 直接 Markdown 渲染器 | 快，但交互弱 | 可作为 fallback |

推荐技术：

```text
Vite + React + TypeScript
Mermaid / React Flow
Fuse.js 或 mini search index
本地 file opener 作为可选能力
```

如果作为 agent-loop skill 的能力，不应该要求目标项目安装前端依赖。可以有两种模式：

| 模式 | 说明 |
|---|---|
| bundled viewer | agent-loop skill 自带 viewer 模板 |
| generated static viewer | 生成到 `.agent-loop/onboarding-db-viewer/` 或临时目录 |

## 文件位置建议

不要把 Viewer 源码默认塞进目标项目。

建议：

```text
skills/agent-loop/viewer/              # skill 自带 viewer 源码或模板

目标项目：
.agent-loop/onboarding-db/
  README.md
  ...
  .viewer/
    manifest.json
    modules.json
    flows.json
    files.json
    diagrams.json
```

本地预览时：

```text
agent-loop viewer serve .agent-loop/onboarding-db
```

或者由 Agent 启动本地 dev server。

## 页面草图

```text
┌──────────────────────────────────────────────┐
│ Project Name        Freshness: needs-review   │
├───────────────┬──────────────────────────────┤
│ Reading Paths │ Overview                     │
│ Modules       │ - Purpose                    │
│ Flows         │ - Stack                      │
│ Architecture  │ - Run / Test                 │
│ Impact Map    │ - Risks                      │
│ Files         │                              │
├───────────────┴──────────────────────────────┤
│ Module Relationship / Core Flow Preview       │
└──────────────────────────────────────────────┘
```

模块页：

```text
Module: Billing

Purpose / Boundary
Core Call Chain Diagram

Key Files
| Path | Role | Why it matters | Tests | Confidence |

Related Flows
Dependencies
Risks / Unknowns
Evidence
```

文件详情：

```text
File: src/billing/service.ts

Summary
Responsibilities
Important Symbols
Related Flows
Related Tests
Code Snippets
[Open local file] [Show full file]
```

## 与 agent-loop 的关系

Viewer 不改变现有主流程，只增加可选能力。

触发场景：

| 用户说法 | 行为 |
|---|---|
| “把 onboarding-db 可视化” | 进入 Viewer Proposal / Generate Viewer Index |
| “我想用网页看项目接管资料” | 建议生成 viewer index 并启动本地 viewer |
| “这个模块看不懂” | 先 Targeted Onboarding Scan，再更新 viewer index |
| “开始开发功能” | 从 Viewer/Onboarding 回到正常 Feature Loop |

Stop condition：

- 生成新的文件解释需要确认；
- 生成新的代码摘要需要确认；
- 展示完整源码前需要确认敏感性；
- 发现 stale/conflict 需要回到 Targeted Scan；
- Viewer 不允许自行改 `project.md`、feature docs、task status。

## 第一版范围

建议 v0 做：

| 能力 | 是否做 |
|---|---|
| 读取 `.viewer/*.json` | 做 |
| Overview 页面 | 做 |
| Reading Paths | 做 |
| Module Explorer | 做 |
| Flow Explorer | 做 |
| Diagram 展示 | 做 |
| File path + file explanation | 做 |
| Code snippets | 可选 |
| Full code viewer | 折叠按需 |
| 全量调用图 | 不做 |
| 自动编辑 onboarding-db | 不做 |
| 在线部署 | 不做 |

## 需要补充到 onboarding-db 的数据

为了让 Viewer 更好用，后续 onboarding scan 应该更稳定地产出这些字段：

| 字段 | 放在哪里 | 用途 |
|---|---|---|
| `Module ID` | module docs / module map | 前端路由和关联 |
| `Flow ID` | flow docs / flow map | 前端路由和关联 |
| `File Role` | Key Files 表 | 文件分类 |
| `Why It Matters` | Key Files 表 | 告诉新人为什么读 |
| `Important Symbols` | file summary 或 module docs | 快速定位代码 |
| `Related Tests` | module / file tables | 改动验证 |
| `Related Diagrams` | metadata | 图索引 |
| `Viewer Tags` | 可选 metadata | 搜索和筛选 |

这些字段不应该一次性强塞到所有 Markdown 模板中。建议先由 Viewer Index 派生，不足时再反向提出 onboarding-db 模板补强。

## 风险

| 风险 | 应对 |
|---|---|
| Viewer 数据 stale | 显示 Last Verified / confidence / source evidence |
| 页面太炫但不好用 | 默认阅读路径和模块/流程小图优先 |
| 代码展示过多 | 默认摘要和关键片段，完整代码按需 |
| 生成 JSON 与 Markdown 不一致 | JSON 只做派生，可重新生成 |
| 增加维护负担 | 第一版静态、本地、只读 |
| 安全和隐私 | 不上传源码，不展示 secrets，不默认发布 |

## 开放问题

1. Viewer 是 agent-loop skill 自带，还是每个项目生成一份静态 HTML？
2. 文件解释是写回 onboarding-db，还是只放在 `.viewer/files.json`？
3. 是否需要本地 “Open in Editor” 能力？
4. 是否允许查看完整源码，还是只展示 snippets？
5. 是否需要搜索？第一版可只做简单客户端搜索。
6. 是否需要截图/导出 onboarding report？暂不建议第一版做。

## 建议结论

建议接受这个能力，但按两阶段做：

```text
Phase 1: Viewer Index
先定义 .viewer/*.json，从 onboarding-db 稳定提取页面数据。

Phase 2: Local Viewer
再实现本地可视化网站，展示 Overview、Modules、Flows、Architecture、Impact、Files。
```

这样可以先解决最难的问题：页面到底需要什么数据，以及这些数据是否能从 onboarding-db 稳定获得。
