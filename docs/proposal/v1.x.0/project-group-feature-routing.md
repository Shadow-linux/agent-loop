# Proposal: 项目组 Feature 路由与并发规则

状态：讨论草案
目标版本：alpha-v1.2.0
创建时间：2026-06-04

## 目的

这份 proposal 用来讨论一个更复杂的问题：

当一个工作区可能是“单个项目”，也可能是“多个项目组成的项目组”时，`agent-loop` 应该怎么判断：

- feature 应该开在当前子项目，还是开在上层项目组；
- 子项目之间能不能并发开 feature；
- 如果存在前后端依赖、API 契约、生成客户端、发布顺序，应该怎么表达依赖；
- 长期记忆应该回补到顶层，还是回补到子项目。

这不是正式规则，先作为 v1.2.0 alpha 的讨论稿。

## 核心收敛

项目形态只分两种：

```text
Single Project
Project Group
```

不要再拆很多特殊形态，否则 agent 会越来越难判断。

| 模式 | 含义 |
|---|---|
| Single Project | 当前目录就是一个主要项目，当前 `.agent-loop/` 负责全部长期记忆和 feature。 |
| Project Group | 当前目录下面有多个长期存在的项目、应用、服务、包、独立 git repo 或 submodule，需要顶层做协作总控。 |

## 术语

| 术语 | 含义 |
|---|---|
| Group Root | 项目组根目录，负责多个子项目之间的总控。 |
| Subproject | 项目组里面的一个长期子项目，例如 frontend、backend、desktop、h5。 |
| Feature Owner Level | feature 应该归属的层级，也就是能完整负责这个 feature 影响范围的最低层。 |
| Group Feature | 影响多个子项目、跨项目 contract、跨发布顺序的 feature。 |
| Subproject Feature | 只影响一个子项目的 feature。 |

## 怎么判断当前是单项目还是项目组

Agent 在初始化、接管旧项目、开启 feature、恢复 feature 前，都应该先判断当前目录拓扑。

| 发现的信号 | 倾向判断 |
|---|---|
| 只有一个主要 app/service/package，且只有一个 git repo | Single Project |
| 当前目录下有多个独立 `.git` 仓库 | Project Group |
| 当前目录下有 submodule，并且 submodule 是真实应用/服务代码 | Project Group |
| 当前目录下有 frontend/backend/desktop/mobile/h5 等多个长期项目 | Project Group |
| 多个子目录有不同 build/test/dev 命令 | Project Group |
| 顶层 `.agent-loop/project.md` 已声明 `Topology: Project Group` | Project Group |
| 子项目 `.agent-loop/project.md` 已声明自己属于某个 Group Root | 当前处于 Subproject context |

如果信号冲突，agent 不应该直接创建 feature，而是先向人类确认。

## 记忆归属

### Single Project

单项目最简单：

```text
当前项目/
  .agent-loop/
    project.md
    requirements/
    features/
```

当前 `.agent-loop/` 负责全部长期记忆、需求归档、feature、task、test、plan、notes。

### Project Group

项目组要分成顶层总控记忆和子项目记忆。

```text
项目组根目录/
  .agent-loop/
    project.md
    project/
      modules/
        <subproject>.md
      contracts.md
      commands.md
      testing.md
    features/

  frontend/
    .agent-loop/
      project.md
      features/

  backend/
    .agent-loop/
      project.md
      features/
```

顶层 `.agent-loop/` 负责：

- 项目组总览；
- 子项目路由；
- 跨项目 feature；
- 跨项目 contract；
- 跨项目当前状态；
- 哪些子项目参与了当前工作；
- 哪些长期变化需要回补到哪些子项目。

子项目 `.agent-loop/` 负责：

- 自己的技术栈；
- 自己的目录边界；
- 自己的命令和测试；
- 自己的 feature 历史；
- 自己代码现实的长期回补；
- 自己的 AGENTS.md / CLAUDE.md 规则。

顶层不要变成所有子项目细节的大垃圾桶。顶层应该是路由器和总控。

## Feature 放哪里

核心规则：

```text
Feature 放在能完整负责它影响范围的最低层。
```

| 场景 | Feature 放置位置 |
|---|---|
| 只影响一个项目 | 子项目 `.agent-loop/features/<feature>/` |
| 影响多个项目 | 顶层 `.agent-loop/features/<feature>/` |
| 涉及 API / SDK / event / schema / shared contract | 顶层 `.agent-loop/features/<feature>/` |
| 一开始不确定影响范围 | 先放顶层，做 scope scan 后再决定是否下放 |
| 已在子项目开 feature，但发现会影响别的子项目 | 暂停执行，提议升级为 Group Feature，人类确认后处理 |
| 已在顶层开 feature，但确认只影响一个子项目 | 提议降级为 Subproject Feature，人类确认后处理 |

不能由 agent 静默搬迁 feature。升级或降级都属于 drift decision，需要人类确认。

## Agent 怎么知道自己开在哪一层

建议 `project.md` 增加拓扑字段：

```text
Topology: Single Project | Project Group | Subproject
Group Root: <path or none>
Subproject ID: <id or none>
Feature Owner Rule: lowest-level-owner
```

建议每个 feature 的 `spec.md` 增加归属字段：

```text
Feature Owner Level: group | subproject
Owning Path: <absolute or repo-relative path>
Affected Projects:
- <project-id>
Scope Confidence: high | medium | low
Promotion/Demotion Status: none | proposed | approved | rejected
```

开启 feature 前，agent 应该用表格汇报它的判断：

| 判断项 | Agent 建议 | 证据 |
|---|---|---|
| 当前目录形态 | Project Group | 发现多个 git repo / submodule |
| Feature 归属层级 | group | 同时影响 frontend 和 backend |
| Feature 文档位置 | 顶层 `.agent-loop/features/...` | 需要跨项目 API contract |
| 涉及子项目记忆 | backend, h5 | backend 是 API producer，h5 是 consumer |

## 子项目 feature 能不能并发多开

可以，但不能默认乱开。

建议分三类：

| 类型 | 含义 | 是否允许并发 |
|---|---|---|
| Independent | 没有共享文件、共享 contract、共享状态，也没有执行顺序依赖 | 人类确认后可以并发 |
| Dependent | 一个 feature/task 依赖另一个的结果 | 不能并发，必须设置 barrier |
| Coupled | 涉及 API、SDK、event、schema、生成客户端、数据迁移、认证安全、发布顺序 | 应该升级为 Group Feature |

并发不能靠 agent 猜，必须写进 `tasks.md`。

## 依赖顺序怎么表达

v1.2.0 alpha 不引入 roadmap graph。

先用 Markdown 表达依赖：

- `Depends on`
- `Unblocks`
- `Barrier`
- `Can run in parallel with`
- `Must not start before`

示例：

```text
## Execution Lanes

Lane A: backend contract
- T001 定义 API contract
- T002 实现 backend endpoint
- Barrier: contract tests pass

Lane B: h5 integration
- T003 生成 API client
- T004 接入 UI flow
- Depends on: Lane A barrier

Lane C: docs/demo
- T005 更新使用文档
- Can run in parallel with: T002
```

任务表也应该表达依赖：

| ID | Owner | Status | Depends On | Barrier | Evidence |
|---|---|---|---|---|---|
| T001 | backend | planned | none | API contract accepted | - |
| T002 | h5 | blocked | T001 | generated client updated | - |
| T003 | e2e | blocked | T001, T002 | browser verification | - |

## 跨项目 feature 怎么关闭

Group Feature 关闭前必须有 Integration Summary。

示例：

| Project | 做了什么 | 验证证据 | 是否影响长期 | 回补位置 |
|---|---|---|---|---|
| backend | 新增 API producer | API tests | 是 | backend `.agent-loop/project/capabilities.md` |
| h5 | 接入 consumer flow | typecheck + E2E | 是 | h5 `.agent-loop/project/capabilities.md` |
| group | 新增跨项目 contract | contract review | 是 | group `.agent-loop/project/contracts.md` |

Group Feature close 需要满足：

- 所有受影响子项目的任务都 done / skipped / removed；
- 每个受影响子项目都有 fresh verification evidence；
- 顶层完成 Review；
- 顶层和子项目都完成 Drift Check；
- 长期影响已经回补到正确层级；
- 人类明确确认 close。

## Feature 升级和降级

### 升级：Subproject Feature -> Group Feature

触发条件：

- 需要修改另一个子项目；
- 需要改变 API / SDK / event / schema；
- 需要生成 client；
- 涉及 shared contract；
- 涉及跨项目发布顺序；
- 需要跨项目 E2E。

### 降级：Group Feature -> Subproject Feature

触发条件：

- targeted scan 证明只影响一个子项目；
- 没有 contract、API、发布顺序问题；
- 人类确认顶层管理是多余开销。

### 升级/降级步骤

1. 停止当前执行。
2. 用表格说明原因和证据。
3. 提议新的 feature 位置。
4. 请求人类确认。
5. 在确认后的层级创建或更新 feature artifacts。
6. 如果旧位置已经有文档，保留一条 redirect note，不静默删除。

## 需要继续讨论的问题

1. Project Group 是否允许默认多个 active subproject feature，还是必须显式开启 `Parallel Feature Mode`？
2. 顶层是否需要单独维护 `active-features.md`，还是 `project.md` 的 Current Work 足够？
3. Group Feature 下面是否要给每个子项目创建镜像 feature 目录，还是只在 close 时回补子项目 memory？
4. Feature 升级/降级时，是移动文件、复制文件，还是旧位置保留 redirect note，新位置重新创建？
5. 独立子项目并发时，是否默认建议 git worktree / branch 隔离，还是只有人类要求才使用？

## 当前建议默认值

先作为 alpha-v1.2.0 的默认讨论方案：

1. 默认每个 owner level 只有一个 active feature。
2. 子项目 feature 并发必须人类明确确认。
3. Group Feature 拥有跨项目 artifacts；子项目默认只接收 memory backfill，不创建镜像 feature 目录。
4. Feature 升级/降级时，旧位置保留 redirect note，新位置创建或更新 artifacts。
5. 依赖顺序用 Markdown lanes / barriers 表达，不引入 roadmap graph。

## 如果 proposal 被接受，需要改哪些地方

- `references/project-memory-mode.md`
  - 增加 Single Project / Project Group 拓扑规则。
- `references/large-projects.md`
  - 增加 feature owner level、升级/降级、并发 lanes。
- `references/stage-guides.md`
  - 在 feature start、work breakdown、drift check、project memory update、close 阶段增加项目组规则。
- `references/document-templates.md`
  - 增加 `project.md` 和 `spec.md` 的拓扑字段。
- `templates/project.md`
  - 增加 `Topology`、`Group Root`、`Subproject ID`。
- `templates/spec.md`
  - 增加 `Feature Owner Level`、`Affected Projects`、`Scope Confidence`。
- `templates/tasks.md`
  - 增加 execution lanes、depends on、barrier 字段。
- `references/validation-scenarios.md`
  - 增加压力场景：
    - 跨项目 feature 被错误开在子项目；
    - 子项目 feature 执行中发现影响 API contract；
    - 两个独立子项目 feature 想并发；
    - 前端在后端 contract 未完成前被错误启动；
    - Group Feature close 时忘记回补子项目 memory。
