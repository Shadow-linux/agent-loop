# Checker Failure Recovery

Use this reference when a canonical Agent Loop checker fails and the failure may come from the checked artifact, the execution environment, or the checker implementation itself.

Feature Definition Review and Implementation Readiness Review do not use a local Feature review Checker. Checker Recovery applies only to other canonical Agent Loop checkers that remain published for structural or freshness contracts; it must never be inserted into the Feature Gate path as a replacement authorization mechanism.

Human decision provenance is not a Checker input that can be repaired. The Agent checks current conversation or preserved Human decision evidence and asks one blocking confirmation only when provenance is genuinely unavailable. Checker Recovery must not manufacture approval or add a local authorization issuer.

Feature Monthly Archive scan output is advisory evidence: ordinary Archive reference findings do not trigger Checker Recovery. The Agent reviews symlink, unsupported-reference, canonical-target, conflict, risk, and recovery evidence directly. Checker Recovery remains available only for an actual canonical implementation contradiction or execution-environment failure, while stranded transactions route to Recovery.

Checker Self-Repair is an internal method of `Diagnose Failure` and `Verify`. It is not a canonical stage, lifecycle, status, Auto Mode, artifact family, or permission to bypass validation.

## Core Rule

The published semantic authority can reveal a defect in its checker implementation, but a modified checker cannot silently approve itself.

The Agent may diagnose a checker defect read-only. Writing or using a temporary checker patch requires an exact Human authorization. The default repair target is an isolated temporary copy, never the installed/global Agent Loop Skill.

## Entry

Enter only after:

1. an exact canonical Agent Loop checker command has run;
2. the same command has been rerun without changing inputs;
3. the Agent has preserved the command, exit status, stdout, stderr, checker path, and checked target;
4. ordinary input/path mistakes are not already sufficient to explain the result.

Then classify:

```text
artifact-invalid | environment-invalid | checker-defect-candidate | unresolved
```

These labels are response-local diagnostic findings, not persistent lifecycle values.

## Classification

### artifact-invalid

Use when the checked artifact violates current published authority and the checker correctly identifies the violation.

Action:

- fix the artifact only through its owning Requirement, ADR, Feature, Bug, Change, guidance, or other existing workflow;
- retain all applicable Human Gates;
- rerun the unmodified canonical checker.

Do not patch the checker merely because fixing the artifact is inconvenient.

### environment-invalid

Use when Python/runtime support, permissions, paths, encoding, missing local support modules, or another capability prevents the checker from evaluating the artifact correctly.

Action:

- repair the environment when already authorized and bounded;
- otherwise report the exact capability gap;
- rerun the unmodified canonical checker.

Do not change validation logic to hide an environment failure.

### checker-defect-candidate

Use when a minimal authority-backed valid fixture fails, or an invalid fixture passes, because checker logic contradicts the current published runtime/reference/template contract.

Candidate is not proof. Reduce the case before requesting a patch.

### unresolved

Use when the available evidence cannot distinguish artifact, environment, and checker responsibility.

Action:

- name the smallest missing evidence;
- run another read-only discriminator when available;
- otherwise ask one focused Human question;
- do not write a checker patch.

## Checker Defect Proof

Before proposing a temporary correction, collect:

| Evidence | Required content |
|---|---|
| Canonical invocation | exact command, target paths, exit status, stdout, stderr |
| Checker identity | path, Agent Loop version or source commit, SHA-256 digest |
| Positive fixture | smallest input that published authority says must pass |
| Published authority | exact runtime/reference/template rule |
| Original behavior | unmodified checker fails the positive fixture for the expected reason |
| Negative controls | at least one invalid input that must remain rejected |
| Artifact integrity | why rewriting the artifact would encode false meaning or a workaround |

If the checker has no determinable published contract, remain `unresolved`; do not let an Agent invent validation meaning.

## Temporary Checker Repair Review

Read-only diagnosis and fixture reduction do not need an extra Gate. Before the first checker/support-file write, present:

| Field | Required content |
|---|---|
| Canonical checker | exact path, version/commit, SHA-256 |
| Original failure | exact command, target, exit status, concise error |
| Published authority | exact rule that the implementation contradicts |
| Defect proof | positive fixture plus negative controls |
| Proposed patch | exact files and semantic change |
| Isolation target | temporary directory by default |
| Permitted use | one exact command and one named Gate |
| Expiry | Gate end or any checker/support/input/authority digest change |
| Rollback | delete isolated copy, or restore a separately authorized in-place preimage |
| Residual | canonical checker remains failed until formal source repair |

The Human decision authorizes only the disclosed write and test scope. It does not authorize Feature, Requirement, ADR, Delivery Contract, project-skill, branch, commit, push, PR, merge, tag, release, publish, installation, production, external, paid, destructive, pause, or close actions.

## Isolation

Use an isolated temporary copy by default:

1. create a bounded OS/project-independent temporary directory;
2. copy only the exact checker and required local support modules;
3. record SHA-256 digests of every copied source;
4. keep target-project artifacts unchanged during checker repair;
5. run the copied checker with the same supported Python runtime;
6. delete the temporary directory when the named Gate ends unless the Human explicitly asks to retain it as evidence.

Do not copy the patched checker into the target project as its permanent validator.

Changing an installed/global Skill in place is not part of the default authorization. It requires a second exact Human decision naming the installed path, preimage digest, backup path, patch, verification commands, scope, expiry, and restore command. Feature Auto-Loop, Task Auto-Run, prior installation approval, and prior temporary-repair approval never authorize an in-place mutation.

## Test-First Temporary Patch

Temporary does not weaken TDD:

```text
copy canonical checker and support
-> run positive fixture against unmodified copy
-> observe expected RED
-> apply the smallest isolated patch
-> run positive fixture and observe GREEN
-> run negative controls and observe rejection
-> run the patched copy against the exact disclosed target
```

The RED must fail because of the suspected checker defect, not a broken fixture, missing import, unsupported Python version, or wrong path.

The patch must not:

- add a general `--force` or bypass mode;
- skip unrelated coverage, state, identity, reference, or safety checks;
- accept all inputs of the affected shape;
- change published product, requirement, ADR, Feature, or project-memory meaning;
- widen supported paths, privileges, external effects, or installation scope;
- modify the canonical installed checker under an isolated-copy authorization.

## Result And One-Gate Substitute

Report both evidence channels:

```text
Canonical validation: failed
Temporary checker recovery: passed | failed
Human substitute decision: accepted-for-this-gate | declined
```

`accepted-for-this-gate` is evidence wording, not a new status or lifecycle.

The Human may accept the temporary result as substitute verification for one named Gate only when:

1. the checker defect proof is complete;
2. RED, GREEN, and negative controls are fresh;
3. the patched run covers the exact target and command;
4. no unresolved product, security, data, permission, migration, destructive, or external-effect meaning is hidden;
5. expiry and rollback are explicit;
6. the residual canonical failure remains visible.

The temporary result does not change the canonical checker to `pass`. A later Gate, target, checker/support digest, fixture, authority, or command requires a new decision or the formally fixed canonical checker.

Any later Submit, Release, Publish, or other action-specific review that relies on this evidence must show the residual canonical failure and the exact Human substitute decision. It receives no inherited authorization.

## Recording

Do not create a mandatory checker-recovery directory or report.

- In a short same-session case, the response-local review and result are sufficient.
- When a current Feature, Bug, Change, Requirement review, ADR review, or guidance review owns the verification, record a compact block in that existing owner.
- When the recovery crosses sessions, is handed off, or reaches a later action-specific Gate while still residual, persist the compact block in the existing owner.

Compact evidence:

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
Upstream Issue URL:
```

Do not persist full temporary directories, unredacted sensitive payloads, or broad command logs.

## Upstream GitHub Issue Reporting

The Agent may prepare a sanitized upstream Issue Draft after checker-defect evidence exists. Drafting is read-only; creating the Issue is an external mutation and requires an independent **Issue Reporting Human Gate** even when Temporary Checker Repair or one-Gate substitute evidence was already accepted.

Before creation, present:

| Field | Required content |
|---|---|
| Repository | exact public GitHub owner/repository |
| Title / body | exact title and complete sanitized body |
| Public evidence | published authority/checker paths, neutral minimal fixture, RED and negative controls |
| Redactions | list of removed credentials, private repository/host/customer names, private absolute paths, payloads, and unnecessary project data |
| Labels / method | exact labels when known and authenticated creation method |
| External effect | one public Issue will be created |
| Explicitly not authorized | repair writes, installed Skill mutation, Feature execution, Git branch/commit/push/tag, PR, release, publish, installation, or synchronization |

Only `create exact issue` authorizes that disclosed submission. `Revise draft` and `keep draft only` do not. Repair authorization does not authorize submission; submission does not authorize repair or any later repository action.

If no authenticated GitHub capability is available, return the exact sanitized draft and the authentication/capability blocker. Do not install a client, request or expose credentials, reuse unrelated authentication, or silently skip reporting. After successful creation, record the Issue URL in the existing compact recovery evidence; do not create a new mandatory artifact.

## Failure And Rollback

If the patch, negative controls, target run, or digest check fails:

1. mark temporary recovery failed;
2. do not use it as substitute verification;
3. delete the isolated workspace or restore only the independently authorized in-place preimage;
4. preserve the original canonical failure;
5. return to `Diagnose Failure`, `unresolved`, or the owning artifact/environment repair.

An incomplete or unprovable restore blocks further in-place mutation. It does not authorize a broader repair.

## Formal Source Repair

Temporary recovery never finishes the checker defect.

Formal repair must:

1. occur in the Agent Loop source repository;
2. retain the minimal failing regression test;
3. update the canonical checker and any genuinely mismatched published authority;
4. run focused and required full validation;
5. pass normal Review and Drift Check;
6. keep commit, push, tag, release, publish, and installation/update as independent Human Gates;
7. rerun the original target with the newly installed canonical checker.

The Agent Loop source repository cannot release a checker fix using only its own isolated temporary patched result. Canonical source tests and the formally changed checker must pass.
