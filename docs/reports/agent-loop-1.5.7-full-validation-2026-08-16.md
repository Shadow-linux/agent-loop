# Agent Loop 1.5.7 全量验证报告

## 1. 基本信息

- 日期：2026-08-16
- 分支：`alpha/v1.5.7`
- 版本：1.5.7（开发中，技术验收）
- 审计对象：当前 HEAD 及本报告所在工作区（实施链 e043d69 → 本收尾提交，共 8 个提交）；基线为 v1.5.6 发布提交 3d8e868
- 提案：`docs/proposal/v1.5.x/progressive-verification-proof-first.md`

## 2. 总分与等级

| 项 | 值 |
|---|---|
| 总分 | **88 / 100** |
| 等级 | **STABLE**（可运行，应处理剩余风险） |
| 测试通过数 | Shell 52/52；Python 420/420；机械检查（YAML×2、JSON、diff-check、围栏平衡、root-AGENTS 13/13 blocks ≤190 行）全部通过 |
| Critical | 0 |
| High | 0 |
| Medium | 1（待人类裁决，见 §4） |

未达 STRONG 的原因：存在一项未获人类批准的设计来源偏差（§4 M-1）；在其裁决前判定 STABLE 是诚实表述。

## 3. 六域评分表

| 域 | 分数 | 稳定性 | 有效性 | 要点 |
|---|---:|---|---|---|
| Logic Correctness | 86 | STABLE | EFFECTIVE | 15/15 变异捕获；压测 10 场景 3 HOLE 修复后复测 SAFE；升档重绑、legacy 兼容、反社工程均有正向断言+变异；关键词断言对"新增矛盾语义"的检测能力有原理性上限（§6） |
| Autonomy | 95 | STABLE | EFFECTIVE | Profile 记录/升档为 Agent 自动记账，不新增确认轮次；降档与下限解除保持人类门禁；Auto-Loop 停止条件完整 |
| Project Entry / Compatibility | 90 | STABLE | EFFECTIVE | legacy Feature 默认 full 兼容段+场景+变异；消息意图与路由轴零变更；Stage Map 仅版本号变化 |
| Development / Test Workflow | 86 | STABLE | EFFECTIVE | 四处档位差异落地且被变异钉住；No-Plan/Strict Mode/helper 边界显式；CI macOS 腿接入；Windows 腿因 BSD sed 语法跳过（§6） |
| Memory | 92 | STABLE | EFFECTIVE | 无新 artifact tree；notes 新字段双模板落点；Markdown 单一状态源；examples 按惯例未回填 |
| Recommendation | 95 | STABLE | EFFECTIVE | Gate 2 Verification 行呈现 Profile 四要素；SKILL/root-AGENTS 摘要含 changed-risk 前置与反覆盖句 |

## 4. 当前问题（按严重级排序）

**M-1（Medium，待人类裁决）**：提案 §2.4（`docs/proposal/v1.5.x/progressive-verification-proof-first.md:93-99`）原设计要求硬下限与 Lightweight hard trigger "抽取为同一份定义"；实现采用"两个自然语言清单 + 对齐义务 + 共享锚点断言（permission/schema/public API/migration/cross-module 双向钉住）"，且实施说明中写入了 auth≈credential/security 等并不严格等价的映射。该偏差已显式记录于提案，但未经人类批准——构成设计来源被实现反向修改。处置二选一：(a) 实现真正单一 owning definition（runtime 拥有清单，Lightweight 引用之，方向为 fail-closed 扩展）；(b) 人类明确批准提案修订为共享锚点方案并删除伪等价映射。裁决前本报告不判定 STRONG。

无 Critical / High 遗留；前三轮评审的 4+1+2+5+1+3 项发现已全部修复并由断言/变异钉住（见 §5、§7）。

## 5. 通过的不变量与压力场景

不变量（抽样）：

- Evidence-driven completion：无新鲜验证不得声称完成（SKILL.md、runtime.md 未动，Repair-First 契约原文保留）。
- Required Verification / Existing Test Obligation / Additional Regression Test 三分结构未动；Bug Verification Matrix 回归/安全列不可降级（4 处独立文本咬合，压测 A8 验证）。
- RED 新鲜度：历史失败日志仅为 intake 证据（压测 A7 修复后，变异 `stale-log-accepted-as-red` 钉住）。
- 硬下限：auth/permission/payment/data deletion/data schema/migration/public API/security/cross-module 不得低于 high-assurance；人类紧迫/担责措辞不可压低（压测 A1/A2，变异 `hard-floor-removed`）。
- 升档重绑：档位提升必须先刷新 Test Design/Plan/回归范围并重跑 Analyze Consistency（二轮 High1，变异 `rebind-removed`）。
- 车道排除：Profile 不给 Lightweight/Review Repair 指派档位；硬下限接触仍升级 owning Feature（变异 `exclusion-flipped`、场景 D + Review Repair Floor Contact Exits Fast Path）。
- 不新增 canonical stage / message intent / status / Mode / Gate / Checker outcome / artifact tree（grep 证实无 state.json、evidence.json、run.jsonl）。

压力场景：

- 压测 10 场景（盲测子 Agent）：7 SAFE，3 HOLE（A3 接触定义、A5 Review Repair 盲区、A7 RED 新鲜度）已修复并复测。
- 场景 83 共 13 景（含 Tier Raise Re-binds The Package、Legacy Feature Defaults To Full、Stale Failure Log Is Not RED、Review Repair Floor Contact Exits Fast Path）。
- E2E 编码模拟（盲测，隔离项目，8 轮人类消息脚本）：工件级全部正确，含 public API 下限前置应用、包络变更回 Gate 2 v2、"已在最高档只记录"处理、Bug 复现即 RED 且重执行、修复 Feature 继承 auth 下限。
- mutation 15/15 捕获（沙箱对照组先行）。

## 6. RED 基线、GREEN 与新增回归

- RED 基线：契约测试在实施前父提交 e043d69 上 exit=1（首断言即失败），存档于 [RED 基线报告](agent-loop-v1.5.7-progressive-verification-red-baseline-2026-08-16.md)。流程偏差如实记录：测试为 GREEN-first 编写，RED 为事后 worktree 回放补建，证据等价但时序不符理想流程。
- GREEN：当前 HEAD 契约 PASS（含 15 变异 + 沙箱对照）。
- 新增回归：`tests/validate-progressive-verification.sh`（关键词 + 反语义 + mutation 沙箱）；既有 51 个 shell 与 22 个 Python 模块全部同步版本断言后通过。
- 未执行项说明：GitHub Actions 线上运行未在本地执行（CI 配置经 YAML 解析与本地同等命令验证）；proposal §6.1 的 Token/轮次度量计划属发布后效果验证，不阻塞本报告。

## 7. 未采纳或降级意见及原因

1. 三轮独立评审建议的"硬下限物理单一清单"：v1.5.7 内未实现（会改写 Lightweight lane 既有契约语义），以共享锚点方案过渡——现升级为 §4 M-1 交人类裁决，本报告不再自行降级该意见。
2. 压测建议的完全语义矛盾检测：超出关键词+变异测试原理上限，以反语义断言部分缓解，其余依赖六域人工/子 Agent 审计（已如实计入 Logic 域扣分）。
3. examples/ 回填新模板结构：仓库历史惯例为快照不回填（v1.5.1 起 Gate 字段等从未回填），维持不采纳。
4. mutation 沙箱 Windows 腿：BSD sed 语法限制，CI 显式 `if: runner.os == 'macOS'`，已知且接受。

## 8. 发布判断与 Git 授权状态

- 技术验收：通过（§2-§6）。发布前置条件：§4 M-1 人类裁决 + 最终 Human Review。
- `commit`：本报告与四轮修复随收尾提交进入 `alpha/v1.5.7`（人类此前已授权该分支的版本提交链）。
- `push`：未请求、未授权（`alpha/v1.5.7` 未推送任何远端）。
- `tag`（`stable-v1.5.7`）：未请求、未授权。
- `main` 同步：未请求、未授权。

以上任一动作需人类在裁决 M-1 并接受本报告后另行明确授权。
