# Proposal: AI-Led Lightweight Feature Gates

状态：实施与验证完成；最终移除本地 Feature Gate Checker，稳定发布已获人类授权
目标版本：1.5.2（版本与 `v1.5.2` 开发分支由后续人类消息单独授权）
创建时间：2026-07-27
前置设计：

- `docs/proposal/v1.5.x/feature-construction-two-gate-review.md`
- `docs/proposal/v1.5.x/gate2-stable-digest-projection-and-checker-issue-reporting.md`

## 摘要

> 最终实施结论（2026-07-28）：后续混沌测试证明，即使把 Checker 收敛为 Stable digest 单职责，仍会因自然语言 artifact 演进产生伪 Gate。最终实现因此进一步移除了本地 Feature Gate Checker 与 digest 授权路径，由 Agent 直接核对语义、清单、漂移和 Human evidence；focused contracts 只保护客观的两 Gate、Later Start、独立 Gate 与 artifact-owner 边界。下文保留原 Proposal 的问题分析与设计演进证据，最终 runtime 语义以 `references/runtime.md` 和 `references/design.md` 为准。

Agent Loop 已将 Feature construction 收敛为 Gate 1 `Feature Definition Review` 与 Gate 2 `Implementation Readiness Review` 两个人类确认点。当前剩余问题不是 Gate 数量，而是 Checker 同时承担了授权校验、文件完整性校验和内容漂移判断。

当 `spec.md`、`tasks.md`、`tests.md` 或派生证据发生合法运行更新时，摘要不匹配容易被统一呈现为 Gate 校验失败。`review-definition-v2` 已减少 tasks/tests 运行字段造成的 Gate 2 误报，但 Gate 1 仍使用整个 `spec.md` 的原始字节摘要，Gate 2 也仍将 `spec.md` 等稳定文件按原始字节处理。继续为每种字段扩充 Checker 投影会让 Checker 越来越像一个脆弱的 Markdown 语义解析器。

本 Proposal 建议采用：

> AI 负责语义、完整性、漂移与全部 Human Gate 判断；Checker 只安全重算 Agent 记录的 Stable digest。

Gate 保持为人类控制边界，但人类只确认最小且有意义的产品定义和执行授权。Digest 保留为变化探测证据，不再把任何字节变化直接等同于 Gate 失效。

## 1. 问题定义

### 1.1 Gate 1 的误报来源

Gate 1 当前记录整个 `spec.md` 的原始 SHA-256。以下变化即使不改变人类接受的 Feature 定义，也会使摘要失配：

- `Updated`；
- Feature lifecycle `Status`；
- Feature Context Snapshot 的 `Verified At`；
- Snapshot `Freshness`；
- 事实确定的派生证据刷新；
- Markdown 换行或其他不改变含义的表现变化。

Gate 1 的真实问题应当是：

```text
目标、Product Slice、范围、行为、验收或明确排除项是否改变？
```

原始字节是否变化不能独立回答这个问题。

### 1.2 Gate 2 的剩余误报来源

Gate 2 的 `review-definition-v2` 已允许明确列出的 tasks/tests runtime ledger 更新，并排除可轮换 Plan。但它仍有以下限制：

- `spec.md`、`context.md`、contracts 和其他 stable files 仍按原始字节保护；
- 一个未预先枚举但语义安全的变化仍会被当作 Gate 失败；
- 新 Markdown 形态会不断要求新增投影规则；
- Checker 必须理解越来越多本应由 Agent 判断的文档语义；
- Gate 1 与 Gate 2 在同一个命令中联合失败，使错误归属不清。

Gate 2 的真实问题应当是：

```text
当前任务、验证、风险、接口、回滚和执行动作是否仍处于人类接受的实施边界内？
```

### 1.3 人类体验问题

人类不应因为以下执行事实反复看到重新审批：

- 一个任务从 `todo` 进入 `review` 或 `done`；
- 测试结果和证据链接被补充；
- `Updated`、`Verified At` 或运行状态变化；
- 当前 Plan 在已接受的执行边界内轮换或拆分任务；
- Agent 对派生上下文进行事实确定的刷新。

人类只应在产品定义、实施边界或授权动作真正变化时重新进入 Gate。

## 2. 已确认原则

本 Proposal 以人类已确认的以下方向为设计约束：

1. 保留 Gate 1 与 Gate 2，不合并成一个 Gate。
2. Gate 1 只确认目标、范围、验收和明确不做什么。
3. Gate 2 只确认 Agent-ready 范围、验证方式、主要风险/回滚，以及是否开始执行。
4. AI 负责产品语义、实施完整性和漂移分类。
5. Checker 只守住 Stable 文件摘要重算；清单完整性、Gate/action/time、Human provenance、Story/Task/Plan/No-Plan 与范围语义全部由 Agent 判断。
6. Digest 变化是漂移信号，不自动等于 Gate 失效。
7. 只有真实语义变化或无法可靠判断的变化才重新阻塞人类。
8. 本 Proposal 推荐：新增 Task ID 本身不等于扩大授权；同一 Story/Product Slice/Acceptance 与风险边界内的拆分或补充由 AI 判断后继续，只有新增执行边界才回 Gate 2。

## 3. 方案比较

### 方案 A：继续扩充 Stable Digest 投影

为 `spec.md`、`context.md` 和未来文档继续编写字段级投影。

优点：确定性强，Checker 可以独立决定通过或失败。

缺点：Checker 需要持续理解 Markdown 语义；每个模板变化都可能新增误报；字段白名单容易漏项或误放行。

结论：不推荐作为长期主模型。

### 方案 B：AI 语义审查 + 最小 Gate Checker

AI 对当前文档、人类接受的 Gate、清单、作用域和当前动作进行一致性审查；Checker 只重算 Stable digest。Digest 变化只触发 AI 审查，不直接判定 Gate 失败。

优点：符合 Agent Loop 的 Agent ownership；人类 Gate 更轻；Checker 边界稳定；不需要把产品语义编码成脆弱解析器。

缺点：语义判断依赖 Agent 质量；跨会话不明漂移仍需保守返回 Human Review。

结论：推荐并选定。

### 方案 C：删除 Digest，只检查 `accepted`

Checker 只判断字段中是否存在 `accepted`。

优点：实现最简单，几乎没有摘要误报。

缺点：无法发现 Gate 后文档变化；旧授权容易被错误复用；不能守住 task/Plan/Auto-Loop 边界。

结论：拒绝。

## 4. 目标

1. 让 Gate 1/2 成为轻量的人类授权，而不是 Markdown 格式验收。
2. 把语义完整性和漂移判断明确交给 AI。
3. 把 Checker 缩小为稳定、可解释的结构与范围校验内核，不让它冒充 Human provenance 证明器。
4. 避免合法运行证据更新反复触发 Gate 错误。
5. 仍然阻止旧授权复用、越权执行和超范围 Plan。
6. 保持所有 Requirement、ADR、Delivery Contract、Git、外部操作、Submit、Close 与 Release Gate 独立。
7. 不新增 canonical stage、Feature lifecycle、Auto Mode 或 artifact family。

## 5. 非目标

本 Proposal 不做：

- 删除 Gate 1 或 Gate 2；
- 把两次 Feature Review 合并；
- 允许 AI 自行接受新的产品语义；
- 允许 Checker 通过关键词猜测产品语义；
- 允许任何 Agent 静默重建 Human-accepted baseline；
- 允许 `accepted` 单字段授权所有后续动作；
- 删除 Task Done Gate、Feature Close Review 或其他 Human Gate；
- 放宽 Delivery Contract、依赖、迁移、安全、数据、权限、外部操作或 Git 边界；
- 创建 JSON/YAML executable schema；
- 新增独立 Gate manifest 文件或 `.agent-loop/gates/` 目录；
- 修改 Skill 版本号、创建分支、提交或发布。

## 6. 核心职责分离

### 6.1 AI Semantic Review

AI 负责：

- Gate 1 前检查 Goal、Product Slice、Scope、Acceptance 与 Exclusions；
- Gate 2 前检查 tasks/tests/code context/Plan/risk/rollback 的完整性和一致性；
- Gate 后出现变化时判断它仍在已接受执行边界内、改变了 Feature 定义、扩大了实施边界或无法判断；
- 输出简短的差异说明与一个推荐路由；
- 在无法证明安全时停止，而不是假设 Gate 仍然有效。

AI Semantic Review 是现有 Feature Definition Review、Analyze Consistency、Review 和 Drift Check 的职责收敛，不是新 canonical stage。

### 6.2 Gate Checker

Checker 只负责一个可确定的问题：由唯一当前 `Gate 2 Stable Files`、算法和 recorded digest，安全读取这些 Agent 命名的文件并重算 Stable digest。路径规范、regular-file、无 symlink/root escape、无 duplicate/same-file alias 和算法/digest 格式只是完成安全确定读取的输入前置，不代表 Checker 认证了清单完整性。

Checker 不负责：

- 判断 Product Slice 是否产品正确；
- 判断验收标准是否足够；
- 判断测试是否覆盖真实风险；
- 判断一个文字变化是否具有产品语义；
- 判断 Task/Story/Plan/No-Plan/Assessment 是否语义有效；
- 判断 Package/Stable 清单是否完整、Stable 是否排除 Plan、triggered detail 是否覆盖；
- 判断 Gate decision、Auto-Loop、readiness、review time 或当前动作是否一致；
- 证明 Human intent，或判断 Contract、Subagent、Git、外部、Submit、Close、Release 是否获得各自授权；
- 用越来越多字段白名单模拟 Agent 的语义审查。

## 7. 轻量 Gate 交互

### 7.1 Gate 1 最小确认

Gate 1 的 Human Review Summary 默认只显示：

| 项目 | 人类确认内容 |
|---|---|
| 目标 | 要解决的问题和期望结果 |
| 范围 | 本 Feature 负责与不负责的边界 |
| 验收 | 可观察的完成条件与关键异常 |
| 明确不做 | 排除项、后续项或外部边界 |

默认选择：

```text
接受定义并准备实施包
调整定义
暂停
```

接受 Gate 1 只授权 Agent 编写和校验实施包，不授权目标实现。

### 7.2 Gate 2 最小确认

Gate 2 的 Human Review Summary 默认只显示：

| 项目 | 人类确认内容 |
|---|---|
| 执行边界 | Product Slice、Story/Acceptance、初始 Agent-ready tasks 与明确的 Human-gated 项 |
| 验证 | 主要 RED/GREEN、回归、集成/E2E 或替代验证 |
| 风险与回滚 | 主要风险、停止条件和回滚方式 |
| 执行选择 | 只接受方案，或接受并开始实现 |

默认选择保持：

```text
接受实施包并开始实现
只接受实施包，暂不实现
调整实施包
暂停
```

完整 artifacts 仍然可供人类展开查看，但不默认把所有字段复制到审批消息。

## 8. Digest 的新角色

### 8.1 Change Detector，而不是 Gate Judge

现有 Gate 1 Spec Digest、Gate 2 Package Digest 和 Stable Digest 保留为可复现的变化探测证据：

```text
digest unchanged
-> Gate Checker 继续检查授权

digest changed
-> 请求 AI Semantic Review
-> 不立即宣称 Gate invalid
```

Digest 不再独立决定应回 Gate 1、Gate 2 或继续执行。

### 8.2 AI 漂移分类

当变化被探测到时，AI 必须给出一个响应级分类：

```text
within-approved-boundary
feature-definition-change
implementation-boundary-change
unresolved
```

这些值是诊断结果，不是 Feature lifecycle、Gate 状态或 canonical stage。

路由规则：

| 分类 | 路由 |
|---|---|
| `within-approved-boundary` | 记录依据后继续，不询问人类；可包含运行证据更新或同一边界内的任务拆分/补充 |
| `feature-definition-change` | 回 Gate 1 |
| `implementation-boundary-change` | 回 Gate 2 |
| `unresolved` | 停止并向人类提出一个阻塞问题 |

### 8.3 跨会话证据

在同一连续上下文中，`within-approved-boundary` 可以记录到现有 Feature `notes.md` 历史证据中，不新增文件。若判断涉及新增任务，记录其 `Derived From`、Story/Product Slice/Acceptance 映射，以及为什么没有改变验证义务、风险、接口或回滚边界。

跨会话、context compaction、Resume 或 later package-only start 依赖该判断时，记录一个紧凑的 Gate Drift Assessment：

```text
Gate Drift Assessment:
- Gate: 1 | 2
- Baseline Digest: sha256:...
- Current Digest: sha256:...
- Classification: within-approved-boundary | feature-definition-change | implementation-boundary-change | unresolved
- Changed Areas: <paths/sections>
- Reason: <evidence-backed semantic reason>
- Assessed At: <ISO-8601>
```

该记录进入现有 `notes.md`，不是新 artifact。它是 Agent-owned audit evidence；Checker 不解析、排序或授权该表。AI 判断为 `within-approved-boundary` 后，先记录 prior/current digest 与理由，再用只读 `--mode digest` 刷新当前摘要并重跑。

## 9. Checker 结果模型

Checker 对外区分以下 evidence 结果，不把摘要一致冒充为授权，也不把所有非零结果描述为 Gate 失败：

```text
EVIDENCE_MATCH
EVIDENCE_CHANGED
EVIDENCE_INVALID
```

- `EVIDENCE_MATCH`：Agent 命名的 Stable 文件重算摘要与记录一致；它不证明清单完整或 Human authorization。
- `EVIDENCE_CHANGED`：有效证据字节变化；Controller 路由 AI Semantic Review，不直接重新询问人类。
- `EVIDENCE_INVALID`：三个 Stable 输入字段或命名文件无法安全、确定地读取与重算。

这些是 Checker 运行结果，不是项目状态。`EVIDENCE_CHANGED` 必须有与 invalid 不同的稳定退出码，避免 Agent 把一次待分析变化误报成 Checker defect。Task/Story/Plan/No-Plan/Assessment 等 Markdown 语义不属于结果计算输入。

## 10. Gate 1 路由规则

以下变化回 Gate 1：

- Feature Goal 或目标用户结果改变；
- Product Slice 新增、删除或重新解释；
- in-scope / out-of-scope 边界改变；
- Added / Modified / Removed behavior 改变；
- Acceptance Criteria 或关键异常/恢复要求改变；
- 角色、权限、状态、事实归属、产品规则或 Requirement/ADR authority 改变；
- AI 无法证明现有 Gate 1 Summary 仍覆盖当前 Feature 定义。

以下变化默认不回 Gate 1：

- `Updated` 或 Feature lifecycle `Status`；
- Snapshot `Verified At` / `Freshness` 的事实刷新；
- 未改变 Product Slice/Scope/Acceptance 的 source digest 刷新；
- 格式、换行、链接修复或证据补充；
- Gate 1 已授权范围内的实施包准备。

若所谓“证据刷新”暴露了新的产品语义，仍回 Gate 1。

## 11. Gate 2 路由规则

以下变化回 Gate 2：

- 新增任务带来新的 Story、Product Slice、Acceptance 或用户可见行为；
- 删除或重排任务导致执行/交付边界、依赖屏障或风险发生实质变化；
- task/story 映射改变且无法继续归属于已接受的 Product Slice/Acceptance；
- 验证命令、关键断言、测试策略或替代验证改变；
- 接口、数据、迁移、安全、权限、依赖或风险级别改变；
- 回滚、停止条件或外部影响改变；
- 新 task 无法证明来自已接受任务/Story/Acceptance，或扩大其执行边界；
- Plan 超出已接受的 Product Slice、Story、Acceptance、验证、风险或回滚边界；
- AI 无法证明当前实施包仍满足 Gate 2 Summary。

以下变化默认不回 Gate 2：

- 任务状态、完成 checkbox、Review/Drift 结果；
- 测试执行结果和证据链接；
- 已接受执行边界内的 Active Plan Scope 轮换；
- 把已接受任务拆成更小任务，或补充同一 Acceptance 所需的实现/测试任务；
- 新任务明确映射到已接受的 Story/Product Slice/Acceptance，且不改变验证义务、风险、接口、依赖和回滚；
- 不改变验证义务、风险、接口或回滚的事实确定实现细化；
- `notes.md` 中的执行证据和进度记录。

因此：

```text
新增 Task ID != 自动重新 Gate 2
新增执行边界 = 重新 Gate 2
```

Gate 2 记录的 Agent-ready task IDs 是人类看到的初始执行分解，不是不可变化的绝对白名单。执行授权最终绑定的是已接受的 Feature/Product Slice/Story/Acceptance 与验证、风险、接口和回滚边界。新增任务必须由 AI 明确分类为 `within-approved-boundary`；Checker 只报告当前完整安全证据是否 `MATCH | CHANGED | INVALID`，不验证其 Task 映射或 Assessment 语义。

## 12. 安全边界

轻量 Gate 不等于弱授权。

以下输入错误由 Checker 返回 `EVIDENCE_INVALID`：三个 Stable 字段缺失/重复、`notes.md` 无法安全读取、Stable list 为空或路径无法安全确定地读取、算法未知或 digest 格式非法。

以下错误由 Agent 硬停止，即使 Checker 返回 `EVIDENCE_MATCH`：Package/Stable 清单遗漏或关系错误；Plan 未排除；Gate/action/time/readiness 不一致；当前 Task/Story/Plan/No-Plan/Assessment 无法映射到接受边界；错误路由 Feature/implementation boundary；借用 Gate 1/2 执行独立授权动作；Human provenance 不可靠；或 `unresolved` 后仍试图继续。

Checker 不提供 `--force`、`--bypass` 或自动重建 accepted baseline 的能力。

## 13. 兼容与迁移

1. 已有 `raw-v1` 和 `review-definition-v2` evidence 保持 reader-compatible。
2. 旧项目不要求批量迁移。
3. 新证据默认使用 `raw-v1`；它不是 legacy。已有显式 `review-definition-v2` 仅保留 reader compatibility。
4. 任一 digest mismatch 都不得静默改写为当前 baseline；先进入 AI Semantic Review，不得通过切换算法隐藏变化。
5. AI 能用现有 artifacts、notes 和明确映射证明变化仍为 `within-approved-boundary` 时，可生成对应 Assessment；跨会话证据不足时使用 `unresolved`，返回人类而不是猜测。
6. 迁移不得改变既有人类 Gate 决定、accepted execution boundary 或 Auto-Loop 授权。
7. 不修改 Skill 版本，除非人类另行批准版本同步。

## 14. 协调实施影响面

这是 coordinated workflow change，因为它改变 Gate Checker 结果、Digest 语义和 Human Review 路由。实施必须一起检查：

- `SKILL.md`
- `references/design.md`
- `references/runtime.md`
- `references/stage-guides.md`
- `references/human-review-summary.md`
- `references/workflow-checklists.md`
- `references/artifact-rules.md`
- `references/project-guidance.md`
- `references/checker-recovery.md`
- `references/validation-scenarios.md`
- `templates/root-AGENTS.md`
- `templates/spec.md`
- `templates/notes.md`
- `templates/tasks.md`
- `templates/tests.md`
- `scripts/check-feature-review.py`
- affected Python/Shell tests
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

实施计划必须先核对实际引用，不允许仅为满足关键词测试修改所有列出的文件。

## 15. RED / GREEN 验证要求

Focused RED 必须至少证明：

1. Gate 1 后只改变 `Updated`/Status/Snapshot evidence 会被当前 Checker 当作 Gate 1 digest failure。
2. Gate 2 后合法 task/test runtime evidence 不会回归，但 `spec.md` 的合法派生证据刷新仍会触发当前失败。
3. 当前 Checker 不能区分“需要 AI 评估”与“授权真正无效”。
4. 当前联合错误不能稳定告诉 Agent 应回 Gate 1、Gate 2 还是 Diagnose Checker。

最终 GREEN 必须至少证明：

1. Stable 输入字段或其命名文件无法安全重算时为 `EVIDENCE_INVALID`；manifest 遗漏和动作配对错误由 Agent 停止。
2. digest 变化返回 `EVIDENCE_CHANGED`，不是 `EVIDENCE_MATCH` 或 Checker defect。
3. Agent 命名的 Stable 文件与摘要一致时返回 `EVIDENCE_MATCH`，但不声称清单完整或 Human authorization。
4. canonical `check` 与兼容别名 review/start/execute 使用完全相同的 Stable digest 路径，并保持只读。
5. fenced examples、Task/Plan/Assessment Markdown 不参与 Checker 语义判断。
6. package-only 不能 execute，但由 Agent 判断；later-start 使用相同 Stable check，不由 Checker 判断动作。
7. AI 继续把 `feature-definition-change`、`implementation-boundary-change`、`unresolved` 路由到 Gate 1、Gate 2 或一个人类问题。
8. accepted boundary 内的 Plan rotation 与 Task 拆分由 AI 判断；新增 Story/Acceptance/依赖/接口/风险/回滚义务仍回 Gate 2。
9. Contract、Subagent、Git、外部、Submit、Close、Release Gate 不被继承。
10. macOS/POSIX 与 Windows Python 3.10+ 入口行为一致。

## 16. Full Validation 要求

实施触及 Human Gate、controller routing 和 checker recovery 语义，必须执行：

- focused RED/GREEN；
- 全部 `tests/*.sh`；
- 全部 Python unittest/discovery；
- YAML / JSON / Shell / Ruby / Markdown fence 检查；
- `git diff --check`；
- `docs/maintenance/full-validation-method.md` 的六域语义审计；
- 新中文验证报告；
- Gate 1、Gate 2、Task Done、Feature Auto-Loop、Task Auto-Run、Feature Context、Checker Recovery、Delivery Contract、Git/Submit/Close 的压力场景。

## 17. 风险与缓解

### 风险 1：AI 错把定义变化判断为运行变化

缓解：Gate Summary 保留人类接受的 Goal/Scope/Acceptance/Exclusions 与 task/verification/risk/rollback 边界；不确定必须使用 `unresolved`；高风险领域变化明确回 Gate。

### 风险 2：Agent 错误记录 Drift Assessment

缓解：Assessment 必须绑定 Feature、Gate、prior/current digest、changed areas 和时间；这是 Agent-owned 审计证据，不由 Checker 冒充语义验证。该机制不能消除 AI 判断风险，但能保留可复核的转换记录。

### 风险 3：Checker 过轻导致旧授权长期复用

缓解：Checker 只验证 Stable bytes 是否变化；Resume/context loss 必须由 Agent 重新检查完整 package、Gate/action/time、Human 证据和 accepted execution boundary。

### 风险 4：轻量化重新增加人类提示

缓解：`within-approved-boundary` 是 Agent-owned 判断，不请求人类；只有真实 Gate 边界变化或 `unresolved` 才停。

## 18. 验收条件

本 Proposal 的实施验收条件：

1. Gate 1 与 Gate 2 保留，但 Human Review Summary 缩减为最小决策信息。
2. AI 成为语义完整性和漂移分类的责任主体。
3. Checker 成为单一职责 Stable digest 重算器，不认证 manifest 完整性，不解析 Gate/Task/Plan/Assessment，也不证明 Human provenance。
4. Digest 变化触发 `EVIDENCE_CHANGED`，不自动宣称 Gate invalid；有效且一致为 `EVIDENCE_MATCH`，确定性证据错误为 `EVIDENCE_INVALID`。
5. `within-approved-boundary` 可由 Agent 记录后继续，不重复询问人类。
6. 新增 Task ID 本身不触发 Gate 2；只有 Feature 定义或实施执行边界变化才分别回 Gate 1 / Gate 2，无法判断才阻塞询问。
7. Stable 输入缺失、危险/别名路径或 digest 非法由 Checker 阻断；清单遗漏、动作类型不匹配和 Task/Plan 映射由 AI 硬停止。
8. 既有独立 Human Gates、质量阶段和完成规则保持不变。
9. 不新增 canonical stage、lifecycle、Auto Mode、JSON/YAML schema 或独立 Gate artifact。
10. 通过 focused 与 full validation 后才可声称实现完成。

## 19. Human Review

已确认：

- 人类要求“让 Gate 轻一点”；
- 人类接受保留两个 Gate；
- 人类接受 AI 校验语义、Checker 校验 Gate 的总体方向。
- 本 Proposal 已纳入“新增 Task ID 不自动重新授权；新增执行边界才重新 Gate 2”的规则；
- 人类已批准 Implementation Plan、`v1.5.2` 开发分支与 1.5.2 版本同步。
- 最终 chaos 暴露本地可重算摘要无法证明 Human provenance 后，人类明确选择轻量方案：不故意防范 AI 越权，Agent 从可靠会话判断授权，Checker 只守确定性证据。
- 第二轮 chaos 暴露 Task/Plan/Assessment Markdown 解析仍会产生新的假阳性/假阴性；第四轮后人类最终确认 Checker 只需重算 Stable 摘要，文件覆盖也回归 Agent。
- 第三轮 chaos 暴露 Stable 闭包、UTF-8、空清单项、same-file alias、fence closing 与 Windows absolute path 边界，以及 `raw-v1`/Pause/内联 notes 的跨文件歧义；人类授权按相同轻量模型修复。
- 第四轮 chaos 继续暴露 v2 非投影文件误报和 review-time 跨文件歧义后，人类明确要求停止扩张 Checker：Checker 只处理 Stable digest，其余全部由 Agent 核对。

待确认：

- 最终 Human Review 是否接受实现与验证结果；
- commit、push、tag、release、publish、`main` 同步和 installed Skill 同步仍未授权。

## 20. 实施结果

主体实现已完成两个轻量 Human Gate与 AI Semantic Review。第四轮决定进一步废止 Checker 的 manifest 完整性、Gate/action/time 与阶段模式判断，只保留 Stable digest 安全重算；`review | start | execute` 仅为同一 `check` 路径的兼容别名。旧 `review-definition-v2` 只投影 Task/Test，其余命名文件按原始字节哈希。未新增 canonical stage、message intent、lifecycle、Auto Mode、独立 Gate artifact 或 executable schema。

验证证据：

- Task 13 RED：29 tests 产生 14 个预期失败记录；GREEN focused 50 / 50 PASS；单职责压力集 7 / 7 PASS；
- Task 13 full Shell：45 / 45 PASS；full Python：338 / 338 PASS；全部机械检查 PASS；

- 第二轮 chaos 最小职责 RED：6 / 6 按预期失败；补充 Gate 1 digest RED：1 / 1 按预期失败；
- focused Feature checker + Python checker contract：51 / 51 PASS；双 Gate Shell contract：PASS；
- 第三轮证据 chaos：79 / 79 PASS；生命周期 executable chaos：31 / 31 PASS；
- full Shell：45 / 45 PASS；full Python：339 / 339 PASS；
- YAML / JSON / Shell / Ruby / Python AST / Markdown fence / `git diff --check`：PASS；
- 第二轮独立 chaos 作为本轮 RED 来源；修复后相同攻击维度均进入 focused GREEN。本轮未在缺少新授权时再次派发 Agent。

最新完整结果见 `docs/reports/agent-loop-v1.5.2-full-validation-2026-07-27.4.md` 与 `docs/reports/ai-led-lightweight-feature-gates-feature-validation-2026-07-27.4.md`。当前仍未执行提交或发布。
