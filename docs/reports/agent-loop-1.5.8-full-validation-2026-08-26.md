# Agent Loop 1.5.8 全量验证与六域评分报告

## 验证摘要

| 项目 | 结果 |
|---|---|
| 验证开始 / 完成 | 2026-08-26 / 2026-08-27（Asia/Shanghai） |
| 仓库 | Agent Loop Skill 源码仓库 |
| 分支 | `alpha/v1.5.8` |
| HEAD | `a25fec3bdd1558398df8870393e90e8d808cfc35` |
| 审计对象 | 上述 HEAD 加 Human-confirmed dirty worktree |
| 最终全量输入 | 42 个 tracked 修改、5 个 untracked 文件，共 47 个路径 |
| 最终全量输入摘要 | `beb56d7c187b265761d33c8bd575dccad5614d180b18ed5962bec4cded215294` |
| 实际环境 | macOS Darwin 25.5.0 arm64；Python 3.14.5；Ruby 2.6.10 |
| Shell 全量 | `53/53 PASS`，约 11 秒 |
| Python 全量 | `420/420 PASS`，81.940 秒 |
| 最终评分 | **96/100 — STRONG** |
| 当前严重问题 | Critical 0；High 0；Medium 0；Low 1 |

结论：Direct Edit Fast Path 与 Human-confirmed Full Test Run 能力在当前工作区形成一致闭环，可进入最终 Human Review。该结论不授权 Commit、Push、Tag、PR、Merge、Release、Publish、Seal 或 installed Skill 同步。

## Human-confirmed Full Run

人类先确认了初始全量签名。第一次 Shell 全量发现一处真实 RED；修复改变输入后，Agent 没有静默重跑，而是展示新的分支、HEAD、dirty inventory、环境和摘要，再取得一次性确认。最终确认绑定：

```text
Branch: alpha/v1.5.8
HEAD: a25fec3bdd1558398df8870393e90e8d808cfc35
Dirty paths: 42 tracked + 5 untracked
Worktree digest: beb56d7c187b265761d33c8bd575dccad5614d180b18ed5962bec4cded215294
Environment: Darwin 25.5.0 arm64 / Python 3.14.5
```

执行命令：

```bash
for test_file in tests/*.sh; do
  bash "$test_file"
done

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'
```

该授权已执行并消费；任何重跑均需新的当前事实与 Human confirmation。

## RED → GREEN 证据

### RED 1：Memory/Git Gate 顺序测试误报

初始 Shell 全量出现：

```text
FAIL: runtime memory/Git gate order is incorrect
```

根因不是 Gate 顺序倒退。`tests/validate-post-merge-memory-reconciliation.sh` 使用全文件 `text.find("Push Gate")`，而 1.5.8 合法地在更前面的 Push-triggered CI 说明中使用同名词，导致断言误取第一个词面位置。修复将断言限制到 `## Memory After Code Integration` 的完整顺序链：

```text
Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate
-> Push Gate -> Release Gate -> Source Branch Cleanup Gate
```

专项 GREEN：`PASS: Post-Merge Memory Reconciliation contract is complete`。

### RED 2：并行语义审计发现跨文件冲突

三位 Human-authorized 只读子 Agent 分别审计：

- Logic Correctness + Autonomy；
- Project Entry / Onboarding + Memory；
- Development / Test Workflow + Recommendation。

主 Agent 对候选发现逐项复核，没有直接采信子 Agent 结论。确认并修复：

1. root Gateway 将 active Feature ownership 与 closed/recent Feature Follow-up 混写；
2. validation/Usage 将计划跨会话错误导向 Lightweight，违背既有 Feature hard trigger；
3. Gate 2 场景没有明确绑定实现后的 final-input rule；
4. Proposal 允许的显式 bounded retry 没有一致投影到 Human docs、root 与 Submit；
5. Project Entry 没有明确“已具体授权的 Direct Edit 不重复询问”；
6. root/projection tests 仍固定旧路由和旧 CI 文案。

新增 focused 断言先因缺少新契约而失败，再同步 runtime-derived references、root projection、人类文档、场景和测试。最终 focused GREEN：11 个受影响 Shell contracts 通过；指定 Python suites 共 61 tests 通过。

### Review finding disposition

| 候选发现 | 主审结论 | 处理 |
|---|---|---|
| bounded retry 与 one-run 冲突 | Proposal 明确允许同一决定预先限定 count/condition；不是功能冲突，但投影不完整 | 对齐 runtime/design/root/Human docs/Submit；维护仓库明确采用更严格的每次重确认规则 |
| active Feature 首跳冲突 | 真实 | root 仅把 closed/recent ownership 导向 Follow-up；active ownership 留在 Active Feature Guard |
| planned cross-session 同时进入 Lightweight/Feature | 真实 | 区分当前会话持久控制/意外中断与 planned multi-session/handoff；后者保持 Feature hard trigger |
| Gate 2 current inputs 可跨实现复用 | 真实 | 正向场景必须有 clearly bound final-input rule；输入不匹配仍过期 |
| Project Entry 对 Direct Edit 二次确认 | 真实投影缺口 | 具体请求通过 Assessment 后不再增加 route confirmation |
| Direct Edit 未独立 mutation 所有 Project Entry 前置 | Low 覆盖缺口，不是当前运行冲突 | 保留为残余风险；通用 runtime/root/project tests 当前覆盖这些前置 |

## 最终全量与机械检查

### Executable regression

| 验证 | 结果 |
|---|---|
| `tests/*.sh` | 53/53 PASS；无 `FAIL` 输出 |
| `python3 -m unittest discover` | 420/420 PASS |
| Direct Edit focused mutation contract | PASS |
| Post-Merge Memory ordering focused contract | PASS |
| root block refresh/checker/lossless projection | PASS |

### Mechanical

| 检查 | 结果 |
|---|---|
| `SKILL.md` YAML | PASS |
| `plugin.json` JSON | PASS |
| 全部 Shell `bash -n` | PASS |
| `git diff --check` | PASS |
| 29 个 changed Markdown fence balance | PASS |
| root managed blocks | 13/13；统一 `1.5.8-20260826.1`；181 行 |
| 当前版本断言 | `SKILL.md` / `plugin.json` / README / Usage 均为 1.5.8 |
| 禁止项搜索 | 仅命中负向测试与“禁止创建”规则；未发现 Direct Edit Mode/Status/Lifecycle、默认目录或 skip/no-verify 能力 |

机械检查过程中，首个 Markdown 命令使用了 Ruby 2.7 的 `filter_map`，在 Ruby 2.6 上报 `NoMethodError`；改用 Ruby 2.6 兼容的只读等价实现后通过。另一次 forbidden 搜索命中测试的 `assert_not_contains` 与禁止性说明，经上下文核对为预期负向证据，不是产品违规。

## 六域评分

| 审计域 | 权重 | 分数 | 结果 | 结论 |
|---|---:|---:|---|---|
| Logic Correctness | 20% | 96 | PASS | 路由优先级、active/closed Feature、一次性 full-run、Gate 2 输入与 Gate 独立性一致 |
| Autonomy | 15% | 96 | PASS | Agent 能自主选择 Direct Edit/Lightweight/Feature/Bug；不确定时零写入并给一个推荐 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | 97 | PASS | Memory Recovery、root guidance、Project Skill、Onboarding 前置均未被 Direct Edit 绕过 |
| Development / Test Workflow | 20% | 97 | PASS | 最小 proof、TDD/Repair-First、Existing Test Obligation、full-run expiry 与 CI 边界闭环 |
| Memory | 15% | 95 | PASS | Direct Edit 零 artifact 不污染 memory；durable facts、planned continuation 与冲突恢复正确升级 |
| Recommendation | 15% | 97 | PASS | 阶段退出、拒绝全量后的 claim 收窄、Release blocker 与唯一 next action 清楚 |

加权总分：

```text
96×20% + 96×15% + 97×15% + 97×20% + 95×15% + 97×15%
= 96.35 -> 96/100
```

等级：**STRONG**。

## 24 个压力场景

| # | 场景 | 最终结果 |
|---:|---|---|
| 1 | 文档 typo 直接编辑 | PASS |
| 2 | 已确认 internal domain 替换 | PASS |
| 3 | Feature-local label tuning | PASS |
| 4 | 结构化 metadata parser check | PASS |
| 5 | 一行 public API/schema | PASS：退出 Direct Edit |
| 6 | external endpoint migration | PASS：进入 owning Feature/external route |
| 7 | explicit Bug | PASS：Bug Management 优先 |
| 8 | persistent recovery 与 planned cross-session 分流 | PASS：前者 Lightweight；后者 Feature |
| 9 | 新测试是唯一可靠证明 | PASS：退出 Direct Edit |
| 10 | minimum check 失败 | PASS：禁止 completion |
| 11 | unrelated dirty work | PASS：要求 exact attribution |
| 12 | Direct Edit 不授予后续动作 | PASS |
| 13 | 历史 Lightweight cards/scanner 不变 | PASS |
| 14 | Existing Test Obligation 保留 | PASS |
| 15 | 同一属性 tuning 只检查最终值 | PASS |
| 16 | business/runtime multiplier 非 cosmetic | PASS |
| 17 | Commit-only 不自动测试 | PASS |
| 18 | 新 full run 等 exact confirmation | PASS |
| 19 | Gate 2 明确绑定 final-input rule 不重复询问 | PASS |
| 20 | HEAD/input/target/environment 变化导致过期 | PASS |
| 21 | 拒绝 optional full 只收窄 claim | PASS |
| 22 | 拒绝 Release-required full 阻断 readiness | PASS |
| 23 | Push-triggered CI 披露且不本地重复 | PASS |
| 24 | manual CI rerun 与显式 bounded retry | PASS |

## Proposal 覆盖与边界

| Proposal 能力 | 证据 |
|---|---|
| Direct Edit 位于 persistent Lightweight 之前 | runtime/design/SKILL/root projection + focused contract |
| 全条件 eligibility 与 hard triggers | dedicated reference + stage/checklist/scenarios |
| zero artifact / no Plan / no new test | artifact/memory/helper/planning references + mutation tests |
| same-scope tuning 最终一次检查 | dedicated reference + stage guide + scenario |
| Active Feature 吸收 bounded edit | runtime + root Active Feature Guard + Feature-local section |
| Lightweight/Feature/Bug 升级 | runtime + corrected persistent/planned-session split |
| targeted evidence 默认 | runtime/design/human review |
| concrete Full Test confirmation | runtime/human review/Usage/root/maintenance method |
| one-run expiry 与 bounded retry | runtime + aligned Human/Submit projections；本仓库 stricter override |
| Commit/Push/CI/Release 独立边界 | submit/root/Usage/scenarios |
| no stage/status/mode/artifact/force/skip | focused negative checks |
| version 1.5.8 同步 | six version surfaces + 13 root revisions |

保留的 Human Gates：Product、ADR、Feature Gate 1/2、Task Done、Verification、Submit、Close、Commit、Push、PR、Merge、Tag、Release、Publish、Seal、External Action、Branch Action、Bug lifecycle、Delivery Contract、Checker repair 与 Subagent execution 均未被 Direct Edit 或 Full Test confirmation 替代。

## macOS 与 Windows 边界

- macOS：Shell、Ruby、Python、YAML、JSON、Markdown、root projection 和 Git mechanical checks 均为实际执行结果。
- Windows：本变更不新增 runtime executable；Windows 仅为 test-defined contract。规则要求 Agent 使用平台原生 parser/syntax/reference check，`py -3` 与 Windows path/shell/environment 构成不同 full-run signature。
- 未在真实 Windows 主机运行，因此不得声明 Windows 实机验证通过。

## 残余风险、范围漂移与停止条件

### Low

Direct Edit focused contract 尚未为 stale-memory、stale root guidance、matching Project Skill、sealed release 分别加入独立 mutation。当前 runtime precedence、root bootstrap、Project Skill tests、branch tests 和 memory tests 已证明这些前置仍存在，因此是未来回归加固项，不是当前 Gate 绕过。

### 范围漂移

- 没有新增 canonical stage、message intent、status、Mode、artifact family、runtime checker 或默认目录。
- 没有修改 Archive/Rehydrate、Full Memory Audit、exact plan hash、transaction journal、post-check、rollback 或 Checker Rescue 安全边界。
- 全量发现后只修复测试作用域和 Direct Edit/full-run 的协调投影；没有进入无关产品能力。

### 当前停止条件

- Phase 2 验证已经完成，停在最终 Human Review。
- 若当前行为文件、测试、HEAD、环境或全量命令变化，现有 full-run 证据不再支持新输入，需要重新判断验证范围。
- Commit、Push、Tag、PR、Merge、Release、Publish、Seal 和 installed Skill 同步仍未授权。

## Git 与发布状态

- 未 stage。
- 未 commit。
- 未 push。
- 未 tag、PR、merge、release、publish 或 seal。
- 未同步 installed Skill。
- 当前分支仍为 `alpha/v1.5.8`；稳定 `v1.5.8` 尚未创建。
