# Agent Loop v1.4.0 Human-Guided Branch Management 全量验证报告

验证日期：2026-07-15
验证分支：`alpha/v1.4.0`
当前 Skill 元数据：`1.4.0`
版本开发线：`v1.4.0`
审计对象：当前未提交工作区中的 Human-Guided Branch Management 实现、Proposal、Implementation Plan、focused contract 与验证证据
基线 HEAD：`5c6112c91316dc00160184b321e4ded5826fcb51`
当前标准 Git 引用快照 SHA-256：`8cd849b94efdd5374409c2832b54d0531e2d3d9526d60bc76c5743879fddeef4`（仅 `refs/heads`、`refs/remotes`、`refs/tags`）
平台声明：本轮在 macOS 本地完成文档、Ruby、Shell、Python 与 Git 检查；未运行新的 Windows CI，不声明 Windows 当前运行证据

## 1. 验证结论

总分：**99/100**
等级：**STRONG**
最终测试：**98/98 Python tests PASS；35/35 `tests/*.sh` PASS**
当前严重度：**Critical 0 / High 0 / Medium 0 / Low 0**

Proposal 的可选 Human-Guided Branch Management 已形成完整运行闭环：Agent 先检查仓库原生策略与 Git 事实，只在人类询问、规则混乱、Target Release Context 不清或客户隔离有风险时推荐；不在每次 branch create/switch 前强制重做策略访谈。推荐必须经 Strategy Adoption Gate 才能成为持久策略；一条明确开发分支的创建或切换由 Branch Action Gate 单独授权；策略采用、计划批准与自动模式均不授权任何 Git mutation。

实现没有新增 canonical stage、message intent、默认 `.agent-loop/branches/`、Bug Management、worktree / branch memory merge 或 executable schema。人类已明确批准版本提升，Skill、plugin、README、Usage 与 root managed-block revision 现已统一为 `1.4.0`；`CHANGELOG.md` 使用 `1.4.0 — 2026-07-15`。

当前结论是：**实现、版本同步与验证已完成；人类已请求进入 Submit / Integrate，但仍要在 staged diff 摘要后通过最终 commit Human Gate。push、tag、PR、merge、release、publish 与 Agent CLI 安装副本同步未获授权。**

## 2. 六域语义审计

| 审计域 | 结果 | 分数 | 本轮结论 |
|---|---|---:|---|
| Logic Correctness | PASS | 99 | Branch Strategy Check 为内部方法；branch-specific Stop 仅在已采用策略或 versioned/customer delivery 适用；sealed、customer isolation 和 action gates 无绕过 |
| Autonomy | PASS | 99 | 人类询问时推荐；规则清晰时保留 existing-project；不因普通 create/switch 强制重做策略访谈 |
| Project Entry / Evidence Graph + DDD Onboarding | PASS | 99 | Project Entry / Project Entry Scan 仅增加只读检查；`not-needed` 简单路径无需 Target Release Context/Target Branch 也能继续 |
| Development / Test Workflow | PASS | 99 | Technical Design、Plan、Execute、Drift、Memory、Submit 使用同一 Branch Context；明确 Branch Action Gate 只授权一次精确 create/switch；Auto Mode 在 Git 动作前停止 |
| Memory | PASS | 99 | `project.md` 只保存确认的长期策略；`declined` 使用 `Profile: not-applicable` 和具体 Decline Reason，不把被拒方案写成现行规则 |
| Recommendation | PASS | 99 | canonical root 仅有一句英文 router，项目可按 guidance 本地化；Human Review 同时列出 requested 与 explicitly-not-authorized actions |

加权结果为 99。没有未解释的 Critical、High 或 Medium。

## 3. RED 基线与 TDD 证据

### 3.1 既有回归基线

在增加新 focused contract 前运行：

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
98/98 PASS

for test_file in tests/*.sh; do bash "$test_file"; done
34/34 PASS
```

这证明新能力开始前没有吸收既有失败。

### 3.2 初始 focused RED

先创建 `tests/validate-branch-management-strategy.sh`，在运行规则修改前执行，真实失败为：

```text
FAIL: missing required file: references/branch-management.md
exit 1
```

完整初始 RED 证据保存在：

```text
docs/reports/agent-loop-v1.3.0-branch-management-red-baseline-2026-07-15.md
```

### 3.3 语义审计追加 RED

首次 GREEN 后，计划逐项审计发现关键词 contract 尚未证明以下细节：

- `plan.md` 应引用 `notes.md` 的 Current Branch Context，而不是复制完整易变状态；
- root 指定提醒应位于 managed ownership block；
- Execute 必须显式重检 Current Branch Context；
- Human Review 必须展示 observed policy、verification/review/drift 和 remaining blocker；
- Current Branch Context 枚举必须与 Proposal 一致；
- runtime 事实优先级必须与详细 reference 一致；
- 压力场景必须包含三项 adversarial authorization/drift cases。

回归断言先扩展，分别出现预期 RED，包括：

```text
FAIL: templates/plan.md missing branch-management contract: Current Branch Context Evidence:
FAIL: references/validation-scenarios.md missing branch-management contract: Strategy Adoption Does Not Authorize Branch Creation
FAIL: templates/notes.md missing branch-management contract: Branch Class: main | standard-release | customer-release | development | unknown
FAIL: SKILL.md missing branch-management contract: branch class or unique Target Branch is unknown
```

随后只修实现/模板/场景，没有删除或弱化 Proposal invariant。

### 3.4 Human Review Repair RED

Human Review 后先扩展同一 focused contract，再修正运行规则。四层缺口按顺序产生了可重现 RED：

```text
FAIL: SKILL.md missing branch-management contract: when an adopted Branch Strategy or versioned/customer delivery applies
FAIL: SKILL.md missing branch-management contract: branch creation, switching, deletion, push, or tag
FAIL: references/branch-management.md missing branch-management contract: existing-project | human-guided-release | not-applicable
FAIL: root AGENTS must contain the exact branch-management reminder once; found 0
```

修复分别封闭了：简单项目被全局 Stop 误伤、Auto Mode/create-switch 授权语义不全、`declined` 保留虚假现行 Profile、canonical root 绑定中文。人类明确未要求“每次 branch create/switch 前强制推荐”，因此 focused contract 还对该扩张做了 negative assertion。完整过程见 RED 基线报告。

### 3.5 Independent Review Follow-up RED

独立只读 Review 在初次 repair GREEN 后发现 1 个 High 和 1 个 Medium 历史问题：

- High：Plan 与 Submit / Integrate 的详细 stage/checklist 仍可能对 simple `not-needed` 无条件要求 Target Release Context/Target Branch；
- Medium：Implementation Plan 的“Tasks 0-7 complete”与未勾选的 tracking checkbox 矛盾。

先扩展 focused contract，确认真实 RED：

```text
FAIL: references/branch-management.md missing branch-management contract: When an adopted Branch Strategy or versioned/customer delivery applies, if Target Release Context or the unique Target Branch is unclear
FAIL: templates/plan.md missing branch-management contract: For a confirmed simple `not-needed` path, set branch-specific fields to `not-applicable`
```

然后将 applicable-context 限定同步到 detailed reference、Plan/Drift/Submit checklists、stage guide、Submit / Integrate reference 和 plan template，并将 simple `not-needed` 的分支专属检查显式记为 `not-applicable`。Implementation Plan 也按历史证据回填完成勾选。修复后 focused contract 重新 GREEN，独立 Review 复核未再发现 Critical/High/Medium，当前严重度回到全 0。

### 3.6 Version Alignment RED

人类明确批准升级至 `1.4.0` 后，先把版本 contract 改为期望 `1.4.0`，在生产文档修改前得到真实 RED：

```text
FAIL: expected 'Version: 1.4.0' in SKILL.md
```

完成主版本字段同步后的残留扫描又发现两处当前口径仍停留在升级前状态。先补断言，再得到 RED：

```text
FAIL: Usage.md missing required text: 当前 1.4.0 使用的是
FAIL: expected 'block-version:1.4.0-20260715' in CHANGELOG.md
```

随后将 Usage 当前版本说明、1.4.0 Changelog 的 root revision 与版本授权说明修正，并保持历史 v1.3.0 报告、发布证据和本轮 pre-bump RED 基线不变。两个版本 contract 均重新 GREEN。

## 4. GREEN 与全量回归

Focused GREEN：

```text
PASS: Human-Guided Branch Management optional profile, gates, artifacts, diagram, and scope contract is complete
```

最终全量回归：

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
Ran 98 tests
OK

for test_file in tests/*.sh; do bash "$test_file"; done
35/35 PASS
```

受影响回归中曾发现 root checker fixture 仍替换旧 revision，导致 stale fixture 不再 stale。根因是同日 managed-block revision 的机械更新没有同步该 `sed` 输入；修正 fixture 后：

```text
PASS: root AGENTS block checker contract is complete
tests.test_root_agents_blocks: 8/8 PASS
```

该修复只恢复测试输入的 stale 语义，没有改变 checker 行为。

Human Review repair 的受影响套件也独立通过：

```text
focused branch contract: 1/1 PASS
affected Python root tests: 8/8 PASS
affected Shell contracts: 8/8 PASS
semantic repair audit: PASS
managed blocks: 13/13 at block-version:1.4.0-20260715
Proposal / Usage Mermaid equality: PASS
```

## 5. Human-Guided Branch Management 十五项压力场景

`references/validation-scenarios.md` 的 15/15 场景均记录 Evidence、Recommendation、Required Human Gate、Forbidden Action 与 Next Stage，并由 focused contract 检查结构和关键对抗场景。

| # | 场景 | 结果 | 核心判断 |
|---:|---|---|---|
| 1 | 标准版本聚合多个 Feature | PASS | 分支数量由人类范围决定；create/merge/push 分别 gated |
| 2 | 版本只有一个 work item | PASS | 不为对称性强拆多个开发分支 |
| 3 | 客户功能只进入匹配客户 release | PASS | customer slug、version、unique target 均必需 |
| 4 | 同 topic 多客户并行 | PASS | customer context 不折叠、不互推 |
| 5 | sealed v1.0.0 修复 | PASS | 阻止同版本写入，推荐人类确认的新 patch |
| 6 | 客户升级标准基线 | PASS | Upgrade Gate，不自动覆盖旧客户版本 |
| 7 | 已有清晰 trunk-based/native 策略 | PASS | 保留 existing-project，不强迁移 |
| 8 | `feature/user-login` 缺 target | PASS | 报告缺口、给一个推荐、问一个 blocker，不 rename/switch |
| 9 | 合并后清理 | PASS | merge evidence + Cleanup Gate；release aggregation branch 保留 |
| 10 | 客户能力通用化 | PASS | 回到产品/requirement/feature 或 Bug Flow-back，不整条反向合并 |
| 11 | 单 main 简单项目 | PASS | 可确认 `not-needed`，不制造 release/customer branches |
| 12 | Memory Merge 消费 Branch Context | PASS | 只提供未来输入，不实现 memory merge |
| 13 | 采用策略试图授权 branch create | PASS | Strategy Adoption 不复用为 mutation grant |
| 14 | external finishing helper 试图 merge/delete/push | PASS | helper 只提供 hygiene evidence，Agent Loop gate 仍拥有动作权限 |
| 15 | Git reality 与 accepted/native policy 冲突 | PASS | Drift Check + 一个最小人类决策，不推断赢家 |

## 6. 分支能力关键不变量

### 6.1 Optionality 与采用

- `references/branch-management.md:3-11` 定义可选 profile，并禁止强制迁移；
- `references/runtime.md:99-133` 定义 Branch Strategy Check、证据顺序、推荐触发、策略状态和适用范围；
- `SKILL.md:166` 只保留简洁路由；
- `references/validation-scenarios.md:3089-3271` 覆盖 clear existing、simple、adoption rationalization 与 drift。

结论：推荐不是默认 Git Flow，清晰 existing-project 与轻量 not-needed 路径可达。`not-needed` 路径不需 Target Release Context 或 Target Branch；只有 adopted/versioned/customer 上下文才启用 branch-specific fail-closed Stop。

### 6.2 Adoption 与 action authorization 分离

- `references/branch-management.md:52-82` 定义 Strategy Adoption Gate 与 recommendation/adoption non-authorization；
- `references/human-review-summary.md:296-313` 同时显示 requested action、explicitly not authorized、risk/blocker 和 human decision；
- `references/workflow-checklists.md:749` 明确 create/switch/merge/delete/push/tag/release/publish 均保持单独 gate；
- `references/external-skill-adapters.md:211-223` 禁止 finishing helper 扩大授权。

结论：采用策略、接受计划、Feature Auto-Loop / Task Auto-Run 或 helper 成功均不能复用为 Git mutation 权限。Branch Action Gate 仅确认一条精确开发分支的 create 或 switch，不外溢到 merge/delete/push/tag/release/publish。

### 6.3 命名、unique target、sealed 与 customer isolation

- 标准 aggregation：`release/v<semver>`；
- 客户 aggregation：`customer/<customer>/v<semver>`；
- 标准 development：`<work-type>/v<semver>/<topic>`；
- 客户 development：`<work-type>/<customer>-v<semver>/<topic>`；
- work type 仅为 `feature | bugfix | hotfix`；
- Target Release Context 必须唯一映射到 aggregation branch；
- `released / sealed` 不再接收相同版本工作；
- 客户 release 不得整条反向进入 `main`、标准 release 或其他客户线。

结论：命名、生命周期和合并方向在 design/runtime/reference/stage/checklist/submit/scenario 中一致。

### 6.4 Artifact ownership

- `templates/project.md:92-118` 保存确认后的 Branch Strategy 与 Current Work Target Release Context；
- `templates/notes.md:9-25` 保存完整 Current Branch Context；
- `templates/plan.md:17-24` 只引用 notes context 并重复 target/sealed/isolation 结论；
- `references/artifact-rules.md` 与 `references/project-memory-mode.md` 在 simple/enterprise 模式下保持相同 durable/volatile 分界；
- 没有创建默认 `.agent-loop/branches/`。

结论：长期策略不会被频繁 Git 状态污染，计划也不会复制第二份完整 branch state。

`declined` 不保留被拒绝的策略为当前 Profile：必须记录 `Profile: not-applicable` 和具体 `Decline Reason`。`accepted` 与 `not-needed` 仍保持各自的有效 profile 语义。

### 6.5 Root guidance 与 canonical stage

- root template 只保留一句 canonical English router，位于 managed ownership block；非英文项目可根据 `references/project-guidance.md` 本地化；
- 13/13 managed blocks 使用 `block-version:1.4.0-20260715`；
- root template 不包含命名 grammar、Adoption Status、sealed lifecycle 或 gate matrix；
- runtime `Stage Order` 没有 `Branch Strategy Check`、`Strategy Adoption Gate`、`Release Scope Gate` 或 `Customer Scope Gate` 行；
- Proposal 与 Usage Mermaid 内容逐字节相等。

结论：root 仍是 navigation，详细规则由 published reference 拥有，Branch Strategy Check 未变成 canonical stage。

## 7. 全仓库代表性压力路径

35/35 Shell contracts 与 98/98 Python tests 继续覆盖 full-validation method 要求的既有路径：

- 复杂 Requirement -> Concept Foundation / Requirement Product Model -> Decision & Design -> Feature Spec；
- reasoned `concept-foundation-not-needed` 简单需求路径；
- Product Brief Source Gate；
- Delivery Contract create/accept/breaking-change Human Gate；
- TDD RED 与非行为型 `not-applicable`；
- Active Feature、Pause、Resume、Close、Feature Follow-up；
- 多 Delivery Phase 的 `partially-implemented` roll-up；
- accepted ADR 与 requirement/implementation drift；
- Follow-up investigate-first；
- Submit / Integrate verification/review/drift/blocker 顺序；
- stale-memory、root guidance、Project Entry 与 Re-Adopt；
- Chat 不创建 requirement/feature/onboarding artifacts；
- archive locator、rehydrate 与恢复 fail-closed。

新增分支检查没有改变上述 stage order、state lifecycle 或 gate ownership。

## 8. 机械检查与 Git 副作用

| 检查 | 结果 |
|---|---|
| `SKILL.md` + `agents/openai.yaml` YAML parse | PASS |
| `plugin.json` JSON parse | PASS |
| `python3 -m compileall -q scripts tests` | PASS |
| Shell `bash -n` | PASS（36 files） |
| Ruby `ruby -c` | PASS（5 files） |
| Markdown fence balance | PASS（204 files，包含本报告） |
| `git diff --check` | PASS |
| repository-root `.agent-loop/` | 不存在 |
| 当前分支 | `alpha/v1.4.0` |
| HEAD | 与 RED 基线一致 |
| 标准 ref snapshot | `8cd849b94efdd5374409c2832b54d0531e2d3d9526d60bc76c5743879fddeef4` |
| 标准 ref reflog | 本轮无 `refs/heads`、`refs/remotes`、`refs/tags` 变更 |

版本核对：

```text
SKILL.md Version: 1.4.0
plugin.json version: 1.4.0
README.md Current version: 1.4.0
Usage.md 版本: 1.4.0
CHANGELOG.md: 1.4.0 — 2026-07-15
```

未创建、切换、合并、删除或 push 任何测试分支；未改变标准 Git refs；未创建 target-project `.agent-loop/`。

原 RED 报告的 raw all-ref hash 包含 Codex 桌面自动维护的 `refs/codex/turn-diffs/*`。该类编辑器内部快照会在文件编辑期间变化，不代表 branch/tag/remote mutation，所以最终证据改为对 `refs/heads refs/remotes refs/tags` 的标准快照和 reflog 检查。HEAD 全程保持 `5c6112c91316dc00160184b321e4ded5826fcb51`。

## 9. Proposal 分阶段符合性

| Proposal 阶段 | 状态 | 落地证据 |
|---|---|---|
| Phase 1: Branch Strategy Contract | PASS | detailed reference、design/runtime authority、SKILL route、concepts、naming/lifecycle/gates |
| Phase 2: Project Memory And Stage Integration | PASS | project/notes/plan ownership，Entry/Plan/Execute/Drift/Memory/Submit 协调 |
| Phase 3: Human Guidance | PASS | root 一句 reminder、Usage 完整 Mermaid/触发方式、README、Human Review Summary |
| Phase 4: Regression And Pressure Validation | PASS | focused RED/GREEN、15 scenarios、98/98 Python、35/35 Shell、六域审计与机械检查 |

Proposal 完成标准逐项结果：

1. 分类、命名、状态、方向跨 authority/reference 一致：PASS；
2. standard/customer aggregation branches 明确：PASS；
3. development branch 携带 work type、target、topic：PASS；
4. 分支数量由人类决定：PASS；
5. 正式版本 sealed：PASS；
6. 客户隔离与通用化安全回流：PASS；
7. release branch 保留、temporary cleanup gated：PASS；
8. create/switch 由精确 Branch Action Gate 授权，merge/delete/push/tag/release/publish 仍保持各自 gate：PASS；
9. project durable / feature volatile ownership：PASS；
10. Usage 完整图：PASS；
11. clear/simple 项目不强制迁移：PASS；
12. 无 Bug Management / Memory Merge / default branches artifact 扩展：PASS。

## 10. 未解决问题、剩余风险与范围漂移

当前未解决逻辑问题：**无**。

剩余风险不是当前缺陷：

- 这是规则、模板和 contract 能力，不是 Git automation；真实目标项目仍需要 Agent 依据仓库证据运行 Branch Strategy Check；
- Windows 未在本轮重新执行，因此只声明 macOS 本地证据；本能力没有新增平台相关执行器；
- 后续 Bug Management 与 worktree / branch memory merge 只能消费本轮 Branch Context，仍需各自 Proposal 和 Human Gate；
- 真实 branch protection、CI policy、CODEOWNERS 与 hosting provider 设置不在本轮范围。

范围漂移检查：

- 未新增 canonical stage 或 message intent；
- 未新增 `.agent-loop/branches/`、YAML/JSON schema 或 branch database；
- 未实现 Bug Management；
- 未实现 worktree / branch memory merge；
- 已按人类明确批准将 skill version 从 `1.3.0` 统一提升为 `1.4.0`；
- 未创建真实 release/customer/feature/bugfix/hotfix refs；
- 未修改 root maintainer `AGENTS.md`；
- 当前报告生成时尚未 commit、push、tag、PR、merge、release、publish 或同步 Agent CLI 安装副本。

## 11. 未采纳或降级意见

- 未把完整 grammar/lifecycle/gate table 放入 root `AGENTS.md`，因为 root 只拥有一句 navigation reminder；
- 未把 Branch Strategy Check 加入 canonical Stage Order，因为它是 Project Entry/Plan/Drift/Submit 内部方法；
- 未把 accepted strategy 当作 Git action grant，因为采用与 mutation 必须分离；
- 未为简单项目自动创建 release/customer branches；
- 未为 branch state 创建新的持久目录或 executable schema；
- 未使用真实分支操作做测试，focused contract 通过文档结构、negative scope、stage extraction、Mermaid equality 与压力场景验证能力。

## 12. 推荐下一阶段

推荐下一阶段：**Submit / Integrate final commit Human Gate**。

人类评审重点：

1. 可选推荐与 existing/simple non-migration 是否符合预期；
2. strategy adoption 与每个 Git action gate 的分离是否足够清晰；
3. standard/customer naming、sealed 和 customer isolation 是否完整；
4. `project.md` 与 feature context ownership 是否可长期维护；
5. root 一句 reminder 与 Usage 完整图的所有权是否合理。

在 staged diff 和验证摘要后等待人类最终 commit 确认。即使 commit 被批准，也不执行 push、tag、PR、merge、release、publish 或 Agent CLI 安装副本同步。
