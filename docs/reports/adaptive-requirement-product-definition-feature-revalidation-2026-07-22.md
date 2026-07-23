# Adaptive Requirement Product Definition 单功能复评报告（修复后 GREEN 复测）

> 方法：`docs/maintenance/feature-validation-method.md`。本报告是 `docs/reports/adaptive-requirement-product-definition-feature-validation-2026-07-22.md`（80 分 STABLE，4 High）的修复后复评：旧报告作为问题输入，所有结论均来自本次独立重跑与独立构造的攻击用例，未采信修复方报告的数字或结论。

## 1. 审计对象

- 日期：2026-07-22；分支：`alpha/v1.5.0`；Skill 版本：`1.5.0`（未升级）
- 审计对象：当前工作区未提交改动（基线 HEAD `e07d50c`；53 文件，含修复轮对 `scripts/check-adr-requirement-model-trace.py` +213 行、`references/runtime.md`、`references/workflow-checklists.md`、`templates/decision.md`、`references/validation-scenarios.md` 及 `tests/test_adr_requirement_model_trace.py` +153 行的改动）
- 复评范围：旧报告 4 High + 2 Medium 的修复验证；修复方指定的全部攻击边界；两条端到端集成路径；范围漂移扫描

## 2. 总分与定级

**总分：90 / 100，等级：STRONG**

- Critical：0；High：0（旧 4 个 High 全部关闭并经独立攻击验证）；Medium：2（本轮新发现的残余验证器缺口，见第 4 节）；Low：1（cosmetic）
- 机械基线（本 Agent 实时重跑、自行统计，与修复方声明一致）：Shell **40/40**；Python discover **255/255 OK**；focused（`validate-adaptive-requirement-product-definition.sh` + 三个 focused Python 文件）**51/51**；`git diff --check` OK

## 3. 五域评分表

| Domain | 权重 | 得分 | 加权 | 结论 |
|---|---:|---:|---:|---|
| Requirement And Scope Fidelity | 15 | 14 | 14.0 | 范围漂移扫描全净（第 6 节） |
| Logic, State, And Human Gates | 30 | 90 | 27.0 | 4 High 语义修复正确；残余 R1 伪造区块漏检 |
| Cross-Surface Consistency | 20 | 90 | 18.0 | M1/M2/High-3 关闭；残余 R2 两验证器结论分裂 |
| Pressure Resistance | 25 | 88 | 22.0 | 12 旧场景 + 15 个新攻击用例，仅 2 个残余穿透 |
| Evidence And Maintainability | 10 | 9 | 9.0 | 修复带 +153 行回归测试；数字经第三方独立复跑 |
| **合计** | 100 | | **90** | |

## 4. 旧发现关闭验证（全部独立构造，非复用旧用例）

### High-1：Brief → ADR 死锁 —— 已关闭

- **G1（原死锁路径）**：brief-valid + `Trace Applicability: not-applicable` + IDs/rules `none` + 具体理由 → `PASS: reasoned confirmed Brief ADR proposed gate is complete`
- M-a：not-applicable 但伪造 `product.md#fake-rule` → 拒绝 `reasoned not-applicable ADR must not declare Product Rule references`
- M-b：理由为 `n/a` → 拒绝 `needs a concrete trace reason`
- M-c：翻面写 `required` + `none` IDs → 拒绝 `reasoned no-model ADR must set Trace Applicability: not-applicable`
- M-d：standard 源 + not-applicable → 拒绝 `confirmed Product Definition ADR must set Trace Applicability: required`（Standard 不能借 Brief 通道绕过 coverage）
- 机制：`check-adr-requirement-model-trace.py:449-499` 新增 `reasoned_brief_not_applicable` 早退分支，与 legacy not-needed 分支并列

### High-2：legacy ADR Gate 兼容 —— 已关闭

- G2：legacy 源 + 旧版完整 Gate 条款 → PASS（8 refs / 5 landed）
- G3：legacy 源 + 当前统一完整 Gate 条款 → PASS（同一 fixture 替换条款后）
- M-f：混合两套条款 → 拒绝；M-g：增加任意条款 → 拒绝；M-h：新源 + 旧条款 → 拒绝
- 机制：`:241-250` legacy 允许任一完整契约精确集合匹配，混合/缺项/增项破坏集合相等而 fail closed

### High-3：Brainstorm checklist 旧所有权映射 —— 已关闭

- `workflow-checklists.md:386` 已改写为：Requirements Discussion 输出 → Requirement `product.md` 草稿，README 只留 source/lifecycle/phase/mapping/decision-link 摘要，Feature 局部澄清 → `spec.md`/`notes.md`，明确 "do not create a new Feature `product.md`"
- `validation-scenarios.md:2417,2462,2477` 三处场景钉住新落点

### High-4：Product Human Review 可绕过 —— 已关闭

- `runtime.md:13` 改写为 "or the owning stage explicitly permits a human bypass. **Product Human Review confirmation cannot be bypassed for a new Effective Product Definition**"
- `runtime.md:23` 不可绕过清单新增 "Product Human Review confirmation for a new Effective Product Definition"
- `stage-guides.md:857`（Feature start 必须 confirmed EPD 或 supported legacy source）与 `:601` 保持不变，三层一致
- P9 场景（draft + 线上紧急 + 人类明示跳过）重推演：runtime 总合同不再提供逐字绕过许可；正规出口仍是 Bug Management / Lightweight 重评估（`runtime.md:44,119`）或 minimum Brief 快通道（`stage-guides.md:857`），"紧急"本身不构成资格

### 旧 Medium：M1 / M2 —— 已关闭

- M1：`validation-scenarios.md:2450-2484` scenario 65 已整体重写为 "Adaptive Product Definition Grill Coverage"，期望输出与新模板一致（grill 产出落 `product.md`、response-local、Product View Applicability、无旧 Feature Brief 章节）
- M2：`<archive-date>` 全仓仅剩 `design.md:59` 一条显式兼容性声明（canonical 为 `<record-date>`，legacy 名可读），不再是命名分裂

## 5. 本轮新发现（残余）

- **R1（Medium）**：reasoned Brief ADR 中**伪造 Scope Inventory / Technical Landing Trace 区块可通过 checker**（实测 M-e3：`PASS`）。`runtime.md:259` 明确 "do not fabricate Concept Definitions, Scope Inventory, or Technical Landing Trace rows"，但验证器在 reasoned 早退路径不检查这两个区块的存在性。伪造内容是 checker 不消费的死文本，不改路由/授权结论，但会在 Human Review 面前呈现看似权威的假模型行。修复方向：reasoned 路径拒绝这两个区块非空存在。
- **R2（Medium）**：`check-concept-foundation-trace.py:111` 仍是子串匹配 `"confirmed" not in normalized(...)`——spec 写 `Product Review Evidence: unconfirmed pending human review` 时该 checker **PASS**，而 `check-requirement-product-definition.py:196-198`（已改为锚定正则 `^confirmed(?:\s|$)`）正确拒绝。同一 artifact 两个验证器两个结论。修复方向：对齐为同一锚定判断。
- **L1（Low, cosmetic）**：legacy Gate 混合/增项时的报错文案为 "missing required items"，实际是集合不相等；不妨碍 fail closed，仅误导排查。

## 6. Freshness 与误判攻击（全部实测）

| 用例 | 结果 |
|---|---|
| spec `Product Review Evidence: unconfirmed ...`（definition checker） | 拒绝 ✓（但见 R2） |
| `Last Confirmed` 未来日期 | 拒绝 `cannot be in the future` ✓ |
| `Last Confirmed` 过去日期但与 `Confirmed At` 不一致 | 拒绝 `must match Product Human Review Confirmed At` ✓ |
| `Previous Source` 不存在 | 拒绝 ✓ |
| `Previous Source` 越界（`../../outside.md`） | 拒绝 `reference escapes Requirement Set` ✓ |
| `Previous Source` 指向当前 `product.md` | 拒绝 ✓ |
| ADR snapshot 同时含 Product Definition 与 Concept Foundation metadata | 拒绝 `must not mix` ✓ |
| Brief 塞入 Standard-only 章节（Product Capability Scope / State Model） | 拒绝 `contains Standard-only product-model views` ✓ |
| spec Product Slice 引用未知 anchor | 拒绝 `unknown source anchors` ✓ |

## 7. 端到端集成路径（实测）

- **简单路径**：Brief → Feature Product Slice（不走 ADR）：brief-valid + 构造最小 spec → 两个 checker 均 PASS
- **复杂路径**：Standard → ADR coverage → Feature Product Slice：standard-valid fixture 三 checker 全 PASS（definition / ADR trace 11 refs 11 landed / concept-foundation trace 2 concepts 10 models）
- **Brief 确需共享技术决策**：reasoned no-model ADR 无死锁（G1）
- **legacy 路径**：`adr-technical-landing/valid`（旧条款）与 examples `adaptive-product-definition`（Requirement→Feature Slice）均 PASS
- **兼容性倒退**：无——legacy fixtures、旧条款、旧 concept-foundation trace 全部保持可读可验

## 8. 范围漂移扫描（全仓 grep，无命中）

无 `complex` Profile；无 Product Hub/Board/Workbench；无 `RULE-*`；message intent 表仍 10 行未新增；无新 canonical stage（focused contract 断言 `Product Brief if Needed` 已移出 runtime）；无可执行 schema；`SKILL.md`/`plugin.json` 版本均 `1.5.0`；root 13 个 managed block 仍 `block-version:1.5.0-20260721.2`。

## 9. 提交判断

- **STRONG（90/100）**：旧 4 High + 2 Medium 全部关闭并经独立攻击验证；两条集成路径通畅；无兼容性倒退、无范围漂移。
- 残余 2 个 Medium（R1 伪造区块漏检、R2 验证器子串判断分裂）不阻断提交，但应在下一修复轮处理并补回归用例；L1 为文案优化。
- 本次复评未修改任何生产代码、未 commit、未 push、未 tag。

## 10. R1/R2 关闭复核（2026-07-22 第二轮，评测 Agent 独立复测）

修复方声明 R1/R2 已修复并通过 Human Review；以下为评测 Agent 独立重打攻击与实时统计，未采信修复方数字：

- **R1 已关闭**：reasoned Brief ADR 伪造 Scope Inventory（`must omit Requirement Model Scope Inventory`）、Technical Landing Trace（`must omit ... Technical Landing Trace`）、Concept Definitions（`must omit Concept Definitions`）均被拒绝；legacy not-needed ADR 伪造 Inventory 同样被拒绝。回归无损：clean reasoned Brief ADR 与 clean legacy not-needed ADR 仍 PASS，未过度阻断。
- **R2 已关闭**：spec `Product Review Evidence: unconfirmed ...` 现被两个 checker 一致拒绝（`Feature Product Review Evidence must be confirmed`）；`confirmed` 回归双 PASS。
- **附带上轮 L1 也已改善**：Gate 混入任意条款时报错现为准确的 `contains unsupported items`，仍 fail closed。
- **数字独立统计**：focused Python **73/73**（`test_requirement_product_definition` 23 + `test_adr_requirement_model_trace` 22 + `test_concept_foundation_trace` 9 + `test_python_checker_contract` 19）；全量 Shell **40/40**；全量 Python **258/258 OK**；YAML/JSON/`bash -n`/Python AST/Markdown 围栏/`git diff --check` 全部通过。与修复方声明一致，但由评测 Agent 实时重跑得出。
- **结论更新**：残余 Medium 清零，无 unresolved High/Critical。本功能维持 **STRONG** 定级，可进入提交审查；commit / push / tag 仍需人类另行授权，本次复核未执行任何 Git 动作。
