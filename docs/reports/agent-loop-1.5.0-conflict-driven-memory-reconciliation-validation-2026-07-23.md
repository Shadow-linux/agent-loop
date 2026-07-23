# Agent Loop v1.5.0 冲突驱动记忆合并全量验证报告

## 1. 审计信息

- 日期：2026-07-23
- 分支：`alpha/v1.5.0`
- 版本：`1.5.0`，本轮未升级版本
- 审计对象：`HEAD c2fd71b4c1283abbe1a82c4144aec62d3206bec5` 加当前未提交工作区
- 行为范围：Post-Merge Memory Reconciliation 从默认全路径审计改为冲突驱动；Full Memory Audit / Recovery 保留为显式授权能力
- 仓库视角：Agent Loop Skill 源仓库维护，不是目标项目运行实例

## 2. 结论

**总分：99/100，STRONG**

- Critical：0
- High：0
- Medium：0
- Low：1
- Shell contract/regression：41/41 PASS
- Python unittest：280/280 PASS
- Memory Reconciliation Python focused：84/84 PASS
- 最终增量 affected Python（Memory + Root + Project Guidance）：100/100 PASS
- Root guidance / project guidance focused：16/16 PASS
- YAML、JSON、Shell syntax、Python AST、Markdown fence、`git diff --check`：PASS

结论：新规则已经把正常记忆合并恢复为“当前理解 + 最新事实”的人类式语义整理。无冲突不扫描、不建报告、不增加 Human Gate；小冲突优先在会话中核对；确定性冲突由 Agent 定向重写和验证；只有真正无法判断的产品/项目含义交给人类。旧四快照、全路径、精确 Plan Hash 和事务 Restore 工具仅能通过显式 Full Memory Audit / Recovery 授权进入。

## 3. 六域评分

| 审计域 | 结果 | 分数 | 结论 |
|---|---|---:|---|
| Logic Correctness | PASS | 100 | 正常冲突路径与 Full Audit / Recovery 已分离；无冲突不再制造工作 |
| Autonomy | PASS | 100 | Agent 先查最小事实并自行解决唯一答案，只把真实语义选择交给人类 |
| Project Entry / Evidence Graph + DDD Onboarding | PASS | 99 | 未改变 Project Entry/Onboarding 主流程；定向冲突只更新直接受影响事实 |
| Development / Test Workflow | PASS | 100 | focused RED/GREEN、全 shell、全 Python、root regression 均通过 |
| Memory | PASS | 100 | Source/Target 不再机械选边；accepted authority、human source、append-only history 受保护 |
| Recommendation | PASS | 99 | 小冲突会话内给少量选项；复杂/跨会话时才建议精简报告 |

## 4. RED 基线

本轮先记录并保留了两个直接 RED：

1. `tests/validate-post-merge-memory-reconciliation.sh`
   - 失败：缺少独立 `templates/full-memory-audit-report.md`，普通模板仍拥有全路径 Plan。
2. `tests/test_memory_reconciliation_scan.py`
   - 失败：未提供任何 Full Audit 授权时，四快照扫描器仍返回成功。

并行语义审计进一步发现旧模型的跨表面残留：

- post-merge 会无条件触发全部月度 Lightweight Change scanner；
- root Required Stops 仍把所有 reconciliation rewrite 当成 Human-gated Apply；
- `project.md` 模板仍只表达旧 Full Audit 状态；
- focused validator 未覆盖 Lightweight Change / project guidance 交叉面。
- root Gateway 中宽泛的 `Memory conflicts or outside-loop work` 会在专用 Post-Merge route 之前命中，把事实可确定的冲突错误送入 Recovery；
- `SKILL.md`、`runtime.md` 和 root Evidence Gate 的无条件 stop 会再次拦截本可由 Agent 可逆定向修复的冲突；
- root managed block 内容已改变但 revision 仍为 `1.5.0-20260721.2`，导致下游无法识别同版本指导更新；新增 RED 真实得到 `managed-revision`、`gateway-contract` 和 root refresh FAIL。

最终独立代码审查又建立了三项 RED：

- Recovery signal 虽已初步收窄，但仍含无边界的 `stale`，会因 runtime 的 Memory Health 分类再次抢先吞掉 observed post-merge conflict；
- 精简 Memory Conflict Report 缺少 changed-path preimage/postimage、bounded rollback evidence 与 remaining risk，不足以支持其 cross-session / recovery-heavy 用途；
- root Gate 只列 Full Memory Audit / Recovery Apply，遗漏同样需要独立 Human Gate 的 Restore。

全 shell 首轮为 40/41，发现 `Usage.md` 缺少既有 ADR handoff 术语 `Effective Requirement Snapshot`。这是文档契约漂移，不是本轮记忆模型设计的一部分；已用一段简洁说明补回并转绿。

## 5. GREEN 修复

### 5.1 正常路径

```text
Verified Code Merge
-> observed memory conflict?
   -> no: reconciliation-not-needed
   -> yes: conflict owner + direct references + minimum evidence
      -> one fact-determined meaning: Agent targeted rewrite + verification
      -> several legitimate meanings: bounded conversation Human Review
```

正常路径明确禁止：

- 为“可能存在漂移”扫描整个 memory root；
- 为 Source/Target 修改了不同文件而启动 reconciliation；
- 列出 unchanged files、absence claims、全路径 hash 或机械 `保留` 项；
- 为一个小冲突强制创建报告；
- 因没有 Full Audit 报告而阻塞独立 Push/Release Gate。

### 5.2 会话与报告

- 小冲突和一个 bounded Human choice 优先留在当前会话。
- 仅在多个耦合冲突、跨会话交接、恢复证据复杂或人类明确要求时，才使用精简 Memory Conflict Report。
- `reconciliation-not-needed` 不写入持久项目记忆。

### 5.3 Full Memory Audit / Recovery

- 旧全路径模板迁移为 `templates/full-memory-audit-report.md`。
- `scan-memory-reconciliation.py` 必须收到 `--full-audit-authorized`。
- 授权检查发生在项目路径、Git commit 和 memory inventory 读取之前。
- 原有 check/apply/restore 安全和跨平台 Python 标准库实现保持通过。

### 5.4 跨能力隔离

- post-merge 不再无条件运行月度 Change scanner。
- 只有观察到的冲突直接涉及某张 Change card 时，才读取该卡和最小直接证据。
- root `Git And Lifecycle Gate` 只保留 Full Memory Audit / Recovery Apply，而不阻塞确定性 targeted rewrite。

### 5.5 路由优先级、写入安全与根指导刷新

- Root Gateway 的 Recovery 入口已收窄为 broad memory damage、没有稳定已验证 post-merge conflict boundary 的 stale/incomplete memory、outside-loop work 或 unresolved reconciliation recovery；稳定代码合并后的已观察冲突进入专用 Post-Merge route。
- Root Evidence Gate、`SKILL.md` 与 `runtime.md` 的 stop 条件均保留“事实唯一、可逆、定向重写”例外；语义未决仍然停止并交给人类。
- 定向写入必须先捕获精确 preimage、计算精确 intended postimage、只保留受影响文件的有界备份，并通过同目录临时文件原子替换；随后逐字节验证 postimage 与最小语义/引用范围。
- 精简冲突报告现在记录每个 changed path 的 exact preimage、intended postimage、rollback scope/backup evidence、restore verification 与 remaining risk，但仍不包含 unchanged-path ledger。
- Root Git/Lifecycle Gate 明确覆盖 Full Memory Audit / Recovery Apply/Restore。
- 13 个 root managed blocks 与所有当前 revision consumers 已同步为 `block-version:1.5.0-20260723.2`，Skill version 仍为 `1.5.0`。

## 6. 代表性压力场景

| 场景 | 结果 |
|---|---|
| Source/Target 各自新增独立 memory 文件，Git clean merge | `reconciliation-not-needed`；零扫描、零报告、零额外 Gate |
| Source-only Requirement/Feature 已被 Git 合入 | 保持现状，不重新 import、分类或审核 |
| 同一 current-state claim 有一侧明显 stale | Agent 查 owner + fresh evidence，定向重写并验证 |
| Source/Target 都 stale，但代码/测试证明第三种当前事实 | 写入第三种事实，不让人类在两个错误答案中二选一 |
| 实现与 accepted Requirement/ADR 冲突 | 保留 accepted authority，报告 implementation drift |
| 两个 Human Decisions 都可能适用 | 会话内展示少量具体选项、推荐和后果 |
| 发现无关 onboarding drift | 单独提示 Recovery candidate，不扩张当前 reconciliation |
| post-merge 存在大量月度 Changes，但冲突未指向它们 | 不运行全月 scanner，不暴露候选 |
| 未授权调用四快照 scanner | 读取项目前失败，提示 Full Memory Audit / Recovery 需要明确授权 |
| 明确授权 Full Audit | 旧四快照/Plan Hash/transaction/restore 测试继续通过 |

全量方法要求的 Requirement、Brief/Standard Product Definition、ADR、Feature Product Slice、Delivery Contract、TDD、Feature lifecycle、Phase roll-up、Follow-up、Submit、stale-memory、root guidance 和 Chat 场景由 41 个 shell contracts 与 280 个 Python tests 一并回归，未发现本轮改造引入的新冲突。

## 7. 执行证据

```text
bash tests/validate-post-merge-memory-reconciliation.sh
PASS

bash tests/validate-lightweight-change-lane.sh
PASS

python3 -m unittest tests.test_memory_reconciliation_scan -v
15/15 PASS

python3 -m unittest tests.test_root_agents_lossless_slimming tests.test_project_guidance_consistency -v
8/8 PASS

for test_file in tests/*.sh; do bash "$test_file"; done
41/41 PASS

python3 -m unittest discover -s tests -p 'test*.py' -v
280/280 PASS

python3 -m unittest \
  tests.test_memory_reconciliation_scan \
  tests.test_memory_reconciliation_check \
  tests.test_memory_reconciliation_apply \
  tests.test_memory_reconciliation_restore \
  tests.test_memory_reconciliation_support \
  tests.test_root_agents_lossless_slimming \
  tests.test_root_agents_blocks \
  tests.test_project_guidance_consistency -v
100/100 PASS

ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
JSON structured parse
Python AST parse
Markdown opening-fence balance
git diff --check
PASS
```

其中 280/280 是最终独立审查前的全 Python 基线；独立审查修复 root route/revision 后，运行覆盖本轮增量的 100 个 Memory/Root/Project Guidance Python tests。最后补齐定向原子写入、Recovery boundary、报告回滚字段和 Apply/Restore Gate 后，再次运行 focused Post-Merge contract、root refresh/checker、16 个 Root/Project Guidance Python tests 与 `git diff --check`，均 PASS；随后再次运行全部 41 个 shell contract，结果见本报告顶部总计。

## 8. 当前问题与残余风险

### Low

正常 conflict-driven route 是自然语言 controller contract，不是一个独立的可执行 merge engine。因此真实 Agent 是否始终把“最小直接证据”控制在合理边界，仍需后续真实项目 merge 观察。当前通过 root/runtime/reference contract、负向断言、压力场景和显式 Full Audit CLI guard 限制漂移。

没有 Critical、High 或 Medium 当前问题。

## 9. 未采纳或降级意见

- 未删除四快照工具：它仍对广泛损坏、取证和事务恢复有价值，但已降级为显式 Full Memory Audit / Recovery。
- 未让 normal reconciliation 完全依赖 Git：Git clean merge 不能证明跨文件 current-state claim 或 direct locator 语义一致。
- 未要求每个冲突写报告：这会重新制造人类和 Agent 的流程负担；小冲突在会话内处理。
- 未把无关 drift 纳入当前冲突：只记录为后续 Recovery candidate，避免递归全库审计。

## 10. 工作区与发布判断

- 未创建目标项目 `.agent-loop/` 产物。
- `.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/` 为未跟踪生成内容，不属于提交范围。
- 当前变更可进入 Human Review。
- 本轮未获得 commit、push、tag、PR、merge、release 或 publish 授权。
- 未修改 Skill version，保持 `1.5.0`。
