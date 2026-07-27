# AI-Led Lightweight Feature Gates 专项验证报告（最小 Evidence Checker）

日期：2026-07-27
分支：`v1.5.2`
版本：`1.5.2`（开发中，未发布）
基线 HEAD：`9a5c5183b47c022e8851f1098697f902e9d38daa`
审计对象：当前未提交工作区中的 Feature Gate 1/2、later-start、AI semantic ownership 与最小 evidence checker

## 结论

总分：**98 / 100 — STRONG**
当前发现：**Critical 0 / High 0 / Medium 0 / Low 2**
focused Feature checker：**24 / 24 PASS**
相关 Python checker contract：**21 / 21 PASS**
专项 Shell contract：**PASS**
判断：可进入最终 Human Review / 提交审查；本报告不授权 commit、push、tag 或发布。

## 最终职责边界

```text
Human provenance、Goal/Scope/Acceptance、Story/Task/Plan/No-Plan、风险与漂移
  -> Agent 读取证据并判断

唯一当前 evidence fields、Gate/action pairing、完整安全 manifest、digest equality
  -> check-feature-review.py 确定性校验
```

Checker 只暴露 `review | start | execute | digest`，结果族为：

- `EVIDENCE_MATCH`（exit 0）：清单安全完整、摘要一致、动作配对一致；不是 Human authorization 证明；
- `EVIDENCE_CHANGED`（exit 3）：有效证据字节发生变化，路由 AI Semantic Review；
- `EVIDENCE_INVALID`（exit 1）：字段、清单、路径、摘要格式或动作配对不合法。

新 evidence 默认 `raw-v1`；Stable manifest 排除 `plan.md` / `plans/*`。显式 legacy `review-definition-v2` 保持 reader compatibility，但不再承担语义验证。

## RED → GREEN

第四轮先保存 6 个真实 RED：正常结果命名越权、digest drift 结果混杂、Task/Plan/Assessment 语义解析、digest 漏 detail、父目录 symlink/resolved alias、fenced field spoofing。实际为 **6 / 6 failures**。随后为 `digest` 缺少 Gate 1 可复制摘要补充 **1 / 1 failure**。

GREEN 后：

```text
python3 -m unittest tests.test_feature_review
# Ran 24 tests — OK

python3 -m unittest tests.test_feature_review tests.test_python_checker_contract
# Ran 45 tests — OK

bash tests/validate-feature-construction-two-gate-review.sh
# PASS
```

RED 原始输出与历轮 chaos 脉络保存在 `docs/reports/agent-loop-v1.5.2-feature-gate-chaos-repair-red-2026-07-27.md`。

## 压力场景矩阵

| 场景 | 期望与结果 |
|---|---|
| package-only review | `EVIDENCE_MATCH` |
| package-only 直接 execute | `EVIDENCE_INVALID` |
| later-start `start -> record -> execute` | 两次均 `EVIDENCE_MATCH`，Human intent 由 Agent 判断 |
| approve-and-start / Auto-Loop 配对错误 | `EVIDENCE_INVALID` |
| Spec 或 Stable bytes 变化 | `EVIDENCE_CHANGED`，不自动宣称 Gate invalid |
| 只轮换 `plan.md` 后 execute | Stable evidence 仍 match；Plan 语义由 AI 检查 |
| Task 新 Story、Human-gated、mixed Derived From | Checker 不解析；AI 必须硬停或回 Gate 2 |
| duplicate Plan Scope / malformed Assessment / escaped pipe | 不再制造 Checker 语义错误 |
| 缺 `spec.md/tasks.md/tests.md` 或触发目录 detail | `EVIDENCE_INVALID` |
| `./`、`..`、absolute、backslash、duplicate path | `EVIDENCE_INVALID` |
| notes/file/parent symlink、resolved-target alias | `EVIDENCE_INVALID` |
| fenced Gate field example | 不计入当前 evidence，缺字段为 `EVIDENCE_INVALID` |
| legacy `review-definition-v2` runtime ledger 更新 | reader-compatible；定义变化仍 `EVIDENCE_CHANGED` |
| `digest` | 只读，先校验 manifest，再输出 Gate 1/Package/Stable 当前摘要 |

第二轮两个只读 chaos Agent 的结果用于形成本轮 RED；本轮 GREEN 由主 Agent 使用相同攻击维度的 focused fixtures 复测。未在缺少新授权时再次派发 Agent。

## 五域评分

| Domain | 得分 | 说明 |
|---|---:|---|
| Requirement And Scope Fidelity | 15 / 15 | 按人类确认把 Checker 收敛为摘要及覆盖校验，两个 Human Gate 与独立 Gates 未改变 |
| Logic, State, And Human Gates | 30 / 30 | 结果不再冒充授权；changed/invalid/match 路由唯一；later-start 动作配对仍受控 |
| Cross-Surface Consistency | 20 / 20 | SKILL/runtime/design/stage/template/root/human docs/scenarios/tests 已协调 |
| Pressure Resistance | 23 / 25 | 第二轮 chaos 漏洞均有 GREEN 回归；未进行修复后的新一轮独立 Agent 实机复测，Windows 未实机 |
| Evidence And Maintainability | 10 / 10 | 真实 RED、focused/full、机械检查及中文报告完整 |
| **总分** | **98 / 100** | **STRONG** |

## 剩余 Low 风险

1. 轻量模型信任守规 Agent；Checker 不抵抗恶意 Agent 同时伪造 Human evidence 与全部本地字段。这是人类明确接受的设计边界。
2. 本轮为 macOS 实跑；Windows 保持 `macOS-verified / Windows-test-defined`。Legacy v2 只作兼容读取，新证据不再依赖其 Markdown 投影。

## Git 与发布

未 stage、commit、push、tag、PR、merge、release、publish，也未同步 installed Skill。
