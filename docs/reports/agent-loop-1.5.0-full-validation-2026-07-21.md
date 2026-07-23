# Agent Loop v1.5.0 补充全量验证报告（Root AGENTS 无损瘦身）

## 1. 审计对象与边界

- 日期：2026-07-21
- 分支：`alpha/v1.5.0`
- Skill 版本：`1.5.0`（本验证不升级版本）
- 审计对象：Git tree `e07d50c` `refactor(v1.5.0): 无损瘦身 Root AGENTS 引导`；之后的工作区改动不属于本报告审计范围
- 改动性质：`templates/root-AGENTS.md` 从 224 行瘦至 170 行，实施方案为 `docs/proposal/v1.5.x/root-agents-lossless-slimming-implementation-plan.md`
- 验证方法：`docs/maintenance/full-validation-method.md`（六域语义审计 + 可执行回归基线）
- 报告定位：对 `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-21.1.md` 的补充问题复核；本报告记录修复前发现，不代表后续工作区状态
- 后续关闭证据：`docs/reports/agent-loop-v1.5.0-root-guidance-consistency-full-validation-2026-07-22.md`

## 2. 总分与定级

**总分：93 / 100，等级：STRONG**

- 机械基线：shell 测试 39/39 通过；Python 测试 221/221 通过（unittest discover）；`SKILL.md`/`agents/openai.yaml` YAML 解析 OK；`plugin.json` JSON 解析 OK；全部 `bash -n` OK；`git diff --check HEAD~1` OK
- Critical：0；High：0；Medium：1；Low：8（其中 2 个为瘦身前已存在）
- 定级约束检查：无 Critical（不得低于 FRAGILE 的限制不触发）；无未解释 High（STRONG 允许）；1 个 Medium 有明确修复路径，见第 4 节

## 3. 六域评分表

| 审计域 | 权重 | 结果 | 评分 | 加权 |
|---|---:|---|---:|---:|
| Logic Correctness | 20% | PASS | 93 | 18.60 |
| Autonomy | 15% | PASS | 94 | 14.10 |
| Project Entry / Onboarding | 15% | PASS | 94 | 14.10 |
| Development / Test Workflow | 20% | PASS | 95 | 19.00 |
| Memory | 15% | PASS | 93 | 13.95 |
| Recommendation | 15% | PASS | 90 | 13.50 |
| **合计** | 100% | | | **93.25 ≈ 93** |

六域语义审计由 6 个独立只读子 Agent 并行完成，主 Agent 对全部 Critical 候选与 Medium 发现逐一做了跨文件证据核对（含 `project-guidance.md:57` vs `:236`、`runtime.md:98,300,462` 的原文确认），未直接采用子 Agent 结论。

## 4. 当前问题（按严重级别排序）

### M1（Medium）：`references/project-guidance.md` 同文件自相矛盾

- 位置：`references/project-guidance.md:236` vs `references/project-guidance.md:57`
- 冲突双方：`:57` 的 stale 检查要求 Message Intent Guard 区分瘦身后的 11 类自然语言 intent；`:236` 的 "Root `AGENTS.md` Should Contain" 仍规定旧版 4 标签 intent（`chat`/`requirements-discussion`/`project-skill-management`/`feature-request`）并要求写入 Brainstorm/Clarify、Concept Foundation Gate 等已被瘦身委托出去的细节；`:251-252` 同样残留旧规定性细则（Delivery Phases 建议、不改 `requirement.md` 等）。
- 实际风险：Agent 按 `:236` 撰写目标项目 root 后，会被同文件 `:57` 的 stale 检查判为不完整，产生"写完即 stale、反复重写"的自相矛盾闭环。
- 主 Agent 核对：已亲自读取两处原文确认，系本次瘦身更新 stale 检查段时漏改 Should Contain 段，属本次改动引入。
- 修复方向：把 `:236` 改写为与 `:57` 一致的新 intent 表述，并从 Root checklist 删除 `:251-252` 的下游细则；配套新增 Should Contain 段与 stale 检查段的 intent 集合一致性回归断言。

### Low（本次瘦身相关）

- **L1**：`templates/root-AGENTS.md:50,56` 把 Lightweight Change Assessment 与 Post-Merge Memory Reconciliation 写进 Message Intent Guard 块，但 `references/runtime.md:98` 与 `runtime.md:462` 明确二者 "not a message intent"。agent 可能误把它俩当 intent 值；controller 加载后 runtime 明文纠正，走偏概率低。
- **L2**：root Evidence Gate 的 "missing Review/Drift/Memory evidence"（`root-AGENTS.md:105`）可能被字面解读为执行中途停车；`runtime.md:575-585` 把语义锚定在 completion 判定点，属烦人但安全的漂移。
- **L3**：旧 stop "tests require unavailable infrastructure" 在 `runtime.md:612-635` 停止清单中无显式等价物，仅由 root Evidence Gate（`root-AGENTS.md:105`）承载；Task Done Gate 封死了无验证收口的路径，不构成 Gate 绕过。
- **L4**：Bug 意图的 Project Entry 优先权从 root 显式条款降为仅 `runtime.md:374` 承载（有 `design.md:400`、场景 15a-2b、`validate-v1.2.3-routing-fixes.sh:26` 三处兜底）。
- **L5**：root Completion 第 4 条（`root-AGENTS.md:118`）的 Feature Completion Check 触发点比 `feature-completion-check.md:11-17` 少 "after Submit / Integrate" 一项；`submit-and-integrate.md:215-225` 的有序退出会把它路由回 Completion Check，无跳到 Close 的路径。
- **L6**：不清晰意图的三层提问模板形状不一致（`SKILL.md:42` 五选一未覆盖 operational-support 方向；`runtime.md:60-62,362` 三个二选一；`workflow-checklists.md:121-122` 两个二选一）。
### Low（瘦身前已存在，非 `e07d50c` 引入）

- **L8a**：`No reliable memory` 行与 `Remote source of truth` 行信号重叠（`root-AGENTS.md:69-70` 行序 vs `runtime.md:306,315` 远程优先）；`project-entry-scan.md:51-53` 的 redirect 兜底使首跳选错也能收敛。旧版 33 行表同样如此排序。
- **L8b**：双根（`.agent-loop/` + legacy `agent-loop/`）同时存在时发现规则不一致：`runtime.md:334` 隐含 `.agent-loop/` 静默胜出 vs `lightweight-change-lane.md:42`、`design.md:520` fail closed。

## 5. 已通过的关键不变量（节选，均经跨文件取证）

- First-match 优先级链 `Safety Stop -> Remote Discovery -> ... -> Normal Stage Continuation` 在 `root-AGENTS.md:65` 与 `runtime.md:300` 逐字一致，双文件有测试断言。
- 25 个 leaf stage 顺序唯一所有者为 `runtime.md:474-510`；`test_runtime_leaf_stages_remain_ordered_and_gateway_owned` 断言；`root-AGENTS.md:86` 声明 Gateway 不删不改排下游 stage。
- controller 缺失 fail-closed：`root-AGENTS.md:16` ↔ `runtime.md:17,305`，有回归断言。
- 旧约 20 条 Required Stops 逐条在 6 类 Gate + `runtime.md:612-635` 找到等价物（含 Complex Artifact Mode、first-version exclusions、SHA-256 Batch Gate、named-skill/concrete-scope）。
- Auto Mode 边界一致且不绕过 6 类 Gate（`root-AGENTS.md:93-96,109` ↔ `runtime.md:538-558,550`）。
- 能动性条款逐条去向确认：文件头 steering 句原样保留（`root-AGENTS.md:5`）；"Own the project outcome"（`:30`）为新增强化；"Do not finish with only done" 移至 `runtime.md:454`；"propose missing artifacts"（`:32`）；"never default to global skill directories" 移至 `project-skills.md:5,108`；blocked 必须给恰好一个 unblock stage（`runtime.md:317-325`）。
- TDD RED 不可跳过、Plan Gate 不可跳过、Task Done Gate 七要素、Feature Close Review 的 design-slice 阻断、Submit 两段确认与独立生命周期 Gate、Post-Merge 前置 verified code integration、code reality wins、Active Feature 唯一、Phase roll-up（`partially-implemented`）均在 references 完整保留且跨文件一致。

## 6. 压力场景（18 个，全部推演通过）

覆盖方法文档要求的代表面：复杂 Requirement -> ADR -> Feature Spec 的 design-slice 阻断、无 ADR 简单路径、TDD RED 不可跳与非行为 `N/A`、Active Feature/Pause/Resume/Close、多 Phase `partially-implemented` 汇总、ADR drift 回 Decision & Design、Follow-up investigate-first、Submit blocker 与两段确认、stale-memory 走 Recovery、普通 Chat 不建产物；另加本次瘦身特有风险面：Auto-Loop 中 staging deploy 被 External Mutation Gate 拦截、无记忆 + 远程提示的路由收敛、无记忆 + Bug 意图的 Project Entry 优先、controller 失效时 merge 请求双重拦截、helper 缺失不削弱推进力、merge 后直接 push 被 Git Gate Separation 拦截。全部场景在 HEAD 规则下均收敛到正确路由或正确停车，无 Gate 绕过、无死锁。

## 7. RED 基线、GREEN 结果与回归测试

- RED 基线：既有行为基线为 39/39 shell + 215/215 Python；新增 lossless-slimming focused contract 随后以 `Ran 6 tests`、`FAILED (failures=1, errors=1)` 进入 RED。实施完成后的 GREEN 才是 221/221 Python；完整原始证据见 `docs/reports/agent-loop-v1.5.0-root-agents-lossless-slimming-red-baseline-2026-07-21.md`。
- 本次验证未执行修复（M1 待人类裁决修复时机），故无 GREEN 区；报告按方法要求与历史基线分区呈现。
- 各域建议补充的回归断言（待人类批准后随修复一并加入）：
  1. M1：`tests/validate-project-guidance-should-contain.sh`（新增）断言 Should Contain 段不再含已委托细则字面量，且其 Message Intent 条目与 `:57` stale 检查集合一致。
  2. 能动性关键短语断言 + mutation 测试："recommend exactly one next action"、"ask exactly one blocking question"、"propose missing artifacts instead of waiting..."、"inspect all safely available evidence first"。
  3. references 侧承载断言：`runtime.md` 含 `Do not end an action report with only "done"`；`stage-guides.md` 含 `Do not ask the human "what next?"`；`feature-completion-check.md` 含 design-slice 阻断与 Standards Review 触发清单。
  4. Message Intent / Bootstrap 块内容契约（含 "only after Bug and active-Feature ownership checks"、"accepted legacy"、"remote-entry evidence"）及对应 mutation 测试。

## 8. 未采纳或降级意见

- Recommendation 域建议统一三层提问模板：降为 Low 观察项。root 的 "ask exactly one blocking question" 语义兼容所有模板，覆盖差不构成冲突；可在下次 SKILL.md 修订时顺手收敛，不单独立项。
- Autonomy 域两条 Low（Evidence Gate 字面解读、两条旧 stop 无显式 Gate 归属）：按"不把希望更详细当缺陷"原则不改文档，仅用回归测试固定映射。
- First-match precedence 已由 `validate-v1.2.4-postfix-pressure-repairs.sh` 对 Root 与 runtime 两侧的同一固定字符串分别断言；额外 parser-based 等值测试可作为测试重构，但不是当前机械保护缺口。

## 9. 发布判断

- 结论：**STRONG（93/100）**。Root AGENTS 无损瘦身达成既定目标：224 -> 170 行（低于 190 上限），能动性条款无弱化且部分强化，无 Critical/High，无 Gate 绕过、死锁或路由不唯一。
- 建议：修复 M1（`project-guidance.md:236,251-252` 与 `:57` 对齐）并补第 7 节回归断言后，`e07d50c` 可进入发布候选验证；L 级问题不阻断。
- `commit`：本验证无代码改动，无需新 commit；`push`、`tag`：**未获得人类授权，未执行**。
