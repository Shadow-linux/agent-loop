# Proposal: ADR Requirement Model Technical Landing Trace

状态：v1.3.0 Release Human Gate 已批准；发布目标 stable-v1.3.0

版本边界：v1.3.x 行为增强，不修改 skill version

## 背景

Concept Foundation 与 Requirement Product Model 已经让 requirement 能够固化产品概念，并用稳定 ID 表达关系、角色/权限、命令/事件、业务流程、产品状态、产品对象/事实、不变量和异常恢复。

现有 Decision & Design / ADR 已明确：

- PRD / Requirement Product Model 拥有产品语义；
- ADR 只能消费 accepted 产品语义，不能重新定义 Concept、生命周期、关系、状态、终态、不变量或 product fact ownership；
- ADR 可以在独立 Human Gate 后选择技术表示；
- Design Slice 将共享技术设计分配给 Feature。

但现有 ADR 模板仍有四个落地缺口：

1. 只记录 `Source Requirements`，没有固定 requirement README 当前指向的 `Effective Concept Source`；
2. `Domain Concepts` 可以引用 Concept ID，但 Business Flow、Data Model、Interface、State、Recovery 等技术章节不要求引用对应 Requirement Product Model ID；
3. Requirement Model 到 Technical Landing、Design Slice、Verification 之间缺少完整性 Gate；
4. effective requirement source 变化后，没有明确规定 accepted ADR 何时必须进入 compatibility review、何时必须 supersede。

结果是 ADR 虽然原则上不能改需求，仍可能基于旧 source、遗漏某个上游模型行，或在技术章节中产生无法追踪的局部解释。

## 目标

让 Decision & Design / ADR 成为 accepted Requirement Product Model 到可开发技术设计的可追踪桥梁：

```text
Effective Requirement Source
→ Source-Wide Requirement Model Scope Inventory
→ Accepted Requirement Model IDs
→ Technical Landing Trace
→ Design Slice Coverage
→ Feature Ownership
→ Verification Evidence
```

同时保持以下边界：

- 不新增 canonical stage；
- 不新增默认中间 artifact；
- 不引入 executable schema；
- 不要求简单或 feature-local 决策创建 ADR；
- 不让 ADR 重新拥有产品语义；
- 模板和运行规则保持领域中立；讲解 Technical Landing Trace 时使用的领域内容只作为示例，不成为默认要求或验收条件。

## 方案比较

### 方案 A：增强现有 ADR（推荐）

在 `templates/decision.md` 中增加 upstream snapshot、Requirement Model Technical Landing Trace、coverage gate 和 compatibility review。现有 Design Slice 继续承担 Feature 分配。

优点：

- 一份 Decision & Design record 即可完成需求到技术的追踪；
- 不新增同步对象；
- 与当前 ADR lane、Design Slice 和 Feature Spec 规则自然衔接。

代价：

- ADR 模板更严格；
- Agent 必须显式处理 scope 内的 Requirement Model IDs。

### 方案 B：新增独立 Requirement-to-Technical Mapping 文档

在 requirement 与 ADR 之间增加单独 mapping artifact。

优点：技术映射可以独立演进。

缺点：新增默认 artifact 和同步关系；mapping、ADR、Feature Spec 容易互相漂移，不符合当前轻量边界。

### 方案 C：使用 YAML / JSON schema 自动生成映射

把 Concept、State、Flow 和技术设计变成机器可执行 schema。

优点：可以进行更强的自动验证。

缺点：超出 v1.3.x 范围，会提前引入 schema 版本、生成器和迁移规则，也容易伪装业务语义真实性。

## 选择

采用方案 A。

## 设计

### 1. Effective Requirement Snapshot

每个由 Requirement Product Model 驱动的 ADR 在头部记录：

```text
Effective Concept Source:
Concept Foundation Status: accepted | concept-foundation-not-needed
Accepted Concept IDs:
Accepted Requirement Model IDs:
Upstream Compatibility: current | review-required
Last Compatibility Check:
Trace Applicability: required | not-applicable
Trace Not-Applicable Reason:
```

规则：

- `Effective Concept Source` 必须解析 requirement README `Effective Concept Foundation` pointer；旧 requirement set 没有 pointer 时使用兼容来源；
- 触发过 Concept Foundation 的复杂 requirement 必须为 `accepted`；
- `candidate` 或 `reopened` 阻止创建或接受 ADR；
- ADR 不复制 Concept 定义或 Requirement Product Model，只记录稳定引用和必要的 unchanged meaning summary；
- `Upstream Compatibility` 不是新的 ADR lifecycle status，不改变 `proposed | accepted | superseded | deprecated`。
- 对有具体理由的 `concept-foundation-not-needed` 来源，accepted ID 字段写 `none`，trace 写 `not-applicable` 和具体原因，不伪造产品模型。

### 2. Requirement Model Scope Inventory

ADR 在选择 coherent scope 前，先盘点 effective source 中全部稳定模型 ID：

```text
REL-* | PERM-* | CMD-* | EVT-* | FLOW-* | STATE-* | PM-* | EX-*
```

每个 source ID 必须有且只有一个 scope disposition：

```text
in-scope | covered-by-accepted-decision | feature-local | proposed-decision | not-applicable
```

规则：

- `in-scope` 必须指向本 ADR，并与 snapshot 的 Accepted Requirement Model IDs 完全一致；
- existing decision / Feature Spec 引用必须解析到真实文件和有效状态；
- 尚未创建的下游 owner 必须使用显式 `planned:` canonical path，不能用模糊名称伪装真实 artifact；
- `not-applicable` 必须有具体理由；
- Scope Inventory 位于现有 ADR 内，不新增 mapping artifact；
- Agent 不得通过缩小 snapshot 和 trace 来静默隐藏 source model。

### 3. Requirement Model Technical Landing Trace

ADR 增加通用追踪表：

| Requirement Model Ref | Accepted Meaning / Constraint | Disposition | Technical Landing | Preserved Invariant | Design Slice | Verification |
|---|---|---|---|---|---|---|
| `STATE-...` | link or concise unchanged meaning | landed | component / state representation / transition owner | invariant reference | `DS-...` | test / evidence target |

允许的 `Disposition`：

```text
landed | covered-by-accepted-decision | feature-local | not-applicable
```

规则：

- ADR scope 内涉及的 `REL-*`、`PERM-*`、`CMD-*`、`EVT-*`、`FLOW-*`、`STATE-*`、`PM-*`、`EX-*` 必须各有一行；
- `landed` 必须指向具体 Technical Landing、Design Slice 和 Verification；
- `covered-by-accepted-decision` 必须引用现有 accepted decision；
- `feature-local` 必须说明下沉到哪个 Feature Spec，不得隐藏共享约束；
- `not-applicable` 必须给出具体理由，并在 ADR Human Gate 中展示；
- 表格不允许创造新的产品含义；发现含义不足时返回 Requirements Discussion。

### 4. Coverage Hard Gate

ADR 不能进入 `accepted`，Feature Spec 不能继续，除非：

- effective source 已解析且 compatibility 为 `current`；
- source-wide Scope Inventory 完整覆盖 effective source 中全部稳定模型 ID；
- scope 内所有 accepted Requirement Model IDs 都有 disposition；
- 所有 `landed` 行都有 Technical Landing、Design Slice 和 Verification；
- 没有未解决的 product-semantic blocker；
- `not-applicable`、`feature-local` 和 deferred/out-of-scope Design Slice 已由人类看到并确认；
- 每个 implementation-bearing technical rule 已进入 Design Slice Coverage。

“已经引用 Applicable Decision”只能证明 Feature 知道 ADR，不能替代 Requirement Model coverage 或 Design Slice ownership。

校验分两步：

1. ADR 保持 `proposed`，先运行 structural preflight；
2. preflight 通过后展示 Decision & Design Human Review Summary；只有人类明确接受后，Agent 才记录 Human Review Evidence、改为 `accepted` 并运行 accepted-mode validation。

Validator pass 只证明可以进入人类评审，不产生 acceptance authority。

### 5. Upstream Compatibility And Drift

当 requirement README 的 effective source 改变，或新 requirement evidence 改变已接受模型时：

1. 将依赖 ADR 的当前判断置为 `Upstream Compatibility: review-required`；
2. 停止新的依赖 Feature Spec、Plan 和 implementation；
3. 比较旧/新 effective source 的 Concept IDs 与 Requirement Model IDs；
4. 如果产品语义变化但现有技术决策仍成立，在 Decision & Design Human Gate 后更新 snapshot/trace；
5. 如果技术选择、边界、数据表示、恢复或 NFR 结论不再成立，创建 superseding ADR；
6. 不原地改写 accepted ADR 的决策含义。

Runtime 中的 `review-required` 是依赖可用性判断，不是新的 decision status。历史 ADR 保持可审计。

### 6. Decision & Design Human Review Summary

`references/human-review-summary.md` 增加专用审批表：

| Item | Review Content |
|---|---|
| Effective Requirement Source | 当前 effective source 与 Concept Foundation status |
| Requirement Model Scope | source total / in-scope / existing-decision / feature-local / proposed-decision / not-applicable / missing |
| Requirement Model Coverage | in-scope total / landed / existing-decision / feature-local / not-applicable / missing |
| Chosen Technical Decision | 选择及主要 rejected alternatives |
| Product Semantics Preserved | yes / no；任何 blocker 必须可见 |
| Migration / Compatibility / Rollout | triggered / not-triggered，以及理由 |
| Design Slice Ownership | unassigned / planned / deferred / out-of-scope |
| Verification | 每个落地行的证明方向 |
| Human Decision | accept / revise / return to Requirements Discussion |

ADR acceptance 仍需要显式人类确认。Human Review Summary 不替代完整 ADR。

accepted ADR 还必须保存 `Decision`、`Confirmed By`、`Confirmed At` 和具体 `Evidence`，使 accepted-mode validation 能证明 Human Gate 已落盘。

### 7. Triggered Operational Landing

只有技术决策引入或改变持久化表示、协议、provider、runtime boundary 或上线兼容性时，ADR 才展开：

- Migration / Backfill；
- Compatibility；
- Rollout / Cutover；
- Rollback / Reversibility。

未触发时记录一条具体 `not-triggered` 理由，不展开对应的 operational landing 章节。示例中的业务动作或技术落点不得被复制成默认设计。

### 8. ADR Scope

一份 ADR 对应一个 coherent durable decision boundary，而不是复制整份 PRD。

- 一个 requirement 可以触发多个互相关联的 ADR；
- ADR 只覆盖其声明 scope 内的 Requirement Model IDs；
- scope 外模型必须在 source-wide inventory 中由另一个 accepted/proposed decision、明确 feature-local placement，或具体 not-applicable 理由处理；
- Related Decisions / Supersedes 保持决策图可追踪。

## Artifact Ownership

| Artifact | Owns | Does Not Own |
|---|---|---|
| Effective requirement source | Concept、关系、角色/权限、命令/事件、业务流程、产品状态、产品事实与不变量 | 技术表示 |
| Requirement README | effective source/status pointer、Design Readiness、decision links | 完整 Concept 或技术设计 |
| ADR | accepted Requirement Model 到技术表示、边界、Design Slice 和验证的落地决策 | 产品语义重定义 |
| Feature Spec | assigned Design Slice 和 feature-local implementation behavior | shared decision 或上游产品语义 |
| Tests / Evidence | 证明产品不变量被保留且技术决策成立 | 反向改写 requirement / ADR |

## Failure Handling

| Failure | Required Route |
|---|---|
| Effective source 缺失或无法解析 | 返回 Requirement Archive / Requirements Discussion 修复来源 |
| Concept Foundation 为 `candidate` / `reopened` | 停止 ADR，返回 Human Grill Contract |
| Requirement Model ID 缺失或含义不清 | 返回 Requirements Discussion，不在 ADR 中补定义 |
| Trace coverage 不完整 | ADR 保持 `proposed` |
| Design Slice 未分配 | Feature Spec 保持阻塞 |
| Upstream Compatibility 为 `review-required` | 返回 Decision & Design compatibility review |
| accepted ADR 技术结论失效 | 创建 superseding ADR |

## 验证策略

先新增 focused contract 并确认 RED，再实现 runtime/reference/template 协调修改。

Focused tests 至少断言：

- ADR template 包含 Effective Requirement Snapshot；
- ADR template 包含通用 Requirement Model Technical Landing Trace；
- 默认模板和 validator 保持领域中立，不把讲解示例中的名词、动作或技术落点当成必填内容；
- coverage gate 阻止 missing、空 landing、空 Design Slice、空 Verification；
- source-wide inventory 阻止静默漏掉 `PERM-*`、`EX-*` 或其他 source model；
- proposed structural preflight 不得代替 Human Gate，accepted-mode 必须验证落盘的 Human Review Evidence；
- 外部 decision/spec 引用必须真实存在，未来 owner 必须显式使用 `planned:` 路径；
- reasoned `concept-foundation-not-needed` 路径不得被误拒绝或诱导生成假模型；
- `candidate` / `reopened` requirement 不能进入 ADR acceptance；
- effective source 变化使 compatibility 进入 `review-required`；
- Human Review Summary 有 Decision & Design Approval；
- Product Brief / Feature Spec / root guidance 不得把 ADR 变成产品语义 owner；
- accepted ADR 的 decision meaning 不被原地改写；不兼容时 supersede。

该修改触及 Decision / ADR Human Gate、dependency 和 drift 规则，因此实现后必须按 `docs/maintenance/full-validation-method.md` 执行全量语义审计、全部 `tests/*.sh` 和机械检查，并保存新的中文报告。

## 预计修改面

Runtime / design authority：

- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
- `references/project-decisions.md`

Stage / gates / guidance：

- `references/human-review-summary.md`
- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/project-guidance.md`
- `templates/root-AGENTS.md`

Artifacts / human docs：

- `templates/decision.md`
- `templates/requirement-set-README.md` only if the current pointer fields are insufficient
- `README.md`
- `Usage.md`
- `CHANGELOG.md`

Validation：

- focused regression test
- generic valid/invalid ADR fixtures or validator
- `references/validation-scenarios.md`
- new full-validation report

## 非目标

- 不创建默认 Delivery Contract；
- 不新增 ADR lifecycle status；
- 不创建 Requirement-level 或 Feature-level ADR 目录；
- 不实现 executable Concept / State / Flow schema；
- 不设计 Design Skill 或 E2E Skill；
- 不把讲解示例中的领域行为或技术落点固化成通用要求；
- 不 bump version，除非人类另行批准。

## 批准结论

1. 采用“增强现有 ADR、不新增 mapping artifact”的方案；
2. Technical Landing Trace 是 ADR acceptance 和依赖 Feature Spec 的 hard gate；
3. effective source 变化后先进入 compatibility review，不兼容时创建 superseding ADR；
4. 实现完成后停在 Human Review Summary，不自动提交或发布；
5. 首轮实现的 validator 绕过必须以对抗性 RED/GREEN 证据修复后才可再次判定完成。
