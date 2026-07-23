# Adaptive Requirement Product Definition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Do not dispatch subagents unless the human separately authorizes them. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace new Feature-level Product Brief authoring with one adaptive `brief | standard` Requirement `product.md`, preserve original human sources, retain legacy readers, and hand confirmed Product Slices directly to ADR and Feature Spec.

**Architecture:** Implement reader compatibility before changing writers. A new standard-library support module resolves either the new README `Effective Product Definition` pointer or the legacy `Effective Concept Foundation` pointer, exposes one normalized product source model, and is consumed by focused product, ADR, and Feature trace validators. Runtime/design then move PRD synthesis into Requirements Discussion, keep Concept Foundation/Product Model/Completeness/Archify as internal methods, and make Feature `spec.md` the only new downstream Product Slice artifact.

**Tech Stack:** Markdown contracts and templates, Bash contract tests, Python 3.10+ standard library validators and `unittest`, Ruby mechanical/adversarial tests, Mermaid/Archify-derived HTML metadata, Git read-only inspection.

---

状态：Task 0–11 已执行；独立评测回流 RED/GREEN 与 full validation 已完成，等待最终 Human Review
设计来源：`docs/proposal/v1.5.x/adaptive-requirement-product-definition.md`
目标分支：`alpha/v1.5.0`
计划基线 HEAD：`e07d50c2c2b0bf80ad22b579e3a476bb71218c06`
目标版本：v1.5.0；不得升级版本
计划创建时间：2026-07-22

## 实施约束

- 这是 Agent Loop Skill 源仓库，不在仓库根目录创建目标项目 `.agent-loop/`。
- 保留当前无关 dirty/untracked 内容，尤其是 `.tmp/`、现有验证报告和 `__pycache__/`；不得恢复、删除、暂存或提交它们。
- Proposal 已获人类方向批准；执行本计划仍需独立 Human Review 确认。
- 严格按 Task 0–11 顺序执行：baseline → RED → reader GREEN → writer/workflow GREEN → focused → full validation。
- 不改变 Proposal 的 `brief | standard`、Requirement `product.md` ownership、legacy compatibility、Human Grill、ADR 和 Feature Slice 语义。
- 不引入 `complex` Profile、`RULE-*`、Product Hub/Board/Workbench、canonical stage、message intent、lifecycle 或 executable schema。
- 不安装或同步 `prd-writer`、Archify、Agent Loop 或其他 installed Skill。
- 不创建/切换分支或 worktree，不派发 Subagent。
- 不执行 stage、commit、push、tag、PR、merge、release、publish。
- Python 使用 3.10+ 标准库；macOS 本机执行，Windows 通过 BOM/CRLF、路径和纯标准库契约定义。没有原生 Windows 证据时报告 `macOS-verified / Windows-test-defined`。

## 文件职责与目标结构

### 新文件

| 文件 | 单一职责 |
|---|---|
| `references/product-definition.md` | Brief/Standard Profile、Product Completeness、Human Review、PRD helper 和 Archify 派生视图的详细运行规则 |
| `scripts/requirement_product_support.py` | 新旧 Effective Product Source 解析、Profile/review/ID inventory、semantic digest 与路径约束 |
| `scripts/check-requirement-product-definition.py` | 结构、适用性、来源、review、Product Slice 和 visual freshness 的只读 validator |
| `tests/test_requirement_product_definition.py` | resolver/checker 的正反例、BOM/CRLF、Windows-style reference 与 mutation 单元测试 |
| `tests/validate-adaptive-requirement-product-definition.sh` | runtime/design/reference/template/docs 的 focused coordinated contract |
| `tests/fixtures/adaptive-product-definition/` | Brief、Standard、新 ADR handoff、无效双源/未评审/stale visual fixtures |
| `examples/adaptive-product-definition/` | 人类可读的新 Requirement `product.md` → Feature `spec.md` 示例 |
| `docs/reports/agent-loop-v1.5.0-adaptive-requirement-product-definition-red-baseline-2026-07-22.md` | 真实 RED 证据 |
| `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-22.md` | 实施后的中文 full-validation 证据；若路径已存在则停止，不覆盖 |

### 修改文件族

| 文件族 | 目标职责 |
|---|---|
| `SKILL.md`, `references/runtime.md`, `references/design.md`, `references/concepts.md` | 新 ownership、两档 Profile、移除新 Product Brief 写入 stage、保持 stage/gate invariants |
| `references/requirement-management.md`, `references/requirement-product-grill.md` | Requirement `product.md`、source preservation、one-blocker、append-only follow-up |
| `references/product-brief.md` | 仅保留 legacy Feature Product Brief compatibility；禁止新写入 |
| `references/project-decisions.md`, `templates/decision.md` | 新 Effective Product Definition 与 legacy Effective Concept Source 双 reader |
| `references/stage-guides.md`, `references/workflow-checklists.md`, `references/human-review-summary.md` | Requirements Discussion 内 PRD synthesis、Product Review、Product Slice handoff |
| `references/artifact-rules.md`, `references/document-templates.md`, `references/project-guidance.md` | 新 artifact authority、inline template、root refresh 行为 |
| `references/skill-routing.md`, `references/external-skill-adapters.md` | PRD helper 落到 Requirement `product.md`，禁用 native/部署输出 |
| `templates/product.md`, `templates/requirement-set-README.md`, `templates/spec.md`, `templates/root-AGENTS.md` | 新 Requirement PRD template、pointer、Feature Slice、first-hop guidance |
| `scripts/check-concept-foundation-trace.py`, `scripts/check-adr-requirement-model-trace.py` | 调用 shared reader；新格式 + legacy format 均可验证 |
| `tests/test_concept_foundation_trace.py`, `tests/test_adr_requirement_model_trace.py` | 新路径集成与 legacy non-regression |
| affected `tests/validate-*.sh` | coordinated workflow contract 从 Feature Product Brief 更新为 Requirement Product Definition |
| `references/validation-scenarios.md`, `README.md`, `Usage.md`, `CHANGELOG.md` | 人类可见行为、压力场景和版本内变更 |

### 删除/停写策略

- 不删除 `references/product-brief.md`、旧 examples 或 fixtures；把它们明确降为 legacy reader contract。
- 不删除旧 Feature `product.md`；新 writer 不再创建。
- 不删除旧 `requirement.md`；新 Requirement writer 使用 `product.md`。
- 不保留两份 runtime `templates/product.md`；该模板切换为 Requirement Product Definition。Legacy Feature Product Brief 只由现有 artifact/fixture 验证，不再拥有写入模板。

## Task 0: Baseline、dirty ownership 与执行前停点

**Files:**
- Read: `AGENTS.md`
- Read: `SKILL.md`
- Read: `references/runtime.md`
- Read: `references/design.md`
- Read: `docs/proposal/v1.5.x/adaptive-requirement-product-definition.md`
- Read: `docs/proposal/v1.5.x/adaptive-requirement-product-definition-implementation-plan.md`
- Read: `docs/maintenance/full-validation-method.md`
- Modify after checks only: `docs/proposal/v1.5.x/adaptive-requirement-product-definition.md`
- Modify after checks only: `docs/proposal/v1.5.x/adaptive-requirement-product-definition-implementation-plan.md`

- [x] **Step 1: Capture exact branch, HEAD and dirty work**

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git diff --name-status
git ls-files --others --exclude-standard
```

Expected:

```text
branch = alpha/v1.5.0
HEAD equals `e07d50c2c2b0bf80ad22b579e3a476bb71218c06`, or the execution notes record one human-explained later full SHA before any write
Proposal and Plan are untracked/modified as expected
all other dirty paths have an identified owner and do not overlap this plan
```

Stop if branch changed, HEAD moved without explainable human work, a target file has unrelated modifications, or an untracked path would be overwritten.

- [x] **Step 2: Read all required authority files completely**

Run:

```bash
cat AGENTS.md
cat SKILL.md
cat references/runtime.md
cat references/design.md
cat docs/proposal/v1.5.x/adaptive-requirement-product-definition.md
cat docs/proposal/v1.5.x/adaptive-requirement-product-definition-implementation-plan.md
cat docs/maintenance/full-validation-method.md
```

Expected: all files exist and no current authority contradicts the approved Proposal. Stop with exact lines if a contradiction changes product ownership, Human Grill, ADR, or Feature Slice semantics.

- [x] **Step 3: Record live test inventory**

Run:

```bash
find tests -maxdepth 1 -type f -name '*.sh' | sort
find tests -maxdepth 1 -type f -name 'test_*.py' | sort
find tests -maxdepth 1 -type f -name '*.rb' | sort
```

Record the actual Shell/Python/Ruby counts in execution notes. Do not reuse a historical report count.

- [x] **Step 4: Run the pre-change full executable baseline**

Run:

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
```

Expected: exit 0 for every existing test. If the baseline is red, stop and report whether the failure is pre-existing, dirty-work-related, or Proposal-related; do not edit runtime to hide it.

- [x] **Step 5: Mark documents as approved/implementation-started only after the baseline is green**

Change the Proposal status to:

```text
状态：已获人类批准，实施中；未 commit / push / tag / release / installed-skill sync
```

Change this plan status to:

```text
状态：已获人类批准，按 Task 0–11 实施中
```

Expected: no runtime file changed in Task 0.

## Task 1: Focused RED contract 与 RED report

**Files:**
- Create: `tests/validate-adaptive-requirement-product-definition.sh`
- Create: `tests/test_requirement_product_definition.py`
- Create: `tests/fixtures/adaptive-product-definition/brief-valid/README.md`
- Create: `tests/fixtures/adaptive-product-definition/brief-valid/product.md`
- Create: `tests/fixtures/adaptive-product-definition/standard-valid/README.md`
- Create: `tests/fixtures/adaptive-product-definition/standard-valid/product.md`
- Create: `tests/fixtures/adaptive-product-definition/standard-valid/spec.md`
- Create: `tests/fixtures/adaptive-product-definition/standard-invalid-unreviewed/`
- Create: `tests/fixtures/adaptive-product-definition/standard-invalid-dual-source/`
- Create: `tests/fixtures/adaptive-product-definition/standard-invalid-stale-visual/`
- Create: `docs/reports/agent-loop-v1.5.0-adaptive-requirement-product-definition-red-baseline-2026-07-22.md`

- [x] **Step 1: Write the shell RED assertions**

Start the focused contract with concrete ownership failures:

```bash
#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)

assert_contains() {
  local file=$1 text=$2
  grep -Fq -- "$text" "$root/$file" || {
    printf 'FAIL: %s missing: %s\n' "$file" "$text" >&2
    exit 1
  }
}

assert_not_contains() {
  local file=$1 text=$2
  if grep -Fq -- "$text" "$root/$file"; then
    printf 'FAIL: %s contains forbidden text: %s\n' "$file" "$text" >&2
    exit 1
  fi
}

assert_contains "references/runtime.md" 'Product Definition Profile: `brief | standard`'
assert_contains "references/artifact-rules.md" '`requirements/<record-date>-<topic>/product.md`'
assert_contains "references/product-definition.md" '# Adaptive Product Definition'
assert_contains "templates/product.md" 'Product Definition Profile: brief | standard'
assert_contains "templates/spec.md" '## Product Slice'
assert_not_contains "references/runtime.md" '→ Product Brief if Needed'
assert_not_contains "references/design.md" '`product.md` is optional feature-level product understanding'
assert_not_contains "references/product-definition.md" 'Product Definition Profile: complex'
```

Add assertions for source immutability, one-blocker Human Grill, Product Human Review non-authorization, PRD helper path, Archify scoped confirmation/fallback, legacy compatibility, ADR dual reader, no Product Hub/Board/Workbench, and no new Feature `product.md` writer.

- [x] **Step 2: Write new-format unit tests before checker code exists**

Use `tests/checker_test_support.py`. Implement this complete harness first:

```python
from __future__ import annotations

import unittest

from tests.checker_test_support import ROOT, combined_output, run_checker

SCRIPT = "scripts/check-requirement-product-definition.py"
FIXTURES = ROOT / "tests/fixtures/adaptive-product-definition"


class RequirementProductDefinitionTests(unittest.TestCase):
    def run_fixture(self, name: str, *, with_spec: bool = True):
        fixture = FIXTURES / name
        args = [str(fixture / "README.md"), str(fixture / "product.md")]
        if with_spec:
            args.append(str(fixture / "spec.md"))
        return run_checker(SCRIPT, *args)

    def test_confirmed_brief_passes_without_model_placeholders(self) -> None:
        result = self.run_fixture("brief-valid", with_spec=False)
        self.assertEqual(result.returncode, 0, combined_output(result))

    def test_confirmed_standard_passes_with_only_applicable_views(self) -> None:
        result = self.run_fixture("standard-valid")
        self.assertEqual(result.returncode, 0, combined_output(result))


if __name__ == "__main__":
    unittest.main()
```

Then add these exact mutation cases using temporary copies of `standard-valid`:

| Test name | Mutation / fixture | Expected diagnostic |
|---|---|---|
| `test_profile_complex_is_rejected` | `Product Definition Profile: complex` | `unsupported Product Definition Profile: complex` |
| `test_unreviewed_product_is_rejected_for_downstream_use` | fixture `standard-invalid-unreviewed` | `Product Review must be confirmed` |
| `test_new_and_legacy_effective_pointers_cannot_coexist` | fixture `standard-invalid-dual-source` | `multiple effective product source pointers` |
| `test_included_view_requires_section_and_ids` | remove included State section | `included view State is missing section` |
| `test_not_applicable_view_requires_concrete_reason` | set reason to `n/a` | `not-applicable view requires a concrete reason` |
| `test_product_slice_cannot_reference_unknown_model_id` | replace one Product Slice ref with `STATE-UNKNOWN` | `Product Slice contains unknown source IDs` |
| `test_stale_visual_digest_is_rejected` | fixture `standard-invalid-stale-visual` | `derived visual digest is stale` |
| `test_bom_crlf_and_windows_style_input_are_supported` | write copied input as UTF-8 BOM + CRLF and use Windows-style relative source evidence | exit 0 and standard PASS output |

The RED harness invokes the not-yet-created checker, so both complete valid-fixture tests must fail before production code exists.

- [x] **Step 3: Add realistic fixtures**

The Standard fixture must contain:

```markdown
Product Definition Profile: standard
Product Review: confirmed

## Product View Applicability

| View | Applicability | Reason / Evidence | Section / Stable IDs |
|---|---|---|---|
| Concepts | included | two actors and one state-bearing request need stable meaning | Concept Definitions / C-REQUEST / C-OPERATOR |
| Relationships | included | operator acts on one request | Concept Relationships / REL-OPERATOR-REQUEST |
| Permissions | included | only operator may approve | Role / Permission Matrix / PERM-APPROVE |
| Actions / Outcomes | included | submit and approve are observable product actions | Commands / Events / CMD-SUBMIT / CMD-APPROVE / EVT-APPROVED |
| Flow | included | request closes through submit and approve | Primary Business Flow / FLOW-SUBMIT / FLOW-APPROVE |
| State | included | request has pending and approved states | Product State Model / STATE-REQUEST |
| Product Facts | included | approval result and owner are durable facts | Requirement Product Model / PM-APPROVAL |
| Exceptions / Recovery | included | rejected approval remains observable | Exception Paths / EX-REJECTED |
| Product Rules | included | approval requires an authorized operator | Product Rules / rule-approval-authority |
```

The Brief fixture must contain no fake stable-ID tables and must still include Problem, User/Scenario, Outcome, Scope, Out of Scope, Acceptance Direction, Source Evidence, Open Questions/Risk, and Product Human Review Evidence.

- [x] **Step 4: Run RED and save exact evidence**

Run:

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
python3 -m unittest tests/test_requirement_product_definition.py
```

Expected RED:

```text
shell fails because references/product-definition.md and new ownership text do not exist
Python fails because scripts/check-requirement-product-definition.py does not exist
```

Record command, exit status, concise failure, branch, HEAD, and why each failure proves the current gap in the RED report. Do not weaken assertions after observing RED.

## Task 2: Shared effective-product reader（reader-first GREEN）

**Files:**
- Create: `scripts/requirement_product_support.py`
- Test: `tests/test_requirement_product_definition.py`
- Modify: `scripts/check-concept-foundation-trace.py`
- Modify: `scripts/check-adr-requirement-model-trace.py`
- Modify: `tests/test_concept_foundation_trace.py`
- Modify: `tests/test_adr_requirement_model_trace.py`

- [x] **Step 1: Add normalized source model and resolver tests**

Test these exact API contracts before implementation:

```python
source = resolve_effective_product_definition(readme_path, supplied_source_path)
self.assertEqual(source.kind, "product-definition")
self.assertEqual(source.profile, "standard")
self.assertEqual(source.review, "confirmed")
self.assertFalse(source.legacy)

legacy = resolve_effective_product_definition(legacy_readme, legacy_requirement)
self.assertTrue(legacy.legacy)
self.assertEqual(legacy.kind, "concept-foundation")
```

Reject: missing pointer, both pointers present, pointer path escape, supplied path mismatch, unsupported Profile, unconfirmed new source, stale/mismatched metadata, and unresolved legacy status.

- [x] **Step 2: Implement the shared dataclass and resolver**

Create this public interface:

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class EffectiveProductSource:
    path: Path
    content: str
    kind: str
    profile: str | None
    review: str
    legacy: bool
    concept_ids: frozenset[str]
    model_ids: frozenset[str]

def resolve_effective_product_definition(
    readme_path: Path,
    supplied_source_path: Path,
) -> EffectiveProductSource:
    """Resolve exactly one new or legacy reviewed product source."""
```

Implementation rules:

```text
new pointer: ## Effective Product Definition
  Source = supplied path
  Profile = brief | standard
  Product Review = confirmed

legacy pointer: ## Effective Concept Foundation
  Effective Source = supplied path
  Status = accepted | concept-foundation-not-needed

both present = fail closed
neither present = fail closed
all relative paths confined to Requirement Set directory
```

- [x] **Step 3: Implement adaptive model inventory**

Expose:

```python
def product_model_inventory(source: EffectiveProductSource) -> tuple[set[str], set[str]]:
    """Return accepted concept/model IDs; optional new views follow applicability."""

def product_semantic_sha256(content: str) -> str:
    """Hash semantic content excluding Derived Visuals and Human Review Evidence."""
```

Legacy inventory keeps the existing mandatory table behavior. New Standard inventory reads `Product View Applicability`: `included` requires its section and valid IDs; `not-applicable` requires a concrete reason and forbids placeholder rows. Brief returns no fabricated model IDs.

- [x] **Step 4: Make existing checkers consume the resolver without changing writer semantics yet**

Refactor duplicated patterns/constants from both checkers into the support module. Preserve current CLI positional arguments and legacy outputs. Add new-path unit tests but do not update runtime/templates in this task.

Expected commands:

```bash
python3 -m unittest tests/test_requirement_product_definition.py
python3 -m unittest tests/test_concept_foundation_trace.py
python3 -m unittest tests/test_adr_requirement_model_trace.py
```

Expected: resolver tests and all legacy checker tests pass. The Task 1 shell contract remains RED because writer/runtime surfaces have not changed.

## Task 3: Product Definition checker、Profile 与 visual freshness

**Files:**
- Create: `scripts/check-requirement-product-definition.py`
- Modify: `scripts/requirement_product_support.py`
- Modify: `tests/test_requirement_product_definition.py`
- Modify: `tests/fixtures/adaptive-product-definition/*`

- [x] **Step 1: Implement CLI and required argument behavior**

Use this CLI:

```text
python3 scripts/check-requirement-product-definition.py \
  <requirement-readme> <effective-product-source> [feature-spec]
```

`feature-spec` is optional for Product Human Review preflight and required for downstream Product Slice validation.

Skeleton:

```python
def validate(readme_path: Path, source_path: Path, spec_path: Path | None) -> str:
    source = resolve_effective_product_definition(readme_path, source_path)
    if source.legacy:
        return validate_legacy_product_source(source, spec_path)
    validate_product_profile(source)
    validate_human_review(source.content)
    validate_visual_manifest(source)
    if spec_path is not None:
        validate_product_slice(source, read_text(spec_path))
    return f"PASS: confirmed {source.profile} product definition is valid"
```

- [x] **Step 2: Validate Brief contract without model inflation**

Brief requires the nine sections from the Proposal. Reject Product View Applicability rows that declare complex included views while Profile is Brief; emit:

```text
brief product definition contains Standard-only product-model views
```

Do not reject a Brief merely because it contains no stable IDs.

- [x] **Step 3: Validate Standard applicability and stable references**

Use allowed view names exactly:

```python
VIEW_CONTRACTS = {
    "Concepts": ("Concept Definitions", CONCEPT_ID_PATTERN),
    "Relationships": ("Concept Relationships", REL_ID_PATTERN),
    "Permissions": ("Role / Permission Matrix", PERM_ID_PATTERN),
    "Actions / Outcomes": ("Commands / Events", ACTION_ID_PATTERN),
    "Flow": ("Primary Business Flow", FLOW_ID_PATTERN),
    "State": ("Product State Model", STATE_ID_PATTERN),
    "Product Facts": ("Requirement Product Model", PM_ID_PATTERN),
    "Exceptions / Recovery": ("Exception Paths", EX_ID_PATTERN),
    "Product Rules": ("Product Rules", None),
}
```

Require exactly one applicability row per view. Allowed applicability is `included | not-applicable`; these are coverage values, not lifecycle/status. Included rows need concrete evidence plus section/IDs; not-applicable rows need a concrete reason and must not point to fake IDs.

- [x] **Step 4: Validate Product Human Review Evidence**

Require:

```markdown
## Product Human Review Evidence

Decision: confirmed
Confirmed By: <human identity or human>
Confirmed At: YYYY-MM-DD
Evidence: <concrete review statement>
Implementation Authorized: no | separately-confirmed
```

`Implementation Authorized` remains evidence only; it does not create Feature or Git authorization. Reject missing/placeholder evidence and future-invalid dates.

- [x] **Step 5: Validate derived visual freshness**

When `## Derived Visuals` exists, parse:

```markdown
| Path | Type | Source IDs | Product Semantic SHA-256 | Status | Human Confirmed |
|---|---|---|---|---|---|
```

Require type `workflow | lifecycle | sequence | relationship | equivalent`, known source IDs, a 64-hex digest matching `product_semantic_sha256`, status `current`, and concrete Human Confirmed evidence. Missing Archify/visuals section remains valid.

- [x] **Step 6: Run focused Python GREEN**

Run:

```bash
python3 -m unittest tests/test_requirement_product_definition.py
python3 -m unittest tests/test_concept_foundation_trace.py
python3 -m unittest tests/test_adr_requirement_model_trace.py
```

Expected: all pass, including BOM/CRLF and stale digest mutations.

## Task 4: Requirement writer、templates 与 Human Review

**Files:**
- Create: `references/product-definition.md`
- Modify: `references/requirement-management.md`
- Modify: `references/requirement-product-grill.md`
- Modify: `references/human-review-summary.md`
- Modify: `references/artifact-rules.md`
- Modify: `references/document-templates.md`
- Modify: `templates/product.md`
- Modify: `templates/requirement-set-README.md`

- [x] **Step 1: Write the owning reference**

`references/product-definition.md` must include, in this order:

```text
Purpose / ownership
Product Definition Depth Scan
Brief all-of eligibility
Standard any-of triggers
adaptive upgrade
Product Completeness Scan
Human Grill integration
Product View Applicability
Product Human Review
source preservation / append-only follow-up
PRD helper adapter boundary
Archify scoped confirmation / freshness / fallback
downstream Product Slice handoff
legacy compatibility
stop rules
```

Keep Concept Foundation and Requirement Product Model as internal methods. Do not add them to stage order.

- [x] **Step 2: Convert `templates/product.md` to Requirement Product Definition**

Start with:

```markdown
# Product Requirement: <Requirement Name>

Requirement ID: <REQ-ID>
Product Definition Profile: brief | standard
Product Review: pending | confirmed

## Source Evidence

| Source | Type | Product Claim Used | Preserved / Referenced |
|---|---|---|---|
```

Include Brief core sections, then clearly marked Standard-only adaptive sections, Product View Applicability, Derived Visuals, Decision Candidates, Product Traceability, and Product Human Review Evidence. Do not include engineering plan, database, API schema, test commands, Feature tasks, or placeholder stable rows.

- [x] **Step 3: Update Requirement README pointer and lifecycle separation**

Add `## Effective Product Definition` exactly as approved. Keep a documented legacy `## Effective Concept Foundation` reader note, but do not render both blocks in one new template.

README must state:

```text
Product Review confirmation does not change Requirement Status or authorize Feature start.
```

- [x] **Step 4: Coordinate Requirement source preservation and follow-up rules**

Update Requirement Management and Artifact Rules so `requirements/<set>/product.md` owns Agent-authored reviewed product definition, while human originals remain source materials. Preserve root-level legacy source layout and recommend `sources/` only for new material packages without forcing empty directories.

Define append-only follow-up names and Effective Product Definition pointer advancement. Do not edit confirmed `product.md` in place after semantic change.

- [x] **Step 5: Replace standalone Concept approval surface with cumulative Product Review coverage**

Keep the evidence-first, recommendation, and one-blocking-question Human Grill contract. Move the cumulative concept/model table into Product Human Review. The summary must show:

```text
Profile decision
source evidence
included/not-applicable product views
confirmed concepts/rules
open blockers
visual freshness
Design Readiness candidates
explicit product-definition decision
non-authorization statement
```

Do not remove the stop on unresolved semantic blockers.

- [x] **Step 6: Run writer/reference focused contract**

Run:

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
python3 -m unittest tests/test_requirement_product_definition.py
```

Expected: ownership/template assertions added through Task 4 pass; runtime stage assertions may remain RED until Task 5.

## Task 5: Runtime/design/stage routing 收敛

**Files:**
- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/concepts.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/product-brief.md`
- Modify: `references/project-guidance.md`
- Modify: `templates/root-AGENTS.md`

- [x] **Step 1: Update controller entry and package map**

Add `references/product-definition.md` to the package map. Requirements Discussion loads it after Requirement Management. Remove new Feature Product Brief authoring language; mark `references/product-brief.md` as legacy compatibility only.

Required controller wording:

```text
Requirements Discussion chooses brief or standard Product Definition depth, uses PRD helpers as methods, and produces one human-reviewed Requirement product.md after the Requirement Record/Archive Gate.
```

- [x] **Step 2: Change runtime ownership and leaf-stage order together with design**

Replace:

```text
Requirement Archive
→ Decision & Design If Needed
→ Product Brief if Needed
→ Brainstorm / Clarify if Needed
→ Feature Spec
```

with the approved order:

```text
Requirements Discussion [internal Brief/Standard Product Definition]
→ Requirement Record / Archive
→ Design Readiness / Decision & Design If Needed
→ Brainstorm / Clarify if Needed for Feature-local implementation uncertainty
→ Feature Spec with Product Slice
```

Do not move Brainstorm / Clarify ahead of accepted product semantics when it would redefine the Requirement. Keep Message Intent, Feature, Bug, Lightweight and ADR precedence unchanged.

- [x] **Step 3: Keep internal methods internal**

Runtime/design must explicitly say:

```text
Product Definition Depth Scan, Product Completeness Scan, Concept Foundation, Requirement Product Model, and derived visual generation are internal Requirements Discussion methods, not canonical stages or message intents.
```

No root Stage Map row may name these as a first hop.

- [x] **Step 4: Convert Product Brief reference to legacy compatibility**

`references/product-brief.md` must say:

```text
Do not create feature/product.md for new work.
Read an existing Feature Product Brief during Resume, Follow-up, Review, Close, or Recovery.
If it conflicts with the Effective Product Definition, stop for Requirement conflict/recovery; do not rewrite either source silently.
```

- [x] **Step 5: Refresh root managed-block content without changing version/revision unless required by approved implementation scope**

Only update the existing Requirements/Feature gateway wording and leaf-order delegation. Preserve all 13 managed blocks, the current revision, 16 Gateway rows, Human Gates, Completion, Submit, and Artifact Authority. Do not put the full PRD algorithm in root.

- [x] **Step 6: Run routing tests**

Run:

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
bash tests/validate-chat-requirements-entry.sh
bash tests/validate-requirement-product-grill.sh
bash tests/validate-concept-foundation-requirement-modeling.sh
bash tests/validate-product-brief-source-gate.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
python3 -m unittest tests/test_root_agents_blocks.py
python3 -m unittest tests/test_root_agents_lossless_slimming.py
```

Expected: updated contracts pass and no root capability/revision drift appears.

## Task 6: Feature Product Slice 与 ADR dual-reader landing

**Files:**
- Modify: `templates/spec.md`
- Modify: `templates/decision.md`
- Modify: `references/project-decisions.md`
- Modify: `references/feature-completion-check.md`
- Modify: `scripts/check-concept-foundation-trace.py`
- Modify: `scripts/check-adr-requirement-model-trace.py`
- Modify: `tests/test_concept_foundation_trace.py`
- Modify: `tests/test_adr_requirement_model_trace.py`
- Modify: `tests/fixtures/adaptive-product-definition/standard-valid/spec.md`
- Create: `tests/fixtures/adaptive-product-definition/standard-valid/decision.md`

- [x] **Step 1: Add Product Requirement Source and Product Slice to Feature Spec**

Use the Proposal table exactly. Require full Requirement Set path, effective source, Profile, review evidence and Applicable Decisions. Product Slice rows use source section/model ID, Feature responsibility, acceptance mapping and `in-scope | out-of-scope | not-applicable` coverage.

- [x] **Step 2: Make concept trace checker support new and legacy modes**

Preserve the current positional legacy mode:

```text
check-concept-foundation-trace.py <legacy-requirement> <legacy-feature-product> <spec>
```

Add explicit new mode to avoid ambiguous three-file guessing:

```text
check-concept-foundation-trace.py --requirement-product \
  <requirement-readme> <requirement-product> <spec>
```

New mode validates the Requirement Product Definition and Product Slice directly; it must not require Feature `product.md`.

- [x] **Step 3: Update ADR Effective Requirement Snapshot**

New ADR template fields:

```text
Effective Product Source:
Product Definition Profile:
Product Review:
Accepted Concept IDs:
Accepted Requirement Model IDs:
Accepted Product Rule References:
Upstream Compatibility:
Last Compatibility Check:
```

Legacy snapshot fields remain accepted by the checker only for legacy Requirement pointers. New source must not use legacy `Effective Concept Source` as its primary field.

- [x] **Step 4: Validate section-anchor Product Rules without adding `RULE-*`**

For new Standard product definitions, parse Product Rule references as `product.md#<anchor>` or `<section>#<rule-slug>`. Require concrete accepted meaning in ADR Scope/Trace; reject free-floating rule text that cannot resolve to the effective source.

- [x] **Step 5: Add real new-format integration test**

Run one fixture through:

```bash
python3 scripts/check-requirement-product-definition.py \
  tests/fixtures/adaptive-product-definition/standard-valid/README.md \
  tests/fixtures/adaptive-product-definition/standard-valid/product.md \
  tests/fixtures/adaptive-product-definition/standard-valid/spec.md

python3 scripts/check-adr-requirement-model-trace.py \
  tests/fixtures/adaptive-product-definition/standard-valid/README.md \
  tests/fixtures/adaptive-product-definition/standard-valid/product.md \
  tests/fixtures/adaptive-product-definition/standard-valid/decision.md \
  tests/fixtures/adaptive-product-definition/standard-valid
```

Expected: both pass; mutation of Profile review, pointer, model ID, Product Rule anchor, Product Slice or Upstream Compatibility fails.

- [x] **Step 6: Preserve legacy integration**

Run:

```bash
python3 scripts/check-concept-foundation-trace.py \
  examples/concept-foundation-refund/requirement.md \
  examples/concept-foundation-refund/product.md \
  examples/concept-foundation-refund/spec.md

python3 -m unittest tests/test_concept_foundation_trace.py
python3 -m unittest tests/test_adr_requirement_model_trace.py
```

Expected: all existing legacy tests pass unchanged or with assertion wording updated only where shared error wording intentionally changed.

## Task 7: PRD helper、Archify、scenarios 与 human docs

**Files:**
- Modify: `references/skill-routing.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/validation-scenarios.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Create: `examples/adaptive-product-definition/requirements/2026-07-22-approval/product.md`
- Create: `examples/adaptive-product-definition/requirements/2026-07-22-approval/README.md`
- Create: `examples/adaptive-product-definition/features/2026-07-22-approval/spec.md`

- [x] **Step 1: Route PRD helpers to Requirements Discussion**

Change routing tables so Brainstorming and PRD/product helpers produce a response-local `product.md` draft and write it only through Requirement Record/Archive. Explicitly map helper Feature List to Product Capability Scope and forbid native `feature_list.md`, `PRD.md`, prototype deployment and Feature `product.md` output.

- [x] **Step 2: Document Archify scoped confirmation and fallback**

Add the source/type/output/use disclosure, Human confirmation, stable-ID binding, semantic digest, stale rule and no-Archify fallback. Do not make Archify a mandatory installed dependency.

- [x] **Step 3: Add pressure scenarios**

Add Proposal scenarios 16.1–16.8 plus mutations for:

```text
short refund demand routed to Standard
Standard without fake STATE table
human-provided PRD preserved under sources
two Features share one product.md through distinct Product Slices
legacy resume without migration
stale visual blocks current claim
Product Review does not authorize Feature start
PRD helper tries to deploy prototype
```

- [x] **Step 4: Write a complete human-readable example**

The example must use a Standard Product Definition with at least one not-applicable view reason, Product Human Review Evidence, and a Feature `spec.md` Product Slice. It must not contain a Feature `product.md`.

- [x] **Step 5: Update README/Usage/CHANGELOG**

Human docs must explain in Chinese:

```text
PRD 以后在哪里
谁写 product.md
Brief 与 Standard 怎么选
为什么没有 Complex PRD
Concept/Product Model/Archify 为什么仍存在但看不到 stage
旧 Feature product.md 怎么处理
Product Review 为什么不等于开始开发
```

Record the behavior under the current v1.5.0 in-progress/unreleased changelog section; do not create a new version heading.

## Task 8: Focused GREEN、affected regression 与 mutation pressure

**Files:**
- Modify as required by failing affected tests only; no unrelated refactor
- Update: `docs/reports/agent-loop-v1.5.0-adaptive-requirement-product-definition-red-baseline-2026-07-22.md`

- [x] **Step 1: Run the focused feature contract**

```bash
bash tests/validate-adaptive-requirement-product-definition.sh
python3 -m unittest tests/test_requirement_product_definition.py
python3 -m unittest tests/test_concept_foundation_trace.py
python3 -m unittest tests/test_adr_requirement_model_trace.py
```

Expected: all pass.

- [x] **Step 2: Run affected shell contracts**

```bash
for test_file in \
  tests/validate-chat-requirements-entry.sh \
  tests/validate-requirement-lifecycle-backlog.sh \
  tests/validate-requirement-product-grill.sh \
  tests/validate-concept-foundation-requirement-modeling.sh \
  tests/validate-decision-design-requirement-landing.sh \
  tests/validate-adr-requirement-model-technical-landing-trace.sh \
  tests/validate-project-decisions-adr-lane.sh \
  tests/validate-product-brief-source-gate.sh \
  tests/validate-grill-with-docs-requirement-product-proposal.sh \
  tests/validate-v1.2.4-requirement-product-docs.sh \
  tests/validate-root-agents-block-checker.sh \
  tests/validate-root-agents-block-refresh.sh \
  tests/validate-v1.2.4-root-stage-coverage.sh; do
  bash "$test_file"
done
```

Expected: every listed contract passes after semantic updates; do not retain obsolete assertions merely to preserve old wording.

- [x] **Step 3: Execute mutation pressure**

Use temporary copies only. Mutate one invariant at a time:

```text
brief -> complex
Product Review confirmed -> pending
remove one Product View Applicability row
included -> not-applicable with n/a
remove Effective Product Definition pointer
add legacy pointer beside new pointer
change Product Slice to unknown STATE ID
change visual digest by one hex
remove Human Grill one-blocker wording
restore Feature Product Brief writer route
```

Expected: the focused checker/contract fails for every mutation. Record commands and observed messages in the RED report's GREEN/mutation closure section.

- [x] **Step 4: Re-run focused tests after restoring temporary mutations**

Expected: all focused tests pass and `git status --short` contains no mutation leftovers.

## Task 9: Full executable regression 与 mechanical checks

**Files:**
- No planned source edits; investigate failures before changing anything

- [x] **Step 1: Recount and run every Shell test**

```bash
shell_total=$(find tests -maxdepth 1 -type f -name '*.sh' | wc -l | tr -d ' ')
printf 'Shell tests: %s\n' "$shell_total"
for test_file in tests/*.sh; do bash "$test_file"; done
```

Expected: every current `tests/*.sh` passes. Record actual count, not the plan-era count.

- [x] **Step 2: Run every Python unittest**

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

Expected: exit 0. Record unittest's actual `Ran N tests` output.

- [x] **Step 3: Run Ruby adversarial tests and syntax checks**

```bash
for test_file in tests/*.rb; do ruby "$test_file"; done
find . -name '*.sh' -type f -not -path './.git/*' -print0 | xargs -0 -n1 bash -n
find scripts tests -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
```

Expected: all exit 0. Remove only `__pycache__` created by this implementation run and only after proving they were not pre-existing human-owned paths; otherwise leave them untouched and report.

- [x] **Step 4: Run YAML/JSON/Markdown/diff checks**

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md"); YAML.load_file("agents/openai.yaml")'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
git diff --check
```

Run the repository Markdown fence checker or the exact Ruby fence balance method documented in current maintenance evidence. Expected: all pass.

- [x] **Step 5: Verify version and forbidden artifacts**

```bash
rg -n 'Version:|"version"|Current version' SKILL.md plugin.json README.md Usage.md
test ! -e .agent-loop
find . -type d -name '__pycache__' -not -path './.git/*' -print
git status --short
```

Expected: version remains 1.5.0; no target-project `.agent-loop/`; unrelated dirty paths preserved.

## Task 10: 六域 full validation 与中文报告

**Files:**
- Create: `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-22.md`
- Modify only for verified report status: Proposal and Plan

- [x] **Step 1: Follow the full method rather than inferring from tests**

Read `docs/maintenance/full-validation-method.md` again and audit:

```text
A. Core Loop And Routing
B. Artifact And Status Integrity
C. Human Gates And Safety
D. Verification And Completion
E. Memory, Recovery And Continuity
F. Documentation, Templates And Regression
```

Expected: current Critical/High/Medium all 0 before declaring strong acceptance. Any severity issue returns to the owning Task; do not lower the score to hide a control defect.

- [x] **Step 2: Run semantic pressure matrix**

At minimum manually trace:

```text
Chat -> no Requirement artifact
Requirements Discussion -> Brief product.md
Requirements Discussion -> Standard product.md
Standard -> Human Grill one blocker
confirmed product.md -> ADR dual reader
confirmed product.md -> Feature Product Slice
legacy requirement.md -> old ADR/spec compatibility
legacy Feature product.md -> Resume/Close compatibility
product follow-up -> ADR/Feature drift
Archify unavailable -> fallback, no permanent block
Product Review -> no implicit Feature/Git authorization
```

- [x] **Step 3: Write the full-validation report**

Include actual date, branch, HEAD, version, dirty-work boundary, RED/GREEN, focused results, actual Shell/Python/Ruby counts, mechanical checks, six-domain score, Critical/High/Medium findings, macOS/Windows status, remaining risk, range drift, and release judgment.

Do not overwrite an existing report path. If the path exists, stop and request a collision-safe suffix.

## Task 11: Proposal/Plan closure 与最终 Human Review

**Files:**
- Modify: `docs/proposal/v1.5.x/adaptive-requirement-product-definition.md`
- Modify: `docs/proposal/v1.5.x/adaptive-requirement-product-definition-implementation-plan.md`
- Read: all diffs and reports

- [x] **Step 1: Check Proposal acceptance item by item**

Create a compliance table mapping every Proposal section 1–20 to implementation files, tests and evidence. Mark only `implemented`, `verified`, `not-applicable with reason`, or `unresolved`.

- [x] **Step 2: Refresh true statuses**

Only if Tasks 0–10 are complete and all required checks pass:

```text
Proposal: 已实施并验证，等待最终 Human Review
Plan: Task 0–11 已执行，等待最终 Human Review
```

Do not mark implementation complete if Windows is only contract-defined; report that qualifier explicitly without treating it as a blocker unless the Proposal requires native Windows evidence.

- [x] **Step 3: Run final workspace audit**

```bash
git diff --stat
git diff --check
git status --short
git diff --name-only
git ls-files --others --exclude-standard
```

Expected: only approved implementation paths plus pre-existing unrelated dirty paths. No staged files, commit, tag or installed-skill changes.

- [x] **Step 4: Stop at Human Review**

Return:

```text
actual modified/new files
RED -> GREEN evidence
focused validation
full validation and actual counts
score and severity
Proposal coverage
legacy/new reader compatibility
macOS/Windows status
remaining risks and scope drift
git status/diff summary
explicit no commit/push/tag/release/sync statement
```

Do not implement any reviewer-requested follow-up, commit, push or release until the human provides new authorization.

## 执行停止条件

立即停止并交还人类，如果：

- Proposal 与 current runtime/design 出现实质冲突；
- 需要恢复 Product Hub/Board/Workbench 或增加 `complex` Profile；
- 需要新增 `RULE-*`、Product lifecycle、canonical stage/message intent 或 executable schema；
- 需要改写、移动或删除原始人类 Requirement source；
- reader-first 不能在不破坏旧 checker/fixture 的情况下实现；
- 新 Requirement 和 legacy pointer 无法可靠消歧；
- Feature Product Slice 无法替代新 Feature Product Brief 而不丢失 accepted semantics；
- Archify freshness 需要修改或安装外部 Archify runtime；
- 需要升级 Skill version 或 managed-block revision；
- 需要增加依赖或使用 Python 标准库之外的包；
- dirty work 与目标文件重叠且归属不清；
- baseline/full validation 反复失败且原因无法确认；
- 需要分支、worktree、Subagent、commit、push、tag、PR、merge、release、publish 或 installed-skill sync。

## Rollback 原则

实施未提交时按任务边界回滚 Agent 自己的修改，不碰执行前 dirty work：

1. Task 1 RED fixtures/report 可单独删除；
2. Task 2 reader module/checker refactor作为一组恢复；
3. Task 3 checker/fixtures 作为一组恢复；
4. Task 4–7 coordinated docs/templates/runtime 必须整体恢复，不能留下半套 ownership；
5. Task 8–10 只恢复 Agent 新增的 mutation/report/status edit；
6. 任何恢复前先保存 `git status --short`、`git diff --name-status` 和失败证据；
7. 禁止使用 `git reset --hard`、`git checkout --` 或清理整个工作区；只能通过精确 `apply_patch` 恢复本次 Agent 修改。

## Plan Human Review Checklist

- [x] 维护者接受 reader-first dual compatibility。
- [x] 维护者接受新增 `references/product-definition.md` 和标准库 checker/support。
- [x] 维护者接受新 Feature `product.md` writer 停用、legacy reader 保留。
- [x] 维护者接受 Product View Applicability 作为 Standard PRD 的 coverage 表，而不是 lifecycle。
- [x] 维护者接受 Archify semantic digest/freshness 仅做派生视图结构验证。
- [x] 维护者接受 Task 0–11 顺序、full validation 和停止条件。
- [x] 维护者授权主 Agent 使用 `executing-plans` inline 实施；未授权 Subagent、Git 或发布动作。

## 独立评测 Flow-back Addendum

- [x] 读取并逐条核验 `docs/reports/adaptive-requirement-product-definition-feature-validation-2026-07-22.md`；
- [x] 保存 `8` 个真实 Python failure 与 coordinated Shell failure 的 RED；
- [x] 修复 Brief → ADR reasoned not-applicable、legacy unified gate、snapshot shape、README freshness、review exactness 与 Brief inflation；
- [x] 协调 runtime/design/checklist/scenario/path/docs/example contracts；
- [x] 恢复 5 个无关 Shell mode churn；
- [x] focused `51/51`、affected Shell `14/14`、all Shell `40/40`、all Python `255/255`、Ruby `2/2`；
- [x] 新全量报告为 `docs/reports/agent-loop-v1.5.0-full-validation-2026-07-22.1.md`；旧报告和 80 分独立评测保留为历史证据；
- [x] 当前停在最终 Human Review，未执行任何 Git/发布/installed-skill 动作。
