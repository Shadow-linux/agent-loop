# Agent Loop v1.5.0 全量验证报告

日期：2026-07-23
分支：`alpha/v1.5.0`
版本：1.5.0
审计对象：基线 `7a74667bc3ce6acd99b34fc867115fbc8455b7f3` 之上的当前工作区，包含 Optional Visual Communication Adapter、README Capability Map 与 Human Docs 重写
验证方法：`docs/maintenance/full-validation-method.md`

## 总结

总分：**99/100**
等级：**STRONG**
当前 Critical / High / Medium / Low：**0 / 0 / 0 / 2**
发布判断：能力、文档、视觉资产与回归验证可进入 Human Review；本报告不授权 commit、push、tag、release、publish 或 installed Agent Loop sync。

| 检查 | 结果 |
|---|---|
| 全部 Shell tests | 41/41 PASS |
| 全部 Python tests | 277/277 PASS，69.528s（提交前最终刷新） |
| Focused visual Python tests | 19/19 PASS，0.639s（提交前最终刷新） |
| Archify workflow validate | showcase PASS，9/9，0 errors / 0 warnings |
| Archify HTML check | 9/9 PASS |
| Skill YAML / repository JSON | YAML PASS；JSON 3/3 PASS |
| Shell syntax / Markdown fence balance | Shell 42/42 PASS；Markdown 273/273 PASS |
| Repository Ruby tests | 2/2 PASS |
| SVG XML parse | PASS |
| `git diff --check` / staged diff check | PASS |

## 六域评分

| 审计域 | 结果 | 分数 | 结论 |
|---|---:|---:|---|
| Logic Correctness | PASS | 100 | Visual Trigger、Project-local → Archify → recommendation → fallback、Visual Scope、durable record 与既有 stage/status/Gate 一致；README/Usage 没有创造新运行规则 |
| Autonomy | PASS | 100 | Agent 主动判断图的价值、优先 project-local/Archify；Archify 缺失但有实质价值时先提精确建议，拒绝/不支持/失败后安全 fallback |
| Project Entry / Evidence Graph + DDD Onboarding | PASS | 99 | Project Entry、legacy evidence、核心流程完整性、Mermaid/ASCII 与 durable Archify pair 的边界一致；运行时差异仍需真实目标项目持续观察 |
| Development / Test Workflow | PASS | 100 | Requirement → Product Definition → Design Readiness/ADR → Product Slice → TDD/Verify/Review/Drift/Memory 闭环完整；轻量、Bug 和 Feature 边界清晰 |
| Memory | PASS | 100 | Markdown 继续承担 semantic authority；视觉只作为 source-bound 派生层；archive、branch 与 post-merge memory reconciliation 的事实归属未漂移 |
| Recommendation | PASS | 100 | README 能力地图与 Usage 触发语均导向唯一 owning route；Product/ADR/Feature/Git/production/close Gate 保持独立 |

## RED 基线、修复与 GREEN

### 能力实现 RED

- focused Shell 缺少 Optional Visual runtime/routing/template anchors；
- focused Python 缺少 shared visual envelope module；
- Requirement 新合同标记配旧列时可能被旧 reader 接受；
- ADR / Onboarding 起初会忽略 render-only manifest。
- Task 13 focused contract 在修订前因缺少“不得仅因 Archify 缺失就先给 Mermaid”的运行约束而 exit 1，证明 fallback-first 解释路径真实存在。
- Task 14 focused contract 在修订前因 Feature Spec 缺少 visual-specific Product Slice / `spec.md` rewrite / Requirements Discussion return contract 而 exit 1。
- 提交前人类文档校准 contract 在 README 尚未表达 Feature Spec visual boundary 时 exit 1；GREEN 后 README / Usage / CHANGELOG 同步该边界，且 Usage Onboarding 明确遵循 Archify-first recommendation 而不是 Mermaid-first。

### Human Docs 重写 RED

首次完整重写后，全部 41 个 Shell tests 中 20 PASS、21 FAIL。失败均来自已发布人类文档合同的精确锚点缺失，例如：

- `Requirement Model Technical Landing Trace`、`Requirement Lifecycle / Backlog`；
- legacy Product/Onboarding 兼容说明；
- Branch Management 的 canonical Mermaid 图；
- root guidance checker、Project Skill discovery 与版本帮助触发语。

第二轮恢复语义兼容锚点后为 39/41；补回 canonical Branch Mermaid 与 Onboarding 图源短语后为 41/41。没有恢复旧 README/Usage 的阶段堆叠和重复说明。

### GREEN

- `scripts/visual_artifact_support.py` 统一校验 path、typed JSON source、source/render digest、generator 与 validation evidence；
- Requirement 新 writer 使用 12 列 `source-render-v1`，历史六列表保持 reader-compatible；
- ADR visual 不能改变 `proposed | accepted`，Onboarding HTML-only 不能满足 required Diagram ID；
- README 以能力地图和完整 Capability Matrix 为主，Usage 以人类触发语和 Agent autonomy 为主；
- runtime/design/routing/stage/checklist/Usage 统一为“project-local → installed Archify → materially-useful recommendation → justified fallback”，旧的 fallback-first 文案已清零；
- Feature Spec visual 只解释 accepted Product Slice、feature responsibility 或 feature-local implementation/acceptance path；feature-local clarification 回写 `spec.md`，新产品语义返回 Requirements Discussion；
- 全部 41 Shell、277 Python、19 focused visual tests 与机械检查通过。

## 关键不变量

| 不变量 | 结果 |
|---|---|
| `SKILL.md` 是入口，design/runtime 是发布运行权威 | PASS |
| root Stage Map 只做 first-hop 导航 | PASS |
| Requirement `product.md` 是新产品语义权威，人类原件 byte-stable | PASS |
| Concept Foundation、Product Model 与 visuals 是 Product Definition 内部方法 | PASS |
| ADR 是条件触发的共享技术落地桥梁，不是所有 Feature 必需 | PASS |
| Feature `spec.md` 只选择 Product Slice，不重定义产品 | PASS |
| Delivery Contract 不是默认 artifact，创建/接受/breaking change 保持 Human Gate | PASS |
| Lightweight Change 只覆盖边界明确的普通非 Bug 变更 | PASS |
| 显式 Bug 保留 Bug identity，代码修复仍由 Feature 承担 | PASS |
| 行为变更保留 TDD RED；非行为 `N/A` 必须有理由 | PASS |
| Visual capability 不新增 stage/status/lifecycle，HTML-only 不是 durable truth | PASS |
| 同时仅一个 Active Feature；Pause/Resume/Close/Reopen 同步 memory | PASS |
| 部分 Phase 完成不会误关 Requirement | PASS |
| code merge 先完成，Target memory 后进行语义重写和 Human Review | PASS |
| Submit、commit、push、PR、merge、tag、release、publish、close Gate 独立 | PASS |

## 代表性压力场景

| 场景 | 结果 |
|---|---|
| Complex Requirement → Standard → visual consensus → Product Review → ADR → Feature Slice | PASS |
| Brief Requirement → `design-not-needed` → Feature Slice | PASS |
| 视觉图与 owning Markdown 不一致 | STOP，先 rewrite owning text |
| Archify unavailable 且有实质价值 | PASS，先给精确安装/使用建议，不先画 Mermaid |
| Archify 不值得安装 / install declined / unsupported / failed | PASS，Mermaid/ASCII/text fallback，不阻塞 owning stage |
| 安装授权存在但 generation/durable/Product/Git 未授权 | STOP at each independent gate |
| HTML-only 或 source/render hash/type drift | REJECT |
| legacy Requirement / Feature Product / Onboarding evidence | PASS without bulk migration |
| 低风险普通非 Bug 小改 | Persistent Lightweight Change card |
| 显式 Bug 或产品含义不清 | Bug Management / Requirements Discussion，不能降级轻量通道 |
| Auto-Loop 遇到公共接口、数据、安全、生产或 Git | STOP at Human Gate |
| 代码已 merge，两个分支记忆冲突 | Four-snapshot semantic reconciliation；不选择整边覆盖 |
| Submit 请求包含无关 dirty work 或旧验证 | BLOCK until review/fresh evidence |

## README Capability Map 审阅

- 图源：`docs/assets/agent-loop-capability-map.workflow.json`
- 交互 render：`docs/assets/agent-loop-capability-map.html`
- README render：`docs/assets/agent-loop-capability-map.svg`
- Archify：本机 active copy 已按人类授权升级，`doctor` PASS
- 视觉配置：`workflow`、Classic、static、`showcase`
- 结果：proper crossings 0、ambiguous corridors 0、label clearance issues 0、errors 0、warnings 0
- 像素审阅：主路径、Human Gate、项目理解、产品设计、执行路由、验证闭环与长期维护可区分；无截断或节点重叠

## 未采纳或降级意见

- 未把 Archify 设为 mandatory helper：视觉由内容复杂度触发，不能给简单任务增加固定成本。
- 未让 HTML/SVG 成为产品或技术真相：继续使用 `render to converge, text to record`。
- 未把全部能力画成 all-to-all 关系网：图只表达主路径和支撑域，README Capability Matrix 承担完整枚举。
- 未删去 Branch Mermaid：它是现有回归合同与人类理解发布/客户/开发分支关系的权威派生图。
- 未修改 Skill version：当前仍是经人类批准的 v1.5.0。

## 当前问题与残余风险

当前无未解决 Critical、High 或 Medium。

两个 Low 与专项评分一致：

- 新 writer 明确要求 `source-render-v1`，但无 contract marker 的文档仍会进入 Proposal 要求保留的 legacy visual reader；validator 无法只凭文档内容机械区分历史输入与新 writer 漏标。
- 人类拒绝 Archify 后进入 fallback 的运行语义已经明确，但尚缺少“同一范围不得跨轮重复推荐”的直接 mutation contract。

另一个长期观察边界是：不同 CLI Agent 是否能在真实项目中稳定发现 Archify、正确判断“materially improve review”、执行 Visual Scope Grant，并持续遵守“图收敛、文字落库”，仍需要后续目标项目使用证据。这些边界保留人类拒绝与 Markdown/Mermaid/ASCII fallback，不阻塞 Product、ADR、Feature Spec 或 Onboarding。

## 工作区与授权

- Archify 已按人类授权更新到 active Codex copy并通过 doctor；
- 未同步本仓库 Agent Loop 到任何 installed Agent Loop copy；
- `.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/` 保持 untracked，不应纳入提交；
- 未 stage、commit、push、tag、PR、merge、release 或 publish；
- 下一步：Human Review 当前 diff、能力地图与验证报告。
