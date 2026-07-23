# Agent Loop v1.3.0 全量验证报告（ADR Technical Landing）

状态：**已被后续审查否定并由 `.2` 修复验证取代**。本文件保留首轮实现的历史证据，不代表当前工作区结论。后续审查发现 proposed/accepted Human Gate 顺序、source-wide scope、外部引用、Hard Gate、Design Slice、operational inventory 和 not-needed 分支存在可复现漏洞；详见 `agent-loop-v1.3.0-adr-technical-landing-review-red-2026-07-13.md`。

日期：2026-07-13

分支：`alpha/v1.3.0`

版本：`1.3.0`

审计对象：当前未提交工作区，包含 approved proposal、Effective Requirement Snapshot、Requirement Model Technical Landing Trace、Coverage Hard Gate、Upstream Compatibility / Drift、Decision & Design Human Review Summary、triggered operational landing、root guidance、领域中立 validator 和回归证据。

同日已有 `docs/reports/agent-loop-v1.3.0-full-validation-2026-07-13.md` 属于 Concept Foundation 历史审计，本轮不覆盖该证据，使用 `.1` 保存新报告。

## 总体结论

| 项目 | 结果 |
|---|---|
| 总分 | **98 / 100** |
| 等级 | **STRONG** |
| 修改前全部测试 | `31/31 PASS` |
| Focused contract | PASS |
| 修改后全部 `tests/*.sh` | `32/32 PASS` |
| Validator valid trace | 6 Requirement Model IDs：3 landed / 1 existing-decision / 1 feature-local / 1 not-applicable |
| Validator invalid fixtures | 5/5 被拒绝 |
| Critical / High / Medium | `0 / 0 / 0` |
| Low | 2 |

结论：ADR 已能作为 accepted Requirement Product Model 到技术落地的可追踪桥梁，且仍是产品语义的消费者而非拥有者。本轮没有新增 canonical stage、默认 mapping artifact、ADR lifecycle status 或 executable schema。

## 六域评分

| 审计域 | 权重 | 结果 | 评分 | 主要证据 |
|---|---:|---|---:|---|
| Logic Correctness | 20% | PASS | 98 | runtime 固定 snapshot、trace、coverage、compatibility 和 supersede 顺序；validator 拒绝缺失 coverage、空 landing、未接受/重开 source 和 `review-required`。 |
| Autonomy | 15% | PASS | 97 | Agent 先解析 effective pointer 和模型 scope，自主计算 coverage，只将产品语义、非落地 disposition、compatibility 和 supersede 真正决策交给人类。 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | PASS | 98 | canonical Stage Order 未改；root Stage Map 仍仅导航到 Decision & Design，只增加必要 stop/completion/artifact 提示。 |
| Development / Test Workflow | 20% | PASS | 99 | 保留正确 RED，实现结构 parser 而非只做关键词断言，混合 disposition valid fixture 与 5 类 invalid fixture 全部按预期运行。 |
| Memory | 15% | PASS | 98 | README effective pointer 是当前 source 索引；accepted ADR 历史不被改写，不兼容技术决策通过 superseding ADR 保留审计链。 |
| Recommendation | 15% | PASS | 98 | 缺 source 回 Requirement Archive / Requirements Discussion，产品语义 blocker 回 Human Grill，coverage 缺失保持 proposed，compatibility 回 Decision & Design，技术结论失效进 supersede。 |

加权得分为 98.05，按整数记为 98。

## RED 基线与 GREEN 证据

修改 runtime/template 前，全部已有测试为：

```text
BASELINE passed=31 failed=0
```

新增 focused contract 后首次运行：

```text
FAIL: SKILL.md missing required text: Effective Requirement Snapshot
```

该 RED 因现有发布入口没有 snapshot/trace contract 而失败，不是 Shell 语法或拼写错误。完整证据保存于 `docs/reports/agent-loop-v1.3.0-adr-technical-landing-red-baseline-2026-07-13.md`。

GREEN 输出：

```text
PASS: ADR technical landing trace covers 6 requirement-model IDs with 3 landed rows
PASS: ADR Requirement Model Technical Landing Trace contract is complete
FULL_SUITE passed=32 failed=0
```

领域中立 validator 同时证明：

- `landed`、`covered-by-accepted-decision`、`feature-local` 和 `not-applicable` 都有可执行规则；
- snapshot 内每个 Requirement Model ID 必须恰好有一个 trace row；
- `landed` 必须有 Technical Landing、Preserved Invariant、Design Slice 和 Verification；
- existing-decision 必须指向 ADR reference，feature-local 必须指向 `spec.md`，not-applicable 必须有具体 reason；
- `candidate`、`reopened`、`review-required`、missing coverage 和 empty landing 均无法进入 acceptance。

## 已通过的跨文件不变量

- `SKILL.md` 仍是简洁入口，详细合同在 runtime/design/project-decisions。
- Effective Requirement Snapshot 和 Technical Landing Trace 是 Decision & Design 内部方法/记录部分，不是 stage。
- requirement README effective pointer、effective source status 和 ADR snapshot 必须一致。
- PRD / Requirement Product Model 继续拥有 Concept、relationship、role/permission、command/event、flow、state、invariant、recovery 和 fact ownership。
- ADR 只记录 unchanged meaning reference 和技术落地，含义不足时回 Requirements Discussion。
- Coverage Hard Gate 同时阻止 ADR acceptance 和依赖的 Feature Spec、Plan、implementation。
- `review-required` 仅是 dependency availability judgment；`Allowed Status` 仍为 `proposed | accepted | superseded | deprecated`。
- accepted ADR 技术结论失效时建立 superseding ADR，不原地改写 decision meaning。
- Operational landing 先分类 `triggered | not-triggered`；只有 triggered concern 产生对应详细章节。
- Human Review Summary 显示 source、coverage 数量、技术决策、语义保留、operational trigger、Design Slice、verification 和人类决定。
- root guidance 修订为 `block-version:1.3.0-20260713.1`，全部 13 个 managed blocks 一致。
- 没有创建仓库根 `.agent-loop/`、mapping directory、YAML/JSON schema 或新的 ADR status。

## 代表性压力场景

| 场景 | 结果 | 结论 |
|---|---|---|
| README pointer 已换源，ADR 仍引用旧 source | PASS | 进入 `review-required`，停止新依赖工作。 |
| 部分 State / Recovery model row 没有落点 | PASS | ADR 保持 proposed，Feature Spec 被阻止。 |
| 人类要求在 ADR 里补产品定义 | PASS | 回 Requirements Discussion / Human Grill，ADR 不填补。 |
| accepted ADR 的一致性边界已失效 | PASS | 保留原记录，Human Review 后新建 superseding ADR。 |
| 用 feature-local / not-applicable 隐藏共享约束 | PASS | 必须给 owner/spec、verification 或具体 reason，并在 Human Review 中显示。 |
| 无迁移/兼容/上线变化仍要写满 operational 章节 | PASS | 只记录 not-triggered 理由，不展开空章节。 |
| 简单单 Feature 需求 | PASS | 既有 `design-not-needed` 路径不受影响，不强制 ADR。 |
| Product Brief Source Gate / Delivery Contract Gate / TDD / Active Feature / Pause-Resume-Close-Reopen / multi-phase roll-up / Follow-up / Submit / stale-memory / Chat | PASS | 原有控制面在 `32/32` 全量回归中继续通过。 |

## 当前问题

### Low-1：Validator 信任 ADR 声明的 coherent scope

证据：`references/project-decisions.md:170`、`scripts/check-adr-requirement-model-trace.rb:124-152`。

风险：Validator 能证明 snapshot 声明的所有 model ID 都有 trace，但无法仅从 Markdown 自动判断 Agent 是否为了避免落地而错误缩小 ADR scope。

处理：scope 外模型必须由 accepted decision、feature-local placement、其他 decision 或具体 not-applicable 说明，并在 Decision & Design Human Review 展示。这是人类决策而非 schema 能证明的业务真实性，故为 Low。

### Low-2：Validator 证明引用形状，不单独证明外部 artifact 当前真实状态

证据：`scripts/check-adr-requirement-model-trace.rb:181-187`。

风险：Parser 要求 existing-decision 具有 ADR reference、feature-local 具有 `spec.md` 引用，但不仅凭单个 ADR 文件确认被引用 decision 当前必然 accepted 或 Feature Spec 已获人类确认。

处理：runtime 要求读取已链接 decision/spec 和状态，Human Review Summary 展示 owner/verification；不在本轮引入 executable schema 或跨文件生成器，故为 Low。

## 未采纳或降级意见

- 未新建 requirement-to-technical mapping artifact：会引入第二个同步对象，与 approved 方案 A 冲突。
- 未把 Effective Snapshot、Coverage Review 或 Compatibility Review 升级为 canonical stage：它们是 Decision & Design 内部方法和 gate。
- 未新增 `review-required` ADR status：它仅表示依赖可用性。
- 未把业务名词、业务动作、vendor、store、protocol 或 rollout topology 写入通用 template/validator。
- 未默认生成 Migration / Rollout / Rollback 章节：只有 trigger assessment 为 triggered 时生成对应详细。
- 未引入 YAML / JSON executable schema：当前 Ruby validator 仅验证 Markdown 结构与可追踪性。

## 范围漂移检查

- 已实现 proposal 要求的 Effective Requirement Snapshot、Technical Landing Trace、Coverage Hard Gate、Upstream Compatibility / Drift、Decision & Design Human Review Summary 和 triggered operational landing。
- 已协调 `SKILL.md`、runtime、design、project-decisions、stage guides、checklists、human review、decision template、root guidance、README、Usage、CHANGELOG、scenarios 和 tests。
- 未修改 `templates/requirement-set-README.md`：现有 `Effective Concept Foundation` pointer 已能支持 snapshot 解析，无需增加字段。
- 未新增 canonical stage、mapping artifact、lifecycle status、executable schema 或目标项目 `.agent-loop/`。
- 版本仍为 `1.3.0`；root managed blocks 只从同日首次修订提升到 `1.3.0-20260713.1`。

## 结构与机械检查

- `SKILL.md` YAML：PASS
- `plugin.json` JSON：PASS
- `scripts/check-adr-requirement-model-trace.rb` Ruby 语法：PASS
- `scripts/check-concept-foundation-trace.rb` Ruby 语法：PASS
- 全部 Shell 语法：PASS
- 变更/新增 Markdown fence：PASS
- 本轮 diff 和 untracked 文件尾随空白：PASS
- `git diff --check`：PASS
- `SKILL.md` / `plugin.json` / `README.md` / `Usage.md` 版本一致：PASS（`1.3.0`）
- root managed block revision：PASS（13/13 为 `1.3.0-20260713.1`）
- target-project `.agent-loop/` guard：PASS
- fixture-specific domain/action/technology token 未进入 template/validator：PASS

## 发布与授权判断

当前实现可进入 Human Review，但报告不构成提交或发布授权。

| 操作 | 是否授权 |
|---|---|
| commit | 否 |
| push | 否 |
| tag | 否 |
| PR / merge | 否 |
| release / publish | 否 |

推荐的唯一下一阶段：**Human Review**。
