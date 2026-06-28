# Proposal: Learning-Path-First Onboarding

状态：讨论草案

目标版本：v1.2.3 / v1.2.x

创建时间：2026-06-28

## 目的

重构 `agent-loop` 的 onboarding 能力，把它从“生成一组项目文档 / deep-dive 文档”调整为“构建一条新人学习路径”。

新的 onboarding-db 应该帮助人类和未来 Agent 从宏观到微观理解项目：

```text
项目为什么存在
→ 系统边界和参与者
→ 多项目 / 多组件关系
→ 对外能力
→ 主流程如何跨组件流动
→ 领域模型和核心概念
→ 代码组件如何承载领域逻辑
→ 运行、配置、测试、排障
→ 变更影响和验证策略
→ 必要 deep-dive 证据链
```

`onboarding-db` 不是代码目录镜像，也不是一次性喷文件。它是一个可持续维护的项目理解知识库。

## 背景问题

近期 onboarding 方案经历了多轮补丁，留下几个概念混乱点：

- `Existing Project Onboarding` 同时承担项目记忆初始化和新人文档建设，职责过重。
- `Deep Onboarding` 过度聚焦 `deep-dives/<topic>.md`，缺少从宏观到微观的学习路径骨架。
- `Focused Onboarding` 容易在“回答一个问题”和“沉淀一个知识库主题”之间摇摆。
- 多项目 / 前后端 / worker / shared package 一体仓库缺少统一讲法。
- 旧方案从 Graph-first、template-first、spec-first 多次变化，proposal 历史已经无法作为清晰参考。
- 网站化查看是正确方向，但不应抢在 Markdown 知识模型稳定前实施。

因此删除旧 onboarding proposals，保留本 proposal 作为后续设计和实施的单一参考。

## 核心原则

1. `project.md` 服务 Agent 执行；`onboarding-db` 服务新人理解。
2. onboarding-db 是学习路径，不是代码目录镜像。
3. 先讲系统为什么存在，再讲它由哪些组件组成。
4. 多项目 / 前后端项目必须用纵向主流程串起来。
5. component docs 负责导航，deep dives 负责讲透。
6. deep dives 数量由项目事实和新人接手需要决定，不设总量上限。
7. 人类给的示例只代表详细程度和解释质量，不代表 topic、数量、领域词或项目结构。
8. onboarding-db 默认中文；代码符号、命令、路径、API、环境变量、配置名、错误信息保持原文。
9. Markdown 是 source of truth；未来网站只是生成的阅读体验。

## 三层职责模型

### 1. Project Entry Scan

目标：让 Agent 能安全进入项目并继续工作。

输出范围：

- `.agent-loop/project.md`
- root `AGENTS.md` / `CLAUDE.md` 状态
- 项目命令、边界、运行形态、低置信未知项
- 是否建议进入 onboarding-db 建设

明确不负责：

- 生成新人长文档
- 生成 deep-dive
- 生成网站
- 试图讲完整项目

### 2. Onboarding Knowledge Base

目标：让新人从宏观到微观理解项目。

输出范围：

- 学习路径
- 系统上下文
- 多项目 / 多组件地图
- 能力地图
- 主流程
- 领域模型
- 组件地图
- 运行与操作
- 变更与验证
- deep dives
- coverage

### 3. Guided / Focused Use

目标：使用已有 onboarding-db 回答问题；发现缺口时产生小的知识库更新建议。

行为：

- 先读现有 onboarding-db。
- 如果现有文档足够，直接解释并推荐下一步。
- 如果文档缺失、过薄、过期或和代码冲突，提出 focused update proposal。
- focused update 不重跑全量 onboarding。
- 只有发现稳定项目事实缺失时，才建议 project memory backfill。

## 推荐 onboarding-db 信息架构

```text
.agent-loop/onboarding-db/
  README.md
  system-context.md
  project-map.md
  capability-map.md
  main-flows.md
  domain-model.md
  component-map.md
  runtime-and-operations.md
  change-and-verification.md
  deep-dives/
    <topic>.md
  coverage-matrix.md
  batch-review.md
```

### README.md：学习路径入口

`README.md` 不是简单文件索引，而是学习路线。

它应该回答：

- 10 分钟了解项目，按什么顺序读？
- 接手业务改动，按什么顺序读？
- 本地运行和排障，按什么顺序读？
- 修改一个前端 / 后端 / worker / shared package，按什么路径读？
- 哪些 deep dives 是必读？
- 哪些主题还没写完或需要人类确认？

示例结构：

```text
## 10 分钟了解项目
1. system-context.md
2. project-map.md
3. capability-map.md

## 接手一个业务改动
1. main-flows.md
2. domain-model.md
3. component-map.md
4. related deep-dives/<topic>.md
5. change-and-verification.md

## 本地运行 / 排障
1. runtime-and-operations.md
2. component-map.md
3. change-and-verification.md
```

### system-context.md：系统为什么存在

讲项目最高层语义：

- 系统服务谁？
- 解决什么业务问题？
- 外部用户 / 调用方 / 系统是谁？
- 核心能力是什么？
- 哪些事情明确不归它管？
- 项目的主要风险或业务约束是什么？

这份文档让新人先建立产品和系统心智模型。

### project-map.md：多项目 / 多组件地图

讲仓库或项目组里有哪些东西，尤其覆盖前后端一体项目：

- frontend app
- backend service / API
- BFF / gateway / OpenResty / Nginx
- worker / scheduled job / consumer
- shared packages / SDK / generated client
- DB / Redis / MQ / object storage
- third-party provider
- deployable unit vs code package
- 本地开发时哪些组件必须一起跑

重点不是列目录，而是解释组件角色和关系。

### capability-map.md：能力地图

按“用户或系统能做什么”组织，而不是按接口列表组织。

每个能力应该连接：

```text
能力名称
→ 前端入口
→ 后端入口
→ 领域逻辑
→ 数据 / 状态
→ 外部依赖
→ 相关测试
→ 相关 deep dives
```

示例：

```text
能力：用户登录
- 前端入口：LoginPage / route
- 后端入口：POST /auth/login
- 领域逻辑：AuthService
- 数据：users / sessions / tokens
- 风险：token 过期、权限刷新
- 相关 deep dive：deep-dives/auth-login.md
```

### main-flows.md：纵向主流程

多项目最容易乱，是因为只按项目或目录讲。`main-flows.md` 必须按业务纵向链路讲。

典型链路：

```text
用户点击前端按钮
→ frontend route / component
→ API client
→ backend controller / route
→ application service
→ domain logic
→ DB / Redis / MQ / external provider
→ response / event / async job
→ frontend state update
```

每条主流程至少要有：

- 业务目标
- 触发入口
- 参与组件
- 跨项目调用链
- 数据读写
- 状态变化
- 失败 / 重试 / 降级
- 验证方式
- 相关 deep dive

### domain-model.md：领域模型

讲项目自己的“名词宇宙”，先讲概念关系，再落到技术实现。

应该覆盖：

- 核心实体 / 概念
- 概念之间的关系
- 谁拥有事实来源
- 哪些状态字段关键
- 谁能改变状态
- 对应 DB table / ORM model / API field / frontend state
- 常见误解

它不是数据字典，也不是完整 schema dump。

### component-map.md：组件导航

讲每个 app / service / package 的职责和入口。

每个组件统一格式：

```text
## <component-name>

职责：
部署单元还是代码包：
主要目录：
入口：
调用谁：
被谁调用：
依赖的 shared packages：
数据 / 外部依赖：
本地启动：
测试方式：
常见改动路径：
相关主流程：
相关 deep dives：
```

这份文档只负责导航，不负责讲透全部细节。

### runtime-and-operations.md：运行、配置、操作、排障

讲怎么跑、怎么部署、怎么排障。

多项目必须有组件运行矩阵：

| Component | Start Command | Port | Env File | Depends On | Health Check | Common Failure |
|---|---|---|---|---|---|---|
| frontend |  |  |  |  |  |  |
| api |  |  |  |  |  |  |
| worker |  |  |  |  |  |  |

还应覆盖：

- 本地启动顺序
- 环境变量和配置来源
- 外部依赖
- 常见启动失败
- 日志 / 指标 / health check
- 生产和测试环境差异

### change-and-verification.md：变更影响和验证

新人接手项目最需要知道“改哪里会影响哪里”。

应覆盖：

- 改前端页面，需要测哪些 API / E2E？
- 改 API schema，会影响哪些 frontend client？
- 改领域逻辑，会影响哪些 jobs / callbacks？
- 改 DB 字段，要看哪些 migrations / seed / tests？
- 改 shared package，哪些 app 会被影响？
- 哪些测试命令或人工验证路径对应哪些改动？
- 哪些风险需要 human review？

### deep-dives/<topic>.md：核心专题深挖

deep dive 只写必须讲透的东西。

适合 deep dive 的主题：

- 主要业务闭环
- 跨前后端关键流程
- 高风险数据流
- 状态机
- 异步任务
- 支付 / 计费 / 权限 / 模型调用等核心领域
- 常被人问、常被改、容易出事故的路径

不建议：

- 按目录创建 deep dive
- 为普通 helper / utils 创建 deep dive
- 因为模板存在而创建 deep dive
- 限制总 deep dive 数量

deep dive 标准结构：

```text
业务意义
参与组件
入口
阶段化流程
代码证据
数据读写
状态变化
失败 / 重试 / 补偿
验证方式
变更风险
阅读顺序
```

### coverage-matrix.md：学习覆盖状态

coverage 跟踪的是学习成果，不是文件数量。

状态建议：

| Status | Meaning |
|---|---|
| discovered | 已发现但还没计划 |
| planned | 已进入 onboarding plan |
| needs-deep-dive | 必须深入讲，但还没写透 |
| draft-deep-dive | deep dive 草稿存在但未 review |
| newcomer-ready | 人类确认新人可读 |
| supporting-summary | 支撑主题，放在 overview/map/index 即可 |
| blocked-by-unknown | 缺代码证据或业务确认 |
| not-applicable | 明确不适用 |

## 生成顺序

### Phase 1：Entry Scan

先完成 Project Entry Scan，只建立 Agent 可安全工作的项目记忆。

输出：

- `project.md`
- root guidance 状态
- 命令 / 边界 / 风险 / 未知项
- 是否建议做 onboarding-db

### Phase 2：Learning Path Spec

如果人类要新人接手文档，先写 `onboarding-spec.md`：

- 目标读者
- 学习目标
- required-core topic inventory
- 不做什么
- 文档语言：中文
- 质量标准
- 人类确认点

### Phase 3：Learning Skeleton

先生成学习骨架，不急着写 deep dives：

- `README.md`
- `system-context.md`
- `project-map.md`
- `capability-map.md`
- `main-flows.md`
- `domain-model.md`
- `component-map.md`
- `runtime-and-operations.md`
- `change-and-verification.md`
- `coverage-matrix.md`

这些文档可以先是高置信概要，但必须形成从宏观到微观的学习路径。

### Phase 4：Deep-Dive Batches

基于 coverage 和人类优先级，分批写 deep dives。

规则：

- 不设总数量上限。
- 默认每批 1-3 篇，只作为 review 节奏。
- 每篇必须有代码证据和数据 / 状态 / 验证路径。
- deep dive 数量由项目事实和新人接手需要决定。

### Phase 5：Guided Use And Refresh

后续人类问问题时：

1. 先读 onboarding-db。
2. 如果能回答，直接解释并推荐下一步。
3. 如果文档缺口明显，提出 focused update。
4. 如果发现稳定项目事实缺失，提出 project memory backfill。

## 多项目 / 前后端一体项目规则

多项目 onboarding 必须避免两种失败：

1. 只按项目分文件，导致新人不知道业务流量怎么跨组件走。
2. 只讲主流程，导致新人不知道每个组件怎么启动、测试、修改。

因此必须同时具备：

- `project-map.md`：组件角色和依赖。
- `main-flows.md`：纵向业务链路。
- `component-map.md`：每个组件的入口、职责、启动、测试。
- `change-and-verification.md`：跨组件变更影响。

主流程优先级高于目录结构。一个跨前后端流程应该用一个纵向 deep dive 讲透，而不是拆成 frontend doc + backend doc 后让读者自己拼。

## 默认中文规则

onboarding-db 默认使用中文：

- 叙事说明：中文
- 表格说明：中文
- 风险 / 未知项：中文
- 阅读路径：中文

保持原文：

- 文件路径
- 命令
- API path
- class / function / variable
- env var
- config key
- error message
- third-party product name

## Website 方向，暂缓实施

固定网站是正确方向，但不是本轮主力。

本 proposal 只保留原则：

```text
Markdown = source of truth
Website = generated reading experience
```

未来 website 应该：

- 从 onboarding-db Markdown 生成。
- 提供学习路径首页。
- 渲染 Mermaid / HTML 图。
- 支持搜索和 coverage dashboard。
- 不成为事实来源。
- 不替代 deep-dive 证据链。

本轮先把 learning-path-first onboarding 做好，再单独设计 website。

## 需要删除 / 替代的旧概念

删除旧 proposal 后，正式实现时也应逐步清理这些概念：

- Graph-first onboarding 作为主模型。
- Quick / Deep / Targeted 作为并列模式。
- Compact / Standard / Expanded layout mode。
- template-first 文档生成。
- 按目录生成 module/flow 文档。
- deep dive 总数上限。
- 示例 topic 复用。

保留但重新定义：

- focused question：变成 Guided / Focused Use 的知识缺口更新。
- project memory backfill：只回填稳定项目事实，不搬运长文档。
- deep-dives：只负责讲透核心专题，不承担整体学习路径。

## 验收标准

实施后，agent-loop 应满足：

- 人类要求“接管旧项目”时，Agent 先区分 Project Entry Scan 和 onboarding-db。
- 人类要求“新人能接手”时，Agent 先建立 learning path skeleton，再分批 deep dive。
- 多项目 / 前后端一体项目必须有项目地图、主流程、组件地图和变更验证。
- onboarding-db 默认中文。
- deep dives 不设总数量上限。
- 人类示例只作为详细程度参考。
- website 不在本轮实施范围内。

## 建议实施顺序

1. 重写 onboarding 概念文档和 runtime/stage/checklist 入口。
2. 重构 onboarding-db 模板目录。
3. 更新 validation scenarios，覆盖多项目 / 前后端 / focused use / 中文默认。
4. 移除或改写旧 spec-first deep-dive-only 规则。
5. 压测真实项目输出质量。
6. 通过后再讨论 generated onboarding website。
