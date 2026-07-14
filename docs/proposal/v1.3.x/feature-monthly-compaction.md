# Proposal: Feature Monthly Archive

状态：已实现；待最终 Human Review

平台证据：`macOS-verified / Windows-test-defined`

Human Review：2026-07-14，人类确认采用整目录按月归档、根 `features/archive.md` locator、统一引用更新、post-check、失败恢复与 rehydrate 设计

实施计划：`docs/proposal/v1.3.x/feature-monthly-archive-implementation-plan.md`

目标版本：v1.3.0 候选

创建时间：2026-07-01

最近更新：2026-07-14

> 文件名保留 `feature-monthly-compaction.md` 以维持历史引用；本 proposal 的能力名称和行为已经收敛为 `Feature Monthly Archive`。这里的 archive 只改变 feature 目录位置和默认发现入口，不压缩、重组或删除 feature 内容。

## 摘要

人类可以选择一个或多个历史月份，例如 5 月和 6 月。Agent 先扫描这些月份对应的 flat feature，只有生命周期为 `closed` 且关闭证据完整的 feature 才能进入候选。人类确认后，Agent 把每个候选 feature 目录原样移动到各自的月份目录，并在 `.agent-loop/features/archive.md` 记录稳定 Feature ID、当前位置和一行交付摘要。

```text
Human selects 2026-05 and 2026-06
→ read-only Feature Monthly Archive Scan
→ show eligible / blocked features and reference updates
→ one Batch Human Gate
→ move each eligible feature directory intact
→ update features/archive.md and durable references
→ post-check paths, links, indexes, and feature contents
```

这个能力解决的是 `.agent-loop/features/` 第一层过长和历史 feature 默认扫描过重的问题，不解决磁盘空间问题。

## 目标

1. 当前或仍在工作的 feature 继续留在 `.agent-loop/features/` 第一层；
2. 人类可以一次选择一个或多个历史月份进行归档；
3. 每个 eligible feature 目录完整移动到 `features/YYYY-MM/`，内部文件结构不变；
4. `features/archive.md` 成为 archived Feature ID 到当前位置的稳定 locator；
5. Follow-up、ADR、Requirement Mapping 和 Project Memory 使用统一引用更新逻辑；
6. 归档前只读发现，归档后强制检查，失败时恢复；
7. macOS 与 Windows 使用同一套 Python 标准库脚本和 fixture。

## 非目标

第一版明确不做：

- 不自动按日历月份运行；
- 不自动归档当前月；
- 不移动 `active`、`blocked` 或 `paused` feature；
- 不修改 feature 的业务内容或生命周期含义；
- 不生成每个 feature 的新 `archive.md`；
- 不创建 `historical/`；
- 不创建 `features/YYYY-MM/INDEX.md`；
- 不删除、打包、外移或摘要替代 `spec.md`、`tasks.md`、`tests.md`、`plan.md`、`notes.md`、`product.md`、`contracts.md` 或细节目录；
- 不压缩 `requirements/`、`.agent-loop/decisions/` 或 project memory；
- 不把 `features/archive.md` 变成产品、需求、决策或验证事实的权威来源；
- 不允许 Agent 手工移动目录来绕过 scan、Human Gate、post-check 或 restore。

Deep Archive、Summary Only 和历史文件删除不属于本 proposal。未来如果确实需要，应单独提案和单独评估恢复风险。

## 目录模型

归档前：

```text
.agent-loop/
  features/
    2026-05-08-login/
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
    2026-06-12-payment/
      product.md
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
      contracts.md
      contracts/
    2026-07-10-current-feature/
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
```

人类选择归档 2026-05 和 2026-06 后：

```text
.agent-loop/
  features/
    archive.md
    2026-05/
      2026-05-08-login/
        spec.md
        tasks.md
        tests.md
        plan.md
        notes.md
    2026-06/
      2026-06-12-payment/
        product.md
        spec.md
        tasks.md
        tests.md
        plan.md
        notes.md
        contracts.md
        contracts/
    2026-07-10-current-feature/
      spec.md
      tasks.md
      tests.md
      plan.md
      notes.md
```

归档只增加月份目录并移动整个 feature 目录。feature 内部同目录或子目录关系保持不变；由于目录深度增加，指向 feature 外部的相对 Markdown 链接必须进入 Reference Impact Scan 并按新位置更新。

## 稳定 Feature ID 与路径解析

Feature ID 保持不变：

```text
2026-05-08-login
```

路径可以变化：

```text
flat:     .agent-loop/features/2026-05-08-login/
archived: .agent-loop/features/2026-05/2026-05-08-login/
```

规则：

1. Feature ID 是稳定身份；目录路径只是当前位置；
2. active / blocked / paused feature 必须位于第一层；
3. archived feature 通过 `features/archive.md` 解析当前位置；
4. 新增或更新的 durable relationship 应同时记录 Feature ID；
5. 仍然保存直接路径的现有引用必须在移动时更新；
6. resolver 不得仅依赖 `features/*/spec.md` 这种单层 glob；
7. archived feature 的原 `spec.md` 仍然是 Feature Spec，归档不会把它替换为摘要。

## `features/archive.md`

`features/archive.md` 是 archive locator 和移动历史账本，不是业务事实来源。它在第一次成功归档时创建，此后由 archive / rehydrate 操作维护。

推荐模板：

```md
# Feature Archive

This file locates archived or rehydrated features. The feature's own spec, tests, notes, requirement sources, and accepted decisions remain authoritative.

| Feature ID | Month | Current Path | Archive State | Closed At | Delivered Summary | Source Requirements | Applicable Decisions | Last Moved At |
|---|---|---|---|---|---|---|---|---|
| 2026-05-08-login | 2026-05 | `.agent-loop/features/2026-05/2026-05-08-login/` | archived | 2026-05-20 | 完成登录认证与失败路径验证 | `.agent-loop/requirements/2026-05-01-login/` | `.agent-loop/decisions/ADR-001-login.md` | 2026-07-14 |
```

字段规则：

- `Feature ID`：稳定且唯一；
- `Month`：来自 Feature ID 的年月，不从移动日期推导；
- `Current Path`：当前真实目录；
- `Archive State`：`archived | rehydrated`，它不是 feature lifecycle status；
- `Closed At`：来自 feature Close Record；
- `Delivered Summary`：来自已关闭 feature 的交付/关闭记录，只写一行，不创造新产品含义；
- `Source Requirements` / `Applicable Decisions`：只保存 locator；
- `Last Moved At`：最近一次 archive 或 rehydrate 日期。

`spec.md` 仍使用正式 lifecycle：

```text
draft | active | blocked | paused | closed
```

归档资格只接受 `closed`。不要把 `implemented` 或 `archived` 写成 feature lifecycle status。

## 人类触发

示例：

```text
把 2026 年 5 月和 6 月已经关闭的 feature 按月份归档。
```

这条指令只授权进入 `Feature Monthly Archive Scan`。Agent 必须先展示扫描结果和精确变更范围，再请求一次 Batch Human Gate；不得收到月份后直接移动目录。

## Feature Monthly Archive Scan

Scan 是只读操作。

输入：

- 人类选择的月份；
- `.agent-loop/features/` 第一层 feature；
- 已有月份目录；
- `features/archive.md`（如果存在）；
- `project.md` Active Feature / Paused Features / Current Work；
- feature `spec.md`、`tasks.md`、`tests.md`、`plan.md`、`notes.md`、close record；
- requirement set README 和 optional `requirements/INDEX.md`；
- `.agent-loop/decisions/*.md`；
- Follow-up / Flow-back、verification、review 和 drift evidence；
- repository 内指向候选 feature 旧路径的文本与 Markdown 链接。

输出：

- Candidate Matrix；
- eligible 和 blocked 原因；
- old path → new path 映射；
- `features/archive.md` 预期新增/更新行；
- Reference Impact List；
- path collision、symlink/path escape 和 stale-plan 检查结果；
- post-check 与 restore 范围；
- Batch Human Review Summary。

## Candidate Matrix

```md
| Month | Feature ID | Current Path | Lifecycle | Close Evidence | Open Follow-up | Reference Impact | Decision |
|---|---|---|---|---|---|---:|---|
| 2026-05 | 2026-05-08-login | `.agent-loop/features/2026-05-08-login/` | closed | complete | none | 4 | eligible |
| 2026-05 | 2026-05-22-import | `.agent-loop/features/2026-05-22-import/` | paused | incomplete | none | 2 | blocked |
| 2026-06 | 2026-06-12-payment | `.agent-loop/features/2026-06-12-payment/` | closed | complete | none | 7 | eligible |
```

资格按 feature 判断，不要求一个月份的所有 feature 都完成。人类可以一次批准多个 selected-month 中的 eligible feature；blocked feature 保持 flat，不影响其他 eligible feature，但 Human Review Summary 必须明确显示同月存在 flat 与 archived feature。

## Eligibility And Safety Gate

每个 candidate 必须同时满足：

- 人类明确选择了该月份；
- 该月份不是当前月份；
- feature `spec.md` lifecycle 是 `closed`；
- Close Record 存在；
- tasks 全部为 `done` 或经过人类确认移出范围的 `skipped`；
- fresh verification、Feature Close Review、drift decision 和 project-memory impact 已记录；
- 没有 open follow-up、unresolved drift、review blocker 或待恢复的失败操作；
- `project.md` 不把它列为 Active Feature 或 Paused Feature；
- requirement `Feature Mapping` / `Implemented By` 和相关 decision `Implemented By` 已完成关闭时回填；
- 源目录真实存在且位于 `.agent-loop/features/` 第一层；
- 目标月份与 Feature ID 年月一致；
- 目标路径不存在，不发生大小写或 Unicode 归一化碰撞；
- 源目录、目标目录和被更新引用不得通过 symlink 逃逸 workspace；
- Reference Impact List 覆盖所有已发现旧路径引用和跨 feature 边界相对链接；
- post-check 和 restore 所需的原路径、目标路径、内容快照与引用快照能够写入批次 transaction journal。

任何一项不满足都必须 fail closed。不要提供 `--force` 绕过资格和安全检查。

## Batch Human Gate

一次普通归档批次只需要一个 Human Gate。确认摘要必须同时列出：

- selected months；
- eligible / blocked Feature IDs；
- 每个 old path → new path；
- 将创建的月份目录；
- `features/archive.md` 预期变化；
- Requirement、ADR、Project Memory、Follow-up 和其他引用更新；
- 不会修改或删除的 feature 内容；
- post-check 与失败 restore 行为。

人类确认这个完整批次后，Agent 可以执行其中列出的目录创建、移动、引用更新和 post-check，不为每个机械步骤重复询问。

任何新增月份、Feature ID、目标路径、引用文件、删除动作或批次范围变化都使原确认失效，必须重新 Scan 和确认。

## 引用更新逻辑

### Feature Follow-up / Flow-back

扫描顺序：

1. 从 `project.md` 读取 Active / Paused feature；
2. 扫描第一层 flat feature；
3. 读取 `features/archive.md`；
4. 对匹配的 archived Feature ID 读取其原有 `spec.md`、`tests.md` 和 `notes.md`；
5. 只有摘要与路径信号不足时才继续读取复杂细节目录。

归档不会改变 owning feature 判断，也不会把 archived feature 自动重开。

### ADR / Decision

- `Applicable Decisions` 和 `Implements Decisions` 的语义不变；
- 直接保存 Feature Spec 路径的 ADR / decision 引用更新到 month path；
- validator 必须同时支持 flat 和 archived Feature Spec；
- 后续 durable mapping 应优先保存 Feature ID，并通过 resolver / `features/archive.md` 定位路径；
- 归档不得改写 accepted decision 的含义、状态或 Human Review Evidence。

### Requirement Mapping

- requirement set README 的 `Feature Mapping` / `Implemented By` 保留 Feature ID；
- 直接路径更新为当前 month path；
- optional `requirements/INDEX.md` 如保存 feature path，也同步更新；
- 原始 requirement source 文件保持不变。

### Project Memory

- Active Feature 和 Paused Features 不得指向 archived feature；
- Current Work 不得把 archived feature 当作正在执行的 feature；
- Recent Feature 或历史 locator 如存在，更新为 Feature ID 加当前路径；
- 不把所有 archive rows 复制进 `project.md`，历史 inventory 由 `features/archive.md` 负责。

### Internal And External Links

- feature 目录内部文件和子目录保持原样；
- 同目录和 feature 内部相对链接通常保持有效；
- 因目录加深而受影响的 `requirements/`、`decisions/`、project docs 等跨边界相对链接必须更新；
- workspace 内指向 old flat path 的 durable reference 必须更新；
- 历史报告中只用于描述过去命令或过去路径的纯文本证据可以保留，但必须由 Reference Impact Scan 分类为 `historical-evidence`，不能静默忽略。

## Apply、Post-Check 与失败恢复

Apply 只能执行人类确认过的 Feature ID 和路径映射。开始时必须重跑关键 preflight；如果文件、状态、引用计数或目标路径与确认时不同，判定 `stale-plan` 并停止。

Apply 在首次写入前创建临时 transaction journal：

```text
.agent-loop/features/.archive-txn/<transaction-id>/
```

journal 只保存本批次操作映射、preflight 摘要，以及将被改写的 `archive.md` / Requirement / ADR / Project Memory / link 文件快照；它不复制 feature 目录。成功 post-check 后删除 journal；失败或进程中断时保留 journal，供 restore 在新的 Agent 进程中恢复。journal 是临时恢复材料，不是 feature lifecycle 或 project memory 的新权威来源。

推荐执行顺序：

```text
revalidate confirmed scope
→ prepare reversible operation snapshot
→ persist transaction journal
→ create selected month directories
→ move whole feature directories
→ update features/archive.md
→ update approved durable references
→ run post-check
→ keep result only when every check passes
```

Post-check 必须确认：

- 每个 source path 已不存在；
- 每个 target path 存在且 Feature ID 与月份匹配；
- feature 文件清单和内容哈希与移动前一致，只有已批准的跨边界链接调整除外；
- `features/archive.md` 每个 Feature ID 恰好一行且 Current Path 存在；
- 没有 durable reference 仍指向 old flat path；
- Requirement、ADR、Project Memory 和 Follow-up resolver 能解析新路径；
- blocked / unselected / current feature 没有变化；
- 重复运行 scan 得到 `already-archived`，不会再次嵌套月份目录。

如果任一写入或 post-check 失败，操作必须恢复：

- 目录移回原 flat path；
- 从 transaction journal 恢复 `features/archive.md` 和引用文件快照；
- 检查恢复后文件清单、哈希和旧路径；
- 报告失败点和恢复结果；
- restore 未完全通过时进入 Safety Stop，不得报告归档成功。

## Rehydrate / Reopen

当 Follow-up 确认 archived feature 是 owning feature，并且人类确认 flow-back / reopen 后：

```text
archived feature selected
→ read-only rehydrate scan
→ Human Review shows month path → flat path and reference impact
→ move the whole directory back to `.agent-loop/features/<feature-id>/`
→ update archive row to `rehydrated` and Current Path to flat
→ update durable references
→ post-check
→ normal Feature Follow-up lifecycle may set the feature active
```

Rehydrate 只是恢复工作目录位置，不自行授权 scope change，不自行把 `closed` 改为 `active`。Feature Follow-up 的人类决定仍然控制是否重开。

## 跨平台脚本边界

生产脚本使用 Python 3.10+ 标准库，并复用 cross-platform runtime 的 UTF-8、BOM/CRLF、确定性排序、path confinement 和 exit-code 约定。

建议入口：

```text
scripts/scan-feature-monthly-archive.py
scripts/apply-feature-monthly-archive.py
scripts/check-feature-monthly-archive.py
scripts/restore-feature-monthly-archive.py
```

契约：

- scan 和 check 只读；
- apply 和 restore 只接受人类确认范围；
- Python capability 不满足时 exit 2 并 fail closed；
- 不回退到 Ruby、Bash、PowerShell 或 Agent 手工移动；
- 不自动安装 Python；
- macOS 与 Windows 对相同 fixture 给出相同候选、阻塞、路径和恢复结论。

## 实施顺序

### Phase 0: Cross-Platform Python Runtime Acceptance

- canonical Python checker、macOS parity 和 CI matrix 已实现；
- 当前本地报告仍标记 `Windows-test-defined`，不得把它写成 Windows 已通过；
- 先读取远端 Windows CI 证据并完成最终 Human Review；
- Phase 0 未最终 accepted 前，不实现 archive apply / restore。

### Phase 1: Proposal Revision

- 本 proposal 收敛为整目录归档；
- 移除内容重组、`historical/`、Deep Archive 和删除路径；
- 明确 Feature ID、archive locator、Batch Human Gate、post-check 和 rehydrate。

### Phase 2: Reader Compatibility

- 增加统一 Feature Path Resolver；
- Follow-up、Targeted Scan、Recovery / Re-Adopt 支持 flat 与 month path；
- ADR / requirement validators 支持 archived Feature Spec；
- 新建 active feature 仍只使用 flat path；
- 增加 `features/archive.md` 模板和 validation scenarios；
- 完成 reader compatibility 后仍不移动真实 feature。

### Phase 3: Scan And Post-Check

- 实现只读 scan 和 check；
- 固定 Candidate Matrix、Reference Impact List、exit code 和 deterministic output；
- 用 fixture 证明 active / paused / blocked、open follow-up、stale path、collision、symlink escape 和 broken link 会 fail closed。

### Phase 4: Apply And Restore

- 实现人类确认后的整目录移动和引用更新；
- 实现 stale-plan stop、失败恢复、幂等和 rehydrate；
- 在 Windows 与 macOS 运行相同 fixture；
- 通过 focused validation、full validation 和 Human Review 后才允许真实项目归档。

## 验收场景

至少覆盖：

1. 人类选择 5 月和 6 月，多个 closed feature 被移动到各自月份；
2. 同月 paused feature 保持 flat，eligible closed feature仍可在明确批次中归档；
3. 当前月、active、blocked、paused、open follow-up 和 incomplete close feature 被拒绝；
4. 整目录移动前后文件清单和哈希一致；
5. 跨边界相对链接和 old flat path 引用被正确更新；
6. `features/archive.md` locator 可以解析所有 archived Feature ID；
7. ADR Feature Spec、Requirement Mapping、Project Memory 和 Follow-up 扫描能解析 month path；
8. 路径碰撞、大小写冲突、Unicode 差异、symlink escape 和 stale-plan 被拒绝；
9. 中途失败恢复全部目录和引用；
10. 重复 apply 不产生 `YYYY-MM/YYYY-MM/<feature>`；
11. rehydrate 把整个 feature 恢复到 flat path，并保持 Feature ID 与文件内容；
12. Windows 与 macOS 对相同 fixture 输出一致；
13. scan / check 不修改任何文件；
14. 任何脚本都不提供删除历史内容或 `--force` 绕过路径。

## Proposal Boundary

本文件仍是 proposal，不是发布运行时权威。它不会自行改变 `SKILL.md`、`references/runtime.md`、`references/design.md`、Feature Follow-up、ADR validator 或目标项目目录。

本实现是在 proposal 与实施计划分别获得 Human Review 授权后开始，并先完成 Phase 0、Reader Compatibility 与 RED/GREEN 契约。源码仓库中的实现与测试不会移动任何真实目标项目 feature；目标项目执行 archive 或 rehydrate 仍必须分别经过运行时 Human Gate。
