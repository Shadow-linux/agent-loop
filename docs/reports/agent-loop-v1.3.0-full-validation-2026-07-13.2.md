# Agent Loop v1.3.0 全量验证报告（ADR Technical Landing 审查修复）

日期：2026-07-13

分支：`alpha/v1.3.0`

版本：`1.3.0`

审计对象：当前未提交工作区；包含 ADR Requirement Model Technical Landing Trace 首轮实现、审查 RED、Human Gate / Scope Inventory / validator 修复、Requirement Product Model `PERM-*` / `EX-*` 增强及协调文档。

本报告取代同日 `.1` 报告的当前结论；`.1` 仅保留首轮实现的历史证据。

## 总体结论

| 项目 | 结果 |
|---|---|
| 总分 | **99 / 100** |
| 等级 | **STRONG** |
| 全部 `tests/*.sh` | `32/32 PASS` |
| ADR focused contract | PASS |
| 对抗性 validator contract | 16/16 场景符合预期 |
| Valid accepted ADR | 8 个 in-scope Requirement Model IDs，5 个 `landed` |
| Valid not-needed ADR | proposed preflight PASS，无伪造产品模型 |
| Concept Foundation trace | 5 Concepts，26 个 model rows |
| Root managed blocks | 13/13 为 `1.3.0-20260713.2` |
| Critical / High / Medium | `0 / 0 / 0` |
| Low | 2 个明确边界，不阻塞 Human Review |

结论：修复后的 ADR lane 能把 accepted Requirement Product Model 可靠落到 source-wide scope、技术落点、Design Slice 和 Verification，同时保持 PRD 的产品语义所有权与 ADR 的独立 Human Gate。首轮评审发现的 Gate 绕过已具备 RED/GREEN 回归，当前没有 Critical、High 或 Medium 问题。

## 六域评分

| 审计域 | 权重 | 结果 | 评分 | 主要证据 |
|---|---:|---|---:|---|
| Logic Correctness | 20% | PASS | 99 | `proposed -> preflight -> Human Review -> accepted + evidence -> accepted validation` 顺序一致；source/scope/snapshot/trace 做集合校验；状态、引用、Hard Gate、operational detail 均结构化验证。 |
| Autonomy | 15% | PASS | 99 | Agent 自动解析 effective source、抽取 `REL/PERM/CMD/EVT/FLOW/STATE/PM/EX`、计算 scope/coverage、验证 artifact；只把产品语义、scope 裁决和 ADR acceptance 留给人类。 |
| Project Entry / Evidence Graph + DDD Onboarding | 15% | PASS | 98 | canonical Stage Order 未变；root guidance 只增加 stop/completion/artifact 导航，13 个 managed block revision 同步。 |
| Development / Test Workflow | 20% | PASS | 100 | 保留首轮 RED 与审查 RED；16 场景对抗 contract、focused tests、32/32 全量回归和机械检查全部通过。 |
| Memory | 15% | PASS | 99 | requirement README effective pointer 继续定位产品语义；source-wide inventory 防静默丢失；accepted ADR 不兼容时 supersede 而非改写历史。 |
| Recommendation | 15% | PASS | 99 | 缺模型意义回 Requirements Discussion；缺 coverage 保持 proposed；compatibility 回 Decision & Design；accepted 结论失效进入 Human-gated supersede。 |

加权分为 99.05，按整数记为 99。

## 首轮审查 RED

首轮实现的机械 suite 虽为 `32/32 PASS`，但临时同源变异证明了 10 个错误接受和 2 个合法输入误拒绝：

- accepted ADR 无 Human Review Evidence 仍通过；
- placeholder `reason: n/a`、任意 Hard Gate、垃圾 ID、silent scope omission 仍通过；
- 不存在的 accepted decision / Feature Spec、非法 Design Slice status 仍通过；
- triggered detail 缺失和 operational concern inventory 残缺仍通过；
- proposed preflight 和 reasoned `concept-foundation-not-needed` 合法分支被误拒绝。

完整 RED 证据见 `agent-loop-v1.3.0-adr-technical-landing-review-red-2026-07-13.md`。因此 `.1` 的 `98/100` 与 `0 High / Medium` 结论已被明确标记为失效历史结论。

## GREEN 修复证据

### Human Gate 顺序

- `scripts/check-adr-requirement-model-trace.rb:176-184`：`proposed` 只做结构预检；`accepted` 必须有 `Decision: accepted`、确认人、ISO 日期和具体证据。
- `references/runtime.md:123-127`：validator pass 只允许请求评审，不授予 acceptance；reasoned not-needed 使用独立分支。
- `templates/decision.md:209-236`：完整 Hard Gate、preflight 指引与 Human Review Evidence 写入同一 ADR。

### Source-Wide Scope 与模型完整性

- `scripts/check-adr-requirement-model-trace.rb:325-342`：source model 集合覆盖 `REL/PERM/CMD/EVT/FLOW/STATE/PM/EX`。
- `scripts/check-adr-requirement-model-trace.rb:364-413`：Scope Inventory 必须与 source 集合相等，in-scope 必须与 snapshot/trace 集合相等。
- `scripts/check-concept-foundation-trace.rb:179-190`：Role / Permission Matrix 使用稳定 `PERM-*` ID。
- `scripts/check-concept-foundation-trace.rb:260-288`：Exception Paths 使用稳定 `EX-*`，并校验 Concept / State / Action 引用。

### 外部引用、Hard Gate 与 Operational Landing

- `scripts/check-adr-requirement-model-trace.rb:145-174`：decision/spec 路径限制在 workspace；existing artifact 校验 status；未来 owner 必须显式 `planned:`。
- `scripts/check-adr-requirement-model-trace.rb:186-200`：Hard Gate 必须与规范清单精确相等，缺项、未勾选、重复或额外伪检查均拒绝。
- `scripts/check-adr-requirement-model-trace.rb:202-236`：四项 operational concern 必须完整；trigger 与 detail heading 一致；全部未触发时禁止空 detail section。
- `scripts/check-adr-requirement-model-trace.rb:276-297`：Design Slice ID、owner、verification 和状态均受验证。

## 对抗性回归结果

| 类别 | 场景 | 结果 |
|---|---|---|
| 正向 | proposed ADR 在 Human Review 前 structural preflight | PASS |
| 正向 | accepted ADR 带 Human Review Evidence | PASS |
| 反向 | accepted ADR 缺 Human Review Evidence | 正确拒绝 |
| 正向 | 显式 `planned:features/<id>/spec.md` owner | PASS |
| 正向 | source model 明确委派给 existing proposed decision | PASS |
| 反向 | placeholder not-applicable reason | 正确拒绝 |
| 反向 | Hard Gate 被任意 checkbox 替换 | 正确拒绝 |
| 反向 | Hard Gate 夹带额外伪检查 | 正确拒绝 |
| 反向 | Accepted Requirement Model IDs 含垃圾 token | 正确拒绝 |
| 反向 | source model 从 snapshot/trace 静默删除 | 正确拒绝 |
| 反向 | 不存在的 accepted decision | 正确拒绝 |
| 反向 | 不存在的 Feature Spec | 正确拒绝 |
| 反向 | 非法 Design Slice status | 正确拒绝 |
| 反向 | triggered concern 缺 detail | 正确拒绝 |
| 反向 | operational concern inventory 不完整 | 正确拒绝 |
| 正向 | reasoned not-needed ADR 无产品模型 | PASS |

## 已通过的跨文件不变量

- `SKILL.md` 保持简洁入口；详细规则位于 runtime/design/project-decisions/stage/checklist/template。
- Effective Requirement Snapshot、Scope Inventory、Technical Landing Trace 和 preflight 是 Decision & Design 内部方法，不是 canonical stage。
- ADR status 仍只有 `proposed | accepted | superseded | deprecated`；`review-required` 只表示 dependency availability。
- effective requirement source 继续拥有 Concept、relationship、permission、action、flow、state、product fact、invariant 与 exception/recovery 产品意义。
- ADR 不创建或重定义产品语义；含义缺失回 Requirements Discussion / Human Grill。
- Scope Inventory 位于现有 ADR 内，没有新增默认 mapping artifact 或 YAML/JSON executable schema。
- `Applicable Decisions` 只证明 awareness，不替代 scope/trace/slice/verification coverage。
- Operational landing 仍为 trigger-based，不默认引入退款、对账、迁移或任何示例业务能力。
- accepted ADR 不兼容时创建 superseding ADR，原 accepted decision 保持可审计。
- root guidance revision 为 `1.3.0-20260713.2`，13/13 managed blocks 一致。
- 没有创建仓库根 `.agent-loop/`，没有修改 skill version。
- Delivery Contract、Submit、Commit、PR、Merge、Release、Publish 与 Tag 的 Human Gate 均未被改动或绕过。

## 代表性压力场景

| 场景 | 结果 | 路由 |
|---|---|---|
| source 中 permission / exception 被从 ADR 静默删除 | PASS | Scope Inventory mismatch，ADR 保持 proposed。 |
| validator 通过后要求自动 accepted | PASS | 停在 Human Review；无 evidence 不能 accepted-mode PASS。 |
| existing-decision / spec 路径伪造 | PASS | 文件或 status 校验失败。 |
| 下游 Feature Spec 尚未创建 | PASS | 只能写显式 canonical `planned:` path，并在 Human Review 可见。 |
| Concept Foundation not-needed 但共享技术约束仍需 ADR | PASS | trace-not-applicable，不伪造产品模型。 |
| requirement effective source 变化 | PASS | `review-required`，停止新的依赖工作并复核/supersede。 |
| Product Brief Source Gate / Delivery Contract / TDD / Active Feature / Pause-Resume-Close-Reopen / multi-phase / Follow-up / Submit / stale-memory / Chat | PASS | 原有 32 项全量 suite 继续通过。 |

## 当前边界

### Low-1：Markdown 证据不能证明人类身份真实性

证据：`scripts/check-adr-requirement-model-trace.rb:176-184` 能证明 accepted ADR 记录了完整 Human Review Evidence，但不能从 Markdown 单独证明确认人身份或 UI 交互真实性。

处理：运行规则明确要求先展示 Human Review Summary 并等待显式人类接受；validator 只做落盘一致性检查，永不授予 acceptance。该边界不能通过伪造自动化审批来“修复”。

### Low-2：显式 planned owner 只证明未来路径清晰

证据：`scripts/check-adr-requirement-model-trace.rb:149-174` 对 `planned:` 路径做 canonical path 与 workspace confinement 验证，但按设计不要求尚未创建的 Feature Spec 文件存在。

处理：planned owner 必须在 Human Review 可见；Feature Spec 创建后，Feature Spec / Drift / Completion 继续验证 Applicable Decision、Design Slice 与证据。没有 `planned:` 前缀的引用必须立即解析到真实 artifact 和有效 status。

## 结构与机械检查

- `SKILL.md` YAML：PASS
- `plugin.json` JSON：PASS
- 全部 Ruby 语法：PASS
- 全部 Shell 语法：PASS
- 全仓 Markdown fence balance：PASS
- tracked diff 与 untracked 文件尾随空白：PASS
- `git diff --check`：PASS
- 版本同步：`SKILL.md` / `plugin.json` / `README.md` / `Usage.md` 均为 `1.3.0`
- root managed block revision：13/13 为 `1.3.0-20260713.2`
- canonical Stage Order：未新增 stage
- target-project `.agent-loop/` guard：PASS
- 默认 mapping artifact / executable schema guard：PASS

## 范围与授权

- 未 bump version；
- 未创建 target-project artifacts；
- 未提交、推送、打 tag、创建 PR、merge、release 或 publish；
- 当前唯一下一阶段：Human Review。

| 操作 | 是否授权 |
|---|---|
| commit | 否 |
| push | 否 |
| tag | 否 |
| PR / merge | 否 |
| release / publish | 否 |
