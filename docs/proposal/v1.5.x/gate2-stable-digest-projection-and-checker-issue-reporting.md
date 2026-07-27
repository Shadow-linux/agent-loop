# Gate 2 Stable Digest Projection And Checker Issue Reporting

Status: Implemented and fully validated; stable release authorized
Version line: 1.5.1
Approved: 2026-07-27
Upstream issue: https://github.com/Shadow-linux/agent-loop/issues/9

## Problem

Gate 2 currently hashes every byte of `tasks.md` as stable package evidence. Task Done Gate then requires the same file to change checkbox, `Status`, `Review`, and `Drift` fields. A valid first task completion therefore invalidates the Gate 2 Stable Digest and prevents a multi-task Feature Auto-Loop from rotating to the next accepted task.

The same mixed definition/runtime shape exists in optional task detail and test artifacts. A repair limited to the root task ledger would leave Complex Artifact Mode and test-result updates exposed to the same false drift.

Checker Failure Recovery already permits a Human-authorized temporary repair, but it does not yet define a safe upstream GitHub Issue reporting path. Downstream Agents need a bounded way to prove, temporarily repair, and report checker defects without turning a patched checker into its own authority.

## Approved Design

### Digest ownership

`Gate 2 Package Digest` remains `raw-v1`. It freezes the complete reviewed package for Gate 2 review and a later package-only start.

`Gate 2 Stable Digest` gains an explicit algorithm field:

```text
Gate 2 Stable Digest Algorithm: review-definition-v2
```

The v2 digest uses the existing sorted path/digest aggregate. File digests are computed as follows:

| Surface | Stable input |
|---|---|
| `spec.md`, optional `context.md`, contracts and other definition-only stable files | raw bytes |
| `tasks.md`, `tasks/**/*.md` | task-definition projection |
| `tests.md`, `tests/**/*.md` | test-definition projection |
| `plan.md`, `plans/*` | excluded as already rotatable |

### Task definition projection

The projection normalizes only recognized runtime ledger fields:

- task completion checkbox on a `T<digits>` task row;
- root/detail `Updated` and document-level runtime `Status` metadata;
- task `Status`, `Review`, and `Drift` fields;
- Task Done Gate checkboxes and its runtime `Evidence`, `Review`, and `Drift` result fields.

It continues to protect Task ID/count/order/title, Story mapping, Mode, Slice Type, Parent, dependencies, blocking definition, Design Slices, Human Gate, Acceptance, Verification, declared evidence location, barriers, risk, interface, and rollback meaning.

### Test definition projection

The projection normalizes only recognized runtime result fields:

- root/detail `Updated` and runtime `Status` metadata;
- Design Slice Verification Matrix result status;
- Bug Verification Matrix result and evidence-link cells.

It continues to protect Test ID, Story/Task mapping, type, purpose, Given/When/Then, data, environment, commands, assertions, expected evidence, regression/safety definition, and cleanup requirements. Runtime evidence remains owned by Feature `notes.md`; unrecognized edits remain stable drift.

### Fail-closed parsing

Projection is section-aware and field-specific. It is not a global line deletion or broad substring filter. Invalid UTF-8, malformed recognized table rows, duplicate/ambiguous task identity, unsupported algorithms, or unsafe paths fail closed.

### Compatibility

- New Gate 2 evidence uses `review-definition-v2`.
- Explicit `raw-v1` remains readable only as the legacy raw algorithm.
- A missing or unknown algorithm fails closed with an actionable migration message.
- An unchanged legacy raw baseline may be re-recorded as v2 only after an explicit Human review of the exact new algorithm and digest.
- A legacy raw mismatch cannot be silently migrated. It returns to Gate 2 unless preserved evidence proves the exact allowed runtime-only changes and the Human explicitly accepts that migration.
- No command overwrites the Gate 2 baseline automatically and no force/bypass option is added.

### Canonical computation

The checker exposes a read-only digest computation mode using the same projection implementation as `review`, `start`, and `execute`. It prints copyable Package/Stable algorithm and digest lines but never edits Feature artifacts.

## Checker Repair And Upstream Issue Reporting

Checker Self-Repair remains an internal Diagnose Failure / Verify method. A downstream Agent may:

1. rerun and preserve the canonical failure;
2. classify and prove a `checker-defect-candidate` with one positive fixture and negative controls;
3. present Temporary Checker Repair Review;
4. after exact Human authorization, patch an isolated copy by default, or one named installed path with preimage, backup, verification, expiry, and restore details;
5. report canonical and temporary results separately;
6. prepare a sanitized upstream Issue Draft;
7. create the exact GitHub Issue only after an independent Issue Reporting Human Gate.

The Issue Review discloses repository, title, sanitized body, public paths/digests, redactions, labels when known, creation method, and the fact that issue creation is an external mutation. Reports must remove credentials, private repository/host/customer names, private absolute paths, payloads, and unnecessary project data. A submitted issue records its URL in the existing compact recovery evidence.

Issue authorization does not authorize checker writes, Feature work, installed Skill mutation, source commits, push, tag, release, publication, or global synchronization. Repair authorization does not authorize Issue submission. If no authenticated GitHub capability exists, the Agent returns the exact sanitized draft and blocker instead of installing tools, leaking credentials, or silently skipping the report.

## Scope

In scope:

- Stable Digest algorithm/version and projections;
- read-only canonical digest computation;
- legacy fail-closed behavior and migration guidance;
- downstream temporary/in-place repair boundary;
- sanitized GitHub Issue reporting gate and evidence;
- runtime/design/templates/scenarios/tests/human docs alignment;
- focused and full validation for 1.5.1.

Out of scope:

- new canonical stage, lifecycle, status, Auto Mode, or artifact family;
- automatic checker self-update;
- automatic GitHub submission without Human authorization;
- general force/bypass flags;
- automatic source PR, merge, release, or `main` synchronization;
- modifying target-project artifacts during this source repair.

## Acceptance

1. Completing T001 through checkbox/Status/Review/Drift updates does not invalidate `review-definition-v2`.
2. Active Plan Scope may rotate to accepted T002 after the valid T001 completion.
3. Definition changes to tasks, tests, spec, context, or contracts remain rejected.
4. Task/test detail runtime updates follow the same rule without weakening definition protection.
5. Missing/unknown algorithms fail closed; explicit legacy behavior is tested.
6. Digest generation and validation call the same canonical implementation.
7. Checker Recovery lets a downstream Agent perform an exact Human-authorized repair and separately report a sanitized GitHub Issue.
8. Existing Human Gates remain independent.
9. Focused and full validation pass with a Chinese report.
10. Version remains 1.5.1.
