# Checker Self-Repair And Temporary Recovery Proposal

**Version:** v1.5.x design line; no version bump is authorized by this Proposal
**Status:** accepted for implementation
**Human Review:** accepted in conversation on 2026-07-25
**Scope:** Agent Loop checker failure diagnosis and one-gate temporary recovery

## 1. Problem

Agent Loop uses canonical Python checkers to protect artifact structure, references, coverage, and state. A checker can still contain a defect. When that happens, a target-project Agent currently has two bad choices:

1. stop even when the artifact is valid; or
2. bypass or modify the checker without a controlled rule.

The first choice blocks correct work. The second weakens the Gate and can silently turn the validator into a self-approved judge.

Agent Loop needs a bounded recovery path that lets an Agent diagnose and temporarily repair a defective checker without pretending the canonical checker passed.

## 2. Accepted Principle

> The Agent may repair the checker long enough to prove the current artifact, but modifying the judge must be explicit, isolated, test-first, reversible, limited to one named Gate, and followed by a formal Agent Loop source repair.

The Agent owns the diagnosis. The human owns the exceptional authorization to use a modified checker as substitute evidence.

## 3. Approaches Considered

### A. Always fail closed until Agent Loop publishes a new version

This preserves strict authority but can block a valid target project for a small checker defect.

**Rejected as the only path.**

### B. Let the Agent patch the installed global Skill silently

This is fast but changes the judge for every project, loses the original failure, and makes rollback and later diagnosis unreliable.

**Rejected.**

### C. Isolated, Human-authorized temporary checker repair

The Agent proves a checker defect with a minimal fixture, copies the exact checker and required local support into an isolated temporary workspace, applies a RED-first minimal patch, verifies positive and negative controls, and asks the human whether that bounded result may substitute for the current Gate.

The canonical result remains recorded as failed. The temporary result is separately recorded and expires after the named Gate.

**Selected.**

## 4. Goals

1. Distinguish invalid artifacts, environment failures, and checker defects before changing anything.
2. Let the Agent create a minimal, isolated checker patch after exact Human authorization.
3. Preserve the canonical checker failure and source digest.
4. Require RED/GREEN evidence and negative controls for the temporary patch.
5. Allow a Human-approved substitute verification for one exact Gate.
6. Avoid mandatory new recovery files when a concise response-local record is sufficient.
7. Require a formal source-repository repair before claiming the canonical checker is fixed.

## 5. Non-Goals

Checker Self-Repair does not:

- silently edit a global or installed Agent Loop package;
- treat every validation failure as a checker bug;
- rewrite the artifact to satisfy a known-wrong checker;
- permit a patched checker to approve its own patch;
- create a new canonical stage, lifecycle, Auto Mode, or persistent status;
- authorize Feature, Requirement, ADR, Delivery Contract, Git, release, publish, production, or destructive actions;
- make a temporary result reusable across Gates, projects, checker versions, or source digests;
- allow an Agent Loop source release to rely on a temporary patched copy of its own checker.

## 6. Internal Flow

Checker Self-Repair is an internal method of `Diagnose Failure` and `Verify`, not a new stage:

```text
Canonical checker fails
-> rerun the same command and preserve full output
-> classify the failure
   -> artifact-invalid: repair the owning artifact through its normal Gate
   -> environment-invalid: repair or report the environment capability
   -> checker-defect-candidate: build a minimal reproducer
-> compare the reproducer with published runtime/reference/template authority
-> checker defect proven?
   -> no: return to artifact/environment repair
   -> yes: present Temporary Checker Repair Review
-> exact Human authorization
-> create isolated temporary checker workspace
-> preserve source checker/support digests
-> verify original copy fails the positive fixture (RED)
-> patch the isolated copy minimally
-> verify patched copy passes the positive fixture (GREEN)
-> verify negative controls still fail
-> run patched copy against the exact target and exact command scope
-> record canonical failure + temporary result + expiry + rollback
-> human may accept the temporary result for one named Gate
-> continue only inside that Gate; retain formal upstream repair as follow-up
```

## 7. Failure Classification

The Agent classifies from evidence, not preference:

| Class | Evidence | Action |
|---|---|---|
| `artifact-invalid` | the artifact violates current published authority and the checker reports it correctly | repair the artifact through its owning workflow |
| `environment-invalid` | Python/runtime/path/encoding/dependency/capability prevents a valid checker run | repair or report the environment; do not patch checker logic |
| `checker-defect-candidate` | a valid authority-backed fixture fails, or an invalid fixture passes, because checker logic contradicts current authority | reduce and prove before asking for temporary repair |
| `unresolved` | evidence cannot distinguish the classes | stop with the smallest missing evidence or one Human question |

These are response-local diagnostic labels, not new artifact lifecycle fields.

## 8. Checker Defect Proof

A checker defect is proven only when all applicable evidence exists:

1. exact canonical command, exit code, stdout, and stderr;
2. checker path, Agent Loop version or source commit, and SHA-256 digest;
3. smallest fixture that demonstrates the mismatch;
4. the published authority that says the fixture should pass or fail;
5. original checker behavior on the positive fixture;
6. at least one negative control that prevents a broad bypass;
7. evidence that changing the target artifact would corrupt accepted meaning or encode a false workaround.

An Agent may investigate read-only without a Human Gate. It may not write a temporary checker patch or alter an installed Skill from diagnosis alone.

## 9. Temporary Checker Repair Review

Before writing the patch, present:

| Field | Required content |
|---|---|
| Canonical checker | exact path, version/commit, SHA-256 |
| Original failure | exact command, target, exit status, concise error |
| Published authority | exact runtime/reference/template rule |
| Defect proof | minimal positive fixture and negative controls |
| Proposed patch | exact files and semantic change |
| Isolation target | temporary directory or separately authorized installed path |
| Permitted use | one exact checker command and one named Gate |
| Expiry | end of the named Gate or any input/checker digest change |
| Rollback | delete isolated copy, or restore exact preimage for an independently authorized in-place patch |
| Residual | canonical checker remains failed until formal source repair |

The default recommendation is an isolated temporary copy. Modifying an installed/global Skill in place requires a second exact authorization naming the installed path, preimage digest, backup, patch, verification, and restore command. Auto modes never grant it.

## 10. Temporary Execution Rules

The Agent must:

- use an OS/project-independent temporary workspace by default;
- copy only the checker and required local support modules;
- keep the target project artifact unchanged during checker diagnosis;
- record the canonical source digest before patching;
- write the failing regression fixture before the temporary implementation;
- verify RED against the unmodified copied checker;
- make the smallest patch that satisfies published authority;
- verify GREEN plus negative controls;
- run the patched checker only against the disclosed target and command;
- delete the isolated workspace when the Gate ends, unless the human asks to retain it as evidence.

The Agent must not:

- replace the canonical checker result with the temporary result;
- add `--force`, skip coverage, weaken unrelated validation, or accept every input;
- reuse a patch after the checker, support file, fixture, target, or authority digest changes;
- copy the temporary checker into the target repository as a permanent validator;
- commit, push, publish, install globally, or release from this authorization.

## 11. Gate Semantics

Default evidence remains:

```text
Canonical validation: failed
Temporary checker recovery: passed | failed
Human substitute decision: accepted-for-this-gate | declined
```

These labels are evidence text, not new lifecycle statuses.

The current named Gate may proceed only when:

1. the checker defect is proven;
2. the temporary patch passes RED/GREEN and negative controls;
3. the human explicitly accepts it as substitute verification for that Gate;
4. no unresolved product, security, data, permission, migration, destructive, or external-effect meaning is hidden by the checker defect;
5. the residual canonical failure is visible at every later action-specific Gate that relies on the result.

A temporary result never changes the canonical checker to `pass`. A later Gate may require the same checker again; that is a new decision unless a formal fixed version is installed.

## 12. Recording Without Ceremony

Do not create a mandatory `.agent-loop/checker-recovery/` directory or standalone report.

- If a Feature, Bug, Change card, ADR review, or Requirement review already owns the verification, record a compact block in that existing evidence owner.
- If the work is short and remains in one conversation, the response-local review and result are sufficient.
- If work crosses sessions, is handed off, or reaches Submit/Release while the residual remains, persist the compact evidence in the current owning artifact.

Minimum compact evidence:

```text
Canonical Checker:
Canonical Result:
Source Digest:
Temporary Patch Scope:
RED / GREEN / Negative Controls:
Temporary Result:
Human Substitute Decision:
Expiry:
Formal Repair Follow-up:
```

## 13. Formal Repair

Temporary recovery does not finish the Checker defect.

Formal repair must:

1. target the Agent Loop source repository;
2. preserve the minimal failing regression test;
3. change the canonical checker and matching runtime/reference/template authority if needed;
4. run focused and required full validation;
5. pass normal Review and Drift Check;
6. use independent commit, push, tag, release, and installation/update Human Gates;
7. rerun the formerly failing target with the newly installed canonical checker.

Inside the Agent Loop source repository, an explicitly authorized checker fix uses the normal source-development workflow. It does not use its own temporary patched checker as release evidence.

## 14. Runtime And Documentation Surfaces

Implementation must align:

- `SKILL.md`
- `references/runtime.md`
- `references/design.md`
- new `references/checker-recovery.md`
- `references/stage-guides.md`
- `references/workflow-checklists.md`
- `references/project-guidance.md`
- `templates/root-AGENTS.md`
- `references/validation-scenarios.md`
- `Usage.md`
- `CHANGELOG.md`
- focused regression tests

No version bump is included without separate Human approval.

## 15. Acceptance Criteria

1. A canonical checker failure cannot be silently bypassed.
2. Artifact, environment, and checker defects have distinct actions.
3. The Agent may investigate without unnecessary Human interruption.
4. A write to a temporary checker requires exact Human authorization.
5. Isolated copy is the default; global/in-place modification is separately authorized.
6. RED, GREEN, and negative controls are mandatory.
7. One exact Human-approved temporary result may substitute for one named Gate.
8. Canonical failure remains visible and reusable authorization is forbidden.
9. No dedicated recovery artifact is required for a short same-session case.
10. Formal source repair and canonical revalidation remain required before claiming Agent Loop itself is fixed.
