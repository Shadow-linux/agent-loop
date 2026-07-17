# Human-Guided Bug Management

## Purpose And Scope

Bug Management is the internal Bug Intake / Triage method of `Feature Follow-up / Flow-back`. It gives a reported problem a stable, deduplicated, recoverable identity while reusing the existing Requirement and Feature workflows.

Load this reference when the human explicitly asks to record, manage, investigate, or fix a bug, regression, failed test, QA finding, production symptom, or post-close defect. Ordinary chat, a request to explain an error, and read-only log interpretation do not create a Bug artifact by default.

Bug Management is not a canonical stage and does not add a message-intent value. The owning intent remains `feature-follow-up`; Project Entry and memory recovery still run first when reliable Agent Loop memory is unavailable.

## Concepts And Authority

The authority split is strict:

| Artifact | Owns | Does Not Own |
|---|---|---|
| Bug Report | one intake event and its source evidence | a new stable Bug identity by itself |
| Bug Record | stable identity, observed facts, provenance, evidence, lifecycle, Resolution Path, relationships, verification, close, and reopen history | product meaning, Requirement lifecycle, Feature implementation, personnel assignment, or Git authority |
| Requirement | product goal, accepted expected behavior, business rules, acceptance direction, and Delivery Phase | Bug investigation or repair progress |
| Feature / maintenance-fix | repair scope, spec, tasks, tests, plan, code execution, verification, review, and drift | Bug report history or the long-lived Bug identity |

The published concepts are Bug Report, Bug Record, Report Origin, Bug Evidence, Expected Behavior Evidence, Resolution Path, Bug Status, Bug Resolution, Reopen Record, and Bug Ownership Lookback.

One or more Bug Reports may belong to one Bug Record. One Bug may relate to zero or more Requirements, Features, Decisions / ADRs, Delivery Contracts, and tests. A Bug has exactly one current Resolution Path. One coherent Feature may resolve multiple Bugs, but each Bug keeps its own identity, verification evidence, Resolution, close decision, and reopen history.

## Artifact Layout

Create the Bug management line only in a target project and only after explicit bug-record, manage, investigate, or fix intent:

```text
.agent-loop/
  bugs/
    INDEX.md
    YYYY-MM-DD-<bug-slug>/
      README.md
      evidence/                 # optional
```

Use a stable identity:

```text
Bug ID: BUG-YYYYMMDD-<slug>
Bug Path: .agent-loop/bugs/YYYY-MM-DD-<bug-slug>/
```

When the same date and slug already exist, append a stable sequence such as `BUG-20260715-login-timeout-02`; never overwrite the prior record.

`bugs/INDEX.md` is the inventory, backlog, and locator. Each Bug ID has exactly one row and the row mirrors current README status, Resolution, Severity, Priority, Resolution Path, Target, and Last Updated. Closed Bugs remain indexed and `deferred` remains open inventory. The Index never owns full reproduction steps, logs, discussion, or Feature tasks.

The Bug README is the coordination source of truth for that Bug. Optional `evidence/` stores bounded local evidence such as redacted logs, screenshots, failure outputs, or test results. Do not copy secrets, tokens, personal sensitive data, or complete production payloads.

Bug artifacts do not own tasks, tests, plans, or code execution.

## Bug Identity And Duplicate Rules

Bug identity depends on evidence, not title similarity. Prefer one Bug when Expected Behavior is the same, Observed Behavior has the same failure semantics, the affected product boundary or repair root cause is shared, or a closed Bug has recurred in the same scope. Split Bugs when expected behavior, repair effect, user/product boundary, or verification closure is independent.

Before creating a record:

1. scan all `bugs/INDEX.md` metadata for open, deferred, in-progress, verifying, and closed candidates;
2. compare Expected Behavior, Observed Behavior, paths, APIs, models, UI, jobs, tests, environment, and evidence overlap;
3. check closed candidates for recurrence;
4. inspect evidence-ranked recent or archived Feature candidates;
5. check Requirement, Decision / ADR, Delivery Contract, and test authority.

Bug identity does not use a time cutoff.

If duplicate evidence is conclusive before the new record is written, append the new Bug Report and evidence to the canonical Bug. Do not create an empty duplicate record.

If an existing record is later confirmed as duplicate, preserve its origin and evidence, set `Resolution: duplicate`, record one valid `Duplicate Of` canonical Bug ID, append the change to Status History, and use the Bug Close Gate. Never delete or silently merge directories. Ambiguous matches remain `triaging` with `Path: investigate-first`; a similar title is insufficient.

## Report Origin

The exact Origin Type values are:

```text
person | customer | group | qa | monitoring | automated-test | agent | external-ticket | other | unknown
```

Report Origin is provenance only. `Origin Reference`, `Intake Channel`, and `Source Link` are optional. `unknown` is valid and must not block triage, investigation, repair, or verification.

Origin never implies Owner, Assignee, permission, customer repair line, Priority, branch type, or responsibility. Later provenance is appended as evidence; it does not replace the original report history.

## Expected Behavior Evidence

A Bug is a claim that observed behavior differs from expected behavior. The Agent must not confirm that claim from inference alone.

Expected Behavior may come from:

- current explicit human product clarification;
- accepted Requirement or Delivery Phase acceptance;
- accepted Decision / ADR or Delivery Contract;
- accepted owning Feature Spec and tests;
- stable product or domain rule;
- previously verified behavior.

Use this precedence when sources conflict:

```text
current explicit human product decision
> accepted Requirement / effective follow-up
> accepted Decision / ADR / Delivery Contract
> accepted Feature Spec and tests
> current verified code/runtime behavior
> Agent inference
```

Code reality proves observed behavior but does not by itself prove correct product expectation. Missing, conflicting, or changed expected behavior returns to Requirements Discussion, Requirement Conflict Review, Requirement Reconciliation, or Decision & Design as applicable; it does not create a guessed repair Feature.

## Status And Resolution

Bug Status and Bug Resolution are separate axes.

```text
reported | triaging | confirmed | in-progress | verifying | deferred | closed
```

```text
unresolved | fixed | duplicate | not-a-bug | cannot-reproduce | accepted-risk | superseded
```

Status transitions:

```text
reported -> triaging
triaging -> confirmed | verifying | deferred
confirmed -> in-progress | deferred
deferred -> confirmed | in-progress
in-progress -> verifying | deferred
verifying -> closed | in-progress | triaging
closed -> triaging | confirmed through the Bug Reopen Gate
```

Rules:

- `closed` must not use `Resolution: unresolved`;
- a non-closed Bug must not be presented as finally complete;
- `deferred` is not `closed` and cannot be rationalized as `accepted-risk`;
- `duplicate` requires one canonical Bug ID and preserved source history;
- `not-a-bug` requires accepted Expected Behavior Evidence;
- `cannot-reproduce` requires environment, inputs, methods, attempts, and missing-evidence details; one failed attempt is insufficient;
- `accepted-risk` requires impact, risk, mitigation, and an explicit human decision;
- `superseded` identifies the replacing Bug, Requirement, or product scope;
- reopening appends a Reopen Record, restores `Resolution: unresolved`, and preserves the old Close Record.

An `in-progress` Bug requires `flow-back | linked-feature | maintenance-fix` plus one Human-confirmed Fix Feature Target. `investigate-first`, `requirement`, and `no-fix` do not represent Feature repair execution and must remain in another valid non-`in-progress` state until their own evidence or gate changes the path.

## Severity And Priority

Severity describes evidence-backed impact. Priority describes the human-decided order of work.

```text
Severity: unknown | low | medium | high | critical
Priority: unset | low | medium | high | urgent
```

The Agent may recommend Severity and uses `unknown` when evidence is insufficient. Priority defaults to `unset`; `urgent` requires an explicit human decision. Severity, Priority, report tone, customer identity, or source type never authorizes hotfix, branch, deploy, release, or publish actions.

## Requirement Relationships

Bug-to-Requirement is an optional `0..N` relationship:

```text
Requirement Impact: none | violates-accepted-behavior | ambiguity-found | change-required
```

A Bug may cite multiple Requirements when the evidence crosses product boundaries. A technical defect may cite no Requirement and instead rely on Feature, test, ADR, Delivery Contract, or runtime evidence.

Requirement artifacts continue to own product meaning. A Bug does not rewrite immutable Requirement sources and does not automatically change Requirement lifecycle. Only current evidence showing that delivery truth is inaccurate may trigger Human-gated Requirement Reconciliation. Product meaning changes use an append-only follow-up or a new Requirement Set.

Post-Merge Memory Reconciliation preserves Bug identity, Status/Resolution separation, verification/close evidence, and append-only status/reopen history. Merged Feature tests or a completed Memory Merge Report do not close/reopen a Bug or satisfy its existing Human Gates.

## Resolution Path And Feature Repair

The exact Resolution Path values are:

```text
investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix
```

Use one current path:

| Path | Use | Required target/action |
|---|---|---|
| `investigate-first` | evidence, duplicate identity, root cause, or expectation is unclear | one concrete investigation action; no Feature creation |
| `flow-back` | accepted behavior belongs to an existing owning Feature | one owning Feature; Human-gated rehydrate/reopen before execution when needed |
| `linked-feature` | repair is an independent coherent delivery scope | one Human-confirmed new linked Feature |
| `maintenance-fix` | narrow internal correction has no product Feature owner | one Human-confirmed `Feature Type: maintenance-fix` workspace |
| `requirement` | expected behavior is missing, conflicting, or changing | one Requirements Discussion / Requirement target before any repair Feature |
| `no-fix` | duplicate, not-a-bug, cannot-reproduce, accepted-risk, or superseded disposition candidate | candidate Resolution evidence, verification, and Close Gate |

`flow-back`, `linked-feature`, `maintenance-fix`, and `requirement` require one valid Target. `investigate-first` and `no-fix` may temporarily omit Target only when their next investigation action or candidate Resolution evidence is concrete.

All code repairs use an existing/reopened Feature, linked new Feature, or `Feature Type: maintenance-fix`. Feature artifacts own spec, tasks, tests, plan, TDD, implementation, verification, Review, Drift Check, and close. Bug confirmation and Resolution Path selection never authorize Feature creation/reopen.

## Bug Identity Scan And 90-Day Feature Ownership Scan

Bug identity and Feature ownership use different discovery bounds:

```text
all Bug Index metadata
-> recent 90-day Feature metadata / summary scan
-> evidence-ranked candidate deep read
-> evidence-triggered extended scan beyond 90 days
```

Default Feature ownership lookback is 90 calendar days.

The default scan reads Active / Paused pointers, flat Feature metadata, and `features/archive.md`, then compares Feature ID, lifecycle, scope summary, paths, APIs, models, tests, and verification references. It deep-reads only candidates with evidence overlap. Calculate age from Feature `Last Updated` / `Closed` facts, never archive month, directory mtime, or archive-operation time.

The 90-day setting is not a hard ownership boundary. A named Feature ID or overlapping path, API, model, test, UI, job, Requirement, or ADR evidence triggers an extended scan and records `outside-default-window`. Multiple medium/high candidates remain `investigate-first`; recency does not authorize an arbitrary owner.

`project.md` may hold a human-confirmed override to the default metadata window. An override changes initial scan breadth only and never disables evidence-driven extended scanning.

## Archived Feature Discovery And Rehydrate Boundary

Archive changes location, not Feature identity or ownership.

Resolve archived candidates through the unique valid `features/archive.md` locator row. The locator only maps Feature ID to current path; it does not own scope, acceptance, lifecycle, or verification.

After the locator is verified, read-only discovery may inspect archived `spec.md`, `tests.md`, `notes.md`, close evidence, and verification evidence. Discovery and Human Review do not require rehydrate.

Only after the human confirms `flow-back` and before the owning Feature is reopened or code repair begins may the Agent run the read-only rehydrate scan, present the exact expected plan SHA-256 Batch Human Gate, apply through the transaction journal, post-check, and restore on failure.

Stop and enter Recovery for a missing/ambiguous locator, flat/month collision, archived directory without a row, `rehydrated` row pointing to a month path, invalid target, or stranded transaction. Never guess or manually move the directory.

## Verification, Close, And Reopen

Feature verification writes candidate Bug evidence. Passing Feature tests may move an `in-progress` Bug to `verifying`, but it does not close the Bug. Bug-specific evidence must trace the original reproduction or accepted substitute, regression/safety coverage, review, drift result, remaining risk, and the candidate Resolution.

Failed Bug-specific verification returns to `in-progress` when the repair is still valid or `triaging` when expected behavior or diagnosis was invalidated. Preserve the failed evidence.

The Bug Close Gate requires complete evidence plus an explicit human decision for the named Bug and Resolution. Feature close and Bug close are separate decisions; one is not inferred from the other. A Bug may remain `verifying` while the human asks for more evidence.

The Bug Reopen Gate requires a named closed Bug, trigger report, new evidence, return status (`triaging` or already-proven `confirmed`), and explicit human decision. Append the Reopen Record, restore `Resolution: unresolved`, and retain the original Close Record and Status History.

## Human Gates And Auto Mode Stops

Keep these action-specific gates:

| Gate | Action requiring explicit confirmation |
|---|---|
| Resolution Path Gate | `flow-back`, `linked-feature`, `maintenance-fix`, `requirement`, or `no-fix` disposition |
| Feature Reopen / Creation Gate | reactivate a closed Feature or create a Feature workspace |
| Requirement Gate | create Requirement, change product meaning, or reconcile lifecycle |
| Delivery Contract Gate | create, accept, or breaking-change a contract |
| Bug Close Gate | accept Resolution and close one named Bug |
| Bug Reopen Gate | reopen one named closed Bug and restore `unresolved` |
| Branch / Submit / Integration / Cleanup / Release gates | create, switch, merge, delete, push, tag, commit, PR, release, or publish |

One Human Review Summary may present several named decisions, but each authorization is separate. “Fix it”, “continue”, Bug confirmation, accepted Requirement, plan acceptance, successful tests, Feature close, commit/push approval, or Auto Mode must not be reused as another gate.

Strict Mode, Feature Auto-Loop, and Task Auto-Run all stop for Bug close/reopen, Feature create/reopen, Requirement creation/lifecycle change, Delivery Contract actions, archive/rehydrate apply, and every Git/release/publish action.

## Project Memory And Recovery

`bugs/INDEX.md` owns Bug inventory, backlog, and locator state in both simple and enterprise memory modes. `project.md` may store only the configurable Feature Follow-up Lookback and ordinary Current Work pointers; it must not contain Open Bugs, Deferred Bugs, Bug assignment lists, reproduction logs, or the Bug backlog.

Project Entry / Re-Adopt may read Bug Index to discover `in-progress`, `verifying`, and `deferred` facts. These facts do not replace the one Active Feature invariant; multiple open Bugs can coexist while only one Feature is active.

Fail closed when:

- Bug Index and README identity, Status, or Resolution disagree;
- `Duplicate Of` is missing, nonexistent, self-referential, or cyclic;
- `closed` uses `unresolved`, or reopen history overwrites close history;
- `in-progress` has no valid Resolution Path or Target;
- Fix Feature cannot be resolved through a flat path or valid archive locator;
- Requirement, Feature, ADR, Delivery Contract, or Expected Behavior authorities conflict;
- verification relies only on an expired external URL with no local understandable summary.

Record the mismatch and recommend exactly one Recovery, investigation, or human decision. Do not infer a state transition.

## Branch And Submit Integration

Bug Management owns Bug identity, lifecycle, and Resolution Path. Branch Management consumes only the Human-confirmed Fix Feature and Target Release Context.

The integration order is:

```text
confirmed Bug
-> Human-confirmed Resolution Path
-> Human-confirmed Fix Feature
-> Target Release Context
-> bugfix/hotfix recommendation if applicable
-> independent Branch Action Gate
```

Severity, Priority, Origin, Bug confirmation, Resolution Path, or Feature plan do not select a Git work type automatically or authorize any mutation. A sealed release remains immutable; repair targets a human-confirmed new patch context. Customer-specific delivery preserves customer isolation and must not reverse-merge the entire customer aggregation line into the standard product.

Submit / Integrate shows related Bug IDs, current Status, candidate Resolution, verification evidence, unresolved close decisions, Target Release Context, and branch isolation. Submit, commit, or push approval does not close a Bug; Bug Close approval does not authorize submission.

## Forbidden Scope

First-version Bug Management does not add:

- a canonical stage or message-intent value;
- Bug-owned `tasks.md`, `tests.md`, `plan.md`, execution directories, or code workflow;
- Owner, Assignee, personnel permissions, staffing, SLA, sprint, workload, story points, or performance reporting;
- an executable YAML/JSON schema, database, mandatory checker, or third-party runtime dependency;
- automatic Priority, hotfix, branch, Feature, Requirement, lifecycle, close, reopen, commit, PR, merge, release, tag, or publish decisions;
- external Issue Tracker creation or bidirectional synchronization;
- Bug archive, compaction, retention, deletion, or scheduled maintenance;
- Security Incident, Production Incident, or Customer Support management;
- worktree / branch memory merge.

External Issue references remain Report Origin evidence only. Existing Requirement, Feature, Delivery Contract, Feature Archive, Branch, Submit, Close, and publication gates remain intact.
