# Agent Loop v1.5.0 Adaptive Requirement Product Definition RED Baseline

日期：2026-07-22
分支：`alpha/v1.5.0`
基线 HEAD：`e07d50c2c2b0bf80ad22b579e3a476bb71218c06`
审计对象：当前工作区，Proposal / Implementation Plan 已获人类批准；production/runtime 尚未修改
状态：RED 已建立并由 reader-first GREEN、workflow GREEN 与 mutation pressure 关闭

## 执行前全量基线

执行命令：

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
```

实际结果：

- Shell：`39/39` 通过；
- Python：`Ran 221 tests in 69.543s`，`OK`；
- 结论：实施前仓库基线为 GREEN，新 RED 不是既有测试失败。

执行前实时 inventory：Shell `39`，Python 文件 `16`，Ruby `2`。

## Focused RED 1：跨文件 ownership / routing contract

执行命令：

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
```

实际结果：exit `1`。

首个失败：

```text
FAIL: references/runtime.md missing: Product Definition Profile: `brief | standard`
```

该失败证明当前 runtime 尚未声明只有 `brief | standard` 两档 Requirement Product Definition，也尚未协调 Requirement `product.md` ownership、Feature Product Slice、PRD helper、Archify 和 legacy reader surfaces。

## Focused RED 2：新 Requirement Product Definition checker

执行命令：

```bash
python3 -m unittest tests/test_requirement_product_definition.py
```

实际结果：exit `1`，`Ran 10 tests`，`FAILED (failures=10)`。

共同失败根因：

```text
can't open file '.../scripts/check-requirement-product-definition.py': [Errno 2] No such file or directory
```

该失败证明当前仓库没有能够解析 `Effective Product Definition`、验证 Brief/Standard、Human Review、Product View Applicability、Product Slice、BOM/CRLF/Windows-style reference 和 derived visual freshness 的 checker。

## RED 覆盖

当前 focused tests 已固定以下缺口：

1. confirmed Brief 在不伪造模型表时应通过；
2. confirmed Standard 只对适用视图建模时应通过；
3. `complex` Profile 必须拒绝；
4. 未确认 Product Review 必须阻止 downstream；
5. 新旧 effective pointers 并存必须 fail closed；
6. `included` view 缺 section / ID 必须拒绝；
7. `not-applicable` 缺具体理由必须拒绝；
8. Product Slice 未知 source ID 必须拒绝；
9. stale derived visual digest 必须拒绝；
10. UTF-8 BOM、CRLF 和 Windows-style relative source reference 必须支持。

## 边界说明

- RED fixture 位于 `tests/fixtures/adaptive-product-definition/`，未在源码仓库根目录创建目标项目 `.agent-loop/`；
- 尚未修改 runtime/design/templates/checker production code；
- 未触碰执行前 `.tmp/`、旧报告和既有 `__pycache__/`；
- 未 commit、push、tag、release 或同步 installed Skill。

## GREEN / Mutation Closure

### Reader-first / downstream GREEN

执行：

```bash
python3 -m unittest tests/test_requirement_product_definition.py
python3 -m unittest tests/test_concept_foundation_trace.py
python3 -m unittest tests/test_adr_requirement_model_trace.py
```

实际结果分别为 `19/19`、`8/8`、`17/17` 通过。随后合并运行 focused Python 集合为 `Ran 44 tests`，`OK`。

真实集成链路：

```text
Requirement README + product.md -> Feature spec Product Slice = PASS
Requirement README + product.md -> ADR Product Rule / model landing = PASS（11 个引用）
legacy requirement.md + Feature product.md + spec.md = PASS（5 concepts / 26 models）
legacy ADR fixture = PASS（8 个引用）
```

### Writer / workflow / affected GREEN

`tests/validate-adaptive-requirement-product-definition.sh` 通过。计划列出的 13 个 affected Shell contracts 全部通过，覆盖 Chat/Requirements entry、Requirement lifecycle、Human Grill、Concept/Product Model、Decision/ADR、legacy Product Brief、root guidance 与旧人类文档回归。

### Mutation pressure

以下十个独立 mutation 都被拒绝：

| Mutation | 实际拦截证据 |
|---|---|
| `brief -> complex` | `unsupported Product Definition Profile: complex` |
| Product Review `confirmed -> pending` | `Product Review must be confirmed` |
| 删除一个 Product View Applicability row | `Product View Applicability mismatch` |
| `included -> not-applicable` 且理由为 `n/a` | `not-applicable view requires a concrete reason` |
| 删除 effective pointer | `missing effective product source pointer` |
| 新旧 pointers 并存 | `multiple effective product source pointers` |
| Product Slice 引用未知 `STATE-*` | `Product Slice contains unknown source IDs` |
| visual digest 改动 | `derived visual digest is stale` |
| 删除 Human Grill 单阻塞问题规则 | Shell RED：`references/product-definition.md missing: 一次只向人类确认一个阻塞问题` |
| 恢复旧 Feature Product Brief writer route | Shell RED：`references/runtime.md contains forbidden text: → Product Brief if Needed` |

所有 mutation 位于 unittest 临时目录或独立临时 source 副本。恢复后 focused Shell 与 `44/44` Python 再次通过，源码工作区无 mutation 残留。
