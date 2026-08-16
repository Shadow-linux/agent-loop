# Proposal: Progressive Verification + Proof First

状态：implemented and validated on alpha/v1.5.7；awaiting final Human release review（验证证据：[RED baseline](../../reports/agent-loop-v1.5.7-progressive-verification-red-baseline-2026-08-16.md)；[full validation](../../reports/agent-loop-1.5.7-full-validation-2026-08-16.md)）

目标版本：v1.5.7（alpha/v1.5.7 分支）

版本定位说明：本提案不新增 artifact tree、脚本、分发面或 canonical stage/status/mode/Gate，量级与 v1.5.4–v1.5.6 的内部方法级变更相当，故落在 1.5.x patch 序列；1.6.0 及以上预留给结构性变更（如 Evidence-driven Runtime 若将来立项）。

创建时间：2026-08-15

默认语言：中文

输入来源：外部提案《Agent Loop 优化提案：Progressive Verification + Evidence-driven Runtime》经两轮交叉审校合并后的收窄结论。原提案的 `Evidence-driven JSON Runtime`（state.json / evidence.json / run.jsonl）被明确排除在本轮之外，仅作为后续独立研究议题。

## 摘要

Agent Loop 已通过 Adaptive Depth、Lightweight Change Lane、Repair-First Verification、No-Plan Decision 与 targeted verification 建立了按风险调节流程深度的能力，但该调节停留在原则层：进入 Feature 通道后，验证深度没有可持久、可审查的决策记录，也没有防止 Agent 自评降档的硬下限。同时，RED 证据在语义上偏重"新写测试"，Bug 修复容易为形式 TDD 制造不必要的新测试；`tests.md` 缺少显式的核心不变量与 Test Oracle 质量检查，无法在人类审查前暴露"写错 Oracle"（测试通过但核心需求未被验证）的风险。

本提案收窄为两项能力：

1. **Feature Verification Profile**：Gate 1 接受后、Work Breakdown / Test Design 前记录一个三档验证档位及理由，治理 Feature 通道的 Plan 深度、测试深度、回归范围与 Review 强度；档位与理由进入 Gate 2 审查表；高风险类目有硬下限；执行期间只能自动升档，降档回到人类。
2. **Proof First 语义澄清**：RED 定义放宽为任何可信的 failure-matched 证明（新写测试、既有失败测试、复现脚本、API/UI 复现证据），保留 TDD 方法名与既有义务边界不变。

不新增 canonical stage、message intent、status、mode、Gate、Checker outcome 或 artifact tree。Required Verification、Existing Test Obligation 与全部 Human Gates 原样保留。

## 1. 已确认原则

1. 不动 Evidence-driven completion：无新鲜验证证据不得声称完成。
2. 现状基线如实描述：Adaptive Depth（`references/design.md`）已允许按风险调节 Plan 与测试细节；本轮增量是把它操作化为可持久、可审查的 Profile 决策与硬下限，不是从零引入比例化验证。
3. Profile 只治理 Feature 通道。Lightweight Change Lane 与 Review Repair Fast Path 维持现有规则，不贴新标签、不改变其入口判定。
4. Profile 是内部验证策略，不是 Mode、stage、status 或 lifecycle；三档命名与既有词汇（Strict Mode、Standard Product Definition）在 `references/concepts.md` 显式消歧。
5. 高风险类目（auth、permission、payment、数据删除、migration、public API、安全、跨模块核心逻辑）有硬下限档位，Agent 自评不得低于下限；硬触发不可覆盖语义与现有 Feature hard trigger 一致。
6. 档位升降规则带时间边界：Gate 2 接受前可凭新证据重算（含合理降档）；Gate 2 接受后的执行期间 Agent 只能自动升档；Gate 2 后降档必须重新向人类展示理由并接受；human-approved substitute verification 机制继续保留。
7. RED = 可信的 failure-matched 证明，来源可以是新写测试、既有失败测试、复现脚本或 API/UI 复现证据；不为制造 RED 形式化新建测试。
8. Bug 原始复现可以满足 RED；修复后必须重新运行 failure-matched proof。Existing Test Obligation 与 Profile 要求的回归保护仍是硬义务；只有义务之外的额外自动化保护进入 Regression Test Advisory。
9. Required Verification 与 Existing Test Obligation 不可降级为 advisory；Additional Regression Test 维持建议属性。
10. "高风险路径零损失""人类门禁和证据义务完全不动"在本提案中只是设计目标，实测验证通过前不得作为事实结论声称。
11. Markdown 继续作为单一状态源；本轮不引入 JSON/JSONL runtime state，不取消、不弱化 Review、Drift 或 Notes 的授权/范围/恢复证据职责。

## 2. Feature Verification Profile

### 2.1 决策点与归属

```text
Feature Spec
-> Gate 1 Feature Definition Review（既有）
-> Verification Profile 决策（内部方法，随 package 准备期完成）
-> Work Breakdown / Test Design / Plan / E2E Discovery（消费档位）
-> Gate 2 Implementation Readiness Review（呈现档位、理由、下限、升级触发器）
```

Profile 决策不产生独立确认轮次，与 Work Breakdown 同期由 Agent 连续完成，作为 package 的一部分进入 Gate 2。这沿用 Repair-First Verification 的"内部方法"先例（`references/design.md` 已确认该模式不新增 stage、status、mode、Gate 或 artifact family）。

### 2.2 档位

推荐命名：

```text
focused | full | high-assurance
```

| 档位 | 适用 | Plan 深度 | 测试深度 | 回归范围 | Review 强度 |
|---|---|---|---|---|---|
| `focused` | 低风险 Feature：单文件/清晰边界/无接口变更 | 收缩 | 最小有效集（边界值 + Invariant 覆盖） | 受影响既有检查 | 轻量 |
| `full` | 普通 Feature（默认档） | 标准 | 标准 | Impacted regression | 标准 |
| `high-assurance` | 硬下限类目或升级触发 | 完整 | 完整 + 边界/精度 | 扩展回归（必要时全量） | Standards Review 强制 |

命名备选 `focused | reinforced | high-assurance` 已评审：`reinforced` 语义为"从基线加强"，在升级矩阵中方向感不自然，不推荐。`strict` 与既有 Strict Mode 撞名、`standard` 与 Standard Product Definition 弱撞名，均排除。

三档在 `references/concepts.md` 中定义为 Feature Verification Profile 值，并显式声明其不是 Mode、stage 或 lifecycle。

### 2.3 记录

Profile 决策记录在 Feature `spec.md` 的固定字段（或 `notes.md` 顶层，实施时二选一并保持一致）：

```text
Verification Profile: focused | full | high-assurance
Profile Rationale: <风险判断依据，引用具体证据>
Profile Floor: <硬下限类目及适用的下限档位>
Escalation Triggers: <本 Feature 适用的升级触发器子集>
Profile Recomputed At: <Gate 2 前重算时间，可选>
```

### 2.4 硬下限

以下类目无论 Agent 自评结果如何，Profile 不得低于 `high-assurance`：

```text
auth / permission / payment / data deletion / data schema / migration /
public API / security-sensitive code / cross-module core logic
```

实施说明：该清单与 Lightweight Change Assessment 的 Feature hard trigger 清单职能不同（入口路由 vs Feature 验证深度），实施后保留各自自然语言形态，通过"同一次变更同步更新"义务 + 共享锚点关键词双向断言（permission、schema、public API、migration、cross-module 在两处均为受钉锚点，语义等价项 auth≈credential/security、payment≈product data、data deletion≈persistence 一并人工复核）防止漂移；完全抽取为单一物理定义留待后续结构性变更。

### 2.5 升级触发矩阵

统一既有分散规则（scope expansion、验证失败不可降级、Gate Drift 分类）为一份矩阵：

| 触发器 | 动作 |
|---|---|
| 未预期文件被修改 / 跨模块修改 | 升档 + 记录 Gate Drift Assessment |
| public API / schema 变更 | 升至 `high-assurance` |
| auth / permission 被触碰 | 升至 `high-assurance` |
| 同一失败重复出现 / 多次投机性修补 | 升一档 |
| Test Oracle 被判定为弱 | 升一档并重做 Test Design 对应部分 |
| 未知回归失败 | 升至 `high-assurance` |
| 范围扩张（scope expansion） | 停止扩展编辑，回到 Human Review |

执行期间触发器由 Agent 自动执行升档并记录；降档不自动执行。Gate 2 接受前凭新证据重算不触发额外人类轮次；Gate 2 接受后降档走既有边界变更语义（回到人类）。

## 3. Proof First 语义澄清

### 3.1 RED 证据来源

保留 "TDD remains the default method" 的方法名与 helper 路由不变，仅澄清 RED 证据定义（`references/runtime.md`、`references/design.md` 同步）：

```text
RED = 任何可信、可复核的 failure-matched 证明
     - 新写的失败测试（原路径）
     - 既有测试的失败运行
     - 复现脚本及其失败输出
     - API 复现证据（期望 vs 实际）
     - UI 复现证据（DOM/断言/控制台文本，非像素主观判断）
```

新 Feature：Behavior Proof First。Bug：Reproduction First（原始复现即合法 RED）。

### 3.2 义务边界（不变部分）

- 修复后必须重新运行 failure-matched proof（GREEN 义务不变）。
- Existing Test Obligation：已接受的测试义务不可降级。
- Bug Verification Matrix 的 Regression / Safety Verification 列进入 Gate 2 接受的包后即为硬义务。
- maintenance-fix 的 "tests.md must include regression coverage or a recorded substitute verification with risk and human decision" 规则原样保留。
- 额外自动化保护仍走 Additional Regression Test Advisory，不阻塞 Task Done / Feature Close。

本提案消除的唯一成本是"为制造 RED 而新写测试"；任何回归保护义务都不因此变为 advisory。

## 4. tests.md 模板增强

`templates/tests.md` 增加两节（深度随 Profile 自适应，`focused` 档可精简到一表）：

```markdown
## Core Invariants

| Invariant ID | Invariant | Source (Spec/Requirement/ADR) | Verified By |
|---|---|---|---|

## Test Oracle

| Case | Expected (Oracle) | Oracle Source | Oracle Quality Check |
|---|---|---|---|
```

Oracle Quality Check 至少回答：该用例是否直接对应一个 Invariant 或 Acceptance 条目；是否存在"测试通过但核心需求未被验证"的缺口（例如只测正向路径、遗漏反向/边界主体）。

不增加 Proof Before / Proof After / Impacted Regression / Escalation Triggers 节：前者是 `notes.md` 既有证据义务的重复落点，后者属于 Profile 全局定义，不逐 Feature 复制，避免重蹈 Artifact Tax。

## 5. 非目标

1. 不新增 canonical stage、message intent、status、mode、Gate、Checker outcome 或 artifact tree。
2. 不治理 Lightweight Change Lane 与 Review Repair Fast Path。
3. 不引入 `state.json` / `evidence.json` / `run.jsonl` 或任何第二套状态源；Markdown 保持单一状态源。
4. 不取消或弱化 Review、Drift、Notes 的授权/范围/恢复证据职责；Artifact 缩短去重只做措辞级优化。
5. 不改变 Required Verification / Existing Test Obligation / Additional Regression Test 三分结构。
6. 不实现证据自动记录 Runtime（后续独立研究，需先证明 Agent 手写 JSON 的成本收益）。

## 6. 度量与验收

### 6.1 度量计划（提案第 19 节方法）

实施后用同任务集（focused / full / high-assurance / Bug 各若干）对比改造前后：

```text
成本：Input/Output Tokens、Tool Calls、LLM Turns、验证耗时、Artifact Token（tests/plan/notes/tasks 单列）
质量：任务成功率、隐藏测试通过率、回归率、需求覆盖、Human Review 发现数、返工数
```

预期口径（待实测校准）：Artifact Token 明显下降为主收益；LLM Turns Feature 档 0–2、Bug 档 1–2；Human Gate 次数不变。

### 6.2 实施范围（协同工作流变更）

本提案触及验证门行为，属于 AGENTS.md 定义的 coordinated workflow change，实施需同变：

```text
references/runtime.md      Profile 决策点、升降规则、RED 语义
references/design.md       Profile 定义、原则、非目标
references/stage-guides.md Gate 1 后 package 准备期步骤、Gate 2 呈现项
references/concepts.md     三档定义与消歧声明
references/document-templates.md / templates/tests.md   两节模板
templates/root-AGENTS.md   受影响 managed blocks
references/validation-scenarios.md + 新增回归测试
```

并按 `docs/maintenance/full-validation-method.md` 跑全量验证（RED 基线先行、新增回归断言、中文报告存档 `docs/reports/`）。

### 6.3 验收条件

1. 三档 Profile 决策在 Gate 1 后 package 准备期被记录并进入 Gate 2 审查表。
2. 硬下限类目无法被 Agent 自评降档（有回归测试证明）。
3. 执行期间升档自动执行并留痕；Gate 2 后降档回到人类（有回归测试证明）。
4. Bug 复现作为 RED 被接受，同时回归/安全覆盖义务不变（有回归测试证明）。
5. tests.md 出现 Core Invariants 与 Test Oracle 两节，focused 档深度自适应。
6. 全库搜索无 JSON runtime 残留；无新增 stage/status/mode/Gate。
7. 全量验证六域通过，报告存档。
