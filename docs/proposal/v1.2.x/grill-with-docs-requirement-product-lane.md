# Proposal: grill-with-docs Requirement / Product Lane

状态：讨论草案
目标版本：v1.2.4
创建时间：2026-06-30

## 目的

这份 proposal 讨论如何把 mattpocock `grill-with-docs` 融入 `agent-loop` 的需求沟通、需求文档和 Product Brief 链路。

目标不是直接引入 `grill-with-docs` 的原生目录结构，而是借用它的工作方法：

- 拷问计划是否符合项目领域语言；
- 澄清模糊术语；
- 用具体场景压出边界；
- 先查代码和现有文档，再问人类；
- 在决策信号出现时，交给 Decision Scan，而不是直接创建 ADR。

## 核心观点

```text
grill-with-docs 是需求澄清和领域语言拷问工具，不是 PRD 生成器，也不是 ADR 生成器。
grill-with-docs 早介入；to-prd 晚合成；Decision Scan 再抽取长期决策候选。
```

它最适合在需求还没有完全沉淀成 product.md / PRD 之前使用，让后续 `to-prd` 和 Feature Spec 有足够清晰的输入。

## 定位

| 能力 | 在 agent-loop 中的定位 | 不负责 |
|---|---|---|
| grill-with-docs | grill-with-docs = 问清楚领域语言、业务场景、边界和矛盾 | 不直接生成最终 PRD，不直接接受 ADR |
| to-prd | to-prd = 将已知上下文合成为 product.md / PRD-like Product Brief | 不采访用户，不决定长期架构 |
| Decision Scan | Decision Scan = 从 product.md / PRD 中识别长期、跨 feature、难逆转、有 trade-off 的决策候选 | 不要求每个候选都创建 decision file |

推荐组合：

```text
Grill = 问清楚
Requirement = 保存人类确认后的需求来源与状态
Product Brief / to-prd = 合成产品意图
Decision Scan = 判断哪些候选需要长期沉淀
Feature Spec = 转成工程行为规格
```

## 介入时机

`grill-with-docs` 应该作为需求和产品阶段的辅助方法，而不是新的独立大阶段。

| agent-loop 阶段 | 是否适合使用 | 用法 |
|---|---:|---|
| Requirements Discussion | 是 | 当需求有模糊术语、领域边界、用户角色、业务流程、异常场景时，逐个追问 |
| Requirement Archive | 是 | 把已确认的术语、场景、来源、开放问题写入 requirement set |
| Delivery Phases | 是 | 用具体场景检查 phase 是否真能闭环，是否混入后续阶段能力 |
| Product Brief If Needed | 是 | 在 `to-prd` 或 fallback product synthesis 前补齐产品上下文 |
| Decision Scan | 是 | 把 hard-to-reverse / surprising / real trade-off 信号交给 Decision Scan |
| Feature Spec | 轻量使用 | 检查 spec 术语、范围和业务规则是否与 requirement/product 一致 |
| Technical Design / Plan | 非默认 | 只有领域概念或业务边界冲突时再使用 |

## 工作流

```text
需求沟通 / 初始想法
→ grill-with-docs 澄清
→ requirement README / requirement.md
→ Delivery Phases 可选
→ to-prd / Product Brief 合成
→ Decision Scan
→ Feature Spec
```

阶段含义：

1. 人类提出需求或想法，Agent 先判断是 ordinary chat、Requirements Discussion，还是明确 Feature Request。
2. 如果进入 Requirements Discussion，Agent 可使用 grill-with-docs 方法澄清术语、边界、具体场景和冲突。
3. 人类确认后，写入 requirement set；原始 source material 保留，整理后的需求进入 `requirement.md` / `README.md`。
4. 如果需求复杂，先整理 Delivery Phases，让人类知道现在做什么，后面做什么。
5. 当上下文足够明确，再用 `to-prd` 或本地 Product Brief 规则合成 `product.md`。
6. `product.md` 和 `to-prd` 的 Implementation / Testing Decisions 进入 Decision Scan。
7. Feature Spec 只承接已确认的 requirement、product 和 applicable decisions。

## 提问原则

`grill-with-docs` 的价值在于追问，但在 agent-loop 中不能变成无限访谈。

规则：

- 一次只问一个阻塞问题。
- 先查已有 project memory、requirement source、product.md、代码和文档；能从事实中回答的问题，不先问人类。
- 每个问题都给出 Agent 推荐答案，降低人类决策成本。
- 只问会影响 scope、用户、业务流程、数据、权限、验收、测试或长期决策的问题。
- 当术语模糊时，提出 canonical term，并列出应避免的别名。
- 当人类说法和现有 Domain Language / code reality 冲突时，立即指出冲突并要求选择。
- 用具体场景追问边界，尤其是失败路径、异常恢复、权限差异、状态变化和多角色协作。
- 不要把普通闲聊升级为文档，除非人类确认要整理需求。

提问前的过往 feature 查找：

- 提问前先检查相关过往 feature 的 `product.md`、`spec.md`、`tests.md`、`notes.md`，如果它们可能已经定义了术语、业务规则、验收方向或历史决策。
- 不做全量 feature 扫描；只按 targeted lookup 查找与当前问题直接相关的历史材料。
- targeted lookup 的线索包括关键词、领域对象、相关 requirement、相同模块/流程、active/paused/recent feature。
- 如果过往 feature 与当前说法冲突，先指出冲突，再问人类选择沿用、覆盖、还是作为新需求处理。

问题形态：

```text
我看到这里的“账户”可能有两个含义：User Account 和 Wallet Account。
推荐把登录主体叫 User，把资金主体叫 Wallet。
这个需求里你说的“账户余额”是指 Wallet balance 吗？
```

## 输出映射

`grill-with-docs` 原生路径和 agent-loop 路径不同。不要采用 grill-with-docs 的原生输出路径。

| grill-with-docs 原生概念 | agent-loop 映射 | 规则 |
|---|---|---|
| CONTEXT.md | `project.md Domain Language` 或 enterprise `.agent-loop/project/*.md` | 只有长期领域语言才回补 project memory，且需要人类确认 |
| CONTEXT-MAP.md | enterprise project memory 中的 contexts / boundaries | 不为普通项目默认创建 |
| docs/adr/ | `.agent-loop/decisions/` | 只通过 Decision Scan 和 human gate 创建 |
| resolved term | requirement README / product.md terminology | 当前需求或 feature 内术语先写局部 artifact |
| ambiguous term | requirement README Open Questions / product.md Open Product Questions / notes.md | 尚未确认前不写成长期事实 |
| concrete scenario | requirement.md / product.md User Stories / Acceptance Direction | 根据阶段写入需求或产品层 |
| conflict with code | notes.md 或 Recovery / Drift 记录 | 如果影响长期事实，后续回补 project memory |

禁止行为：

- 不要直接创建 CONTEXT.md。
- 不要直接创建 docs/adr/。
- 不要把 implementation details 写入 Domain Language。
- 不要把未确认术语写入 project.md。

## Requirement 文档生成关系

`grill-with-docs` 最适合服务 Requirements Discussion 阶段。

在这个阶段：

- grill-with-docs 负责把需求问清楚；
- requirement.md 记录人类确认后的需求表述；
- README.md 记录来源、状态、Delivery Phases、开放问题和术语；
- Product Brief / product.md 不拥有 requirement lifecycle；
- feature `spec.md` 只能从已确认 requirement / product 中派生。

推荐 requirement README 增加这些局部信息，而不是直接写 project memory：

```md
## Terminology

| Term | Meaning In This Requirement | Avoid / Ambiguity |
|---|---|---|
| Wallet | 用户资金账户 | 不要和登录 User Account 混用 |

## Open Product Questions

| Question | Recommended Answer | Status |
|---|---|---|
| 余额不足时是否允许继续调用 LLM？ | 不允许，返回余额不足并停止服务 | proposed |
```

当术语后来被多个 feature 复用，Project Memory Update 再建议把它提升到 `project.md Domain Language`。

## 与 to-prd 的关系

`to-prd` 不负责采访用户。它适合在上下文已经足够明确后，把当前 conversation context 和代码理解合成为 PRD-like Product Brief。

因此：

```text
grill-with-docs 负责补齐 to-prd 之前缺失的上下文。
to-prd 负责将已知上下文合成为 product.md。
```

映射规则：

`to-prd` 的 `Implementation Decisions` 和 `Testing Decisions` 不能直接等同于 ADR。它们只是 Product Brief 之后的候选输入，必须经过 Decision Scan 分流。

| to-prd 字段 | agent-loop 去向 | 备注 |
|---|---|---|
| Problem Statement | `product.md` | 来自已确认需求 |
| Solution | `product.md` | 用户视角方案 |
| User Stories | `product.md`，后续转入 `spec.md` | 应覆盖核心和异常路径 |
| Implementation Decisions | `product.md` 初稿 + Decision Scan 输入 | 不直接等于 ADR |
| Testing Decisions | `tests.md` 输入 + Decision Scan 输入 | 复杂目标同步到 decision verification |
| Out of Scope | requirement README / product.md / spec.md | 防止实施时漂移 |
| Further Notes | `notes.md` 或 product.md 补充 | 不作为长期事实 |

`to-prd` 默认发布 issue tracker 的行为不应在 agent-loop 中默认执行。除非人类明确要求，否则输出应写入 `product.md` 或 proposal 中指定的 agent-loop artifact。

## 与 Decision / ADR 的关系

grill-with-docs 可以发现 decision point，但不直接创建 accepted decision。

当追问过程中出现以下三类信号时，进入 Decision Scan：

| Signal | Meaning | Next |
|---|---|---|
| Hard to reverse | 改错成本很高，例如数据模型、支付流程、外部依赖 | 建议 decision candidate |
| Surprising without context | 未来读者会问为什么这样做 | 建议记录原因 |
| Real trade-off | 存在多个合理方案且选择会排除其他路线 | 建议比较 options |

这些信号进入 Decision Scan，而不是直接写成 ADR。

Decision Scan 再决定：

- 留在 `product.md`；
- 写进 `spec.md` 的 `Design Decisions`；
- 写进 `tests.md`；
- 建议创建 `.agent-loop/decisions/*.md`；
- 或作为 Human-gated question 继续澄清。

## Human Gate

`grill-with-docs` 可以作为提问和分析方法自动使用，但写入 artifact 仍遵守 agent-loop gate。

需要人类确认的动作：

- 开始正式 requirement 文档整理需要人类确认；
- 创建 requirement set 需要人类确认；
- 写入 project.md Domain Language 需要人类确认；
- 创建 product.md 需要人类确认；
- 创建 .agent-loop/decisions/*.md 需要人类确认；
- 将局部术语提升为长期项目语言需要人类确认；
- 把一个模糊答案标记为 accepted 需要人类确认。

Agent 可自主执行：

- 识别模糊术语；
- 基于代码和文档回答可发现问题；
- 提出推荐答案；
- 汇总 unresolved questions；
- 建议是否进入 Product Brief、Decision Scan 或 Feature Spec。

## 与现有 agent-loop 设计的关系

这份 proposal 不增加新的正式 stage，而是增强现有阶段的方法：

```text
Requirements Discussion
Product Brief If Needed
Decision Scan
Feature Spec
```

它保持这些边界：

- `requirements/` 保存人类源需求和 lifecycle；
- `product.md` 是 feature-level 产品理解；
- `spec.md` 是工程行为规格；
- `.agent-loop/decisions/` 只保存长期 / 跨 feature 决策；
- `project.md` 只保存当前长期事实和索引，不保存完整访谈过程。

## 待讨论问题

- 是否要把 `Terminology` 和 `Open Product Questions` 固定加入 requirement README 模板？
- grill-with-docs 是否应该成为 Requirements Discussion 的 preferred helper，还是只在术语/边界复杂时触发？
- Product Brief 是否应该明确区分 `to-prd synthesis` 和 `grill clarification notes`？
- 是否需要独立 `references/requirement-product-grill.md`？
- 是否需要为 grill 问答增加 response-local pending record，避免无 feature workspace 时丢失上下文？
