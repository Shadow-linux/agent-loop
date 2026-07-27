# Agent Loop v1.5.2 全量验证报告（最小 Evidence Checker）

日期：2026-07-27
分支：`v1.5.2`
版本：`1.5.2`（开发中，未发布）
基线 HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
审计对象：AI-Led Lightweight Feature Gates、历轮 chaos repair 与第二轮 chaos 后的最小 Checker 职责之当前未提交工作区

## 结论

总分：**99 / 100 — STRONG**
当前发现：**Critical 0 / High 0 / Medium 0 / Low 2**
回归结果：**Shell 45 / 45 PASS；Python 333 / 333 PASS**
focused：**Feature checker 24 / 24；Python checker contract 21 / 21；Shell contract PASS**
平台证据：**macOS-verified / Windows-test-defined**
判断：功能与全仓语义可进入 Human Review / 提交审查；本报告不授权提交或发布。

本轮把 Checker 从 Markdown workflow parser 收敛为 deterministic evidence checker。Human provenance、Goal/Scope/Acceptance、Story/Task/Plan/No-Plan、风险与 drift 由 Agent 判断；Checker 只验证唯一当前 evidence fields、完整安全 manifest、digest equality 和最小 Gate/action pairing。

## RED → GREEN

第四轮新增并保存：

- 6 个 focused RED：结果命名越权、变化结果混杂、Task/Plan/Assessment 语义解析、digest 漏 detail、parent symlink/resolved alias、fenced field spoofing；实际 **6 / 6 failures**；
- 1 个 `digest` Gate 1 可复制摘要 RED；实际 **1 / 1 failure**。

GREEN 后：

```text
python3 -m unittest tests.test_feature_review
# Ran 24 tests — OK

python3 -m unittest tests.test_feature_review tests.test_python_checker_contract
# Ran 45 tests — OK

bash tests/validate-feature-construction-two-gate-review.sh
# PASS
```

完整 RED 证据见 `docs/reports/agent-loop-v1.5.2-feature-gate-chaos-repair-red-2026-07-27.md`。

## 全量回归

实时重新统计并执行：

```text
for test_file in tests/*.sh; do bash "$test_file"; done
# SHELL_TOTAL=45 SHELL_PASS=45 SHELL_FAIL=0

python3 -m unittest discover -s tests -p 'test_*.py' -q
# Ran 333 tests in 88.518s
# OK
```

Python 数量从旧报告 371 降为 333，是因为旧 `test_feature_review.py` 中 62 个 Checker 语义解析测试被 24 个 evidence-only 契约替换（净减 38），不是遗漏 discovery 或跳过测试。

## 机械检查

| 检查 | 结果 |
|---|---|
| `SKILL.md` YAML | PASS |
| `plugin.json` JSON | PASS |
| Shell syntax | 46 / 46 PASS |
| Ruby syntax | 5 / 5 PASS |
| Python AST | 47 / 47 PASS |
| Markdown fence parser | 308 / 308 PASS |
| `git diff --check` | PASS |
| root AGENTS 行数 | 176 |
| root managed blocks | 13 / 13，`1.5.2-20260727.2` |

## 六域语义审计

| 审计域 | 分数 | 结果与证据 |
|---|---:|---|
| Logic Correctness | 100 | 两个 Gate 保留；`EVIDENCE_MATCH/CHANGED/INVALID` 各自唯一；Checker 不再把 Markdown 语义猜测当授权 |
| Autonomy | 100 | Agent 可自主处理 within-boundary delta 与确定性 evidence repair；只有真实产品/执行边界或不确定 Human provenance 才询问 |
| Project Entry / Evidence Graph + DDD Onboarding | 99 | Requirement/ADR/Feature Context authority 未改变；root guidance 仍为 13 blocks 且相关 contract 全过 |
| Development / Test Workflow | 100 | Gate 1/2、Plan、TDD、Task Done、Verify/Review/Drift/Memory/Completion 与独立 Action Gates 保持 |
| Memory | 99 | Accepted Stories、initial Tasks、Plan/No-Plan 与 Assessment 继续作为 Agent-owned memory；无新 artifact family |
| Recommendation | 100 | changed -> AI review、invalid -> fact repair、real boundary -> owning Gate、checker contradiction -> Recovery，路由不重叠 |

加权总分：**99 / 100**。

## 通过的不变量与压力场景

1. Gate 1 与 Gate 2 的数量、Human choices、包准备/执行边界未改变。
2. `EVIDENCE_MATCH` 只表示证据一致，不证明 Human speech，不继承 Git/Contract/Subagent/Submit/Close/Release 权限。
3. package-only 不能 execute；later-start 保持 `start -> reliable Human instruction -> record approve-and-start/enabled/time -> execute`。
4. `digest` 与 review/start/execute 使用同一 manifest/path/digest kernel；漏 detail 不能生成可复制摘要。
5. `spec.md/tasks.md/tests.md`、`plan.md`（存在时）、optional context/contracts 与触发目录均纳入完整 Package；Stable 排除 rotatable Plans。
6. 非规范/重复路径、symlink component、resolved-target alias、root escape、非普通文件和 fenced current-field spoofing fail closed。
7. Task 增减/取消/替换、Story mapping、Plan/No-Plan、Assessment table 与 escaped pipe 不再由 Checker 猜测；AI 仍必须按 accepted boundary 硬停止越界工作。
8. Legacy `review-definition-v2` 可读取；新 evidence 使用 `raw-v1`，避免继续扩大 Markdown parser。
9. Delivery Contract、Human-gated Task、Subagent、Git、external、Submit、Pause、Close、commit、PR、merge、tag、release、publish Gates 未继承或删除。
10. Requirement、ADR、Feature Product Slice、Feature Context、Task Done、Completion 与 memory ownership 未改变。
11. 未新增 canonical stage、message intent、lifecycle、Auto Mode、目录或 executable schema。
12. 普通 Chat、Brief/Standard Product Definition、ADR optionality、Follow-up、stale memory、root guidance 等全仓场景由 45 个 Shell contract 与 333 个 Python tests 覆盖通过。

## 未采纳 / 降级意见

- 不继续增加 Task/Plan/Assessment Markdown parser：第二轮 chaos 已证明这会不断创造新假阳性/假阴性，且超出 Checker 的确定性职责。
- 不让 Checker 验证 Human provenance：同一 Agent 可写文件并调用本地工具，任何本地摘要都不能证明谁说过什么。
- 不把 `EVIDENCE_CHANGED` 当 Gate failure：它只触发 AI comparison；只有语义路由能决定 Gate 1、Gate 2 或继续。

## 剩余 Low 风险

- **Low-1：信任模型边界。** 设计默认运行 Agent 遵守 runtime 并读取真实会话；它不抵抗恶意 Agent 同时伪造全部本地状态。这是维护者明确接受的轻量边界。
- **Low-2：平台证据。** 本轮 macOS 实跑；Python 3.10+ 标准库与 Windows 路径拒绝/`py -3` 入口有测试定义，但未取得 Windows 实机结果。

## 范围与工作区保护

- 没有创建目标项目 `.agent-loop/`。
- 没有创建/切换分支或 worktree，没有同步 installed Skill。
- `AGENTS.md` 的既有一行修改、`.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/` 未清理、恢复、暂存或纳入本功能归属。
- 版本保持 `1.5.2`；root revision 保持 `1.5.2-20260727.2`。

## Git 与发布

未执行 `git add`、commit、push、tag、PR、merge、release、publish 或 `main` 同步。
