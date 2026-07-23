# Proposal: Agent-Guided Lightweight Change Lane

状态：Proposal、实施、focused validation 与全量验证已完成，待最终 Human Review
目标版本：v1.5.0
创建时间：2026-07-17
默认语言：中文

## 摘要

Agent Loop 当前擅长把行为变更组织成 Feature，再通过 spec、tasks、tests、plan、TDD、Verify、Review、Drift 和 Close 保证实施质量。这条完整路径适合新能力、复杂修复、跨模块变更和高风险工作，但对边界清楚的一次性小修改可能产生明显高于修改本身的流程成本。

本 Proposal 建议在完整 Feature 流程旁增加一条由 Agent 主动判断的 `Lightweight Change Lane`（轻量变更旁路）：

```text
普通非 Bug 修改请求
→ Agent 评估影响、风险、不确定性和可验证性
→ Lightweight Execution Card
→ 按风险伸缩 Plan 与测试深度
→ Execute
→ Targeted Verification
→ Diff Review
→ Result
```

它不是“无计划直接修改”。每次轻量变更仍然必须写明背景、目标、完成标准、范围、影响、Plan、当前进度、验证和回滚，只是不创建完整 Feature workspace，也不机械要求 construction-grade plan 或完整 RED / GREEN / REFACTOR。

当 Agent 能可靠判断时，由 Agent 自主选择轻量旁路或 Feature；当 Agent 不确定时，必须停止并询问人类，给出选项、推荐和理由，在人类回答前不修改代码。

人类明确要求按 Bug 管理的问题继续走现有 Human-Guided Bug Management，不因修复看起来很小而绕过 Bug Record、Resolution Path、Feature 修复、验证和关闭逻辑。

## 1. 背景与问题

### 1.1 当前完整 Feature 路径的价值

现有 Agent Loop 通过完整 Feature 路径保证：

- 产品行为、验收标准和技术实施保持一致；
- 多步骤工作具有可恢复的任务和计划记录；
- 行为变化优先通过 TDD 获得失败与修复证据；
- 实施完成后执行 fresh verification、Review、Drift Check 和 Project Memory Update；
- Feature Close、commit、push、merge、release、publish 保持独立 Human Gate；
- Bug 修复具有稳定的问题身份、Expected Behavior、Resolution Path 和关闭证据。

这些能力不能因为新增轻量旁路而削弱。

### 1.2 当前效率问题

当前规则虽然存在 narrow one-off bypass 和 trivial task 的 No-Plan Decision，但它们不足以形成一条可稳定执行的轻量路径：

- one-off bypass 主要依赖人类明确要求跳过完整流程，Agent 不会稳定地主动判断；
- No-Plan Decision 仍发生在 Feature、task、tests 等构造完成之后；
- `maintenance-fix` 要求完整 Feature workspace；
- TDD 是统一默认，配置、路径、域名、常量等事实修正也容易被机械转换为单元测试；
- Feature Follow-up 对“小改动”保持谨慎，但缺少“不是 Bug、也不改变产品行为”的独立出口；
- Agent 可能把“步骤超过一个”误当作“必须创建 Feature”的充分条件。

结果是：一次生产脚本中已确认域名的替换，可能需要先建立 Feature、补齐完整文档、写详细 plan、制造 RED 测试，再开始实际修改。流程质量没有问题，但投入与风险不成比例。

### 1.3 根因

根因不是 Agent Loop “过于严谨”，而是当前只有两种容易被识别的实施深度：

```text
不实施 / 只讨论
或
完整 Feature 实施
```

缺少一条同时满足以下要求的正式中间路径：

- 有背景和计划；
- 有进度和完成标准；
- 有新鲜验证和 diff review；
- 不创建不必要的长期 Feature artifacts；
- 根据失败模式选择验证，而不是根据“改了代码”机械要求完整 TDD；
- 影响扩大时能可靠升级到 Feature；
- Agent 无法判断时把选择交还人类。

## 2. 已确认的核心设计

本轮讨论已经确认：

1. 这是 v1.5.0 新增的旁路能力，不是 v1.4.1 对现有 Feature 流程的修复。
2. 轻量旁路不取消背景、Plan、进度、验证或回滚说明。
3. Plan 必须存在，但详细程度由 Agent 根据风险、范围和不确定性决定。
4. TDD 不是旁路中的固定仪式；行为逻辑变化使用最小、针对性的 RED / GREEN，事实修正使用与失败模式匹配的验证。
5. Agent 能判断时自主选择轻量旁路或 Feature，不要求人类每次主动说“轻量处理”。
6. Agent 不确定时必须询问人类，并给出选项、推荐和理由。
7. 影响范围大、需要严谨设计、存在长期追踪价值或触发硬边界时，直接走 Feature。
8. 人类明确要求按 Bug 管理时，按 Bug 管理，不使用轻量旁路替代 Bug 逻辑。
9. 轻量执行过程中发现范围扩大、事实不清或验证策略失效时，停止旁路并重新路由，不能继续扩大修改。
10. commit、push、merge、release、publish、生产写入、付费调用和其他既有 Human Gate 不因旁路而获得授权。

## 3. 目标

本 Proposal 的目标是：

1. 为边界明确、低耦合、可验证、可回滚的普通非 Bug 修改提供正式轻量路径。
2. 让 Agent 主动判断实施深度，而不是以文件数、代码行数或步骤数量机械创建 Feature。
3. 保留最小但完整的背景、Plan、进度、验证、回滚和结果信息。
4. 让 Plan、测试和记录深度随风险伸缩。
5. 明确轻量旁路、Bug Management 和 Feature Construction 的优先级与边界。
6. 在 Agent 不确定时生成低认知负担的人类选择，而不是静默猜测。
7. 在执行中发生 scope expansion 时安全升级到 Feature。
8. 保持所有生产、外部副作用、Git、Submit、Release 和 Publish Human Gate 不变。

## 4. 非目标

本 Proposal 不做以下事情：

- 不把 Feature 流程改成可选建议；
- 不为明确 Bug 建立第二套修复流程；
- 不允许无 Plan 修改；
- 不允许无 fresh verification 的完成声明；
- 不以“一行修改”“一个文件”“五分钟以内”等机械阈值判断风险；
- 不允许人类一句“简单处理”覆盖安全、数据、公共契约或生产门禁；
- 不新增默认 `.agent-loop/quick-fixes/`、`.agent-loop/changes/` 或轻量任务 backlog；
- 不把每次轻量修改写入 `project.md`；
- 不引入新的持久生命周期状态；
- 不自动 commit、push、merge、release、publish 或执行生产写入；
- 不在 Proposal 阶段修改 Skill runtime、模板、版本号或安装副本。

## 5. 核心概念

### 5.1 Lightweight Change Lane

`Lightweight Change Lane` 是 Agent Loop 在 Feature construction 之前，对普通非 Bug 修改提供的内部执行旁路。

它不是 canonical stage，不是 Feature Type，不是 Bug Resolution Path，也不创建新的长期项目状态。

### 5.2 Lightweight Execution Card

`Lightweight Execution Card`（轻量执行卡）是旁路的一次性执行控制面，至少表达：

- 为什么要改；
- 要达到什么结果；
- 修改范围是什么；
- 为什么可以不创建 Feature；
- 计划如何执行；
- 当前做到哪一步；
- 如何验证；
- 如何回滚；
- 哪些动作仍需要 Human Gate。

执行卡默认保存在当前任务上下文中，不默认写入目标项目 `.agent-loop/`。如果工作需要跨会话恢复、暂停、handoff、subagent、长期追踪或复杂证据保存，应升级为 Feature，而不是新增一套轻量 workspace。

### 5.3 Adaptive Depth

`Adaptive Depth` 表示 Agent 根据影响、风险、不确定性、范围、可验证性和可回滚性决定：

- 执行卡写多细；
- Plan 包含多少步骤；
- 是否需要最小 TDD；
- 使用哪些 targeted verification；
- 是否已超过旁路边界并应升级 Feature。

Adaptive Depth 不允许 Agent降低 Human Gate、fresh verification 或完成声明标准。

## 6. 路由模型

### 6.1 总体路由

```text
Latest Human Message
→ Message Intent Classification
→ explicit Bug management intent?
   ├─ yes
   │  → Human-Guided Bug Management
   │  → Bug Record / Resolution Path
   │  → existing Feature-based repair flow
   │
   └─ no
      → actionable non-Bug change?
         ├─ no  → existing Chat / Requirements / Operational / other route
         └─ yes → Lightweight Change Assessment
                  ├─ clearly eligible    → Lightweight Execution Card
                  ├─ Feature trigger     → Feature Construction
                  └─ uncertain           → Human Choice with Agent Recommendation
```

### 6.2 Bug 优先规则

人类明确要求“这是 Bug”“登记为 Bug”“按 Bug 跟踪”“走 Bug 管理”或表达等价管理意图时：

- 直接进入 Human-Guided Bug Management；
- 不因为修复范围小而把它降级成轻量执行卡；
- Bug Record 继续拥有身份、证据、Expected Behavior、Status、Resolution、Resolution Path、验证和关闭；
- Feature 继续拥有修复 tasks、tests、plan、实现、Review 和 Drift。

判断基于人类意图和上下文，不以是否出现英文 `bug` 单词作为唯一规则。

### 6.3 普通小修改规则

下列表达通常进入 Lightweight Change Assessment，而不是自动建 Feature：

- “把这个已确认的域名替换掉”；
- “更新脚本里的路径”；
- “修正这个配置键”；
- “同步已经决定的版本号或常量”；
- “改一下这段文档或命令示例”；
- “把现有规则在另一个已知引用点同步一下”。

Assessment 仍要检查真实影响，不能只相信“小改一下”等主观描述。

### 6.4 Project Entry 边界

轻量旁路不能绕过 Project Entry 分类、root guidance、dirty work、目标文件和安全边界检查，但也不能为了一个合格的小修改强制初始化或修复整套 `.agent-loop/` 长期记忆。

- 已有可靠 `.agent-loop/` 时，只读取判断当前修改所需的项目记忆、active Feature 和相关约束；
- 没有 `.agent-loop/` 时，不为了执行卡创建它，只检查 root guidance、Git/dirty 状态、目标文件、附近引用和验证入口；
- 只有当旁路判断实际依赖某项 project memory claim 时，才要求该 claim 可靠；
- 如果已有记忆声明与代码事实冲突，或者缺失记忆使影响无法判断，停止并进入 Recovery、Feature 或 Human Choice；
- Project Entry classification 始终需要，但完整 Project Entry Scan / Init Project 不是轻量旁路的默认前置产物。

## 7. Agent 自主判断模型

Agent 至少从六个维度判断：

| 维度 | 轻量信号 | Feature 信号 |
|---|---|---|
| 产品语义 | 已决定事实的机械同步 | 新能力、验收变化、产品规则变化 |
| 边界影响 | 已知的局部调用或引用 | 公共 API、事件、数据、状态、权限、安全边界 |
| 范围 | 可枚举、耦合低、所有者清楚 | 跨模块、未知消费者、范围持续扩张 |
| 不确定性 | 输入、目标和完成标准明确 | 需要需求、设计、ADR 或架构判断 |
| 验证 | 存在精确、快速、可重复的验证 | 需要完整测试矩阵、E2E、迁移或长期观察 |
| 恢复 | 修改可逆且回滚明确 | 不可逆迁移、外部状态变化或复杂恢复 |

文件数量、代码行数和步骤数量只能作为辅助证据，不能单独决定路由。

### 7.1 轻量旁路准入条件

进入旁路前，Agent 必须能同时确认：

1. 目标和完成标准明确；
2. 修改范围可以枚举；
3. 不需要新的产品或技术决策；
4. 不改变公共契约、数据语义、状态模型、权限或安全边界；
5. 不引入新依赖、迁移或长期架构边界；
6. 存在准确、可执行的 targeted verification；
7. 修改可回滚；
8. 不需要 Bug 身份或 Feature 级长期追踪；
9. 不需要跨会话、handoff 或 subagent 才能完成；
10. 当前证据足以让 Agent承担旁路判断责任。

### 7.2 Feature 硬触发器

出现任一项时，默认直接走 Feature：

- 新增或改变用户可见行为；
- 改变验收标准、业务规则或产品概念；
- 改变 API、事件、schema、持久化数据、状态流或数据来源；
- 涉及权限、安全、凭据处理或信任边界；
- 涉及数据迁移、不可逆操作或复杂恢复；
- 引入新依赖、服务、架构边界或跨模块协议；
- 存在未知调用方或影响范围无法界定；
- 需要 ADR、Delivery Contract、复杂 E2E 或多环境发布设计；
- 需要跨会话、暂停恢复、handoff、subagent 或长期进度追踪；
- 人类明确要求按 Feature 或 Bug 管理；
- 轻量执行过程中触发 scope expansion。

## 8. Agent 不确定时的人类选择

Agent 无法可靠判断时必须停止，不得先创建 Feature，也不得先修改代码。

人类选择必须保持简短：

```markdown
## 路由需要确认

发现：该修改可能影响生产域名的外部调用方，目前证据不足以确认。

选项 A：轻量执行卡
- 适用于仅替换已确认的内部脚本配置。
- 验证：引用扫描、语法检查、dry-run。

选项 B：Feature
- 适用于正式域名迁移或存在外部调用方。
- 增加影响分析、完整测试与发布/回滚设计。

Agent 推荐：B
原因：当前无法排除公共调用契约变化。

请确认选择 A 或 B。
```

规则：

- 必须给出 Agent 推荐，不能把未整理的问题全部甩给人类；
- 必须解释推荐所依据的具体证据和未知项；
- 只提供当前真实可行的少量选项；
- 人类回答前不执行修改；
- 人类选择旁路不能覆盖 Feature 硬触发器或既有 Human Gate；
- 新证据出现后允许重新判断并再次询问。

## 9. Lightweight Execution Card

### 9.1 最小字段

```markdown
## 轻量执行卡

背景：
目标与完成标准：
修改范围：
旁路判断：
影响与风险：

执行计划：
- [ ] 定位并核对修改点
- [ ] 完成限定修改
- [ ] 执行针对性验证
- [ ] 检查 diff、影响与回滚

当前进度：
验证方式：
回滚方式：
Human Gates：
结果与遗留：
```

背景、目标、Plan、当前进度和验证不得省略。无适用内容的字段应写明“无”及原因，不能留空或使用模糊占位符。

### 9.2 Plan 深度

Plan 始终存在，但按风险伸缩：

| 情况 | 合适深度 |
|---|---|
| 单点事实替换 | 2–4 个步骤，写清文件、旧值/新值、验证和回滚 |
| 多处一致性同步 | 增加引用发现、受影响文件清单和残留扫描 |
| 少量内部逻辑 | 增加最小行为测试、RED/GREEN 预期和回归检查 |
| 外部环境相关 | 增加环境、入口、影响、受控验证和回滚；副作用另行 Human Gate |
| 范围或失败模式不清 | 不继续加长轻量 Plan，升级 Feature 或询问人类 |

轻量 Plan 不要求为 near-zero-context executor 写完整 construction-grade code context，但必须足以让当前任务明确“做到哪一步”和“还剩什么”。

### 9.3 进度

不新增持久状态枚举。进度由执行计划 checkbox 和一句 `当前进度` 表达。

Agent 在执行过程中应及时更新当前步骤；完成报告必须说明：

- 哪些步骤完成；
- 哪些未完成或被取消；
- 是否发生路由升级；
- fresh verification 结果；
- 是否存在需人类处理的遗留。

## 10. 轻量 TDD 与验证

### 10.1 原则

旁路不取消测试，而是按照真实失败模式选择最小有效证据：

```text
behavior logic changed and isolatable
→ targeted RED
→ minimal GREEN
→ focused regression

fact/config/path/domain/docs changed
→ syntax / parse / reference / residual / dry-run checks
→ focused regression when applicable
```

不要为了满足 TDD 形式而制造不能证明风险的测试。

### 10.2 验证选择矩阵

| 修改类型 | 默认验证 |
|---|---|
| 域名、路径、常量 | 新旧值核对、旧值残留扫描、引用检查、语法或配置解析 |
| Shell / Python 等脚本参数 | 语法检查、帮助输出、参数解析、限定 dry-run |
| 少量脚本分支逻辑 | 一个最小失败用例、RED/GREEN、相关脚本回归 |
| 文档、示例、元数据 | 格式、链接、引用、一致性和旧值残留检查 |
| 构建或部署描述 | 配置解析、生成物检查、非生产 dry-run、回滚命令核对 |
| 生产相关事实 | 本地/静态检查先行；任何真实生产读取、写入或外部调用按既有授权边界执行 |

### 10.3 完成标准

轻量变更不能仅凭“代码已经改了”完成。必须同时满足：

- Plan 已执行或明确记录未执行项；
- targeted verification 新鲜通过，或如实报告失败/受限；
- diff 只包含授权范围；
- 没有发现 Feature 硬触发器或未处理 scope expansion；
- 回滚方式仍然有效；
- durable memory impact 已检查；
- 结果摘要已交付人类；
- commit、push、release 等后续动作仍等待各自 Human Gate。

## 11. Scope Expansion 与升级

### 11.1 升级信号

轻量执行中发现以下情况时立即停止扩大修改：

- 目标文件或消费者超出原执行卡范围；
- 新旧值并非单纯同步，而是产品或技术选择；
- 验证失败揭示新的行为缺陷；
- 需要修改 API、数据、状态、权限、安全或架构边界；
- 需要新依赖、迁移、Delivery Contract 或 ADR；
- 需要暂停、跨会话继续或交给其他 Agent；
- 无法给出可靠回滚；
- 当前变更应被明确识别为 Bug。

### 11.2 升级动作

Agent 必须：

1. 停止未授权的扩大修改；
2. 保留已经获得的调查、diff 和验证证据；
3. 说明触发升级的具体事实；
4. 推荐进入 Bug Management、Requirements Discussion 或 Feature Construction 中唯一合适的一条路径；
5. 询问人类确认；
6. 人类确认后，把执行卡中的背景、范围、证据和未完成 Plan 作为新流程输入，避免重复调查。

如果已经产生安全且独立的局部修改，Agent 仍不得自行决定保留、回退或提交；应在升级摘要中向人类说明现状和推荐。

## 12. 与现有能力的关系

### 12.1 与 Feature 的关系

- 轻量旁路发生在 Feature workspace 创建之前；
- 它不创建 `spec.md`、`tasks.md`、`tests.md`、`plan.md` 或 `notes.md`；
- 如果已有 active Feature 明确拥有该修改，继续使用已有 Feature，不建立旁路逃逸；
- 如果需要 Feature 级追踪，升级后按现有 Feature construction 和 Plan Gate 执行；
- 轻量旁路的 Plan 不等于 Feature `plan.md`。

### 12.2 与 Bug Management 的关系

- 人类明确 Bug 管理意图时，Bug Management 优先；
- 轻量旁路不成为新的 Bug Resolution Path；
- 已存在 Bug Record 的修复仍按 Human-confirmed Resolution Path 执行；
- Agent 不得因为修复小而静默关闭或绕过 Bug；
- 轻量执行中识别出应被跟踪的缺陷时，停止并推荐 Bug intake。

### 12.3 与 Operational Support 的关系

- 只读诊断、运行、查询和操作支持继续按 Operational Support；
- 当支持过程中确认只需要一个普通非 Bug 的局部代码/配置修改时，可进入 Lightweight Change Assessment；
- 涉及外部服务、生产、付费调用、配置写入或部署的动作继续使用原有 Human Gate；
- 旁路授权不能从“修改本地脚本”扩展为“执行生产变更”。

### 12.4 与 Project Memory / Drift 的关系

- 每次旁路完成前检查 durable memory impact；
- 已经由人类确认的项目事实可以在同一执行卡内做机械一致性同步，但必须列入修改范围和验证；
- 如果修改本身决定了新的长期产品、架构、环境或发布事实，不能通过旁路写入，应升级到相应流程；
- 不把轻量执行历史、临时进度或任务 backlog 写进 `project.md`；
- 没有 durable change 时，明确记录 `Project Memory Impact: none`。

### 12.5 与 Branch / Submit / Git 的关系

- 已采用 Branch Strategy 时，旁路仍要核对当前分支和 Target Release Context；
- sealed release 规则仍然生效，不能因为修改小而继续修改已发布版本；
- 创建、切换、删除分支仍需 Branch Action / Cleanup Gate；
- commit、push、PR、merge、tag、release、publish 各自保持独立 Human Gate；
- 轻量执行卡只授权其中明确写出的本地修改和验证，不隐含任何 Git mutation。

## 13. 典型场景

### 13.1 已确认生产脚本域名替换

事实：新域名已经由现有配置/规范确认，本次只把脚本里的旧引用同步为新值，无外部调用方变化。

推荐：轻量执行卡。

Plan：

1. 定位脚本及相关引用；
2. 替换限定值；
3. 执行旧域名残留扫描和脚本语法检查；
4. 在不触发生产副作用的前提下 dry-run；
5. 检查 diff 和回滚方式。

不要求为字符串替换制造单元测试。

### 13.2 正式生产域名迁移

事实：需要决定新入口，涉及 DNS、证书、调用方、灰度、回滚或公开接口。

推荐：Feature；必要时进入 Decision & Design 和 Delivery Contract。

即使最终代码只改一行，也不能进入轻量旁路。

### 13.3 小范围脚本条件修正

事实：预期行为已明确，只修改一个可隔离的内部条件分支，无公共契约变化。

推荐：可使用轻量执行卡，并增加一个最小失败用例：先证明旧逻辑失败，再修复并运行相关回归。

如果失败揭示状态、数据或调用方问题，立即升级 Feature。

### 13.4 人类明确报告 Bug

事实：“这是一个 Bug，请登记并修复。”

推荐：Bug Management。

即使疑似一行修复，也先建立/匹配 Bug Record，确认 Expected Behavior 和 Resolution Path，再进入现有修复流程。

### 13.5 Agent 无法确认调用范围

事实：目标看起来是域名替换，但代码中存在多个生成入口，无法排除外部消费者。

推荐：停止并向人类提供 Lightweight / Feature 选项，Agent 推荐 Feature，等待回答。

## 14. 失败与恢复

| 情况 | Agent 行为 |
|---|---|
| 路由证据不足 | 停止，给人类选项和推荐 |
| 修改范围扩大 | 停止，输出 scope expansion 摘要并推荐升级 |
| targeted verification 失败 | 不声明完成；诊断是否仍适合旁路，否则升级 |
| 发现无关 dirty work | 隔离并报告；不能覆盖或带入结果 |
| 生产验证需要授权 | 先完成本地检查，停在生产 Human Gate |
| 修改已部分完成但需升级 | 报告当前 diff、可保留/回退建议，等待人类决定 |
| 上下文即将中断 | 若不能安全完成和汇报，推荐升级 Feature 或暂停，不创建隐藏的临时长期状态 |

## 15. 权限模型

### Agent 可以自主执行

- 只读检查项目事实；
- 判断是否满足轻量旁路条件；
- 创建 response-local Lightweight Execution Card；
- 在已授权修改范围内决定 Plan 详细程度；
- 选择 targeted verification 或最小 TDD；
- 更新执行卡进度；
- 发现 scope expansion 后停止并推荐升级；
- 输出结果、风险、验证和回滚摘要。

### Agent 必须询问人类

- 无法可靠选择 Lightweight / Feature / Bug 路由；
- scope expansion 需要升级流程；
- 人类意图可能是 Bug 管理但不明确；
- 需要新的产品、架构、API、数据、状态、权限或安全决策；
- 需要生产/外部副作用、配置写入或付费调用授权；
- 需要分支、subagent、commit、push、PR、merge、tag、release、publish；
- 需要保留还是回退已经产生的部分修改。

## 16. 建议实现范围

本 Proposal 获批后，Implementation Plan 应至少评估并协调以下 surface：

### 核心 authority

- `SKILL.md`：增加轻量旁路入口、执行卡摘要、stop/upgrade 规则；
- `references/runtime.md`：定义 canonical routing precedence、eligibility、uncertain Human Choice、scope expansion 和 gate boundaries；
- `references/design.md`：定义 Lightweight Change Lane、Execution Card、Adaptive Depth、authority 和 invariants；
- `references/concepts.md`：增加精简概念定义。

### 执行与路由

- `references/stage-guides.md`：增加 Lightweight Change Assessment / execution procedure，并修正 Operational Support code-change fallback；
- `references/workflow-checklists.md`：增加轻量判断、执行卡、针对性验证、升级和完成检查；
- `references/skill-routing.md`：明确轻量旁路不进入 mandatory Plan / Execute helper stage；最小 RED/GREEN 直接受执行卡约束，只有升级 Feature 后才恢复强制 helper 协议；
- `references/external-skill-adapters.md`：说明外部 helper 不能把 response-local card 扩张成外部文档目录或完整 Feature；
- `references/feature-follow-up.md`：保持明确 Bug 与 Feature-owned follow-up 的现有规则，同时为普通非 Bug 局部修改保留前置 assessment；
- `references/bug-management.md`：明确 Bug intent 优先且不增加 Lightweight Resolution Path；
- `references/implementation-planning.md`：区分 Feature construction-grade plan 与轻量 response-local plan。

### 模板与人类文档

- 新增 source-level `templates/lightweight-execution-card.md`，仅作为 response 模板，不默认复制进目标项目；
- `templates/root-AGENTS.md`：只增加一句简短提醒，避免把完整规则塞进根 guidance；
- `README.md`：说明轻量旁路与完整 Feature 的关系；
- `Usage.md`：增加域名、路径、配置、最小逻辑修正和不确定询问示例；
- `CHANGELOG.md`：记录 v1.5.0 新能力；
- `references/validation-scenarios.md`：增加正向、反向和 scope expansion 压力场景。

### Version Sync

实现经人类批准进入 v1.5.0 时，按仓库 Version Sync Checklist 同步：

- `SKILL.md`；
- `plugin.json`；
- `README.md`；
- `Usage.md`；
- `CHANGELOG.md`；
- `templates/root-AGENTS.md` managed block revision。

Proposal 本身不授权版本变更。

## 17. 验证设计

该能力改变 canonical routing precedence、Plan/TDD selection 和 Feature entry boundary，实施时必须按 `docs/maintenance/full-validation-method.md` 完成 RED baseline、focused regressions、全量 executable tests 和六域语义审计。

### 17.1 必须覆盖的 focused 场景

1. 已确认内部域名替换进入轻量旁路，不创建 Feature。
2. 正式域名迁移触发 Feature。
3. 一行 API/schema/state/security 修改仍触发 Feature。
4. 多文件但机械一致性同步可在证据充分时进入轻量旁路。
5. 人类明确 Bug 意图时进入 Bug Management，不进入旁路。
6. Agent 不确定时停下、给出选项和推荐，回答前零修改。
7. 执行卡始终包含背景、目标、Plan、进度、验证和回滚。
8. 事实修正不强造 RED 测试，但必须执行 targeted verification。
9. 少量可隔离逻辑使用最小 RED/GREEN。
10. scope expansion 停止执行并推荐升级 Feature。
11. 已有 active Feature 拥有修改时不使用旁路逃逸。
12. Project Memory durable fact 只是同步时可以列入卡片；产生新决策时升级。
13. 生产、付费、外部写入和 Git Human Gates 保持不变。
14. sealed release 不因旁路而被修改。
15. response-local card 不默认创建 `.agent-loop/changes/` 或类似目录。
16. 没有 `.agent-loop/` 的项目只做最小 Project Entry/guidance/scope 检查，不为轻量执行卡初始化长期记忆。

### 17.2 反向压力断言

实现后的验证必须拒绝以下错误行为：

- “改动只有一行，所以直接轻量处理”；
- “人类说简单处理，所以跳过安全/数据影响”；
- “旁路不需要 Plan”；
- “旁路不需要测试”；
- “所有代码修改都必须制造 RED 测试”；
- “明确 Bug 因修复小而跳过 Bug Management”；
- “不确定时 Agent 默认选旁路”；
- “scope expansion 后继续修改”；
- “轻量卡自动授权 commit/push/生产写入”；
- “为每次轻量修改创建长期目录或污染 project.md”。

## 18. 验收标准

Proposal 实施完成后，应能证明：

1. Agent 对普通非 Bug 修改先按影响判断，而不是按步骤数直接创建 Feature。
2. 合格的小修改使用 Lightweight Execution Card，且背景、Plan、进度、验证和回滚完整。
3. Plan 与测试深度由风险驱动，但完成证据标准不降低。
4. 事实修正使用 targeted verification，少量逻辑变化使用最小针对性 TDD。
5. Feature 硬触发器能够阻止高影响工作进入旁路。
6. 明确 Bug 始终进入 Bug Management。
7. Agent 不确定时只向人类提出整理后的少量选项，并给出推荐。
8. 人类回答前不创建 Feature、不修改代码、不执行外部副作用。
9. scope expansion 能停止、保留证据并升级到正确流程。
10. 轻量旁路不会创建新的默认目标项目目录、backlog 或状态系统。
11. 生产、外部调用、Git、Submit、Release 和 Publish Human Gate 完整保留。
12. focused validation 与 full validation 均通过，并保存新的中文报告。

## 19. Proposal Gate

本 Proposal 已通过 Human Review，只确认产品和运行模型，不授权实施。

Human Review 需要确认：

- 是否接受 `Lightweight Change Lane` 作为 v1.5.0 新能力；
- 是否接受明确 Bug 始终优先走 Bug Management；
- 是否接受 response-local Lightweight Execution Card，不新增默认目标项目目录；
- 是否接受 Agent 自主判断、无法判断时询问人类；
- 是否接受 Adaptive Plan 与 targeted TDD / verification；
- 是否接受 scope expansion 自动停止并升级判断；
- 是否进入独立 Implementation Plan。

下一步是编写 construction-grade Implementation Plan。Implementation Plan、实施、版本同步、commit、push、tag、release 和 publish 都有独立 Human Gate。
