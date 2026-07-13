# Agent Loop v1.3.0 ADR Technical Landing RED Baseline

日期：2026-07-13

分支：`alpha/v1.3.0`

审计对象：当前工作区；实施前只有人类提供的 approved proposal，未修改 runtime、design、ADR template 或 validator。

## 修复前仓库基线

在新增 focused contract 之前运行全部已有 `tests/*.sh`：

```text
BASELINE passed=31 failed=0
```

该基线证明现有仓库测试健康，但不证明 ADR 已实现 Requirement Model Technical Landing Trace。

## Focused Contract RED

新增：

```text
tests/validate-adr-requirement-model-technical-landing-trace.sh
```

先验证 Shell 语法，再执行：

```text
$ bash -n tests/validate-adr-requirement-model-technical-landing-trace.sh
$ bash tests/validate-adr-requirement-model-technical-landing-trace.sh
FAIL: SKILL.md missing required text: Effective Requirement Snapshot
```

判定：`RED`，且失败原因正确。当前发布入口只说明 ADR 消费 accepted product semantics，尚未要求固定 effective source snapshot、模型行到技术落点的逐项 coverage、compatibility review 或相应 Human Review Summary。

## RED 覆盖的实际漏洞

- ADR 可以只链接 requirement set，但没有固定 README 当前 effective source/status。
- `Domain Concepts` 只保护 Concept 引用，不证明 scope 内 `REL-*` / `CMD-*` / `EVT-*` / `FLOW-*` / `STATE-*` / `PM-*` 已落地。
- `Applicable Decisions` 和既有 Design Slice Coverage 无法单独证明 Requirement Model 没有遗漏。
- effective source 变化后，accepted ADR 可能被新 Feature 继续使用，而没有进入 `review-required`。
- 既有 Human Review Summary 没有展示 coverage 计数、产品语义保留、operational trigger 和未分配 Design Slice。
- Migration / Compatibility / Rollout / Rollback 容易被模板默认展开，尚无按需触发的统一判断。

## GREEN 必须证明

- effective README pointer、source status 和 ADR snapshot 一致；
- `candidate` / `reopened` / `review-required` 会阻止 ADR acceptance 和依赖工作；
- scope 内每个 accepted Requirement Model ID 都有合法 disposition；
- `landed` 行具有非空 Technical Landing、Preserved Invariant、Design Slice 和 Verification；
- accepted ADR 不得重新定义产品语义，不兼容时创建 superseding ADR；
- template 和 validator 只依赖通用字段、ID 与结构，不固化 fixture 业务名词、动作或技术落点；
- 不新增 canonical stage、默认 mapping artifact、ADR lifecycle status 或 executable schema。
