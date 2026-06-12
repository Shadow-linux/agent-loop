# Proposal: Project Onboarding DB 模板规范

状态：讨论草案
目标版本：alpha-v1.2.0
创建时间：2026-06-07

## 目的

这份 proposal 定义 `Project Onboarding DB` 的模板规范。

它不是直接实现模板文件，而是先明确：

- 每个 onboarding-db 文档必须有哪些字段；
- 每个字段解决什么问题；
- 哪些内容应该写，哪些内容不应该写；
- 证据和可信度怎么标；
- 什么时候需要配图；
- 什么时候需要回补 `project.md` 或 `project/*.md`；
- 后续 Agent 更新文档时应该遵守什么规则。

核心原则：

```text
模板不是空壳。
模板要约束 Agent 写出可验证、可阅读、可维护的项目理解资料。
```

## 模板总体规则

所有 `onboarding-db` 文档都应该使用同一套基础元信息，但不应该让元信息压过正文阅读。

模板字段分三层：

| 层级 | 作用 | 使用规则 |
|---|---|---|
| Core Required | 保证资料可信、可读、可追溯 | 所有 onboarding-db 文档必须有 |
| Optional | 在有价值时补充索引和维护信息 | 不强制每个文件都写满 |
| Expanded Only | 大项目或复杂主题才需要 | 只在 Expanded Layout 或人类要求时使用 |

每个文件顶部至少包含：

```md
# <Document Title>

Document Language:
Last Verified:
Confidence:
Source Evidence:
Human Review Status:
```

字段说明：

| 字段 | 是否必填 | 说明 |
|---|---|---|
| `Document Language` | 必填 | 正文语言，默认中文，跟随项目文档或人类协作语言 |
| `Last Verified` | 必填 | 最近核对代码现实或命令的日期 |
| `Confidence` | 必填 | high / medium / low / mixed |
| `Source Evidence` | 必填 | 关键证据来源，文件路径、命令、配置、测试 |
| `Human Review Status` | 必填 | draft / reviewed / needs-review / stale |

可选元信息：

| 字段 | 说明 |
|---|---|
| `Created` | 文档创建日期 |
| `Last Updated` | 最近内容修改日期 |
| `Freshness Window` | 默认 7 days |
| `Verification Scope` | 本次验证覆盖了哪些内容 |
| `Maintainer` | 人类或 Agent 维护者 |
| `Related Project Memory` | 对应 `project.md` 或 `project/*.md` |
| `Related Diagrams` | 关联图文件 |

在 Compact Layout 中，正文可只保留 Core Required 元信息。其他元信息可以统一集中到 `README.md` 的文档索引表中。

在 Standard / Expanded Layout 中，重要文档可以补充可选元信息，但仍然不要求所有字段机械填满。

## Layout Mode 与模板颗粒度

模板定义的是理解维度，不等于必须创建同名物理文件。

| Layout Mode | 模板使用方式 |
|---|---|
| Compact | 合并相近模板到少量文档，章节内仍保留核心字段和证据 |
| Standard | 多数核心模板独立成文件，低频主题可合并 |
| Expanded | 复杂模块、复杂流程、复杂运维主题可拆独立文件 |

Compact 合并建议：

| 合并文档 | 承载模板 |
|---|---|
| `code-map.md` | `directory-map`、`entrypoints`、模块摘要 |
| `architecture-and-integrations.md` | `module-map`、`architecture-boundaries`、`api-surface`、`integrations`、`async-and-events` |
| `flows-and-data.md` | `core-flows`、`data-model`、`jobs-and-schedules`、关键状态图 |
| `verification-and-risks.md` | `testing-and-verification`、`change-impact-map`、`risks-and-unknowns`、`glossary` 摘要 |

Standard 拆分建议：

| 类型 | 建议独立 |
|---|---|
| 主阅读路径 | README、overview、setup、directory、module、boundaries、core-flows、testing、risks |
| 项目存在才独立 | async、jobs、api、integrations、data-model |
| 复杂才独立 | decisions-and-history、deployment、security、observability |

Expanded 拆分建议：

| 触发 | 可拆文件 |
|---|---|
| 模块长期边界清晰 | `module-<name>.md` |
| 核心链路很长或跨进程 | `flow-<name>.md` |
| 多套部署/环境 | `deployment-and-operations.md` |
| 权限复杂 | `security-and-permissions.md` |
| 历史决策多 | `design-decisions.md`、`architecture-history.md` |

合并后的文档必须在 `README.md` 的 `Document Index` 中标明承载了哪些理解维度，避免人类找不到内容。

## 统一章节结构

每个正文文档都应尽量使用下面结构。

```md
## Purpose

## How To Read

## Key Facts

## Details

## Evidence

## Unknowns

## Update Rules

## Project Memory Backfill
```

章节说明：

| 章节 | 作用 |
|---|---|
| `Purpose` | 这个文档帮助人类解决什么理解问题 |
| `How To Read` | 人类应该如何读这个文档，先看哪里 |
| `Key Facts` | 最重要的结论，优先给人类快速理解 |
| `Details` | 结构化细节 |
| `Evidence` | 支撑结论的代码、配置、命令、测试 |
| `Unknowns` | 不确定、冲突、待确认 |
| `Update Rules` | 什么时候更新，更新前需要什么确认 |
| `Project Memory Backfill` | 哪些内容需要同步到 `project.md` 或 `project/*.md` |

Compact Layout 中可以把 `Evidence`、`Unknowns`、`Project Memory Backfill` 合并成每节末尾的短表格；Standard / Expanded 中再独立成章节。

## 人类可读格式规则

`onboarding-db` 是给人类接管项目时阅读的资料库，默认应该偏向报告式、人类可读格式。

核心规则：

```text
先摘要，再表格，再图，最后证据和未知。
Human-readable first.
Table-first when comparing, scanning, listing, or reviewing.
```

推荐格式：

| 内容类型 | 推荐格式 |
|---|---|
| 项目总览 | 短摘要 + 表格 |
| 技术栈 | 表格 |
| 启动命令 | 表格 |
| 环境变量 | 表格 |
| 目录职责 | 表格 |
| 模块职责 | 模块卡片 + 表格 |
| API 面 | 表格 |
| 定时任务 | 表格 |
| 异步链路 | 表格 + 流程图 |
| 状态机 | 表格 + 状态图 |
| 风险未知 | 表格 |
| 阅读路径 | 表格 |
| 证据 | 表格或短列表 |
| 业务背景 | 短段落 |
| 业务流程 | 简短说明 + 流程图 |

写作要求：

- 不写成 Agent 运行日志。
- 不写成大段自言自语。
- 多对象对比默认用表格。
- 跨模块、跨进程、跨状态、跨时间的内容优先用图。
- 背景和意图用短段落，不强行表格化。
- 证据保留在每节末尾或专门的 `Evidence` 区域，避免打断阅读。

示例结构：

```md
## Key Facts

| Item | Value | Evidence | Confidence |
|---|---|---|---|

## What To Read First

| Goal | Read | Why |
|---|---|---|

## Risks

| Risk | Impact | Evidence | Follow-Up |
|---|---|---|---|
```

如果某项不存在，写：

```text
Not applicable
```

如果扫描未发现，写：

```text
Not found
```

如果无法确认，写：

```text
Unknown
```

不能把未知写成确定事实。

## 证据和可信度规则

所有重要事实都应该有证据和可信度。

可信度定义：

| 可信度 | 含义 |
|---|---|
| high | 已通过代码、配置、测试、命令或 CI 明确验证 |
| medium | 从代码结构或脚本推断，但未实际运行 |
| low | 文档提到或命名暗示，但缺少代码/命令验证 |
| mixed | 同一主题下不同事实可信度不同 |

证据格式：

```md
- Fact:
  - Evidence:
  - Confidence:
  - Last Verified:
```

命令证据格式：

```md
- Command:
  - Purpose:
  - Evidence:
  - Last Run:
  - Result:
  - Confidence:
```

路径证据格式：

```md
- Path:
  - Role:
  - Evidence:
  - Confidence:
```

## 写入确认规则

`onboarding-db` 面向人类阅读，所有写入和更新都需要人类确认。

写入前，Agent 应该展示：

| 项 | 内容 |
|---|---|
| 目标文件 | 准备创建或更新哪个文档 |
| 变更类型 | create / update / refresh / correct / diagram |
| 变更摘要 | 这次会新增或修改什么 |
| 证据 | 代码、配置、命令、测试、文档 |
| 可信度 | high / medium / low / mixed |
| 是否影响长期事实 | 是 / 否 |
| 是否需要回补 project memory | 是 / 否 |
| 是否需要人类确认业务事实 | 是 / 否 |

写入后，Agent 应该汇报：

```text
Updated files
Evidence used
Remaining unknowns
Suggested next read
Project memory backfill status
```

## Batch Human Review 模板

Deep Project Onboarding Scan 不应该让人类为每个小文件单独确认。

这个模板也应该作为 agent-loop 的通用文档确认模板。凡是 Agent 准备新建/修改多个文档、多个条目、多个长期事实时，都应该优先使用表格批量确认。

Agent 应该先生成批次摘要，再让人类批量选择。

通用批量确认模板：

```md
## Batch Human Review: <stage-or-topic>

| File / Item | Action | Change Summary | Source Evidence | Confidence | Affects Long-Term Memory | Suggested Action |
|---|---|---|---|---|---|---|
```

Onboarding DB 批次摘要模板：

```md
## Onboarding DB Review Batch: <name>

| File | Change Summary | Key Facts | Evidence | Confidence | Needs Human Fact Check | Suggested Action |
|---|---|---|---|---|---|---|
```

建议批次：

| Batch | Typical Files |
|---|---|
| Project Basics | README、overview、setup/environment、directory/code map |
| Architecture | module、boundary、API、integration、async/jobs |
| Flows And Data | core flows、data model、state diagrams、flow diagrams |
| Verification And Risks | testing、change impact、risks、unknowns、glossary |
| Memory Backfill | project.md / project/*.md 回补建议 |

人类选择项：

| Choice | 行为 |
|---|---|
| approve all | 写入当前批次并标记 reviewed |
| approve selected | 只写入选中的文件或事实 |
| revise selected | 修改后再次展示批次摘要 |
| defer selected | 暂不写入，保留为 draft 或 unknown |
| skip this batch | 不写入当前批次 |

可信度高的事实可以进入草案，但不能绕过批量确认直接成为 reviewed。

适用范围：

| 场景 | 是否使用 |
|---|---|
| onboarding-db 文档创建/更新 | 必须 |
| project memory backfill | 必须 |
| AGENTS.md / CLAUDE.md 更新 | 必须 |
| drift check 回补 | 必须 |
| close feature 前最终文档同步 | 必须 |
| feature spec / tasks / tests / plan 生成或调整 | 建议 |

## 禁止内容

模板应阻止 Agent 写入这些内容：

| 禁止内容 | 原因 |
|---|---|
| 没证据的确定性结论 | 会误导新人 |
| 全量文件树 | 信息噪音太大 |
| 全量函数调用关系 | 不适合作为人类接管入口 |
| 开发过程流水账 | 应放 feature `notes.md` |
| 当前任务状态 | 应放 `project.md` 或 feature 文档 |
| 未确认的业务决策 | 需要人类确认 |
| 密钥、token、真实密码 | 安全风险 |
| 与项目无关的通用教程 | 稀释项目理解资料 |

## README.md 模板字段

目标：作为 onboarding-db 的阅读导航。

必须字段：

```md
# Project Onboarding DB

Document Language:
Last Verified:
Freshness Window:
Project Scope:
Confidence:

## What This DB Is

## How To Start Reading

## Reading Paths

## Document Index

## Diagrams Index

## Freshness Status

## Human Review Notes
```

`Reading Paths` 必须包含：

| 路径 | 必须包含 |
|---|---|
| 10 分钟快速接管 | `overview.md`、`setup-and-run.md`、`directory-map.md` |
| 准备开发需求 | `architecture-boundaries.md`、`module-map.md`、`change-impact-map.md`、`testing-and-verification.md` |
| 排查问题 | `entrypoints.md`、`core-flows.md`、`risks-and-unknowns.md` |
| 理解异步 | `async-and-events.md`、`jobs-and-schedules.md`、相关 diagrams |
| 理解数据 | `data-model.md`、`diagrams/data-entity-map.md` |

禁止写：

- 长篇项目细节；
- 任务状态；
- 具体 feature 计划。

## overview.md 模板字段

目标：一页看懂项目。

必须字段：

```md
# Overview

## Project Purpose

## Users / Actors

## Product Capabilities

## Tech Stack

## Runtime Shape

## Main Modules

## Core Flows Summary

## Start Here

## Evidence

## Unknowns
```

`Product Capabilities` 推荐表格：

| Capability | Status | Evidence | Confidence |
|---|---|---|---|

`Tech Stack` 推荐表格：

| Layer | Technology | Evidence | Confidence |
|---|---|---|---|

## setup-and-run.md 模板字段

目标：帮助新人把项目跑起来。

必须字段：

```md
# Setup And Run

## Prerequisites

## Install Dependencies

## Required Services

## Local Run Commands

## Ports And URLs

## Common Startup Failures

## Verification After Startup

## Evidence

## Unknowns
```

命令表格：

| Command | Purpose | Working Directory | Evidence | Last Run | Result | Confidence |
|---|---|---|---|---|---|---|

必须记录：

- 运行目录；
- 依赖服务；
- 端口；
- 环境文件；
- 最小验证方式。

## environment.md 模板字段

目标：说明配置、环境变量、运行环境差异。

必须字段：

```md
# Environment

## Environment Files

## Required Variables

## Optional Variables

## Environment Modes

## Secrets Handling

## Local / Test / Prod Differences

## Containers / Remote Runtime

## CI Environment

## Evidence

## Unknowns
```

环境变量表格：

| Variable | Required | Used By | Source | Safe To Commit | Evidence | Confidence |
|---|---|---|---|---|---|---|

禁止写真实密钥和密码。

## deployment-and-operations.md 模板字段

目标：说明生产部署、发布流程、运行拓扑、回滚和线上排障入口。

这个文档不是所有项目都必须独立存在：

| Layout Mode | 放置方式 |
|---|---|
| Compact | 放在 `setup-and-run.md` 的 `Deployment Notes`，或 `architecture-and-integrations.md` 的 `Runtime / Deployment` 小节 |
| Standard | 基础环境放 `environment.md`；部署较复杂时独立创建 |
| Expanded | 独立 `deployment-and-operations.md`，并关联 `diagrams/deployment-map.md` |

必须字段：

```md
# Deployment And Operations

## Deployment Overview

## Environments

## Deployment Pipeline

## Runtime Topology

## Release / Rollback

## Migrations / Seeds

## Health Checks

## Logs / Metrics / Tracing

## Operational Access

## Related Diagrams

## Evidence

## Unknowns
```

部署环境表格：

| Environment | Runtime | Deploy Trigger | Config Source | URL / Entry | Owner | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

发布流程表格：

| Step | Command / System | Working Directory | Preconditions | Rollback | Evidence | Confidence |
|---|---|---|---|---|---|---|

运维入口表格：

| Entry | Purpose | Where | Safe Access Notes | Evidence | Confidence |
|---|---|---|---|---|---|

必须关联或说明：

```text
diagrams/deployment-map.md
```

禁止写真实密钥、token、密码、生产连接串。只能记录变量名、配置来源、用途、安全说明和是否需要人类权限。

## directory-map.md 模板字段

目标：告诉新人主要目录从哪里看。

必须字段：

```md
# Directory Map

## How To Navigate

## Main Directories

## Generated / Vendor / Ignored Areas

## Test Directories

## Config And Scripts

## Documentation Areas

## Evidence

## Unknowns
```

目录表格：

| Path | Responsibility | Read First? | Related Module | Evidence | Confidence |
|---|---|---|---|---|---|

禁止写全量文件树。

## module-map.md 模板字段

目标：说明每个长期模块或子系统做什么。

必须字段：

```md
# Module Map

## Module Summary

## Module Details

## Module Relationship Notes

## Related Diagrams

## Evidence

## Unknowns
```

每个模块必须有模块卡片：

```md
## Module: <name>

Purpose:
Boundary:
Entrypoints:
Core Flows:
Key Files:
Evidence:
Confidence:
```

模块卡片字段分层：

| 层级 | 字段 |
|---|---|
| Core Required | Purpose、Boundary、Entrypoints、Core Flows、Key Files、Evidence、Confidence |
| Optional | Depends On、Called By、Key Data、Configuration、Tests、Risks |
| Expanded Only | Operational Notes、Runtime Ownership、Deployment Unit、Observed Failure Modes、Related Decisions |

Agent 不应该为了填满卡片而编造信息。没有发现或无法确认的字段应写 `Not found` 或 `Unknown`，也可以放入 `risks-and-unknowns.md`。

如果模块没有独立业务流程，也要写支持性职责，例如 shared types、generated client、storage adapter、test utilities。

必须关联：

```text
diagrams/module-relationship-map.md
```

## architecture-boundaries.md 模板字段

目标：说明系统分层、边界和调用方向。

必须字段：

```md
# Architecture Boundaries

## Boundary Overview

## Boundary Table

## Allowed Dependency Direction

## Cross-Boundary Contracts

## Boundary Risks

## Related Diagrams

## Evidence

## Unknowns
```

边界表格：

| Boundary | Responsibility | Entrypoints | Talks To | Must Not Know | Evidence | Confidence |
|---|---|---|---|---|---|---|

必须关联：

```text
diagrams/boundary-map.md
```

## core-flows.md 模板字段

目标：说明核心业务链路。

必须字段：

```md
# Core Flows

## Flow Index

## Core Flow: <name>

## Evidence

## Unknowns
```

每条业务链路字段：

```md
## Core Flow: <name>

User / Trigger:
Start Point:
End State:
Modules Involved:
Steps:
Data Changed:
External Systems:
Async Parts:
Failure Points:
Verification:
Related Diagram:
Key Files:
Evidence:
Confidence:
```

至少一条核心业务链路必须有图：

```text
diagrams/core-flow-<name>.md
```

## entrypoints.md 模板字段

目标：告诉新人代码从哪里进入。

必须字段：

```md
# Entrypoints

## Runtime Entrypoints

## UI Entrypoints

## API Entrypoints

## Config Entrypoints

## Job / Worker Entrypoints

## Test Entrypoints

## Evidence

## Unknowns
```

入口表格：

| Entrypoint | Type | Path | What Starts Here | Related Module | Evidence | Confidence |
|---|---|---|---|---|---|---|

## data-model.md 模板字段

目标：说明核心实体、表、聚合、状态机。

必须字段：

```md
# Data Model

## Entity Summary

## Entities / Tables

## Relationships

## State Machines

## Migrations / Schema Sources

## Related Diagrams

## Evidence

## Unknowns
```

实体表格：

| Entity | Purpose | Storage | Key Fields | Relationships | Evidence | Confidence |
|---|---|---|---|---|---|---|

状态机表格：

| Entity | State Field | States | Transitions | Diagram | Evidence | Confidence |
|---|---|---|---|---|---|---|

发现状态机时必须建议图：

```text
diagrams/state-flow-<entity>.md
```

存在持久化数据时必须关联：

```text
diagrams/data-entity-map.md
```

## api-surface.md 模板字段

目标：说明 API 面、消费者和契约风险。

必须字段：

```md
# API Surface

## API Groups

## Consumers

## Authentication / Authorization

## Generated Clients

## Contract Risks

## Related Diagrams

## Evidence

## Unknowns
```

API 表格：

| API Group | Entrypoint | Consumer | Auth | Generated Client | Tests | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

如果调用链复杂，建议图：

```text
diagrams/api-call-flow-<name>.md
```

## async-and-events.md 模板字段

目标：说明异步调用、事件、队列、回调和补偿。

必须字段：

```md
# Async And Events

## Async Flow Index

## Producers

## Queues / Brokers

## Consumers

## Callbacks / Webhooks

## Retry / DLQ / Compensation

## Observability

## Related Diagrams

## Evidence

## Unknowns
```

每条异步链路字段：

```md
## Async Flow: <name>

Trigger:
Producer:
Message / Event:
Queue / Broker:
Consumer:
State Changes:
Retry:
DLQ:
Idempotency:
Callback / Webhook:
Observability:
Verification:
Related Diagram:
Evidence:
Confidence:
```

发现异步链路时必须建议图：

```text
diagrams/async-flow-<name>.md
```

## jobs-and-schedules.md 模板字段

目标：说明定时任务、后台任务、worker、scheduler。

必须字段：

```md
# Jobs And Schedules

## Job Index

## Scheduled Jobs

## Background Workers

## Queue Consumers

## Operational Notes

## Related Diagrams

## Evidence

## Unknowns
```

任务字段：

```md
## Job: <name>

Trigger:
Schedule:
Entrypoint:
Dependencies:
Data Affected:
Failure Impact:
Retry / Compensation:
Observability:
Manual Run:
Verification:
Related Diagram:
Evidence:
Confidence:
```

发现定时或后台任务时必须建议图：

```text
diagrams/job-flow-<name>.md
```

## change-impact-map.md 模板字段

目标：帮助开发前判断改需求会影响哪里。

必须字段：

```md
# Change Impact Map

## Change Categories

## Impact Table

## Test Selection Guide

## Risky Change Types

## Related Diagrams

## Evidence

## Unknowns
```

影响表格：

| Change Type | Likely Modules | Likely Files | APIs | Data | Tests To Run | Risks | Evidence |
|---|---|---|---|---|---|---|---|

如果影响跨多个模块，建议图：

```text
diagrams/change-impact-map.md
```

## testing-and-verification.md 模板字段

目标：说明测试体系和验证方式。

必须字段：

```md
# Testing And Verification

## Test Systems

## Fast Checks

## Full Checks

## E2E / Browser Checks

## Manual Verification

## Known Baseline Failures

## Test Data / Fixtures

## Evidence

## Unknowns
```

测试命令表格：

| Command | Test Type | Scope | Working Directory | Last Run | Result | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

## integrations.md 模板字段

目标：说明外部服务、SDK、存储、第三方 API。

必须字段：

```md
# Integrations

## Integration Index

## External Services

## SDKs / Clients

## Storage / Queue / Cache

## Webhooks / Callbacks

## Credentials / Config

## Related Diagrams

## Evidence

## Unknowns
```

集成表格：

| Integration | Type | Used By | Config | Failure Impact | Tests | Evidence | Confidence |
|---|---|---|---|---|---|---|---|

callback 或 webhook 必须关联：

```text
diagrams/integration-flow-<name>.md
```

## risks-and-unknowns.md 模板字段

目标：集中记录不确定、冲突、待确认。

必须字段：

```md
# Risks And Unknowns

## High-Risk Unknowns

## Documentation Conflicts

## Unverified Commands

## Missing Diagrams

## Human Questions

## Follow-Up Scans
```

风险表格：

| Item | Risk | Evidence | Confidence | Suggested Follow-Up | Owner |
|---|---|---|---|---|---|

## decisions-and-history.md 模板字段

目标：记录关键设计决策、历史取舍、迁移背景和技术债，让新人理解“为什么这样设计”。

这个文档不是每个项目都必须独立存在：

| Layout Mode | 放置方式 |
|---|---|
| Compact | 放在 `architecture-and-integrations.md` 的 `Decisions And History` 小节 |
| Standard | 独立 `decisions-and-history.md` |
| Expanded | 可拆为 `design-decisions.md`、`architecture-history.md`、`technical-debt.md` |

建议字段：

```md
# Decisions And History

## Decision Index

## Decision: <name>

## Architecture History

## Tradeoffs

## Current Technical Debt

## Evidence

## Unknowns
```

单条决策字段：

| 字段 | 说明 |
|---|---|
| Decision | 决策内容 |
| Context | 当时的背景和约束 |
| Alternatives | 已知备选方案 |
| Why This Choice | 选择原因 |
| Consequences | 带来的收益和代价 |
| Current Status | active / superseded / unknown |
| Evidence | 文档、代码、commit、issue、PR 或人类确认 |
| Confidence | high / medium / low |

如果只有代码证据，只能说明“现在是什么”，不能强行推断“当时为什么这么做”。原因类结论通常需要现有文档、历史记录或人类确认。

## glossary.md 模板字段

目标：记录领域语言、缩写、角色定义。

必须字段：

```md
# Glossary

## Domain Terms

## Roles

## Acronyms

## Synonyms / Naming Conflicts

## Evidence

## Unknowns
```

术语表格：

| Term | Chinese Meaning | English Meaning | Used In | Synonyms / Aliases | Evidence | Confidence |
|---|---|---|---|---|---|---|

`Synonyms / Aliases` 用来记录缩写、旧名称、冲突命名、中英文别名、同义业务词。

长期稳定术语应建议回补：

```text
project/domain-language.md
```

## 图模板统一规范

所有图文档都应该是 Markdown + Mermaid。

统一字段：

```md
# Diagram: <name>

Document Language:
Created:
Last Updated:
Last Verified:
Diagram Type:
Question Answered:
Scope:
Source Evidence:
Confidence:

## Diagram

## How To Read

## Notes

## Unknowns
```

图必须回答一个具体问题。

禁止：

- 一张图画完整仓库；
- 一张图塞太多流程；
- 用图展示复杂度而不是帮助定位；
- 没有证据的推测关系。

## Mermaid 类型建议

| 图 | Mermaid 类型 | 说明 |
|---|---|---|
| `module-relationship-map.md` | `flowchart LR` | 模块依赖关系 |
| `boundary-map.md` | `flowchart LR` | 系统边界和调用方向 |
| `core-flow-<name>.md` | `sequenceDiagram` 或 `flowchart TD` | 业务链路 |
| `async-flow-<name>.md` | `sequenceDiagram` | 事件、队列、worker、callback |
| `job-flow-<name>.md` | `flowchart TD` | 定时或后台任务 |
| `state-flow-<entity>.md` | `stateDiagram-v2` | 状态机 |
| `data-entity-map.md` | `erDiagram` 或 `flowchart LR` | 实体关系 |
| `api-call-flow-<name>.md` | `sequenceDiagram` | API 调用链 |
| `integration-flow-<name>.md` | `sequenceDiagram` | 第三方集成 |
| `auth-flow.md` | `sequenceDiagram` 或 `flowchart TD` | 鉴权链路 |
| `file-flow-<name>.md` | `sequenceDiagram` | 文件上传下载 |
| `failure-recovery-flow.md` | `flowchart TD` | 失败补偿 |
| `deployment-map.md` | `flowchart LR` | 部署与环境 |
| `change-impact-map.md` | `flowchart LR` | 改动影响 |

## 最小合格标准

初始 onboarding-db 合格标准：

| 项 | 标准 |
|---|---|
| README | 有阅读路径和文档索引 |
| overview | 能一页说明项目用途、栈、能力 |
| setup-and-run | 有最小启动路径和验证方式 |
| directory-map | 能告诉新人从哪些目录开始看 |
| module-map | 每个长期模块都有模块卡片 |
| diagrams | 有模块关系图、边界图、至少一张核心流程图 |
| async/jobs | 若发现异步或任务，必须有文档和图建议 |
| testing | 有最小验证命令和完整验证命令 |
| risks | 所有不确定和冲突都有记录 |
| confidence | 关键事实都有证据和可信度 |
| human review | 写入前后都有确认和状态 |

不满足这些条件时，Agent 不能说 onboarding-db 完整，只能说：

```text
Onboarding DB draft is usable but incomplete.
```

## 与 Project Memory 的关系

模板中所有长期事实都要判断是否回补 project memory。

`project.md` 是 agent-loop 的运行入口和索引，不应该承担解释整个项目细节的责任。

推荐问题路由：

```text
project.md answers: 当前做到哪、下一步做什么、长期事实索引在哪。
onboarding-db answers: 项目是什么、怎么跑、怎么理解、模块怎么协作、流程怎么走。
code reality answers: 当前真实实现是什么。
```

当 `project.md` 不足以回答人类或 Agent 的项目理解问题时，Agent 应该转向 `onboarding-db/`。如果 `onboarding-db/` 仍不足以回答，或文档可能过期，再读取代码现实并建议更新 onboarding-db。

问题路由表：

| 问题类型 | 优先读取 |
|---|---|
| 当前 active feature / next action | `project.md` |
| 项目整体用途、技术栈、核心能力 | `onboarding-db/overview.md` |
| 怎么启动、配置、测试 | `onboarding-db/setup-and-run.md`、`environment.md`、`testing-and-verification.md` |
| 目录和模块职责 | `onboarding-db/directory-map.md`、`module-map.md` |
| 模块之间关系 | `onboarding-db/diagrams/module-relationship-map.md` |
| 系统边界 | `onboarding-db/architecture-boundaries.md`、`diagrams/boundary-map.md` |
| 核心业务链路 | `onboarding-db/core-flows.md`、`diagrams/core-flow-*.md` |
| 异步队列、订阅消费、callback | `onboarding-db/async-and-events.md`、`diagrams/async-flow-*.md` |
| 定时任务和后台任务 | `onboarding-db/jobs-and-schedules.md`、`diagrams/job-flow-*.md` |
| 实体、数据模型、状态机 | `onboarding-db/data-model.md`、`diagrams/state-flow-*.md` |
| 改需求影响范围 | `onboarding-db/change-impact-map.md` |
| 文档不确定或冲突 | `onboarding-db/risks-and-unknowns.md` + 代码现实 |

约束：

```text
onboarding-db 可以帮助理解，但不能替代代码现实。
如果 onboarding-db 和代码冲突，以代码现实为当前事实基础，然后建议修正 onboarding-db。
```

回补规则：

| Onboarding DB 内容 | 可能回补位置 |
|---|---|
| 核心能力摘要 | `project/capabilities.md` |
| 主要命令和验证策略 | `project/commands.md` / `project/testing.md` |
| 架构边界 | `project/boundaries.md` / `project/architecture.md` |
| 领域语言 | `project/domain-language.md` |
| 产品上下文 | `project/product-context.md` |
| 环境事实 | `project/environments.md` |

回补仍需人类确认。

## 后续实现建议

如果本 proposal 被接受，下一步实现时应：

1. 新增少量核心模板：`README.md`、`overview.md`、`setup-and-run.md`、`code-map.md`、`architecture-and-integrations.md`、`flows-and-data.md`、`verification-and-risks.md`、`decisions-and-history.md`、`deployment-and-operations.md`、`batch-review.md`、`diagram.md`。
2. 允许 Standard / Expanded Layout 从核心模板派生细分文档，但不要为每一种图或每一个主题默认创建独立模板文件。
3. 新增 `references/onboarding-db-templates.md`，承载这份模板字段规范。
4. 新增 `references/onboarding-db.md`，负责 Onboarding DB 生命周期、读取、写入、Freshness Check 和问题路由。
5. 更新 `references/project-onboarding-scan.md`，负责 Deep Project Onboarding Scan 流程。
6. 更新 `references/existing-project-onboarding.md`，只作为旧项目接管入口、Quick Onboarding 主流程和 Quick / Deep / Targeted 选择门禁。
7. 更新 `references/validation-scenarios.md`，加入模板字段缺失、Layout Mode、Batch Human Review、P0/P1/P2 优先级、Subagent 冲突合并、模块阅读路径、部署分层、Targeted Onboarding Scan、决策历史压力场景。
8. 确保 Agent 创建或更新 onboarding-db 前展示 Human Review Summary 或 Batch Review Summary。
