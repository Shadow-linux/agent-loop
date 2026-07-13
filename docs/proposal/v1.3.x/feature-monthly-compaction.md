# Proposal: Feature Monthly Compaction

状态：讨论草案
目标版本：v1.2.4 候选
创建时间：2026-07-01

## 背景

`agent-loop` 现在把 feature workspace 直接放在 `.agent-loop/features/` 第一层：

```text
.agent-loop/features/YYYY-MM-DD-<feature-slug>/
```

这个结构对当前开发很友好：路径短、Agent 易写、recent scan 易查。但 feature 越来越多以后，第一层目录会变长，人类浏览困难，Agent 做 Feature Follow-up / Flow-back、Targeted Feature Scan、Re-Adopt 时也容易扫描过多历史细节。

问题不是“历史 feature 不重要”，而是旧 feature 的主要价值已经从施工过程转为交付摘要：

```text
当前 feature 需要完整施工上下文。
旧 feature 更需要稳定的最终事实、交付行为、验证摘要和索引关系。
```

## 目标

本 proposal 目标是定义一套安全的 feature 月度压缩规则：

1. 当前月保持 flat，不影响正在开发的 feature；
2. 上个月且整月全部完成后，才允许月度压缩；
3. 压缩后第一层目录按月份收束；
4. 旧 feature 以 `archive.md` 作为主入口；
5. 历史施工文件默认进入 `historical/`，不默认删除；
6. 明确哪些索引关系、引用路径和扫描规则会受影响；
7. 为未来实施提供安全 gate 和验证方向。

## 非目标

第一版不做以下事情：

- 不自动压缩当前月 feature；
- 不在月份中存在 active / paused / in-progress feature 时自动压缩整月；
- 不默认删除 `spec.md`、`tasks.md`、`tests.md`、`plan.md`、`notes.md` 等历史细节；
- 不默认做 Partial month compaction；
- 不把 `requirements/` 的原始需求材料压缩成摘要；
- 不把 feature archive 变成 project memory；
- 不替代 Feature Follow-up / Flow-back 的归属判断；
- 不破坏 human gate：移动、压缩、删除历史细节都必须经过人类确认。

## 核心观点

```text
当前月保持 flat。
上个月且整月全部完成后，才允许月度压缩。
Slim With History 是默认压缩模式。
Deep Archive / Summary Only 永远不是默认动作。
```

目录压缩解决的是 `.agent-loop/features/` 第一层过长的问题。内容压缩解决的是旧 feature 不应再让 Agent 默认深读完整施工过程的问题。

这两个目标可以一起做，但默认策略必须保守：移动到月目录、生成摘要、保留历史细节。

## 压缩模式

| Mode | 适用对象 | 目录形态 | 内容策略 | 默认 |
|---|---|---|---|---|
| Full | 当前月 feature；active / paused / in-progress feature；有 open follow-up 的 feature | `.agent-loop/features/YYYY-MM-DD-<feature-slug>/` | 保留完整 `product.md`、`spec.md`、`tasks.md`、`tests.md`、`plan.md`、`notes.md`、handoffs 和复杂细节目录 | 是 |
| Slim With History | 上个月或更早，且整月全部完成、无 open follow-up、索引已回填 | `.agent-loop/features/YYYY-MM/YYYY-MM-DD-<feature-slug>/` | `archive.md` 成为主入口；旧施工文件移入 `historical/` | 是 |
| Deep Archive / Summary Only | 更早月份，且人类明确要求进一步深压缩 | `.agent-loop/features/YYYY-MM/YYYY-MM-DD-<feature-slug>/` | 默认只保留 `README.md` 和 `archive.md`；删除、打包或外移 `historical/` 需要强 human gate | 否 |

Deep Archive 永远不是默认动作。即使 5 月及以前的 feature 已经很旧，也只是具备“可建议深压缩”的资格，不代表 Agent 可以自动删除历史细节。

## 推荐目录

当前月保持 flat：

```text
.agent-loop/
  features/
    2026-07-01-wallet-recharge/
      product.md
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
```

上个月整月完成后压缩为 Slim With History：

```text
.agent-loop/
  features/
    2026-07-01-wallet-recharge/
    2026-07-03-token-deduction/
    2026-06/
      INDEX.md
      2026-06-13-login/
        README.md
        archive.md
        historical/
          product.md
          spec.md
          tasks.md
          tests.md
          plan.md
          notes.md
          handoffs/
          plans/
          tasks/
          tests/
```

更早月份在强确认后可进入 Deep Archive / Summary Only：

```text
.agent-loop/
  features/
    2026-05/
      2026-05-08-upload/
        README.md
        archive.md
```

## 触发入口

人类可以这样说：

```text
现在 7 月了，把 6 月份已经做完的 feature 压缩一下。
```

Agent 应进入 Feature Compaction Scan，而不是直接移动文件。

## Feature Compaction Scan

输入：

- 当前日期；
- `.agent-loop/features/` 第一层 flat feature；
- 已有 month bucket；
- `project.md` Active Feature / Paused Features；
- feature `spec.md`、`tasks.md`、`tests.md`、`plan.md`、`notes.md`、close 记录；
- requirement set README 和 optional `requirements/INDEX.md`；
- `.agent-loop/decisions/*.md`；
- recent Feature Follow-up / Flow-back notes。

输出：

- Candidate Matrix；
- blocked month / blocked feature reason；
- proposed compaction mode；
- affected index relationship list；
- human confirmation request。

## Candidate Matrix

Agent 在执行压缩前必须展示类似表格：

| Month | Feature | Current Path | Status | Open Follow-up | Index Backfill | Proposed Mode | Decision |
|---|---|---|---|---|---|---|---|
| 2026-06 | 2026-06-13-login | `.agent-loop/features/2026-06-13-login/` | closed | none | complete | Slim With History | pending-human |
| 2026-06 | 2026-06-20-upload | `.agent-loop/features/2026-06-20-upload/` | in-progress | none | incomplete | Full | blocked |

如果某个月存在 blocked feature，默认不做整月压缩。

## Safety Gate

整月进入 Slim With History 前，必须满足：

- 该月份不是当前月；
- 该月份所有 feature 都是 terminal 状态，例如 closed / implemented / archived；
- 没有 active / paused / in-progress feature；
- 没有 open follow-up、unresolved drift、未完成 verification、未处理 review blocker；
- requirement set README 的 `Implemented By` / `Feature Mapping` 已回填；
- optional `requirements/INDEX.md` 如存在，也已更新实现状态；
- relevant `decisions/*.md` 的 `Implemented By` 已回填；
- `project.md` 不再把这些 feature 作为 Active Feature 或 Paused Features；
- archive summary 能覆盖 delivered behavior、verification evidence、drift / follow-up notes、changed files / public interfaces；
- Agent 已列出所有需要更新的索引关系；
- 人类明确确认。

## Human Gate

以下动作都必须 Human-gated：

- 创建 month bucket；
- 移动 feature workspace；
- 生成或覆盖 `archive.md`；
- 移动历史细节到 `historical/`；
- 更新 requirement / decision / project memory 索引引用；
- 执行 Partial month compaction；
- 执行 Deep Archive / Summary Only；
- 删除、打包、外移 `historical/`。

Partial month compaction 不是默认行为。只有当人类明确要求“这个月部分完成的也先压缩已完成 feature”时，Agent 才能建议，并且必须在 `features/YYYY-MM/INDEX.md` 标记该月份为 `mixed`。

## Archive Summary Template

`archive.md` 应该成为旧 feature 的主入口：

```md
# Feature Archive: <Feature Name>

Status: archived
Compaction Mode: Slim With History | Deep Archive / Summary Only
Original Feature ID: YYYY-MM-DD-<feature-slug>
Current Path:
Archived At:
Archived By:

Source Requirements:
- <requirement path>

Applicable Decisions:
- <decision path>

Implements Decisions:
- Decision:
  - Implemented Slice:

Delivered Behavior:
- <delivered behavior>

Key Design Decisions:
- <design decision>

Changed Files / Public Interfaces:
- <file or interface>

Verification Summary:
- Evidence:
- Commands:
- Result:

Drift / Follow-up Notes:
- <drift or follow-up note>

Known Risks:
- <known risk>

Historical Detail Location:
- historical/
```

`README.md` 应很短：

```md
# Archived Feature

Read `archive.md` first.
Historical implementation details are under `historical/` when present.
```

## 影响的索引关系

Feature 月度压缩会改变路径和默认阅读入口，因此会影响以下索引关系。

| Index / Relationship | 当前用途 | 压缩影响 | 必须更新 |
|---|---|---|---|
| `features/INDEX.md` | 全 feature inventory、month view、状态视图 | 需要记录 feature 当前路径、month bucket、compaction mode、archive path | 是 |
| `features/YYYY-MM/INDEX.md` | 月份内 feature 列表 | 新增月度索引，记录该月是否 fully compacted / mixed / deep archived | 是 |
| requirement set README | `Implemented By`、`Delivery Phases`、`Feature Mapping` | feature 路径从 flat 改为 month bucket；phase 到 feature 的链接要改到 archive path 或 current path | 是 |
| `requirements/INDEX.md` | requirement inventory、implemented view、backlog/deferred view | 如果存在，要同步 implemented feature path 和 status | 条件是已存在或本来应更新 |
| `.agent-loop/decisions/*.md` | ADR / decision 的 `Implemented By` | feature 实现引用要改到新的 archive path；`Applicable Decisions` / `Implements Decisions` 在 archive summary 中保留 | 是 |
| `project.md` | Active Feature、Paused Features、Current Work、recent references | Active Feature 和 Paused Features 不能指向 archived feature；旧 closed feature 可指向 archive summary | 是 |
| feature internal links | `Source Requirements`、`Applicable Decisions`、`Implements Decisions` | `archive.md` 需要保留这些关系；historical 文件内的旧相对链接可保留为历史证据，但外部索引要更新 | 是 |
| Feature Follow-up / Flow-back | recent / historical feature ownership scan | 扫描规则要同时支持 flat feature 和 month bucket；archived feature 先读 `archive.md`，必要时再读 `historical/` | 是 |
| Drift Check | 关闭后行为和文档一致性 | 压缩前要确认 drift 已处理；压缩后要确认 archive summary 与 requirement/decision/project memory 一致 | 是 |
| verification evidence | 测试、构建、E2E、review evidence | `archive.md` 必须摘要 verification evidence；完整 evidence 留在 `historical/notes.md` 或 historical detail | 是 |
| scripts / validation glob | 查找 `features/*/spec.md`、`notes.md`、`tests.md` 的脚本 | 需要兼容 `features/YYYY-MM/<feature>/archive.md` 和 `features/YYYY-MM/<feature>/historical/spec.md` | 是 |
| recovery / re-adopt scans | 重接管项目时识别历史 feature | 不应把 archived feature 当 active feature；应优先读 archive summary | 是 |

## 路径兼容规则

第一版需要同时支持两种 feature layout：

```text
.agent-loop/features/YYYY-MM-DD-<feature-slug>/
.agent-loop/features/YYYY-MM/YYYY-MM-DD-<feature-slug>/
```

扫描顺序建议：

1. Active / Paused feature from `project.md`;
2. current-month flat features;
3. recent flat features in 30-day lookback;
4. month bucket `archive.md`;
5. `historical/` only when archive summary is insufficient.

Feature ID 仍然是 `YYYY-MM-DD-<feature-slug>`。路径可能变化，ID 不变。索引更新必须使用当前路径。

## Requirements 策略

Requirements 不做内容压缩。

原因：

- requirement 是人类源材料；
- 需求源材料保持原样，不应被摘要替代；
- requirement lifecycle 和 Delivery Phases 仍由 requirement set README 负责；
- 压缩 feature 不应改变原始需求。

后续可以讨论 requirement month bucket：

```text
.agent-loop/requirements/YYYY-MM/YYYY-MM-DD-<topic>/
```

但第一版只把 feature 压缩作为第一版默认能力。Requirement 的第一层过长问题优先靠 `requirements/INDEX.md` 和未来可选 bucket 解决，不做内容压缩。

## 与 Feature Follow-up / Flow-back 的关系

Feature Follow-up / Flow-back 的默认 30 天 lookback 仍然有效，但不再假设所有 feature 都在 `.agent-loop/features/*/` 第一层。

如果 bug/change 指向 archived feature：

1. 先读 `archive.md`；
2. 判断 delivered behavior、changed files、public interfaces、known risks 是否匹配；
3. 不足时再读 `historical/spec.md`、`historical/tests.md`、`historical/notes.md`；
4. 如果确认为 owning feature，可以建议 flow-back；
5. 如果 archived feature 已 deep archived 且缺少 historical detail，应记录 evidence limitation。

## 与 Close / Drift Check 的关系

Feature Close 不直接压缩，但要让未来可压缩：

- close summary 要足够支持 archive summary；
- requirement mapping 要完整；
- decision mapping 要完整；
- verification evidence 要可摘要；
- drift decision 要记录；
- project memory update 要完成或明确 none。

Feature Compaction Scan 可以视为月度 close 后维护动作。它不替代单个 feature close。

## 迁移策略

### Phase 0: Cross-Platform Script Runtime

- 先批准并实现 `docs/proposal/v1.3.x/cross-platform-python-script-runtime.md`；
- 月度压缩的发现、执行、恢复和后检脚本统一使用 Python 3 标准库；
- 新脚本必须在原生 Windows 与 macOS 上对相同 fixture 给出一致结果；
- Python capability 不可用时 fail closed，不得回退到 Ruby、Bash 或 Agent 手工移动；
- Phase 0 未完成前，不进入本 proposal 的 Runtime Support 或 Compaction Command 实现。

### Phase 1: Proposal

- 只建立规则和影响面；
- 不改运行时规则；
- 不移动现有 feature。

### Phase 2: Runtime Support

- 增加 feature path resolver；
- 所有 recent / targeted / follow-up scan 支持 flat 和 month bucket；
- 增加 `archive.md` / monthly `INDEX.md` 模板；
- 增加 validation scenarios。

### Phase 3: Compaction Command

- 人类触发 Feature Compaction Scan；
- Agent 输出 Candidate Matrix；
- 人类确认后执行 Slim With History；
- 复验所有索引关系。

### Phase 4: Optional Deep Archive

- 仅在更早月份、人类明确要求、historical detail 已不再需要时执行；
- 必须单独列出将删除或外移的文件；
- 必须保留 `archive.md` 和必要 verification summary。

## 待讨论问题

- `features/INDEX.md` 是否应该在第一个 month bucket 出现时自动创建？
- old flat feature 的外部人类书签会失效，是否需要额外生成迁移报告？
- Deep Archive 是否应该支持压缩包，而不是删除 `historical/`？
- requirement month bucket 是否应该和 feature compaction 同期实现，还是作为独立 proposal？
- 如果一个月份有一个 long-running paused feature，是否允许其他 closed features 做 Partial month compaction？
