# Agent Loop v1.5.7 Progressive Verification + Proof First 全量验证报告

日期：2026-08-16
分支：alpha/v1.5.7
验证对象：e043d69..HEAD（提案 → 实施 → 三轮独立复核修复）
提案：`docs/proposal/v1.5.x/progressive-verification-proof-first.md`

## 1. 实施范围

| 表面 | 内容 |
|---|---|
| references/runtime.md | Feature Verification Profile 章节：三档表、硬下限（9 类含 data schema）与接触定义、升档重绑包、升降时间边界、Auto-Loop 停止条件、Proof First 段（RED 新鲜度）、legacy 兼容 |
| references/design.md、concepts.md | Profile/Proof First 定义、Adaptive Depth 操作化关系、与 Strict Mode/Standard Product Definition 消歧 |
| references/stage-guides.md | Gate 1 后记录时序、Gate 2 Verification 决策行呈现、Test Design 消费档位、Work Breakdown/Plan/Review 三档差异、Execute/Verify 升级检查与重绑、Review Repair 硬下限出口 |
| references/implementation-planning.md、workflow-checklists.md、human-review-summary.md、skill-routing.md | Plan owner 表、Gate 2 检查清单与呈现行、TDD helper 边界 |
| templates/tests.md、document-templates.md | Core Invariants + Test Oracle 两节（双落点） |
| templates/notes.md、document-templates.md | 五个 Profile 顶层字段 + Profile Escalation Log 表（双落点） |
| templates/root-AGENTS.md | gates/completion 块更新，13 blocks 升 `1.5.7-20260815.1` |
| SKILL.md、plugin.json、README.md、Usage.md | 版本 1.5.7（开发中）同步 |
| validation-scenarios.md | 场景 83 共 13 景 |
| tests/validate-progressive-verification.sh | 新契约测试：关键词断言 + 反语义断言 + 沙箱对照 + 16 变异 |
| .github/workflows/cross-platform-checkers.yml | macOS 腿新增运行契约测试 |

## 2. RED → GREEN

见 [RED 基线报告](agent-loop-v1.5.7-progressive-verification-red-baseline-2026-08-16.md)：实施前父提交 e043d69 上 exit=1（首断言即失败）；当前 HEAD PASS 且 16 变异全捕获。流程偏差如实记录：测试为 GREEN-first 编写、RED 为事后 worktree 回放补建，证据等价但时序不符理想流程。

## 3. 全量可执行回归

| 套件 | 结果 |
|---|---|
| Shell（tests/validate-*.sh 全部 52 个，含新契约与其 16 变异 + 沙箱对照） | 52/52 PASS |
| Python（unittest discover，22 模块） | 420/420 PASS |
| SKILL.md frontmatter YAML、plugin.json JSON | PASS |
| git diff --check、Markdown 围栏平衡 | PASS |
| root-AGENTS.md | 178 行（≤190）、13/13 managed blocks `1.5.7-20260815.1` |

## 4. 机械之外的行为验证（本版本新增的三层）

1. **对抗性压测**（盲测子 Agent，10 场景）：7 SAFE / 3 HOLE / 0 矛盾 / 4 FRAGILE；3 HOLE 与 4 FRAGILE 全部修复并有变异钉住。
2. **端到端编码模拟**（盲测子 Agent，隔离 /tmp 项目，8 轮人类消息脚本）：工件级评分全对——Profile 初始即 high-assurance（public API 下限前置）、包络变更正确回 Gate 2 v2、Escalation Log 正确处理"已在最高档只记录"、Bug 复现即 RED 且重执行、修复 Feature 正确继承 auth 下限。唯一瑕疵：模拟 Agent 手误重复一行字段（非模板缺陷）。
3. **三轮独立评审**：第一轮 4 阻断（notes 模板、Gate 2 呈现、升级矩阵弱化、同源断言不实）+ 复核 1 回归（auth/permission 分组）全修复；第二轮 2 High（升档不重绑、legacy 兼容）+ 5 Medium 修复（含 CI 接入、mutation 扩容）；第三轮 1 High（本报告）+ 3 Medium 修复（档位名笔误、执行面重绑同步、proposal schema 对齐与锚点机制）。

## 5. 六域语义审计

| 域 | 评估 | 依据 |
|---|---|---|
| 逻辑正确性 | 通过 | 16 变异全捕获；压测 3 HOLE 修复后复测 SAFE；升档重绑/legacy 默认/反社工程措辞均有正向断言 + 变异 |
| 自主性 | 通过 | Profile 记录与升级为 Agent 自动记账，不新增确认轮次；降档与硬下限解除保持人类门禁 |
| 入口/兼容 | 通过 | legacy Feature 默认 full 兼容段 + 场景 + 变异；消息意图与路由轴零变更；Stage Map 仅版本号变化 |
| 开发/测试工作流 | 通过 | Work Breakdown/Plan/Review/Test Design 四处档位差异落地且被变异钉住；No-Plan、Strict Mode、helper 边界显式；CI 接入 |
| 记忆 | 通过 | 无新 artifact tree；notes.md 新增字段有模板双落点；Markdown 单一状态源未破坏 |
| 推荐与呈现 | 通过 | Gate 2 Verification 行呈现 Profile 四要素；SKILL/root-AGENTS 摘要含 changed-risk 前置与反覆盖句 |

## 6. 已知接受的风险与限制

1. 硬下限与 Lightweight 硬触发为"对齐义务 + 共享锚点断言"而非物理单一清单（proposal 实施说明已记录；完全抽取留待结构性变更）。
2. 契约测试为关键词 + 变异级，检测不了任意位置新增的矛盾语义；该风险由六域人工/子 Agent 审计与反语义断言部分缓解。
3. mutation 沙箱使用 BSD sed 语法，CI 仅 macOS 腿运行（Windows 腿跳过）。
4. 度量计划（proposal §6.1 的 Token/轮次/隐藏测试对比）尚未执行——其结论不影响本版本行为正确性，属于发布后的效果验证。
5. examples/ 按仓库历史快照惯例未回填新模板结构。

## 7. 范围漂移检查

无 canonical stage、message intent、status、Mode、Gate、Checker outcome、artifact tree 新增；Required Verification / Existing Test Obligation / Additional Regression Test 三分结构未动；Repair-First、Git Fast Path、Lightweight、Bug Management 契约文本零语义删改（版本串替换除外）；grep 确认无 state.json / evidence.json / run.jsonl 引入。

## 8. 发布判断

技术验收就绪：全部可执行回归、变异契约、行为模拟、三轮独立评审问题闭环。等待最终 Human Review 接受后，走既有独立 Gates（commit → tag `stable-v1.5.7` → main 同步）。
