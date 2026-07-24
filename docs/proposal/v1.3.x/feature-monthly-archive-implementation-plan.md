# Feature Monthly Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task after Plan Human Review. Use `test-driven-development` for every behavior change, `systematic-debugging` for unexpected failures, `verification-before-completion` before completion claims, and `requesting-code-review` before handoff. This plan is intended for a separate development Agent, but writing the plan does not authorize implementation, subagent dispatch, commit, push, tag, PR, release, or publication.

**Goal:** Add a Human-gated, cross-platform Feature Monthly Archive capability that moves eligible closed feature directories intact into `.agent-loop/features/YYYY-MM/`, maintains `.agent-loop/features/archive.md` as the stable Feature ID locator, updates durable references, verifies the result, restores failed transactions, and rehydrates archived features before follow-up work.

**Architecture:** Implement Reader Compatibility first through one standard-library `feature_archive_support.py` module that owns Feature ID/path resolution, archive-index parsing, deterministic plans, reference-impact discovery, hashing, path confinement, and transaction-journal primitives. Four thin Python CLIs then expose scan, check, apply, and restore operations; apply always recomputes and matches a Human-reviewed plan hash before writing. Only after reader compatibility and executable tests pass should the published runtime, root Stage Map, templates, and human docs advertise the capability.

**Tech Stack:** Python 3.10+ standard library (`argparse`, `dataclasses`, `datetime`, `hashlib`, `json`, `os`, `pathlib`, `re`, `shutil`, `tempfile`, `typing`, `unittest`, `unicodedata`, `urllib.parse`), Markdown artifacts, existing `scripts/checker_support.py`, existing shell contract tests, GitHub Actions Windows/macOS matrix.

---

## Execution Status

```text
Proposal: accepted by Human Review on 2026-07-14
Plan: accepted and implementation authorized by Human Review on 2026-07-14
Implementation: Task 0-7 completed and pre-release full validation passed
Review: local Spec/Standards Review and Human feature review completed
Platform: macOS-verified / Windows-verified
Release: Human Gate approved on 2026-07-14; target tag stable-v1.3.0
Tag condition: the exact release-evidence commit must pass the Windows/macOS CI matrix before tag creation
```

## Execution Boundary

Included:

- Feature ID and flat/month-path resolver;
- `.agent-loop/features/archive.md` template, parser, validator, and locator behavior;
- ADR Feature Spec reference compatibility for archived closed features;
- explicit `feature-archive-maintenance` message intent and triggered `Feature Monthly Archive` stage;
- read-only deterministic archive/rehydrate scan;
- read-only pre/post/restore checking;
- Human-confirmed whole-directory archive and rehydrate operations;
- persistent transaction journal and failure restore;
- durable Markdown reference updates and conservative blocker reporting;
- Windows/macOS native tests using only Python standard library;
- coordinated runtime, design, Stage Map, checklist, template, scenario, Usage, README, changelog, and report updates;
- mandatory full validation because routing, Feature Follow-up, recovery, root guidance, and feature path invariants change.

Excluded:

- per-feature archive summaries;
- `historical/` content reorganization;
- per-month `INDEX.md`;
- deletion, packing, compression, external storage, or Deep Archive;
- automatic scheduled archival;
- automatic archive without a Batch Human Gate;
- moving `active`, `blocked`, `paused`, current-month, incomplete-close, open-follow-up, or drifted features;
- changing original requirement sources or accepted ADR meaning;
- third-party Python packages;
- generic repository-wide link rewriting outside Markdown and Agent Loop-owned YAML metadata;
- version bump without separate Human approval.

## Stage Helper Resolution

```text
Stage: Plan Gate / Plan If Needed
Canonical Candidate: superpowers:writing-plans
Canonical Result: unavailable under that qualified name in the current runtime
Alias Candidate: writing-plans
Resolved Helper: writing-plans
Status: loaded
Load Evidence: /Users/shaodowyd/.codex/skills/writing-plans/SKILL.md read completely on 2026-07-14
Fallback Used: no
Method Used: exact file map, interface-first design, bite-sized TDD steps, RED/GREEN commands, risks, rollback, and self-review
Agent Loop Path Override: docs/proposal/v1.3.x/feature-monthly-archive-implementation-plan.md
Human Gates Preserved: Plan approval; implementation start; any development-Agent/subagent dispatch; archive Batch Human Gate; rehydrate Human Gate; commit; push; tag; PR; release; publish
```

## Preconditions And Hard Stops

1. Preserve the verified remote `cross-platform-checkers.yml` evidence for commit `7253461`: all four macOS/Windows × Python 3.10/3.x jobs succeeded in run <https://github.com/Shadow-linux/agent-loop/actions/runs/29320389912>. Do not replace execution evidence with matrix configuration alone.
2. Preserve unrelated dirty work. At plan time, unrelated paths include `docs/proposal/v1.3.x/onboarding-core-flow-completeness.md`, deleted v1.4 proposal files, and `docs/proposal/v2.0.x/`. Do not stage, revert, rewrite, or include them in validation claims.
3. Do not move any real target-project feature directory while developing this source repository. All mutation tests use temporary fixtures.
4. If any pre-existing full-suite test fails before the first RED, stop and diagnose it separately; do not normalize it into this feature.
5. No command exposes `--force`, skips the expected-plan hash, or silently treats an unresolved reference as historical evidence.

## Non-Negotiable Invariants

```text
Feature identity = YYYY-MM-DD-slug Feature ID
Feature lifecycle = draft | active | blocked | paused | closed
Archive state = archived | rehydrated; never a feature lifecycle value
Active / blocked / paused path = features/<feature-id>/
Archived path = features/YYYY-MM/<feature-id>/
Archive eligibility = closed + complete close evidence + no open blocker
Archive authority = original feature artifacts; archive.md is locator only
Mutation authorization = exact Human-reviewed plan SHA-256
Failure behavior = fail closed + persistent journal + verified restore
Content policy = move intact; no deletion or content-summary substitution
```

## CLI Contract

All four entrypoints use the same exit classes:

```text
0 = scan/check/apply/restore completed successfully
1 = artifact, eligibility, stale-plan, reference, transaction, or post-check contract failed
2 = command usage, missing path, unsupported Python, invalid date/month, or capability error
```

Archive scan:

```text
python scripts/scan-feature-monthly-archive.py \
  --project-root /workspace/project \
  --operation archive \
  --month 2026-05 \
  --month 2026-06 \
  --as-of 2026-07-14
```

Rehydrate scan:

```text
python scripts/scan-feature-monthly-archive.py \
  --project-root /workspace/project \
  --operation rehydrate \
  --feature-id 2026-05-08-login \
  --as-of 2026-07-14
```

Apply binds to the exact scan result:

```text
python scripts/apply-feature-monthly-archive.py \
  --project-root /workspace/project \
  --operation archive \
  --month 2026-05 \
  --month 2026-06 \
  --as-of 2026-07-14 \
  --expected-plan-sha256 64-lowercase-hex-characters
```

Post-check and transaction restore:

```text
python scripts/check-feature-monthly-archive.py --project-root /workspace/project --operation archive --plan /absolute/path/plan.json
python scripts/restore-feature-monthly-archive.py --project-root /workspace/project --transaction-id 20260714T120000Z-0123456789ab
```

Scan prints deterministic UTF-8 JSON to stdout. The controlling Agent may save that output to an OS temporary file for apply/check; the script must not create a target-project artifact during scan. The Batch Human Review Summary displays `plan_sha256`, selected months, eligible/blocked Feature IDs, moves, reference edits, unchanged files, and restore behavior.

## JSON Plan Contract

The serialized plan has this exact top-level shape:

```json
{
  "schema_version": 1,
  "operation": "archive",
  "as_of": "2026-07-14",
  "selected_months": ["2026-05", "2026-06"],
  "selected_feature_ids": [],
  "candidates": [],
  "moves": [],
  "archive_entries": [],
  "reference_edits": [],
  "skipped_references": [],
  "snapshots": {},
  "plan_sha256": "64-lowercase-hex-characters"
}
```

`plan_sha256` is SHA-256 over canonical JSON of every field except `plan_sha256`, using `sort_keys=True`, `ensure_ascii=False`, `separators=(",", ":")`, UTF-8 encoding, POSIX workspace-relative paths, sorted lists, and no current timestamp. Absolute project paths and output formatting are excluded so the same fixture produces the same hash on Windows and macOS. Content snapshots and relative paths still bind the plan to the exact project state.

## Interface Contracts

### `ArchiveContractError`

Location: `scripts/feature_archive_support.py`

Kind: exception dataclass

Signature:

```python
@dataclass(frozen=True)
class ArchiveContractError(Exception):
    category: str
    detail: str
    exit_code: int = 1
```

Errors: `usage`, `memory-root`, `feature-id`, `month`, `eligibility`, `path-collision`, `path-escape`, `archive-index`, `reference-impact`, `stale-plan`, `transaction`, `post-check`, `restore`.

### `FeatureLocation`

Location: `scripts/feature_archive_support.py`

Kind: immutable dataclass

Signature:

```python
@dataclass(frozen=True)
class FeatureLocation:
    feature_id: str
    relative_path: str
    layout: Literal["flat", "archived"]
    month: str | None
```

Validation: flat is exactly `features/<feature-id>`; archived is exactly `features/YYYY-MM/<feature-id>` and month equals the first seven characters of Feature ID.

### `ArchiveEntry`

Location: `scripts/feature_archive_support.py`

Kind: immutable dataclass

Signature:

```python
@dataclass(frozen=True)
class ArchiveEntry:
    feature_id: str
    month: str
    current_path: str
    archive_state: Literal["archived", "rehydrated"]
    closed_at: str
    delivered_summary: str
    source_requirements: str
    applicable_decisions: str
    last_moved_at: str
```

### `ReferenceEdit`

Location: `scripts/feature_archive_support.py`

Kind: immutable dataclass

Signature:

```python
@dataclass(frozen=True)
class ReferenceEdit:
    path: str
    kind: Literal["literal-path", "relative-link", "archive-index"]
    old: str
    new: str
    occurrences: int
    before_sha256: str
    after_sha256: str
```

### `SkippedReference`

Location: `scripts/feature_archive_support.py`

Kind: immutable dataclass

Signature:

```python
@dataclass(frozen=True)
class SkippedReference:
    path: str
    classification: Literal["immutable-requirement-source", "historical-evidence", "unsupported"]
    matched_value: str
    reason: str
```

`immutable-requirement-source` and concrete `historical-evidence` rows are displayed at Human Review and preserved. Any `unsupported` row blocks apply.

### `Move`

Location: `scripts/feature_archive_support.py`

Kind: immutable dataclass

Signature:

```python
@dataclass(frozen=True)
class Move:
    feature_id: str
    month: str
    source: str
    target: str
```

Paths are POSIX project-relative paths. Archive moves are flat-to-month; rehydrate moves are month-to-flat.

### `ArchiveCandidate`

Location: `scripts/feature_archive_support.py`

Kind: immutable dataclass

Signature:

```python
@dataclass(frozen=True)
class ArchiveCandidate:
    feature_id: str
    month: str
    current_path: str
    lifecycle: str
    close_evidence: Literal["complete", "incomplete"]
    open_follow_up: str
    delivered_summary: str
    source_requirements: str
    applicable_decisions: str
    blockers: Sequence[str]
```

Eligibility is `not blockers`; blocker strings are stable category/detail messages sorted lexically.

### `ArchivePlan`

Location: `scripts/feature_archive_support.py`

Kind: immutable dataclass with canonical JSON serialization

Fields:

```python
@dataclass(frozen=True)
class ArchivePlan:
    schema_version: int
    operation: Literal["archive", "rehydrate"]
    as_of: str
    selected_months: Sequence[str]
    selected_feature_ids: Sequence[str]
    candidates: Sequence[ArchiveCandidate]
    moves: Sequence[Move]
    archive_entries: Sequence[ArchiveEntry]
    reference_edits: Sequence[ReferenceEdit]
    skipped_references: Sequence[SkippedReference]
    snapshots: Mapping[str, str]
```

Import `Literal`, `Mapping`, and `Sequence` from `typing`. Store tuples and a read-only copied mapping internally even though the public annotations use collection protocols.

Required methods and exact behavior:

| Method | Return | Behavior |
|---|---|---|
| `to_payload(include_hash: bool = True)` | `dict[str, object]` | Serialize every dataclass collection in stable sorted order; include the computed lowercase hash only when requested |
| `canonical_bytes()` | `bytes` | Call `to_payload(include_hash=False)` and encode through `canonical_json_bytes` |
| `computed_sha256()` | `str` | Return `sha256_bytes(self.canonical_bytes())` |
| `assert_hash(expected: str)` | `None` | Reject malformed hashes as usage exit 2 and mismatches as `stale-plan` exit 1 |

### `resolve_feature_location`

Location: `scripts/feature_archive_support.py`

Signature:

```python
def resolve_feature_location(memory_root: Path, feature_id: str) -> FeatureLocation:
```

Behavior:

1. Reject malformed Feature ID.
2. If exact flat directory exists, reject any simultaneous archived locator/directory collision and return flat.
3. Otherwise parse `features/archive.md`, require exactly one matching row, confine `Current Path`, require existing directory and matching Feature ID/month, then return archived or rehydrated location.
4. A `rehydrated` row must point to the flat path.

Related exact signatures:

```text
parse_archive_index(memory_root: Path) -> Sequence[ArchiveEntry]
render_archive_index(entries: Sequence[ArchiveEntry]) -> str
```

`render_archive_index` uses `templates/feature-archive.md` header text, escapes table-breaking newlines/pipes in one-line summary fields, and produces one trailing newline.

### `build_archive_plan`

Location: `scripts/feature_archive_support.py`

Signature:

```python
def build_archive_plan(
    project_root: Path,
    *,
    operation: Literal["archive", "rehydrate"],
    selected_months: Sequence[str],
    selected_feature_ids: Sequence[str],
    as_of: date,
) -> ArchivePlan:
```

Side effects: none.

### `apply_archive_plan`

Location: `scripts/feature_archive_support.py`

Signature:

```python
def apply_archive_plan(
    project_root: Path,
    plan: ArchivePlan,
    *,
    expected_plan_sha256: str,
) -> str:
```

Return: transaction ID after successful post-check and journal cleanup.

Side effects: creates/removes month directories, moves whole feature directories, updates approved Markdown files and `features/archive.md`, creates a temporary transaction journal, and removes the journal only after successful post-check.

### `restore_transaction`

Location: `scripts/feature_archive_support.py`

Signature:

```python
def restore_transaction(project_root: Path, transaction_id: str) -> None:
```

Behavior: load the persistent journal, restore directory moves in reverse order, restore backed-up bytes atomically, run restore check, mark `restored`, then remove the journal. Any incomplete restore leaves the journal and raises `ArchiveContractError("restore", detail)` with the concrete failed path/operation in `detail`.

## File Responsibility Map

### New runtime and template files

| File | Responsibility |
|---|---|
| `scripts/feature_archive_support.py` | Feature IDs, memory-root discovery, archive index, resolver, candidate eligibility, plan/hash, references, journal, apply/check/restore primitives |
| `scripts/scan-feature-monthly-archive.py` | Read-only archive/rehydrate plan CLI and deterministic JSON output |
| `scripts/check-feature-monthly-archive.py` | Read-only pre/post/restore contract validation CLI |
| `scripts/apply-feature-monthly-archive.py` | Human-confirmed expected-hash apply CLI |
| `scripts/restore-feature-monthly-archive.py` | Persistent-journal recovery CLI |
| `templates/feature-archive.md` | Copy-ready `features/archive.md` locator template |

### New native tests

| File | Responsibility |
|---|---|
| `tests/feature_archive_test_support.py` | Temporary target-project builder, feature/requirement/decision/project fixtures, subprocess runner, snapshots |
| `tests/test_feature_archive_support.py` | Feature ID, month, index parsing, resolver, collision, path escape, BOM/CRLF, deterministic plan/hash |
| `tests/test_feature_monthly_archive_scan.py` | Eligible/blocked classification, multi-month plan, reference impacts, no-mutation, rehydrate scan |
| `tests/test_feature_monthly_archive_apply.py` | Whole-directory moves, exact reference edits, archive index, stale-plan, idempotency, post-check |
| `tests/test_feature_monthly_archive_restore.py` | Injected failure, persistent journal, reverse restore, rehydrate, interrupted-process recovery |
| `tests/validate-feature-monthly-archive-runtime.sh` | Coordinated runtime/stage/template/human-gate/source-authority contract |

### Existing code and CI files to modify

| File | Planned change |
|---|---|
| `scripts/checker_support.py` | Add reusable Markdown code-span stripping, canonical JSON/hash, atomic UTF-8/bytes write, and normalized relative-path helpers without weakening existing checkers |
| `scripts/check-adr-requirement-model-trace.py` | Replace one-level Feature Spec regex with resolver-aware flat/month validation; allow `closed` only for a valid existing owner path |
| `tests/test_adr_requirement_model_trace.py` | Add archived closed Feature Spec and missing/mismatched archive-index cases |
| `tests/test_python_checker_contract.py` | Add four archive commands and `feature_archive_support` to stdlib/local-import, runtime guard, help/usage, scan/check-read-only contracts |
| `.github/workflows/cross-platform-checkers.yml` | Run all five new archive suites on Windows/macOS and Python 3.10/current |

### Published runtime and design files to modify together

| File | Planned change |
|---|---|
| `SKILL.md` | Add feature-archive intent/routing, script map, archived-path inspection rule, and Human Gate boundary concisely |
| `references/runtime.md` | Add `feature-archive-maintenance` intent, precedence/routing, triggered stage order, inspection of `features/archive.md`, and no-manual-move stop |
| `references/design.md` | Add directory-only archive model, locator authority boundary, archive/rehydrate state, and core flow placement |
| `references/concepts.md` | Define Feature Monthly Archive, Archive State, Feature Locator, and Rehydrate |
| `references/artifact-rules.md` | Add flat/month layouts, `features/archive.md` ownership, archived/rehydrated distinction, and stable Feature ID rules |
| `references/feature-follow-up.md` | Resolve archive rows during lookback/extended scan and require rehydrate before reopened execution |
| `references/feature-completion-check.md` | Produce a deterministic Archive Readiness record at close without auto-archiving |
| `references/stage-guides.md` | Add complete Feature Monthly Archive entry/read/write/gate/exit procedure |
| `references/workflow-checklists.md` | Add scan, Batch Human Gate, apply/post-check/restore, and rehydrate checklist |
| `references/human-review-summary.md` | Add Feature Monthly Archive Batch Review table with plan hash and restore scope |
| `references/recovery-and-backfill.md` | Treat missing/stale archive rows, stranded journals, dual flat/month locations, and missing target paths as stale memory/recovery signals |
| `references/project-decisions.md` | Allow archived closed Feature Spec owner paths without rewriting accepted decision meaning |
| `references/requirement-management.md` | Preserve Feature ID while updating `Feature Mapping` / `Implemented By` current path after archive/rehydrate |
| `references/project-memory-mode.md` | Add optional archive locator to simple/enterprise memory trees; keep history out of `project.md` |
| `references/project-guidance.md` | Clarify first-level active state versus month archive and canonical scripts |
| `references/document-templates.md` | Add inline archive-index and Batch Review derived templates |
| `templates/notes.md` | Add the Archive Readiness block consumed by scan |
| `templates/root-AGENTS.md` | Add message intent and Stage Map row; bump every managed block revision on the approved 1.3.0 version |
| `references/validation-scenarios.md` | Add archive, blocked mixed month, stale plan, interrupted restore, follow-up rehydrate, and no-content-loss pressure scenarios |

### Human-facing and maintenance evidence files

| File | Planned change |
|---|---|
| `README.md` | Explain directory-only historical archive and locator boundary |
| `Usage.md` | Add trigger phrases, two-stage Human Gate example, archive/rehydrate behavior, and Windows/macOS commands |
| `CHANGELOG.md` | Record implemented 1.3.0 archive capability without version bump |
| `docs/proposal/v1.3.x/feature-monthly-compaction.md` | Change status from accepted design to implemented only after verification/Human Review |
| `docs/reports/agent-loop-v1.3.0-feature-monthly-archive-validation-2026-07-14.md` | Focused RED/GREEN, platform, fixture, recovery, scope, and remaining-risk report |
| `docs/reports/agent-loop-v1.3.0-full-validation-2026-07-14.md` | Required Chinese six-domain full-validation report |
| `examples/login-feature/notes.md` | Add a complete backward-compatible Archive Readiness example for the closed login feature |

Review but do not mechanically rewrite generic `<feature>` paths in `references/e2e-discovery.md`, `references/delivery-contracts.md`, `references/complex-artifacts.md`, `references/external-skill-adapters.md`, and `templates/subagent-brief.md`: active work is rehydrated to flat before execution, so those execution paths remain correct. Add a regression assertion preventing those surfaces from recommending execution inside an archived month directory.

## Task 0: Establish Baseline And Phase-0 Evidence

**Files:**

- Read: `.github/workflows/cross-platform-checkers.yml`
- Read: `docs/reports/agent-loop-v1.3.0-cross-platform-python-script-runtime-validation-2026-07-13.md`
- Read: `AGENTS.md`
- No writes before baseline completes

- [ ] **Step 1: Record the exact workspace boundary**

Run:

```text
git status --short --branch
git log -1 --oneline
```

Expected: branch `alpha/v1.3.0`; unrelated dirty paths remain visible and unstaged. Record them in the new focused report once implementation is authorized.

- [ ] **Step 2: Run the existing native and shell baseline**

Run:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
for test_file in tests/validate-*.sh; do bash "$test_file"; done
```

Expected baseline at plan creation: 36 Python tests PASS and every existing shell contract PASS. A changed count is acceptable only when every pre-existing test still passes and the report records the exact count.

- [ ] **Step 3: Verify remote Windows evidence without guessing**

Preferred command when GitHub CLI is authenticated:

```text
gh run list --workflow cross-platform-checkers.yml --branch alpha/v1.3.0 --limit 10
```

Expected: locate the run containing commit `e49673c`, then inspect all Windows matrix jobs. If no authenticated CLI or remote evidence is available, record `Windows evidence unavailable` and keep Phase 0 blocked; do not claim cross-platform acceptance.

- [ ] **Step 4: Baseline review checkpoint**

Do not edit or commit. If baseline or Windows evidence fails unexpectedly, use `systematic-debugging` before proceeding.

## Task 1: Establish RED Archive Contracts And Fixture Builder

**Files:**

- Create: `tests/feature_archive_test_support.py`
- Create: `tests/test_feature_archive_support.py`
- Create: `tests/test_feature_monthly_archive_scan.py`
- Modify: `tests/test_python_checker_contract.py`

- [ ] **Step 1: Create the temporary target-project builder**

Create `tests/feature_archive_test_support.py` with this public interface:

```python
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from tests.checker_test_support import ROOT


@dataclass
class ArchiveWorkspace:
    project_root: Path

    @property
    def memory_root(self) -> Path:
        return self.project_root / ".agent-loop"

    @property
    def features_root(self) -> Path:
        return self.memory_root / "features"

    def write(self, relative: str, content: str) -> Path:
        path = self.project_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return path

    def feature(self, feature_id: str, *, status: str = "closed", close_complete: bool = True) -> Path:
        root = self.features_root / feature_id
        root.mkdir(parents=True, exist_ok=True)
        self.write(f".agent-loop/features/{feature_id}/spec.md", f"# Feature Spec\n\nStatus: {status}\n")
        task_status = "done" if close_complete else "in-progress"
        self.write(f".agent-loop/features/{feature_id}/tasks.md", f"# Tasks\n\n- Status: {task_status}\n")
        close = (
            "## Feature Close Review\n\nDecision: pass\n\n"
            "## Drift Check\n\nDecision: no-drift\n\n"
            "## Close Record\n\nClosed At: 2026-05-20\nHuman Decision: confirmed\n\n"
            f"## Archive Readiness\n\nClosed At: 2026-05-20\nDelivered Summary: completed {feature_id}\n"
            "Verification: complete\nFeature Close Review: complete\nDrift: resolved\n"
            "Project Memory Impact: none\nOpen Follow-up: none\n"
            if close_complete else "## Close Record\n\nClosed At:\n"
        )
        self.write(f".agent-loop/features/{feature_id}/notes.md", f"# Notes\n\n{close}")
        self.write(f".agent-loop/features/{feature_id}/tests.md", "# Tests\n\nStatus: passing\n")
        self.write(f".agent-loop/features/{feature_id}/plan.md", "# Plan\n\nStatus: closed\n")
        return root


def run_archive_command(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def tree_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def json_output(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    return json.loads(result.stdout)
```

- [ ] **Step 2: Write resolver and deterministic-plan RED tests**

Create `tests/test_feature_archive_support.py` with these exact cases and assertions:

| Test name | Fixture | Assertion |
|---|---|---|
| `test_flat_feature_resolves_without_archive_index` | one flat closed feature | `layout == "flat"`, `month is None`, path is `features/2026-05-08-login` |
| `test_archived_feature_requires_matching_unique_index_row` | one month directory plus one matching row | `layout == "archived"`, month `2026-05`; deleting or duplicating the row raises `archive-index` |
| `test_flat_and_archived_collision_fails_closed` | same Feature ID at both paths | raises `path-collision` |
| `test_month_must_match_feature_id` | ID starts `2026-05`, directory uses `2026-06` | raises `month` |
| `test_archive_index_accepts_bom_and_crlf` | index bytes start BOM and use CRLF | row parses with exact Unicode summary |
| `test_symlink_escape_is_rejected` | archived path symlinks outside project | raises `path-escape` |
| `test_plan_hash_is_stable_across_absolute_roots` | identical relative trees under two temp roots | equal `plan_sha256` |

Use `self.assertRaisesRegex(ArchiveContractError, "archive-index")`, `"path-collision"`, `"month"`, or `"path-escape"` according to the failure row above, and exact `FeatureLocation` equality for success. The archived fixture row must use the accepted columns from `templates/feature-archive.md`; create the same relative tree under two temporary absolute roots and assert equal `plan_sha256`.

- [ ] **Step 3: Write multi-month and no-mutation RED tests**

Create `tests/test_feature_monthly_archive_scan.py` with this representative test body and companion cases for current month, active, blocked, paused, incomplete close, open follow-up, path collision, and rehydrate:

```python
def test_scan_selects_closed_features_across_two_months_and_preserves_blocked(self) -> None:
    with tempfile.TemporaryDirectory() as temp:
        workspace = ArchiveWorkspace(Path(temp))
        workspace.feature("2026-05-08-login")
        workspace.feature("2026-05-22-import", status="paused")
        workspace.feature("2026-06-12-payment")
        before = tree_snapshot(workspace.project_root)
        result = run_archive_command(
            "scan-feature-monthly-archive.py",
            "--project-root", str(workspace.project_root),
            "--operation", "archive",
            "--month", "2026-05",
            "--month", "2026-06",
            "--as-of", "2026-07-14",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json_output(result)
        self.assertEqual(
            [move["feature_id"] for move in payload["moves"]],
            ["2026-05-08-login", "2026-06-12-payment"],
        )
        self.assertIn("2026-05-22-import", [item["feature_id"] for item in payload["candidates"]])
        self.assertEqual(tree_snapshot(workspace.project_root), before)
```

- [ ] **Step 4: Extend the Python command contract in RED**

In `tests/test_python_checker_contract.py`, add:

```python
ARCHIVE_COMMANDS = (
    "scripts/scan-feature-monthly-archive.py",
    "scripts/check-feature-monthly-archive.py",
    "scripts/apply-feature-monthly-archive.py",
    "scripts/restore-feature-monthly-archive.py",
)
```

Update the import allowlist to include `feature_archive_support`; assert all commands exist, call `require_supported_python`, use only standard-library/local imports, and return exit `2` with `usage` when invoked without arguments. Keep the existing checker inventory assertions unchanged.

- [ ] **Step 5: Run RED and preserve the reason**

Run:

```text
python3 -m unittest \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_python_checker_contract -v
```

Expected RED: missing `scripts/feature_archive_support.py`, the four missing CLI files, and missing `templates/feature-archive.md`. The RED must not be an import-path or fixture-construction error.

- [ ] **Step 6: Review checkpoint**

Inspect only the new tests and the contract-test diff. Do not commit; commit remains a separate Human Gate.

## Task 2: Implement Feature Locator, Archive Index, Plan Hash, And ADR Reader Compatibility

**Files:**

- Create: `scripts/feature_archive_support.py`
- Create: `templates/feature-archive.md`
- Modify: `scripts/checker_support.py`
- Modify: `scripts/check-adr-requirement-model-trace.py`
- Modify: `tests/test_adr_requirement_model_trace.py`
- Test: `tests/test_feature_archive_support.py`

- [ ] **Step 1: Add reusable safe-write and canonical helpers**

Add these exact signatures to `scripts/checker_support.py`:

```python
def strip_code_span(value: str) -> str:
    cleaned = value.strip()
    return cleaned[1:-1].strip() if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] == "`" else cleaned


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
```

Import only `hashlib`, `json`, `os`, and `tempfile` from the standard library. Add focused tests proving UTF-8 bytes, replacement, and no leftover temporary file after an injected `os.replace` failure.

- [ ] **Step 2: Create the copy-ready archive index template**

Create `templates/feature-archive.md` exactly with the explanatory authority boundary and these columns:

```md
# Feature Archive

This file locates archived or rehydrated features. Feature specs, tests, notes, requirement sources, and accepted decisions remain authoritative.

| Feature ID | Month | Current Path | Archive State | Closed At | Delivered Summary | Source Requirements | Applicable Decisions | Last Moved At |
|---|---|---|---|---|---|---|---|---|
```

An empty template is valid before the first row; do not use the existing `table()` helper directly because it rejects empty tables. `parse_archive_index()` must parse the header and allow zero rows.

- [ ] **Step 3: Implement immutable models and archive-index parsing**

Create `scripts/feature_archive_support.py`. Use the interface contracts above and these constants:

```python
FEATURE_ID_RE = re.compile(r"^(?P<month>\d{4}-(?:0[1-9]|1[0-2]))-(?P<day>0[1-9]|[12]\d|3[01])-[a-z0-9][a-z0-9-]*$")
MONTH_RE = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")
ARCHIVE_COLUMNS = (
    "Feature ID", "Month", "Current Path", "Archive State", "Closed At",
    "Delivered Summary", "Source Requirements", "Applicable Decisions", "Last Moved At",
)
ARCHIVE_STATES = frozenset({"archived", "rehydrated"})
```

Implement:

```python
def discover_memory_root(project_root: Path) -> Path:
    hidden = project_root / ".agent-loop"
    legacy = project_root / "agent-loop"
    if hidden.is_dir() and legacy.is_dir():
        raise ArchiveContractError("memory-root", "both .agent-loop and legacy agent-loop exist")
    if hidden.is_dir():
        return hidden.resolve()
    if legacy.is_dir():
        return legacy.resolve()
    raise ArchiveContractError("memory-root", "no agent-loop memory root exists", 2)
```

`parse_archive_index`, `render_archive_index`, and `resolve_feature_location` must sort by `(month, feature_id)`, reject duplicate IDs, reject duplicate normalized paths, reject unknown states, verify `rehydrated` points flat, and verify `archived` points to `features/YYYY-MM/<feature-id>`.

- [ ] **Step 4: Implement deterministic plan serialization**

Implement `ArchivePlan.to_payload`, `canonical_bytes`, `computed_sha256`, and `assert_hash`. The payload used for hashing excludes `plan_sha256`; candidate, move, reference-edit, and snapshot collections are sorted by stable tuple keys. Reject expected hashes that do not match `^[0-9a-f]{64}$` with exit `2`; a valid but different hash is `stale-plan` exit `1`.

- [ ] **Step 5: Make ADR Feature Spec references resolver-aware**

Replace the current single-level check at `scripts/check-adr-requirement-model-trace.py` `validate_feature_reference` with:

```python
FEATURE_SPEC_RE = re.compile(
    r"(?:^|/)features/(?:(?P<month>\d{4}-\d{2})/)?(?P<feature_id>[^/]+)/spec\.md$"
)
```

Rules:

- `planned:` accepts flat `features/<feature-id>/spec.md` only;
- existing flat or archived paths must exist and stay confined;
- an archived path requires a matching archive-index row when `features/archive.md` exists;
- `Status: proposed | accepted | closed` is valid for an existing Feature Spec owner;
- `closed` proves historical ownership only and does not authorize new execution;
- an archived month mismatch, missing archive row, duplicate row, or `rehydrated` row pointing to a month path fails.

Add native tests using `features/2026-05/2026-05-08-login/spec.md` plus matching/missing/mismatched index rows.

- [ ] **Step 6: Run GREEN for locator and ADR compatibility**

Run:

```text
python3 -m unittest \
  tests.test_feature_archive_support \
  tests.test_adr_requirement_model_trace \
  tests.test_python_checker_contract -v
bash tests/validate-adr-requirement-model-technical-landing-trace.sh
```

Expected: all selected tests PASS; existing valid/proposed/not-needed ADR fixtures retain their prior conclusions.

- [ ] **Step 7: Review checkpoint**

Run `python3 -m compileall -q scripts tests` and inspect the new public interfaces for name/type consistency. Do not commit.

## Task 3: Implement Read-Only Archive/Rehydrate Scan And Check

**Files:**

- Create: `scripts/scan-feature-monthly-archive.py`
- Create: `scripts/check-feature-monthly-archive.py`
- Modify: `scripts/feature_archive_support.py`
- Test: `tests/test_feature_monthly_archive_scan.py`
- Create: `tests/test_feature_monthly_archive_apply.py` with pre/post-check RED cases only

- [ ] **Step 1: Implement exact eligibility extraction**

Add these pure helper interfaces:

| Function | Exact signature |
|---|---|
| Inspect one candidate | `inspect_feature(memory_root: Path, feature_id: str, as_of: date) -> ArchiveCandidate` |
| Discover first-level features | `discover_flat_features(memory_root: Path) -> Sequence[FeatureLocation]` |
| Discover exact reference edits | `discover_reference_impacts(project_root: Path, moves: Sequence[Move]) -> Sequence[ReferenceEdit]` |
| Build deterministic plan | `build_archive_plan(project_root: Path, *, operation: Literal["archive", "rehydrate"], selected_months: Sequence[str], selected_feature_ids: Sequence[str], as_of: date) -> ArchivePlan` |

`inspect_feature` reads `spec.md`, `tasks.md`, `notes.md`, and `project.md`. It requires `Status: closed`, a concrete `## Close Record`, and this exact `## Archive Readiness` metadata contract:

```md
## Archive Readiness

Closed At: 2026-05-20
Delivered Summary: completed login authentication and verified failure paths
Verification: complete
Feature Close Review: complete
Drift: resolved
Project Memory Impact: complete | none
Open Follow-up: none | FU-001, FU-002
```

`Open Follow-up` must be exactly `none` for eligibility. Existing closed features without the block are classified `missing-archive-readiness`; the Agent may propose a human-reviewed notes backfill from existing close evidence, but scan/apply may not infer readiness. `inspect_feature` records blockers instead of throwing so mixed eligible/blocked months produce one reviewable plan.

Current month is `as_of.strftime("%Y-%m")`. Never call `date.today()` inside planning logic.

- [ ] **Step 2: Implement conservative Markdown reference impact discovery**

Scan UTF-8 Markdown files under project root while excluding `.git`, `.archive-txn`, `node_modules`, `vendor`, `.venv`, `dist`, and `build`. Reject symlinked directories and files outside project root. For files above 2 MiB, add a `skipped_references` blocker instead of reading them.

Support two deterministic edit kinds:

1. literal canonical paths beginning `.agent-loop/features/<feature-id>/` or `agent-loop/features/<feature-id>/`;
2. Markdown inline links and reference definitions inside moved feature files when the old link resolves within project root but outside the moved feature directory.

Preserve anchors and URL query strings with `urllib.parse`; ignore `http`, `https`, `mailto`, and same-document `#anchor` links. Any unparsable candidate containing the old feature path becomes a blocker; do not guess.

Do not rewrite original human requirement source files. Paths under `requirements/<set>/` other than `README.md` and lifecycle-owned index files are recorded as `SkippedReference(classification="immutable-requirement-source")`. Completed proposal/report text that clearly describes a past path may be classified `historical-evidence`; every such row remains visible in the Batch Human Review. Any old-path occurrence that is neither an approved edit nor one of those two preserved classes becomes `unsupported` and blocks apply.

- [ ] **Step 3: Implement the scan CLI**

`scripts/scan-feature-monthly-archive.py` must:

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a read-only Feature Monthly Archive plan")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--operation", choices=("archive", "rehydrate"), required=True)
    parser.add_argument("--month", action="append", default=[])
    parser.add_argument("--feature-id", action="append", default=[])
    parser.add_argument("--as-of", required=True)
    return parser
```

Archive requires at least one month and no feature IDs; rehydrate requires at least one Feature ID and no months. Print `json.dumps(plan.to_payload(), ensure_ascii=False, sort_keys=True, indent=2)` plus one newline. Catch `ArchiveContractError as error`, call `print(f"{error.category}: {error.detail}", file=sys.stderr)`, and exit with `error.exit_code`.

- [ ] **Step 4: Implement the read-only check CLI**

`scripts/check-feature-monthly-archive.py` accepts `--project-root`, `--operation archive|rehydrate|restore`, and `--plan`. It loads UTF-8 JSON, reconstructs/validates `ArchivePlan`, checks current paths, archive rows, snapshots, allowed reference edits, absence/presence of source/target paths appropriate to the operation, and prints a stable PASS summary. It rejects every `unsupported` skipped reference and every remaining durable old-path occurrence; immutable requirement sources and approved historical-evidence rows remain unchanged and are reported separately. It never writes.

- [ ] **Step 5: Prove scan/check are read-only and cross-root deterministic**

Run:

```text
python3 -m unittest \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply -v
```

Expected: scan suites PASS; apply tests that require the missing apply CLI remain RED for the next task. Snapshots before/after scan and pre-check must be byte-identical.

- [ ] **Step 6: Review checkpoint**

Search the two read-only CLIs for `write_text`, `write_bytes`, `mkdir`, `rename`, `replace`, `move`, `unlink`, and `rmtree`; only plan-free pure support imports are permitted. Do not commit.

## Task 4: Implement Expected-Hash Apply, Transaction Journal, Restore, And Rehydrate

**Files:**

- Create: `scripts/apply-feature-monthly-archive.py`
- Create: `scripts/restore-feature-monthly-archive.py`
- Modify: `scripts/feature_archive_support.py`
- Complete: `tests/test_feature_monthly_archive_apply.py`
- Create: `tests/test_feature_monthly_archive_restore.py`

- [ ] **Step 1: Write apply and restore RED cases**

Cover these exact tests before implementation:

| Test name | Required assertion |
|---|---|
| `test_apply_moves_two_closed_features_intact_and_updates_archive_index` | two source dirs disappear, two month dirs exist, file bytes match except approved link edits, two sorted locator rows exist |
| `test_apply_rejects_valid_but_different_plan_hash_without_writes` | exit 1 contains `stale-plan`; full tree snapshot unchanged |
| `test_apply_rejects_state_drift_after_scan` | edit one candidate note after scan; apply exits 1; no journal or move exists |
| `test_apply_updates_only_precomputed_reference_edits` | known project/requirement/decision links change; an unrelated Markdown file is byte-identical |
| `test_apply_is_idempotent_and_never_nests_month_directory` | second scan says `already-archived`; second apply has no moves; nested month path does not exist |
| `test_injected_reference_write_failure_restores_directories_and_bytes` | subprocess exits 1; before/after full snapshots equal; restored journal removed |
| `test_interrupted_transaction_can_be_restored_by_new_process` | leave journal at `moving`, invoke restore CLI, assert original tree and no journal |
| `test_incomplete_restore_keeps_journal_and_fails_closed` | create target collision before restore; exit 1; journal remains with `restoring` state |
| `test_rehydrate_moves_archived_feature_flat_and_updates_locator` | month source disappears, flat target exists, row is `rehydrated`, original `spec.md` remains `closed` |

Use environment variable `AGENT_LOOP_ARCHIVE_FAIL_AFTER=<operation-count>` only inside tests to inject a deterministic failure. Production docs must label it test-only; reject the variable unless `AGENT_LOOP_ARCHIVE_TEST_MODE=1` is also set.

- [ ] **Step 2: Implement the journal schema and atomic backup**

Journal path:

```text
.agent-loop/features/.archive-txn/<transaction-id>/journal.json
.agent-loop/features/.archive-txn/<transaction-id>/backups/<workspace-relative-path>
```

Journal JSON fields:

```json
{
  "schema_version": 1,
  "transaction_id": "20260714T120000Z-0123456789ab",
  "operation": "archive",
  "plan_sha256": "64-lowercase-hex-characters",
  "state": "prepared",
  "moves": [],
  "backups": [],
  "completed_operations": []
}
```

Allowed states: `prepared`, `moving`, `references-updated`, `checking`, `restoring`, `restored`, `verified`. Persist journal state with `atomic_write_bytes` before and after each irreversible step. Backup only files listed in `reference_edits` plus existing `features/archive.md`; record `missing-before` for newly created index files.

- [ ] **Step 3: Implement exact-hash revalidation and archive apply**

The apply CLI uses the same parser fields as scan plus required `--expected-plan-sha256`. It rebuilds the plan from current state, compares the hash before creating `.archive-txn`, then:

1. creates the journal and backups;
2. creates month directories only for confirmed moves;
3. uses `Path.rename()` for same-memory-root directory moves;
4. renders `features/archive.md` from sorted entries;
5. applies exact precomputed `ReferenceEdit` replacements only when current file hash equals `before_sha256`;
6. writes changed files atomically;
7. runs the same post-check core used by the check CLI;
8. marks verified and removes the transaction directory;
9. removes an empty month directory created by a failed transaction during restore.

Any exception after journal creation immediately calls `restore_transaction`; report both the original failure and restore result.

- [ ] **Step 4: Implement rehydrate through the same plan/apply path**

For `operation=rehydrate`, require the archive row state `archived`, source month path, flat target absence, closed feature, and explicit Feature ID selection. Move the whole directory flat, set row `Archive State: rehydrated`, set `Current Path` to `features/<feature-id>/`, update references, and post-check. Do not change `spec.md Status`; Feature Follow-up owns the later `closed -> active` transition.

- [ ] **Step 5: Implement standalone restore CLI**

`restore-feature-monthly-archive.py` accepts only `--project-root` and `--transaction-id`. Validate the ID against `^\d{8}T\d{6}Z-[0-9a-f]{12}$`, confine the journal path, restore moves in reverse order, restore exact backup bytes or remove `missing-before` files, verify the pre-transaction snapshots, then remove the journal. Never infer a transaction ID by choosing the newest directory.

- [ ] **Step 6: Run GREEN including injected failures**

Run:

```text
python3 -m unittest \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply \
  tests.test_feature_monthly_archive_restore -v
```

Expected: every success, stale-plan, injected-failure, restore, idempotency, and rehydrate case PASS; no temporary `.archive-txn` remains after successful or successfully restored tests.

- [ ] **Step 7: Review checkpoint**

Run `python3 -m compileall -q scripts tests`, inspect mutation functions line-by-line, and confirm no delete/archive-content path exists. Do not commit.

## Task 5: Publish Coordinated Runtime, Stage, Gate, Template, And Reader Rules

**Files:**

- Create: `tests/validate-feature-monthly-archive-runtime.sh`
- Modify all published runtime/design files listed in the File Responsibility Map
- Modify: `templates/root-AGENTS.md`
- Modify: `references/validation-scenarios.md`

- [ ] **Step 1: Write the coordinated RED contract first**

Create `tests/validate-feature-monthly-archive-runtime.sh` with `assert_contains` / `assert_not_contains` checks that require:

```text
feature-archive-maintenance
Feature Monthly Archive
features/archive.md
Feature ID is stable
archive state is not feature lifecycle
scan is read-only
expected plan SHA-256
Batch Human Gate
transaction journal
post-check
restore
rehydrate before reopened execution
active / blocked / paused features stay flat
no per-feature archive summary
no historical/
no Deep Archive
no --force
```

Require coordinated mentions in `SKILL.md`, `references/runtime.md`, `references/design.md`, `references/artifact-rules.md`, `references/feature-follow-up.md`, `references/stage-guides.md`, `references/workflow-checklists.md`, `references/human-review-summary.md`, `references/recovery-and-backfill.md`, `templates/root-AGENTS.md`, `references/validation-scenarios.md`, and `templates/feature-archive.md`.

Run:

```text
bash tests/validate-feature-monthly-archive-runtime.sh
```

Expected RED: missing runtime intent/stage/gate/template references.

- [ ] **Step 2: Add routing without creating an ordinary feature stage**

Add `feature-archive-maintenance` to Message Intent. Route it after Safety Stop, Remote Discovery, and Memory Recovery, but before Active Feature Guard because it is maintenance of closed history rather than new/active feature execution. If selected candidates include current active/paused paths, eligibility blocks those candidates; it does not switch active work.

The stage order adds `Feature Monthly Archive If Explicitly Requested` after Re-Adopt/Recovery and before feature construction stages. Auto modes never authorize archive or rehydrate; both stop at their Batch Human Gates.

- [ ] **Step 3: Add the complete stage procedure and checklist**

`references/stage-guides.md` section must state:

```text
Entry: explicit archive/rehydrate request after reliable project memory
Reads: project.md, archive.md, selected feature close artifacts, requirements, decisions, Markdown references
Writes: none during scan; confirmed month moves, archive.md, approved references, temporary journal during apply
Human Gate: exact plan SHA-256 Batch Review
Exit: verified archive/rehydrate, verified restore, or one blocker stage
Next: Chat/report when complete; Ask Human for stale plan/scope; Recovery for stranded journal; Feature Follow-up after verified rehydrate
```

Add the matching checklist and Human Review table. The review table includes operation, plan SHA-256, selected months/IDs, eligible, blocked, moves, reference edits, unchanged content, journal/restore, platform evidence, and decision.

Update `templates/notes.md`, `references/document-templates.md`, and `references/feature-completion-check.md` so close records write the exact `Archive Readiness` block above. This does not auto-archive and does not add a new Close Human Gate. Update `examples/login-feature/notes.md` with a concrete completed block. Regression tests must reject archive eligibility when the block is missing, contains a non-concrete summary, has any value other than the allowed terminal values, or lists an open follow-up ID.

- [ ] **Step 4: Update Feature Follow-up and recovery rules**

Follow-up lookup reads Active/Paused first, flat recent features second, `features/archive.md` third, archived feature artifacts fourth. A confirmed archived owner must rehydrate through its own Human-reviewed plan before Feature Follow-up changes lifecycle or starts execution.

Recovery treats these as stale-memory/safety conditions:

- archive row target missing;
- archived directory without row;
- duplicate flat/month Feature ID;
- `rehydrated` row pointing to month path;
- incomplete `.archive-txn`;
- old path durable references after verified apply.

- [ ] **Step 5: Update root Stage Map and block revision**

Add a row for explicit historical feature archive/rehydrate requests and route to `references/stage-guides.md`, `references/artifact-rules.md`, and `references/feature-follow-up.md`. Update precedence wording consistently. Bump all managed blocks from the current `block-version:1.3.0-20260713.2` to one new full revision value such as `block-version:1.3.0-20260714.1`; use the exact same full value in every managed block and update root-block regression expectations.

- [ ] **Step 6: Add pressure scenarios**

Add at least these scenarios to `references/validation-scenarios.md`:

1. human selects May/June with closed and paused features;
2. plan changes between review and apply;
3. accepted ADR references a closed archived Feature Spec;
4. archived feature owns a day-45 regression and must rehydrate;
5. journal remains after process interruption;
6. duplicate flat/month path and stale archive row;
7. user says “compress” but asks to delete history—route outside this capability;
8. auto mode attempts archive without Batch Human Gate;
9. archive scan under missing controller fallback—read-only discussion only, no apply;
10. reference scanner finds an ambiguous old path and blocks.

- [ ] **Step 7: Run GREEN coordinated contracts**

Run:

```text
bash tests/validate-feature-monthly-archive-runtime.sh
bash tests/validate-feature-monthly-compaction-proposal.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
bash tests/validate-root-agents-block-refresh.sh
```

Expected: all PASS with the new intent, Stage Map, block revision, gate, and preserved proposal boundary.

## Task 6: Publish Human Docs, CI, Changelog, And Current Authority

**Files:**

- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`
- Modify: `.github/workflows/cross-platform-checkers.yml`
- Modify: `tests/test_python_checker_contract.py`
- Modify: `docs/proposal/v1.3.x/feature-monthly-compaction.md`
- Create: `docs/reports/agent-loop-v1.3.0-feature-monthly-archive-validation-2026-07-14.md`

- [ ] **Step 1: Add human trigger and safety examples**

Usage must include this ordinary-language flow:

```text
Human: 把 2026 年 5 月和 6 月已经关闭的 feature 按月份归档。
Agent: runs read-only scan and shows plan SHA-256, eligible/blocked rows, moves, references, unchanged content, and restore scope.
Human: confirms the exact batch.
Agent: applies, post-checks, reports transaction evidence, and does not commit automatically.
```

Add a rehydrate example showing a separate Human Gate before flow-back. README should explain the directory shape and that archive means location/index compaction, not content deletion.

- [ ] **Step 2: Extend native CI**

Append these modules to the workflow unittest command:

```text
tests.test_feature_archive_support
tests.test_feature_monthly_archive_scan
tests.test_feature_monthly_archive_apply
tests.test_feature_monthly_archive_restore
```

Update `test_cross_platform_ci_runs_the_native_suite` to require all four modules and all four archive command paths. Keep Python 3.10/current and Windows/macOS matrix unchanged.

- [ ] **Step 3: Record current-version behavior**

Update the 1.3.0 changelog section with implemented behavior, not proposal promises. Do not alter 1.2.4 historical entries and do not bump the version.

Set proposal status only after fresh verification:

```text
状态：v1.3.0 Release Human Gate 已批准；发布目标 stable-v1.3.0
```

If Windows jobs have not actually run successfully, write `macOS-verified / Windows-test-defined` and do not mark the proposal implemented cross-platform.

- [ ] **Step 4: Write focused validation report from real evidence**

The report must include exact Python/shell counts, RED reasons, eligible/blocked cases, no-mutation hashes, stale-plan evidence, injected-failure restore, rehydrate, platform evidence, Critical/High/Medium findings, scope exclusions, and commit/push authorization status. Do not copy scores from an older report.

- [ ] **Step 5: Run focused GREEN**

Run:

```text
python3 -m unittest \
  tests.test_python_checker_contract \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply \
  tests.test_feature_monthly_archive_restore \
  tests.test_adr_requirement_model_trace -v
bash tests/validate-feature-monthly-archive-runtime.sh
bash tests/validate-feature-monthly-compaction-proposal.sh
```

Expected: all focused suites PASS; scan/check no-mutation and apply/restore fixture cleanup assertions pass.

## Task 7: Full Validation, Review, And Development-Agent Handoff

**Files:**

- Read and follow: `docs/maintenance/full-validation-method.md`
- Create: `docs/reports/agent-loop-v1.3.0-full-validation-2026-07-14.md`
- Review: every file in this plan's responsibility map

- [ ] **Step 1: Run all native Python and shell tests**

Run:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
for test_file in tests/validate-*.sh; do bash "$test_file"; done
```

Expected: zero failures. Record exact counts from output.

- [ ] **Step 2: Run mechanical checks**

Run:

```text
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m compileall -q scripts tests
for shell_file in scripts/*.sh tests/*.sh; do bash -n "$shell_file"; done
for ruby_file in scripts/*.rb; do ruby -c "$ruby_file" >/dev/null; done
git diff --check
```

Run the repository Markdown-fence and JSON parsers used by the prior 1.3.0 full validation. Remove generated `__pycache__` directories after compile checks.

- [ ] **Step 3: Perform six-domain semantic pressure review**

Audit Logic Correctness, Autonomy, Project Entry/Onboarding, Development/Test Workflow, Memory, and Recommendation. Explicitly test routing priority for feature archive versus Active Feature Guard; Batch Human Gate non-bypass; archive state versus lifecycle; rehydrate before execution; stale memory/journal recovery; and no deletion/manual move rationalization.

- [ ] **Step 4: Request code review**

Use `requesting-code-review`. Run Spec Review against every proposal acceptance scenario and Standards Review because the diff changes routing, root guidance, recovery, filesystem mutation, and cross-platform tooling. Fix accepted findings through TDD and rerun all affected plus full tests.

- [ ] **Step 5: Save the full validation report**

Write a Chinese report with real RED/GREEN evidence, exact counts, score, severity totals, unresolved risks, Windows status, unrelated dirty-work boundary, and explicit statement that commit/push/tag/PR remain unauthorized unless the human separately confirms them.

- [ ] **Step 6: Final implementation handoff checkpoint**

Present a table containing proposal coverage, plan tasks completed, tests, platform evidence, review, drift, changed files, unrelated files excluded, remaining risks, and exactly one recommended next stage. Do not commit, push, tag, PR, release, publish, close, or move real project feature directories without the corresponding later Human Gate.

## Expected Commit Decomposition After A Separate Submit Gate

If the human later authorizes commits, prefer these reviewable commits; do not create them during plan execution without the Submit two-stage confirmation:

1. `feat(v1.3.0): 增加 feature 归档路径解析能力`
   - shared locator/index/plan model;
   - ADR archived Feature Spec compatibility;
   - native resolver tests.
2. `feat(v1.3.0): 实现 feature 月度归档事务命令`
   - scan/check/apply/restore;
   - transaction journal, stale-plan, rehydrate;
   - mutation and recovery tests.
3. `docs(v1.3.0): 发布 feature 月度归档工作流`
   - runtime/design/stage/root guidance/templates;
   - human docs, scenarios, changelog, reports;
   - full validation evidence.

Each meaningful commit uses the repository-required Chinese multiline body. Push only to the locally configured remotes explicitly authorized by the human. Do not tag unless separately requested.

## Plan Self-Review

### Proposal coverage

| Accepted proposal requirement | Plan coverage |
|---|---|
| Whole feature directory moves intact | Task 4 apply + file/hash assertions |
| Root `features/archive.md` locator | Task 2 template/parser/resolver |
| Stable Feature ID | Task 2 model and Task 5 artifact rules |
| Only eligible closed historical features | Task 3 eligibility and Task 5 gate |
| Mixed month allowed with blocked feature flat | Task 1/3 fixtures and runtime scenario |
| Follow-up / ADR / Requirement / Project Memory references | Task 2 ADR plus Task 5 coordinated rules |
| Read-only scan and check | Task 3 snapshots and command review |
| Exact Batch Human Gate | Task 5 Human Review and expected plan hash |
| Stale-plan protection | Task 2 hash plus Task 4 apply |
| Persistent failure restore | Task 4 journal and interrupted-process tests |
| Rehydrate before execution | Task 4 behavior plus Task 5 Follow-up routing |
| Windows/macOS standard-library behavior | Tasks 0, 6, and 7 |
| No summary/history/delete/deep archive | Boundary, Task 4 mutation review, runtime negative assertions |

### Type and naming consistency

- CLI operation values are exactly `archive | rehydrate`; check adds `restore` only for validation mode.
- Archive state values are exactly `archived | rehydrated`.
- Feature lifecycle remains `draft | active | blocked | paused | closed`.
- Plan hash field and CLI flag consistently use `plan_sha256` / `--expected-plan-sha256`.
- All target-project paths serialize as POSIX paths relative to project root.
- All dates supplied to deterministic behavior use explicit ISO `YYYY-MM-DD` arguments.

### Risk review

| Risk | Control |
|---|---|
| Reader misses month paths | Reader Compatibility completes and passes before apply exists |
| Human-approved plan drifts | apply rebuilds plan and requires exact SHA-256 |
| Process dies mid-move | journal state and backups persist before mutation |
| Restore destroys new work | file hashes and exact transaction ID gate restoration; mismatch fails closed |
| Relative links change with directory depth | deterministic Reference Impact edits plus pre/post hashes |
| Accepted ADR meaning is rewritten | only locator/path changes; decision content/status/review stays immutable |
| Active feature is archived | eligibility, project memory, lifecycle, and current-month blockers |
| Same Feature ID exists twice | flat/month collision hard failure |
| Cross-platform paths differ | POSIX serialization, explicit dates, standard library, Windows/macOS fixtures |
| Scope expands into content deletion | negative runtime/test assertions and no deletion CLI |

### Placeholder and ambiguity result

The placeholder scan must return no matches for any forbidden incomplete-plan pattern defined by `writing-plans`. If execution discovers a new artifact schema, file boundary, public interface, deletion need, or unsupported reference form, stop at Human Review instead of improvising beyond the accepted proposal.
