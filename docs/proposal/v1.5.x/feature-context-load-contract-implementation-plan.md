# Feature Context Snapshot And Load Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every Feature execution stage start from a freshness-checked local product context while keeping Requirement `product.md` and accepted ADRs authoritative.

**Architecture:** Add a read-only Python 3.10+ checker that resolves project-root-relative Requirement and ADR paths from Feature `spec.md`, verifies authority and SHA-256 evidence, and returns `current`, `refresh-required`, or `blocked`. Store the default derived Snapshot inside `spec.md`, allow an optional expanded `context.md` only for complex Features, and make Runtime/Stage guidance require the same load contract for Task, Test, Plan, Resume, Execute, Handoff, Verify, Review, Drift, and Close.

**Tech Stack:** Markdown contracts and templates, Python 3.10+ standard library, `unittest`, POSIX shell contract tests, existing Agent Loop checker support.

**Authority:** `docs/proposal/v1.5.x/feature-context-load-contract.md`

**Execution boundary:** Work in the current dedicated `v1.5.1` branch. Do not create/switch a branch or worktree, commit, push, tag, release, publish, or run the mandatory full validation without the corresponding Human Gate. Preserve unrelated untracked files and generated `__pycache__` directories.

---

## File Map

### New files

- `scripts/check-feature-context.py` — read-only Feature Context Snapshot freshness checker.
- `tests/test_feature_context.py` — executable checker behavior and adversarial coverage.
- `tests/fixtures/feature-context/current/.agent-loop/requirements/2026-07-25-example/README.md` — accepted Requirement authority fixture.
- `tests/fixtures/feature-context/current/.agent-loop/requirements/2026-07-25-example/product.md` — confirmed Product Definition fixture.
- `tests/fixtures/feature-context/current/.agent-loop/decisions/0001-example.md` — accepted current ADR fixture.
- `tests/fixtures/feature-context/current/.agent-loop/features/2026-07-25-example/spec.md` — current Snapshot and Product Slice fixture.
- `tests/validate-feature-context-load-contract.sh` — cross-reference and workflow contract regression test.
- `templates/feature-context.md` — optional expanded Snapshot template for complex Features.

### Modified operational files

- `SKILL.md` — package map, execution defaults, and context-loading invariant.
- `references/runtime.md` — Inspection Order, Auto Mode stop, Resume/re-entry, and stage transition contract.
- `references/design.md` — Feature Context Snapshot definition and authority invariant.
- `references/product-definition.md` — downstream Snapshot handoff.
- `references/stage-guides.md` — Feature Spec, Checklist, Work Breakdown, Test Design, Technical Design, Plan, Analyze, Execute, Verify, Review, Drift, and Close behavior.
- `references/artifact-rules.md` — Snapshot/context ownership and drift rules.
- `references/implementation-planning.md` — Task/Test/Plan derivation from current Snapshot.
- `references/complex-artifacts.md` — optional `context.md` trigger and index behavior.
- `references/workflow-checklists.md` — operator checklists for all dependent stages.
- `references/project-guidance.md` — downstream root guidance projection.
- `templates/root-AGENTS.md` — concise startup reminder without adding a stage.
- `templates/spec.md` — default Snapshot section.
- `references/document-templates.md` — inline template parity.
- `references/validation-scenarios.md` — pressure scenarios from the Proposal.

### Modified validation and human-facing files

- `tests/test_python_checker_contract.py` — register the new standard-library checker.
- `README.md` — explain freshness-checked Feature execution context.
- `Usage.md` — explain normal fast path and refresh/block behavior.
- `CHANGELOG.md` — record the unreleased v1.5.x behavior change without bumping version.

## Checker Contract

Command:

```bash
python3 scripts/check-feature-context.py \
  --project-root <target-project-root> \
  <feature-spec-path>
```

Windows equivalent:

```text
py -3 scripts\check-feature-context.py --project-root <target-project-root> <feature-spec-path>
```

Exit contract:

| Exit | Output prefix | Meaning |
|---:|---|---|
| `0` | `CURRENT:` | Snapshot authority, paths, digests, Product Slice references, and ADR compatibility are current |
| `3` | `REFRESH_REQUIRED:` | authority is resolvable but local derived context is missing, stale, or incomplete |
| `1` | `BLOCKED:` | authority is unsafe, ambiguous, outside root, unconfirmed, incompatible, or semantically unresolvable |
| `2` | argparse / Python capability error | command or runtime usage is invalid |

The checker performs no writes.

---

### Task 1: Add RED Contract Tests And Current Fixture

**Files:**
- Create: `tests/fixtures/feature-context/current/.agent-loop/requirements/2026-07-25-example/README.md`
- Create: `tests/fixtures/feature-context/current/.agent-loop/requirements/2026-07-25-example/product.md`
- Create: `tests/fixtures/feature-context/current/.agent-loop/decisions/0001-example.md`
- Create: `tests/fixtures/feature-context/current/.agent-loop/features/2026-07-25-example/spec.md`
- Create: `tests/test_feature_context.py`
- Create: `tests/validate-feature-context-load-contract.sh`

- [x] **Step 1: Create one realistic accepted Requirement/Product/ADR/Feature fixture**

Use project-root-relative paths in the Feature fixture:

```markdown
## Feature Context Snapshot

Requirement Set: .agent-loop/requirements/2026-07-25-example/README.md
Requirement Lifecycle: accepted
Resolved Product Source: .agent-loop/requirements/2026-07-25-example/product.md
Product Definition Profile: standard
Product Review: confirmed
Product Source SHA-256: <real lowercase SHA-256 after CRLF / lone CR -> LF canonicalization>
Applicable Decisions: .agent-loop/decisions/0001-example.md
Decision Source SHA-256: .agent-loop/decisions/0001-example.md=<real lowercase canonical-text SHA-256>
Product Slice References: C-ACCOUNT / FLOW-RECHARGE / STATE-RECHARGE / EX-PAYMENT-UNKNOWN / product.md#confirmed-credit
Verified At: 2026-07-25T12:00:00+08:00
Freshness: current

### Product Outcome

An authorized operator can complete one observable recharge without duplicate credit.

### Actors And Core Journey

The operator starts a recharge, observes pending/unknown/success/failure, and receives one confirmed credit.

### Applicable Product Rules And Invariants

`product.md#confirmed-credit` permits credit only after confirmed success.

### Applicable States, Exceptions, And Recovery

`STATE-RECHARGE` and `EX-PAYMENT-UNKNOWN` keep unknown visible and recoverable.

### Feature Boundary And Acceptance Context

This Feature implements the accepted recharge slice and excludes provider migration.
```

The fixture Requirement README must use `Status: accepted` and one `Effective Product Definition` section with `Source: product.md`, `Profile: standard`, and `Product Review: confirmed`. The product fixture must include the stable IDs and `### Confirmed Credit` anchor cited by the Product Slice. The ADR fixture must use `Status: accepted` and `Upstream Compatibility: current`.

- [x] **Step 2: Write CLI tests before the checker exists**

Create `tests/test_feature_context.py` with these concrete cases:

```python
from __future__ import annotations

import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


SCRIPT = "scripts/check-feature-context.py"
FIXTURE = ROOT / "tests/fixtures/feature-context/current"
FEATURE = ".agent-loop/features/2026-07-25-example/spec.md"


class FeatureContextCheckerTests(unittest.TestCase):
    def run_project(self, mutate=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        shutil.copytree(FIXTURE / ".agent-loop", root / ".agent-loop")
        if mutate:
            mutate(root)
        return run_checker(
            SCRIPT,
            "--project-root",
            str(root),
            str(root / FEATURE),
        )

    def test_current_snapshot_passes(self):
        result = self.run_project()
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertIn("CURRENT:", result.stdout)

    def test_changed_product_digest_requires_refresh(self):
        def mutate(root):
            product = root / ".agent-loop/requirements/2026-07-25-example/product.md"
            product.write_text(
                product.read_text(encoding="utf-8") + "\nEditorial change.\n",
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 3, combined_output(result))
        self.assertIn("REFRESH_REQUIRED:", combined_output(result))

    def test_missing_snapshot_requires_refresh(self):
        def mutate(root):
            spec = root / FEATURE
            text = spec.read_text(encoding="utf-8")
            start = text.index("## Feature Context Snapshot")
            end = text.index("## Product Slice")
            spec.write_text(text[:start] + text[end:], encoding="utf-8")

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 3, combined_output(result))

    def test_unconfirmed_product_blocks(self):
        def mutate(root):
            readme = root / ".agent-loop/requirements/2026-07-25-example/README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "Product Review: confirmed", "Product Review: pending"
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))
        self.assertIn("BLOCKED:", combined_output(result))

    def test_unknown_product_slice_anchor_blocks(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "product.md#confirmed-credit", "product.md#missing-rule"
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_review_required_adr_blocks(self):
        def mutate(root):
            decision = root / ".agent-loop/decisions/0001-example.md"
            decision.write_text(
                decision.read_text(encoding="utf-8").replace(
                    "Upstream Compatibility: current",
                    "Upstream Compatibility: review-required",
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))

    def test_project_root_escape_blocks(self):
        def mutate(root):
            spec = root / FEATURE
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    ".agent-loop/requirements/2026-07-25-example/README.md",
                    "../outside/README.md",
                ),
                encoding="utf-8",
            )

        result = self.run_project(mutate)
        self.assertEqual(result.returncode, 1, combined_output(result))


if __name__ == "__main__":
    unittest.main()
```

Add further tests in the same file for redirected Effective Product Definition, missing required Snapshot fields, invalid Requirement lifecycle, changed ADR digest, missing ADR, Product Slice unknown ID, CRLF/BOM input, Feature-relative Requirement path rejection, and proof that the checker leaves every fixture byte unchanged.

- [x] **Step 3: Write the shell contract RED test**

`tests/validate-feature-context-load-contract.sh` must use existing `assert_contains`, `assert_not_contains`, and `assert_file_exists` patterns and assert:

```text
Feature Context Snapshot
Freshness: current | refresh-required | blocked
scripts/check-feature-context.py
Work Breakdown
Test Design
Plan Gate / Plan
Resume
Subagent Handoff
Auto Mode cannot continue
project-root-relative
```

It must assert these across the owning runtime/design/stage/template/checklist surfaces, not only the Proposal.

- [x] **Step 4: Run RED and preserve the expected failure**

Run:

```bash
python3 -m unittest tests.test_feature_context -v
bash tests/validate-feature-context-load-contract.sh
```

Expected:

```text
FAIL because scripts/check-feature-context.py and runtime/template contract text do not yet exist.
```

Record the exact RED output in the implementation handoff; do not weaken the tests.

### Task 2: Implement The Read-Only Feature Context Checker

**Files:**
- Create: `scripts/check-feature-context.py`
- Modify: `tests/test_python_checker_contract.py`
- Test: `tests/test_feature_context.py`

- [x] **Step 1: Implement the CLI and explicit result model**

Use:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from checker_support import CheckFailure, optional_section, read_text, require_supported_python, table
from requirement_product_support import (
    CONCEPT_ID_PATTERN,
    MODEL_ID_PATTERN,
    ProductDefinitionError,
    normalized,
    resolve_effective_product_definition,
)


CURRENT = 0
BLOCKED = 1
REFRESH_REQUIRED = 3
COMPATIBLE_REQUIREMENT_STATUS = {
    "accepted",
    "in-progress",
    "partially-implemented",
    "implemented",
}


@dataclass(frozen=True)
class ContextResult:
    status: str
    reasons: tuple[str, ...]

    @property
    def exit_code(self) -> int:
        return {
            "current": CURRENT,
            "refresh-required": REFRESH_REQUIRED,
            "blocked": BLOCKED,
        }[self.status]
```

Use `configure_utf8_stdio()` from `checker_support.py`, call `require_supported_python()`, and accept exactly `--project-root` plus one Feature spec path.

- [x] **Step 2: Add local field, path, digest, and anchor helpers**

Implement:

```python
FIELD = re.compile(r"(?mi)^\\s*(?:-\\s*)?{name}\\s*:\\s*(.*?)\\s*$")


def field(text: str, name: str) -> str | None:
    match = re.search(
        rf"(?mi)^\\s*(?:-\\s*)?{re.escape(name)}\\s*:\\s*(.*?)\\s*$",
        text,
    )
    return match.group(1).strip() if match else None


def project_path(project_root: Path, value: str) -> Path:
    cleaned = normalized(value).replace("\\", "/")
    candidate = Path(cleaned)
    if candidate.is_absolute():
        raise ValueError(f"path must be project-root-relative: {value}")
    resolved = (project_root / candidate).resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError as error:
        raise ValueError(f"path escapes project root: {value}") from error
    return resolved


def compatible_text_digests(path: Path) -> frozenset[str]:
    raw = path.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    crlf = canonical.replace(b"\n", b"\r\n")
    return frozenset(
        hashlib.sha256(content).hexdigest()
        for content in (raw, canonical, crlf)
    )


def heading_anchors(content: str) -> set[str]:
    values = re.findall(r"^#{2,3}\\s+(.+?)\\s*$", content, re.MULTILINE)
    anchors = set()
    for value in values:
        cleaned = re.sub(r"[^a-z0-9 -]", "", value.lower())
        anchors.add(re.sub(r"[ -]+", "-", cleaned).strip("-"))
    return anchors
```

Reject project-root-relative paths that escape the root. Require Requirement, product, and ADR paths to remain inside the unique accepted real-directory `.agent-loop/` or legacy `agent-loop/` memory root containing the Feature; root files, root symlinks, and dual roots fail closed. Validate `Verified At` as a timezone-aware ISO-8601 timestamp.

- [x] **Step 3: Resolve authority before comparing the cache**

Implement this order:

```text
locate Snapshot section
-> if absent and Feature Product Requirement Source is resolvable: refresh-required
-> resolve Requirement Set README from Snapshot
-> verify README lifecycle is compatible
-> resolve one Effective Product Definition through requirement_product_support
-> verify new Product Review is confirmed
-> verify resolved product stays in the same Requirement Set and accepted memory root
-> validate Product Slice IDs and anchors against the resolved source
-> resolve every Snapshot ADR path, accepted Status, and current Upstream Compatibility
-> only then compare recorded path/digest/profile/review/decision evidence
```

Authority failures return `blocked`. A valid authority with a missing/incomplete Snapshot or mismatched path/digest returns `refresh-required`.

- [x] **Step 4: Validate Product Slice and ADR evidence**

For Product Slice:

```python
rows = table(spec_text, "Product Slice")
known_ids = set(source.concept_ids) | set(source.model_ids)
known_anchors = heading_anchors(source.content)
for row in rows:
    reference = row.get("Source Section / Model ID", "")
    ids = set(CONCEPT_ID_PATTERN.findall(reference))
    ids.update(MODEL_ID_PATTERN.findall(reference))
    anchors = set(re.findall(r"product\\.md#([a-z0-9-]+)", reference))
    if ids - known_ids:
        raise ValueError("Product Slice contains unknown source IDs")
    if anchors - known_anchors:
        raise ValueError("Product Slice contains unknown source anchors")
```

For decisions, accept `none` or a comma-separated list of project-root-relative Markdown paths. `Decision Source SHA-256` accepts `none` or semicolon-separated `path=digest` pairs. Reject duplicate paths, missing files, non-`accepted` status, missing/non-current `Upstream Compatibility`, malformed digests, root escape, recorded decision paths that differ from `Applicable Decisions`, or a Snapshot decision set that conflicts with Product Requirement Source.

- [x] **Step 5: Keep classification deterministic**

Aggregate reasons and choose precedence:

```python
if blocked_reasons:
    result = ContextResult("blocked", tuple(sorted(set(blocked_reasons))))
elif refresh_reasons:
    result = ContextResult(
        "refresh-required", tuple(sorted(set(refresh_reasons)))
    )
else:
    result = ContextResult("current", ("authority and digests match",))
```

Print:

```python
prefix = {
    "current": "CURRENT",
    "refresh-required": "REFRESH_REQUIRED",
    "blocked": "BLOCKED",
}[result.status]
print(f"{prefix}: {'; '.join(result.reasons)}")
return result.exit_code
```

Do not write Snapshot freshness or digests from the checker.

- [x] **Step 6: Register the checker contract**

Add `scripts/check-feature-context.py` to the canonical Python checker list in `tests/test_python_checker_contract.py`. Assert it:

- requires Python 3.10+;
- uses standard library and repository-local modules only;
- supports UTF-8 deterministic output;
- has no Ruby compatibility entry;
- contains no write operation against target artifacts.

- [x] **Step 7: Run GREEN and refactor without widening behavior**

Run:

```bash
python3 -m unittest tests.test_feature_context -v
python3 -m unittest tests.test_python_checker_contract -v
```

Expected:

```text
All Feature Context and Python checker contract tests pass.
```

Refactor only duplicated parsing or error assembly. Rerun both commands after refactor.

### Task 3: Add Snapshot And Optional Complex Context Artifacts

**Files:**
- Modify: `templates/spec.md`
- Create: `templates/feature-context.md`
- Modify: `references/document-templates.md`
- Modify: `references/artifact-rules.md`
- Modify: `references/complex-artifacts.md`
- Modify: `references/product-definition.md`
- Test: `tests/validate-feature-context-load-contract.sh`

- [x] **Step 1: Add the default Snapshot to `templates/spec.md`**

Insert after `## Product Requirement Source` and before `## Product Slice`:

```markdown
## Feature Context Snapshot

Requirement Set: .agent-loop/requirements/<requirement-id>/README.md
Requirement Lifecycle: accepted | in-progress | partially-implemented | implemented
Resolved Product Source: .agent-loop/requirements/<requirement-id>/product.md
Product Definition Profile: brief | standard | legacy
Product Review: confirmed | accepted | concept-foundation-not-needed
Product Source SHA-256:
Applicable Decisions: none | .agent-loop/decisions/<decision>.md
Decision Source SHA-256: none | .agent-loop/decisions/<decision>.md=<sha256>
Product Slice References:
Verified At:
Freshness: current | refresh-required | blocked

### Product Outcome

### Actors And Core Journey

### Applicable Product Rules And Invariants

### Applicable States, Exceptions, And Recovery

### Feature Boundary And Acceptance Context
```

Explain immediately below it that the Snapshot is derived, README resolves authority, paths are project-root-relative, the checker is read-only, and `## Product Slice` remains the responsibility/coverage table.

- [x] **Step 2: Add the optional expanded `context.md` template**

`templates/feature-context.md` must contain the same source identity, digest, and Freshness fields plus expanded sections. It must say:

```text
Derived Context: yes
Authority: Requirement README -> Effective Product Definition -> accepted ADRs
Independent Product Truth: no
```

It must not add lifecycle, approval, task, test, plan, code-fact, or execution authority.

- [x] **Step 3: Align artifact ownership and complexity rules**

Update:

- `references/artifact-rules.md`: Snapshot is derived execution context inside `spec.md`; optional `context.md` is expanded derived context; neither owns product meaning.
- `references/complex-artifacts.md`: do not create `context.md` for ordinary Features; create it only when the Snapshot makes `spec.md` no longer locally understandable, using the existing Complex Artifact Human Gate; keep exact source/digest parity.
- `references/product-definition.md`: downstream handoff now includes the Snapshot fields and freshness checker before Product Slice reliance.
- `references/document-templates.md`: mirror the updated Feature Spec and optional context template.

- [x] **Step 4: Run the artifact-focused contract test**

Run:

```bash
bash tests/validate-feature-context-load-contract.sh
```

Expected: it still fails only on runtime/stage surfaces not yet updated; template/artifact assertions pass.

### Task 4: Make Feature Context Loading A Runtime Invariant

**Files:**
- Modify: `SKILL.md`
- Modify: `references/runtime.md`
- Modify: `references/design.md`
- Modify: `references/stage-guides.md`
- Modify: `references/implementation-planning.md`
- Modify: `references/workflow-checklists.md`
- Modify: `references/project-guidance.md`
- Modify: `templates/root-AGENTS.md`
- Modify: `references/validation-scenarios.md`
- Test: `tests/validate-feature-context-load-contract.sh`

- [x] **Step 1: Update design authority without adding a stage**

Add a definition and invariant to `references/design.md`:

```text
Feature Context Snapshot is a derived execution cache inside Feature spec.md by default.
Requirement README and Effective Product Definition remain authoritative.
Freshness is current | refresh-required | blocked and is not lifecycle.
```

Add the authority chain:

```text
Requirement README
-> Effective Product Definition
-> accepted ADRs
-> Feature Context Snapshot
-> Product Slice
-> Tasks / Tests / Plan
-> Execute / Verify / Review
```

- [x] **Step 2: Repair Runtime Inspection Order and re-entry**

In `references/runtime.md`, change Feature inspection from “read all Feature ledgers first” to:

```text
read spec.md as bootstrap
-> run Feature Context freshness check
-> if current, load remaining stage-relevant ledgers
-> if refresh-required, run semantic refresh before downstream generation
-> if blocked, route to the owning Requirement / Decision / Feature Definition / Recovery gate
```

Require this after context compaction, Resume, controller re-entry, long-running uncertainty, source change, and before Plan/Execute reliance. Add `refresh-required | blocked` to Auto Mode stop conditions. Do not add a canonical stage or Human Gate.

- [x] **Step 3: Update every dependent stage**

In `references/stage-guides.md`, require:

- Feature Spec creates the Snapshot from one current source.
- Requirement Checklist checks Snapshot completeness.
- Work Breakdown loads current Snapshot before creating Tasks.
- Test Design traces roles, states, rules, exceptions, recovery, and acceptance from current Snapshot.
- Technical Design separates accepted product meaning, ADR meaning, and code facts.
- Plan Gate rejects stale Snapshot and maps Plan to Product Slice/invariants.
- Analyze Consistency reruns freshness and traces Product Slice through Tasks/Tests/Plan.
- Execute rejects non-current context.
- Subagent Handoff records Feature path, Snapshot digest/freshness, Product Slice IDs, ADRs, and expiry on digest change.
- Verify/Review/Drift/Close recheck source freshness and report code/product disagreement as drift.

- [x] **Step 4: Update construction planning and workflow checklists**

In `references/implementation-planning.md`, state:

```text
Task/Test/Plan derive from:
current Feature Context Snapshot
+ current Product Slice
+ applicable accepted ADRs
+ relevant code facts
```

Require each Task/Test/Plan mapping defined in Proposal section 14.

Mirror executable checks in `references/workflow-checklists.md`, including the exact checker command and exit behavior.

- [x] **Step 5: Project the rule into startup guidance**

Keep `templates/root-AGENTS.md` concise. Add one sentence to the complete workflow/gate section:

```text
Before Task/Test/Plan/Execute/Resume relies on a Feature, load its Feature Context Snapshot and require the Requirement/ADR freshness check to be current.
```

Because this changes downstream managed guidance, refresh all 13 managed blocks to the next full root block revision and align the root block regression expectations without changing the Skill version.

Align `references/project-guidance.md`. Do not add Feature Context as a new Gateway, stage, or standalone Human Gate.

- [x] **Step 6: Add pressure scenarios**

Add all Proposal section 21 cases to `references/validation-scenarios.md`, with explicit expected routes and forbidden behavior. Include:

- unchanged fast path;
- product/ADR digest refresh;
- scope-changing block;
- missing/ambiguous source block;
- context compaction Resume;
- Subagent expiry;
- archived/rehydrated behavior;
- code drift not overwriting product truth;
- Auto Mode stop.

- [x] **Step 7: Run runtime contract GREEN**

Run:

```bash
bash tests/validate-feature-context-load-contract.sh
bash tests/validate-root-agents-block-refresh.sh
python3 -m unittest tests.test_root_agents_blocks -v
```

Expected: all pass.

### Task 5: Complete Human Docs, Focused Validation, And Review Boundary

**Files:**
- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/proposal/v1.5.x/feature-context-load-contract-implementation-plan.md`
- Test: all focused commands below

- [x] **Step 1: Update human-facing documentation**

Add concise human wording:

```text
Feature work now starts from a local Feature Context Snapshot.
Agent Loop checks the real Requirement product.md and applicable ADR digests first.
Unchanged sources use the fast path; changed sources are refreshed before work continues.
```

Usage must explain that humans do not need to manually identify or reopen `product.md`; the Agent resolves it from Feature `spec.md`. Do not expose checker internals as required human knowledge.

- [x] **Step 2: Record the unreleased behavior change**

Under the current v1.5.x in-progress/unreleased CHANGELOG section, record:

- Feature-local derived Snapshot;
- Requirement README authority resolution;
- freshness checker and three outcomes;
- mandatory Task/Test/Plan/Resume/Execute/Handoff integration;
- no new Human Gate and no Feature-level product truth.

Do not change any version-bearing file.

- [x] **Step 3: Run focused executable validation**

Run:

```bash
python3 -m unittest tests.test_feature_context -v
python3 -m unittest tests.test_python_checker_contract -v
bash tests/validate-feature-context-load-contract.sh
bash tests/validate-adaptive-requirement-product-definition.sh
bash tests/validate-concept-foundation-requirement-modeling.sh
bash tests/validate-decision-design-requirement-landing.sh
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
bash tests/validate-root-agents-block-refresh.sh
python3 -m unittest tests.test_requirement_product_definition -v
python3 -m unittest tests.test_adr_requirement_model_trace -v
python3 -m unittest tests.test_root_agents_blocks -v
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
git diff --check
```

Expected: all focused commands pass with no warnings or unexpected output.

- [x] **Step 4: Perform semantic self-review**

Confirm:

- no path is Feature-relative;
- archive/rehydrate cannot invalidate source paths;
- `current` never relies on an unconfirmed or incompatible source;
- `refresh-required` never silently proceeds;
- `blocked` routes to an existing owning Gate;
- checker performs no writes;
- Feature Snapshot/context never becomes product authority;
- no new stage, lifecycle, Auto Mode, or Human Gate was introduced;
- existing legacy Feature `product.md` compatibility remains;
- root guidance remains concise;
- no unrelated untracked/generated files were modified.

- [x] **Step 5: Stop at the full-validation boundary**

This is a coordinated workflow change. Do not claim final completion and do not run full validation automatically. Report:

```text
Implementation and focused validation are complete.
Mandatory full Agent Loop validation remains required before final acceptance.
No commit, push, tag, release, publish, branch, or worktree action was performed.
```

Wait for the human's explicit full-validation instruction. Commit and push remain later independent Human Gates.
