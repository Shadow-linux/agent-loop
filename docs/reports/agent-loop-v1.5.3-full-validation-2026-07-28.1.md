# Agent Loop v1.5.3 全量验证报告（Feature Context Soft Gate）

## 1. 审计对象与结论

- 日期：2026-07-28
- 分支：`v1.5.3`
- 基线 HEAD：`6086d7d6fc758221af2dee41ea269d0acf237795`
- 审计对象：当前未提交组合工作区；包含先前已批准的 Feature Monthly Archive / Rehydrate Reference Scan 软 Gate，以及本轮 Feature Context Fact Scan 软 Gate
- 本轮 Proposal：`docs/proposal/v1.5.x/feature-context-fact-scan-soft-gate.md`
- 本轮 Implementation Plan：`docs/proposal/v1.5.x/feature-context-fact-scan-soft-gate-implementation-plan.md`
- 总分：**99.7 / 100**
- 等级：**STRONG**
- 当前缺陷：Critical 0、High 0、Medium 0
- 平台证据：`macOS-verified / Windows-test-defined`
- Git/发布状态：未 stage、未 commit、未 push、未 tag、未 PR、未 merge、未 release、未 publish、未同步 installed Skill

结论：Feature Context 仍是 Feature 下游依赖 Requirement/ADR 前的必需事实检查，但 checker 不再替 Agent 裁决普通缓存漂移或产品/决策影响。`CURRENT / 0` 走快速路径，`CHANGED / 0` 要求 Agent 评估、修复派生上下文并在依赖前重跑到 `CURRENT`，`BLOCKED / 1` 仅保留给无法安全解析 authority 的物理矛盾。现有 Product、ADR、Feature Gate、Delivery Contract、TDD、完成与 Git Human Gate 均未减少。

## 2. 工作区边界

本轮开始前已有 Feature Archive soft-gate 修改及其 Proposal、Plan、RED/full report；这些内容在本轮保持并参与组合全量验证。`.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/` 为既有未跟踪本地缓存，未纳入功能设计。

本轮 Feature Context 实际修改或新增：

- 控制与实现：`SKILL.md`、`scripts/check-feature-context.py`
- canonical 规则：`references/design.md`、`references/runtime.md`
- 协调 references：`references/product-definition.md`、`references/implementation-planning.md`、`references/artifact-rules.md`、`references/project-guidance.md`、`references/stage-guides.md`、`references/workflow-checklists.md`、`references/document-templates.md`、`references/validation-scenarios.md`
- 模板与人类文档：`templates/spec.md`、`templates/feature-context.md`、`templates/root-AGENTS.md`、`README.md`、`Usage.md`、`CHANGELOG.md`
- focused tests：`tests/test_feature_context.py`、`tests/validate-feature-context-load-contract.sh`
- root revision contracts：`tests/test_root_agents_blocks.py`、`tests/test_root_agents_lossless_slimming.py`、`tests/validate-root-agents-block-refresh.sh`、`tests/validate-root-agents-block-checker.sh`、`tests/validate-v1.2.4-root-stage-coverage.sh`、`tests/validate-lightweight-change-lane.sh`、`tests/validate-bug-management.sh`、`tests/validate-requirement-lifecycle-backlog.sh`、`tests/validate-branch-management-strategy.sh`、`tests/validate-project-local-skills.sh`、`tests/validate-project-skill-discovery-guard.sh`
- 设计与证据：本轮 Proposal、Implementation Plan、RED 报告和本报告

未在技能源码仓库创建目标项目 `.agent-loop/`。

## 3. RED 基线

本轮改动前组合工作区全量基线：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
```

- Shell：`47 / 47 PASS`
- Python：`327 / 327 PASS`

真实 focused RED：

```bash
python3 -m unittest tests.test_feature_context
bash tests/validate-feature-context-load-contract.sh
```

- Python：27 项中 15 项按新契约失败，12 项通过；旧 checker 对普通 changed facts 返回 `REFRESH_REQUIRED / 3` 或 `BLOCKED / 1`
- Shell：模板仍使用旧 `current | refresh-required | blocked`，contract 失败
- 物理负向控制在 RED 阶段仍通过

完整失败证据见 `docs/reports/agent-loop-v1.5.3-feature-context-soft-gate-red-2026-07-28.md`。

## 4. GREEN 与 focused validation

### Feature Context focused GREEN

```bash
python3 -m unittest tests.test_feature_context
bash tests/validate-feature-context-load-contract.sh
```

- Python：`30 / 30 PASS`
- Shell contract：PASS

新增或改写的压力场景覆盖：

- Product/ADR editorial digest 变化、缺失/不完整 Snapshot、错误时间戳、legacy freshness：`CHANGED / 0`
- deferred Requirement、未确认 Product Review、proposed/review-required ADR：`CHANGED / 0`，由 Agent 返回原有 owner/Gate
- 未解析 Product Slice ID/anchor、cached Requirement/Product/profile/review/decision 分歧：`CHANGED / 0`
- authoritative Requirement pointer 缺失、Requirement README 缺失、双 effective Product pointer、Product path 越界/缺失：`BLOCKED / 1`
- ADR path 越界、非 Markdown、文件缺失：`BLOCKED / 1`
- zero/dual/symlinked memory root 与 Feature path 越界：`BLOCKED / 1`
- LF/CRLF digest 兼容、稳定排序和运行前后文件快照一致：保持通过

### 跨 surface focused validation

```bash
python3 -m unittest tests.test_feature_context tests.test_python_checker_contract
python3 -m unittest tests.test_adr_requirement_model_trace
bash tests/validate-feature-construction-two-gate-review.sh
bash tests/validate-adaptive-requirement-product-definition.sh
bash tests/validate-checker-self-repair.sh
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
bash tests/validate-decision-design-requirement-landing.sh
bash tests/validate-project-decisions-adr-lane.sh
bash tests/validate-project-decisions-adr-proposal.sh
```

- Feature Context + Python checker contract：`49 / 49 PASS`
- ADR trace：`25 / 25 PASS`
- 所列 Shell contracts：全部 PASS

### Root managed-block revision

本轮再次修改 root `gates` 摘要，因此 13 个 managed blocks 的同日 revision 统一为 `1.5.3-20260728.1`。相关 Python 14/14 与 9 个 root/branch/bug/skill/lifecycle Shell contracts 全部通过。

## 5. 最终全量可执行测试

实时重新枚举并执行：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
```

- Shell：`47 / 47 PASS`
- Python：`333 / 333 PASS`，最终复跑 62.772 秒
- 相比本轮 RED 前基线新增 6 个 Python 回归场景；测试数量未沿用历史报告

## 6. 机械检查

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
# 对仓库内全部 Markdown 执行 fence balance 检查
python3 -m py_compile scripts/check-feature-context.py
git diff --check
```

结果：YAML PASS、JSON PASS、Shell syntax PASS、Markdown fence PASS、Python compile PASS、`git diff --check` PASS。

## 7. 六域语义审计

| 审计域 | 结果 | 评分 | 通过证据 |
|---|---|---:|---|
| Logic Correctness | PASS | 100 | `CURRENT/CHANGED/BLOCKED` 分类互斥；exit 0 不等于执行许可；physical authority failure 仍 fail closed；无 Gate 绕过或循环 |
| Autonomy | PASS | 100 | checker 只报事实；Agent 负责 `no-semantic-impact / derived-context-update / feature-definition-impact / decision-impact / unresolved`，仅最后一种问一个阻塞问题 |
| Project Entry / Evidence Graph + DDD Onboarding | PASS | 99 | 唯一真实 memory root、Requirement README、effective Product 和 ADR authority 仍受物理约束；未改变 Project Entry/Onboarding 路由 |
| Development / Test Workflow | PASS | 100 | Task/Test/Plan/Execute/Handoff/Verify/Review/Drift/Close 在依赖前都要求评估 CHANGED 并取得 CURRENT；TDD 与 Gate 1/2 不变 |
| Memory | PASS | 99 | Snapshot/context 继续是派生缓存；Requirement `product.md` 与 accepted ADR 继续拥有语义；legacy freshness 可读且无需批量迁移 |
| Recommendation | PASS | 100 | changed meaning 返回现有 owner/Gate；纯派生刷新无需新增 Human Gate；Agent 无法判断时只提出一个阻塞问题 |

加权总分：`99.7 / 100`，等级 `STRONG`。

## 8. 关键跨文件不变量与代表性压力场景

已核对并通过：

- `SKILL.md` 保持简洁控制入口，完整规则由 runtime/design/references 承载；
- root Stage Map 仍只提供 first hop，13 个 managed blocks 完整保留；
- Requirement `product.md` 是产品语义 owner，Feature Product Slice 不重定义产品含义；
- Brief Product Definition 可直接进入无需 ADR 的 Feature；Standard Product Definition 在需要共享技术落地时仍经过 Decision Scan/ADR；
- pending Product Review、deferred Requirement、proposed/review-required ADR 虽由 checker 报 `CHANGED / 0`，runtime 仍禁止下游实施并返回原有 Gate；
- `CHANGED / 0` 不授权 Feature Auto-Loop、Task Auto-Run、代码写入、subagent、Delivery Contract 或任何 Git 动作；
- Gate 1、Gate 2、Delivery Contract、TDD RED、Task Done、Review/Drift/Memory、Feature Completion、Submit、Close 保持原义；
- accepted ADR 与实现 drift 仍返回 Drift Check / Decision & Design；
- Active Feature、Pause、Resume、Close、Reopen 和 multi-phase `partially-implemented` 契约通过全量回归；
- Feature Archive 的 advisory scanner 与 exact-plan Human Gate/transaction boundary 不受 Feature Context 改动破坏；
- 普通 Chat 不创建 Requirement、Feature 或目标项目 artifact。

## 9. 当前问题、剩余风险与范围漂移

当前问题：Critical 0、High 0、Medium 0。

剩余 Low 风险：

- 外部自定义调用方若只检查进程退出码、不读取输出 prefix，可能把 `CHANGED / 0` 误当 `CURRENT`。发布的 runtime、design、SKILL、模板和回归契约已明确禁止该用法；仓库内 canonical surfaces 已同步。
- 本轮在 macOS 执行；checker 使用 Python 3.10+ 标准库并保留 LF/CRLF 与路径负向测试，但没有实际 Windows runner，因此只声明 `macOS-verified / Windows-test-defined`。

范围漂移检查：无。未删除 Feature Context，未新增 canonical stage、message intent、lifecycle、Human Gate、artifact family、schema 或依赖；未放松 project/memory/Requirement/Product/ADR 物理 containment；未改变版本 `1.5.3`；未创建分支/worktree 或目标项目 `.agent-loop/`。

## 10. Proposal 验收与发布判断

Proposal 10 项 Acceptance Criteria 全部满足：检查仍必需；hard failure 仅限 physical/authority resolution；changed facts 可见且退出 0；Agent assessment 明确；CHANGED 不授权执行；legacy Snapshot 无需批量迁移；focused RED/GREEN 与负向控制成立；full/mechanical/六域验证通过；版本保持 1.5.3；没有 Git/发布动作。

当前工作区可以进入最终 Human Review。未经后续明确授权，不执行 stage、commit、push、tag、PR、merge、release、publish 或 installed-Skill sync。
