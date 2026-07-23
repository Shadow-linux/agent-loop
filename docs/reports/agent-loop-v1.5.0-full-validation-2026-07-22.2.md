# Agent Loop v1.5.0 全量验证报告（Product Review / Reasoned ADR checker 修复）

## 1. 审计对象与结论

- 日期：2026-07-22
- 分支：`alpha/v1.5.0`
- HEAD：`e07d50c2c2b0bf80ad22b579e3a476bb71218c06`
- Skill 版本：`1.5.0`，未升级
- Root managed block：13 个，统一为 `1.5.0-20260721.2`，未修改
- 审计对象：当前工作区中 Adaptive Requirement Product Definition 的全部未提交改动，以及本轮针对独立复评 R1 / R2 的修复
- 当前结论：**99 / 100，STRONG**
- 当前严重问题：Critical `0`、High `0`、Medium `0`、Low `1`

本报告取代 `agent-loop-v1.5.0-full-validation-2026-07-22.1.md` 的当前结论。旧报告仍保留为修复前历史证据；独立复评发现的 R1 / R2 已在本轮用真实 RED 回归关闭。

## 2. 本轮修复范围

| 文件 | 修复内容 |
|---|---|
| `scripts/check-adr-requirement-model-trace.py` | reasoned Brief 与 legacy `concept-foundation-not-needed` 早退前拒绝伪造 `Concept Definitions`、`Requirement Model Scope Inventory`、`Requirement Model Technical Landing Trace` 区块 |
| `scripts/requirement_product_support.py` | 增加共享、行首锚定、大小写不敏感的 `is_confirmed_review_evidence()` 判定 |
| `scripts/check-concept-foundation-trace.py` | 改用共享 Product Review Evidence 判定，拒绝 `unconfirmed` 等包含 `confirmed` 子串的假证据 |
| `scripts/check-requirement-product-definition.py` | 改用同一共享判定，消除两个 checker 的结果漂移 |
| `tests/test_adr_requirement_model_trace.py` | 增加 Brief 三类伪造区块与 legacy 共享早退路径的回归攻击 |
| `tests/test_concept_foundation_trace.py` | 增加 `unconfirmed pending human review` 的跨 checker 回归 |
| `CHANGELOG.md` | 记录 checker hardening，不改变版本号 |
| 本报告 | 保存 RED / GREEN、全量验证、语义审计与剩余风险 |

未修改 runtime/design 语义：`references/runtime.md` 已要求 no-model ADR 不得伪造这些产品模型区块；本轮修复的是 checker 与既有合同之间的执行缺口。

## 3. RED 基线

修复前先建立现有基线：

```text
tests/*.sh: 40 / 40 PASS
python3 -m unittest discover -s tests -p 'test_*.py': 255 / 255 PASS
```

随后只增加回归测试，不修改生产 checker：

```bash
python3 -m unittest \
  tests.test_adr_requirement_model_trace.ProductDefinitionAdrTraceTests.test_reasoned_brief_rejects_fabricated_model_sections \
  tests.test_adr_requirement_model_trace.ProductDefinitionAdrTraceTests.test_reasoned_legacy_source_rejects_fabricated_model_sections \
  tests.test_concept_foundation_trace.ConceptFoundationTraceTests.test_requirement_product_mode_rejects_unconfirmed_review_evidence
```

真实 RED：

```text
Ran 3 tests
FAILED (failures=4)

Brief + fabricated Scope Inventory: checker 错误 PASS
Brief + fabricated Technical Landing Trace: checker 错误 PASS
legacy not-needed + fabricated Scope Inventory: checker 错误 PASS
Product Review Evidence: unconfirmed: concept checker 错误 PASS
```

对 runtime 同一句禁止规则继续做同类边界检查：Brief 加入伪造 `Concept Definitions` 时再次得到目标 RED：

```text
Ran 1 test
FAILED (failures=1)
PASS: reasoned confirmed Brief ADR proposed gate is complete
```

这些失败均由目标漏洞造成，不是 fixture、路径或测试框架错误。

## 4. GREEN 与 focused validation

最小修复后，同一 targeted 命令：

```text
Ran 3 tests in 0.459s
OK
```

最终 focused Python：

```bash
python3 -m unittest \
  tests.test_adr_requirement_model_trace \
  tests.test_concept_foundation_trace \
  tests.test_requirement_product_definition \
  tests.test_python_checker_contract
```

结果：`73 / 73 PASS`。

受影响的 Shell contracts 全部通过：

- `validate-adaptive-requirement-product-definition.sh`
- `validate-adr-requirement-model-technical-landing-trace.sh`
- `validate-concept-foundation-requirement-modeling.sh`
- `validate-decision-design-requirement-landing.sh`
- `validate-product-brief-source-gate.sh`
- `validate-project-decisions-adr-lane.sh`
- `validate-requirement-product-grill.sh`

## 5. 全量回归与机械检查

最终生产代码冻结后重新执行，不复用第一次 GREEN 数字：

| 检查 | 结果 |
|---|---:|
| 实时枚举 `tests/*.sh` | `40 / 40 PASS` |
| `python3 -m unittest discover -s tests -p 'test_*.py'` | `258 / 258 PASS`，93.945 秒 |
| `SKILL.md`、`agents/openai.yaml` YAML | `2 / 2 PASS` |
| `plugin.json` JSON | `1 / 1 PASS` |
| 全仓 Shell syntax | PASS |
| 全仓 Ruby syntax | `5 / 5 PASS` |
| `scripts/`、`tests/` Python AST | `41 / 41 PASS` |
| Markdown fence balance | `267 / 267 PASS` |
| `git diff --check` | PASS |

当前验证环境为 macOS。未在本轮启动独立 Windows runner；修复只使用 Python 3.10+ 标准库、字符串正则与既有 Markdown section parser，现有跨平台 contract 全部通过。结论记录为 `macOS-verified / Windows-contract-regressed`，不声称本轮完成真实 Windows 执行。

## 6. 代表性压力路径

| 路径 / 攻击 | 结果 |
|---|---|
| Standard `product.md` → Product Slice definition checker | PASS |
| Standard `product.md` → Concept trace checker | PASS |
| Standard `product.md` → ADR 11 个 source refs / 11 landed rows | PASS |
| Brief `product.md` → Product Slice，无 ADR | PASS |
| Brief → reasoned no-model ADR，无伪造模型区块 | PASS |
| legacy reasoned `concept-foundation-not-needed` ADR | PASS |
| Brief 伪造 `Concept Definitions` | 拒绝 |
| Brief 伪造 Scope Inventory | 拒绝 |
| Brief 伪造 Technical Landing Trace | 拒绝 |
| legacy 共享早退路径伪造 Scope Inventory | 拒绝 |
| `Product Review Evidence: unconfirmed pending human review` | 两个 checker 均拒绝 |

共享谓词为：`^confirmed(?:\s|$)`、`re.IGNORECASE`。全仓扫描未发现旧的 `"confirmed" not in normalized(...)` 子串判断；两个 Product Slice checker 现在消费同一函数。

## 7. 六域语义审计

| 审计域 | 得分 | 加权 | 结论 |
|---|---:|---:|---|
| Logic Correctness | 98 | 19.6 / 20 | R1/R2 均关闭；保留一个不影响 fail-closed 的 Low 诊断文案问题 |
| Autonomy | 100 | 15 / 15 | 未改变 Agent Ownership、唯一下一阶段或调查优先级 |
| Project Entry / Evidence Graph + DDD Onboarding | 100 | 15 / 15 | 无入口、Onboarding 或 root routing 漂移 |
| Development / Test Workflow | 97 | 19.4 / 20 | TDD、focused、全量与机械验证完整；本轮未运行真实 Windows runner |
| Memory | 100 | 15 / 15 | 未改变 Requirement/Feature/Project memory ownership |
| Recommendation | 100 | 15 / 15 | Product Review、ADR Human Gate 与 Git Gate 仍独立且无新增旁路 |
| **总分** | | **99 / 100** | **STRONG** |

关键不变量检查：

- Requirement `product.md` 继续拥有有效产品定义；Feature `spec.md` 只消费 Product Slice，不重定义产品语义。
- Product Review `confirmed` 继续是新 Effective Product Definition 的不可绕过 Gate。
- reasoned Brief / legacy not-needed 仍可进入 ADR preflight，但只能使用 `Trace Applicability: not-applicable` 的无模型形态。
- Standard Product Definition 的 Scope Inventory / Technical Landing Trace 完整覆盖没有被削弱。
- ADR proposed preflight、accepted-mode Human Review、Feature、commit、push、tag、release 等 Gate 未合并或放宽。
- 未新增 canonical stage、message intent、artifact、schema、依赖或版本号。

## 8. 剩余问题与风险

### Low：legacy Coverage Hard Gate 错误信息不够精确

legacy Gate 混合或增加条款时能够正确 fail closed，但部分集合不匹配仍可能报告为 `missing required items`，排查体验不够精确。它不改变路由、状态、授权或 Human Gate 结论，因此不在本轮 R1/R2 修复范围内。

### 平台证据

本轮没有真实 Windows runner 证据。现有 Windows/POSIX contract 与全部本地回归通过，但跨平台发布验收仍应沿用仓库 CI，而不能由本报告替代。

## 9. 范围漂移与 Git 状态

- 分支仍为 `alpha/v1.5.0`；Skill 版本仍为 `1.5.0`。
- 13 个 root managed block revision 仍为 `1.5.0-20260721.2`。
- 没有创建目标项目 `.agent-loop/` artifact。
- 没有创建或切换分支/worktree。
- 保留了本轮开始前已有的全部无关 dirty work；没有恢复、删除、暂存或提交它们。
- 本轮未执行 stage、commit、push、tag、PR、merge、release、publish 或 installed Skill 同步。

## 10. 发布判断

R1 与 R2 已由 RED → GREEN 回归关闭，当前无 Critical / High / Medium。该工作区可以进入 Human Review；是否提交仍需独立的人类 Git 授权。
