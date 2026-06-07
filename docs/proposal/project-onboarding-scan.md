# Proposal: Project Onboarding Scan 与 Onboarding DB

状态：讨论草案
目标版本：alpha-v1.2.0
创建时间：2026-06-07

## 目的

`Project Onboarding Scan` 是 agent-loop 的项目接管理解能力。

它的目标不是生成一张全量代码关系图，而是帮助新人、人类负责人、以及新进入项目的 Agent 快速回答：

- 这个项目是做什么的；
- 怎么启动、怎么配置、怎么测试；
- 代码应该从哪里开始看；
- 核心业务链路怎么走；
- 改一个需求通常会影响哪些目录、接口和测试；
- 当前项目有哪些风险、不确定和文档冲突；
- 哪些内容应该回补到 agent-loop 的长期项目记忆。

这份 proposal 同时定义 `Project Onboarding DB`：一个面向人类阅读的项目接管资料库。

## 核心观点

```text
Project Onboarding Scan 是接管项目的扫描流程。
Project Onboarding DB 是扫描后沉淀出来的人类可读资料库。
project.md 是 agent-loop 的运行入口和记忆索引。
```

三者不能互相替代。

| 对象 | 主要读者 | 作用 |
|---|---|---|
| `project.md` | Agent | 当前状态、Active Feature、Next Action、长期记忆索引、运行路由 |
| `onboarding-db/` | 人类 + Agent | 新人接管项目时阅读的项目理解资料库 |
| `project/*.md` | Agent | enterprise mode 下的长期事实分片 |
| `features/<feature>/` | Agent + 人类审核 | 单个 feature 的 spec、task、test、plan、notes |

## 反目标

`Project Onboarding Scan` 不做这些事：

| 不做什么 | 原因 |
|---|---|
| 不默认生成全量函数调用图 | 对人类接管帮助低，信息爆炸 |
| 不默认生成全仓库文件依赖图 | 容易变成炫技图，不利于定位问题 |
| 不深扫每个文件 | 成本高，也会让 Agent 偏离接管目标 |
| 不把所有发现都塞进 `project.md` | 大项目会让 project memory 失控 |
| 不替代 feature scan | onboarding 负责建立地图，具体需求仍走 Targeted Feature Scan |
| 不静默写入文档 | `onboarding-db` 面向人类，写入必须确认 |

## 触发场景

| 场景 | 行为 |
|---|---|
| 新人说“带我接管这个项目” | 进入 Guided Onboarding |
| 项目没有 `.agent-loop/` | Existing Project Onboarding 前运行 Project Onboarding Scan |
| 项目已有 `.agent-loop/` 但文档很薄 | 建议补一次 Project Onboarding Scan |
| 项目一段时间没用 agent-loop | Re-Adopt 时运行轻量 Project Onboarding Scan + Recovery Backfill |
| 大仓库或复杂单项目 | 先运行拓扑和边界扫描，再决定是否拆模块 |
| 人类问“这个项目怎么看/怎么跑/怎么改” | 读取或更新 onboarding-db |
| onboarding-db 超过 7 天未验证且有人要接管 | 先做 Freshness Check |

## 接管模式

接管旧项目时，Agent 不应该默认运行重扫描。

Agent 应该先向人类解释两种模式，并说明收益、成本和产物。

| 模式 | 目标 | 产物 | 成本 |
|---|---|---|---|
| Quick Onboarding | 让 Agent 能安全进入后续 feature 开发 | `.agent-loop/project.md`、基础目录、必要 `AGENTS.md` / `CLAUDE.md` 建议 | 较快，文档少 |
| Deep Project Onboarding Scan | 让人类和 Agent 都能理解项目，适合新人接管和长期维护 | Quick 全部产物 + `.agent-loop/onboarding-db/` + 必要图 + 更完整证据和可信度 | 较慢，生成文件多 |

入口提示建议：

```text
我可以做两种接管：

1. Quick Onboarding：较快，建立 agent-loop 基础项目记忆，适合马上进入功能开发。
2. Deep Project Onboarding Scan：更完整，会生成 onboarding-db、模块图、边界图、核心流程图、异步/任务图，适合新人接管和长期维护，但会花更久并生成较多文档。

你希望先做哪一种？
```

Deep Project Onboarding Scan 包含 Quick Onboarding 的全部基础产物。

Deep 至少包含：

| 产物 | 说明 |
|---|---|
| `.agent-loop/project.md` | agent-loop 运行入口和项目记忆索引 |
| `.agent-loop/requirements/` | 需求材料归档目录或索引 |
| `.agent-loop/features/` | feature workspace 根目录 |
| 根目录 `AGENTS.md` | Agent 工作流引导，写入前确认 |
| 根目录 `CLAUDE.md` | 通常指向 `AGENTS.md`，写入前确认 |
| `.agent-loop/onboarding-db/` | 人类可读项目接管资料库 |
| `onboarding-db/diagrams/` | 模块关系、边界、核心流程等必要图 |
| Project Memory Backfill Proposal | 哪些长期事实需要回补 `project.md` 或 `project/*.md` |

如果人类拒绝 Deep：

```text
只做 Quick Onboarding。
不生成 onboarding-db。
不画图。
只建立足够继续开发的 project.md 和必要 guidance。
后续需要时再补 Deep Project Onboarding Scan。
```

可选折中：

| 模式 | 用法 |
|---|---|
| Targeted Onboarding Scan | 只扫描某个模块、业务链路、异步任务或问题区域 |

## 输出位置

默认根位置：

```text
.agent-loop/
  onboarding-db/
```

Onboarding DB 的核心目标是更好阅读，不是为了缩减而省略关键信息。

每个项目都应该覆盖同一套理解维度，但物理文件数量和拆分深度可以按阅读压力分层。换句话说：

```text
信息维度统一。
物理文件数量分层。
合并是为了更好阅读，不是为了少写关键信息。
```

## Onboarding DB Layout Mode

Deep Project Onboarding Scan 应该先判断或询问 `Onboarding DB Layout Mode`，再决定生成多少物理文件。

| 模式 | 适用项目 | 文件策略 | 目标 |
|---|---|---|---|
| Compact | 单一应用、单一技术栈、模块少、异步少、测试体系简单 | 5 到 7 个核心文档，合并相近主题 | 让新人 10 到 20 分钟能读完主路径 |
| Standard | 常规业务系统，有 UI/API/DB/jobs 或多个长期模块 | 8 到 12 个文档，核心主题独立，低频主题合并 | 在可读性和完整性之间平衡 |
| Expanded | 10 万行以上、5 个以上长期模块、2 套以上测试系统、复杂异步/多环境/多外部集成 | 12 到 18 个文档，必要主题独立拆分 | 支持大项目接管和长期维护 |

切换信号：

| 信号 | 建议 |
|---|---|
| 单一应用、单一运行命令、无复杂异步 | Compact |
| 有前后端/API/DB/background job 中的多个边界 | Standard |
| 5 个以上长期模块或 bounded context | Expanded |
| 2 套以上测试系统 | Expanded |
| 多环境、多部署入口、多外部集成 | Standard 或 Expanded |
| 人类明确要求快速接管 | Compact，后续按问题补充 |
| 人类明确要求完整接管文档 | Standard 或 Expanded |

Layout Mode 只影响“怎么组织文档”，不影响“必须理解什么”。

例如 Compact 模式下，`api-surface`、`integrations`、`async-and-events` 可以合并到 `architecture-and-integrations.md`；`data-model`、`jobs-and-schedules` 可以合并到 `operations-and-data.md`。如果扫描发现某一块复杂度上升，Agent 应该建议把对应主题从合并文档拆出来。

建议文件布局：

### Compact Layout

```text
.agent-loop/onboarding-db/
  README.md
  overview.md
  setup-and-run.md
  code-map.md
  architecture-and-integrations.md
  flows-and-data.md
  verification-and-risks.md
  diagrams/
```

### Standard Layout

```text
.agent-loop/onboarding-db/
    README.md
    overview.md
    setup-and-run.md
    environment.md
    directory-map.md
    module-map.md
    architecture-boundaries.md
    core-flows.md
    entrypoints.md
    data-model.md
    api-surface.md
    async-and-events.md
    jobs-and-schedules.md
    change-impact-map.md
    testing-and-verification.md
    integrations.md
    risks-and-unknowns.md
    glossary.md
    diagrams/
      module-relationship-map.md
      boundary-map.md
      core-flow-<name>.md
      async-flow-<name>.md
      job-flow-<name>.md
      state-flow-<entity>.md
      api-call-flow-<name>.md
      integration-flow-<name>.md
      auth-flow.md
      file-flow-<name>.md
      failure-recovery-flow.md
      data-entity-map.md
      deployment-map.md
      change-impact-map.md
```

### Expanded Layout

Expanded Layout 以 Standard Layout 为基础，在下列主题复杂时进一步拆分：

```text
.agent-loop/onboarding-db/
  decisions-and-history.md
  security-and-permissions.md
  deployment-and-operations.md
  observability.md
  module-<name>.md
  flow-<name>.md
```

Expanded 不应该无脑按所有模块拆文件。只有当一个模块有清晰边界、独立入口、独立测试、独立数据或独立业务流程时，才建议拆成独立模块文档。

每个项目都应该使用同一套信息骨架。差异只在内容深浅和承载方式，不在是否缺少关键要点。

必备骨架：

| 类别 | 必须覆盖 |
|---|---|
| 项目总览 | 项目用途、用户、技术栈、核心能力、当前状态 |
| 运行验证 | 启动、配置、环境、测试、构建、lint/typecheck |
| 代码导航 | 主要目录、模块职责、入口文件、关键文件 |
| 架构理解 | 模块关系、边界图、外部依赖、数据模型 |
| 业务理解 | 每个核心模块做什么、核心业务链路、关键状态流转 |
| 改动判断 | 改需求会影响哪些模块、接口、数据、测试 |
| 风险未知 | 不确定结论、文档冲突、无法验证内容 |

可以允许某个文件内容很短，但不应该因为项目小就省略这个理解维度。若某项不存在，也要明确写 `Not found`、`Not applicable` 或 `Unknown`，并附证据或原因。

## Batch Human Review

`onboarding-db` 写入仍然需要人类确认，但 Deep Scan 不应该让人类为几十个小文件逐个确认。

这个规则也应该扩展为 agent-loop 的通用确认方式：

```text
凡是 Agent 准备新建/修改多个文档、多个条目、多个长期事实时，
默认用表格给人类做批量确认。
```

适用场景：

| 场景 | 是否使用 Batch Human Review | 原因 |
|---|---|---|
| 新建/修改 onboarding-db 文档 | 必须 | 面向人类接管，文件和事实通常较多 |
| project memory backfill | 必须 | 会影响长期 Agent 行为 |
| AGENTS.md / CLAUDE.md 更新 | 必须 | 会影响后续 Agent 工作方式 |
| drift check 后回补 | 必须 | 需要明确代码现实和文档差异 |
| close feature 前最终文档同步 | 必须 | 关闭前要避免状态、证据、记忆不一致 |
| feature spec 修改 | 建议 | 需求/范围变化需要人类快速审阅 |
| tasks/tests/plan 生成或调整 | 建议 | 人类更适合批量看范围、风险、验证 |

Agent 应该先自动形成草案和证据摘要，然后按批次请求确认。

通用确认表：

| 文件/条目 | 操作 | 变更摘要 | 来源证据 | 可信度 | 是否影响长期记忆 | 建议动作 |
|---|---|---|---|---|---|---|

建议批次：

| 批次 | 包含内容 | 人类主要确认什么 |
|---|---|---|
| Project Basics | overview、setup、environment、directory/code map | 项目用途、启动方式、主要目录是否准确 |
| Architecture | module map、boundaries、integrations、API、async/jobs | 边界、调用方向、外部依赖是否准确 |
| Flows And Data | core flows、data model、state、diagrams | 业务链路、状态流转、核心实体是否准确 |
| Verification And Risks | testing、change impact、risks、unknowns | 测试策略、风险、未知是否准确 |
| Memory Backfill | project.md / project/*.md 回补建议 | 哪些长期事实进入 agent-loop memory |

每个批次汇报应该用表格：

| 文件 | 变更摘要 | 证据 | 可信度 | 是否需要人类确认业务事实 | 建议动作 |
|---|---|---|---|---|---|

人类可以选择：

```text
approve all
approve selected
revise selected
defer selected
skip this batch
```

高可信内容可以自动草拟，但不能自动标记为 `reviewed`。只有人类确认后，`Human Review Status` 才能从 `draft` 变成 `reviewed`。

## 决策和历史

Onboarding DB 不应该只有结构化卡片，也应该保留关键架构决策和历史取舍，帮助新人理解“为什么这样设计”。

建议记录：

| 内容 | 示例 |
|---|---|
| 架构决策 | 为什么使用当前框架、队列、数据库、部署方式 |
| 历史取舍 | 为什么某模块没有重构、为什么保留兼容逻辑 |
| 迁移历史 | 从旧服务迁到新服务、从同步改异步 |
| 约束条件 | 团队、成本、性能、合规、外部系统限制 |
| 当前债务 | 未来应该重构但暂时不能动的地方 |

按 Layout Mode 放置：

| 模式 | 放置方式 |
|---|---|
| Compact | 放在 `architecture-and-integrations.md` 的 `Decisions And History` 小节 |
| Standard | 独立 `decisions-and-history.md` |
| Expanded | 可拆为 `design-decisions.md`、`architecture-history.md`、`technical-debt.md` |

这类内容仍然必须标证据和可信度。代码能证明“现在是什么”，但“为什么当时这么做”通常需要现有文档、commit/PR、issue 或人类确认。

## 文档语言策略

`onboarding-db` 是给人类接管项目时阅读的资料库，正文语言应该优先服务人类理解。

语言选择规则：

| 信号 | 建议语言 |
|---|---|
| 项目现有 README / docs / AGENTS / CLAUDE 主要使用中文 | 中文 |
| 人类主要用中文发问或协作 | 中文 |
| 项目现有文档主要使用英文，团队也用英文协作 | 英文 |
| 项目文档语言混杂，无法判断 | 默认中文 |

默认规则：

```text
Default Onboarding DB Language: Chinese
```

稳定 artifact 名称、文件名、stage 名称、技术术语可以保留英文，例如 `Project Onboarding Scan`、`onboarding-db`、`core-flows.md`、`API`、`worker`、`callback`。

`onboarding-db/README.md` 应该记录：

```text
Document Language: 中文
Language Evidence: existing docs / human conversation / project convention
```

如果后续人类要求切换语言，Agent 应该先展示影响范围并请求确认，不要混写一半中文一半英文导致资料库难读。

## README.md 作为阅读导航

`onboarding-db/README.md` 必须告诉人类每个文件是做什么的，以及从哪里开始读。

建议包含：

```text
适用范围
最后验证时间
可信度说明
10 分钟快速接管路径
准备开发需求的阅读路径
排查问题的阅读路径
文档目录说明
需要刷新或确认的内容
```

阅读路径示例：

| 目标 | 推荐阅读 |
|---|---|
| 10 分钟快速接管 | `README.md` -> `overview.md` -> `setup-and-run.md` -> `directory-map.md` |
| 准备开发新需求 | `overview.md` -> `architecture-boundaries.md` -> `change-impact-map.md` -> `testing-and-verification.md` |
| 排查问题 | `entrypoints.md` -> `core-flows.md` -> `risks-and-unknowns.md` -> `testing-and-verification.md` |
| 理解某个模块 | `README.md` -> 模块阅读路径 -> `module-map.md` 或 `module-<name>.md` -> 相关 flow / diagram |
| 理解数据 | `data-model.md` -> `diagrams/data-entity-map.md` |
| 理解后台任务 | `jobs-and-schedules.md` -> `integrations.md` |

README 还应该提供按模块的阅读路径，避免人类只能看到文件索引，却不知道“我要理解支付模块/会议纪要模块/登录模块时先看哪里”。

模块阅读路径表：

| 模块 | 先读 | 再读 | 相关图 | 适合的问题 |
|---|---|---|---|---|
| `<module>` | `module-map.md#<module>` | `core-flows.md#<flow>` | `diagrams/<flow>.md` | 这个模块做什么、入口在哪、改它影响谁 |

如果使用 Compact Layout，模块阅读路径可以指向合并文档里的章节，例如 `code-map.md#<module>`、`flows-and-data.md#<flow>`。

## 文档内容定义

| 文档 | 内容 |
|---|---|
| `README.md` | 使用说明、阅读路径、更新时间、可信度、文件目录说明 |
| `overview.md` | 一页项目总览：项目用途、用户、技术栈、核心能力、当前状态 |
| `setup-and-run.md` | 依赖安装、本地启动、端口、依赖服务、常见启动失败原因 |
| `environment.md` | `.env`、配置文件、环境变量、dev/test/prod、容器、CI、远程环境 |
| `deployment-and-operations.md` | 生产部署、发布流程、运行拓扑、回滚、运维入口、线上排障 |
| `directory-map.md` | 主要目录职责，不写全量文件树，只写“从哪看” |
| `module-map.md` | 每个长期模块/子系统的职责、入口、依赖、核心流程、主要数据、验证方式 |
| `architecture-boundaries.md` | UI、API、Domain、DB、Jobs、External Services 的边界和调用方向 |
| `core-flows.md` | 核心业务链路，例如登录、下单、会议纪要生成、上传、审批 |
| `entrypoints.md` | 启动入口、路由入口、配置入口、核心 service、任务入口、模型入口 |
| `data-model.md` | 核心实体、表、聚合、关系、状态机 |
| `api-surface.md` | API 分组、消费者、鉴权、生成客户端、契约风险 |
| `async-and-events.md` | 异步调用、事件发布订阅、队列生产消费、callback、webhook、重试补偿 |
| `jobs-and-schedules.md` | 定时任务、后台任务、队列消费者、worker、scheduler |
| `change-impact-map.md` | 改某类需求通常影响哪些目录、接口、测试 |
| `testing-and-verification.md` | 单测、API 测试、E2E、lint、typecheck、手动验证 |
| `integrations.md` | 外部服务、SDK、消息队列、对象存储、第三方 API、AI 服务 |
| `risks-and-unknowns.md` | 不确定、待确认、文档和代码冲突、不可验证命令 |
| `glossary.md` | 业务术语、领域语言、缩写、角色定义 |

## 部署和运维

部署信息不应该全部塞进一个文档。它同时关系到新人本地启动、环境配置、生产发布和长期 Agent 记忆。

推荐分层：

| 内容 | 放置位置 | 理由 |
|---|---|---|
| 本地怎么启动、端口、依赖服务 | `setup-and-run.md` | 帮新人快速跑起来 |
| 环境变量、dev/test/prod 差异、容器、CI 环境 | `environment.md` | 部署依赖环境配置，和运行环境强相关 |
| 生产部署架构、服务器/容器/云服务、发布流程、回滚、运维入口 | `deployment-and-operations.md` | 这是线上运行和发布运维，不应该混入本地 setup |
| 部署拓扑图 | `diagrams/deployment-map.md` | 服务、容器、DB、队列、外部依赖之间关系用图更清楚 |
| 长期稳定摘要 | `.agent-loop/project/environments.md` 或 `project.md` 索引 | 给 Agent 后续判断环境边界、验证策略和发布风险 |

Layout Mode 规则：

| 模式 | 处理方式 |
|---|---|
| Compact | 部署内容合并进 `setup-and-run.md` 的 `Deployment Notes`，或 `architecture-and-integrations.md` 的 `Runtime / Deployment` 小节 |
| Standard | 基础环境写 `environment.md`；如果有容器、CI、远程服务或发布流程，补 `diagrams/deployment-map.md` |
| Expanded | 单独创建 `deployment-and-operations.md`，并关联 `diagrams/deployment-map.md` |

触发独立 `deployment-and-operations.md` 的信号：

| 信号 | 说明 |
|---|---|
| 有多环境发布 | dev / staging / prod 差异明显 |
| 有容器编排或云服务 | Docker Compose、Kubernetes、ECS、Cloud Run、serverless 等 |
| 有 CI/CD 发布流程 | GitHub Actions、GitLab CI、Jenkins、ArgoCD 等 |
| 有回滚或迁移流程 | rollback、migration、seed、release script |
| 有运维入口 | admin、monitoring、logs、metrics、trace、health check |
| 部署失败会影响业务状态 | 发布会触发任务、迁移、缓存刷新、异步消费 |

部署相关结论必须有证据。可用证据包括：

```text
Dockerfile / docker-compose*
Kubernetes manifests / Helm charts
.github/workflows / .gitlab-ci.yml / Jenkinsfile
Makefile / Taskfile / justfile
package scripts / deploy scripts
infra / ops / deployment docs
health check endpoints
monitoring / logging configs
```

禁止记录真实密钥、token、密码、生产连接串。只记录变量名、配置来源、用途和安全说明。

## 定时任务和后台任务

定时任务不应该只散落在 `integrations.md` 或 `entrypoints.md` 里。

建议单独创建：

```text
.agent-loop/onboarding-db/jobs-and-schedules.md
```

记录字段：

| 字段 | 说明 |
|---|---|
| 任务名称 | cron job、Celery task、worker、scheduler、consumer 名称 |
| 触发方式 | cron、Celery beat、queue、GitHub Actions schedule、systemd timer |
| 执行入口 | 代码文件、函数、命令 |
| 运行频率 | 每 5 分钟、每天、事件触发 |
| 依赖资源 | DB、Redis、队列、对象存储、外部 API |
| 影响数据 | 表、状态字段、缓存、外部系统 |
| 失败影响 | 哪些业务会延迟、错误或不一致 |
| 验证方式 | 单测、手动触发、日志检查、任务状态检查 |
| 证据 | 文件路径、配置、测试、运行命令 |
| 可信度 | high / medium / low |

## 异步、事件和队列

异步链路是 onboarding-db 的一级关注对象，不是 `integrations.md` 的附属小节。

建议单独创建：

```text
.agent-loop/onboarding-db/async-and-events.md
.agent-loop/onboarding-db/diagrams/async-flow-<name>.md
```

记录字段：

| 字段 | 说明 |
|---|---|
| 异步入口 | API 提交任务、上传完成、消息入队、定时触发、外部 callback |
| 事件/消息名称 | domain event、queue message、webhook event |
| Producer | 哪个模块发布事件或写入队列 |
| Queue / Broker | Redis、RabbitMQ、Kafka、Celery、BullMQ、SQS 等 |
| Consumer | 哪个 worker、handler、subscriber 消费 |
| 状态变化 | pending -> processing -> completed -> failed |
| Retry / DLQ | 重试、死信队列、失败补偿、幂等策略 |
| Callback / Webhook | 外部服务回调到哪个 endpoint |
| 观测方式 | 日志、trace id、task id、metrics、admin page |
| 验证方式 | 单测、集成测试、手动触发、查看队列/日志 |
| 证据 | 文件路径、配置、测试、运行命令 |
| 可信度 | high / medium / low |

发现 queue、broker、consumer、subscriber、callback、webhook、retry、DLQ、异步状态流转时，必须补一张对应的小图，或者在 `risks-and-unknowns.md` 说明为什么暂时无法确认。

## 图的规则

图是辅助视图，不是项目理解主入口。

默认只生成小图，一张图只回答一个问题。

| 图 | 解决的问题 | 粒度 |
|---|---|---|
| `module-relationship-map.md` | 模块之间是什么关系，谁依赖谁，谁是入口，谁是下游 | 模块 / 子系统级 |
| `boundary-map.md` | 系统有哪些层和边界，谁调用谁 | UI / API / Domain / DB / Jobs / External |
| `core-flow-<name>.md` | 某条业务链路怎么走 | 业务步骤级 |
| `async-flow-<name>.md` | 异步调用、事件发布订阅、队列生产消费怎么流转 | 事件 / 队列 / worker 级 |
| `job-flow-<name>.md` | 定时任务或后台任务何时触发、影响什么数据 | job / scheduler 级 |
| `state-flow-<entity>.md` | 状态字段如何合法流转 | 状态机级 |
| `api-call-flow-<name>.md` | 前端、网关、后端、外部服务之间如何调用 | API 调用链级 |
| `integration-flow-<name>.md` | 第三方 SDK、callback、webhook 如何接入 | 外部集成级 |
| `auth-flow.md` | 登录、token、refresh、role、permission 如何流转 | 鉴权权限级 |
| `file-flow-<name>.md` | 上传、下载、对象存储、回调、权限如何流转 | 文件链路级 |
| `failure-recovery-flow.md` | retry、rollback、DLQ、人工补偿如何工作 | 错误恢复级 |
| `data-entity-map.md` | 核心实体和状态怎么关联 | 实体 / 表 / 状态 |
| `deployment-map.md` | 服务、容器、环境、外部依赖怎么部署 | 服务 / 环境级 |
| `change-impact-map.md` | 改需求会影响哪里 | 目录 / API / 测试级 |

禁止默认生成：

```text
函数级全量调用图
全仓库文件依赖图
全量知识图谱
```

图必须服务定位问题，不服务展示复杂度。

初始 Onboarding DB 至少应该建立：

| 初始图 | 是否必须 | 说明 |
|---|---|---|
| `module-relationship-map.md` | 必须 | 帮新人知道模块之间怎么协作 |
| `boundary-map.md` | 必须 | 帮新人知道系统边界和调用方向 |
| `core-flow-<name>.md` | 至少 1 张 | 选择最核心业务链路先画，其他链路可逐步补 |
| `data-entity-map.md` | 如果存在持久化数据则必须 | 没有 DB 或核心实体时写明 `Not applicable` |
| `deployment-map.md` | 如果存在多环境/容器/远程服务则必须 | 单脚本项目可写明 `Not applicable` |

## Diagram Trigger Rule

一般来说，人类不容易在脑内稳定理解的内容，都应该画图。

触发原则：

```text
如果一个事实跨越 2 个以上模块、2 个以上进程、2 个以上状态，或需要按时间顺序理解，就优先用图表达。
```

分级规则：

| 等级 | 规则 |
|---|---|
| 必须画 | 模块关系、系统边界、至少一条核心业务流程 |
| 发现就画 | 异步队列、定时任务、状态机、callback/webhook、鉴权、外部集成、对象存储文件流 |
| 按需画 | API 调用链、部署图、改动影响图、失败补偿图 |

发现即必须补图：

| 发现 | 必须补的图 |
|---|---|
| 有 queue / broker / consumer / subscriber | `async-flow-<name>.md` |
| 有 cron / scheduler / worker / background job | `job-flow-<name>.md` |
| 有状态字段和状态迁移 | `state-flow-<entity>.md` |
| 有 callback / webhook | `integration-flow-<name>.md` |
| 有外部认证、token、role、permission 流转 | `auth-flow.md` |
| 有对象存储、上传、下载、文件回调 | `file-flow-<name>.md` |
| 有 retry / rollback / DLQ / 人工补偿 | `failure-recovery-flow.md` |

图不要求大，也不要求覆盖全仓库。每张图只回答一个具体问题。

## 扫描流程

建议流程：

```text
Project Onboarding Scan
-> Topology Detection
-> Existing Docs Scan
-> Shallow Repo Scan
-> Runtime / Tooling Scan
-> Entrypoint Scan
-> Module Map Scan
-> Boundary Scan
-> Async / Events Scan
-> Core Flow Extraction
-> Commands / Tests Verification
-> Onboarding DB Draft
-> Human Review Summary
-> Confirmed Write
-> Project Memory Backfill Proposal
```

## 扫描优先级

扫描流程不是机械线性 10 步。Agent 应该按 P0/P1/P2 优先级推进，先拿到能安全接管和继续开发的事实，再补完整文档。

| 优先级 | 目标 | 包含扫描 | 产出 |
|---|---|---|---|
| P0 | 让 Agent 能判断项目形态、运行入口和风险，避免误接管 | Project Shape、Existing Docs、Shallow Repo、Runtime / Tooling、Entrypoints | Quick Onboarding、project.md 草案、风险和未知 |
| P1 | 让人类能理解主要模块、边界和核心流程 | Module Map、Boundary、Core Flow、Commands / Tests Verification | onboarding-db 主阅读路径、模块关系图、边界图、至少一条核心流程图 |
| P2 | 补齐复杂项目长期维护资料 | Async / Events、Jobs、Data Model、Deployment、Integrations、Decisions、Change Impact | 细分文档、专题图、project memory backfill proposal |

执行规则：

| 情况 | 行为 |
|---|---|
| 人类选择 Quick Onboarding | 只做 P0，必要时记录 P1/P2 待补 |
| 人类选择 Deep Project Onboarding Scan | 先完成 P0，再做 P1，最后按项目现实和 Layout Mode 选择 P2 |
| 项目很大或信息不清 | 不直接全量扫 P2，先用 P0/P1 形成边界和阅读路径 |
| 发现高风险未知 | 暂停或降级输出，先让人类确认风险 |
| 人类只关心某个模块/问题 | 进入 Targeted Onboarding Scan，不跑完整 P2 |

### 1. Project Shape Detection

判断当前目录内的项目形态和主要边界。

本 proposal 暂不实施 Project Group 规则。若发现多个独立项目、多个 git repo 或 submodule，只记录为 `Project Group candidate`，停止创建跨项目 onboarding-db，并建议后续走单独的 Project Group proposal。

### 2. Existing Docs Scan

先读已有文档：

```text
README.md
AGENTS.md / CLAUDE.md / GEMINI.md
docs/
CONTRIBUTING.md
CHANGELOG.md
OpenAPI / Swagger docs
architecture docs
```

文档是线索，不是最终事实。

### 3. Shallow Repo Scan

只做浅层目录扫描，识别：

- 主要 app / service / package；
- 测试目录；
- 配置目录；
- 脚本目录；
- 文档目录；
- CI / Docker / deployment。

### 4. Runtime / Tooling Scan

读取：

```text
package.json / pnpm-workspace.yaml / turbo.json / nx.json
pyproject.toml / requirements.txt
go.mod / Cargo.toml / pom.xml
Makefile / Taskfile / justfile
Dockerfile / docker-compose*
.github/workflows / .gitlab-ci.yml
test runner configs
```

提炼启动、构建、测试、lint、typecheck、E2E 命令。

### 5. Entrypoint Scan

定位：

- 服务启动入口；
- UI 路由入口；
- API 路由入口；
- 配置入口；
- 核心 service；
- 数据模型；
- worker / job 入口；
- 外部集成入口。

### 6. Module Map Scan

识别每个长期模块、子系统、应用、服务或包。

每个模块都应该记录一张模块卡片：

```text
模块名称
模块职责
所属边界
主要入口
主要依赖
被谁调用
核心流程
核心数据/实体
关键配置
关键测试
风险和未知
证据
可信度
```

如果某个模块没有独立业务流程，也要说明它的支持性职责，例如 shared types、generated client、storage adapter、test utilities。

### 7. Boundary Scan

提炼：

- UI；
- API；
- Domain；
- DB / migrations；
- Jobs / workers；
- External Services；
- Auth / permissions；
- Shared packages / generated clients。

### 8. Async / Events Scan

识别异步调用、事件发布订阅、队列生产消费、callback、webhook、重试补偿和后台 worker。

如果发现异步链路：

1. 写入 `async-and-events.md`。
2. 创建或建议创建 `diagrams/async-flow-<name>.md`。
3. 若涉及定时或后台任务，同步写入 `jobs-and-schedules.md` 和 `diagrams/job-flow-<name>.md`。
4. 若涉及状态变化，同步更新 `data-model.md` 和 `diagrams/state-flow-<entity>.md`。
5. 若无法确认 producer、consumer、状态或失败补偿，写入 `risks-and-unknowns.md`。

### 9. Core Flow Extraction

先提炼最重要的 3 到 7 条业务链路，同时保证每个核心模块都能被至少一条流程、模块卡片或边界说明覆盖。

每条链路应该包含：

```text
触发者
入口
核心步骤
数据变化
外部依赖
失败点
验证方式
关键文件
```

如果模块很多，不要求一次性为每个模块都画独立流程图，但必须在 `module-map.md` 中写清楚每个模块做了什么、参与哪些流程、和哪些模块相连。后续可以按人类问题或 feature 需求补充更多 `core-flow-<name>.md`。

### 10. Commands / Tests Verification

命令必须分可信度：

| 可信度 | 含义 |
|---|---|
| high | 已运行或 CI 明确使用 |
| medium | 从脚本推断，未运行 |
| low | 文档提到但代码未验证 |

不要把未验证命令写成确定事实。

## 写入确认规则

`onboarding-db` 的后续写入都必须询问人类。

原因：

- 它面向人类阅读；
- 它会影响新人理解项目；
- 它比 feature `notes.md` 更像长期说明书；
- Agent 自动写多了会降低可信度。

写入前必须展示：

| 项 | 内容 |
|---|---|
| 准备写入的文件 | 例如 `core-flows.md` |
| 新增或修改内容 | 简短摘要 |
| 证据 | 代码路径、命令、文档 |
| 可信度 | high / medium / low |
| 是否影响 project memory | 是 / 否 |
| 是否需要人类确认事实 | 是 / 否 |

## Onboarding DB Learning Rule

Agent 回答项目问题时，可以发现新知识，但不能默认写入。

| 情况 | 行为 |
|---|---|
| 一次性回答 | 不写文档 |
| 发现长期有用的项目事实 | 建议更新 onboarding-db |
| 已有文档过期 | 建议修正 |
| 发现新的业务链路 | 建议更新 `core-flows.md` 和对应图 |
| 发现新的定时任务 | 建议更新 `jobs-and-schedules.md` |
| 发现新的外部集成 | 建议更新 `integrations.md` |
| 人类说“记录下来” | 进入写入确认流程 |
| 开启 Auto-Learning Mode | 可自动草拟，但写入前仍要汇报，关键事实仍需确认 |

## Freshness Check

`onboarding-db` 是长期资料库，但不是每日开发主状态。

建议每份 DB 记录：

```text
Last Verified: 2026-06-07
Freshness Window: 7 days
Verification Scope: docs + commands + entrypoints + core directories
```

超过 7 天不是自动失效，而是需要 Freshness Check。

触发场景：

- 新人需要接管；
- 新 Agent 第一次进入大项目；
- 人类明确要看项目资料；
- 项目最近有较大结构变化；
- feature close 改变了长期架构、命令、核心链路或外部集成。

Freshness Check 做轻量核对：

- README / AGENTS / CLAUDE 是否变化；
- 启动和测试命令是否变化；
- 入口文件是否变化；
- 核心目录是否变化；
- 主要业务链路是否变化；
- 已知风险是否仍然成立。

## Guided Onboarding

Agent 应该能引导人类接管项目，而不是只丢一堆文档。

人类说：

```text
带我接管这个项目
```

Agent 应该按阶段带读：

| 阶段 | 引导内容 |
|---|---|
| 了解项目 | 读 `overview.md` |
| 跑起来 | 读 `setup-and-run.md` |
| 看代码入口 | 读 `entrypoints.md` / `directory-map.md` |
| 理解业务链路 | 读 `core-flows.md` |
| 准备开发 | 读 `change-impact-map.md` / `testing-and-verification.md` |
| 看风险 | 读 `risks-and-unknowns.md` |

每一步都应该能回答：

```text
你现在知道了什么？
下一步该看哪里？
如果要开发需求，应该进入哪个 agent-loop stage？
```

## 和日常开发的关系

`onboarding-db` 不是日常开发主事实源。

日常开发默认主读：

```text
.agent-loop/project.md
.agent-loop/project/*.md
.agent-loop/features/<feature>/
代码现实
```

`onboarding-db` 在这些场景启用：

| 场景 | 是否读取 |
|---|---|
| 新人接管 | 读取 |
| 新 Agent 第一次进入大项目 | 读取 |
| 人类问项目理解问题 | 读取 |
| 开 feature 前需要找边界 | 可读取 |
| 文档超过 7 天且有人要 onboarding | 先 Freshness Check |
| feature 改变长期架构/链路/命令 | close 时建议更新 |
| 日常小 task | 不默认读取 |

## 问题路由规则

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

## Project Memory Backfill

`onboarding-db` 和 `project.md` 可以互相引用，但不能互相替代。

| 发现内容 | 主要写入 |
|---|---|
| 当前 Active Feature / Next Action | `project.md` |
| 项目理解说明 | `onboarding-db/` |
| 启动、测试、环境详细说明 | `onboarding-db/`，必要摘要回补 `project/commands.md` 或 `project/testing.md` |
| 业务术语和长期产品共识 | `onboarding-db/glossary.md`，必要摘要回补 `project/domain-language.md` |
| 核心能力 | `onboarding-db/overview.md`，必要摘要回补 `project/capabilities.md` |
| 架构边界 | `onboarding-db/architecture-boundaries.md`，必要摘要回补 `project/boundaries.md` |
| 执行证据和开发过程 | feature `notes.md` |

如果 `onboarding-db` 的事实和代码现实冲突：

```text
代码现实 = 当前事实基础
onboarding-db = 历史理解资料
project.md = agent-loop 当前运行入口
```

Agent 应该提出修正建议，而不是静默覆盖。

## Project Group 暂缓

Project Group 是独立能力，当前 proposal 先不实施。

如果扫描发现当前目录更像项目组，Agent 应该：

1. 标记为 `Project Group candidate`。
2. 汇报发现依据，例如多个独立 git repo、submodule、多个长期应用或服务。
3. 询问人类是否只对当前子项目运行 Project Onboarding Scan。
4. 不创建顶层 group onboarding-db。
5. 不创建跨项目模块关系或跨项目 feature 路由。

Project Group 的顶层记忆、子项目记忆、跨项目 feature、并发和依赖顺序，统一留给 `docs/proposal/v1.x.0/project-group-feature-routing.md` 后续讨论。

## Subagent 支持

大项目可以建议 bounded subagent scanning，但必须人类确认。

推荐 scan lanes：

```text
docs-and-overview
commands-and-environments
directory-and-entrypoints
boundaries-and-integrations
core-flows-and-data-model
async-and-events
testing-and-verification
jobs-and-schedules
risks-and-unknowns
```

子代理只能返回：

```text
Findings
Evidence
Confidence
Uncertainties
Suggested onboarding-db entries
Files read
```

子代理不能：

- 直接写 `onboarding-db`；
- 直接写 `project.md`；
- 创建 `AGENTS.md` / `CLAUDE.md`；
- 开始 feature 实现；
- 声称完成项目接管；
- 更新长期事实。

主 Agent 负责汇总、冲突处理、可信度标注、人类确认和最终写入。

## Subagent 冲突处理流程

Subagent 协作不能只规定“不能做什么”，还必须规定主 Agent 如何处理多个 scan lane 的冲突。

主 Agent 收到 subagent 结果后，必须先合并审查，再进入人类确认。

处理流程：

```text
Subagent Returns
-> Normalize Findings
-> Deduplicate Facts
-> Detect Conflicts
-> Check Evidence Quality
-> Assign Confidence
-> Produce Conflict Table
-> Main Agent Decision / Human Question
-> Batch Human Review
-> Confirmed Write
```

冲突表：

| 冲突项 | Subagent A 结论 | Subagent B 结论 | 证据 A | 证据 B | 当前判断 | 处理方式 |
|---|---|---|---|---|---|---|

处理规则：

| 情况 | 主 Agent 行为 |
|---|---|
| 两个 subagent 对同一事实结论一致 | 合并证据，提高可信度 |
| 结论不同但代码证据更强 | 以代码现实为当前事实基础，标注被覆盖结论 |
| 结论不同且证据都弱 | 写入 `risks-and-unknowns.md` 草案，不写成确定事实 |
| 涉及业务意图、历史原因、部署权限 | 问人类，不让 subagent 推断 |
| 涉及长期 project memory | 放入 Memory Backfill 批次，等待人类确认 |
| 涉及安全、数据、生产发布 | 降低自动化程度，要求明确确认 |

主 Agent 不应该直接把 subagent 输出拼接进 onboarding-db。所有 subagent 结果都必须经过证据归一、冲突处理、可信度标注和 Batch Human Review。

## 模板需求

如果 proposal 被接受，需要新增模板：

```text
templates/onboarding-db/README.md
templates/onboarding-db/overview.md
templates/onboarding-db/setup-and-run.md
templates/onboarding-db/code-map.md
templates/onboarding-db/architecture-and-integrations.md
templates/onboarding-db/flows-and-data.md
templates/onboarding-db/verification-and-risks.md
templates/onboarding-db/decisions-and-history.md
templates/onboarding-db/deployment-and-operations.md
templates/onboarding-db/batch-review.md
templates/onboarding-db/diagram.md
```

这些模板是实现入口，不是一对一限制最终产物。Standard / Expanded Layout 可以从这些模板派生出更细文件，例如 `module-map.md`、`async-and-events.md`、`jobs-and-schedules.md`、`data-model.md`、`api-surface.md`。图模板默认使用一个通用 `diagram.md`，通过 `Diagram Type` 区分 module、boundary、core-flow、async-flow、job-flow、state-flow 等逻辑类型。

也需要新增或调整 reference：

```text
references/project-onboarding-scan.md
references/onboarding-db.md
references/stage-guides.md
references/existing-project-onboarding.md
references/recovery-and-backfill.md
references/project-memory-mode.md
references/validation-scenarios.md
```

Reference 分工：

| Reference | 职责 |
|---|---|
| `existing-project-onboarding.md` | 旧项目接管入口、Quick Onboarding 主流程、Quick / Deep / Targeted 选择门禁 |
| `project-onboarding-scan.md` | Deep Project Onboarding Scan 的流程规则 |
| `onboarding-db.md` | Onboarding DB 的读取、写入、Freshness Check、Learning Rule、问题路由 |
| `onboarding-db-templates.md` | Onboarding DB 每个文档和图的模板字段规范 |

后续实现时不要把 `existing-project-onboarding.md` 改成大而全的 Deep Scan 文档。它应该保留为入口和 Quick 流程，Deep 细节拆到新 reference。

## 验证场景

后续实现时需要补压力场景：

| 场景 | 期望 |
|---|---|
| 老项目没有 `.agent-loop` | 先运行 Project Onboarding Scan，再提议创建 project memory |
| 人类拒绝 Deep Project Onboarding Scan | 只做 Quick Onboarding，不生成 onboarding-db 和 diagrams |
| 人类选择 Deep Project Onboarding Scan | 生成 Quick 全部基础产物，再生成 onboarding-db 和必要图 |
| 人类要求“带我接管项目” | Agent 进入 Guided Onboarding，而不是只给文档路径 |
| 项目已有全量爆炸图 | Agent 不把它作为主入口，只作为辅助证据 |
| 发现定时任务 | 写入 `jobs-and-schedules.md` 的草案，并请求确认 |
| 发现异步队列或事件消费 | 写入 `async-and-events.md` 草案，并建议创建 `async-flow-<name>.md` |
| 发现状态机 | 写入 `data-model.md`，并建议创建 `state-flow-<entity>.md` |
| 发现 callback/webhook | 写入 `integrations.md` 和 `async-and-events.md`，并建议创建 `integration-flow-<name>.md` |
| 人类问出新业务链路 | Agent 回答后建议更新 `core-flows.md`，写入前确认 |
| onboarding-db 超过 7 天 | Agent 建议 Freshness Check，不直接宣称过期 |
| README 和代码现实冲突 | 标记冲突和可信度，代码现实作为当前事实基础 |
| 发现疑似 Project Group | Agent 标记 `Project Group candidate`，不直接创建 group onboarding-db |
| 项目有多个长期模块 | Agent 建立 `module-map.md` 和 `diagrams/module-relationship-map.md` |
| 某个模块没有业务流程 | Agent 仍记录模块职责、支持性流程、依赖和验证方式 |
| 初始 onboarding 没有核心流程图 | Agent 不应认为 onboarding-db 完整，至少补一条核心链路图或说明无法确认 |
| feature close 改变长期链路 | Agent 建议更新 onboarding-db 和 project memory，分别确认 |
| 小项目选择 Compact Layout | 物理文件较少，但 README 明确索引所有理解维度 |
| 大项目选择 Expanded Layout | 只把复杂模块/流程拆文件，不按所有目录机械拆分 |
| Agent 发现高可信事实 | 可以进入草案，但不能绕过批量确认标记 reviewed |
| 人类要求快速阅读 | Agent 合并文档以提高可读性，不省略关键维度 |
| 发现架构历史或设计取舍 | 写入 `decisions-and-history.md` 或对应章节，原因类结论需证据或人类确认 |
| Agent 准备同时修改 spec/tasks/tests/plan/project memory | 必须使用 Batch Human Review 表格汇报，不逐条口头确认，也不静默写入 |
| 人类选择 Quick Onboarding | Agent 只执行 P0，记录 P1/P2 待补项，不直接进入完整 Deep Scan |
| 人类选择 Deep Project Onboarding Scan | Agent 先完成 P0，再做 P1，最后按 Layout Mode 和项目现实选择 P2 |
| Subagent 返回互相冲突的扫描结果 | 主 Agent 生成冲突表、比较证据、标可信度，不能直接拼接写入 onboarding-db |
| README 缺少模块阅读路径 | Agent 不应认为 onboarding-db 完整，必须补“理解某模块先读什么”的路径或说明无法确认 |
| 发现部署/发布/回滚信息 | Agent 按分层写入 setup、environment、deployment-and-operations、deployment-map，不把所有部署信息塞进单一文档 |
| 人类只要求理解某个模块、链路或异步任务 | Agent 进入 Targeted Onboarding Scan，不跑完整 Deep Scan，也不生成无关 onboarding-db 文件 |

## 当前建议默认值

1. `Project Onboarding Scan` 作为 Existing Project Onboarding、Re-Adopt、Guided Onboarding 的能力。
2. `Project Onboarding DB` 默认放在 `.agent-loop/onboarding-db/`。
3. 接管旧项目时先让人类选择 Quick Onboarding 或 Deep Project Onboarding Scan。
4. Deep Project Onboarding Scan 包含 Quick Onboarding 的全部基础产物。
5. `onboarding-db` 面向人类，所有写入和更新都需要人类确认。
6. 日常开发不默认读取 `onboarding-db`，除非需要项目理解、边界定位、freshness check 或人类明确要求。
7. 7 天作为 freshness window，超过后触发轻量核对，不自动失效。
8. 初始 Onboarding DB 必须包含模块关系图、边界图和至少一张核心业务链路图；其他图按项目现实补充。
9. 发现异步、队列、订阅消费、定时任务、状态机、callback/webhook、鉴权、对象存储文件流时，应优先补对应小图。
10. `onboarding-db` 正文语言跟随项目主要文档语言或人类协作语言；无法判断时默认中文。
11. 图只画模块关系、边界、业务链路、异步事件、状态、实体、部署、改动影响，不默认画全量函数/文件关系图。
12. Deep Scan 必须选择或建议 `Onboarding DB Layout Mode`：Compact、Standard、Expanded。
13. Layout Mode 控制物理文件颗粒度，不控制理解维度是否存在。
14. 写入确认采用批量确认模式，允许草案自动生成，但 reviewed 状态必须人类确认。
15. 保留 `decisions-and-history` 能力，用来记录关键设计决策、历史取舍、迁移背景和技术债。
