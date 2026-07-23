# Optional Visual Communication Adapter 单功能验证报告

> 方法：`docs/maintenance/feature-validation-method.md`（五域 100 分模型）。所有攻击用例与测试数字均由本 Agent 独立构造、实时重跑，未采信实施方报告结论。

## 1. 审计对象与 Scope Lock

- 日期：2026-07-23；分支：`alpha/v1.5.0`；Skill 版本：`1.5.0`（未升级）
- 审计对象：HEAD `7a74667`（`feat(v1.5.0): 引入自适应需求产品定义`）之上的**当前工作区未提交改动**（21 个修改文件 + 新增 `scripts/visual_artifact_support.py`、`tests/test_optional_visual_communication_adapter.py`、`tests/validate-optional-visual-communication-adapter.sh`）
- 目标行为（`docs/proposal/v1.5.x/optional-visual-communication-adapter.md`）：Archify 作为 Optional Visual Communication Adapter——Visual Trigger 成立时 preferred 而非 mandatory；未授权不安装；有边界的 Visual Scope Grant 支持同问题多轮迭代；semantic authority → diagram source → render 三层模型；新 durable visual 使用 `source-render-v1`（typed JSON source + validated render + 双 SHA-256 + generator@version + validation evidence）；HTML-only 不能充当新长期 Diagram Artifact；旧 render-only reader 兼容
- 非目标：不 vendor Archify、不进 mandatory helper 表、不新增 stage/intent/lifecycle/Auto Mode、不改版本、root-AGENTS 默认不改

## 2. 总分与定级

**总分：91 / 100，等级：STRONG**（无 Critical/High；1 个 unresolved Medium 不触发 hard cap）

- Critical：0；High：0；Medium：1；Low：1
- 机械基线（本 Agent 实时统计）：Shell **41/41**；Python discover **277/277 OK**；focused shell PASS；focused Python **19/19 OK**；`git diff --check` OK——与实施方声明一致但为独立复跑

## 3. 五域评分表

| Domain | 权重 | 得分 | 加权 | 结论 |
|---|---:|---:|---:|---|
| Requirement And Scope Fidelity | 15 | 13 | 13.0 | 验收 18 条中 17 条独立验证通过；#9 的 Feature Spec 部分缺失（M1） |
| Logic, State, And Human Gates | 30 | 28 | 28.0 | Grant/Install/三层模型/Gate 独立完整；M1 缺口 |
| Cross-Surface Consistency | 20 | 17 | 17.0 | 其余表面一致；M1 即跨表面缺口 |
| Pressure Resistance | 25 | 24 | 24.0 | 约 20 个独立攻击全部被拒；无 Gate 推断路径 |
| Evidence And Maintainability | 10 | 9 | 9.0 | RED 真实、fixture 真实、数字独立复现 |
| **合计** | 100 | | **91** | |

## 4. 发现（按严重级别排序）

### M1（Medium）：Feature Spec 视觉边界无 published runtime 承载

- 提案要求：§9.2 "Feature Spec 只解释 accepted Product Slice…不得通过图新增 Product Concept/role/permission/state/terminal/invariant/fact ownership…如果图形讨论暴露这些新含义，停止 Feature Spec，返回 Requirements Discussion"；§16.2 明确 `stage-guides.md` 应覆盖 "Requirements、**Feature Spec**、Decision & Design、Onboarding、Review 的使用与回流"；验收 #9 把 Feature Spec 列入边界清单。
- 现状：`stage-guides.md` 有 Requirements Discussion（:314-315）、Decision & Design（:697）、close/review（:1388）的视觉条目，但 **Feature Spec stage（:855-900）无任何视觉条目**；`external-skill-adapters.md` adapter 段未提 Feature Spec；`validation-scenarios.md` 无对应用例。
- 缓解（不定 High 的原因）：通用禁令仍在——spec 不得重定义已确认产品语义（`stage-guides.md:893-894`，前轮已验证）与 adapter 的 "the render cannot create a product rule"（`external-skill-adapters.md:60`）覆盖主要风险；缺口是"Feature Spec 中如何正确使用图 + 何时回流"的显式指引。
- 修复方向：在 `stage-guides.md` Feature Spec stage 增加视觉条目（只解释 accepted Product Slice / 新语义回流 Requirements Discussion），补一个 validation-scenarios 用例与 focused contract 断言。

### L1（Low）：legacy manifest 路径无法区分新旧 writer

- 任何 `product.md` 不写 `Visual Manifest Contract` metadata 即走 legacy 六列表 reader（实测 A15：HTML-only render + 正确 digest/status/evidence → PASS）。这是文档化的兼容设计（writer 侧规则在 `product-definition.md`），checker 无法机械区分新旧 Requirement。记录为已知边界，不要求修复。

## 5. 独立攻击结果（全部实测，非复用实施方用例）

### Requirement durable manifest（自建 standard fixture + 真实 Archify pair）

| 用例 | 结果 |
|---|---|
| G-valid：合法 source-render-v1 pair | PASS ✓ |
| A1：HTML-only 充当 source definition | 拒绝 `source definition and render must differ` |
| A2：source JSON 篡改（hash drift） | 拒绝 `source SHA-256 is stale` |
| A3：render 篡改（hash drift） | 拒绝 `render SHA-256 is stale` |
| A4：编辑 product 正文 → 语义 digest stale | 拒绝 `derived visual digest is stale` |
| A5：visuals 行引入未知 `STATE-NOPE` | 拒绝 `unknown source IDs` |
| A6：generator 无版本 | 拒绝 `generator must be archify@version` |
| A7：缺 `check=pass` | 拒绝 `validation evidence requires validate=pass and check=pass` |
| A8：`meta.output` 与 render 不符 | 拒绝 `meta.output does not match render` |
| A9：路径越界 `../` | 拒绝 `escapes owning root` |
| A10：`Status: stale` | 拒绝 `status must be current` |
| A11：Source IDs 为空 | 拒绝 `must name source IDs` |
| A12：Human Confirmed 空洞（`n/a`） | 拒绝 `requires concrete Human Confirmed evidence` |
| A13：两个 Diagram ID 复用同一 source | 拒绝 `duplicate values` |
| A14：未知 contract 值 `source-render-v2` | 拒绝 `unsupported Visual Manifest Contract` |
| A15：legacy 六列表 HTML-only | PASS（文档化兼容设计，见 L1） |

### Onboarding（真实复制 `examples/ai-meeting-minutes-backend/onboarding-db` 构造）

| 用例 | 结果 |
|---|---|
| O1：合法 archify pair 满足 required Diagram ID | PASS ✓ |
| O2：HTML-only required diagram | 拒绝 `source definition file is missing` |
| O3：evidence 无 `symbol#anchor` | 拒绝 `needs symbol/config evidence` |
| O4：`Status: stale` | 拒绝 `status must be current` |

### 规则层（文本核验 + Gate 推断路径搜寻）

- 解析顺序：`matching active project-local visual skill → installed Archify → 推荐 → Markdown/Mermaid/ASCII fallback`（`external-skill-adapters.md:34-39`；`skill-routing.md:113`），Project Skill Discovery Guard 优先权保留，**未进 mandatory helper 表**（全表 grep 无 Archify）。
- Installation Authorization：精确披露 source/pinned revision/command/target/effects/doctor/fallback；失败不授权提权/换镜像/换仓库/换包管理器；不 vendor、不硬编码跨运行时安装命令（`external-skill-adapters.md:57-58`）。
- Visual Scope Grant：六字段披露；同问题迭代不重复 Gate；source/stage/type/durable path/外部副作用/实质语义问题变化需新 Grant（`external-skill-adapters.md:43-55`、`product-definition.md:176+`、`runtime.md:206`）。
- 三层模型与 Gate 独立："render to converge, text to record"；"installation or generation does not authorize Product Human Review, ADR acceptance, Feature start, Git, release, publish, or future external actions"（`external-skill-adapters.md:60-72`）；ADR 视觉不能 accept ADR、不能替代 landing coverage（`stage-guides.md:210-212,697`）。
- 未发现任何"确认画图→推断安装→推断持久化→推断 commit"的文本推断链。

## 6. 范围漂移扫描（全仓 grep，无命中）

无新 canonical stage / message intent / lifecycle / Auto Mode（`runtime.md:50,52` 显式声明 internal method）；`SKILL.md`/`plugin.json` 版本均 `1.5.0`；root 13 个 managed block 仍 `1.5.0-20260721.2` 且 `git diff 7a74667 -- templates/root-AGENTS.md` 为空（验收 #16 满足）；未 vendor Archify 源码/schema/renderer；无默认 `.agent-loop/tmp/`；CHANGELOG 已记录且未升版本。

## 7. 证据评价

- RED 真实：focused shell 因 adapter 不存在失败、focused Python 因 `visual_artifact_support` 模块缺失失败，既有基线 40/40 + 258/258 全绿（`agent-loop-v1.5.0-optional-visual-communication-adapter-red-baseline-2026-07-23.md`）。
- GREEN 与 mutation：实施方 19 tests + 12 mutations；本 Agent 另独立执行约 20 个攻击用例（第 5 节），结论一致。
- 实施方 full validation（`agent-loop-1.5.0-full-validation-2026-07-23.md`，99/100 STRONG）未捕获 M1；本报告为单功能视角，不替代该报告。

## 8. 提交判断

- **STRONG（91/100）**：能力闭环成立，artifact 验证层 fail-closed 完备，规则层无 Gate 推断路径，兼容性无损。
- 提交前应修 M1（补 Feature Spec 视觉条目 + 场景 + focused 断言）；L1 为已知兼容边界，不阻断。
- 本次验证未修改任何生产代码、未安装 Archify、未 commit、未 push、未 tag。
