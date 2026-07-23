# Proposal: Project Skill Discovery Guard

状态：Proposal 已批准，实施与验证完成，待 Human Review
目标版本：v1.4.0 开发线；不修改 Skill 版本号
创建时间：2026-07-16
默认语言：中文

## 摘要

Agent Loop 已经支持项目私有的 `.agent-loop/skills/`、`bootstrap | on-demand` 渐进加载、SHA-256 Validated Content Manifest 和每次调用的 Execution Gate，但当前发现规则主要绑定 Project Entry、Resume、Re-Adopt、上下文恢复和 controller re-entry。

这留下一个路由漏洞：当 Agent 已经进入项目、随后收到一个新的可执行意图时，可能只查看运行时暴露的全局 Skill inventory，先断言“没有相关 Skill”或进入通用 Operational Support，直到人类提醒后才检查 `.agent-loop/skills/INDEX.md`。

本 proposal 在现有 Project-Local Skills 模型内增加一个轻量的 `Project Skill Discovery Guard`：

```text
reliable Agent Loop project context
-> latest actionable intent / stage route
-> inspect project skill INDEX metadata
-> match active bootstrap / on-demand candidates
-> verify matched INDEX row, path, and manifest
-> read-only load the matched Project Skill
-> disclose invocation scope
-> Execution Gate
-> execute only after authorization

no valid match
-> only then permit generic helper / Operational Support fallback
```

它是 Intent Routing 与 stage action 之间的内部守卫，不新增 canonical stage、message intent、artifact、lifecycle status 或自动执行权限。

## 1. 背景与现有能力

### 1.1 当前已经具备

Agent Loop 当前已经规定：

- `.agent-loop/skills/INDEX.md` 是项目技能生命周期和发现索引；
- `active` Project Skill 才能进入正常路由；
- `bootstrap` 在 Project Entry、Resume、Re-Adopt、上下文恢复和 controller re-entry 时可发现；
- `on-demand` 根据 message、stage 或 task context 的 trigger 渐进加载；
- Agent 在依赖技能前必须验证精确 INDEX row、技能路径和 Validated Content Manifest；
- 发现、读取 INDEX、匹配 trigger 和只读加载不需要人类确认；
- 每次实际调用仍必须通过 Execution Gate；
- Agent Loop controller 和 Human Gates 高于 Project Skill、runtime/global helper 和内置 fallback；
- Project Skill 不全局安装，也不复制到运行时原生 Skill 目录。

### 1.2 已观察到的失败

一次真实使用中，目标项目已经存在与当前操作匹配的 active Project Skill，但 Agent 的初始处理顺序是：

```text
收到项目操作请求
-> 只基于当前运行时 / 全局 Skill inventory 判断能力
-> 错误声称没有相关专用 Skill
-> 进入通用 Operational Support 并准备执行环境动作
-> 人类提醒检查项目 Skill
-> 才读取 .agent-loop/skills/INDEX.md 并找到正确 Skill
```

该失败不是 Project Skill 缺失，也不是 Execution Gate 缺失，而是发现时机和 fallback 优先级没有形成不可绕过的跨文件 contract。

### 1.3 根因

现有规则允许 Agent 合理化以下错误路径：

- “Project Entry 时检查过，当前消息不需要再匹配 INDEX。”
- “原生 Skill inventory 没显示，所以项目没有相关 Skill。”
- “先进入通用 Operational Support，之后再看是否有更具体流程。”
- “on-demand 表示等人类明确点名 Skill 后才读取。”
- “只要最终找到 Project Skill，前面启动通用副作用不算问题。”

当前 focused test 主要验证 Project Skill、INDEX、状态和 Execution Gate 等关键词跨 surface 存在，没有直接证明“generic fallback 前必须完成项目 Skill 发现判断”。

## 2. 目标

本次修复必须做到：

1. 在可靠项目上下文中，新的可执行意图进入通用 helper、Operational Support 或内置 fallback 前，先运行 Project Skill Discovery Guard。
2. 将运行时 / 全局 Skill inventory 与项目 `.agent-loop/skills/INDEX.md` 明确视为两个不同发现来源。
3. Agent 不得在未检查项目 INDEX 的情况下声称“没有相关 Skill”“项目没有专用 Skill”或等价结论。
4. 只扫描 INDEX metadata；只有匹配候选才验证 manifest 并加载正文，避免全量加载所有 Project Skill。
5. 发现有效匹配后，先使用项目 Skill 约束本次方法，再保持现有 Execution Gate。
6. INDEX、目标路径或 manifest 不可靠时，按 project-skill drift fail closed，不得降级为“没有 Skill”并继续通用执行。
7. 普通 chat 不因本守卫产生无意义扫描或写入。
8. 上下文压缩、长会话不确定、controller re-entry 和阶段边界恢复后重新建立可靠的项目 Skill 发现状态。
9. runtime、design、project-skill reference、stage guidance、root guidance、human docs、scenarios 和 tests 对该不变量保持一致。

## 3. 非目标

本次不做：

- 不新增 canonical stage 或 message intent；
- 不新增 `.agent-loop/skills/` 之外的 Skill artifact 或 discovery cache；
- 不在 Agent Loop 源码仓库创建目标项目 `.agent-loop/`；
- 不把 Project Skill 安装、复制、软链接或同步到 `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.kimi/skills/`；
- 不让 Project Skill 变成运行时原生 Skill chip 的必要条件；
- 不在每条普通聊天消息中读取全部 Project Skill；
- 不预加载全部 `SKILL.md`、references 或 scripts；
- 不因发现或加载 Project Skill 自动执行命令、工具、文件写入或外部动作；
- 不减少、合并或绕过现有 Execution Gate 及其他风险门禁；
- 不改变 `proposed | active | disabled | deprecated` 生命周期；
- 不改变 `bootstrap | on-demand` 加载策略；
- 不新增 executable YAML / JSON schema、数据库、守护进程或定时扫描；
- 不修改 Skill 版本号；
- 不自动 commit、push、tag、PR、merge、release、publish 或同步已安装 Skill。

## 4. 核心概念

### 4.1 Project Skill Discovery Guard

`Project Skill Discovery Guard` 是 Agent Loop controller 内部的只读路由检查。它在可靠 memory root 已确定、Message Intent 已可判断之后执行，并且必须早于所选 stage 的通用方法或副作用。

它回答三个问题：

1. 当前项目是否存在 Project Skill INDEX；
2. 是否有与当前可执行意图 / stage / task context 匹配的 active Project Skill；
3. 匹配 Skill 的精确 INDEX row、路径和 manifest 是否仍可信。

它不回答“是否允许执行”。执行权限仍由 Execution Gate 和其他适用 Human Gates 决定。

### 4.2 Actionable Intent

本 proposal 中的 actionable intent 指可能进入工作流方法、命令、工具、文件修改、环境访问、外部系统访问或其他副作用的最新人类意图。

至少包括：

- `operational-support`；
- `feature-request`；
- `feature-follow-up`；
- `project-skill-management` 之外、可能由已有 Project Skill 辅助的 stage action；
- 人类明确询问、点名或要求使用某个项目能力；
- Agent 准备使用 generic helper 或 Agent Loop built-in fallback 的可执行场景。

普通解释、规则问答和无执行意图的 chat 不需要逐消息运行完整匹配。

### 4.3 Negative Discovery Claim

以下表述属于 negative discovery claim：

- “没有相关 Skill”；
- “项目没有专用 Skill”；
- “只能使用通用流程”；
- “当前没有可复用的项目能力”；
- 任何以 Skill 不存在为理由直接进入 fallback 的等价判断。

Agent 只有在检查过当前项目 INDEX 后才能做出该判断。若 INDEX 缺失、没有 active 匹配、或匹配项发生 drift，必须分别报告，不能混成同一个“没有 Skill”。

## 5. 路由与优先级

### 5.1 守卫位置

守卫不改变现有 Routing Axes 和 canonical stage order。它位于可靠 memory routing 与具体 stage action 之间：

```text
Bootstrap Agent Loop controller
-> locate memory root
-> Remote Discovery / Memory Recovery if required
-> classify latest Message Intent and current stage
-> Project Skill Discovery Guard when applicable
-> resolve stage method
-> Execution Gate and other Human Gates
-> stage action
```

如果 Memory Health 为 `stale | outside-loop`，仍先执行现有 Memory Recovery；守卫不得依赖不可靠的 INDEX claim。

### 5.2 方法优先级

保持现有控制关系：

```text
Agent Loop controller and Human Gates
-> valid active project-local skill match
-> runtime/global helper skill where applicable
-> Agent Loop built-in or generic Operational Support fallback
```

说明：

- 人类明确点名一个能力时，该请求用于选择候选，但不改变控制优先级；Agent 仍需确认名称的 owner 和实际路径，同名冲突不得静默选择。
- Project Skill 不能替代 mandatory stage helper resolution；两者同时适用时，由 Agent Loop controller 保持 stage contract、artifact ownership 和 Human Gates。
- runtime/global helper inventory 不包含 Project Skill，不能据此证明项目 Skill 不存在。
- fallback 只有在 Guard 得出 `index-absent | no-active-match` 后才可继续。
- `project-skill-drift` 不是 fallback 许可，而是 Recovery / Project Skill Creation / Update 的停止条件。

### 5.3 发现结果

Guard 的响应级结果限定为：

```text
matched-active
index-absent
no-active-match
project-skill-drift
```

这些是本次只读检查结果，不是持久 lifecycle status，不新增 artifact 字段。

| 结果 | 后续行为 |
|---|---|
| `matched-active` | 验证精确 row、路径和 manifest；加载匹配 Skill；准备 Execution Gate |
| `index-absent` | 可以继续所选 stage 的通用方法，但不得声称运行时 inventory 已代表项目检查 |
| `no-active-match` | 可以继续通用方法；`proposed/disabled/deprecated` 不进入正常路由 |
| `project-skill-drift` | fail closed，报告证据并推荐 Recovery 或 Project Skill Creation / Update |

## 6. 渐进读取与运行成本

该守卫必须保持轻量：

1. Project Entry、Resume、Re-Adopt、context recovery 和 controller re-entry 读取 INDEX metadata。
2. 新的 actionable intent 只匹配 INDEX 中的 `active` rows、Load Policy、Triggers 和 Scope。
3. 只有候选匹配后才读取目标 `SKILL.md`、validation manifest 和本次需要的 references/scripts metadata。
4. 不匹配时不得为“保险”读取所有技能正文。
5. 同一未压缩上下文、同一连续 stage、INDEX 未变化时，可以复用已验证 metadata；不得在一个命令序列的每一步重复扫描。
6. 出现上下文压缩、长会话不确定、controller re-entry、stage boundary uncertainty、INDEX 变化或 manifest 变化时，重新读取并验证。
7. 不创建持久 discovery cache；INDEX 仍是唯一发现索引。

因此日常成本是一次小型 metadata 匹配，而不是全项目 Skill 全量加载。

## 7. Execution Gate 保持不变

Project Skill Discovery Guard 只允许发现和只读加载，不授权调用。

匹配成功后，Agent 必须展示现有 Execution Gate 摘要：

- Skill 名称、项目相对路径、`active` 状态和 manifest 验证结果；
- 命中的 trigger 与当前请求；
- 本次计划动作、环境、对象和范围；
- 外部影响、风险、重试上限、停止条件、恢复和验证；
- 授权仅限本次 invocation。

在 Execution Gate 满足前，不得：

- 执行 Skill scripts；
- 运行其建议的命令；
- 创建临时环境资源；
- 修改文件；
- 请求外部系统产生副作用；
- 以“只是先准备一下”为理由提前执行通用 Operational Support 动作。

若人类的当前消息已经明确点名 Skill 和完整具体范围，仍按现有规则先展示摘要；只有没有新增未披露动作、影响、环境或边界时，该消息才可满足本次 Gate。

## 8. Fallback 与失败处理

### 8.1 INDEX 缺失

当可靠 memory root 下没有 `.agent-loop/skills/INDEX.md` 时，记录 `index-absent`，继续当前 stage 的通用方法。不得因此创建空 `skills/` 或主动创建 Project Skill。

### 8.2 无 active 匹配

当 INDEX 存在但没有 active row 匹配时，记录 `no-active-match`。Agent 可以使用 runtime/global helper 或内置 fallback，不加载 `proposed | disabled | deprecated` 技能正文。

### 8.3 Drift

以下情况为 `project-skill-drift`：

- INDEX target 缺失；
- INDEX active claim 无有效 validation evidence；
- 精确 INDEX row 与 manifest 不一致；
- 当前 instruction-bearing / executable file 与 manifest 不一致；
- 一个名称解析到多个不一致 owner；
- Skill path 逃逸项目边界或包含未确认外部 symlink。

发生 drift 时，Agent 必须：

1. 停止依赖该 Skill；
2. 不进入可能产生相同副作用的通用 fallback；
3. 报告 INDEX row、路径和验证冲突证据；
4. 推荐 exactly one Recovery 或 Project Skill Creation / Update 动作；
5. 等待适用 Human Gate。

### 8.4 证据位置

Guard 结果默认只需体现在当前响应中，不新增日志 artifact。若当前 stage 已有合法 evidence owner，可将关键 drift 或 gate evidence 写入该 artifact，但不得为了记录 discovery 单独创建 Feature、Requirement 或目录。

## 9. Root Guidance 边界

`templates/root-AGENTS.md` 只增加简短启动提醒，不承载完整 Project Skill 规则。建议语义为：

> 在声称没有相关项目 Skill 或进入通用执行 fallback 前，先检查 `.agent-loop/skills/INDEX.md`；匹配 active Skill 时仍须经过本次 Execution Gate。

完整时机、优先级、drift 和 fallback contract 继续由 `references/runtime.md`、`references/design.md` 和 `references/project-skills.md` 拥有。

## 10. 实施影响面

该修复属于 routing precedence、controller guard 和 root guidance 的 coordinated workflow change。预计同步检查和修改：

- `SKILL.md`：在 Required Runtime Behavior 和 Project Skill defaults 中加入 discovery-before-fallback guard；
- `references/runtime.md`：在 Inspection Order、intent/stage routing、Operational Support fallback 和 active Project Skill 规则中固化守卫；
- `references/design.md`：增加 Project Skill Discovery Guard 核心不变量和优先级；
- `references/project-skills.md`：增加完整 guard、negative claim、drift 和 fallback contract；
- `references/stage-guides.md`：Code-Guided Operational Support 等适用 stage 在第一个 action 前执行守卫；
- `references/workflow-checklists.md`：增加发现结果、匹配证据和 gate 检查；
- `references/project-guidance.md`：同步 root guidance 生成与刷新规则；
- `templates/root-AGENTS.md`：只增加一句简短路由提醒并刷新 managed block revision，保持 v1.4.0；
- `references/validation-scenarios.md`：增加真实 loophole 的压力场景；
- `README.md`、`Usage.md`：澄清 Project Skill 不一定显示为运行时原生 Skill，但由 Agent Loop INDEX 发现；
- `CHANGELOG.md`：记录 v1.4.0 开发线的路由修复；
- `tests/validate-project-local-skills.sh` 及必要的新 focused contract：证明 guard、优先级、drift 和 Execution Gate 跨 surface 一致；
- `docs/reports/`：保存 RED baseline 和中文 full-validation report。

实现阶段必须先检查当前工作区 dirty state，只修改本 proposal 授权的 surface，并保留所有无关修改。

## 11. TDD 与验证设计

### 11.1 RED Baseline

实现前新增 focused contract，并确认它在当前 runtime 上失败。RED 必须证明以下实际缺口，而不是只搜索 `Project Skill` 关键词：

```text
given reliable project memory
and an active on-demand Project Skill whose INDEX trigger matches the request
when the Agent is about to use generic Operational Support
then current rules do not yet require a successful Project Skill discovery decision before fallback
```

RED 报告保存到：

```text
docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-red-baseline-2026-07-16.md
```

报告记录实际命令、失败断言、现有规则为什么允许错误路径，以及工作区基线。

### 11.2 GREEN Contract

GREEN 至少验证：

1. `matched-active` 早于 generic fallback，并停在 Execution Gate；
2. `index-absent` 可以进入通用方法，但不产生错误的 inventory 等价判断；
3. `no-active-match` 不加载全部 Skill 正文；
4. `proposed | disabled | deprecated` 不进入正常匹配；
5. path / row / manifest drift fail closed；
6. context recovery 和 controller re-entry 重新建立 discovery state；
7. root guidance 只提供简短路由，不复制完整规则；
8. runtime、design、project-skills、stage guides、checklists 和 scenarios 使用一致的优先级；
9. Execution Gate 和其他 Human Gates 未被削弱；
10. 源码仓库未创建目标项目 `.agent-loop/skills/`。

Focused contract 应检查规则结构、路由先后关系和失败分支，不得只检查零散关键词存在。

### 11.3 压力场景

至少增加以下场景：

1. **Active On-Demand Match Before Operational Fallback**：请求命中 active Skill；Agent 先加载 Skill，再停在 Execution Gate，不能先执行通用动作。
2. **Runtime Inventory Is Not Project Skill Inventory**：运行时原生 Skill 列表无匹配，但项目 INDEX 有匹配；不得声称无 Skill。
3. **Index Absent Allows Generic Method**：项目没有 INDEX；Agent 可以继续通用方法，但不能创建空目录。
4. **No Active Match Avoids Full Body Scan**：INDEX 有多个 Skill 但无 active trigger 匹配；只检查 metadata。
5. **Inactive Skill Cannot Route**：proposed、disabled、deprecated 即使 trigger 匹配也不能进入正常调用。
6. **Manifest Drift Blocks Fallback**：候选 Skill 路径或 manifest 不一致；报告 drift 并停止，不能通过通用方法绕开。
7. **Execution Gate Still Blocks Side Effects**：Skill 成功发现但未获本次授权；不能运行命令、创建资源或访问外部系统产生副作用。
8. **Context Re-entry Rechecks Discovery**：上下文压缩或 controller re-entry 后不依赖旧记忆直接执行。
9. **Same-Name Ownership Is Explicit**：runtime/global 与 project-local Skill 同名；报告 owner/path，不能静默选取。
10. **Chat Remains Lightweight**：普通规则问答不触发全量 Skill 正文读取或 artifact 写入。

### 11.4 Focused Validation

实现后至少运行：

- 新的 Project Skill Discovery Guard focused contract；
- 现有 Project-Local Skills validation；
- Operational Support validation；
- mandatory helper routing validation；
- skill re-entry / controller bootstrap validation；
- root guidance checker、refresh 和 contract tests；
- Human Gate、validation scenarios 和 human docs 相关测试。

实际测试文件名和数量必须从实现时的 `tests/*.sh` 重新统计，不得沿用历史报告。

### 11.5 Full Validation

该变更触及 routing precedence、controller fallback、root Stage Map / guidance 和跨文件 workflow invariant，因此 GREEN 后必须按 `docs/maintenance/full-validation-method.md` 执行完整语义审计和全量回归，包括：

- 全部 `tests/*.sh`；
- SKILL.md YAML；
- Markdown fence；
- YAML / JSON / Shell / Ruby 等仓库现有机械检查；
- `git diff --check`；
- 工作区 hygiene 与 diff review；
- 中文 full-validation report。

建议报告路径：

```text
docs/reports/agent-loop-v1.4.0-project-skill-discovery-guard-full-validation-2026-07-16.md
```

## 12. 验收标准

1. 新的 actionable intent 在 generic helper、Operational Support 或 built-in fallback 前检查项目 Skill INDEX。
2. Agent 不再将 runtime/global Skill inventory 等同于 Project Skill inventory。
3. 未检查项目 INDEX 时，Agent 不得声称“没有相关项目 Skill”或等价结论。
4. 匹配 active Skill 时，精确 INDEX row、路径和 manifest 在加载前得到验证。
5. 只有匹配 Skill 正文被加载；不因守卫全量加载所有 Project Skill。
6. `index-absent | no-active-match` 才允许 generic fallback。
7. `project-skill-drift` fail closed，不能借通用 Operational Support 绕过。
8. 每次实际调用仍经过现有 Execution Gate；发现不等于授权。
9. 普通 chat 保持轻量且不产生 artifact。
10. 不新增 canonical stage、message intent、持久状态、cache artifact 或 executable schema。
11. root AGENTS template 只保留简短路由提醒，完整规则留在 runtime/design/reference。
12. focused RED/GREEN、受影响测试、全部 `tests/*.sh`、语义审计和机械检查通过。
13. 中文报告记录实际命令、实际测试数量、RED/GREEN 证据和剩余风险。
14. Skill 版本保持 v1.4.0；未获单独授权时不 commit、push、tag、PR、merge、release、publish 或同步已安装 Skill。

## 13. 停止条件

实施中出现以下情况必须停止并交还人类：

- 需要改变 Project Skill lifecycle、Load Policy 或 Execution Gate；
- 需要新增 canonical stage、message intent 或第二套 controller；
- 需要把 Project Skill 安装到全局 / runtime-native Skill 目录；
- 需要新增 discovery cache、数据库、守护进程、第三方依赖或 executable schema；
- 需要让 generic Operational Support 在 drift 时继续执行；
- 需要扩大 root AGENTS template 为完整 Project Skill 规范；
- 需要修改 Skill 版本号；
- 发现无关 dirty work 与授权 surface 冲突；
- focused 或 full validation 无法可靠通过；
- 需要 commit、push、tag、PR、merge、release、publish 或同步安装副本。

## 14. Proposal Boundary

本文件是现有 Project-Local Skills 能力的 corrective design input，不是当前 runtime authority。

在人类完成 Proposal Review、Implementation Plan Review、TDD 实现和 full validation Human Review 之前：

- 当前 `references/runtime.md` 和 `references/design.md` 仍是发布运行权威；
- 不得声称 Project Skill Discovery Guard 已经生效；
- 不在源码仓库创建目标项目 `.agent-loop/skills/`；
- 不修改 Skill 版本号；
- 不自动提交、推送、发布或同步已安装 Skill。

## 15. 推荐实施顺序

```text
Human approves this Proposal
-> write Implementation Plan
-> Human reviews the plan
-> add focused contract and capture RED
-> coordinated runtime/design/reference/template/docs implementation
-> focused GREEN and pressure scenarios
-> full validation and Chinese report
-> Human Review Summary
-> wait for separate submit authorization
```

该方案保持“一次性维护改动中等、下游运行成本轻量”：用一个明确守卫关闭真实路由漏洞，同时继续依赖 INDEX 渐进发现和现有 Execution Gate，不把 Project Skill 变成全局安装或自动执行系统。
