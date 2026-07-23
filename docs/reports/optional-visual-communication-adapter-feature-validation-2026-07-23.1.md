# Optional Visual Communication Adapter 当前单功能验证报告

> 方法：`docs/maintenance/feature-validation-method.md`。本报告重新审计当前工作区，包含 2026-07-23 人类确认的 Archify-first recommendation 修订；不覆盖此前的独立评测报告。

## 1. Scope Lock

- 日期：2026-07-23
- 分支：`alpha/v1.5.0`
- HEAD：`7a74667bc3ce6acd99b34fc867115fbc8455b7f3`
- Skill 版本：`1.5.0`，未升级
- 审计对象：HEAD 之上的当前 Optional Visual Communication Adapter 未提交工作区实现
- 最新人类确认顺序：匹配的 active project-local visual skill → installed Archify → materially useful 时先提出精确 Archify 安装/使用建议 → Mermaid/table/ASCII fallback
- 目标行为：Visual Trigger、Archify-first routing、Installation Authorization、Visual Scope Grant、`render to converge, text to record`、`source-render-v1`、Requirement/ADR/Onboarding/Feature Spec 边界、非阻塞 fallback
- 明确非目标：Archify 不是 mandatory helper；不新增 stage/intent/lifecycle；不 vendor Archify；不修改 root managed block 或 Skill version；不授权 Git、release、publish 或 installed-skill sync
- 排除：`.tmp/`、`__pycache__/` 和与本功能无关的工作区内容不计入得分

## 2. 当前评分

**总分：97 / 100，等级：STRONG**

当前发现：

- Critical：0
- High：0
- Medium：0
- Low：2

该等级表示主路由、Feature Spec visual boundary 和 Human Gate 闭环成立。Proposal 验收标准要求的 Medium=0 已满足；剩余两项为兼容/防漂移 Low。

| Domain | 权重 | 得分 | 结论 |
|---|---:|---:|---|
| Requirement And Scope Fidelity | 15 | 15 | Archify-first 与 Feature Spec visual boundary 均符合已确认 Proposal |
| Logic, State, And Human Gates | 30 | 29 | 安装、生成、持久化、Product/ADR/Onboarding/Feature/Git Gate 独立；legacy 兼容入口保留一个低风险 writer 识别边界 |
| Cross-Surface Consistency | 20 | 20 | runtime/design/adapter/skill routing/Feature Spec stage/checklist/scenario 对视觉边界给出同一结论 |
| Pressure Resistance | 25 | 24 | Feature Spec 新语义变体已进入 focused contract/scenario；拒绝后不重复推荐仍缺一个直接 mutation contract |
| Evidence And Maintainability | 10 | 9 | 真实 RED/GREEN、focused regression、跨平台 path fixture 和机械检查齐全；本轮未获授权派发隔离评测 Agent |
| **合计** | **100** | **97** | **STRONG，Critical/High/Medium 均为 0** |

## 3. RED → GREEN 证据

### 原始能力 RED

- focused Shell 在 adapter 尚不存在时因缺少 `Optional Visual Communication Adapter` 失败；
- focused Python 在 shared validator 尚不存在时因 `ModuleNotFoundError: scripts.visual_artifact_support` 失败。

### Archify-first follow-up RED

在修改运行规则前，新增优先级合同并执行：

```bash
bash tests/validate-optional-visual-communication-adapter.sh
```

真实结果：

```text
FAIL: references/external-skill-adapters.md missing: Do not offer Markdown / table / Mermaid / ASCII as the first drawing path merely because Archify is absent.
```

该 RED 证明旧规则仍允许“先 fallback、再考虑推荐”的解释路径。

### Feature Spec visual boundary RED

在修改发布运行规则前，继续扩展同一 focused contract：

```bash
bash tests/validate-optional-visual-communication-adapter.sh
```

真实结果：

```text
FAIL: references/runtime.md missing: Feature Spec may use a visual only to explain the accepted Product Slice.
```

随后将断言收敛为 Proposal 的完整边界：accepted Product Slice、feature responsibility、feature-local implementation/acceptance path；新产品语义返回 Requirements Discussion。

### 提交前人类文档校准 RED

在校准 README / Usage / CHANGELOG 前，将 Feature Spec 视觉边界与 Onboarding 的 Archify-first 表达加入 focused contract。真实结果：

```text
FAIL: README.md missing: In Feature Spec, a visual may explain only the accepted Product Slice, feature responsibility, and feature-local implementation or acceptance path.
```

GREEN 后，README、Usage 和 CHANGELOG 使用同一 Feature Spec 边界；Usage 的 Onboarding 表达不再产生 Mermaid-first 歧义。

### 当前 GREEN

```text
bash tests/validate-optional-visual-communication-adapter.sh
PASS

python3 -m unittest tests.test_optional_visual_communication_adapter -q
Ran 19 tests
OK
```

发布运行时现在统一表达：

```text
matching active project-local visual skill
→ installed Archify
→ recommend Archify before fallback when it would materially improve review
→ Markdown / table / Mermaid / ASCII fallback
```

## 4. Findings

### 已解决 M1：Feature Spec visual boundary

当前规则已协调到：

- `references/runtime.md` 与 `references/design.md`：Feature Spec 是 Visual Trigger 下的适用 surface；
- `references/external-skill-adapters.md` 与 `references/skill-routing.md`：图只解释 accepted Product Slice、feature responsibility 或 feature-local implementation/acceptance path；
- `references/stage-guides.md` 与 `references/workflow-checklists.md`：feature-local clarification 回写 `spec.md`；
- 新 product concept、role/permission、relationship、flow、state、invariant、terminal、fact ownership 或 product rule 停止 Feature Spec 并返回 Requirements Discussion；
- Feature Spec 不得直接编辑 Requirement `product.md`；
- `references/validation-scenarios.md` 与 focused contract 覆盖 “it is only a diagram” 压力变体。

本轮不再记录 Medium。

### L1（Low）：无 contract marker 的新文档可进入 legacy visual reader

`scripts/check-requirement-product-definition.py` 在 `Derived Visuals` 没有 `Visual Manifest Contract` 时使用 legacy 六列 reader。测试 `test_legacy_product_visual_row_remains_readable` 证明 HTML-only legacy row 仍可通过。

这是 Proposal 明确要求的历史兼容，不应破坏或批量迁移；残余风险是 checker 无法机械判断一个无 marker 文档究竟是历史 reader 输入，还是新 writer 漏写 marker。当前 writer/template/runtime 均要求 `source-render-v1`，因此记录为 Low，不作为破坏兼容的修复理由。

### L2（Low）：拒绝后不重复推荐缺少直接 mutation contract

Published runtime 已规定人类拒绝后进入 fallback、不得阻塞 owning stage，能够阻止主路径死锁；但 focused Shell contract 与 Scenario 75 没有直接断言“同一范围内不得反复推荐”。Proposal mutation pressure 明确列出了该变体。

风险：未来文本漂移可能保留 fallback，却重新引入重复施压。当前行为规则可推导正确结果，因此是测试维护缺口，不是当前 Gate 绕过。

## 5. 压力场景

| 场景 | 当前结果 | 证据/判断 |
|---|---|---|
| Visual Trigger 不成立但 Archify 已安装 | PASS | installed capability alone is not a trigger |
| 匹配 active project-local visual skill | PASS | Project Skill precedence 在 Archify 之前 |
| Archify 已安装且视觉有实质价值 | PASS | 获得 Visual Scope Grant 后优先使用 Archify |
| Archify 缺失且视觉有实质价值 | PASS | 先给精确、可拒绝的 Installation Authorization，不先画 Mermaid |
| Archify 不值得安装 | PASS | 直接使用 Markdown/table/Mermaid/ASCII，不制造依赖 |
| 人类拒绝 + 时间紧急 + 以前安装成功 | PASS | fallback，不安装、不阻塞；旧成功与紧急不扩权 |
| 安装命令/来源/位置变化 | PASS | 旧授权失效，重新确认；失败不能提权、换源或换包管理器 |
| 同一问题内视觉微调 | PASS | 同一 Visual Scope Grant 可迭代 |
| source/stage/type/durable path 改变 | PASS | 要求新 Grant |
| 人类确认 working render | PASS | 先回写 owning Markdown；不能直接形成 Product/ADR acceptance |
| HTML/PNG/SVG 无 typed source | REJECT | `source-render-v1` validator fail closed |
| source/render/hash/type/meta.output drift | REJECT | focused Python mutation tests 拒绝 |
| ADR 图 + 人类未接受 ADR | PASS | ADR 保持 proposed；图不能满足 Technical Landing coverage |
| Onboarding 漂亮图但无 code/config evidence | REJECT | Diagram ID / source-render / evidence hard gate |
| Feature Spec 图引入新产品语义 | PASS | 停止 Feature Spec，返回 Requirements Discussion；不得写入 `spec.md` 或直接编辑 `product.md` |
| 新 writer 漏写 contract marker | LEGACY PASS | 兼容 reader 无法区分，见 L1 |
| 人类拒绝后跨轮重复推荐 | WEAK | fallback 语义存在，直接 mutation regression 缺失，见 L2 |
| 安装/Visual Grant 被解释成 commit/push/release | REJECT | 独立 Gate 明文禁止 |

## 6. Feature-Scoped Tests

实际执行：

```text
8 / 8 affected Shell suites PASS
69 / 69 direct Python tests PASS
41 / 41 full Shell suites PASS
277 / 277 full Python tests PASS，69.528s
```

Shell suites：

- `validate-optional-visual-communication-adapter.sh`
- `validate-adaptive-requirement-product-definition.sh`
- `validate-adr-requirement-model-technical-landing-trace.sh`
- `validate-project-decisions-adr-lane.sh`
- `validate-evidence-graph-ddd-onboarding.sh`
- `validate-onboarding-core-flow-completeness.sh`
- `validate-human-help-version-docs.sh`
- `validate-feature-validation-method.sh`

Direct Python modules：

- `tests.test_optional_visual_communication_adapter`
- `tests.test_requirement_product_definition`
- `tests.test_adr_requirement_model_trace`
- `tests.test_onboarding_core_flow_coverage`

机械检查：

| 检查 | 结果 |
|---|---|
| `SKILL.md` YAML | PASS |
| repository JSON | 3 / 3 PASS |
| repository Shell syntax | 42 / 42 PASS |
| repository Ruby tests | 2 / 2 PASS |
| tracked/current Markdown fence balance | 273 / 273 PASS |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |

全仓 41 Shell / 277 Python 已按协调 workflow change 要求重新执行并记录到单独的 full-validation 报告；它们证明未引入跨功能回归，但不用于抬高专项五域得分。

## 7. Proposal Coverage

| Proposal area | 结果 |
|---|---|
| Visual Trigger / simple-content no-trigger | PASS |
| project-local → Archify → recommendation → fallback | PASS |
| exact Installation Authorization | PASS |
| bounded multi-round Visual Scope Grant | PASS |
| semantic authority → typed source → render | PASS |
| Requirement durable visual and legacy compatibility | PASS，带 L1 |
| ADR visual and Human Gate independence | PASS |
| Onboarding visual/evidence completeness | PASS |
| Feature Spec visual ownership/return | PASS |
| Human decline/failure non-blocking | PASS，mutation coverage 带 L2 |
| no new stage/intent/lifecycle/version/root block | PASS |
| commit/push/tag/release independence | PASS |

## 8. 评分判断与下一步

当前功能为 **97/100 STRONG**：

- Archify-first 与 Feature Spec visual boundary 已闭环，未发现 Gate 绕过、fallback 死锁或优先级冲突；
- Critical / High / Medium 为 0；
- L1 是明确兼容边界；L2 是后续可补的防漂移测试，不阻断 Human Review；
- 推荐下一阶段：Human Review 当前 diff 与报告；未经授权不进入 commit/push。

本次评分未 stage、commit、push、tag、PR、merge、release、publish 或同步 installed Skill。
