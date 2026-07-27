# Agent Loop v1.5.2 全量验证报告

日期：2026-07-27
分支：`v1.5.2`
版本：`1.5.2`（开发中，未发布）
基线 HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`（`stable-v1.5.1`）
审计对象：当前未提交工作区中的 AI-Led Lightweight Feature Gates coordinated workflow change

## 结论

> **后续混沌审计更正（2026-07-27）：** 本报告记录的是实施结束时的既有测试与六域审计结果。随后两条独立 Feature chaos 测试线发现 1 个 Critical、3 个 High 和 2 个 Medium，包含重复 Gate 字段覆盖执行授权与合法同 Story Task replacement 被误阻断。因此本报告原 `99 / 100 — STRONG` 与“可进入提交审查”的判断已被后续证据撤销，当前验收以 [ai-led-lightweight-feature-gates-feature-validation-2026-07-27.md](ai-led-lightweight-feature-gates-feature-validation-2026-07-27.md) 的 `67 / 100 — FRAGILE` 为准；修复并复跑 full validation 前不得据此提交。

> **修复后状态：** 上述阻断项及第二轮混沌复测发现已完成 TDD 修复；新的验收权威为 [agent-loop-v1.5.2-full-validation-2026-07-27.2.md](agent-loop-v1.5.2-full-validation-2026-07-27.2.md) 与 [ai-led-lightweight-feature-gates-feature-validation-2026-07-27.2.md](ai-led-lightweight-feature-gates-feature-validation-2026-07-27.2.md)。本文件继续保留为历史验证快照。

总分：**99 / 100 — STRONG**
当前发现：**Critical 0 / High 0 / Medium 0 / Low 2**
回归结果：**Shell 45 / 45 PASS；Python 348 / 348 PASS**
平台证据：**macOS verified / Windows-test-defined**
发布判断：实现与验证已满足 Human Review 条件；尚未获得 commit、push、tag、release、`main` 同步或 installed Skill 同步授权，因此不是正式稳定发布。

## RED 基线与 GREEN 证据

RED 详情见 [agent-loop-v1.5.2-lightweight-feature-gates-red-baseline-2026-07-27.md](agent-loop-v1.5.2-lightweight-feature-gates-red-baseline-2026-07-27.md)。

- 实施前 Shell：45 个，43 PASS / 2 个既有日期断言失败；实际 Changelog 日期为 2026-07-27，旧测试仍写 2026-07-25。
- 实施前 Python discovery：335 / 335 PASS。
- focused pre-RED：27 / 27 PASS。
- 首个 focused RED：35 tests / 10 failures，真实证明旧 Checker 只有通用 `FAIL`、无法消费 exact Assessment，且把初始 Task IDs 当永久白名单。
- 额外 RED：`T003 [US2]` 仅凭 `Derived From: T001` 曾错误得到 `GATE_VALID`；新增反例后修复为 accepted Story 映射不可替代。
- 最终 focused GREEN：`python3 tests/test_feature_review.py -v`，39 / 39 PASS。
- checker platform/stdlib contract：`python3 -m unittest tests.test_python_checker_contract -v`，21 / 21 PASS。
- two-gate coordinated contract：`bash tests/validate-feature-construction-two-gate-review.sh`，PASS。

## 全量回归

执行命令：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -v
```

结果：

- Shell 实时计数：45；首次实现后 44 PASS / 1 FAIL，失败项仅为旧压力测试仍锁定 `disclosed Agent-ready scope` 文案；将契约断言更新为 `accepted execution boundary` 后重跑为 **45 / 45 PASS**。
- Python 实时计数：**348 / 348 PASS**，耗时 64.773s。
- 没有删除或放宽 Gate、Task Done、Feature Context、Requirement/ADR、Delivery Contract、Branch/Git、Submit、Close、Release 相关测试。

## 机械检查

| 检查 | 结果 |
|---|---|
| `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'` | PASS |
| 3 个仓库 JSON 文件结构解析 | PASS |
| 46 个 Shell 文件 `bash -n` | PASS |
| 5 个 Ruby 文件 `ruby -c` | PASS |
| 全仓库 Markdown fence balance | PASS |
| `git diff --check` | PASS |
| Python 3.10+ / stdlib-only checker contract | PASS |
| root managed blocks | 13 / 13 为 `1.5.2-20260727.1` |

## 六域语义审计

| 审计域 | 分数 | 结果 | 主要证据 |
|---|---:|---|---|
| Logic Correctness | 100 | PASS | runtime/design 同步声明 AI/Checker 分工；typed outcomes、exact binding、hard blocks 和新 Task 边界均有正反例 |
| Autonomy | 100 | PASS | `ASSESSMENT_REQUIRED` 先路由 AI Semantic Review；仅 `unresolved` 或真实边界变化打断人类 |
| Project Entry / Evidence Graph + DDD Onboarding | 99 | PASS | Feature Context 与 Requirement/ADR authority 未改变，相关 Shell/Python 回归全绿 |
| Development / Test Workflow | 100 | PASS | 两个 Gate、Plan Gate、Analyze Consistency、TDD、Task Done、Verify/Review/Drift/Memory/Completion 均保持 |
| Memory | 98 | PASS | Assessment 绑定 Feature/Gate/baseline/current，Resume/compaction/later start 必须重新核对；无新 artifact family |
| Recommendation | 99 | PASS | 四种 AI 分类与三种 checker outcome 均有唯一 owning route，Human Review 收敛为最小决策表 |

加权总分按整数报告为 **99 / 100**。

## 关键不变量与压力场景

已确认：

1. Gate 1 与 Gate 2 保留，且仍分别授权 Feature 定义/包准备与执行边界/开工选择。
2. AI 负责语义完整性与边界漂移；Checker 不解析产品语义，只验证 Human Gate/action scope、Task/Plan 绑定、结构证据和 exact Assessment reuse。
3. Digest mismatch 返回 `ASSESSMENT_REQUIRED`，不会自动改写 baseline 或直接宣称 Gate invalid。
4. `feature-definition-change` 回 Gate 1；`implementation-boundary-change` 回 Gate 2；`unresolved` 只问一个阻塞问题。
5. 新 Task ID 可在同一 accepted Story/Product Slice/Acceptance 内继续，但必须存在、Agent-ready、映射 accepted Story、Plan 有效并绑定 exact current Gate 2 Assessment。
6. `Derived From` 只能追溯，不能替代 Story 映射或夹带新 Story。
7. 缺 Gate、package-only 执行、Human-gated Task、missing Task、story mismatch、malformed/stale/copied Assessment 继续硬阻断。
8. Delivery Contract、subagent、Git、external、Submit、Pause、Close、commit、PR、merge、tag、release 和 publish Gate 未被 Feature Gate 继承。
9. Requirement `product.md`、ADR、Feature Product Slice、Feature Context、Task Done、Feature Completion 与项目记忆 ownership 未改变。
10. 未新增 canonical stage、message intent、lifecycle、Auto Mode、JSON/YAML executable schema 或独立 Gate artifact。

代表性压力场景：Gate 1 metadata/evidence refresh、Gate 2 stable drift、package-only later start、Plan rotation、new mapped Task、new Story smuggling、Human-gated Task、wrong Feature/baseline/current binding、malformed timestamp、legacy `raw-v1`、unknown algorithm、missing durable evidence，全部得到预期结果。

## Proposal Phase / 验收符合性

Proposal 的 10 条验收条件全部落实：

- Human Review 已压缩为 Gate 1 四项与 Gate 2 四项，完整 artifacts 保持 authority；
- AI/Checker 责任边界、Digest change signal、typed outcomes 已同步到 runtime/design/reference/template/human docs；
- within-boundary Assessment 与新增 Task 路由已实现并有 RED/GREEN；
- hard authorization、mapping 和 independent Human Gates 保持；
- 无范围扩张与新增状态/目录/schema；
- focused 与 full validation 已完成。

## 当前风险

### Low-1：AI 语义判断不可由结构 Checker 证明

这是已确认的责任边界：Checker 只能验证 Assessment 绑定与结构，不能判断 `Reason` 是否真的保持产品语义。通过 compact Gate Summary、四类诊断、`unresolved` stop rule、exact fingerprint binding 和反例测试降低风险。

### Low-2：本机未直接执行 Windows runner

实现仅用 Python 3.10+ 标准库，保留 `py -3` 路径与 cross-platform checker contract；本轮在 macOS 实跑全部测试，Windows 证据为测试定义与 CI contract，故标记 `macOS-verified / Windows-test-defined`。

## 范围漂移与工作区保护

- 没有创建目标项目 `.agent-loop/`。
- 没有创建/切换额外 worktree，也没有同步 installed Skill。
- `AGENTS.md` 的 stable tag 规范修改、`.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/` 均为实施前已有或无关 dirty work，本轮未恢复、清理、暂存或纳入实现结论。
- 安装示例仍指向最新正式 tag `stable-v1.5.1`；仓库中没有 `stable-v1.5.2` 发布或安装声明。

## Git 与发布状态

当前未执行 `git add`、commit、push、tag、PR、merge、release、publish、`main` 同步或 installed Skill 同步。下一步是维护者 Human Review；通过后再单独决定 Git 与发布动作。
