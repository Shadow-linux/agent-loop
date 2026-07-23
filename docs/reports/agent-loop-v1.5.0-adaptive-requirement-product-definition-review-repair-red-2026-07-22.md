# Agent Loop v1.5.0 Adaptive Requirement Product Definition 评测回流 RED 证据

日期：2026-07-22
分支：`alpha/v1.5.0`
基线 HEAD：`e07d50c2c2b0bf80ad22b579e3a476bb71218c06`
输入评测：`docs/reports/adaptive-requirement-product-definition-feature-validation-2026-07-22.md`
状态：RED 已建立并由评测回流 GREEN 与全量验证关闭

## 修复前 focused 基线

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
python3 -m unittest -v \
  tests.test_requirement_product_definition \
  tests.test_concept_foundation_trace \
  tests.test_adr_requirement_model_trace
```

结果：

- Shell contract：通过；
- Python：`Ran 44 tests in 3.044s`，`OK`；
- 说明：既有 focused suite 为 GREEN，但未覆盖独立评测识别出的跨文件缺口。

## 新增评测回流契约后的真实 RED

```bash
python3 -m unittest -v \
  tests.test_requirement_product_definition \
  tests.test_adr_requirement_model_trace
```

结果：exit `1`，`Ran 42 tests in 2.684s`，`FAILED (failures=8)`。

八个失败点：

1. README `Last Confirmed` 未与 Product Human Review `Confirmed At` 对齐；
2. Brief 可带入 `Product Capability Scope` 而未被识别为 Standard 膨胀；
3. Brief 可带入 `User Segments / Roles / Scenarios` 而未被识别为 Standard 膨胀；
4. Brief 可带入 `Experience / Operations / Measurement` 而未被识别为 Standard 膨胀；
5. Feature `Product Review Evidence: unconfirmed ...` 因子串匹配被错误接受；
6. legacy accepted source 使用当前统一 `templates/decision.md` Coverage Gate 时被拒绝；
7. confirmed Brief 的 reasoned `Trace Applicability: not-applicable` 被 ADR checker 强制改成 `required`；
8. 新 Product Definition snapshot 混入 legacy Concept Foundation metadata 未被拒绝。

Shell coordinated contract：

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
```

结果：exit `1`，首个失败为：

```text
FAIL: references/runtime.md missing: Product Human Review confirmation cannot be bypassed for a new Effective Product Definition.
```

该 RED 证明 runtime/design 尚未把新 Effective Product Definition 的 Product Human Review 写入不可绕过控制面；同一 focused contract 还约束 Requirement `product.md` ownership、Scenario 65、record-date、Usage 和 examples/package map 修复。

## RED 边界

- 只新增 tests 与本报告，未先修改 production checker、runtime 或 design；
- 未创建目标项目 `.agent-loop/`；
- 未改变 `brief | standard`、Requirement `product.md` ownership、ADR 产品/技术边界或版本；
- 未执行 stage、commit、push、tag、PR、merge、release、publish 或 installed-skill sync。

## GREEN 关闭

- focused Python：`51/51 PASS`；
- affected Shell：`14/14 PASS`；
- all Shell：`40/40 PASS`；
- all Python：`255/255 PASS`；
- 完整结果见 `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-22.1.md`。
