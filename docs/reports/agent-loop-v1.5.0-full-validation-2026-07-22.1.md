# Agent Loop v1.5.0 Adaptive Requirement Product Definition 评测回流全量验证报告

日期：2026-07-22
分支：`alpha/v1.5.0`
基线 HEAD：`e07d50c2c2b0bf80ad22b579e3a476bb71218c06`
Skill 版本：`1.5.0`（未升级）
审计对象：当前工作区中完整 Adaptive Requirement Product Definition 实现，以及独立单功能评测报告指出问题的 flow-back 修复
验证平台：macOS 本机；Windows 为标准库、BOM/CRLF、Windows-style path contract-defined，未取得原生 Windows 执行证据

## 1. 结论

总分：**100 / 100，STRONG**。

- 当前 Critical：`0`；
- 当前 High：`0`；
- 当前 Medium：`0`；
- 独立评测的 `4 High + 2 Medium` 已逐项关闭；
- focused Python：`51/51 PASS`；
- affected Shell：`14/14 PASS`；
- 全部 Shell：`40/40 PASS`；
- 全部 Python：`255/255 PASS`；
- Ruby adversarial：`2/2 PASS`；
- YAML、JSON、Shell syntax、Python compile、Markdown fence、`git diff --check` 均通过；
- 当前可进入最终 Human Review，但本轮未获 commit、push、tag、PR、merge、release、publish 或 installed-skill sync 授权。

## 2. 独立评测问题关闭情况

输入报告：`docs/reports/adaptive-requirement-product-definition-feature-validation-2026-07-22.md`。

| 评测问题 | 修复 | 回归证据 | 当前状态 |
|---|---|---|---|
| High-1 Brief → ADR deadlock | confirmed Brief 无 stable model/rule 时允许 reasoned `Trace Applicability: not-applicable`，不制造模型表 | `test_confirmed_brief_allows_reasoned_not_applicable_trace` | closed |
| High-2 legacy source + current decision gate rejected | legacy reader 接受“精确旧 gate”或“精确统一 gate”，混合/额外条款仍拒绝 | `test_legacy_source_accepts_the_current_unified_gate_template` + adversarial gate tests | closed |
| High-3 Brainstorm checklist 反向写入旧 owner | Requirements Discussion 改为 Requirement `product.md`；Feature 只写 `spec.md` / `notes.md` | focused shell ownership assertions | closed |
| High-4 Product Human Review 可被总合同 bypass | runtime/design/human-review/product-definition 明确新 Effective Product Definition 不可绕过 Product Human Review | P9 urgent-bypass scenario + focused shell | closed |
| Medium-1 Scenario 65 stale | 改为 Adaptive Product Definition / Standard depth / applicability / one-blocker /独立 Gate | focused shell Scenario 65 assertion | closed |
| Medium-2 record/archive placeholder split | 新工作统一 `<record-date>-<topic>`；design 解释其为记录/归档日期，legacy 名称保持可读 | focused shell cross-surface negative assertions | closed |

同时关闭的 Low：

- Feature Product Review Evidence 从子串判断改为起始状态词精确判断，`unconfirmed` 不再通过；
- README `Last Confirmed` 与 Product Human Review `Confirmed At` 必须一致；`Previous Source` 必须存在、受目录约束且不能指向当前 source；
- ADR snapshot 禁止混合 Product Definition 与 legacy Concept Foundation metadata；
- Brief 膨胀守卫补齐模板明确标注的三个 Standard-only section；
- Analyze Consistency 只在 legacy Feature `product.md` 存在时读取；
- Usage 产出 owner 改为 Requirement `product.md`；
- legacy example 增加明确标识，adaptive example 登记进 Skill Package Map；
- README 顶层流程不再把 Requirements Discussion 显示两次；
- 评测指出的 5 个 Shell 执行位已恢复，当前无 mode-only diff。

未采纳的 Low 建议：不新增 `Product Consensus Candidates` 平行标记。当前 `Decision Candidates` 已是唯一 owner；Proposal 明确不恢复 Product Design Hub / Board / Workbench，增加旧 marker 会制造第二套术语和状态入口。

## 3. RED → GREEN

### 3.1 修复前 focused 基线

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
python3 -m unittest -v \
  tests.test_requirement_product_definition \
  tests.test_concept_foundation_trace \
  tests.test_adr_requirement_model_trace
```

结果：Shell PASS；Python `44/44 PASS`。说明旧 suite 本身是 GREEN，但覆盖边界不足。

### 3.2 评测回流 RED

新增回归契约后：

```bash
python3 -m unittest -v \
  tests.test_requirement_product_definition \
  tests.test_adr_requirement_model_trace
```

结果：exit `1`，`Ran 42 tests in 2.684s`，`FAILED (failures=8)`。

Shell coordinated contract 同时 exit `1`：

```text
FAIL: references/runtime.md missing: Product Human Review confirmation cannot be bypassed for a new Effective Product Definition.
```

完整 RED 证据：`docs/reports/agent-loop-v1.5.0-adaptive-requirement-product-definition-review-repair-red-2026-07-22.md`。

### 3.3 GREEN

```bash
python3 -m unittest -v \
  tests.test_requirement_product_definition \
  tests.test_concept_foundation_trace \
  tests.test_adr_requirement_model_trace
bash tests/validate-adaptive-requirement-product-definition.sh
```

结果：Python `51/51 PASS`；Shell PASS。新增的 Brief→Feature Product Slice 正向 fixture 同样通过。

计划指定的 13 个 affected Shell，加上独立评测涉及的 grill artifact template contract：`14/14 PASS`。

## 4. 全量可执行回归

### 4.1 全部 Shell

```bash
shell_total=$(find tests -maxdepth 1 -type f -name '*.sh' | wc -l | tr -d ' ')
for test_file in tests/*.sh; do bash "$test_file"; done
```

实时统计结果：`40/40 PASS`。完成最后的人类文档与 cross-surface assertion 后再次执行，仍为 `40/40 PASS`。

### 4.2 全部 Python

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

最终结果：`Ran 255 tests in 115.513s`，`OK`。

### 4.3 Ruby adversarial

```bash
ruby tests/validate-adr-requirement-model-trace-adversarial.rb
ruby tests/validate-concept-foundation-trace-adversarial.rb
```

结果：`2/2 PASS`。旧/new gate mutation、缺失 coverage、未知 owner、placeholder reason、无 Human Review 等负向输入均被拒绝。

## 5. 机械检查

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md"); YAML.load_file("agents/openai.yaml")'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
find scripts tests -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
# 全仓 Markdown fence balance scan
git diff --check
```

| 检查 | 结果 |
|---|---|
| YAML | `2/2 PASS` |
| JSON | `1/1 PASS` |
| Python compile | PASS |
| Shell syntax | PASS |
| Markdown fence | `265/265 PASS` |
| `git diff --check` | PASS |
| untracked text whitespace/final newline 补充检查 | `34` 个相关文件 PASS；Markdown 合法双空格换行允许 |
| Skill version | `1.5.0` |
| root managed blocks | `13/13`，revision `1.5.0-20260721.2` |
| 仓库根 `.agent-loop/` | 不存在 |
| 恢复执行位 | `5/5` executable，且无 mode-only diff |

## 6. 六域语义审计

| Domain | 权重 | 得分 | 结果 | 关键证据 |
|---|---:|---:|---|---|
| Logic Correctness | 20 | 100 | PASS | Brief/Standard、new/legacy、not-applicable、snapshot shape、freshness、non-bypass Gate 无冲突/死锁 |
| Autonomy | 15 | 100 | PASS | Agent 做 depth/completeness scan、one-blocker 推荐；不把 internal method 交给人类选择 |
| Project Entry / Onboarding | 15 | 100 | PASS | root 只做 first-hop；Requirement product owner 与 byte-stable source 边界未破坏 |
| Development / Test Workflow | 20 | 100 | PASS | Product Review、Requirement lifecycle、ADR、Feature、Plan/TDD、Git Gates 独立；RED/GREEN 与全量回归完整 |
| Memory | 15 | 100 | PASS | README pointer/freshness、append-only previous source、legacy reader 和 Product Slice ownership 一致 |
| Recommendation | 15 | 100 | PASS | Brief 快路径、Standard signal、ADR if needed、urgent bypass 与 conflict recovery 均有唯一下一步 |
| **总计** | **100** | **100** | **STRONG** | Critical/High/Medium = `0/0/0` |

## 7. 代表性压力场景

| 场景 | 结果 | 证据 |
|---|---|---|
| 复杂 Requirement → Standard → ADR → Feature Product Slice | PASS | standard fixture、new ADR `11` refs、Product Slice checker |
| 简单 Requirement → Brief → Feature Product Slice，无 ADR | PASS | `brief-valid/spec.md` + direct handoff test |
| confirmed Brief 因共享技术决策进入 ADR | PASS | reasoned no-model trace-not-applicable test |
| legacy source 使用 current decision template | PASS | unified gate compatibility test |
| old legacy decision 保持旧 gate | PASS | existing legacy valid/adversarial fixtures |
| new/legacy snapshot metadata 混合 | BLOCKED | explicit shape rejection |
| `Last Confirmed` stale / `Previous Source` missing | BLOCKED | resolver freshness tests |
| Feature 写 `unconfirmed` review evidence | BLOCKED | exact review-state test |
| draft + 紧急 + 人类要求绕过 Product Review | BLOCKED | runtime non-bypass + Scenario 66C |
| Brief 塞入 Standard-only section | BLOCKED | three section mutations + model-view mutation |
| Human Grill 输出回写旧 `requirement.md` / Feature `product.md` | BLOCKED | ownership focused contract |
| Product Hub/Board/Workbench、`complex`、`RULE-*` 回流 | BLOCKED / absent | focused negative contract + scope audit |
| Delivery Contract/TDD/Submit 等既有 Gate | PASS | full Shell/Python regression，无放宽 |
| 普通 Chat 不创建 workflow artifact | PASS | full chat/requirements entry contracts |

## 8. Proposal 1–20 符合性

| Proposal 范围 | 结果 | 实现/证据 |
|---|---|---|
| 1–3 方向、现状与目标 | verified | Requirement `product.md` 唯一新产品 owner；`brief | standard` |
| 4 核心设计原则 | verified | adaptive depth、evidence-first、人类确认、无平行 PRD owner |
| 5 非目标 | verified | 无 Hub/Board/Workbench、complex、RULE、schema、stage/intent/lifecycle |
| 6 流程 | verified | Requirements Discussion → Product Review → Record → ADR/Feature Product Slice |
| 7 Artifact ownership | verified | README/source/product/follow-up/spec/ADR ownership 与 reader-first 兼容 |
| 8 Brief | verified | 九核心 section，无模型占位，可直接 handoff Product Slice |
| 9 Standard | verified | applicability + 按需 concepts/models/rules，无空表膨胀 |
| 10 Product Completeness/Human Grill/visuals | verified | one blocker、结构 checker 不冒充语义、人类确认派生图 |
| 11 Feature Product Brief 收敛 | verified | 新 Feature 不写 product；legacy reader 保留 |
| 12 ADR handoff | verified | new/legacy Effective Snapshot、no-model Brief、coverage/drift gate |
| 13 helper adapters | verified | PRD/Archify 只提供方法，不接管 artifact/deploy |
| 14 legacy compatibility | verified | legacy Requirement/Feature product/decision gate 不迁移即可读取 |
| 15 TDD/validation | verified | 独立 RED、51 focused、14 affected、40 Shell、255 Python、2 Ruby |
| 16 docs/examples/version | verified | human docs/example/changelog 已同步；版本仍 1.5.0 |
| 17 implementation order | verified | reader-first 后 writer/workflow，评测 flow-back 再 RED→GREEN |
| 18 acceptance | verified | 所有条目有 focused/full/mechanical/semantic evidence |
| 19 risks | verified | 同名 source、Gate 混淆、legacy drift、helper/visual boundary 均有 stop/validator |
| 20 scope drift | verified | 无目标项目 `.agent-loop/`、外部安装、版本/Git/发布动作 |

## 9. 剩余风险与验证边界

- 自动 checker 只验证结构、引用、状态、freshness 和绑定；产品语义是否正确仍由 Product Human Review 判断；
- Windows 仅有 Python 3.10+ 标准库、BOM/CRLF 与 Windows-style path contract evidence，状态为 `macOS-verified / Windows-test-defined`；
- legacy ADR 同时允许两套完整 gate 字面是有意兼容；不允许混合条款，但长期可在独立版本迁移中再决定是否弃用旧字面；
- `Previous Source` 当前验证边界是 confined existing file + not current source；没有引入 executable history graph 或 schema，符合本 Proposal 范围。

以上均不是当前 Critical、High 或 Medium。

## 10. 工作区与授权边界

验证开始/修复前 HEAD 保持 `e07d50c2c2b0bf80ad22b579e3a476bb71218c06`。当前分支相对 `origin/alpha/v1.5.0` 为 `ahead 1`，属于进入本轮前已有 Git 状态，本轮没有创建 commit。

最终工作区审计到：tracked changed `53` 个，untracked path `85` 个，tracked diff `+1501/-1173`；其中包含完整获批实现、历史/既有报告与执行前明确保留的 `.tmp/`、`scripts/__pycache__/`、`tests/__pycache__/`。无 staged 文件。

本轮未执行：stage、commit、push、tag、PR、merge、release、publish、installed-skill sync、分支/worktree 创建或切换。

结论：停在最终 Human Review，等待维护者验收。
