# Cross-Platform Python Script Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task after Plan Human Review. Use `test-driven-development` for every port, `verification-before-completion` before completion claims, and `requesting-code-review` before handoff. Subagent execution is not authorized by this plan.

**Goal:** Replace the four current Bash/Ruby checker implementations with Python 3.10+ standard-library canonical implementations that preserve existing safety behavior and run natively on Windows and macOS.

**Execution Status:** Implemented and verified on macOS and Windows. Commit `7253461` passed all four GitHub Actions jobs (`macos-latest` / `windows-latest` × Python 3.10 / 3.x) on 2026-07-14: <https://github.com/Shadow-linux/agent-loop/actions/runs/29320389912>. The v1.3.0 Release Human Gate was approved on 2026-07-14; the exact release-evidence commit must pass the same CI matrix before creating `stable-v1.3.0`.

**Architecture:** A small `scripts/checker_support.py` module owns deterministic UTF-8 Markdown parsing, table parsing, path confinement, and CLI failure semantics. Four standalone `.py` entrypoints own their existing checker-specific rules. Existing `.sh` / `.rb` paths remain one-cycle compatibility launchers only; cross-platform `unittest` suites invoke the canonical scripts with `sys.executable` and run unchanged fixtures on Windows and macOS.

**Tech Stack:** Python 3.10+ standard library (`argparse`, `dataclasses`, `datetime`, `hashlib`, `json`, `pathlib`, `re`, `shutil`, `subprocess`, `tempfile`, `unittest`), existing Markdown fixtures, optional GitHub Actions matrix for `macos-latest` and `windows-latest`.

---

## Execution Boundary

This plan implements only the approved `Cross-Platform Python Script Runtime` proposal.

Included:

- port four checker entrypoints to canonical Python;
- preserve valid/invalid behavior, exit-code classes, path confinement, and read-only guarantees;
- add Windows/macOS-native Python tests;
- convert old Bash/Ruby entrypoints to compatibility launchers after parity passes;
- update current authoritative script references and current-version changelog;
- save a focused validation report and run the repository-required full validation.

Excluded:

- Feature Monthly Compaction implementation;
- rewriting all `tests/*.sh` as Python;
- rewriting historical proposals or reports;
- generic YAML parsing;
- third-party Python dependencies;
- version bump, commit, push, tag, PR, release, or publish without a later explicit Human Gate.

## Stage Helper Resolution

```text
Stage: Plan Gate / Plan If Needed
Canonical Candidate: superpowers:writing-plans
Canonical Result: unavailable in current runtime
Alias Candidate: writing-plans
Resolved Helper: writing-plans
Status: loaded
Load Evidence: /Users/shaodowyd/.codex/skills/writing-plans/SKILL.md read completely on 2026-07-13
Fallback Used: no
Agent Loop Path Override: docs/proposal/v1.3.x/cross-platform-python-script-runtime-implementation-plan.md
Human Gates Preserved: plan acceptance; commit; push; tag; PR; release; publish
```

## File Responsibility Map

### New canonical runtime files

| File | Responsibility |
|---|---|
| `scripts/checker_support.py` | Shared UTF-8 reading, metadata/section/table parsing, concrete-value checks, path confinement, stable diagnostics |
| `scripts/check-root-agents-blocks.py` | Read-only managed-block parser and root `AGENTS.md` drift report |
| `scripts/check-onboarding-core-flow-coverage.py` | Core Flow Inventory, slice, diagram, section, direction, and hard-gate coverage validation |
| `scripts/check-concept-foundation-trace.py` | Concept Foundation, Requirement Product Model, permission, action, state, exception, and downstream trace validation |
| `scripts/check-adr-requirement-model-trace.py` | Effective source, model inventory, landing trace, operational trigger, Human Review, path, and coverage validation |

### New cross-platform tests

| File | Responsibility |
|---|---|
| `tests/checker_test_support.py` | `sys.executable` subprocess runner, repo paths, UTF-8 fixture helpers, stable assertion helpers |
| `tests/test_python_checker_contract.py` | Python version, canonical file inventory, stdlib-only imports, help/usage and read-only contract |
| `tests/test_root_agents_blocks.py` | Native replacement for root checker behavioral fixture generation |
| `tests/test_onboarding_core_flow_coverage.py` | Valid, deferred, missing-recovery, detached-trace, CRLF, and BOM behavior |
| `tests/test_concept_foundation_trace.py` | Valid/not-needed/invalid/adversarial Concept Foundation cases |
| `tests/test_adr_requirement_model_trace.py` | Proposed/accepted/not-needed/invalid/adversarial ADR cases and workspace confinement |
| `.github/workflows/cross-platform-checkers.yml` | Run the same `unittest` command on Windows and macOS using Python 3.10 and current stable Python |

### Compatibility and active-reference files

| File | Planned change |
|---|---|
| `scripts/check-root-agents-blocks.sh` | Replace embedded Ruby rules with a thin Python launcher after parity passes |
| `scripts/check-onboarding-core-flow-coverage.rb` | Replace validation rules with a thin Python launcher after parity passes |
| `scripts/check-concept-foundation-trace.rb` | Replace validation rules with a thin Python launcher after parity passes |
| `scripts/check-adr-requirement-model-trace.rb` | Replace validation rules with a thin Python launcher after parity passes |
| `tests/validate-root-agents-block-checker.sh` | Invoke canonical Python checker and retain the existing POSIX contract wrapper |
| `tests/validate-root-agents-block-refresh.sh` | Expect canonical `.py` references |
| `tests/validate-onboarding-core-flow-completeness.sh` | Invoke canonical Python checker |
| `tests/validate-concept-foundation-requirement-modeling.sh` | Invoke canonical Python checker and Python adversarial suite |
| `tests/validate-adr-requirement-model-technical-landing-trace.sh` | Invoke canonical Python checker and Python adversarial suite |
| `tests/validate-concept-foundation-trace-adversarial.rb` | Preserve as historical compatibility test during this version; canonical cases move to `test_concept_foundation_trace.py` |
| `tests/validate-adr-requirement-model-trace-adversarial.rb` | Preserve as historical compatibility test during this version; canonical cases move to `test_adr_requirement_model_trace.py` |

### Current authority and human-facing files

| File | Planned change |
|---|---|
| `SKILL.md` | Publish the canonical `.py` root checker path and Python capability rule |
| `Usage.md` | Show native Windows/macOS invocation examples |
| `references/project-guidance.md` | Use the canonical Python root checker and fail closed when Python is unavailable |
| `references/workflow-checklists.md` | Use the canonical Python root checker in both guidance checks |
| `CHANGELOG.md` | Record the current 1.3.0 script portability behavior without a version bump |
| `docs/reports/agent-loop-v1.3.0-cross-platform-python-script-runtime-validation-2026-07-13.md` | Record RED, parity, macOS evidence, Windows CI evidence, remaining limitations, and full-validation result |

Historical `docs/reports/*` and completed implementation plans that cite `.rb` / `.sh` remain unchanged.

## Exit-Code Contract

All canonical checkers use:

```text
0 = validation passed or --help completed
1 = checked artifact violates the contract
2 = command usage, missing argument, missing input, unsupported Python, or capability error
```

The old scripts currently mix `abort` exit `1` with explicit usage exit `2`. Before replacing an old implementation, capture its current fixture result and lock the intended exit class above in the Python tests. Human-readable wording may improve, but every diagnostic must retain a stable error category substring used by regression tests.

## Task 1: Establish RED Portability And Standard-Library Contract

**Files:**

- Create: `tests/checker_test_support.py`
- Create: `tests/test_python_checker_contract.py`
- Read: `scripts/check-root-agents-blocks.sh`
- Read: `scripts/check-onboarding-core-flow-coverage.rb`
- Read: `scripts/check-concept-foundation-trace.rb`
- Read: `scripts/check-adr-requirement-model-trace.rb`

- [ ] **Step 1: Add the shared subprocess test helper**

Create `tests/checker_test_support.py` with this complete interface:

```python
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_checker(script: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / script), *map(str, args)],
        cwd=str(cwd or ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def combined_output(result: subprocess.CompletedProcess[str]) -> str:
    return (result.stdout + result.stderr).strip()
```

- [ ] **Step 2: Write the failing canonical inventory and stdlib-only tests**

Create `tests/test_python_checker_contract.py` with the canonical inventory below. Parse imports with `ast`, allow modules in `sys.stdlib_module_names`, and allow only the local module `checker_support` outside that set.

```python
from __future__ import annotations

import ast
import sys
import unittest

from checker_test_support import ROOT, combined_output, run_checker


CHECKERS = (
    "scripts/check-root-agents-blocks.py",
    "scripts/check-onboarding-core-flow-coverage.py",
    "scripts/check-concept-foundation-trace.py",
    "scripts/check-adr-requirement-model-trace.py",
)


class PythonCheckerContractTests(unittest.TestCase):
    def test_python_runtime_is_supported(self) -> None:
        self.assertGreaterEqual(sys.version_info[:2], (3, 10))

    def test_canonical_checker_files_exist(self) -> None:
        for relative in CHECKERS:
            with self.subTest(relative=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_canonical_checkers_use_only_stdlib_and_local_support(self) -> None:
        allowed_local = {"checker_support"}
        for relative in CHECKERS:
            path = ROOT / relative
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imported: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".", 1)[0])
            external = imported - set(sys.stdlib_module_names) - allowed_local
            self.assertEqual(external, set(), f"{relative}: {sorted(external)}")

    def test_missing_arguments_fail_with_usage_exit_two(self) -> None:
        for relative in CHECKERS:
            with self.subTest(relative=relative):
                result = run_checker(relative)
                self.assertEqual(result.returncode, 2, combined_output(result))
                self.assertIn("usage", combined_output(result).lower())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run RED and record the expected failure**

Run:

```text
python3 -m unittest tests/test_python_checker_contract.py -v
```

Expected: FAIL at `test_canonical_checker_files_exist` because the four `.py` entrypoints do not exist. Record this exact RED result in the final validation report draft; do not create the report before the implementation stage is authorized.

- [ ] **Step 4: Capture current old-script fixture outcomes without editing them**

Run:

```text
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-onboarding-core-flow-completeness.sh
bash tests/validate-concept-foundation-requirement-modeling.sh
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
```

Expected: all four commands PASS before porting. Any failure is a pre-existing blocker and must route to Diagnose Failure rather than being normalized into the port.

- [ ] **Step 5: Review checkpoint**

Inspect `git diff -- tests/checker_test_support.py tests/test_python_checker_contract.py`. Do not commit. Agent Loop commit authorization remains absent.

## Task 2: Build Shared Markdown Support And Port Root AGENTS Checker

**Files:**

- Create: `scripts/checker_support.py`
- Create: `scripts/check-root-agents-blocks.py`
- Create: `tests/test_root_agents_blocks.py`
- Reference behavior: `scripts/check-root-agents-blocks.sh:1`
- Reference fixtures: `tests/validate-root-agents-block-checker.sh:1`

- [ ] **Step 1: Write root-checker RED tests using only Python fixture operations**

`tests/test_root_agents_blocks.py` must copy `templates/root-AGENTS.md` into `tempfile.TemporaryDirectory()` and cover these exact outcomes:

```text
PASS current template
FAIL missing message-intent
FAIL missing workflow-stage-map
FAIL stale block-version
FAIL broken end marker
FAIL nested block
FAIL duplicate section
FAIL unexpected managed section
FAIL missing local source
FAIL malformed bare start
FAIL malformed bare end
FAIL two markers on one line
PASS --no-source-check when only the local source is missing
```

Use this invocation pattern:

```python
result = run_checker(
    "scripts/check-root-agents-blocks.py",
    "--template", str(template),
    "--target", str(target),
)
self.assertEqual(result.returncode, expected_code, combined_output(result))
```

Run:

```text
python3 -m unittest tests/test_root_agents_blocks.py -v
```

Expected: FAIL because `scripts/check-root-agents-blocks.py` does not exist.

- [ ] **Step 2: Implement shared Markdown primitives**

Create `scripts/checker_support.py` with these concrete contracts:

```python
from __future__ import annotations

import re
from datetime import date
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


def read_text(path: str | Path) -> str:
    candidate = Path(path)
    if not candidate.is_file():
        raise CheckFailure(f"missing file: {candidate}")
    return candidate.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def metadata(content: str, label: str) -> str | None:
    match = re.search(rf"^{re.escape(label)}:\s*(.+?)\s*$", content, re.MULTILINE)
    return match.group(1).strip() if match else None


def section(content: str, title: str, level: int = 2, required: bool = True) -> str | None:
    marker = "#" * level
    match = re.search(
        rf"^{re.escape(marker)} {re.escape(title)}\s*$\n(.*?)(?=^#{{1,{level}}}\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not match and required:
        raise CheckFailure(f"missing section: {marker} {title}")
    return match.group(1) if match else None


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table(content: str, title: str, level: int = 2) -> list[dict[str, str]]:
    body = section(content, title, level)
    assert body is not None
    lines = [line.strip() for line in body.splitlines()]
    start = next((index for index, line in enumerate(lines) if line.startswith("|")), None)
    if start is None:
        raise CheckFailure(f"missing table in section: {title}")
    table_lines: list[str] = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        table_lines.append(line)
    if len(table_lines) < 3:
        raise CheckFailure(f"missing table in section: {title}")
    headers = split_row(table_lines[0])
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = split_row(line)
        if len(cells) != len(headers):
            raise CheckFailure(f"column count mismatch in section: {title}")
        rows.append(dict(zip(headers, cells, strict=True)))
    if not rows:
        raise CheckFailure(f"empty table in section: {title}")
    return rows


def parse_iso_date(value: str | None, context: str) -> date:
    if not value:
        raise CheckFailure(f"{context} is missing")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise CheckFailure(f"{context} must be YYYY-MM-DD") from error


def confined_path(root: str | Path, relative: str) -> Path:
    root_path = Path(root).resolve()
    candidate = (root_path / relative).resolve(strict=False)
    try:
        candidate.relative_to(root_path)
    except ValueError as error:
        raise CheckFailure(f"reference escapes workspace root: {relative}") from error
    return candidate
```

- [ ] **Step 3: Implement the root checker as a read-only Python CLI**

Create `scripts/check-root-agents-blocks.py` with:

- `ManagedBlock` and `MarkerError` dataclasses;
- regexes equivalent to current `START_RE` and `END_RE`;
- `parse_blocks(path) -> tuple[dict[str, ManagedBlock], list[MarkerError]]`;
- `local_source(source) -> bool`;
- `build_findings(template, target, check_sources) -> list[list[str]]`;
- an `argparse` CLI supporting `--template`, `--target`, `--no-source-check`;
- exact PASS prefix `PASS root AGENTS managed blocks are current`;
- exact FAIL prefix `FAIL root AGENTS drift found` and the six-column Markdown table;
- exit `2` for missing arguments/files, `1` for drift, `0` for PASS/help.

Use `Path.exists()` only; never write the template, target, or source paths.

- [ ] **Step 4: Run GREEN and the original contract**

Run:

```text
python3 -m unittest tests/test_python_checker_contract.py tests/test_root_agents_blocks.py -v
bash tests/validate-root-agents-block-checker.sh
```

Expected: Python tests PASS; the original shell test still PASS against the old compatibility path at this stage.

- [ ] **Step 5: Review checkpoint**

Run `python3 -m py_compile scripts/checker_support.py scripts/check-root-agents-blocks.py tests/test_root_agents_blocks.py`. Inspect the diff. Do not commit.

## Task 3: Port Onboarding Core Flow Coverage Checker

**Files:**

- Create: `scripts/check-onboarding-core-flow-coverage.py`
- Create: `tests/test_onboarding_core_flow_coverage.py`
- Reference behavior: `scripts/check-onboarding-core-flow-coverage.rb:1`
- Existing fixtures: `tests/fixtures/onboarding-core-flow/`
- Existing example: `examples/ai-meeting-minutes-backend/onboarding-db/`

- [ ] **Step 1: Write failing native tests**

Cover:

```text
PASS examples/ai-meeting-minutes-backend/onboarding-db
PASS tests/fixtures/onboarding-core-flow/valid-deferred
FAIL invalid-missing-recovery with missing required slice/recovery diagnostic
FAIL invalid-detached-trace with missing diagram/section trace diagnostic
PASS a temporary copy converted to CRLF
PASS a temporary copy whose first Markdown file starts with UTF-8 BOM
FAIL missing onboarding root with exit 2
```

Run `python3 -m unittest tests/test_onboarding_core_flow_coverage.py -v`.

Expected: FAIL because the canonical checker does not exist.

- [ ] **Step 2: Port the validator without changing its semantic surface**

Implement a `CoreFlowCoverage` class by translating the current methods one-for-one:

| Python method | Ruby source | Exact responsibility |
|---|---|---|
| `validate` | lines 16-55 | read five required artifacts, select critical/important rows, require planned/deferred, count both branches |
| `validate_deferred` | lines 59-63 | require `impact=`, `missing=`, and `next=` fields |
| `validate_planned` | lines 65-112 | validate slices, flow docs, placeholders, diagrams, section targets, symbol/config evidence, call/data direction, and hard gates |
| `read_required` | lines 114-119 | choose the first existing candidate and decode it with `read_text` |
| `read_flow_docs` | lines 121-127 | deterministically sort `03-flows/*.md`, otherwise use `flow.md` |
| `require_token` | lines 129-131 | reject a missing flow/slice token |
| `require_hard_gate_pass` | lines 133-136 | require the flow row to contain `PASS` |
| `require_hard_gate_before_score` | lines 138-146 | require the gate and ensure it precedes `## Score` |

Use this complete CLI boundary around the translated class:

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate onboarding core-flow coverage")
    parser.add_argument("onboarding_root")
    args = parser.parse_args(argv)
    try:
        planned, deferred = CoreFlowCoverage(Path(args.onboarding_root)).validate()
    except CheckFailure as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f"PASS: core-flow coverage trace is complete ({planned} planned, {deferred} deferred)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The class must preserve all checks from Ruby lines 16-146 in the same order so first-failure categories remain stable.

CLI output remains:

```text
PASS: core-flow coverage trace is complete (1 planned, 0 deferred)
```

- [ ] **Step 3: Run GREEN and focused legacy tests**

Run:

```text
python3 -m unittest tests/test_onboarding_core_flow_coverage.py -v
python3 scripts/check-onboarding-core-flow-coverage.py examples/ai-meeting-minutes-backend/onboarding-db
bash tests/validate-onboarding-core-flow-completeness.sh
```

Expected: all PASS.

- [ ] **Step 4: Review checkpoint**

Run `python3 -m py_compile scripts/check-onboarding-core-flow-coverage.py tests/test_onboarding_core_flow_coverage.py`. Inspect the diff. Do not commit.

## Task 4: Port Concept Foundation Trace Checker

**Files:**

- Create: `scripts/check-concept-foundation-trace.py`
- Create: `tests/test_concept_foundation_trace.py`
- Reference behavior: `scripts/check-concept-foundation-trace.rb:1`
- Reference adversarial behavior: `tests/validate-concept-foundation-trace-adversarial.rb:1`
- Existing examples/fixtures: `examples/concept-foundation-refund/`, `tests/fixtures/concept-foundation/`

- [ ] **Step 1: Write failing native tests**

Port all current adversarial cases by creating temporary copies and transforming text with Python `str.replace`, `re.sub`, and `splitlines(keepends=True)`. The test suite must reject:

```text
downstream use of unconfirmed concepts
missing Concept Candidate Inventory
open blocking ambiguity
non-concrete concept-foundation-not-needed reason
downstream model omitted from Concept-To-Product trace
duplicate Concept Definition ID
missing effective Concept Foundation source
command actor without target permission
invalid-unaccepted fixture
invalid-detached-model fixture
```

It must accept the current complete refund example and a reasoned not-needed case. Run `python3 -m unittest tests/test_concept_foundation_trace.py -v`; expected RED is missing canonical checker.

- [ ] **Step 2: Port shared table and ID validation logic**

Use `checker_support.metadata`, `section`, `table`, and `read_text`. Implement these checker-local helpers with Python `set` semantics:

```python
def ids(text: str, pattern: re.Pattern[str]) -> set[str]:
    return set(pattern.findall(text or ""))


def assert_defined(used: set[str], defined: set[str], context: str) -> None:
    missing = used - defined
    if missing:
        raise CheckFailure(f"undefined IDs in {context}: {', '.join(sorted(missing))}")


def assert_unique_ids(values: list[str], context: str, pattern: re.Pattern[str]) -> None:
    invalid = sorted({value for value in values if pattern.fullmatch(value) is None})
    if invalid:
        raise CheckFailure(f"invalid IDs in {context}: {', '.join(invalid)}")
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise CheckFailure(f"duplicate IDs in {context}: {', '.join(duplicates)}")


def assert_confirmed(used: set[str], confirmed: set[str], context: str) -> None:
    unconfirmed = used - confirmed
    if unconfirmed:
        raise CheckFailure(f"unconfirmed Concept IDs in {context}: {', '.join(sorted(unconfirmed))}")


def reject_placeholders(content: str, path: Path) -> None:
    forbidden = ("<topic>", "C-EXAMPLE", "C-OTHER", "TBD", "TODO", "待补充")
    found = [token for token in forbidden if token in content]
    if found:
        raise CheckFailure(f"placeholder content in {path}: {', '.join(found)}")
```

Port every current validation block in source order so the first-failure category remains stable:

```text
status and effective-source alignment
reasoned not-needed branch
section order
candidate/definition/confirmation/ambiguity
relationships
permission matrix
commands/events and actor permission
primary flow
state model
requirement product model
exception paths
Concept-To-Product trace completeness
Product Brief / Feature Spec no-redefinition rules
downstream concept/model coverage
```

- [ ] **Step 3: Preserve CLI and PASS behavior**

CLI accepts exactly `REQUIREMENT PRODUCT SPEC`; usage/missing input returns `2`, validation failures return `1`, and success returns `0` with one of:

```text
PASS: reasoned concept-foundation-not-needed trace
PASS: accepted Concept Foundation trace is complete (4 concepts, 9 model rows)
```

- [ ] **Step 4: Run GREEN and original focused tests**

Run:

```text
python3 -m unittest tests/test_concept_foundation_trace.py -v
python3 scripts/check-concept-foundation-trace.py examples/concept-foundation-refund/requirement.md examples/concept-foundation-refund/product.md examples/concept-foundation-refund/spec.md
bash tests/validate-concept-foundation-requirement-modeling.sh
```

Expected: all PASS.

- [ ] **Step 5: Review checkpoint**

Run `python3 -m py_compile scripts/check-concept-foundation-trace.py tests/test_concept_foundation_trace.py`. Inspect the diff. Do not commit.

## Task 5: Port ADR Requirement Model Technical Landing Checker

**Files:**

- Create: `scripts/check-adr-requirement-model-trace.py`
- Create: `tests/test_adr_requirement_model_trace.py`
- Reference behavior: `scripts/check-adr-requirement-model-trace.rb:1`
- Reference adversarial behavior: `tests/validate-adr-requirement-model-trace-adversarial.rb:1`
- Existing fixtures: `tests/fixtures/adr-technical-landing/`

- [ ] **Step 1: Write failing fixture and adversarial tests**

The Python suite must accept:

```text
proposed structural preflight without Human Review Evidence
accepted ADR with complete Human Review Evidence
planned canonical Feature Spec owner
source model delegated to an existing proposed decision
reasoned concept-foundation-not-needed ADR
```

It must reject:

```text
accepted ADR without Human Review Evidence
placeholder not-applicable reason
arbitrary or extra Coverage Hard Gate items
garbage Accepted Requirement Model ID
silently omitted source model
missing accepted-decision target
missing feature-local target
invalid Design Slice coverage status
triggered operational concern without detail
incomplete operational concern inventory
invalid-missing-coverage fixture
invalid-empty-landing fixture
invalid-unaccepted-source fixture
invalid-reopened-source fixture
invalid-review-required fixture
workspace escape using ../
Windows-style case-collision reference where two existing paths differ only by case
```

Run `python3 -m unittest tests/test_adr_requirement_model_trace.py -v`; expected RED is missing canonical checker.

- [ ] **Step 2: Port parser, value, date, and confinement helpers**

Use shared support where behavior is identical. Implement checker-local functions matching the current Ruby contracts:

```python
def normalized(value: str | None) -> str:
    return (value or "").strip().strip("`")


def concrete(value: str | None) -> bool:
    text = normalized(value)
    if not text or re.fullmatch(r"-|none|n/a|na|not applicable|tbd|todo|unknown", text, re.IGNORECASE):
        return False
    return re.search(r"<[^>]+>", text) is None


def concrete_reason(value: str | None) -> bool:
    text = normalized(value)
    return concrete(text) and len(text) >= 12


def assert_unique(values: list[str], context: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise CheckFailure(f"duplicate IDs in {context}: {', '.join(duplicates)}")


def parse_id_list(
    value: str | None,
    pattern: re.Pattern[str],
    context: str,
    allow_none: bool = False,
) -> list[str]:
    text = (value or "").strip()
    if allow_none and text.casefold() == "none":
        return []
    if not text:
        raise CheckFailure(f"{context} is missing")
    tokens = [normalized(token) for token in text.split(",")]
    invalid = [token for token in tokens if pattern.fullmatch(token) is None]
    if invalid:
        raise CheckFailure(f"invalid values in {context}: {', '.join(invalid)}")
    assert_unique(tokens, context)
    return tokens


def markdown_path(value: str | None) -> str | None:
    match = re.search(r"([A-Za-z0-9._/-]+\.md)\b", normalized(value))
    return match.group(1) if match else None
```

Translate the remaining complex validators one-for-one from these exact sources:

| Python function | Ruby source | Required behavior |
|---|---|---|
| `validate_decision_reference` | lines 149-162 | planned rule, Markdown path extraction, confinement, existence, allowed decision status |
| `validate_feature_reference` | lines 164-174 | canonical Feature Spec shape, confinement, existence, proposed/accepted status |
| `validate_human_review` | lines 176-184 | proposed bypass only; accepted decision, confirmer, ISO date, concrete evidence |
| `validate_gate` | lines 186-200 | reject unchecked, duplicate, missing, and extra gate items |
| `validate_operational` | lines 202-237 | exact concern inventory, trigger reason, detail presence/absence and headings |

Use `PurePosixPath` semantics for Markdown paths, reject backslashes in canonical Markdown references, then resolve through `confined_path`. Before accepting an existing path on Windows/macOS, build a case-folded sibling map and reject ambiguous names that differ only by case.

- [ ] **Step 3: Port the two validation branches in source order**

Preserve:

```text
README effective-source resolution
source/pointer/snapshot status agreement
proposed vs accepted Human Review behavior
Upstream Compatibility current
Design Slice validation
exact Coverage Hard Gate inventory
exact Operational Landing inventory
reasoned not-needed trace-not-applicable branch
accepted Concept/Model source inventory
Scope Inventory equality and dispositions
Technical Landing Trace equality and dispositions
Design Slice references for landed rows
```

CLI accepts `REQUIREMENT_README REQUIREMENT_SOURCE DECISION [WORKSPACE_ROOT]`. PASS output remains one of:

```text
PASS: reasoned concept-foundation-not-needed ADR proposed gate is complete
PASS: ADR accepted technical landing trace covers 8 in-scope requirement-model IDs with 3 landed rows
```

- [ ] **Step 4: Run GREEN and focused legacy tests**

Run:

```text
python3 -m unittest tests/test_adr_requirement_model_trace.py -v
python3 scripts/check-adr-requirement-model-trace.py tests/fixtures/adr-technical-landing/valid/README.md tests/fixtures/adr-technical-landing/valid/requirement.md tests/fixtures/adr-technical-landing/valid/decision.md
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
```

Expected: all PASS.

- [ ] **Step 5: Review checkpoint**

Run `python3 -m py_compile scripts/check-adr-requirement-model-trace.py tests/test_adr_requirement_model_trace.py`. Inspect the diff. Do not commit.

## Task 6: Switch Active Tests And Add One-Cycle Compatibility Launchers

**Files:**

- Modify: `scripts/check-root-agents-blocks.sh`
- Modify: `scripts/check-onboarding-core-flow-coverage.rb`
- Modify: `scripts/check-concept-foundation-trace.rb`
- Modify: `scripts/check-adr-requirement-model-trace.rb`
- Modify: `tests/validate-root-agents-block-checker.sh`
- Modify: `tests/validate-root-agents-block-refresh.sh`
- Modify: `tests/validate-onboarding-core-flow-completeness.sh`
- Modify: `tests/validate-concept-foundation-requirement-modeling.sh`
- Modify: `tests/validate-adr-requirement-model-technical-landing-trace.sh`

- [ ] **Step 1: Change shell contract tests to invoke canonical Python**

At the top of each affected shell test, resolve:

```bash
python_cmd=${PYTHON:-python3}
if ! command -v "$python_cmd" >/dev/null 2>&1; then
  printf 'FAIL: Python 3.10+ is required: %s\n' "$python_cmd" >&2
  exit 2
fi
```

Replace every checker invocation explicitly:

```text
scripts/check-root-agents-blocks.sh -> python3 scripts/check-root-agents-blocks.py
scripts/check-onboarding-core-flow-coverage.rb -> python3 scripts/check-onboarding-core-flow-coverage.py
scripts/check-concept-foundation-trace.rb -> python3 scripts/check-concept-foundation-trace.py
scripts/check-adr-requirement-model-trace.rb -> python3 scripts/check-adr-requirement-model-trace.py
```

Update file-existence and forbidden-domain assertions to target `.py`. Keep the shell tests as POSIX maintainer wrappers; Windows uses `unittest` directly.

- [ ] **Step 2: Replace the old root shell implementation with a launcher**

The compatibility launcher must contain no marker parsing. Resolve `python3`, then `python`, verify `>=3.10`, and `exec` the sibling `.py` with unchanged arguments. On failure print `deprecated compatibility entry requires Python 3.10+; invoke check-root-agents-blocks.py directly` and exit `2`.

- [ ] **Step 3: Replace each old Ruby implementation with a launcher**

Each `.rb` compatibility file must use `RbConfig::CONFIG["host_os"]` only to choose candidate commands, find its sibling `.py`, forward `ARGV`, and exit with the child status. It must contain no validation regex, tables, domain IDs, or artifact rules.

- [ ] **Step 4: Run parity and active focused tests**

Run:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-onboarding-core-flow-completeness.sh
bash tests/validate-concept-foundation-requirement-modeling.sh
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
```

Expected: all PASS. Run each old launcher once against a valid fixture and confirm it returns the same PASS category as the canonical Python entrypoint.

- [ ] **Step 5: Review checkpoint**

Search old files for validation leakage:

```text
rg -n 'Concept ID|Requirement Model|managed-start|Core Flow|Coverage Hard Gate' scripts/*.rb scripts/*.sh
```

Expected: no business/validation rules remain in compatibility launchers. Do not commit.

## Task 7: Switch Current Documentation And Record The Behavior Change

**Files:**

- Modify: `SKILL.md:121`
- Modify: `Usage.md:273`
- Modify: `references/project-guidance.md:37`
- Modify: `references/project-guidance.md:161`
- Modify: `references/project-guidance.md:178`
- Modify: `references/workflow-checklists.md:136`
- Modify: `references/workflow-checklists.md:222`
- Modify: `CHANGELOG.md` under `1.3.0`
- Preserve: `docs/reports/**`
- Preserve: completed proposal implementation plans that record old commands

- [ ] **Step 1: Add a failing documentation-reference assertion**

Extend `tests/test_python_checker_contract.py` so current authority files must contain `scripts/check-root-agents-blocks.py` and must not contain `scripts/check-root-agents-blocks.sh`:

```python
    def test_current_authority_uses_python_root_checker(self) -> None:
        current = (
            "SKILL.md",
            "Usage.md",
            "references/project-guidance.md",
            "references/workflow-checklists.md",
        )
        for relative in current:
            content = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("scripts/check-root-agents-blocks.py", content, relative)
            self.assertNotIn("scripts/check-root-agents-blocks.sh", content, relative)
```

Run the test and expect FAIL before editing docs.

- [ ] **Step 2: Update current authority references**

Use the canonical path and include both invocation forms where commands are shown:

```text
macOS: python3 "$AGENT_LOOP_SKILL/scripts/check-root-agents-blocks.py" --template "$AGENT_LOOP_SKILL/templates/root-AGENTS.md" --target "$PROJECT_ROOT/AGENTS.md"
Windows: py -3 "%AGENT_LOOP_SKILL%\scripts\check-root-agents-blocks.py" --template "%AGENT_LOOP_SKILL%\templates\root-AGENTS.md" --target "%PROJECT_ROOT%\AGENTS.md"
```

State that interpreter discovery is read-only, Python must be `>=3.10`, missing capability blocks the checker, and no Agent/manual fallback counts as validation.

- [ ] **Step 3: Add a `Cross-Platform Python Script Runtime` section to the 1.3.0 changelog**

Record:

- four canonical Python standard-library checkers;
- Windows/macOS native fixture coverage;
- one-cycle deprecated compatibility entrypoints;
- fail-closed interpreter policy;
- historical reports/proposals unchanged;
- monthly compaction still not implemented.

- [ ] **Step 4: Verify no current authority reference remains stale**

Run:

```text
python3 -m unittest tests/test_python_checker_contract.py -v
rg -n 'scripts/check-root-agents-blocks\.sh' SKILL.md Usage.md references templates README.md
```

Expected: unittest PASS; `rg` returns no current authority match. Matches in `docs/reports/` or completed proposals are allowed and remain unchanged.

- [ ] **Step 5: Review checkpoint**

Inspect the docs diff separately from code. Do not commit and do not bump `Version: 1.3.0`.

## Task 8: Add Dual-Platform CI And Complete Verification

**Files:**

- Create: `.github/workflows/cross-platform-checkers.yml`
- Create: `docs/reports/agent-loop-v1.3.0-cross-platform-python-script-runtime-validation-2026-07-13.md`
- Review: `docs/maintenance/full-validation-method.md`
- Review: `docs/maintenance/feature-validation-method.md`

- [ ] **Step 1: Add the Windows/macOS Python matrix**

Create:

```yaml
name: Cross-platform Python checkers

on:
  push:
    branches: ["alpha/v1.3.0", "v1.3.0"]
  pull_request:

jobs:
  checker-tests:
    strategy:
      fail-fast: false
      matrix:
        os: [macos-latest, windows-latest]
        python-version: ["3.10", "3.x"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -m unittest discover -s tests -p "test_*.py" -v
```

This workflow validates only the cross-platform Python checker scope. It does not claim that Bash maintainer tests run natively on Windows.

- [ ] **Step 2: Run the complete Python suite locally on macOS**

Run:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m compileall -q scripts tests
```

Expected: all Python tests PASS and compileall exits `0`.

- [ ] **Step 3: Run all existing shell regressions on macOS**

Run each file independently so failures are attributable:

```text
for test_file in tests/*.sh; do bash "$test_file" || exit 1; done
```

Expected: every current shell test PASS.

- [ ] **Step 4: Run repository-required mechanical checks**

Run:

```text
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json >/dev/null
git diff --check
```

Run a Markdown fence-balance check over every changed Markdown file. Expected: all PASS.

- [ ] **Step 5: Follow the full-validation method**

Because current published checker references, root guidance validation, and multiple accepted artifact validators change together, follow `docs/maintenance/full-validation-method.md`: preserve RED evidence, run semantic audit, pressure tests, full regression, cross-file consistency review, and save the Chinese report at the planned report path.

The report must distinguish:

```text
macOS local evidence
Windows CI evidence
old/new parity evidence
stdlib-only evidence
historical-document preservation
remaining maintainer-shell limitation
monthly-compaction not implemented
```

- [ ] **Step 6: Verification helper and review helper gates**

Before claiming completion, resolve and load `verification-before-completion`; run fresh commands and cite outputs. Then resolve and load `requesting-code-review`; perform Spec Review and Standards Review because this is a broad cross-platform tooling change.

- [ ] **Step 7: Final Human Review Summary**

Present changed files, Python test counts, shell regression counts, macOS evidence, Windows evidence availability, full-validation score/findings, drift, compatibility limitations, and the exact next action.

Do not commit or push. If Windows CI evidence cannot exist until push, report the capability as `macOS-verified / Windows-test-defined`, keep the proposal status out of completed, and ask for the Submit/CI gate rather than claiming dual-platform completion.

## Plan Self-Review

### Spec coverage

- Standard-library-only runtime: Tasks 1-5 and contract test.
- Native Windows/macOS behavior: Tasks 1-5 tests plus Task 8 matrix.
- Four current checkers: Tasks 2-5.
- One-cycle compatibility: Task 6.
- Current Markdown references: Task 7.
- Historical evidence preservation: execution boundary and Task 7.
- Fail-closed interpreter behavior: Tasks 1, 6, and 7.
- No monthly compaction implementation: execution boundary, changelog, and final report.
- No version bump/submit action: execution boundary and final gate.

### Placeholder scan

The plan contains no unresolved implementation marker or unnamed file/command placeholder. Dynamic output examples use concrete fixture counts.

### Type and naming consistency

- Canonical filenames consistently use hyphenated `.py` entrypoints.
- Shared module name is consistently `checker_support`.
- Tests invoke canonical scripts with `sys.executable` through `run_checker`.
- Markdown repository-relative paths remain `/`-separated; filesystem paths use `Path`.
- Success/failure/usage exit codes are consistently `0/1/2`.
