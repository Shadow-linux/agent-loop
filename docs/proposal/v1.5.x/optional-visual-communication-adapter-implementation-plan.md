# Optional Visual Communication Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Do not dispatch subagents unless the human separately authorizes them. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a preferred-when-useful but non-mandatory Archify visual communication adapter that helps humans converge on Requirement, ADR, and Onboarding meaning while preserving Agent Loop artifact authority, bounded installation authorization, durable source/render verification, and non-blocking fallback.

**Architecture:** Keep Agent Loop as controller and treat Archify as an optional stage method. Working previews remain response-local or temporary; accepted meaning is written back to the owning Requirement `product.md`, ADR, or Onboarding artifact. New durable Archify diagrams use a reader-compatible, writer-strict `source-render-v1` contract backed by a shared Python standard-library envelope validator, while historical render-only Requirement rows remain readable.

**Tech Stack:** Markdown runtime contracts and templates, Bash focused contract tests, Python 3.10+ standard library validators and `unittest`, Archify typed JSON IR plus validated HTML/SVG/PNG/JPEG/WebP renders, Git read-only inspection.

---

状态：Tasks 0–14 实施与全量验证已完成；等待 Human Review；未 commit / push / tag / release / installed Agent Loop sync
设计来源：`docs/proposal/v1.5.x/optional-visual-communication-adapter.md`
目标分支：`alpha/v1.5.0`
计划基线 HEAD：`7a74667bc3ce6acd99b34fc867115fbc8455b7f3`
目标版本：v1.5.0；不得升级版本
计划创建时间：2026-07-23
上游能力：<https://github.com/tt-a1i/archify>

## 实施约束

- 这是 Agent Loop Skill 源仓库，不在仓库根目录创建目标项目 `.agent-loop/`。
- 保留当前无关 dirty/untracked 内容，尤其是 `.tmp/`、`scripts/__pycache__/` 和 `tests/__pycache__/`；不得删除、暂存或提交它们。
- Proposal 已确认的只是设计和本计划编写；开始 Task 0 之前仍需人类明确授权实施。
- 不把 Archify 加入 mandatory helper table，不新增 canonical stage、message intent、lifecycle、status、Auto Mode 或 root Stage Map row。
- 不在 Agent Loop 仓库内复制 Archify schema、renderer、assets、CLI 或安装器。
- Agent Loop 不硬编码一个跨运行时安装命令。运行时 Agent 必须发现当前环境的可信安装机制，展示 exact source / revision / command / target / effects / doctor / fallback，再请求一次精确授权。
- 安装授权、Visual Scope Grant、durable record、Product Human Review、ADR acceptance、Onboarding Gate、Feature start、Git 和 release 动作保持独立。
- `Visual Trigger` 不成立时不画图；Archify 缺失、被拒绝或失败时使用 Markdown、table、Mermaid 或 ASCII 继续。
- 产品语义只写回 Requirement `product.md`；技术决策只写回 ADR；代码与环境事实只由代码、配置、测试和运行证据承担。
- 新 durable Archify artifact 必须有 typed JSON source、validated render、source binding、digest、generator/version 和 validation evidence；HTML-only 不能满足新 durable contract。
- 历史 Requirement render-only visual 继续由 legacy reader 接受，不批量迁移、不改写人类原始材料。
- Python 仅使用标准库，保持 UTF-8 BOM、CRLF 和 Windows-style path reader compatibility。
- 实施完成后必须执行 focused RED/GREEN、mutation pressure 和 `docs/maintenance/full-validation-method.md`；机械测试不能替代六域语义审计。
- 本计划不授权创建/切换分支或 worktree，不授权 Subagent，不授权安装、commit、push、tag、PR、merge、release、publish 或 installed-skill sync。

## 文件职责与目标结构

### 新文件

| 文件 | 单一职责 |
|---|---|
| `scripts/visual_artifact_support.py` | 验证新 durable Archify source/render envelope、路径、JSON identity、hash、generator 和 validation evidence |
| `tests/test_optional_visual_communication_adapter.py` | source/render validator、Requirement/ADR/Onboarding integration、BOM/CRLF/path 和 mutation tests |
| `tests/validate-optional-visual-communication-adapter.sh` | 跨 runtime/design/routing/gate/template/docs 的 focused textual contract |
| `tests/fixtures/optional-visual-communication-adapter/` | valid source-render、render-only、stale、missing-file、ADR 和 Onboarding fixtures |
| `docs/reports/agent-loop-v1.5.0-optional-visual-communication-adapter-red-baseline-2026-07-23.md` | 实施前真实 RED 证据 |
| `docs/reports/agent-loop-v1.5.0-optional-visual-communication-adapter-focused-validation-2026-07-23.md` | focused GREEN 与 mutation 证据 |

### 修改文件族

| 文件族 | 目标职责 |
|---|---|
| `SKILL.md`, `references/runtime.md`, `references/design.md` | adapter 可发现性、Visual Trigger、Visual Scope Grant、安装授权、authority layering 和 fallback |
| `references/external-skill-adapters.md`, `references/skill-routing.md` | optional visual adapter resolution、preferred-when-triggered、安装与失败边界；不进入 mandatory helper resolution |
| `references/product-definition.md`, `templates/product.md` | Requirement preview-to-consensus 与新 durable `source-render-v1` manifest |
| `scripts/check-requirement-product-definition.py`, `tests/test_requirement_product_definition.py` | writer-strict / legacy-reader product visual validation |
| `references/project-decisions.md`, `templates/decision.md`, `scripts/check-adr-requirement-model-trace.py`, `tests/test_adr_requirement_model_trace.py` | ADR option/comparison visual、source binding、proposed/accepted Gate 独立性 |
| `references/onboarding-knowledge-base.md`, `templates/onboarding-db/flow.md`, `scripts/check-onboarding-core-flow-coverage.py`, `tests/test_onboarding-core-flow-coverage.py` | embedded Mermaid/ASCII 或 Archify source+render representation；HTML-only 不得满足 required Diagram ID |
| `references/stage-guides.md`, `references/workflow-checklists.md`, `references/human-review-summary.md` | Requirements-first visual convergence、Feature semantic return、review summary 和 Gate 检查 |
| `references/validation-scenarios.md` | 正反例与 mutation pressure 的语义场景 |
| `examples/ai-meeting-minutes-backend/onboarding-db/` 与 affected fixtures | 为 required Diagram ID 补 representation metadata，不改变示例含义 |
| `README.md`, `Usage.md`, `CHANGELOG.md` | 人类触发方式、安装授权示例、fallback、upstream URL 和 v1.5.0 未发布行为记录 |
| `docs/reports/agent-loop-1.5.0-full-validation-2026-07-23.md` | 全量验证中文报告；若路径已存在则使用不覆盖历史证据的新日期后缀 |

### 明确不修改

- `templates/root-AGENTS.md`：现有 Requirements Discussion / Decision / Onboarding first-hop 足够；实施审计只有证明不可达时才回到人类重新批准范围。
- Skill version-bearing files：本能力属于当前 v1.5.0，不升级版本。
- installed Archify 与 installed Agent Loop：只在目标运行时、人类另行授权时操作，不属于本仓库实施。
- Archify upstream 内容：只引用 URL 和运行时发现结果，不 vendor。

## Durable Visual Contract

新 writer 使用显式合同标记：

```text
Visual Manifest Contract: source-render-v1
```

Requirement `Derived Visuals` 的新表头固定为：

```markdown
| Diagram ID | Source Definition | Render | Type | Source IDs | Product Semantic SHA-256 | Source SHA-256 | Render SHA-256 | Generator | Validation Evidence | Status | Human Confirmed |
|---|---|---|---|---|---|---|---|---|---|---|---|
```

ADR `Optional Visual Evidence` 的新表头固定为：

```markdown
| Diagram ID | Review Question | Semantic References | Source Definition | Render | Type | Source SHA-256 | Render SHA-256 | Generator | Validation Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|
```

Onboarding `Diagram Artifact Manifest` 的新表头固定为：

```markdown
| Diagram ID | Evidence References | Source Definition | Render | Type | Source SHA-256 | Render SHA-256 | Generator | Validation Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|
```

共享 envelope 规则：

- `Diagram ID` 匹配 `D-[A-Z0-9-]+`，在所属 manifest 内唯一；
- `Type` 只能是 Archify 的 `architecture | workflow | sequence | dataflow | lifecycle`；
- source path 必须是 Requirement/ADR/Onboarding owning root 内的相对 `.json` regular file；
- render path 必须是 owning root 内不同于 source 的相对 `.html | .svg | .png | .jpeg | .jpg | .webp` regular file；
- JSON 顶层必须是 object，`schema_version == 1`，`diagram_type` 与 manifest `Type` 一致，`meta.output` 的 basename 与 render basename 一致；
- `Source SHA-256`、`Render SHA-256` 是实际 bytes 的 64 位 lowercase SHA-256；
- `Generator` 匹配 `archify@<numeric-version>`；
- `Validation Evidence` 同时包含 `validate=pass` 与 `check=pass`；
- `Status` 只能以 `current` 进入任何 Human Review；source、semantic source 或 render 改变后必须重新验证并更新 hashes；
- Requirement 另需 known stable IDs、当前 Product Semantic SHA-256 和 concrete Human confirmation；
- ADR 另需具体 Review Question 和来自 Effective Requirement Snapshot / ADR section 的 Semantic References；
- Onboarding 另需 code/config Evidence References，且 required Diagram ID 的 representation 必须是 `embedded-mermaid | embedded-ascii | archify-source-render` 之一。

兼容规则：没有 `Visual Manifest Contract`、仍使用旧六列表头的已存在 Requirement visual 走 legacy read path；新 template、runtime writer 和 examples 一律写 `source-render-v1`。若标记存在但列缺失，validator 必须 fail closed。

## Task 0: Baseline、dirty ownership 与实施 Gate

**Files:**
- Read: `AGENTS.md`
- Read: `SKILL.md`
- Read: `references/runtime.md`
- Read: `references/design.md`
- Read: `docs/proposal/v1.5.x/optional-visual-communication-adapter.md`
- Read: `docs/proposal/v1.5.x/optional-visual-communication-adapter-implementation-plan.md`
- Read: `docs/maintenance/full-validation-method.md`
- Modify only after authorization: Proposal and this Plan status lines

- [x] **Step 1: Capture branch, HEAD and dirty ownership**

Run:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git diff --name-status
git ls-files --others --exclude-standard
```

Expected: branch is `alpha/v1.5.0`; HEAD is the plan baseline or a later human-explained commit; Proposal/Plan are the only owned pending documents; `.tmp/` and cache directories remain unrelated and untouched.

- [x] **Step 2: Read all controlling sources completely**

Run:

```bash
cat AGENTS.md
cat SKILL.md
cat references/runtime.md
cat references/design.md
cat docs/proposal/v1.5.x/optional-visual-communication-adapter.md
cat docs/proposal/v1.5.x/optional-visual-communication-adapter-implementation-plan.md
cat docs/maintenance/full-validation-method.md
```

Expected: no newer human decision contradicts optionality, Requirements-first use, independent gates, source/render layering, legacy compatibility or full-validation scope.

- [x] **Step 3: Run the pre-change executable baseline**

Run:

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
```

Expected: all existing tests pass. Record live counts; never reuse a historical report count. If any baseline is red, stop and classify it before writing implementation files.

- [x] **Step 4: Mark implementation started only after explicit Human authorization**

Use these exact status meanings:

```text
Proposal: confirmed, implementation authorized and in progress
Plan: Task 0 started; no install/Git/release authorization
```

Do not treat plan approval as Archify installation or Git approval.

## Task 1: Focused RED contracts and evidence

**Files:**
- Create: `tests/validate-optional-visual-communication-adapter.sh`
- Create: `tests/test_optional_visual_communication_adapter.py`
- Create: `tests/fixtures/optional-visual-communication-adapter/`
- Create: `docs/reports/agent-loop-v1.5.0-optional-visual-communication-adapter-red-baseline-2026-07-23.md`

- [x] **Step 1: Add a focused shell contract that must initially fail**

The new script must use the repository `assert_contains` / `assert_not_contains` pattern and assert these exact behavior anchors:

```bash
assert_contains references/external-skill-adapters.md 'Optional Visual Communication Adapter'
assert_contains references/external-skill-adapters.md 'https://github.com/tt-a1i/archify'
assert_contains references/external-skill-adapters.md 'preferred when a Visual Trigger materially lowers misunderstanding risk'
assert_contains references/external-skill-adapters.md 'Installation Authorization'
assert_contains references/external-skill-adapters.md 'Visual Scope Grant'
assert_contains references/external-skill-adapters.md 'do not hard-code one cross-runtime install command'
assert_contains references/external-skill-adapters.md 'does not authorize Product Human Review, ADR acceptance, Feature start, Git, release, publish, or future external actions'
assert_contains references/skill-routing.md 'optional visual communication adapter'
assert_not_contains references/skill-routing.md '| Requirements Visual Communication | `archify` |'
assert_contains references/product-definition.md 'render to converge, text to record'
assert_contains references/product-definition.md 'source-render-v1'
assert_contains references/project-decisions.md 'Optional Visual Evidence'
assert_contains references/onboarding-knowledge-base.md 'archify-source-render'
assert_contains templates/product.md 'Visual Manifest Contract: source-render-v1'
assert_contains templates/decision.md '## Optional Visual Evidence'
assert_contains templates/onboarding-db/flow.md 'Representation: embedded-mermaid | embedded-ascii | archify-source-render'
assert_contains README.md 'https://github.com/tt-a1i/archify'
assert_contains Usage.md 'Visual Scope Grant'
```

The final line must be:

```bash
printf 'PASS: optional visual communication adapter routing, gates, durable source/render, fallback, and compatibility contract is complete\n'
```

- [x] **Step 2: Add Python RED cases before support code**

Create these exact test methods and assertions:

| Test method | Assertion |
|---|---|
| `test_valid_archify_source_render_pair_passes` | returned source/render paths equal the confined files |
| `test_source_path_escape_is_rejected` | raises `VisualArtifactError` containing `source definition escapes owning root` |
| `test_render_only_pair_is_rejected` | raises `VisualArtifactError` containing `source definition is required` |
| `test_source_type_mismatch_is_rejected` | raises `VisualArtifactError` containing `diagram_type does not match manifest Type` |
| `test_meta_output_mismatch_is_rejected` | raises `VisualArtifactError` containing `meta.output does not match render` |
| `test_source_hash_drift_is_rejected` | raises `VisualArtifactError` containing `source SHA-256 is stale` |
| `test_render_hash_drift_is_rejected` | raises `VisualArtifactError` containing `render SHA-256 is stale` |
| `test_generator_without_version_is_rejected` | raises `VisualArtifactError` containing `generator must be archify@version` |
| `test_validation_without_validate_and_check_is_rejected` | raises `VisualArtifactError` containing `validation evidence requires validate=pass and check=pass` |
| `test_product_source_render_manifest_passes` | Product checker exits 0 |
| `test_product_contract_marker_with_legacy_columns_is_rejected` | Product checker exits 1 with `source-render-v1 columns mismatch` |
| `test_legacy_product_visual_row_remains_readable` | current six-column legacy fixture still exits 0 |
| `test_adr_visual_cannot_change_accepted_status` | proposed ADR remains proposed and accepted mode still requires existing Human Review Evidence |
| `test_onboarding_archify_pair_satisfies_required_diagram` | Onboarding checker exits 0 |
| `test_onboarding_html_only_required_diagram_is_rejected` | checker exits 1 with `archify-source-render requires source and render` |
| `test_onboarding_embedded_mermaid_and_ascii_remain_valid` | both representations exit 0 without manifest rows |
| `test_bom_crlf_and_windows_style_paths_are_supported` | valid pair passes with BOM JSON and backslash manifest paths |

Use `tempfile.TemporaryDirectory`, `hashlib.sha256`, `json.dumps`, `pathlib.Path`, `shutil.copytree`, `unittest`, and `tests.checker_test_support.run_checker`; do not add packages.

- [x] **Step 3: Run only the new tests and capture real RED**

Run:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
python3 -m unittest tests.test_optional_visual_communication_adapter -v
```

Expected: both fail because the adapter contract and support module do not exist. The RED report records command, exit status, the first relevant failure, intended invariant, branch, HEAD and dirty boundary. It must not claim GREEN.

## Task 2: Shared durable visual envelope validator

**Files:**
- Create: `scripts/visual_artifact_support.py`
- Test: `tests/test_optional_visual_communication_adapter.py`

- [x] **Step 1: Implement the shared standard-library API**

Create these public definitions and implementation:

```python
from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass
from pathlib import Path


ARCHIFY_TYPES = frozenset({"architecture", "workflow", "sequence", "dataflow", "lifecycle"})
RENDER_SUFFIXES = frozenset({".html", ".svg", ".png", ".jpeg", ".jpg", ".webp"})
DIAGRAM_ID = re.compile(r"D-[A-Z0-9-]+")
GENERATOR = re.compile(r"archify@[0-9]+(?:\.[0-9]+)+")
LOWER_SHA256 = re.compile(r"[0-9a-f]{64}")

@dataclass(frozen=True)
class DurableVisualArtifact:
    diagram_id: str
    diagram_type: str
    source_path: Path
    render_path: Path
    source_sha256: str
    render_sha256: str
    generator: str

class VisualArtifactError(ValueError):
    pass


def _value(raw: str) -> str:
    text = (raw or "").strip()
    if len(text) >= 2 and text[0] == text[-1] == "`":
        text = text[1:-1].strip()
    return text


def _owned_file(root: Path, raw: str, *, label: str) -> Path:
    value = _value(raw).replace("\\", "/")
    if not value:
        raise VisualArtifactError(f"{label} is required")
    candidate = Path(value)
    if candidate.is_absolute() or re.match(r"^[A-Za-z]:/", value):
        raise VisualArtifactError(f"{label} must be relative")
    if ".." in candidate.parts:
        raise VisualArtifactError(f"{label} escapes owning root")
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as error:
        raise VisualArtifactError(f"{label} escapes owning root") from error
    if not resolved.is_file():
        raise VisualArtifactError(f"{label} file is missing: {value}")
    return resolved


def _actual_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_durable_visual(
    root: Path,
    *,
    diagram_id: str,
    source_definition: str,
    render: str,
    diagram_type: str,
    source_sha256: str,
    render_sha256: str,
    generator: str,
    validation_evidence: str,
) -> DurableVisualArtifact:
    if DIAGRAM_ID.fullmatch(_value(diagram_id)) is None:
        raise VisualArtifactError("Diagram ID must match D-[A-Z0-9-]+")
    kind = _value(diagram_type)
    if kind not in ARCHIFY_TYPES:
        raise VisualArtifactError(f"unsupported Archify Type: {kind}")
    source_path = _owned_file(root, source_definition, label="source definition")
    render_path = _owned_file(root, render, label="render")
    if source_path == render_path:
        raise VisualArtifactError("source definition and render must differ")
    if not source_path.name.endswith(f".{kind}.json"):
        raise VisualArtifactError("source definition filename must include Type and .json")
    if render_path.suffix.lower() not in RENDER_SUFFIXES:
        raise VisualArtifactError("unsupported render suffix")

    try:
        payload = json.loads(source_path.read_bytes().decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VisualArtifactError("source definition must be UTF-8 JSON") from error
    if not isinstance(payload, dict):
        raise VisualArtifactError("source definition root must be an object")
    if payload.get("schema_version") != 1:
        raise VisualArtifactError("source definition schema_version must be 1")
    if payload.get("diagram_type") != kind:
        raise VisualArtifactError("diagram_type does not match manifest Type")
    meta = payload.get("meta")
    if not isinstance(meta, dict) or not isinstance(meta.get("output"), str):
        raise VisualArtifactError("source definition meta.output is required")
    output_name = Path(meta["output"].replace("\\", "/")).name
    if output_name != render_path.name:
        raise VisualArtifactError("meta.output does not match render")

    expected_source = _value(source_sha256)
    expected_render = _value(render_sha256)
    if LOWER_SHA256.fullmatch(expected_source) is None:
        raise VisualArtifactError("source SHA-256 must be 64 lowercase hex")
    if LOWER_SHA256.fullmatch(expected_render) is None:
        raise VisualArtifactError("render SHA-256 must be 64 lowercase hex")
    if not hmac.compare_digest(_actual_sha256(source_path), expected_source):
        raise VisualArtifactError("source SHA-256 is stale")
    if not hmac.compare_digest(_actual_sha256(render_path), expected_render):
        raise VisualArtifactError("render SHA-256 is stale")

    generator_value = _value(generator)
    if GENERATOR.fullmatch(generator_value) is None:
        raise VisualArtifactError("generator must be archify@version")
    evidence = _value(validation_evidence).lower()
    if "validate=pass" not in evidence or "check=pass" not in evidence:
        raise VisualArtifactError(
            "validation evidence requires validate=pass and check=pass"
        )
    return DurableVisualArtifact(
        diagram_id=_value(diagram_id),
        diagram_type=kind,
        source_path=source_path,
        render_path=render_path,
        source_sha256=expected_source,
        render_sha256=expected_render,
        generator=generator_value,
    )
```

The function must normalize backslashes to `/`, reject absolute/escaping/non-file paths, reject identical source/render paths, parse source with `encoding="utf-8-sig"`, require the JSON envelope specified above, compare actual byte hashes with `hmac.compare_digest`, require `validate=pass` and `check=pass`, and return only validated absolute Paths. Configure deterministic UTF-8 output through existing `checker_support` callers rather than adding runtime dependencies.

- [x] **Step 2: Run the shared validator unit subset**

Run:

```bash
python3 -m unittest \
  tests.test_optional_visual_communication_adapter.OptionalVisualArtifactSupportTests -v
```

Expected: valid pair and BOM/CRLF/path cases pass; path escape, render-only, mismatched type/output/hash, unsupported generator and incomplete evidence fail with one stable reason each.

- [x] **Step 3: Refactor only after GREEN**

Keep path confinement, JSON-envelope validation and hash validation in `visual_artifact_support.py`; Product, ADR and Onboarding checkers may add ownership-specific meaning but must not duplicate shared file validation.

## Task 3: Controller, design and optional adapter routing

**Files:**
- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/skill-routing.md`
- Modify: `references/skill-routing.md`
- Test: `tests/validate-optional-visual-communication-adapter.sh`

- [x] **Step 1: Add the controller contract without a new stage**

Add one concise `SKILL.md` rule that routes triggered visual communication to `references/external-skill-adapters.md`, while stating that Agent Loop retains stage/gate/artifact control and fallback remains valid.

Add this exact internal order to runtime/design, expressed in repository terminology:

```text
current owning stage
→ decide whether one Visual Trigger materially improves a named Review Question
→ resolve active project-local visual skill first, then installed Archify
→ if loaded: disclose or reuse the bounded Visual Scope Grant
→ if unavailable: recommend Archify with exact install disclosure and fallback
→ if authorized: execute only the disclosed install, run doctor, then use the disclosed current scope
→ generate and validate a working preview
→ human accepts or corrects the meaning
→ write accepted meaning back to the owning text artifact
→ create a durable source/render pair only through a separate exact-path record decision
→ continue the existing owning-stage Human Gate
```

- [x] **Step 2: Define adapter resolution and installation authorization**

`references/external-skill-adapters.md` must state:

- Archify is an optional adapter, never a mandatory helper or stage blocker;
- a matching active project-local Skill wins before a global/runtime Archify Skill;
- installed Archify is preferred only when Visual Trigger is true;
- unavailable Archify produces one contextual recommendation, upstream URL, resolved source/revision, exact command, target path, network/file/global impact, doctor/equivalent check and fallback;
- the Agent may install only after explicit Human authorization and may continue into the already disclosed Visual Scope only when that scope was included in the request;
- failed install stops without elevation, mirror/source/package-manager/location changes or automatic retry;
- the adapter never chooses stage, output owner, product meaning, ADR result, lifecycle, Product Review, Feature start or Git action;
- a declined recommendation is not repeated in the same unchanged Review Context;
- Agent Loop contains no universal installer command and no vendored Archify implementation.

- [x] **Step 3: Add optional routing without touching mandatory resolution**

Add Archify to the `Preferred Skills` behavior for Requirements Discussion, Decision & Design, Onboarding and Review as a conditional visual method. Do not add a row to `Mandatory Helper Resolution Protocol`; do not make fallback require an `unavailable` mandatory-helper record unless the owning stage already has such a requirement for another helper.

- [x] **Step 4: Run routing RED/GREEN subset**

Run:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
bash tests/validate-mandatory-helper-routing.sh
bash tests/validate-project-skill-discovery-guard.sh
bash tests/validate-adaptive-requirement-product-definition.sh
```

Expected: all pass; the mandatory helper table is unchanged; Project Skill Discovery Guard still precedes generic/global fallback; root Stage Map remains unchanged.

## Task 4: Requirement visual convergence and source-render manifest

**Files:**
- Modify: `references/product-definition.md`
- Modify: `templates/product.md`
- Modify: `scripts/check-requirement-product-definition.py`
- Modify: `tests/test_requirement_product_definition.py`
- Add fixtures under: `tests/fixtures/optional-visual-communication-adapter/requirement-*`

- [x] **Step 1: Replace per-generation confirmation with bounded Visual Scope**

Keep Archify optional, but replace “confirm every generation” with:

```text
Visual Scope Grant = Stage/Review Context + Review Question + Diagram Type Family + exact semantic source + stable references + working output boundary + optional durable output + iteration boundary + fallback
```

State that corrections inside the same Review Question/source/type/working boundary may iterate without another Gate. New source, stage, diagram family, durable path, external effect or product meaning requires a new grant. After each accepted correction, update `product.md` first; regenerate from the new semantic digest rather than treating the picture as authority.

- [x] **Step 2: Change the new writer template**

Replace the current six-column `Derived Visuals` template with the exact `source-render-v1` marker and twelve-column table in this plan. Explain directly above the table that working previews are omitted and only separately confirmed durable pairs are recorded.

- [x] **Step 3: Add dual-reader validation**

Refactor `validate_visual_manifest` into three named functions: `validate_legacy_visual_manifest`, `validate_source_render_visual_manifest`, and the routing `validate_visual_manifest`. All three accept the existing `EffectiveProductSource`; the first two also accept parsed row dictionaries.

Routing rules:

- absent section: pass;
- absent contract marker plus exact legacy columns: run existing legacy rules unchanged;
- `source-render-v1`: require exact new columns and call `validate_durable_visual` with `source.path.parent` plus every shared envelope field from the row;
- any other marker, mixed columns or missing required column: fail closed;
- new rows additionally require unique Diagram ID, known Source IDs, current Product Semantic SHA-256, `Status == current`, and concrete Human confirmation;
- existing legacy fixture and historical row stay valid without file migration.

- [x] **Step 4: Run Product tests**

Run:

```bash
python3 -m unittest tests.test_requirement_product_definition -v
python3 -m unittest \
  tests.test_optional_visual_communication_adapter.RequirementVisualIntegrationTests -v
bash tests/validate-adaptive-requirement-product-definition.sh
```

Expected: new pair passes; marker-plus-legacy columns, unknown ID, stale semantic digest, source/render drift, render-only and path escape fail; historical legacy visual continues to pass.

## Task 5: ADR visual comparison and independent acceptance

**Files:**
- Modify: `references/project-decisions.md`
- Modify: `templates/decision.md`
- Modify: `scripts/check-adr-requirement-model-trace.py`
- Modify: `tests/test_adr_requirement_model_trace.py`
- Add fixtures under: `tests/fixtures/optional-visual-communication-adapter/adr-*`

- [x] **Step 1: Add ADR visual boundaries**

Define visuals as optional aids for comparing architecture, sequence, dataflow, lifecycle or workflow alternatives. A picture may clarify options and impacts, but accepted technical text still lives in ADR sections; a picture cannot introduce product meaning or change `Status: proposed` to `accepted`.

If the diagram reveals uncertain product meaning, return to Requirements Discussion. If it reveals a technical choice, update the ADR and rerun proposed preflight before asking for the existing Decision & Design Human Review.

- [x] **Step 2: Add optional template section**

Add `## Optional Visual Evidence` with `Visual Manifest Contract: source-render-v1` and the exact eleven-column ADR table. State that the section is removed when unused, working previews are not recorded, and `Status: current` does not mean ADR accepted.

- [x] **Step 3: Extend ADR checker without widening lifecycle**

When the optional section exists:

- require the marker and exact columns;
- validate each durable pair against `decision_path.parent` through shared support;
- require unique Diagram IDs and concrete Review Question;
- require Semantic References to resolve to Effective Requirement Snapshot stable IDs, Product Rule references, or ADR section anchors;
- require `Status == current`;
- do not infer Human Review Evidence or alter accepted/proposed validation paths.

- [x] **Step 4: Run ADR focused tests**

Run:

```bash
python3 -m unittest tests.test_adr_requirement_model_trace -v
python3 -m unittest \
  tests.test_optional_visual_communication_adapter.AdrVisualIntegrationTests -v
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
bash tests/validate-decision-design-requirement-landing.sh
```

Expected: valid optional pair passes both proposed and accepted structural validation when the pre-existing lifecycle evidence is correct; visual-only acceptance, new product meaning, stale source/render or unresolved references fail.

## Task 6: Onboarding representation and HTML-only prevention

**Files:**
- Modify: `references/onboarding-knowledge-base.md`
- Modify: `templates/onboarding-db/flow.md`
- Modify: `scripts/check-onboarding-core-flow-coverage.py`
- Modify: `tests/test_onboarding_core_flow_coverage.py`
- Modify: `tests/validate-onboarding-core-flow-completeness.sh`
- Modify: affected `examples/ai-meeting-minutes-backend/onboarding-db/03-flows/*.md`
- Modify: affected `tests/fixtures/onboarding-core-flow/**/*.md`
- Add fixtures under: `tests/fixtures/optional-visual-communication-adapter/onboarding-*`

- [x] **Step 1: Define source-vs-render ownership**

Keep Mermaid/ASCII as valid canonical embedded diagram sources. Permit Archify only as `archify-source-render` with a valid manifest row. Required Diagram IDs still need Flow Slice, narrative section and evidence trace; a polished render cannot replace any of them.

- [x] **Step 2: Add representation metadata and optional manifest**

Every new required Diagram definition uses:

```text
- Diagram ID: D-EXAMPLE
- Representation: embedded-mermaid | embedded-ascii | archify-source-render
- Covered Slice IDs: CF-EXAMPLE/S01
```

Add an optional `## Diagram Artifact Manifest` with the exact ten-column Onboarding table. Embedded representations do not create manifest rows. Archify representation requires exactly one matching row.

- [x] **Step 3: Extend coverage validation**

For each required Diagram ID:

- locate exactly one definition block in a flow document;
- `embedded-mermaid` requires a Mermaid fenced block in that definition section;
- `embedded-ascii` requires a text fenced block in that definition section;
- `archify-source-render` requires one manifest row, concrete evidence reference with code/config location, and a valid shared source/render pair rooted at the Onboarding DB;
- missing/unknown representation or HTML-only path fails;
- preserve existing Flow Slice, section, code evidence, Completeness Hard Gate and score ordering rules.

Update current examples and fixtures only by adding the representation that matches their existing fenced source. Do not convert existing diagrams to Archify merely to exercise the feature.

- [x] **Step 4: Run Onboarding tests**

Run:

```bash
python3 -m unittest tests.test_onboarding_core_flow_coverage -v
python3 -m unittest \
  tests.test_optional_visual_communication_adapter.OnboardingVisualIntegrationTests -v
bash tests/validate-onboarding-core-flow-completeness.sh
bash tests/validate-evidence-graph-ddd-onboarding.sh
```

Expected: current embedded examples pass; valid Archify pair passes; HTML-only, missing source, stale hash, missing evidence, missing representation and detached Diagram ID fail.

## Task 7: Stage behavior, Feature return path and Human Review summaries

**Files:**
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/human-review-summary.md`
- Test: `tests/validate-optional-visual-communication-adapter.sh`

- [x] **Step 1: Make Requirements Discussion the primary use case**

Add the Visual Trigger after evidence inspection and before high-cost textual explanation. The Agent must name the Review Question, recommend a diagram type, show the source boundary, and use the picture to invite correction. Human corrections update the current product draft; the Agent does not ask the human to author the design.

- [x] **Step 2: Add secondary stage rules**

- Brainstorm / Clarify: use a temporary visual only when it materially clarifies the bounded blocker.
- Feature Spec: visualize only the accepted Product Slice; any newly discovered product meaning returns to Requirements Discussion before continuing.
- Decision & Design: compare technical options, then write the chosen rationale/impact into the ADR and preserve its separate acceptance Gate.
- Onboarding: derive from code/evidence, use representation rules, preserve the existing two Human Gates.
- Review/presentation: derive from current accepted artifacts; a shareable render is not acceptance evidence by itself.

- [x] **Step 3: Update checklists and summaries**

Checklists must cover trigger decision, capability result, exact install authorization when applicable, Visual Scope, source binding, working-vs-durable boundary, validator evidence, fallback and owning-artifact rewrite. Human Review summaries show visuals as supporting evidence with `current | stale | absent/not-needed`; they do not create an extra approval status.

- [x] **Step 4: Run stage contract tests**

Run:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
bash tests/validate-chat-requirements-entry.sh
bash tests/validate-requirement-product-grill.sh
bash tests/validate-project-decisions-adr-lane.sh
```

Expected: requirements remain before ADR/Feature, new meaning returns upstream, and no visual grant satisfies another Human Gate.

## Task 8: Human docs, scenarios and changelog

**Files:**
- Modify: `references/validation-scenarios.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Test: `tests/validate-human-help-version-docs.sh`
- Test: `tests/validate-optional-visual-communication-adapter.sh`

- [x] **Step 1: Add semantic pressure scenarios**

Add scenarios for all twenty focused cases in Proposal section 17.1 and explicit mutations for:

- mandatory Archify;
- silent install;
- missing exact source/command/location disclosure;
- infinite scope reuse;
- HTML-only durable Requirement/ADR/Onboarding artifact;
- stale semantic/source/render hash;
- Feature-created product meaning;
- visual-created ADR acceptance;
- declined/failed install blocking progress;
- visual authorization widening into Git, release or paid/external actions.

Each scenario states signal, wrong behavior, required stop/fallback, owning artifact and independent Gate.

- [x] **Step 2: Add human-facing usage**

README gives a concise capability description and links the official upstream URL. Usage shows three conversations:

1. installed Archify + triggered Requirements visual;
2. unavailable Archify + exact installation disclosure + Human authorization + doctor + current Visual Scope;
3. Human decline or failed install + Mermaid/ASCII fallback.

The examples must explicitly say the resolved installation command depends on the current runtime and must be shown before execution; do not publish a fictional universal command.

- [x] **Step 3: Record the v1.5.0 change**

Under current v1.5.0, add one `Optional Visual Communication Adapter` subsection covering Requirements-first use, optional routing, authorized install, Visual Scope, source/render validation, legacy read compatibility and independent Gates. Do not change any version string.

- [x] **Step 4: Run docs tests**

Run:

```bash
bash tests/validate-human-help-version-docs.sh
bash tests/validate-optional-visual-communication-adapter.sh
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
```

Expected: all pass and current version remains 1.5.0 everywhere.

## Task 9: Focused GREEN and mutation pressure

**Files:**
- Modify: `docs/reports/agent-loop-v1.5.0-optional-visual-communication-adapter-focused-validation-2026-07-23.md`
- Read/execute: all files changed in Tasks 1–8

- [x] **Step 1: Run the complete focused suite**

Run:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
bash tests/validate-adaptive-requirement-product-definition.sh
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
bash tests/validate-decision-design-requirement-landing.sh
bash tests/validate-onboarding-core-flow-completeness.sh
bash tests/validate-evidence-graph-ddd-onboarding.sh
bash tests/validate-mandatory-helper-routing.sh
bash tests/validate-project-skill-discovery-guard.sh
python3 -m unittest tests.test_optional_visual_communication_adapter -v
python3 -m unittest tests.test_requirement_product_definition -v
python3 -m unittest tests.test_adr_requirement_model_trace -v
python3 -m unittest tests.test_onboarding_core_flow_coverage -v
```

Expected: every command exits 0.

- [x] **Step 2: Run isolated mutation copies**

Copy the current tree to a temporary directory excluding `.git`, then make one mutation at a time and run the smallest owning test. Every mutation listed in Task 8 must produce a non-zero result for the intended reason. Restore by deleting the temporary copy, never by mutating the real worktree back and forth.

- [x] **Step 3: Write the focused report**

Record RED command/output, GREEN commands/live counts, mutation table, compatibility result, macOS execution environment, Windows-defined evidence, changed files, residual risks and all actions not authorized. Do not present historical counts as current.

## Task 10: Full validation and semantic audit

**Files:**
- Create or update without overwriting prior evidence: `docs/reports/agent-loop-1.5.0-full-validation-2026-07-23.md`
- Read: `docs/maintenance/full-validation-method.md`

- [x] **Step 1: Run all executable tests**

Run:

```bash
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
for test_file in tests/*.rb; do ruby "$test_file"; done
```

Expected: every discovered test exits 0. Report live Shell/Python/Ruby counts separately.

- [x] **Step 2: Run mechanical validation**

Run:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json >/dev/null
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
python3 -m compileall -q scripts tests
git diff --check
```

Also run the repository Markdown fence balance check and remove only cache files created by this validation when they are positively identified as current-run outputs; never touch pre-existing unrelated cache ownership.

- [x] **Step 3: Perform six-domain semantic audit**

Explicitly pressure:

- Requirements Discussion → Standard Product Definition → visual convergence → Product Human Review → ADR → Feature Product Slice;
- simple Brief path with no visual;
- installed, unavailable, declined, authorized-install and install-failed Archify paths;
- one bounded Visual Scope with iterative corrections and each scope-expansion stop;
- product/ADR/onboarding authority conflicts and stale regeneration;
- legacy render-only Requirement reader;
- Project Skill priority over runtime Archify;
- Auto Mode and all independent Human Gates;
- Windows path/BOM/CRLF compatibility;
- no new canonical stage, root Stage Map row, default target directory or mandatory dependency.

Score all six domains using the maintenance method. Critical/High/Medium findings must be zero before recommending acceptance; otherwise return to RED with a regression test.

- [x] **Step 4: Write a current Chinese full-validation report**

Include branch, full SHA, dirty boundary, score, grade, per-domain findings, live test counts, RED/GREEN evidence, mutation results, compatibility, residual risk, and explicit statements that no install, commit, push, tag, release, publish or installed-skill sync occurred.

## Task 11: Final drift review and Human handoff

**Files:**
- Modify: `docs/proposal/v1.5.x/optional-visual-communication-adapter.md`
- Modify: `docs/proposal/v1.5.x/optional-visual-communication-adapter-implementation-plan.md`
- Read: all changed files and reports

- [x] **Step 1: Reconcile Proposal coverage**

Build a table mapping every Proposal acceptance criterion 1–18 to code/reference/template/test/report evidence. Any uncovered criterion returns to the owning Task; do not waive it in prose.

- [x] **Step 2: Inspect final workspace boundary**

Run:

```bash
git status --short --branch
git diff --stat
git diff --name-status
git diff --check
git ls-files --others --exclude-standard
```

Expected: every changed implementation path belongs to this plan; `.tmp/` and unrelated caches remain excluded; no target-project `.agent-loop/` artifact exists.

- [x] **Step 3: Update status without claiming Git actions**

Set Proposal and Plan to:

```text
Implementation and validation complete; waiting Human Review; no commit / push / tag / release / installed-skill sync
```

Do not mark released or installed.

- [x] **Step 4: Present one Human Review summary and stop**

Report conclusion, behavior impact, exact files, focused/full validation, compatibility, rollback boundary, residual risk and unperformed actions. Ask for review of the implementation. Commit remains a later exact-action Human Gate; push remains separate from commit.

## Task 12: Complete Human Docs And README Capability Map

**Files:**
- Create: `docs/assets/agent-loop-capability-map.workflow.json`
- Create: `docs/assets/agent-loop-capability-map.html`
- Create: `docs/assets/agent-loop-capability-map.svg`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/proposal/v1.5.x/optional-visual-communication-adapter.md`
- Modify: `docs/proposal/v1.5.x/optional-visual-communication-adapter-implementation-plan.md`

- [x] **Step 1: Author one complete, source-grounded capability inventory**

Derive the inventory from `SKILL.md`, `references/runtime.md`, `references/design.md`, and the matching capability references. Group every current formal capability under Project Understanding, Product Definition, Right-sized Delivery, Quality And Evidence, or Long-term Maintenance. Exclude proposals, reports, historical Hub experiments, and first-version exclusions.

- [x] **Step 2: Generate the Archify overview**

Use Archify `workflow` with Classic preset, static output, `showcase` quality, stable relationship IDs, bilingual English label / Chinese sublabel nodes, and at most five guided views. Keep one readable primary path and express supporting capabilities through lanes and cards rather than a dense all-to-all graph.

Run:

```bash
node ~/.codex/skills/archify/bin/archify.mjs validate workflow docs/assets/agent-loop-capability-map.workflow.json --json --quality showcase
node ~/.codex/skills/archify/bin/archify.mjs deliver workflow docs/assets/agent-loop-capability-map.workflow.json docs/assets/agent-loop-capability-map.html --json --quality showcase
node ~/.codex/skills/archify/bin/archify.mjs check docs/assets/agent-loop-capability-map.html
```

Expected: all commands exit 0; the delivery receipt records final HTML bytes and SHA-256. Export the canonical dual-theme SVG from that checked artifact without changing semantic topology.

- [x] **Step 3: Rewrite README by responsibility**

Keep README as the concise product overview:

1. positioning and current version;
2. embedded capability map plus interactive/source links;
3. full current Capability Matrix;
4. right-sized routing and Human Gate model;
5. concise artifact model;
6. install and quick start;
7. links to Usage, examples, published sources, and Archify.

Do not duplicate the full runtime stage order or turn README into a second Usage guide.

- [x] **Step 4: Rewrite Usage around human triggers and Agent autonomy**

Start with copy-ready prompts for:

```text
Use Agent Loop to take ownership of this project. Inspect current evidence, recommend one next action, and continue authorized work until verified completion; stop only at a real Human Gate.
Use Agent Loop to maintain this project autonomously. Diagnose drift, choose the smallest safe lane, verify changes, update project memory, and tell me the next gate.
Use Agent Loop to develop this accepted requirement. Run Design Readiness, build the Product Slice, and use Feature Auto-Loop after the required acceptance gates.
```

Then organize task-oriented sections for Project Entry, Requirements / Product Definition, Visual Communication, ADR, Lightweight Change, Feature, Bug, Operational Support, Onboarding, Project Skills, Branch / Archive / Memory maintenance, and Submit / Close. Every section states what the Agent owns, what artifact is produced, and where it must stop.

- [x] **Step 5: Reorganize the v1.5.0 changelog**

Keep older version sections byte-stable. Reorganize only v1.5.0 under distinct capability headings for Adaptive Requirement Product Definition, Optional Visual Communication, Agent Ownership / Root Guidance, and Lightweight Change. Preserve every implemented behavior claim and do not mix proposals or reports into runtime capability.

- [x] **Step 6: Validate content, visuals, and regression**

Run the focused human-doc and visual adapter tests, all shell/Python tests, YAML/JSON/Shell/Python/Markdown/diff checks, and the repository full-validation method because the working tree still contains the coordinated Optional Visual Communication change. Inspect both light and dark rendered pixels, make no more than two focused Archify correction rounds, and refresh the focused/full reports with current counts.

- [x] **Step 7: Stop at Human Review**

Report Archify installation result separately from repository changes. List the README capability coverage, Usage autonomy triggers, changelog organization, visual receipt, validation counts, rollback boundary, and residual risks. Do not commit, push, tag, release, publish, or sync installed Agent Loop without later explicit authorization.

## Self-Review

实施记录：计划中的 optional fixture directory 最终改为 `tempfile.TemporaryDirectory` 动态构造 source/render/ADR/Onboarding fixtures，避免长期保存重复生成物；覆盖范围未缩小。最终 focused 为 19/19 Python + 1 Shell PASS，full validation 为 41/41 Shell、277/277 Python 和全部静态检查 PASS。验证报告记录了 12 个 isolated mutation 反例。

### Proposal coverage

| Proposal requirement | Plan owner |
|---|---|
| Requirements-first visual convergence | Tasks 3, 4, 7 |
| installed Archify preferred when triggered | Task 3 |
| unavailable recommendation and upstream URL | Tasks 3, 8 |
| Human-authorized exact install and doctor | Task 3 |
| declined/failed non-blocking fallback | Tasks 3, 7, 8 |
| bounded multi-round Visual Scope Grant | Tasks 3, 4 |
| source/stage/type/durable/external scope expansion | Tasks 3, 4, 8 |
| semantic authority → source → render | Tasks 2, 4, 5, 6 |
| Product, ADR and Onboarding ownership | Tasks 4, 5, 6 |
| Feature new-meaning return | Tasks 7, 14 |
| HTML-only rejection for new durable artifacts | Tasks 2, 4, 6 |
| legacy Requirement visual compatibility | Task 4 |
| Project Skill precedence | Tasks 3, 9, 10 |
| independent Human Gates | Tasks 3, 5, 7, 10 |
| no new stage/root row/version/install/vendor | Tasks 0, 3, 8, 10 |
| focused RED/GREEN and mutations | Tasks 1, 9 |
| full validation | Task 10 |
| Human Review stop before Git | Task 11 |
| Archify-first recommendation before Mermaid fallback | Task 13 |

## Task 13: Archify-first recommendation before Mermaid fallback

**Files:**
- Modify: `docs/proposal/v1.5.x/optional-visual-communication-adapter.md`
- Modify: `tests/validate-optional-visual-communication-adapter.sh`
- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/skill-routing.md`
- Modify: `references/product-definition.md`
- Modify: `references/onboarding-knowledge-base.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/validation-scenarios.md`
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Refresh: focused/full validation reports owned by this Proposal

- [x] **Step 1: Add a focused RED contract for the approved priority**

Extend `tests/validate-optional-visual-communication-adapter.sh` to require:

```text
matching active project-local visual skill
→ installed Archify
→ recommend Archify before Mermaid / table / ASCII fallback when it would materially improve review
```

Also require runtime and human docs to forbid offering Mermaid first merely because Archify is absent, and require the validation scenarios to cover this mutation.

- [x] **Step 2: Run the focused contract and preserve the real RED**

Run:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
```

Expected: FAIL on the new Archify-first recommendation anchor before runtime sources are changed.

- [x] **Step 3: Coordinate GREEN across authoritative and derived surfaces**

Keep Project Skill Discovery Guard first. When no matching active project-local visual skill exists:

```text
installed Archify
→ if absent and materially useful, exact Archify recommendation / Installation Authorization
→ Mermaid / table / ASCII fallback only when not justified, declined, unsupported, unavailable, or failed
```

Do not make Archify mandatory, do not remove fallback, and do not merge Installation Authorization with Visual Scope Grant or any existing Product/ADR/Onboarding/Git gate.

- [x] **Step 4: Run focused GREEN and affected regression tests**

Run:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
python3 -m unittest tests.test_optional_visual_communication_adapter -v
```

Expected: PASS with the priority contract, source/render validation, legacy reader compatibility, and independent gates unchanged.

- [x] **Step 5: Run full validation and refresh reports**

Follow `docs/maintenance/full-validation-method.md`, rerun all `tests/*.sh`, all Python tests, YAML, JSON, Shell, Ruby, Markdown-fence checks, and `git diff --check`. Refresh the focused/full reports with live commands and counts; do not reuse the earlier totals.

- [x] **Step 6: Stop at Human Review**

Report the RED/GREEN evidence, changed surfaces, full-validation totals, unchanged version, remaining risks, dirty boundary, and explicit no-commit/no-push/no-tag/no-release status.

## Task 14: Feature Spec visual boundary follow-up

**Files:**
- Modify: `tests/validate-optional-visual-communication-adapter.sh`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/external-skill-adapters.md`
- Modify: `references/stage-guides.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/validation-scenarios.md`
- Modify: `CHANGELOG.md`
- Refresh: `docs/reports/optional-visual-communication-adapter-feature-validation-2026-07-23.1.md`

- [x] **Step 1: Add the focused RED contract**

Require the Feature Spec stage to state all three invariants:

```text
Feature Spec visuals explain only the accepted Product Slice, feature responsibility, or feature-local implementation and acceptance path.
Accepted feature-local clarification is rewritten into spec.md.
Any new product meaning stops Feature Spec and returns to Requirements Discussion.
```

Require the adapter applicability text, Feature Spec checklist, and one validation scenario named `Feature Spec Visual Cannot Create Product Meaning`.

- [x] **Step 2: Run the focused contract and capture RED**

Run:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
```

Expected: FAIL because the Feature Spec visual-specific stage rule does not yet exist.

- [x] **Step 3: Coordinate the minimum GREEN**

Add Feature Spec to the Optional Visual Communication stage applicability without creating a new stage or artifact. Keep Requirement `product.md` as product authority and Feature `spec.md` as the accepted Product Slice owner. A visual correction that changes product meaning returns to Requirements Discussion; a correction that only clarifies the already accepted slice is rewritten into `spec.md`.

- [x] **Step 4: Run focused and affected regressions**

Run:

```bash
bash tests/validate-optional-visual-communication-adapter.sh
python3 -m unittest tests.test_optional_visual_communication_adapter -v
bash tests/validate-adaptive-requirement-product-definition.sh
```

Expected: PASS with Product Review, ADR, Onboarding, Feature start, Git, and fallback gates unchanged.

- [x] **Step 5: Refresh the single-feature score, full validation, and mechanical checks**

Rerun the feature-scoped test boundary, every `tests/*.sh`, all Python tests, YAML/JSON/Shell/Markdown-fence checks, and `git diff --check`. Refresh the current single-feature and full-validation reports from actual evidence because Feature Spec helper routing is a coordinated workflow invariant.

- [x] **Step 6: Stop at Human Review**

Report the resolved Medium, remaining Low findings, updated score, exact validation counts, and explicit no-commit/no-push status.

### Type consistency

- Adapter name is always `Optional Visual Communication Adapter`.
- Runtime trigger is always response-local `Visual Trigger`.
- Iteration authorization is always `Visual Scope Grant`.
- External mutation gate is always `Installation Authorization`.
- New durable contract marker is always `source-render-v1`.
- Shared function is always `validate_durable_visual` returning `DurableVisualArtifact`.
- Archify types are always `architecture | workflow | sequence | dataflow | lifecycle`.
- Onboarding representations are always `embedded-mermaid | embedded-ascii | archify-source-render`.
- Product authority remains Requirement `product.md`; technical authority remains accepted ADR.

### Scope check

This is one coordinated capability rather than independent products: routing, Product, ADR and Onboarding must share the same authorization and source/render invariants. They therefore remain in one plan and one full-validation cycle. No UI prototype, E2E Skill, Product Workbench, Archify vendor integration or installer implementation is included.

## Execution Handoff

After Human Review, use one of these paths:

1. **Inline execution:** use `executing-plans` in the current session, complete Tasks 0–11 in order, and stop at Human Review.
2. **Separate development Agent:** give the Agent this Plan and Proposal, require it to use `executing-plans`, forbid Subagent dispatch unless separately authorized, and require the same Human Review stop.

Neither path is authorized by this document alone. The Human must explicitly say to begin implementation.
