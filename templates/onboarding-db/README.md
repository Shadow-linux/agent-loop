# Onboarding Knowledge Base

> 默认中文说明；代码符号、文件路径、命令、API、配置名、错误信息和第三方产品名保持原文。

## 这是什么

这是项目接手手册入口，不是文件索引。先从 Evidence Graph 和 Onboarding Spec 确认文档可信度，再按模块、流程、运行和变更路径阅读。

## 推荐阅读路径

### 10 分钟理解项目

1. `00-overview/system-context.md`
2. `00-overview/architecture-map.md`
3. `01-domain/domain-map.md`
4. `coverage-matrix.md`

### 接手一个模块

1. `coverage-matrix.md` 找模块状态和评分。
2. `02-modules/<module-name>.md` 阅读模块手册。
3. 相关 `03-flows/<flow-name>.md` 阅读跨模块流程。
4. `07-change-guides/<change-type>.md` 查看改动路径。

### 排查线上 / 测试环境问题

1. `03-flows/<flow-name>.md` 找请求或事件链路。
2. `02-modules/<module-name>.md` 找 owner、状态对象、失败模式。
3. `06-deploy/` 和 `05-infra/` 找运行和依赖。

## 当前生产状态

- Evidence Graph：
- Onboarding Spec：
- Onboarding Tasks：
- Current Batch：
- Human Review：

## 质量要求

- `critical` / `important` 核心流程必须从触发闭合到业务终态，并通过 Flow Slice Coverage 连接代码证据、图和正文。
- 核心流程默认包含 Core Flow Overview / Boundary、ASCII State Machine / Decision、Timeline / Sequence；Timeline / Sequence 是单流程主叙事。
- 模块和其他内容文档按真实语义选图；stateless glossary、静态配置清单和纯索引不强制状态图。
- 普通流程图和时序图优先用 Mermaid flowchart / sequenceDiagram；状态机、复杂原理图和复杂示例图优先用 ASCII。
- 禁止用无边界、无状态、无数据对象的 `A-->B-->C` flowchart 当主图。
- module / flow 默认单文件长文档，不默认拆成很多小文件。
- 不允许空文件、TODO 占位、泛泛摘要。
- Completeness Hard Gate 先于质量评分；missing/blocked critical slice 不能标记 `newcomer-ready`。
