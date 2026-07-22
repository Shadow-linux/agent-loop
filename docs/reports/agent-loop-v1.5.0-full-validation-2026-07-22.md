# Agent Loop v1.5.0 Adaptive Requirement Product Definition 全量验证报告

> 历史报告：独立单功能评测随后发现本报告未覆盖的 4 High / 2 Medium；这些问题已通过 flow-back RED/GREEN 修复。当前验收请使用 `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-22.1.md`，本文件保留原始实施验证证据。

日期：2026-07-22
分支：`alpha/v1.5.0`
基线 HEAD：`e07d50c2c2b0bf80ad22b579e3a476bb71218c06`
Skill version：`1.5.0`
审计对象：基线 HEAD 加当前未提交的 Adaptive Requirement Product Definition 实施工作区
结论：`STRONG`，`100/100`；当前 Critical `0`、High `0`、Medium `0`

## 1. 范围与 dirty-work 边界

本轮按以下已批准设计与计划实施：

- `docs/proposal/v1.5.x/adaptive-requirement-product-definition.md`
- `docs/proposal/v1.5.x/adaptive-requirement-product-definition-implementation-plan.md`

实施前已存在且不归本功能所有的未跟踪路径保持原样：

- `.tmp/`
- `docs/reports/agent-loop-1.5.0-full-validation-2026-07-21.md`
- `scripts/__pycache__/`
- `tests/__pycache__/`

未创建目标项目根 `.agent-loop/`，未创建或切换分支/worktree，未派发 Subagent，未同步 installed Skill，未执行 stage、commit、push、tag、PR、merge、release、publish。

## 2. RED 基线

实施前全量基线：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
```

- Shell：`39/39 PASS`
- Python：`Ran 221 tests in 69.543s`，`OK`

随后建立真实 focused RED：

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
python3 -m unittest tests/test_requirement_product_definition.py
```

实际结果：

- Shell exit `1`：`FAIL: references/runtime.md missing: Product Definition Profile: \`brief | standard\``；
- Python exit `1`：`Ran 10 tests`，`FAILED (failures=10)`；共同根因为 `scripts/check-requirement-product-definition.py` 尚不存在。

完整 RED 证据见：`docs/reports/agent-loop-v1.5.0-adaptive-requirement-product-definition-red-baseline-2026-07-22.md`。

## 3. GREEN 与 focused validation

### 3.1 Reader-first 双兼容

共享 reader 与 checker 先于 writer 路由切换完成：

- 新格式：README `Effective Product Definition` -> confirmed Requirement `product.md`；
- legacy：README `Effective Concept Foundation` / reviewed `requirement.md` 与既有 Feature `product.md`；
- 新旧 pointer 并存、缺失、越界、路径不一致、未确认或未知 source 均 fail closed；
- UTF-8 BOM、CRLF 与 Windows-style relative reference 有测试覆盖；
- 旧 reader/fixture 不要求批量迁移。

真实链路结果：

| 链路 | 结果 |
|---|---|
| Requirement README + `product.md` -> Feature `spec.md` Product Slice | PASS |
| Requirement README + `product.md` -> ADR product model/rule landing | PASS，`11` 个引用完成落地核对 |
| legacy `requirement.md` + Feature `product.md` + `spec.md` | PASS，`5` concepts / `26` models |
| legacy ADR fixture | PASS，`8` 个引用 |

### 3.2 Focused tests

```bash
python3 -m unittest -v \
  tests.test_requirement_product_definition \
  tests.test_concept_foundation_trace \
  tests.test_adr_requirement_model_trace
```

结果：`Ran 44 tests in 2.621s`，`OK`。

其中：

- Requirement Product Definition：`19/19 PASS`；
- Concept Foundation trace：`8/8 PASS`；
- ADR Requirement Model trace：`17/17 PASS`；
- 计划指定的 affected Shell contracts：`13/13 PASS`；
- focused ownership/routing contract：PASS。

### 3.3 Mutation pressure

以下 `10/10` mutation 均被预期拒绝，恢复后 focused Shell 与 Python `44/44` 再次通过：

| Mutation | 拦截结果 |
|---|---|
| `brief -> complex` | unsupported Profile |
| Product Review `confirmed -> pending` | downstream blocked |
| 删除 applicability row | coverage mismatch |
| `not-applicable: n/a` | concrete reason required |
| 删除 effective pointer | missing pointer |
| 新旧 pointers 并存 | multiple pointers |
| Product Slice 未知 `STATE-*` | unknown source ID |
| visual digest 改一位 | stale derived visual |
| 删除 one-blocker 规则 | focused Shell RED |
| 恢复 Feature Product Brief writer route | focused Shell RED |

## 4. 全量可执行回归

### 4.1 Shell

```bash
shell_total=$(find tests -maxdepth 1 -type f -name '*.sh' | wc -l | tr -d ' ')
for test_file in tests/*.sh; do bash "$test_file"; done
```

实时库存与结果：`40/40 PASS`。

### 4.2 Python

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

最终 fresh 结果：`Ran 246 tests in 58.009s`，`OK`。

第一次全量 GREEN 运行暴露 `tests/test_python_checker_contract.py` 尚未登记新 checker/support，修复 import allowlist 并补齐 CHANGELOG canonical path 后重新执行；本报告只把上述 fresh `246/246` 作为最终结果，不沿用失败运行。

### 4.3 Ruby 与语法

```bash
for test_file in tests/*.rb; do ruby "$test_file"; done
find . -name '*.sh' -type f -not -path './.git/*' -print0 | xargs -0 -n1 bash -n
find scripts tests -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
```

- Ruby adversarial tests：`2/2 PASS`；
- Shell syntax：PASS；
- Python `py_compile`：PASS。

## 5. 机械检查

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md"); YAML.load_file("agents/openai.yaml")'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
# 全仓 Markdown fence balance scan
git diff --check
```

| 检查 | 结果 |
|---|---|
| `SKILL.md` + `agents/openai.yaml` YAML | `2/2 PASS` |
| `plugin.json` JSON | PASS |
| Markdown fence balance | `259/259 PASS` |
| `git diff --check` | PASS |
| Skill version | `1.5.0`，未升级 |
| root managed blocks | `13/13` 为 `1.5.0-20260721.2`，未修改 revision |
| 根 `.agent-loop/` | 不存在 |
| `__pycache__` | 仅保留执行前已记录的 `scripts/`、`tests/` 路径 |

## 6. 六域语义审计

| 审计域 | 权重 | 结果 | 得分 | 关键证据 |
|---|---:|---|---:|---|
| Logic Correctness | 20 | PASS | 100 | intent precedence、Brief/Standard depth、one-blocker、唯一 effective pointer、Product Review/Gate 解耦与 stop rules 一致 |
| Autonomy | 15 | PASS | 100 | Agent 先查证据、推荐 Profile/定义、一次询问一个阻塞问题；helper/Archify 不可用有本地 fallback |
| Project Entry / Evidence Graph + DDD Onboarding | 15 | PASS | 100 | Project Entry 只路由到 Product Definition/ADR/Product Slice；onboarding 不复制产品 authority；legacy/stale memory 继续 fail closed |
| Development / Test Workflow | 20 | PASS | 100 | Product Slice/ADR gate、TDD、Verify/Review/Drift/Memory/Completion 顺序及 Submit 独立 Gate 保留 |
| Memory | 15 | PASS | 100 | Requirement README 只索引 current source/lifecycle；human originals byte-stable；append-only follow-up 与 legacy reader 保留 |
| Recommendation | 15 | PASS | 100 | 普通 Chat answer-only；Requirements Discussion、Design Readiness、Feature Spec 的单一推荐下一阶段与 blocker 规则可达 |

加权总分：`100/100`，等级 `STRONG`。

当前发现：

| Severity | 数量 | 结论 |
|---|---:|---|
| Critical | 0 | 无 Gate 绕过或不可预测主流程 |
| High | 0 | 无路由、状态或 memory 冲突 |
| Medium | 0 | 无跨文件遗漏或可绕过迁移缺口 |

## 7. 语义压力矩阵

| 场景 | 预期/实测路由 | 结果 |
|---|---|---|
| Chat | answer-only，不创建 Requirement artifact | PASS |
| 简单且边界清楚的 Requirements Discussion | Agent 起草 Brief `product.md`，仍需 Product Human Review/Record Gate | PASS |
| 有复杂信号的 Requirements Discussion | Standard + applicability/completeness，禁止 `complex` | PASS |
| Standard 语义阻塞 | evidence -> candidate -> recommendation -> 每轮一个 blocker | PASS |
| confirmed `product.md` -> ADR | dual reader snapshot、model/rule coverage、upstream compatibility | PASS |
| confirmed `product.md` -> Feature | `spec.md` Product Slice，不创建 Feature `product.md` | PASS |
| legacy Requirement -> ADR/Spec | legacy pointer/source 可读，不迁移 | PASS |
| legacy Feature `product.md` -> Resume/Close | 只读兼容；冲突进入 Requirement Conflict/Recovery | PASS |
| Product follow-up | append-only follow-up + README pointer；ADR/Feature 重新做 drift/compatibility | PASS |
| Archify unavailable | Markdown/table/Mermaid/no visual fallback，不永久阻塞 Product Review | PASS |
| Product Review confirmed | 不隐式授权 Requirement lifecycle、ADR、Feature、code 或 Git | PASS |
| Delivery/Task/Completion/Submit | 既有 Human Gates、TDD、fresh evidence、Review/Drift/Memory 顺序不变 | PASS |

## 8. Proposal 1–20 符合性

| Proposal section | 状态 | 实施与验证证据 |
|---:|---|---|
| 1 已确认方向 | verified | `references/product-definition.md`、Requirement template、Product Slice 与双 reader |
| 2 最高原则 | verified | source ownership、Product Review、ADR/Feature non-redefinition rules |
| 3 问题定义 | verified | 移除新 Feature Product Brief writer，PRD helper 改落 Requirement |
| 4 目标 | verified | runtime/design/reference/template/docs/tests coordinated change |
| 5 非目标 | verified | 无 Hub/Board/Workbench、stage/status/schema/外部安装 |
| 6 推荐运行模型 | verified | `brief | standard` depth scan、升级规则与 runtime flow |
| 7 Requirement Set contract | verified | `templates/product.md`、`templates/requirement-set-README.md`、append-only/source preservation |
| 8 Human Grill/Product Model | verified | `references/product-definition.md`、grill/checklists、one-blocker mutation |
| 9 PRD Helper Adapter | verified | external adapter/skill routing；禁止 native output/deploy |
| 10 Archify | verified | Human-confirmed scope、source IDs、semantic digest、freshness/fallback |
| 11 Feature Product Brief 收敛 | verified | legacy-only reference + Feature Spec Product Slice + regressions |
| 12 ADR 下游追踪 | verified | dual-reader Effective Requirement Snapshot 与 Product Rule anchors |
| 13 Human Gates/stop rules | verified | Product Review/lifecycle/Feature/ADR/Git 分离，pending/stale/conflict fail closed |
| 14 影响面 | verified | runtime/design/references/templates/root/human docs/examples/scripts/tests 已同步 |
| 15 TDD/focused contract | verified | 独立 RED 报告、44 focused Python、affected Shell 与 mutations |
| 16 压力场景 | verified | fixtures、validation scenarios、本报告压力矩阵 |
| 17 实施顺序 | verified | reader-first 后 writer/routing，Task 0–10 顺序执行 |
| 18 验收标准 | verified | 验收条目均由 focused/full/mechanical/semantic evidence 覆盖 |
| 19 风险与缓解 | verified | 双路径消歧、review separation、slice、applicability、digest、legacy reader |
| 20 范围漂移 | verified | 无批准外 capability/version/revision/dependency/Git/installed-skill 动作 |

## 9. 剩余风险与边界

1. 当前为 `macOS-verified / Windows-test-defined`：macOS 完成全部可执行验证；Windows 通过 Python 3.10+ 标准库、BOM/CRLF、Windows-style path 与 checker import contract 定义，未取得原生 Windows 实跑证据。
2. checker 只验证结构、摘要、引用、稳定 ID、Product Slice/ADR 绑定和 visual freshness，不能证明产品语义本身正确；Product Human Review 与 Human Grill 因此仍是硬边界。
3. Product Rules 本版使用 `product.md#<anchor>` 而非稳定 `RULE-*`。anchor 变更必须进入 compatibility/drift；是否引入稳定规则 ID 需另立 Proposal。
4. 外部 PRD helper 与 Archify 没有在本轮安装、同步或调用；只验证了 Agent Loop adapter contract 与本地 fallback。

以上均为 Proposal 已声明边界，不构成当前 Critical/High/Medium 缺陷。

## 10. 范围漂移与发布判断

- Product Definition 只有 `brief | standard`；
- 未恢复 Product Design Hub、Product Review Board、Workbench 或 HTML questionnaire；
- 未新增 canonical stage、message intent、Product lifecycle、`RULE-*` 或 executable schema；
- 未改变 ADR 技术落地职责；
- 未升级 Skill version 或 root managed-block revision；
- 未修改 human original source；
- 未在源码仓库创建目标项目 `.agent-loop/`；
- 未执行 commit、push、tag、PR、merge、release、publish 或 installed-skill sync。

当前实现与验证可以进入最终 Human Review。`STRONG` 是逻辑与回归结论，不是发布授权；正式提交和发布仍等待维护者另行确认。
