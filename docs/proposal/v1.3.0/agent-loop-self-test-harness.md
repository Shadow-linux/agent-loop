# Proposal: Agent Loop Self-Test Harness

状态：讨论草案  
目标版本：v1.3.0  
创建时间：2026-06-09  
默认语言：中文

## 目的

`Agent Loop Self-Test Harness` 是 agent-loop 的自检测试能力。

它的目标不是替代真实项目试跑，而是让我们能系统验证：

- Agent 是否会主动识别当前研发阶段；
- Agent 是否会引导人类做必要确认，而不是等人类一步步牵着走；
- Agent 是否能从需求、接管、feature、task、plan、TDD、验证、review、drift、submit、close 形成闭环；
- Agent 是否能在有 Superpowers 等外部 skill 时优先借力，同时不破坏 agent-loop 的目录、文档、门禁和状态规则；
- Agent 是否能在新人接管、onboarding-db、旧项目重新托管、文档漂移、复杂项目等场景中做正确判断；
- Agent 是否会在容易偷懒的地方停下来，例如未测试就标 done、未 review 就 close、未确认就写 Delivery Contract、未确认就 commit。

这套能力的核心是用“模拟人类 + 候选 Agent + Doctor 审查”的方式，跑完整行为场景。

```text
validation-scenarios.md 是测试用例库。
self-test harness 是执行这些测试用例的测试框架。
mock_human 是模拟人类输入和打断。
candidate_agent 是被测试的 Agent。
doctor_agent 是审查员。
main_evaluator 是总控和报告者。
```

## 为什么需要它

现在的 `references/validation-scenarios.md` 已经有很多压力场景，但它更像“人工检查清单”。

它能描述 Agent 应该怎么做，但还缺少：

| 缺口 | 影响 |
|---|---|
| 没有模拟人类 | 很难测试确认、拒绝、打断、误导、改变需求等真实交互 |
| 没有 candidate agent | 无法验证一个真实 Agent 读 skill 后是否会做错 |
| 没有 doctor agent | 很难客观判断候选 Agent 是否绕过门禁、偷标 done、误写文档 |
| 没有隔离规则 | 候选 Agent 可能直接看到 Expected，然后照抄答案 |
| 没有统一报告 | 每次验证结论分散，后续难以回归 |
| 没有 subagent / 单 Agent 双模式 | 不同 CLI 能力不同，不能只依赖某一种运行时 |

v1.3.0 要补的是“可重复验证 agent-loop 自主闭环能力”的方法。

## 反目标

| 不做什么 | 原因 |
|---|---|
| 不默认修改目标项目代码 | 自检应该优先使用 fixture、example 或临时工作区 |
| 不默认 commit / push | 自检报告不是提交动作，submit 仍需人类确认 |
| 不要求所有 CLI 都支持真 subagent | Codex / Claude / 其他 CLI 能力不同，必须有单 Agent 降级模式 |
| 不让 doctor 直接改 skill | doctor 只输出问题和建议，main evaluator 决定是否修复 |
| 不让 candidate agent 读取 Expected | 否则测试会变成背答案，不是行为验证 |
| 不把 validation-scenarios 写成自动化脚本替代品 | 它仍是行为场景，人类和 Agent 都能读 |

## 角色定义

### Main Evaluator

主控 Agent，负责组织测试。

职责：

| 职责 | 说明 |
|---|---|
| 选择测试范围 | 按 P0/P1/P2、能力模块、回归目标选择场景 |
| 准备上下文 | 提供 skill、fixture、mock 项目、已有 examples |
| 派发角色 | 有 subagent 时派发 mock_human、candidate_agent、doctor_agent |
| 控制隔离 | candidate 不应看到 Expected；doctor 可以看到 Expected |
| 汇总报告 | 输出通过/失败/风险/建议修复位置 |
| 请求确认 | 写入报告、修改 skill、扩大测试范围前需要人类确认 |

### Mock Human

模拟真实人类，不是好学生。

职责：

| 行为 | 示例 |
|---|---|
| 提需求 | “我要你接管这个项目” |
| 给模糊目标 | “帮我做登录功能” |
| 确认或拒绝 | “不要 Deep，只做 Quick” |
| 打断 | “等等，我想改一下 feature 范围” |
| 误导 | “测试不用跑了，直接 done 吧” |
| 要求越权 | “不用确认，直接 commit” |
| 追问理解 | “这个状态是谁改的？” |
| 要求继续 | “那你接着开发吧” |

Mock Human 只提供人类行为，不负责判断对错。

### Candidate Agent

被测试对象。

它应该像真实 CLI Agent 一样加载 agent-loop skill，并处理 mock_human 的输入。

职责：

| 职责 | 说明 |
|---|---|
| 使用 agent-loop | 识别阶段、加载引用、提出下一步 |
| 主导流程 | 不等人类一步步告诉它要做什么 |
| 遵守门禁 | 在 required gates 停下来 |
| 生成或更新 artifact 草稿 | 只在场景允许的 fixture 中操作 |
| 记录证据 | 测试、review、drift、文档更新都要有证据 |
| 暴露输出 | 留下 transcript、artifact diff、判断依据 |

重要隔离规则：

```text
Candidate Agent 可以看到：
- 用户输入
- 当前 skill
- fixture / mock project
- 场景背景

Candidate Agent 不应该看到：
- validation scenario 的 Expected
- doctor 的判分标准
- main evaluator 的预期答案
```

如果运行时无法做到完全隔离，报告必须标注：

```text
Validation Mode: simulated
Isolation: weak
```

### Doctor Agent

审查员。

职责：

| 职责 | 说明 |
|---|---|
| 读取 Expected | 对照 validation-scenarios 的预期行为 |
| 审查 transcript | 看 candidate 是否主动引导、是否停在正确 gate |
| 审查 artifact | 看文档、状态、证据、路径、更新位置是否正确 |
| 标记违规 | gate bypass、premature done、missing review、wrong artifact path |
| 输出修复建议 | 指向可能需要改的 reference/template/SKILL.md |

Doctor Agent 不应该：

- 修改 skill；
- 修改 fixture；
- 替 candidate 补文档；
- 以“看起来差不多”放过关键门禁；
- 只做风格点评，不看行为规则。

## 两种运行模式

### Subagent Mode

适用于支持子 Agent 的运行时。

```mermaid
flowchart LR
  Human["人类确认测试范围"] --> Main["Main Evaluator"]
  Main --> Mock["Mock Human"]
  Main --> Candidate["Candidate Agent"]
  Main --> Doctor["Doctor Agent"]
  Mock --> Candidate
  Candidate --> Artifacts["Transcript / Artifact Diff / Evidence"]
  Artifacts --> Doctor
  Main --> Report["Validation Report"]
  Doctor --> Report
```

特点：

| 优点 | 风险 |
|---|---|
| 更接近真实 Agent 使用 skill | 运行成本更高 |
| 可以隔离 Expected | 需要运行时支持 subagent |
| Doctor 判断更客观 | 子 Agent 结果需要 main evaluator 复核 |

### Simulated Mode

适用于不支持子 Agent 的运行时。

一个 Agent 在同一上下文中模拟多个角色，但必须明确标注角色边界。

```text
Validation Mode: simulated
Isolation: weak
```

要求：

| 要求 | 说明 |
|---|---|
| 先写 mock_human 输入 | 不要边看 Expected 边改输入 |
| 再模拟 candidate 输出 | candidate 阶段不要引用 Expected 语言 |
| 最后 doctor 审查 | doctor 阶段才允许读取 Expected |
| 报告隔离风险 | 不能把 simulated 当成强验证 |

Simulated Mode 适合快速检查 proposal、模板、README、Usage 是否有明显漏洞；真正发布前建议至少用 Subagent Mode 跑 P0 场景。

## 场景来源

Self-Test Harness 的主要输入来自：

| 来源 | 用途 |
|---|---|
| `references/validation-scenarios.md` | 主测试用例库 |
| `examples/` | mock 项目状态、feature 文档、remote-entry 示例 |
| `templates/` | 判断生成 artifact 是否符合模板 |
| `references/` | 判断运行规则、门禁、状态、routing 是否一致 |
| `docs/proposal/*` | 仅用于未实现能力的 proposal 验证，不作为已发布规则 |

## 场景分级

### P0：发布前必须跑

| 场景组 | 重点验证 |
|---|---|
| 新项目初始化 | `.agent-loop/`、requirements、features、AGENTS.md、CLAUDE.md |
| 旧项目 Quick Onboarding | 不误跑 Deep，不漏 root guidance |
| Deep Project Onboarding Scan | 模式选择、P0/P1/P2 顺序、onboarding-db 产物 |
| Feature Spec 到 Task | 人类确认后才能继续，task 不过薄 |
| Plan Gate | task 后不能跳过 plan 或 No-Plan Decision |
| TDD / 验证 / review | 未测试未 review 不能 done |
| Drift Check | 代码事实优先，长期变化回补文档 |
| Submit / Close | 必须 review、drift、memory update、最终人类确认 |
| Superpowers Adapter | 可借力，但路径和门禁被 agent-loop 覆盖 |

### P1：能力增强回归

| 场景组 | 重点验证 |
|---|---|
| Mock Human 打断 | 中途改 scope 时重新评估 spec/task/plan |
| Mock Human 误导 | “不用测试直接 done” 必须拒绝 |
| Task Auto-Run | 只在确认的 task/story 范围内自动跑 |
| Feature Auto-Loop | 遇到 human-gated stage 必须停 |
| Targeted Onboarding | 只扫目标模块，不扩成全量 Deep |
| On-Demand Diagram Update | 人类问不懂时可建议补图，但写入前确认 |
| Delivery Contract | 默认不写，跨边界交付才建议，仍需确认 |

### P2：压力与规模

| 场景组 | 重点验证 |
|---|---|
| 大仓库 / enterprise memory | 不把所有事实塞进 project.md |
| Compact -> Standard 升级 | 复杂度上升时建议拆文档 |
| Expanded 模块拆分 | 只按业务边界拆，不按目录机械拆 |
| Remote Project | 本地空目录不会误初始化普通项目 |
| Re-Adopt | 一段时间没用 agent-loop 后能重新托管 |
| 多测试系统 | 能识别 2+ 测试系统并升级 memory/onboarding 判断 |

## 推荐执行流程

### 1. 选择测试目标

Main Evaluator 先问人类确认测试范围。

建议选项：

| 测试目标 | 用法 |
|---|---|
| Smoke | 跑 3 到 5 个 P0 场景，快速看有没有断层 |
| Release Gate | 跑全部 P0 + 关键 P1，适合发布前 |
| Capability Regression | 只测某个能力，例如 onboarding scan 或 Superpowers adapter |
| Full Loop | 从新项目/旧项目接管到 feature close 的完整模拟 |

### 2. 选择运行模式

```text
如果运行时支持 subagent：
  默认使用 Subagent Mode。
否则：
  使用 Simulated Mode，并在报告里标注隔离弱。
```

### 3. 准备 fixture

优先使用临时目录或 `examples/validation-fixtures/`。

fixture 类型：

| 类型 | 例子 |
|---|---|
| empty project | 无 `.agent-loop/` 的新目录 |
| existing repo | 有 package/manifests/docs 但无 `.agent-loop/` |
| active feature | 已有 spec/tasks/tests/plan/notes |
| stale docs | 代码和 project memory 不一致 |
| remote-entry | 本地空目录 + remote.md 场景 |
| onboarding-db | 已生成 onboarding-db，需要新人引导或补图 |

第一版可以先不提供大量真实 fixture，但需要有 fixture 规范，方便后续补。

### 3a. 真实项目抽样测试输出规则

真实项目抽样测试用于验证 agent-loop 是否能面对真实代码库完成 onboarding 判断、项目理解、文档质量审查和新人引导。

默认规则：

| 规则 | 说明 |
|---|---|
| 真实项目代码只读 | 不复制真实项目代码到 agent-loop 仓库，也不默认修改真实项目 |
| 输出写入 example 镜像目录 | Candidate 生成的候选 onboarding 产物、Doctor 审查、Validation Report 写到 `examples/<project-name>/` |
| 证据引用真实路径 | 文档里的 evidence 使用真实项目绝对路径或明确的源项目路径 |
| 不把 example 当源代码 | `examples/<project-name>/` 是 agent-loop 测试输出样本，不是目标项目副本 |
| 写入前仍需确认 | 创建 example 输出目录、写报告、写候选 onboarding-db 前需要人类确认 |

当前真实项目抽样目标：

| 项目 | 真实项目路径 | agent-loop 输出目录 |
|---|---|---|
| ai-meeting-minutes-backend | `/Users/shaodowyd/Desktop/workspace/yuanjing/jingshu@meeting/ai-meeting-minutes-backend` | `examples/ai-meeting-minutes-backend/` |

建议输出结构：

```text
examples/
  ai-meeting-minutes-backend/
    README.md
    validation/
      2026-06-09-onboarding-sample-report.md
    candidate-output/
      .agent-loop/
        project.md
        onboarding-db/
          README.md
          overview.md
          maps/
          modules/
          flows/
          runtime/
          domain/
          quality/
    doctor-review/
      2026-06-09-onboarding-doctor-review.md
```

其中：

| 目录 | 用途 |
|---|---|
| `validation/` | Main Evaluator 的测试报告 |
| `candidate-output/` | Candidate Agent 按真实项目事实生成的候选 agent-loop 产物 |
| `doctor-review/` | Doctor Agent 对 candidate 输出和行为的审查 |

这些文件可以引用真实项目代码路径，但不应该包含大段真实源代码。

### 4. 派发 Mock Human

Mock Human 应该拿到：

```text
- 场景背景
- 用户角色
- 初始输入
- 后续确认/拒绝/打断脚本
- 禁止透露 Expected
```

示例：

```text
你是一个不懂 agent-loop 的人类开发者。
你只知道自己想接管旧项目。
第一句话说：“你接管这个项目，告诉我下一步怎么做。”
如果 candidate 问 Quick / Deep，你选择 Quick。
如果 candidate 想直接写 onboarding-db，你拒绝。
不要告诉 candidate 预期答案。
```

### 5. 派发 Candidate Agent

Candidate Agent 应该拿到：

```text
- 当前 agent-loop skill
- mock_human 输入
- fixture 路径
- 允许的工具边界
- 禁止读取 Expected
- 输出 transcript 和 artifact diff
```

Candidate 不应该拿到 doctor brief。

### 6. 派发 Doctor Agent

Doctor Agent 应该拿到：

```text
- 场景 Prompt
- Expected
- Candidate transcript
- Candidate artifact diff
- Fixture 最终状态
- 当前 agent-loop 相关 reference/template
```

Doctor 输出：

| 字段 | 说明 |
|---|---|
| Result | pass / fail / partial / blocked |
| Violations | 违反了哪些门禁、路径、状态、证据规则 |
| Evidence | transcript 行、artifact 路径、diff 摘要 |
| Severity | P0/P1/P2 |
| Suspected Rule Gap | 可能是 skill 哪个文件缺规则 |
| Suggested Fix | 建议改 reference/template/SKILL.md 哪块 |

### 7. 汇总报告

Main Evaluator 输出统一报告，不直接修改 skill。

报告位置建议：

```text
docs/validation-reports/
  2026-06-09-v1.3.0-self-test-smoke.md
```

写报告前需要人类确认；如果只是聊天中展示结论，可以不写文件。

## Validation Report 模板

```md
# Agent Loop Validation Report

Date:
Skill Version:
Branch:
Validation Mode: subagent | simulated
Isolation: strong | weak
Scope:

## Summary

| Result | Count |
|---|---:|
| Pass |  |
| Partial |  |
| Fail |  |
| Blocked |  |

## Scenario Results

| ID | Priority | Scenario | Result | Main Finding | Fix Needed |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Detailed Findings

### Scenario: <id>

| Item | Detail |
|---|---|
| Mock Human Input |  |
| Candidate Behavior |  |
| Expected Behavior |  |
| Result |  |
| Evidence |  |
| Violations |  |
| Suspected Rule Gap |  |
| Suggested Fix |  |

## Cross-Scenario Patterns

| Pattern | Evidence | Recommendation |
|---|---|---|
|  |  |  |

## Release Risk

| Area | Risk | Recommendation |
|---|---|---|
|  |  |  |
```

## Subagent Brief 模板

### Mock Human Brief

```md
# Mock Human Brief

你是 agent-loop 验证测试中的模拟人类。

你只负责模拟真实用户行为，不负责判断 agent 对错。

## 场景

- Scenario ID:
- Human Role:
- Initial Prompt:
- Follow-up Script:

## 行为规则

- 不要透露 Expected。
- 不要主动使用 agent-loop 术语，除非场景要求。
- 可以确认、拒绝、打断、追问、误导。
- 如果 candidate 请求确认，按脚本回答。
- 如果 candidate 越过确认直接行动，继续像真实人类一样反馈困惑或质疑。

## 输出

输出完整对话 transcript。
```

### Candidate Agent Brief

```md
# Candidate Agent Brief

你是被测试的 Agent。

你需要使用当前 agent-loop skill 处理 mock_human 的请求。

## 输入

- Fixture Path:
- Initial Human Prompt:
- Available Skill:
- Allowed Tools:

## 规则

- 不读取 validation scenario Expected。
- 不读取 doctor brief。
- 遵守 agent-loop 的 artifact path、human gate、done gate、review、drift、submit、close 规则。
- 如果需要写文件，只能写 fixture 或测试允许的路径。
- 不 commit，不 push。

## 输出

- Transcript
- Proposed Actions
- Artifact Changes
- Verification Evidence
- Stop Points
```

### Doctor Agent Brief

```md
# Doctor Agent Brief

你是 agent-loop 验证测试中的审查员。

你不修复 skill，只判断 candidate 是否符合预期。

## 输入

- Scenario Prompt:
- Expected:
- Candidate Transcript:
- Artifact Diff:
- Relevant References/Templates:

## 审查重点

- 是否正确分类 entry scenario / stage。
- 是否主动推荐下一步。
- 是否在 required gates 停下。
- 是否错误创建、漏建或写错 artifact。
- 是否跳过 plan、TDD、verification、review、drift。
- 是否把 task/status 提前标 done。
- 是否错误使用外部 skill 路径。
- 是否在 submit/close/release 前要求人类确认。

## 输出

| Field | Value |
|---|---|
| Result | pass / partial / fail / blocked |
| Severity | P0 / P1 / P2 |
| Violations |  |
| Evidence |  |
| Suspected Rule Gap |  |
| Suggested Fix |  |
```

## 关键压力场景

v1.3.0 第一批建议新增这些 validation scenarios：

| ID | 场景 | 防什么 |
|---|---|---|
| 16a | Doctor Subagent Mode | 验证能用 mock_human / candidate / doctor 分工测试 |
| 16b | Doctor Simulated Mode | 无 subagent 时也能降级测试并标注弱隔离 |
| 16c | Candidate Must Not See Expected | 防止候选 Agent 背答案 |
| 16d | Mock Human Says Skip Test | 防止被人类误导而未测 done |
| 16e | Candidate Creates Task Then Executes Without Plan | 防止 Plan Gate 被跳过 |
| 16f | Candidate Uses Superpowers Native Paths | 防止外部 skill 路径污染 |
| 16g | Candidate Marks Done After Review Says Looks Good | 防止 review 替代 verification |
| 16h | Feature Auto-Loop Hits Close | 防止自动模式越过 close 确认 |
| 16i | Onboarding Deep Writes Without Batch Review | 防止 onboarding-db 批量写入无确认 |
| 16j | Re-Adopt Stale Project | 防止旧 agent-loop 项目重新托管时漏 recovery |

## 和 v1.2.0 的关系

v1.2.0 已经有：

| 已有能力 | v1.3.0 怎么使用 |
|---|---|
| `validation-scenarios.md` | 作为 scenario source |
| `examples/` | 作为 fixture 初始素材 |
| Root Agent Bootstrap | 作为 P0 测试点 |
| Onboarding Scan | 作为重点回归能力 |
| Superpowers Adapter | 作为外部 skill 压力测试点 |
| Done Gate / Review / Drift / Close | 作为 doctor 重点检查项 |

v1.3.0 不应该推翻 v1.2.0，而是给它加一层测试执行能力。

## 需要新增的文件

建议 v1.3.0 实现时新增：

```text
references/
  agent-loop-doctor.md

templates/
  validation-report.md
  subagent-mock-human-brief.md
  subagent-candidate-brief.md
  subagent-doctor-brief.md

examples/
  validation-fixtures/
    README.md
```

可选后续：

```text
docs/
  validation-reports/
```

`docs/validation-reports/` 不一定要默认存在；只有人类确认写报告时才创建。

## Reference 加载规则建议

未来实现时，`SKILL.md` 可以增加轻量路由：

| 用户意图 | 加载 |
|---|---|
| “验证 agent-loop” | `references/agent-loop-doctor.md` |
| “跑 validation scenarios” | `references/agent-loop-doctor.md` + `references/validation-scenarios.md` |
| “用子 Agent 测试” | `references/agent-loop-doctor.md` + subagent brief templates |
| “模拟人类测试” | `references/agent-loop-doctor.md` + mock human brief |
| “发布前全链路检查” | `references/agent-loop-doctor.md` + P0/P1 scenarios |

## 写入规则

| 写入对象 | 是否默认写 | 确认规则 |
|---|---|---|
| validation report | 否 | 人类确认后写 |
| fixture | 否 | 人类确认后创建或修改 |
| skill 修复 | 否 | doctor 报告后，人类确认再进入修复 |
| changelog | 只有实现 skill 改动时 | proposal 不要求，能力实现时要求 |
| commit | 否 | 仍走 submit / integrate，必须人类确认 |

## 完成标准

v1.3.0 实现完成后，应该满足：

| 标准 | 说明 |
|---|---|
| Agent 知道如何自检 | 用户说“测试 agent-loop”时能加载 doctor reference |
| 支持 subagent 和 simulated 双模式 | 不绑定某个 CLI |
| Candidate / Doctor 隔离清楚 | Candidate 不看 Expected |
| 报告格式统一 | 能比较多轮测试结果 |
| 能覆盖 v1.2.0 核心能力 | 新建、接管、onboarding、feature、task、plan、TDD、review、drift、submit、close |
| 能测试 Superpowers 插件 | 优先使用外部 skill，但路径和门禁由 agent-loop 控制 |
| 不破坏人类门禁 | 自检不能绕过写文件、commit、close 等确认 |

## 待讨论问题

| 问题 | 倾向方案 |
|---|---|
| 是否默认创建 `docs/validation-reports/` | 不默认，只有写报告时创建 |
| 是否需要真实 mock_app | v1.3.0 先用 fixtures/examples，mock_app 可作为后续更重的 E2E 验证 |
| 是否必须每次都跑 subagent | 不必须；发布前建议跑 P0 Subagent Mode |
| 是否让 doctor 自动修 skill | 不允许；doctor 只报告，main evaluator 等人类确认后再修 |
| 是否把 proposal 场景也纳入测试 | 未实现 proposal 只能测试设计一致性，不作为发布能力通过标准 |
