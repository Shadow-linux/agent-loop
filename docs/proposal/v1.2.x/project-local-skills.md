# Proposal: Project-Local Skills

状态：设计确认，待实施
目标版本：未指定；实现期间保持当前技能版本不变，版本升级需人类另行确认
适用对象：使用 Agent Loop 的下游目标项目

## 1. 背景

Agent Loop 当前可以发现运行时已经暴露的 skills、plugins 和 helpers，但下游项目缺少一个由 Agent Loop 管理的项目私有技能库。复杂、顺序敏感或容易遗忘的项目流程即使成功执行，通常也只留在聊天记录、`notes.md` 或根指导中，后续 Agent 仍需重新推导。

部分 Agent 会自动扫描 `.agents/skills/`，但这不是 Agent Loop 可以跨运行时依赖的统一能力。Agent Loop 需要提供自己的项目级常驻技能入口，同时保持渐进加载、Human Gate 和现有控制器优先级。

## 2. 目标

在下游目标项目中支持：

```text
.agent-loop/
  skills/
    INDEX.md
    <skill-name>/
      SKILL.md
      agents/openai.yaml  optional
      references/         optional
      scripts/            optional
      assets/             optional
      templates/          optional
```

该能力需要做到：

1. 人类明确说“把这个流程/动作做成技能”时，进入 Project Skill Creation。
2. Agent 在复杂流程成功并验证后，可以主动提出 Project Skill Candidate。
3. 创建技能目录前必须经过 Human Gate。
4. 技能创建遵循 RED -> GREEN -> REFACTOR。
5. 优先使用 Superpowers `writing-skills`；本地 `skill-creator` 可作为脚手架和格式验证助手。
6. 外部 helper 的默认输出路径必须重定向到目标项目 `.agent-loop/skills/`。
7. 新技能在创建和验证期间为 `proposed`，全部验证通过后自动变成 `active`。
8. Project Entry、Resume 和上下文恢复能稳定发现项目技能，但不把所有技能正文永久塞入上下文。
9. 每次真正执行项目技能前都必须获得本次执行范围的人类确认；自动发现或加载不等于执行授权。

## 3. 非目标

第一版不做：

- 不在 Agent Loop 源码仓库根目录创建 `.agent-loop/skills/`。
- 不在每个下游项目初始化时创建空 `skills/` 目录。
- 不把项目技能默认复制、软链接或同步到 `.agents/skills/`、`.codex/skills/`、`.claude/skills/` 或 `.kimi/skills/`。
- 不自动安装项目技能到用户全局目录。
- 不让项目技能覆盖 Agent Loop Human Gates、状态机、工件路径、提交或关闭规则。
- 不因加载 `SKILL.md` 自动执行其 `scripts/`。
- 不因技能状态为 `active`、加载策略为 `bootstrap` 或当前启用了 auto mode 而自动执行技能。
- 不为项目技能增加未经 loader 支持的 `SKILL.md` frontmatter 字段。
- 不把一次性操作、普通项目约定或可由机械校验完全替代的规则强行做成技能。

## 4. 核心概念

### 4.1 Project Skill

Project Skill 是存放在目标项目 `.agent-loop/skills/<skill-name>/` 下、只服务该项目的可复用流程、模式或参考能力。

它不同于：

- 全局个人技能：跨项目安装在 Agent 专属技能目录。
- Agent Loop 分发包内 reference：定义 Agent Loop 自身运行规则。
- 根 `AGENTS.md`：保存项目级启动指导与稳定约束。
- `.agent-loop/project.md`：保存项目事实，不保存完整技能方法。

### 4.2 Project Skill Candidate

Agent 在一个复杂流程成功完成并取得验证证据后，可以提出候选，但不能直接创建技能文件。

候选摘要至少包含：

- 建议技能名称；
- 人类会使用的触发语句；
- 适用流程与不适用场景；
- 本次成功证据；
- 可复用步骤；
- 建议打包的 scripts、references、assets 或 templates；
- 建议加载策略；
- 敏感信息、环境依赖和清理要求；
- 创建后的验证方式。

### 4.3 常驻能力

“常驻”表示 Agent Loop 总能发现项目技能目录和索引，不表示所有 `SKILL.md` 正文在每次消息中全部加载。

```text
目录和 metadata 可发现
-> 根据 load policy 和 trigger 加载正文
-> 命中技能后展示本次执行范围
-> 人类确认后才执行流程或资源
```

## 5. 触发入口

### 5.1 人类显式触发

以下表达应进入 Project Skill Creation：

- “把这个流程做成技能。”
- “把刚才成功的操作沉淀成 skill。”
- “这个步骤以后经常用，做成项目常驻能力。”
- “更新项目里的某个 skill。”

显式触发授权 Agent 进入候选分析和设计，不自动授权创建目录、激活技能、提交或发布。

### 5.2 Agent 主动建议

同时满足以下信号时，Agent 可以在当前工作完成后提出候选：

- 流程已经成功执行；
- 有新鲜验证证据；
- 流程复杂、顺序敏感、容易遗漏或容易失败；
- 同类操作已经重复出现，或未来重复概率高；
- 能抽象成稳定触发条件和复用方法；
- 不包含无法安全抽象的临时凭据或个人秘密。

主动建议不能打断当前任务的 Verify、Review、Drift 或 Close Gate，也不能把当前任务“做完”自动等价为创建技能。

## 6. Human Gates

### Gate 1: Create Project Skill

在创建 `.agent-loop/skills/`、`INDEX.md` 或 `<skill-name>/` 前，Agent 必须展示 Project Skill Candidate 和预计文件树，并获得人类明确确认。对 `active` 技能进行实质性流程、触发条件、输出契约、危险操作、依赖或权限修改时，也复用同一个 Gate 1 展示更新范围。

如果 Candidate 计划使用压力测试 subagent，必须同时列出独立场景 lane、每个 Agent 的 brief/角色、允许读写边界、停止条件、主 Agent 审核责任和授权 `active -> consumed` 生命周期。人类确认包含这些字段的 Gate 1 时，可以同时满足这组技能创作压力测试的 subagent dispatch gate；验证记录写入技能 `validation.md`，不创建 feature 或 `handoffs/`。

允许回复示例：

```text
确认创建这个项目技能
修改候选设计
先不创建
只保留建议
```

Gate 1 通过后，Agent 可以连续完成 RED/GREEN/REFACTOR、结构验证和前向测试。全部验证通过后，Agent 先完成最终 `active` INDEX row，并为该精确 row、`SKILL.md` 和所有指令型/可执行资源记录 SHA-256 Validated Content Manifest，再自动将技能标记为 `active`，不请求第二次激活确认。

如果验证失败，技能保持 `proposed`，不得进入常驻或 on-demand 正常路由。如果实现过程中发现范围、危险操作、依赖、权限或输出契约超出 Gate 1 已确认内容，Agent 停止并用更新后的 Candidate 重新进入同一个 Gate 1。

普通错字或不改变行为的说明修正可以走窄范围更新，但仍需要验证；不新增单独的激活或 breaking-update Gate。

### Execution Gate: Run Project Skill

发现、读取 INDEX、加载 `SKILL.md` 和检查触发条件属于只读准备，不需要确认。Agent 一旦准备按项目技能推进流程、执行命令、调用工具、修改文件、访问外部系统或产生其他副作用，必须先获得人类对本次执行范围的确认。

执行摘要至少包含：

- 技能名称、路径和 `active` 状态；
- 本次命中的 trigger 和预期结果；
- 计划执行的主要步骤、命令、文件或外部动作；
- 风险、回滚和验证方式；
- 授权范围仅限本次 invocation。

如果人类已经明确说“使用 `<skill-name>` 执行 `<具体范围>`”，Agent 仍需先展示执行摘要；只有计划未增加任何未披露动作、影响、环境或边界时，这条消息才可满足 Execution Gate，且无需再问一次。生产、破坏性、凭据、付费、非幂等或外部写操作还必须明确环境/账号、资源、操作和重试上限、危险影响、停止条件、恢复和验证。仅提到技能、只说“继续”、自动命中 trigger、`bootstrap` 加载或 Feature Auto-Loop / Task Auto-Run 均不构成执行授权。

Invocation 从第一个超出发现/加载的技能动作开始，到结果报告、abort/pause、上下文丢失、manifest 变化或计划/范围实质变化时结束；重试只有在触发条件、次数上限和影响已预先确认时才属于同一次 invocation。一次确认不得自动延续到未来会话、下一次 invocation、另一个任务或另一个项目技能。

Execution Gate 与生产、凭据、外部服务、破坏性操作、submit/release 等门禁可以合并为一次确认，但前提是摘要显式列出全部适用事实；技能确认本身不会隐式满足其他门禁。

## 7. 工作流位置与意图

新增 Message Intent：`project-skill-management`。

它适用于人类明确要求创建、更新、禁用或弃用项目技能。默认下一阶段是 `Project Skill Creation / Update`，前提是 Project Entry 已完成且项目记忆可依赖。

该阶段：

- 不创建 requirement set；
- 不创建 feature workspace；
- 不把技能创建伪装成普通一次性编辑；
- 不因存在 paused feature 而阻塞；
- 当 active feature 尚有 Verify、Review、Drift、Memory Update 或 Close Gate 时，不抢占当前闭环。

Agent 主动发现候选时，当前 Message Intent 不会被静默改写。Agent 应先完成当前已授权阶段，在安全边界提出 Project Skill Candidate；候选建议本身不需要先加载创作 helper。人类确认包含完整范围的 Candidate 后，该回复可直接满足 Gate 1；下一轮进入 `project-skill-management`，先解析 helper 再创作，helper 导致实质范围变化时才重新 Gate 1。人类直接显式请求创建技能时，则先解析 helper、完善 Candidate，再展示 Gate 1。

`Project Skill Creation / Update` 应出现在 canonical stage 导航和 root Stage Map 中，并拥有独立 reference、entry/exit condition、Human Review Summary 和验证场景。

## 8. Helper Capability Scan

Project Skill Creation 是 helper-backed 能力。Agent Loop 保持控制器身份，外部 helper 只改进创建方法。

### 8.1 解析顺序

```text
writing-skills available?
  yes -> 用于 RED/GREEN/REFACTOR 和压力测试
skill-creator available?
  yes -> 用于脚手架、agents/openai.yaml 和格式验证
neither available?
  yes -> 使用 Agent Loop 内置模板和验证 fallback
```

`writing-skills` 与 `skill-creator` 不是互斥候选。两者同时存在时：

- `writing-skills` 控制技能创作纪律和压力测试；
- `skill-creator` 提供初始化、资源目录选择、metadata 生成和 `quick_validate.py`；
- Agent Loop 控制输出位置、Human Gates、状态和项目记忆。

如果两个 helper 的写作规则冲突，`writing-skills` 的 RED/GREEN/REFACTOR、触发型 description 和压力测试规则优先；`skill-creator` 不得借脚手架默认值覆盖这些规则。

### 8.2 候选名称

运行时应检查可用的 canonical name 和别名，包括：

- `writing-skills`
- `superpowers:writing-skills`
- `skill-creator`

解析结果记录在项目技能的验证记录或 `.agent-loop/skills/INDEX.md` 对应条目中。没有 feature workspace 时，不创建 feature `notes.md` 只为记录 helper。

### 8.3 路径覆盖

无论 helper 默认建议写入哪里，Agent Loop 都必须覆盖为：

```text
<target-project>/.agent-loop/skills/<skill-name>/
```

禁止默认写入：

```text
~/.agents/skills/
~/.codex/skills/
~/.claude/skills/
~/.kimi/skills/
docs/superpowers/
```

## 9. INDEX.md 模型

`.agent-loop/skills/INDEX.md` 是项目技能清单和生命周期索引，不复制技能正文。

建议字段：

| 字段 | 含义 |
|---|---|
| Skill | 技能名称及相对路径 |
| Status | `proposed | active | disabled | deprecated` |
| Load Policy | `bootstrap | on-demand` |
| Triggers | 简短触发词或场景 |
| Scope | 适用项目边界 |
| Helper Resolution | `writing-skills`、`skill-creator` 或 fallback |
| Evidence | RED/GREEN/REFACTOR 或结构验证证据位置 |
| Updated | 最近更新时间 |

完整技能正文、测试材料和复杂验证记录属于技能目录；INDEX 只保留导航和当前状态。`validation.md` 必须保存精确 INDEX row 的 SHA-256，使 `Status`、`Load Policy`、`Triggers`、`Scope` 或 `Evidence` 的越权修改也会让 active trust 失效。

## 10. 加载策略

### 10.1 Bootstrap

适用于每次 Agent Loop 进入项目都必须掌握的项目能力，例如特殊发布流程、授权运维入口或稳定的领域操作约束。

加载时机：

- Project Entry；
- Resume；
- Re-Adopt；
- 上下文压缩后的控制器重入；
- 长会话中工作流状态不确定时。

同一会话中已加载且精确 INDEX row、技能文件和资源均与 manifest 一致时，不需要在每条消息重复读取。

Bootstrap 只授予发现和加载能力，不授予执行能力。每次实际使用仍需通过 Execution Gate。

### 10.2 On-Demand

适用于只在特定任务或操作出现时需要的技能。Agent 在 Message Intent、Stage Helper Capability Scan 或任务上下文命中 `description` / INDEX triggers 后读取完整 `SKILL.md`。

### 10.3 状态限制

- `active`：可正常发现和加载。
- `proposed`：只用于当前创建与验证流程。
- `disabled`：保留历史文件但不得加载执行。
- `deprecated`：仅作为迁移或历史证据读取，不进入正常路由。

## 11. 优先级与冲突处理

```text
Agent Loop controller and Human Gates
-> active project-local skills
-> runtime/global helper skills
-> Agent Loop built-in fallback
```

项目技能不能覆盖：

- Agent Loop canonical stage order 和 routing precedence；
- Human Gate、Stop And Ask 或 auto-mode stop conditions；
- `.agent-loop/` 工件所有权；
- Task Done Gate、Feature Completion Check 或 Close Gate；
- Delivery Contract acceptance 和 breaking-change Gate；
- Submit、Commit、PR、Merge、Release、Publish 或 Tag 授权。

如果项目技能与控制器、根指导、人类要求或另一个 active 项目技能冲突，Agent 必须停止加载冲突行为，报告证据，并请求人类选择更新、禁用或弃用哪一条能力。

## 12. 安全规则

- 读取技能不等于执行脚本。
- 读取和匹配技能不等于获得 Execution Gate 授权。
- `scripts/` 中的命令仍需经过 Execution Gate、当前环境权限、风险检查和其他适用 Human Gate。
- 不把真实凭据、token、私钥、账号密码或不可公开的临时值写入技能。
- 将环境差异写成参数、前置检查或 references，不硬编码个人路径和机器状态。
- 不自动跟随指向项目外部的 symlink；外部路径必须单独确认。
- 创建前检查项目 INDEX 和运行时暴露的 installed-skill inventory；不无边界扫描 home。遇到同名时报告两个 owner，改用不同项目名或另行设计迁移，避免静默覆盖。
- 技能目录只包含执行该能力所需的文件，不添加 README、CHANGELOG 或无关过程记录。

## 13. Project Skill 流程

### 13.1 Creation / Update

```text
Explicit Human Request
-> Helper Capability Scan
-> Candidate Analysis
-> Gate 1: Create Project Skill
or Human-Accepted Proactive Candidate
-> Gate 1 already satisfied
-> Helper Capability Scan before authoring
-> RED baseline without the new skill
-> Scaffold proposed skill in .agent-loop/skills/
-> GREEN implementation
-> Forward-test with the skill
-> REFACTOR loopholes and re-test
-> Structure and path validation
-> finalize active INDEX row and SHA-256 manifest
-> all verification passes
-> INDEX status active automatically
-> Project memory / root guidance impact check
```

技能创建本身不自动授权 commit、push、global install 或外部发布。

### 13.2 Execution

```text
Message / Stage matches active project skill
-> discover INDEX metadata
-> load SKILL.md as needed
-> build invocation scope and risk summary
-> Execution Gate: human confirms this invocation
-> execute only the confirmed scope
-> verify result and report evidence
-> scope changes? stop and confirm again
```

技能成功执行一次不会产生永久授权，也不会让后续 invocation 跳过 Execution Gate。

## 14. RED/GREEN/REFACTOR 测试模型

### RED

在新运行规则写入前，用隔离场景验证当前 Agent 的自然行为。场景至少覆盖：

1. 人类要求“把刚才的复杂操作做成项目技能”，Agent 错写到全局技能目录或 `.agents/skills/`。
2. Agent 完成复杂流程后，直接创建技能而没有 Human Gate。
3. Agent 只检查 `skill-creator`，忽略已存在的 `writing-skills`。
4. Agent 把 helper 的默认路径当作最终路径，绕过 `.agent-loop/skills/`。
5. Agent 激活未经前向测试的 proposed 技能。
6. Agent 在普通 Project Entry 中加载 disabled/proposed 技能或自动执行 scripts。
7. Agent 因技能是 `active` / `bootstrap` 或处于 auto mode，未确认便执行项目技能。
8. Agent 把一次执行确认复用到后续 invocation、会话或扩大后的范围。

记录 Agent 的实际选择和合理化理由，作为 GREEN 最小规则的输入。

### GREEN

只增加足以关闭已观察失败的运行规则、模板和回归断言。复跑相同场景，要求 Agent：

- 识别 Project Skill Creation；
- 提交候选并停在 Gate 1；
- 解析正确 helper 组合；
- 保持路径覆盖；
- 验证全部通过后自动标记为 `active`；
- 验证失败时保持 `proposed`；
- 不执行未授权脚本；
- 不加载非 active 技能。
- 加载 active 技能后先展示 Execution Gate 摘要；人类消息已明确授权技能和完整具体范围且计划无未披露动作时，无需再次提问；
- 不复用历史执行授权，范围变化时重新确认。

### REFACTOR

捕获新合理化，例如“人类提过做成技能，所以不需要 Gate 1”“写到 `.agents/skills` 更容易自动发现”“流程已经成功，所以不需要 RED”“验证失败也可以先 active”“active 或 bootstrap 等于允许执行”“上次确认过，所以这次也能执行”。将每个漏洞写入规则和回归断言，并持续复测。

## 15. 模板

源码仓库预计新增：

```text
templates/project-skills/INDEX.md
templates/project-skills/SKILL.md
templates/project-skills/validation.md
```

这些模板只供下游 Agent 在 Gate 1 后复制或适配。模板本身不代表源码仓库拥有 `.agent-loop/skills/`。

## 16. 运行时与文档改动面

实现需要协调更新：

- `SKILL.md`：能力入口、加载规则和 artifact layout；
- `references/runtime.md`：意图识别、Project Entry/Resume 扫描和 Gate；
- `references/design.md`：Project Skill 核心模型与优先级；
- 新增 `references/project-skills.md`：Project Skill Creation / Update 的完整阶段规则；
- `references/project-guidance.md`：root guidance 中的发现和恢复规则；
- `references/skill-routing.md`：Project Skill Creation helper 解析；
- `references/external-skill-adapters.md`：`writing-skills` / `skill-creator` 路径与 Gate 覆盖；
- `references/stage-guides.md` 和 `references/workflow-checklists.md`：候选、创建、激活和更新流程；
- `templates/root-AGENTS.md`：下游 Agent 的 bootstrap 发现规则；
- `templates/project.md`：项目技能索引状态；
- `templates/project-skills/*`：下游技能模板；
- `README.md`、`Usage.md`、`CHANGELOG.md`：人类入口和版本记录；
- `references/validation-scenarios.md`、`tests/*.sh`：跨文件约束和压力场景。

该改动涉及 controller bootstrap、helper routing、root guidance 和 Human Gate，完成前必须执行仓库全量验证方法并生成中文报告。

## 17. 验收标准

1. 源码仓库不出现目标项目 `.agent-loop/skills/` 工件。
2. 人类显式请求和 Agent 主动候选都能进入 Project Skill Creation。
3. 创建目录前有明确 Gate 1。
4. Gate 1 通过后，全部验证通过可自动激活；验证失败保持 `proposed`。
5. 实现范围超出 Gate 1 时必须重新使用同一个 Gate 1，不新增其他激活或破坏性更新 Gate。
6. `writing-skills` 优先承担 RED/GREEN/REFACTOR；`skill-creator` 可同时承担脚手架和验证。
7. 所有 helper 默认路径被覆盖到目标项目 `.agent-loop/skills/`。
8. `proposed`、`disabled` 和 `deprecated` 不进入正常技能路由。
9. `bootstrap` 与 `on-demand` 均采用渐进加载，不自动执行 scripts。
10. 每次执行 active 项目技能都经过 Execution Gate；明确点名技能和完整具体范围的人类命令在执行摘要无新增未披露动作时可满足本次 Gate。
11. Execution Gate 授权只对定义清楚的本次 invocation、确认范围和预先声明的重试有效，不能跨任务、会话或范围复用。
12. 精确 INDEX row、技能正文和指令型/可执行资源均与 SHA-256 manifest 绑定，任一不匹配都按 project-skill drift 处理。
13. 项目技能不能覆盖 Agent Loop 控制器和 Human Gates。
14. 新增专项测试先证明 RED，再证明 GREEN，并通过全部仓库测试。
15. README、Usage、root guidance、runtime/design、templates 和 validation scenarios 保持一致。
16. 不在未经人类批准时修改技能版本号、提交、推送或发布。

## 18. 后续可能扩展

以下能力留待单独设计：

- `.agents/skills`、`.codex/skills`、`.claude/skills` 或 `.kimi/skills` 的兼容导出；
- 跨项目技能提升为全局个人技能；
- 项目技能 marketplace；
- 技能签名或远端分发；
- 自动统计技能命中率和成功率。
