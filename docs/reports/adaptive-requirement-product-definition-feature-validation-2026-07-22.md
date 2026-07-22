# Adaptive Requirement Product Definition 单功能验证报告

> 方法：`docs/maintenance/feature-validation-method.md`（五域 100 分模型）。本报告不替代、也不冒充 full validation；实施方另有 `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-22.md`。

> 2026-07-22 复评说明：本报告记录**修复前**的 80 分 STABLE 结论（4 High），作为问题输入保留。其中 4 个 High 与 2 个 Medium 已修复并经独立复测关闭，当前结论见 `docs/reports/adaptive-requirement-product-definition-feature-revalidation-2026-07-22.md`（90 分 STRONG）。请勿把本报告的 80 分当作当前评分。

## 1. 审计对象与 Scope Lock

- 日期：2026-07-22；分支：`alpha/v1.5.0`；Skill 版本：`1.5.0`（未升级）
- 审计对象：**当前工作区未提交改动**（基线 HEAD `e07d50c`，49 文件 +1300/−1126），实现 `docs/proposal/v1.5.x/adaptive-requirement-product-definition.md`
- 目标行为：新产品定义收敛到 Requirement Set `product.md`（仅 `brief | standard`）；Feature 不再写 `product.md`，只在 `spec.md` 记 Product Slice；Concept Foundation/Product Model/Completeness/Archify 变为内部按需方法；旧 `requirement.md` 与旧 Feature `product.md` 兼容双读
- 非目标（Proposal §5）：无 `complex` Profile、无 `RULE-*`、无 Hub/Board/Workbench、无新 canonical stage/intent/lifecycle、无版本变更、无 Git/发布动作
- 明确排除：`.tmp/`、`__pycache__/`、与本功能无关的既有仓库问题不计分

## 2. 总分与定级

**总分：80 / 100，等级：STABLE**（触发 hard cap：存在 4 个 unresolved High，不得评 STRONG）

- Critical：0；High：4；Medium：2；Low：约 10
- 机械基线（feature-scoped，全部实跑于本工作区）：focused shell `validate-adaptive-requirement-product-definition.sh` PASS；focused + 关联 Python 69 tests OK；14 个受影响 `validate-*.sh` 全部 PASS；YAML/JSON/`bash -n`/`git diff --check`/Markdown 围栏平衡全部 OK
- 无 Gate 端到端绕过（4 个 High 均为"冲突两侧都有文本依据，需 agent 主动选错侧"或 fail-closed 过度阻断），故无 Critical

## 3. 五域评分表

| Domain | 权重 | 得分 | 加权 | 结论 |
|---|---:|---:|---:|---|
| Requirement And Scope Fidelity | 15 | 13 | 13.0 | Proposal §18 验收标准与 §5 非目标逐项有证据；扣分见 L 级残留 |
| Logic, State, And Human Gates | 30 | 78 | 23.4 | Profile 状态机/Gate 顺序/append-only/legacy 双读闭环；ADR 消费路径 2 个 High |
| Cross-Surface Consistency | 20 | 86 | 17.2 | 主事实全表面一致；scenario 65 未迁移、目录占位符命名分裂、Brainstorm checklist 漏改 |
| Pressure Resistance | 25 | 78 | 19.5 | 12 场景 10 个闭环；P9 组合压力经 runtime 旧豁免条款部分穿透 |
| Evidence And Maintainability | 10 | 7 | 7.0 | RED/GREEN/mutation 证据真实；但测试边界未覆盖 Brief→ADR 等真实集成路径 |
| **合计** | 100 | | **80.1 ≈ 80** | |

三域深度审计由独立只读子 Agent 执行（压力域按方法要求隔离，只读发布运行时、不读 Proposal）；**全部 High 与关键 Medium 均由主 Agent 亲自复现/阅读原文核实**，未直接采信子 Agent 结论。

## 4. 当前问题（按严重级别排序）

### High-1：Brief → ADR 路径死锁（checker 拒绝 runtime 文档化的路径）

- `references/runtime.md:259` 明确："For a confirmed Brief … set Trace Applicability to `not-applicable`, keep IDs as `none`"；`references/workflow-checklists.md` ADR 清单同述；`templates/decision.md` 的 Coverage Hard Gate 也含 "or trace is reasoned not-applicable"。
- 但 `scripts/check-adr-requirement-model-trace.py:450-452` 对一切非 legacy 源强制 `Trace Applicability: required`，not-applicable 早退仅在 `:416` legacy 分支。
- **主 Agent 复现**（临时目录，brief-valid fixture + 按 runtime 写的 decision.md）：
  - `Trace Applicability: not-applicable` → `confirmed Product Definition ADR must set Trace Applicability: required`
  - 改写 `required` + `Accepted Concept IDs: none` → `invalid values in ADR Accepted Concept IDs: none`
- 四条出路（not-applicable / required+none / 留空 / 编造 ID）全被封死，且无文档化恢复路径；agent 可能合理化"原地升级 Brief 为 Standard"或"跳过 preflight"。并发不一致：`references/stage-guides.md:694` 仍只写 `concept-foundation-not-needed` 的 not-applicable 路径，未同步 Brief。`tests/test_adr_requirement_model_trace.py` 无任何 Brief 用例。
- 属性：fail-closed 过度阻断（不是绕过），评 High。修复方向：checker 对 `Product Definition Profile: brief` 源放行 reasoned not-applicable + `none` IDs，补 Brief→ADR fixture 与 mutation 用例。

### High-2：legacy 源 ADR 按当前模板写 Coverage Hard Gate 必被拒

- `scripts/check-adr-requirement-model-trace.py:241-250` `validate_gate` 对 legacy 源强制旧字面条款（`REQUIRED_GATE_ITEMS`），且 extra 条款同样拒绝；而 `templates/decision.md` 是当前新文案（与 `NEW_REQUIRED_GATE_ITEMS` 逐字相同，域 B 已核实），模板未说明 legacy 源须回退旧条款字面。
- 后果：legacy requirement 走 Decision & Design（legacy 主路径）时，agent 按必读模板写 Gate → preflight 必败，只能从报错反推旧条款。报错含旧条款全文、机械可恢复，故 High 而非 Critical。
- 修复方向：模板显式标注 legacy/new 两套条款分叉，或 checker 接受新条款等价映射；补 legacy 源 + 新模板条款用例。

### High-3：Brainstorm / Clarify checklist 残留旧所有权映射，与同文件新规则直接矛盾

- `references/workflow-checklists.md:386`："Write accepted answers back into the current stage artifact: detailed requirements-discussion output to `requirement.md` … feature output goes to `product.md` …"。
- 与同文件 `:120,374`（"No new Feature `product.md`"）、`references/product-definition.md:19`、`references/requirement-product-grill.md:148-162`（Output Mapping → Requirement `product.md`）直接冲突。主 Agent 已读原文确认；该行在 HEAD 已存在，但本次改动重写了相邻三个 checklist 区块却漏改此块，属改动造成的不完整迁移。
- 风险：agent 把澄清结果写进 `requirement.md`（制造第二 effective source）或为 Feature 新建 `product.md`——SKILL.md 把 workflow-checklists 列为阶段 checklist 权威，选哪侧都有文本依据。

### High-4：runtime 总合同 bypass 条款未把 Product Human Review 纳入不可绕过清单

- `references/runtime.md:13`："Do not move to a later stage until the prior stage artifact is accepted **or explicitly bypassed by the human**"；`:23` 不可绕过清单（Project Entry、re-adoption、source preservation、Onboarding、Task Done、Contract、fresh verification、submit、close）**不含** Product Human Review / confirmed Effective Product Definition。
- 而 `references/stage-guides.md:857`（Feature start 必须引用 confirmed Effective Product Definition，无例外条款）、`:895`（Product Review pending 阻断 Feature Spec）、`references/product-definition.md:213`（Stop Rules）均无 bypass 出口。SKILL.md 赋权 runtime 为 gate 权威，冲突时 agent 有文本依据选 bypass 侧。
- 压力实证（P9：Draft 阶段 + 人类催"先写代码文档回头补" + 线上紧急）：绕过许可逐字可读。缓解：真正紧急缺陷可走 Bug Management，bounded 非 Bug 可走 Lightweight lane，`stage-guides.md:857` 有 minimum Brief 快通道——正规出路存在，但规则文本留下了绕过许可。
- 修复方向：`runtime.md:23` 清单加入 "Product Human Review / confirmed Effective Product Definition before Feature Spec"，或显式声明 :13 bypass 不豁免 product-definition.md Stop Rules；补 P9/P8 变体压力场景。

### Medium

- **M1**：`references/validation-scenarios.md:2450-2484` scenario 65 整块未迁移：Expected A/B 仍要求旧 requirement 文档章节（Terminology/Acceptance Scenarios 等）与已删除的旧 Feature Product Brief 章节（Primary User Journey/Product Tradeoffs/Success Signals），与 `templates/product.md` 直接冲突；本 diff 同时从 `tests/validate-grill-artifact-templates.sh` 移除了对应守卫断言。
- **M2**：Requirement Set 目录占位符分裂 `<record-date>-<topic>`（SKILL.md/runtime/product-definition 等）vs `<archive-date>-<topic>`（document-templates/concepts/templates README/workflow-checklists），最刺眼的是 `stage-guides.md` Requirement Archive Write 列表相邻两行混用两种拼写。

### Low（择要）

- spec 侧 `Product Review Evidence` 仅子串匹配（`unconfirmed` 含 `confirmed` 可通过，`check-requirement-product-definition.py:193`）；
- README 指针的 `Last Confirmed`/`Previous Source` 未校验；
- ADR snapshot 新旧双形式并存不被拒绝（模板要求 "Never use both forms"，checker 只读对应分支）；
- checker 的 Brief 膨胀守卫 `STANDARD_ONLY_SECTIONS` 未覆盖模板全部 Standard-only 章节；
- `workflow-checklists.md:626` 的 `product.md` 缺 `when present` legacy 限定；
- `README.md` 概览流程中 Requirements Discussion 出现两次；
- `Usage.md:320` grill 产出归属仍用 legacy 章节名；
- "product consensus candidates" 在新模板中失去标记落点；
- `examples/concept-foundation-refund/product.md` 旧格式无 legacy 标注，且 `examples/adaptive-product-definition/` 未登记进 SKILL.md 示例清单；
- 5 个 shell 测试丢失执行位（100755→100644，无关 metadata churn）。

## 5. 压力场景矩阵（隔离复测，12 项）

| 场景 | 结果 | 关键依据 |
|---|---|---|
| P1 简单目标选 Brief、不建 Feature 产物 | PASS | `product-definition.md:23-46`；受 High-3 误导风险 |
| P2 "支持退款"不得按句短选 Brief | PASS | `product-definition.md:37-44` |
| P3 外部 PRD byte-stable、不自动确认 | PASS | `requirement-management.md:17,80,262` |
| P4 无状态机不制造 `STATE-*` 占位 | PASS | `product-definition.md:84`；`templates/product.md:7,112` |
| P5 Archify 不可用 fallback 不阻断 | PASS | `product-definition.md:186` |
| P6 一份 Standard 拆两个 Feature | PASS | `product-definition.md:188-198`；checker 指针/Profile 一致性 |
| P7 legacy resume 不强制迁移 | PASS | `product-brief.md:22-31`；`product-definition.md:202` |
| P8 Auto-Loop + 人类离线 + 历史成功 + 未确认 product.md | PASS（四层拦截） | `runtime.md:549-553,561`；`stage-guides.md:891,895` |
| P9 Draft + 催进度 + 紧急，试图跳过 Product Human Review | **FAIL（部分穿透）** | High-4：`runtime.md:13,23` |
| P10 新旧双 effective pointer | PASS（fail closed） | `product-definition.md:158,215`；resolver 实测拒绝 |
| P11 spec 重定义已确认产品语义 | PASS | `stage-guides.md:893-894` |
| P12 PRD helper 写 native PRD/部署原型 | PASS | `product-definition.md:169-170`；`external-skill-adapters.md:40,148-150` |

## 6. RED / GREEN / 证据评价

- RED（实施方证据，`docs/reports/agent-loop-v1.5.0-adaptive-requirement-product-definition-red-baseline-2026-07-22.md`）：focused shell exit 1、focused Python 10/10 失败，基线 39/39 + 221/221 全绿——真实 RED，非既有失败。主 Agent 抽查认可。
- GREEN：RED 报告称 focused Python 44/44、focused shell PASS、13 个 affected shell PASS、10 项 mutation 全部被拒；本次审计独立复跑 focused + 关联集合 69 tests OK、14 个 affected shell 全 PASS，与报告一致。
- 诚实性扣分：测试边界未覆盖 Brief→ADR 集成（High-1 无任何 fixture）、legacy 源 + 新模板 Gate 条款（High-2）、Brainstorm checklist 落点（High-3）、bypass 条款组合压力（High-4）；实施方的 2026-07-22 full-validation 报告同样未捕获这 4 个 High，建议修复后重跑对应部分。另有 5 个 shell 测试执行位的无关 churn。

## 7. 未执行项与原因

- 全仓库 39 shell + 全量 Python discover：由实施方 full-validation 报告覆盖，本次只跑 feature-scoped 集合（方法允许）；本报告分数不以全量测试为前提。
- pytest：环境无 pytest，统一使用项目规范 unittest runner。
- installed-skill sync / Windows 实机：非本报告范围；实施方声明 `macOS-verified / Windows-test-defined`。

## 8. 提交判断

- **STABLE（80/100）**：主路径闭环、无 Gate 端到端绕过，但 4 个 High（2 个 ADR checker 契约死锁/矛盾、2 个文档冲突/豁免缺口）必须在 commit 前处理。
- 建议最小修复集：① checker 放行 Brief reasoned not-applicable；② 模板/checker 对齐 legacy Gate 条款分叉；③ 改写 `workflow-checklists.md:386` 为新所有权映射；④ `runtime.md:23` 纳入 Product Human Review；随修复补第 4 节各回归断言（Brief→ADR fixture、legacy 新条款用例、P9/P8 变体压力场景、scenario 65 迁移 + 守卫、占位符命名统一），然后重跑 focused + affected 集合并复审。
- 本次验证未做任何文件修改、未 commit、未 push、未 tag。
