# AI-Led Lightweight Feature Gates 单功能验证报告（第三轮 Chaos Repair）

日期：2026-07-27
分支：`v1.5.2`
版本：`1.5.2`（开发中，未发布）
审计对象：第三轮 chaos 暴露的 deterministic evidence boundary 与 Pause/模板一致性修复

## 结论

评分：**99 / 100 — STRONG**
当前发现：**Critical 0 / High 0 / Medium 0 / Low 2**
提交判断：可进入 Human Review / 提交审查，但本报告不授权 Git 或发布动作。

## Scope Lock

目标：保持 Gate 1/2 轻量、AI-owned semantics 和 evidence-only Checker；补齐 Stable closure、UTF-8、manifest、same-file alias、fence 与跨平台路径的确定性缺口，并消除 `raw-v1`、Pause 和 inline notes 的跨文件歧义。

非目标：不恢复 Task/Story/Plan/No-Plan/Assessment parser；不新增 Gate、stage、lifecycle、Auto Mode、artifact family、schema 或授权签发系统；不改变独立 Contract/Subagent/Git/Submit/Close/Release Gates。

## 五域评分

| Domain | 得分 | 结论 |
|---|---:|---|
| Requirement And Scope Fidelity | 15 / 15 | 完整遵守“Checker 只检查摘要和可信清单”的人类确认方向，没有扩张语义职责 |
| Logic, State, And Human Gates | 30 / 30 | Gate/action pair 与 evidence outcomes 唯一；Pause 使用 live Gate Mode，不破坏 durable Gate history |
| Cross-Surface Consistency | 20 / 20 | runtime/design/artifact/stage/completion/checklist/direct+inline template/scenario/Proposal/Plan 已协调 |
| Pressure Resistance | 24 / 25 | 两个独立只读 chaos 方向转绿；扣 1 分仅因 Windows 没有实机 runner |
| Evidence And Maintainability | 10 / 10 | 保存真实 RED、focused GREEN、同 fixture 复测与全仓验证；无放宽断言 |
| **总分** | **99 / 100** | **STRONG** |

## RED / GREEN / REFACTOR

- RED：30 个 Feature checker tests 中 6 个失败；Shell contract 在 `raw-v1` 冲突处失败。
- GREEN：Feature checker + Python checker contract **51 / 51 PASS**；Two-Gate Shell contract PASS。
- Chaos GREEN：evidence **79 / 79**；lifecycle executable **31 / 31**；lifecycle semantic **51 / 51**。
- REFACTOR：非法 UTF-8 从 12 条噪音收敛为 1 条 `EVIDENCE_INVALID`，先观察 **1 / 1 RED** 再修复。

## 压力场景矩阵

| 场景组 | 结果 |
|---|---|
| package-only review/start 与 approve-and-start execute | PASS |
| Task 增删、取消、替换、合并、拆分与 Plan rotation | PASS；语义由 AI 判断 |
| 新 Story/Product Slice/Human-gated Task | PASS；Checker 不冒充语义 Gate，AI 保持硬停止 |
| Package/Stable/triggered detail closure | PASS |
| empty item、POSIX/Windows absolute、same-file alias、symlink/root escape | PASS |
| invalid UTF-8 与 malformed fence closing | PASS；结构化 INVALID，无 traceback/伪字段 |
| Pause/Resume current mode 与 durable Gate pair | PASS；单一持久化路径 |
| Contract/Subagent/Git/Submit/Close/Release 独立 Gate | PASS；无权限继承 |

## 实际命令

```text
python3 -m unittest tests.test_feature_review tests.test_python_checker_contract
# 51 / 51 PASS

bash tests/validate-feature-construction-two-gate-review.sh
# PASS

python3 /tmp/agent-loop-evidence-chaos-3-harness.py
# 79 / 79 PASS

python3 /tmp/agent-loop-lifecycle-chaos-3-run.py
# 31 / 31 PASS

for test_file in tests/*.sh; do bash "$test_file"; done
# 45 / 45 PASS

python3 -m unittest discover -s tests -p 'test_*.py' -q
# 339 / 339 PASS
```

机械检查：YAML、JSON、Shell 46/46、Ruby 5/5、Python AST 47/47、Markdown fence 310/310、`git diff --check` 全部 PASS。

## 剩余风险

- Low：轻量信任模型不抵抗恶意 Agent 同时伪造全部本地 evidence；这是已确认取舍。
- Low：Windows 行为由跨平台路径测试定义，未取得 Windows 实机运行证据。

## Git 与发布

未 stage、commit、push、tag、PR、merge、release、publish 或同步 installed Skill。
