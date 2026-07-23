# Agent Loop v1.5.0 Root Guidance Consistency 全量验证报告

- 日期：2026-07-22
- 分支：`alpha/v1.5.0`
- 基线 HEAD：`e07d50c2c2b0bf80ad22b579e3a476bb71218c06`
- Skill version：`1.5.0`（未升级）
- 审计对象：基线 HEAD 加当前未提交的 Adaptive Requirement Product Definition 实施，以及本轮 Root guidance consistency 修复
- 验证方法：`docs/maintenance/full-validation-method.md`
- 结论：`STRONG`，`100/100`；Critical `0`、High `0`、Medium `0`

## 1. 范围与 dirty-work 边界

本轮只追加以下修复，不覆盖、还原或重新归属当前 Adaptive Requirement Product Definition 改动：

- 对齐 `references/project-guidance.md` 的 stale Message Intent contract 与 `Root AGENTS Should Contain`；
- 从 Root checklist 删除已委托给 Requirement owners 的 `Delivery Phases` 和 source-lifecycle 细则；
- 把双 memory root 的 fail-closed 规则提升到 `SKILL.md`、`references/runtime.md`、`references/design.md` 和 `references/project-guidance.md` 的通用入口；
- 扩展 dual-root pressure scenario，新增跨文件回归测试；
- 校正 `docs/reports/agent-loop-1.5.0-full-validation-2026-07-21.md` 的 RED 数量、问题计数和 precedence 测试描述。

未修改 `templates/root-AGENTS.md`，其 170 行、13 个 managed blocks、16-row Gateway 和 `block-version:1.5.0-20260721.2` 保持不变。未创建目标项目 `.agent-loop/`，未清理现有 `.tmp/` 或 `__pycache__`，未执行 commit、push、tag、PR、merge、release、publish 或 installed-Skill 同步。

## 2. Root Cause 与 RED 基线

### 2.1 修复前组合工作区基线

- Shell：`40/40 PASS`
- Python：`246/246 PASS`
- `git diff --check`：PASS

### 2.2 Root Cause

1. Root 瘦身更新了 `AGENTS.md is stale` 的完整 intent 集合，却保留了 `Root AGENTS Should Contain` 中旧的四类 intent 和下游 Requirement 细则。当前生成模板没有丢失能力，但未来按撰写指南刷新时可能重新引入冗余或产生指南漂移。
2. 通用 `runtime.md` Inspection Order 使用“`.agent-loop/` 不存在才看 legacy”措辞，而 Lightweight Change owner 已规定双根 fail closed。一般 Project Entry 可能把表面优先顺序误当成 owner 选择规则。

### 2.3 Focused RED

新增 `tests/test_project_guidance_consistency.py` 后执行：

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_project_guidance_consistency
```

真实结果：`Ran 2 tests`，`FAILED (failures=5)`：

- stale intent contract 未出现在 `Root AGENTS Should Contain`；
- `SKILL.md`、runtime、design、project-guidance 四个 controller surfaces 均缺少同一条通用 dual-root fail-closed contract。

## 3. GREEN 与回归证据

### 3.1 Focused GREEN

- 新增 consistency tests：`2/2 PASS`；
- Root consistency + checker Python：`35/35 PASS`；
- 受影响 Shell contracts：root refresh、postfix pressure、state lifecycle、Lightweight Change、Adaptive Product Definition，`5/5 PASS`。

### 3.2 全量可执行回归

```text
all tests/*.sh: 40/40 PASS
python3 -m unittest discover -s tests -p 'test_*.py': 248/248 PASS
SKILL.md + agents/openai.yaml YAML: PASS
plugin.json JSON: PASS
all Shell bash -n: PASS
all Markdown fence balance: PASS
git diff --check: PASS
```

### 3.3 压力场景

| 场景 | 结果 | 结论 |
|---|---|---|
| `.agent-loop/` 与 legacy `agent-loop/` 同时存在 | PASS | controller 在读取任一根为 authoritative 前进入 Recovery |
| 只有 legacy `agent-loop/` | PASS | 继续复用唯一 accepted root，迁移仍需 Human Gate |
| 两个根都不存在 | PASS | 继续 new/existing entry classification，不制造可靠 memory |
| Requirements Discussion 与 bounded ordinary non-Bug 同时可疑 | PASS | stale 与 Should Contain 使用同一 intent family；Gateway owner 决定 first hop |
| Root template refresh | PASS | 170 行模板、13 blocks、16 Gateway、完整 leaf-stage owner 保持不变 |
| Adaptive Product Definition 组合回归 | PASS | 既有 Product Definition、Product Slice 与 ADR reader/writer contract 全部通过 |

### 3.4 Full-validation 代表面

| 代表面 | 结果 | 当前证据 |
|---|---|---|
| complex Requirement -> Standard Product Definition -> Decision Scan / ADR -> Product Slice | PASS | Adaptive ownership Shell contract、ADR trace 与 accepted Concept/model fixtures |
| simple requirement -> Brief Product Definition -> Feature Product Slice | PASS | Brief/Standard checker、new-writer stop 与 Product Slice tests |
| Requirement product ownership / Product Human Review | PASS | `validate-adaptive-requirement-product-definition.sh` 与 requirement checker tests |
| Delivery Contract Human Gate | PASS | 全量既有 contract regression；本轮未改变该 owner |
| behavior TDD RED / non-behavior `N/A` | PASS | 本轮 focused RED→GREEN 及既有 workflow tests |
| Active Feature / Pause / Resume / Close / Reopen | PASS | state-lifecycle 与 full Shell regression |
| multi-Phase `partially-implemented` | PASS | requirement lifecycle regression |
| accepted ADR drift | PASS | ADR Requirement Model trace 与 decision landing regression |
| Follow-up investigate-first | PASS | Bug / Feature Follow-up regression |
| Submit / Integrate blockers | PASS | root submit projection与 full regression |
| stale memory / root guidance / Project Entry | PASS | consistency tests、root refresh contract 与 dual-root pressure |
| ordinary Chat creates no artifact | PASS | chat / requirements entry contract |

## 4. 六域语义审计

| 审计域 | 评分 | 结果 | 结论 |
|---|---:|---|---|
| Logic Correctness | 100 | PASS | intent 撰写/判 stale contract 对齐；dual-root 路由唯一且 fail closed |
| Autonomy | 100 | PASS | 未扩张 Root 细节，Agent 仍依据 owner references 自行推进 |
| Project Entry / Onboarding | 100 | PASS | 零根、唯一 legacy、双根三种入口不再含静默选择歧义 |
| Development / Test Workflow | 100 | PASS | RED/GREEN、Root focused、Adaptive focused 与 full suite 完整通过 |
| Memory | 100 | PASS | 一个 accepted root 的 authority 明确；双根进入 Recovery，不隐式迁移或合并 |
| Recommendation | 100 | PASS | Recovery 只在真实 ownership 冲突时触发；其他 Low 观察项未被误扩写为流程缺陷 |

加权总分：`100/100`，等级 `STRONG`。

## 5. 未采纳或独立观察项

- Lightweight Change Assessment 与 Post-Merge Memory Reconciliation 位于 Root 的 Message Intent Guard 块，但正文把它们表达为内部 route，而非持久 message-intent 值；未发现路由冲突，不为形式统一改写 Root。
- unavailable infrastructure、Bug Project Entry 优先权、Submit 后 Feature Completion Check 均已有明确 owner 承载；不把“Root 不重复细节”判成能力缺失。
- 不同 ambiguity prompt 服务不同局部上下文，不要求形成一个全局固定选项枚举。
- First-match precedence 已由现有 Shell contract 对 Root 与 runtime 两侧的同一固定字符串分别断言；不重复建立等价测试。
- Evidence Gate 的 Review/Drift/Memory 措辞仍可做未来可读性优化，但 runtime 明确要求 Agent 先补齐可生成证据，只在真实 blocker 时请求人类；本轮不触碰 Root template 或 managed-block revision。

## 6. 发布判断

Root AGENTS 无损瘦身无需回退。补充审计发现的 M1 已关闭，既有 dual-root 一般入口歧义已关闭；未发现新的 Gate 绕过、死锁、路由不唯一、Root 回膨或 Adaptive Product Definition 回归。

本轮没有获得 commit、push、tag、PR、merge、release、publish 或 installed-Skill 同步授权，均未执行。
