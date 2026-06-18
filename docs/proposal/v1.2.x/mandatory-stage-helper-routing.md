# Proposal: Mandatory Stage Helper Routing

状态：已实施，待提交

目标版本：v1.2.x

创建时间：2026-06-18

默认语言：中文

## 背景

`agent-loop` 已经具备 Stage Helper Capability Scan 和 External Skill Adapter，也明确说明在 Superpowers 可用时优先借用对应方法。

但当前规则仍然偏软：

- `prefer` / `use as quality bar` 容易被 Agent 理解为可选建议；
- helper capability scan 只有自然语言流程，没有阶段完成断言；
- helper 不可用时可以 fallback，但没有要求记录“检查过哪些名称、为什么不可用”；
- `superpowers:writing-plans` 与 `writing-plans` 等名称可能因运行时不同而产生别名歧义；
- Agent 即使跳过 helper，也可能直接使用 agent-loop fallback 完成阶段，错误不会显性暴露。

因此，需要把关键阶段的 helper 调用从“优先建议”升级为“可检查的阶段协议”。

## 目标

对以下七个 Superpowers helper 建立强制路由：

1. `brainstorming`
2. `writing-plans`
3. `test-driven-development`
4. `systematic-debugging`
5. `verification-before-completion`
6. `requesting-code-review`
7. `subagent-driven-development`

达到这些结果：

- 进入对应阶段前必须解析并加载 helper；
- 支持 canonical name 和非前缀 alias；
- 只有 helper 确实不可用或加载失败时才能 fallback；
- 每次解析和 fallback 都有 artifact 留痕；
- agent-loop 始终保留 controller 权限；
- Superpowers 默认输出路径不能覆盖 agent-loop 目录规范；
- 未完成 helper resolution 的阶段不能宣称完成。

## 非目标

本 proposal 不做以下事情：

- 不把整个 agent-loop 工作流交给 Superpowers；
- 不改变 `.agent-loop/` 的目录结构；
- 不默认创建 `docs/superpowers/`；
- 不取消任何 agent-loop 人类门禁；
- 不允许 helper 直接修改 task done、feature close、submit 或 project memory 状态；
- 不把 Feature Auto-Loop 或 Task Auto-Run 解释为 subagent 授权；
- 不要求未安装 Superpowers 的运行时停止工作。

## Controller 权限

`agent-loop` 继续负责：

- 判断当前 stage 和下一 stage；
- 管理 Strict Mode、Feature Auto-Loop、Task Auto-Run；
- 管理人类确认门禁；
- 管理 task 状态和 Task Done Gate；
- 管理 feature close、pause、submit、commit、PR、merge、release；
- 管理 drift、project memory 和 Delivery Contract；
- 决定 helper 输出写入哪个 agent-loop artifact。

Superpowers helper 只负责阶段内部的方法质量。

```text
agent-loop decides when and where.
Superpowers improves how.
agent-loop records and governs the result.
```

## 优先级

发生规则冲突时使用以下优先级：

```text
Human instructions
> agent-loop lifecycle, gates, state, and artifact ownership
> loaded Superpowers method rules
> agent-loop fallback guidance
```

## 强制 Stage Helper 协议

进入 mandatory helper-backed stage 前，必须执行：

1. 根据当前 stage 确定 required helper。
2. 按顺序检查 canonical name 和 alias；canonical 不存在或加载失败时仍须继续检查 alias。
3. 找到后，在任何 stage action 前加载完整 `SKILL.md`。
4. 记录 requested helper、resolved helper、resolution status 和 artifact overrides。
5. 使用 helper 的方法完成阶段内部工作。
6. 仍由 agent-loop 执行 human gate、状态更新和下一阶段选择。
7. 阶段结束前验证 Stage Helper Resolution 记录存在。

初始 Resolution 必须在第一个 stage action 前记录；阶段结束时再补齐 method、fallback 和 artifact evidence。不存在已确认 feature workspace 时，不得为了留痕自行创建 feature，应先在响应中给出 `response-local-pending` 记录，并在下一次经人类批准的 artifact write 中回填。

如果 helper 无法加载：

1. 记录检查过的候选名称；
2. 将状态记录为 `unavailable` 或 `load-failed`；
3. 记录 fallback 文件和方法；
4. 才允许使用 agent-loop fallback。

禁止以下行为：

- 未检查 helper 就直接 fallback；
- helper 已成功加载后仍绕开它使用 fallback；
- 只凭记忆使用 helper，而不加载当前完整 `SKILL.md`；
- 不记录 resolution 就结束阶段；
- 因 helper 自带路径或流程而跳过 agent-loop gate。

## 名称解析

按 canonical name 优先、alias 次之解析：

| Stage | Canonical name | Alias |
|---|---|---|
| Brainstorm / Clarify | `superpowers:brainstorming` | `brainstorming` |
| Plan Gate / Plan If Needed | `superpowers:writing-plans` | `writing-plans` |
| Execute Task / Story | `superpowers:test-driven-development` | `test-driven-development` |
| Diagnose Failure | `superpowers:systematic-debugging` | `systematic-debugging` |
| Verify | `superpowers:verification-before-completion` | `verification-before-completion` |
| Review / Feature Close Review | `superpowers:requesting-code-review` | `requesting-code-review` |
| Subagent Execution If Approved | `superpowers:subagent-driven-development` | `subagent-driven-development` |

如果运行时提供其他命名空间下的等价 helper，Agent 可以解析它，但必须在 Resolution 记录中写明实际名称和判断依据。

## 各阶段前置规则

### Brainstorm / Clarify

在产品或行为设计前加载 `brainstorming`。

借用：

- 上下文探索；
- 一次一个高影响问题；
- 2-3 个方案比较；
- 设计确认。

覆盖：

- 输出写到 `product.md`、`spec.md`、`notes.md`；
- 不写 `docs/superpowers/specs/`；
- 不自动进入 writing-plans，仍由 agent-loop 推荐下一阶段。

### Plan Gate / Plan If Needed

在写入或批准 `plan.md` 前加载 `writing-plans`。

借用：

- construction-grade plan；
- 精确文件路径和代码上下文；
- 测试代码；
- RED/GREEN 命令和预期输出；
- no-placeholder 和 self-review。

覆盖：

- 输出写到 feature 的 `plan.md` 或 `plans/*`；
- 不写 `docs/superpowers/plans/`；
- 执行方式由 agent-loop gate 决定。

### Execute Task / Story

行为、测试或实现变化开始前加载 `test-driven-development`。

借用：

- RED；
- verify RED；
- GREEN；
- verify GREEN；
- refactor。

覆盖：

- 证据写入 `notes.md`；
- task 状态仍由 Task Done Gate 管理；
- 无法使用 TDD 时必须停止、解释并进入 Human Gate。

### Diagnose Failure

发现测试失败、构建失败、E2E 失败或异常行为后，在提出修复方案前加载 `systematic-debugging`。

借用：

- 稳定复现；
- 根因追踪；
- 单一假设；
- 最小验证；
- 回归测试。

覆盖：

- 根因、证据、修复决定和复验写入 `notes.md`；
- 修复仍返回 agent-loop 的 Execute / Verify / Review 流程。

### Verify

任何 `passed`、`fixed`、`complete`、`ready` 声明前加载 `verification-before-completion`。

借用：

- 识别能证明结论的命令；
- 新鲜完整执行；
- 阅读完整结果；
- 证据先于声明。

覆盖：

- 证据写入 `notes.md`；
- completion、close 和 submit 仍由 agent-loop gate 决定。

### Review / Feature Close Review

task 从 review 向 done 推进、Submit / Integrate 前、Feature Close Review 前加载 `requesting-code-review`。

借用：

- 结构化代码审查；
- 需求覆盖检查；
- 风险和缺陷识别。

覆盖：

- findings 写入 `notes.md`；
- helper review 通过不能直接标记 task done；
- Task Done Gate 和 Feature Close Review 仍是最终规则。

### Subagent Execution If Approved

只有人类明确批准 subagent dispatch 后，才加载 `subagent-driven-development` 并派发。

借用：

- 每个 task 使用明确 brief；
- 独立上下文；
- 主 agent 分阶段 review；
- bounded execution。

覆盖：

- Feature Auto-Loop 和 Task Auto-Run 不等于 subagent 授权；
- brief/return 写入 `handoffs/*`；
- dispatch 前授权状态必须是 `active`；dispatch group 返回或停止后标记 `consumed`，不得复用 consumed/revoked/expired 授权；
- 主 agent 负责 synthesis、review、merge 和状态更新；
- subagent 不能 close、submit、更新 project memory、接受 Delivery Contract、批准 breaking change 或标记 task done。

## 路径覆盖规则

agent-loop artifact paths 始终覆盖 external skill default paths。

| External output | Agent-loop destination |
|---|---|
| brainstormed design/spec | `.agent-loop/features/<feature>/product.md` / `spec.md` |
| implementation plan | `.agent-loop/features/<feature>/plan.md` / `plans/*` |
| TDD evidence | `.agent-loop/features/<feature>/notes.md` |
| debugging evidence | `.agent-loop/features/<feature>/notes.md` |
| verification evidence | `.agent-loop/features/<feature>/notes.md` |
| review findings | `.agent-loop/features/<feature>/notes.md` |
| subagent brief/return | `.agent-loop/features/<feature>/handoffs/*` |

不得默认创建：

```text
docs/superpowers/specs/
docs/superpowers/plans/
```

只有人类明确请求 native Superpowers output，并在 Agent 解释路径覆盖后再次确认，才允许创建这些目录。

## Resolution 留痕

每次 mandatory helper stage 在 feature `notes.md` 中记录：

```markdown
## Stage Helper Resolutions

### YYYY-MM-DD — <Stage>

- Requested Helper: writing-plans
- Invocation Scope: task
- Execution Unit: T003
- Resolved At:
- First Stage Action At:
- Candidate Results:
  - superpowers:writing-plans: loaded — <evidence>
  - writing-plans: not-needed-after-success
- Resolved Helper: superpowers:writing-plans | none
- Resolution Status: loaded | unavailable | load-failed
- Fallback Used: yes | no
- Fallback Source:
- Method Used:
- Agent-loop Overrides:
  - Artifact Path:
  - Human Gate:
  - State Ownership:
- Evidence:
- Persistence: notes.md | response-local-pending
```

成功加载时：

- `Resolution Status: loaded`
- `Fallback Used: no`
- `Resolved Helper` 不能是 `none`，并且必须有完整加载与 method-used evidence

不可用或加载失败时：

- 状态只能是 `unavailable` 或 `load-failed`；
- 必须列出候选名称；
- `Fallback Used: yes` 时必须写明 fallback source。
- `unavailable` 要求所有候选均不存在；`load-failed` 要求所有可发现候选都有加载错误，且 alias 也已尝试。

## 阶段完成断言

mandatory helper-backed stage 结束前必须满足：

- Stage Helper Resolution 记录存在；
- status 是 `loaded`、`unavailable` 或 `load-failed`；
- `loaded` 时已经使用 helper 方法且没有 fallback；
- fallback 时 status 必须是 `unavailable` 或 `load-failed`；
- artifact path、human gate 和 state ownership 仍归 agent-loop；
- 相关证据已写入 owning artifact。

缺少任何一项时，该阶段不能宣称完成，也不能进入下一阶段。

## Fallback

Superpowers 未安装或 helper 无法加载时，agent-loop 仍能自主运行。

| Stage | Fallback |
|---|---|
| Brainstorm / Clarify | `stage-guides.md` clarification rules |
| Plan Gate / Plan | `implementation-planning.md` + `templates/plan.md` |
| Execute Task / Story | `stage-guides.md` RED/GREEN flow |
| Diagnose Failure | reproduce → isolate → hypothesize → verify |
| Verify | fresh proof command and evidence record |
| Review | agent-loop Spec Review / Standards Review |
| Subagent Execution | 单 Agent 执行，或在已批准前提下使用运行时原生 bounded dispatch |

fallback 是兼容路径，不是跳过 helper resolution 的捷径。

## 验证场景

实施时至少覆盖：

1. canonical Superpowers helper 已安装，Agent 完整加载并记录 `loaded`；
2. 只有非前缀 alias，Agent 仍能解析并加载；
3. 两个名称都不存在，Agent 记录 `unavailable` 后 fallback；
4. helper 可发现但读取失败，Agent 记录 `load-failed` 后 fallback；
5. helper 已加载但 Agent 仍使用 fallback，验证应拒绝；
6. writing-plans 试图写入 `docs/superpowers/plans/`，Agent 改写到 feature `plan.md`；
7. brainstorming 试图自动进入 writing-plans，Agent 停在 agent-loop gate；
8. review helper 通过但 Task Done Gate 未完成，task 保持 `review`；
9. Feature Auto-Loop 已启用但未批准 subagent，Agent 不得 dispatch；
10. subagent 已批准，brief/return 写入 `handoffs/*`，主 agent 保持最终控制。
11. 尚未确认 feature workspace 时，helper 留痕使用 response-local pending record，不得越权建文件；
12. 旧 subagent 授权不能复用于新的 task、lane 或扩大后的文件边界。

## 预计修改范围

实施阶段预计修改：

- `SKILL.md`
- `references/skill-routing.md`
- `references/external-skill-adapters.md`
- `references/stage-guides.md`
- `templates/notes.md`
- `references/validation-scenarios.md`
- `README.md`
- `Usage.md`
- `CHANGELOG.md`
- helper routing contract test

不修改 skill 版本号，除非人类另行批准版本升级。

## 接受标准

- 七个阶段都有明确 required helper；
- canonical name 与 alias 都有解析规则；
- helper 必须在 stage action 前完整加载；
- fallback 只允许 `unavailable` 或 `load-failed`；
- helper resolution 有统一留痕；
- Resolution 在首个 stage action 前初始化，且矛盾状态会阻止阶段执行或完成；
- agent-loop controller、gate、status、memory 和 submit 权限不变；
- `.agent-loop/` 目录规范不变；
- `docs/superpowers/*` 不会被默认创建；
- subagent 仍需独立人类授权；
- 静态契约测试和行为验证场景覆盖上述规则。
