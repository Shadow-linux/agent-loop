# Feature Archive Reference Scan Soft Gate Implementation Plan

**Status:** completed and validated; awaiting Human Review

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans task-by-task. Do not dispatch subagents without separate human authorization.

**Goal:** Make Feature Monthly Archive / Rehydrate scan and check report symlink and uncertain-reference facts without acting as an authorization Gate, while preserving exact-plan, project-boundary, transaction, post-check, and restore correctness.

**Architecture:** Reuse SkippedReference as the deterministic advisory channel. Reference discovery never traverses symlinks; it records project-relative reference-scan-symlink rows and continues through ordinary paths. validate_archive_plan_state verifies the exact current plan and executor boundaries but no longer rejects advisory/unsupported reference findings; the Agent reviews those facts before presenting the existing Batch Human Gate.

**Tech Stack:** Python 3.10+ standard library, unittest, Bash contract tests, Markdown runtime/templates, Git mechanical checks.

---

## File Map

- Modify scripts/feature_archive_support.py for deterministic findings and non-authorizing validation.
- Modify tests/test_feature_monthly_archive_scan.py and tests/test_feature_monthly_archive_apply.py; reuse existing support/restore negative controls for mutation validation.
- Create tests/validate-feature-archive-soft-gate.sh for cross-surface contracts.
- Coordinate SKILL.md, runtime/design, artifact/stage/checklist/Human Review/scenario references, and root guidance.
- Synchronize approved version 1.5.3 in SKILL.md, plugin.json, README.md, Usage.md, CHANGELOG.md, and all 13 root managed blocks.
- Create RED and full-validation reports under docs/reports/.
- Refresh the Proposal and this plan after validation.

## Task 0: Establish Baseline

- [x] Confirm branch, HEAD, and dirty work.

~~~
git status --short --branch
git log -1 --oneline --decorate
git diff --stat
~~~

Expected: branch v1.5.3; only the approved Proposal/plan plus pre-existing cache directories are untracked.

- [x] Run the existing full executable baseline.

~~~
for test_file in tests/*.sh; do bash "$test_file"; done
python3 -m unittest discover -s tests -p 'test_*.py'
~~~

Expected: current Shell and Python suites pass before the focused contract exists.

- [x] Record actual commands, counts, elapsed time, branch, and HEAD in docs/reports/agent-loop-v1.5.3-feature-archive-soft-gate-red-2026-07-28.md.

## Task 1: Add Focused RED Tests

**Files:**

- Modify tests/test_feature_archive_support.py.
- Modify tests/test_feature_monthly_archive_scan.py.
- Modify tests/test_feature_monthly_archive_apply.py.
- Create tests/validate-feature-archive-soft-gate.sh.

- [x] Add an internal-alias fixture:

~~~python
(workspace.project_root / ".agents").mkdir()
workspace.write(
    ".agents/feature-reference.md",
    ".agent-loop/features/2026-05-08-login/spec.md\n",
)
(workspace.project_root / ".claude").symlink_to(
    ".agents", target_is_directory=True
)
~~~

Future assertions:

~~~python
self.assertEqual(result.returncode, 0, result.stderr)
payload = json_output(result)
findings = [
    item for item in payload["skipped_references"]
    if item["classification"] == "reference-scan-symlink"
]
self.assertEqual(findings[0]["path"], ".claude")
self.assertEqual(
    findings[0]["matched_value"],
    "directory:internal:.agents",
)
self.assertEqual(findings[0]["reason"], "not-followed")
self.assertIn(".agents/feature-reference.md", payload["snapshots"])
~~~

- [x] Add separate fixtures for external, broken, cyclic, and symlinked Markdown paths. Assert scan exit 0, deterministic advisory rows, no external absolute target in JSON, no alias traversal, and no mutation.

- [x] Add an apply fixture containing an unsupported reference row bound into the exact plan. Assert check/apply does not reject merely because the advisory exists, while expected SHA-256, journal, move, locator, and post-check remain correct.

- [x] Preserve negative controls for symlinked move source, escaped move target, symlinked reference-edit target, stale SHA-256, and stranded journal. These must still prevent out-of-plan or out-of-project writes.

- [x] Add a focused Shell contract asserting:

~~~
reference findings are evidence, not Checker authorization
Agent decides whether reference coverage is sufficient
exact plan SHA-256 Batch Human Gate remains
Apply cannot write outside the reviewed plan or project
ordinary Archive findings do not trigger Checker Recovery
~~~

- [x] Run focused RED:

~~~
python3 -m unittest \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan \
  tests.test_feature_monthly_archive_apply
bash tests/validate-feature-archive-soft-gate.sh
~~~

Expected: Python fails because _markdown_files still raises path-escape; the Shell contract fails because runtime surfaces lack the soft-Gate rules.

## Task 2: Implement Deterministic Findings

**Files:**

- Modify scripts/feature_archive_support.py.
- Test with support and scan suites.

- [x] Add a private resolver returning the existing SkippedReference type:

~~~python
def _symlink_reference_finding(
    project_root: Path,
    candidate: Path,
    kind: str,
) -> SkippedReference:
    relative = candidate.relative_to(project_root).as_posix()
    try:
        resolved = candidate.resolve(strict=True)
    except RuntimeError:
        resolution, target = "cycle", ""
    except FileNotFoundError:
        resolution, target = "broken", ""
    except OSError:
        resolution, target = "unresolved", ""
    else:
        try:
            target = resolved.relative_to(project_root.resolve()).as_posix()
        except ValueError:
            resolution, target = "external", ""
        else:
            resolution = "internal"
    matched = f"{kind}:{resolution}" + (f":{target}" if target else "")
    return SkippedReference(
        relative,
        "reference-scan-symlink",
        matched,
        "not-followed",
    )
~~~

Catch ordering may adapt for Windows/POSIX differences, but output must remain deterministic and never expose an external absolute target.

- [x] Change _markdown_files to return ordinary Markdown paths and symlink findings:

~~~python
def _markdown_files(
    project_root: Path,
) -> tuple[Sequence[Path], Sequence[SkippedReference]]:
~~~

Prune symlink directories, record them, and do not traverse them. Record symlinked Markdown files and do not read them.

- [x] Seed _discover_reference_impact skipped rows with these findings, scan only ordinary Markdown paths, and retain existing deterministic sorting and plan schema.

- [x] Run:

~~~
python3 -m unittest \
  tests.test_feature_archive_support \
  tests.test_feature_monthly_archive_scan
~~~

Expected: all support/scan tests pass.

## Task 3: Remove Checker Authorization From Findings

**Files:**

- Modify scripts/feature_archive_support.py.
- Test apply/check/restore suites.

- [x] Remove the unsupported-classification rejection from validate_archive_plan_state. Do not replace it with another classification whitelist.

- [x] Keep skipped_references hash-bound in the exact plan. Confirm a changed link/finding produces stale-plan during rebuild.

- [x] Verify Apply still resolves every move and reference-edit through confined project paths, journals before mutation, performs only plan-listed edits, post-checks, and restores on failure.

- [x] Run:

~~~
python3 -m unittest \
  tests.test_feature_monthly_archive_apply \
  tests.test_feature_monthly_archive_restore \
  tests.test_feature_monthly_archive_scan
~~~

Expected: advisory-plan application and all existing path/stale/journal negative controls pass.

## Task 4: Coordinate Runtime Ownership

**Files:**

- Modify SKILL.md.
- Modify references/design.md and references/runtime.md together.
- Modify references/artifact-rules.md.
- Modify references/stage-guides.md.
- Modify references/human-review-summary.md.
- Modify references/workflow-checklists.md.
- Modify references/validation-scenarios.md.
- Modify templates/root-AGENTS.md.

- [x] State that scan/check findings neither authorize nor reject Archive/Rehydrate. Agent judgment owns symlink, unsupported/ambiguous reference, and unrelated-layout review; the exact-plan Batch Human Review remains the action Gate.

- [x] Require the Agent to expose advisory rows, inspect relevant canonical targets and likely reference coverage, explain residual risk, and recommend either the existing Batch Gate or one blocking question.

- [x] State that ordinary Archive findings do not trigger Checker Recovery. Recovery remains for actual implementation contradictions, environment failures, stranded transactions, or executor failures.

- [x] Describe exact-plan, transaction, project confinement, post-check, and restore as executor correctness rather than Archive eligibility.

- [x] Add pressure scenarios for internal alias, external/broken alias, ambiguous old reference, stale advisory plan, and attempted out-of-plan write.

- [x] Keep root guidance concise; do not copy the algorithm into root AGENTS.

- [x] Run:

~~~
bash tests/validate-feature-archive-soft-gate.sh
bash tests/validate-feature-monthly-archive-runtime.sh
bash tests/validate-checker-self-repair.sh
bash tests/validate-root-agents-block-refresh.sh
bash tests/validate-v1.2.4-root-stage-coverage.sh
~~~

Expected: all pass.

## Task 5: Synchronize Version 1.5.3 And Human Docs

**Files:**

- Modify SKILL.md, plugin.json, README.md, Usage.md, CHANGELOG.md, and templates/root-AGENTS.md.

- [x] Change current version-bearing surfaces to 1.5.3.

- [x] Set all 13 managed blocks to:

~~~
block-version:1.5.3-20260728
~~~

- [x] Add a 1.5.3 changelog section describing advisory Archive findings, Agent ownership, unchanged Batch Human Gate, and executor confinement.

- [x] Explain the same behavior in README/Usage without exposing implementation detail.

- [x] Search current surfaces for stale 1.5.2 values while preserving historical reports/proposals/releases.

~~~
rg -n \
  'Version: 1\.5\.2|"version": "1\.5\.2"|block-version:1\.5\.2' \
  SKILL.md plugin.json README.md Usage.md templates/root-AGENTS.md
~~~

Expected: no current-version match.

## Task 6: Focused GREEN And Mutation Validation

- [x] Run every focused test from Tasks 1–5 and record actual counts.

- [x] Mutation: restore the old _markdown_files symlink exception. Expected: internal-alias focused test turns RED.

- [x] Mutation: restore unsupported rejection in validate_archive_plan_state. Expected: advisory-plan apply test turns RED.

- [x] Mutation: bypass a confined-path check on a planned write. Expected: existing path-escape negative control turns RED.

- [x] Restore production code after every mutation and rerun focused GREEN. No mutation may remain in the worktree.

## Task 7: Full Validation And Human Review

- [x] Run all Shell tests with live enumeration.

~~~
for test_file in tests/*.sh; do bash "$test_file"; done
~~~

- [x] Run all Python tests with live enumeration.

~~~
python3 -m unittest discover -s tests -p 'test_*.py'
~~~

- [x] Run mechanical checks.

~~~
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
python3 -m json.tool plugin.json >/dev/null
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n
git diff --check
~~~

Run the repository Markdown fence balance check and record its actual result.

- [x] Perform the six-domain semantic audit from docs/maintenance/full-validation-method.md, including Archive/Rehydrate, Checker Recovery non-trigger, Feature Gates, Project Entry, Requirement/ADR authority, transaction recovery, and Submit/Release independence.

- [x] Write docs/reports/agent-loop-v1.5.3-full-validation-2026-07-28.md in Chinese with actual test counts, elapsed time, RED/GREEN/mutation evidence, platform evidence, remaining risk, version sync, and Git action status.

- [x] Refresh Proposal and plan status truthfully.

- [x] Stop at final Human Review. Do not stage, commit, push, tag, PR, merge, release, publish, or synchronize installed Skills without a new exact authorization.

## Plan Self-Review

- Proposal coverage: Tasks 1–4 cover Scanner facts, Agent judgment, existing Batch Human Gate, no ordinary Checker Recovery, exact-plan execution, transaction journal, rollback, and project confinement.
- TDD order: Task 1 creates and runs genuine RED before production behavior changes.
- Type consistency: implementation reuses SkippedReference; no new payload schema, lifecycle, status, or canonical stage is introduced.
- Scope: Feature Monthly Archive / Rehydrate reference discovery and owning runtime surfaces only; Feature Gate, Project Skill, Requirement, ADR, Bug, and Git semantics remain unchanged.
- Git boundary: branch/version authorization exists; commit/push/tag/release authorization does not.
