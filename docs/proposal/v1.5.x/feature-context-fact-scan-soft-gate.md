# Feature Context Fact Scan Soft Gate Proposal

**Version:** v1.5.3 development line; no version bump
**Status:** implemented; final Human Review
**Created:** 2026-07-28
**Human Review:** approved in conversation on 2026-07-28
**Scope:** soften Feature Context checker authority without removing Feature Context freshness or existing Human Gates

## 1. Problem

Feature Context Snapshot prevents Tasks, Tests, Plans, execution, and verification from silently relying on stale Requirement or ADR meaning. That invariant remains necessary.

The current `scripts/check-feature-context.py` also acts as a workflow judge. It returns non-zero for every stale digest, cached-field mismatch, unresolved Product Slice reference, pending product review, incompatible lifecycle, or ADR compatibility state. Shell callers therefore stop before the Agent can distinguish:

- a formatting or cached-evidence repair;
- a source change with no Product Slice impact;
- an ordinary semantic review route;
- a genuinely unavailable, ambiguous, or unsafe authority chain.

This couples objective fact collection to workflow authorization and can create Checker Recovery work even when the Agent can safely inspect the evidence and use an existing Gate.

## 2. Accepted Boundary

> Keep Feature Context. The checker collects objective authority and freshness facts. The Agent interprets changed facts and decides whether to refresh, return to an existing Gate, or stop. Only physical or authority-resolution contradictions remain a checker-level hard failure.

The result contract becomes:

| Result | Exit | Meaning |
|---|---:|---|
| `CURRENT` | `0` | authority resolves and recorded context facts match |
| `CHANGED` | `0` | facts differ or need review; Agent must assess impact before relying on the context |
| `BLOCKED` | `1` | authority cannot be resolved safely because of a physical, uniqueness, containment, or existence contradiction |

`REFRESH_REQUIRED` exit `3` is removed from the active runtime contract. Existing Snapshot values using `refresh-required` remain readable and are reported as `CHANGED` until refreshed.

## 3. Checker Responsibility

The checker may determine:

- whether exactly one real memory root exists;
- whether Feature, Requirement, Product, and ADR paths exist and remain inside their physical boundaries;
- whether Requirement README contains one effective-source pointer;
- whether required files are readable;
- recorded versus actual paths, metadata, IDs, anchors, digests, and timestamps;
- whether accepted ADR metadata currently says accepted/current;
- deterministic changed and blocked reason lists.

The checker does not decide:

- whether changed prose has Product Slice impact;
- whether a missing/changed cached field is harmless;
- whether an unresolved Product Slice reference requires repair or Requirement review;
- whether pending lifecycle/review/ADR metadata should route to Product Review, Decision & Design, Gate 1, or Recovery;
- whether Feature Auto-Loop may continue after changed evidence;
- whether Human approval exists beyond reporting the recorded evidence.

## 4. Hard-Failure Boundary

`BLOCKED` is limited to facts that prevent safe authority resolution:

- Feature spec is missing, unreadable, outside the project, outside the accepted memory root, or outside `features/`;
- the project has zero, dual, symlinked, or non-directory memory roots where an existing Feature is being checked;
- Product Requirement Source or Requirement Set pointer is absent;
- Requirement README path escapes the project/requirements boundary, is not `README.md`, or is missing;
- effective Product pointer is absent, duplicated, absolute, escapes its Requirement Set, or resolves to a missing/unreadable file;
- an Applicable Decision path escapes the accepted decisions boundary, is not Markdown, or resolves to a missing/unreadable file.

The following are `CHANGED`, not checker hard failures:

- missing/incomplete Snapshot;
- malformed, legacy, or changed digest/timestamp/freshness metadata;
- cached Requirement/Product/profile/review/decision values disagreeing with resolved authority;
- Requirement lifecycle or Product Review not currently implementation-compatible;
- Product Definition structural or review evidence needing Agent review;
- unknown Product Slice ID/anchor;
- ADR status not accepted or Upstream Compatibility not current;
- changed Product or ADR content;
- recorded `Freshness: refresh-required | blocked`.

The runtime may still stop after a `CHANGED` result. That stop belongs to Agent semantic assessment or the existing owning Human Gate, not to the checker exit code.

## 5. Agent Assessment Contract

After `CHANGED`, the Agent reads the reported facts and only the affected Requirement/ADR sections, then records one assessment:

```text
no-semantic-impact
derived-context-update
feature-definition-impact
decision-impact
unresolved
```

- `no-semantic-impact`: refresh cached evidence and continue inside current authorization.
- `derived-context-update`: repair Snapshot/Tasks/Tests/Plan references, rerun the checker, then continue when `CURRENT`.
- `feature-definition-impact`: return to Requirements Discussion or Gate 1.
- `decision-impact`: return to Decision & Design compatibility review.
- `unresolved`: ask exactly one blocking Human question.

The Agent must not treat exit `0` alone as `CURRENT`; it must read the result prefix. `CHANGED` never authorizes target implementation and never bypasses Product, ADR, Gate 1, Gate 2, Delivery Contract, verification, Git, or lifecycle gates.

## 6. Compatibility

- Existing Feature Context Snapshot structure remains readable.
- Existing raw LF/CRLF digest compatibility remains.
- Existing `Freshness: refresh-required` and `Freshness: blocked` values are advisory input and produce `CHANGED`.
- No bulk migration of target Feature artifacts is required.
- `spec.md` remains the Feature bootstrap and Requirement/ADR Markdown remains authoritative.
- No new canonical stage, message intent, lifecycle, Auto Mode, artifact family, dependency, or executable schema is introduced.

## 7. Coordinated Surfaces

Implementation coordinates:

- `scripts/check-feature-context.py`;
- `tests/test_feature_context.py` and focused contract tests;
- `SKILL.md`;
- `references/design.md` and `references/runtime.md`;
- Feature Context, Product Definition, planning, artifact, project-guidance, stage-guide, checklist, template, and validation-scenario surfaces;
- `README.md`, `Usage.md`, and `CHANGELOG.md`.

Historical Feature Context proposals remain historical evidence and are not rewritten to look as if they originally specified this behavior.

## 8. Required Pressure Scenarios

1. unchanged authority returns `CURRENT / 0`;
2. editorial Product or ADR change returns `CHANGED / 0`;
3. missing/incomplete Snapshot returns `CHANGED / 0`;
4. malformed digest, timestamp, or cached freshness returns `CHANGED / 0`;
5. unknown Product Slice ID/anchor returns `CHANGED / 0` for Agent assessment;
6. pending Product Review, deferred Requirement, proposed ADR, or `review-required` ADR returns `CHANGED / 0` and keeps its owning runtime stop;
7. cached source/profile/decision disagreement returns `CHANGED / 0`;
8. missing/dual/symlinked memory root remains `BLOCKED / 1`;
9. missing/ambiguous/escaping Requirement or Product authority remains `BLOCKED / 1`;
10. missing/escaping/non-Markdown ADR authority remains `BLOCKED / 1`;
11. Checker never mutates target artifacts;
12. runtime text forbids interpreting `CHANGED` as execution authorization;
13. Gate 1, Gate 2, ADR acceptance, Delivery Contract, TDD, Task Done, Submit, and Close remain unchanged.

## 9. Acceptance Criteria

1. Feature Context authority and freshness checks remain mandatory before downstream reliance.
2. Checker hard failure is limited to physical/authority-resolution contradictions.
3. Changed or semantically questionable evidence is visible but exits successfully as `CHANGED`.
4. Agent performs and records the semantic impact decision.
5. `CHANGED` cannot silently authorize execution or bypass an existing Gate.
6. Existing Snapshot files need no bulk migration.
7. Focused RED/GREEN proves both the softened positive cases and retained physical negative controls.
8. Full Shell/Python, mechanical checks, and six-domain semantic validation pass on the final combined worktree.
9. Skill version remains `1.5.3`.
10. No commit, push, tag, release, publish, installed-Skill sync, branch, or worktree action is implied.
