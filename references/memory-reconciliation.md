# Post-Merge Memory Reconciliation

Use this internal Submit / Integrate method only after code integration is complete and verified. It makes Target memory read like one person's current understanding of the merged project. It is not a canonical stage, a Git merge engine, or a routine audit of `.agent-loop/`.

## Core Rule

```text
Verified Code Merge
-> Is there an Observed Memory Conflict?
   -> no: reconciliation-not-needed
   -> yes: inspect the conflict and minimum direct evidence
      -> facts determine one current meaning: Agent rewrites and verifies it
      -> facts support multiple meanings: ask the human to choose
-> continue to the next independently authorized Git/lifecycle gate
```

Memory Reconciliation does not perform the code merge.

No observed conflict means no scan, no Memory Merge Report, no reconciliation Human Gate, and no blocker for a separately authorized commit, push, release, publish, or Source cleanup.

## What Counts As An Observed Memory Conflict

Enter conflict-driven reconciliation when current evidence shows at least one concrete contradiction:

- Git reports a conflict inside the accepted Agent Loop memory root;
- two merged memory claims assign incompatible current meanings or lifecycle states to the same stable ID;
- a changed locator, mapping, or index points at a missing, duplicate, or incompatible canonical owner;
- merged code, tests, configuration, or fresh environment evidence directly invalidates a current Agent-maintained memory claim;
- a targeted check of changed memory finds a broken direct reference caused by this merge;
- Source and Target both changed the same semantic owner and their meanings cannot coexist.

These are not entry signals by themselves:

- Source and Target changed different memory files;
- a Source-only Requirement, Feature, Change, Bug, Decision, or evidence artifact merged cleanly;
- a memory file was unchanged and has not recently been audited;
- unrelated drift might exist somewhere else;
- full Base/Source/Target/Result hashes have not been assembled.

Do not manufacture a conflict to justify reconciliation.

## Current-Understanding Model

The Target branch is the current workspace, not a universal winner. Resolve each observed conflict from:

```text
current Target understanding
+ Source facts already integrated by the code merge
+ latest verified implementation / test / config / environment facts
+ accepted Requirement / Product / ADR / Human Decision constraints
+ valid historical evidence that must remain preserved
```

Use latest verified facts for the disputed question, not the newest Markdown timestamp or the branch side that happened to merge last.

Use the authority that owns the disputed question:

| Question | Primary authority |
|---|---|
| What did the human originally provide? | immutable human source and provenance |
| What product behavior is accepted? | effective accepted Requirement / Product Definition and Human Decisions |
| What technical decision is accepted? | effective accepted ADR and supersession evidence |
| What is implemented now? | merged code, tests, configuration, generated/runtime evidence |
| What is currently active, closed, or located where? | canonical lifecycle owner plus current project evidence |
| What is true in an environment? | fresh bounded environment evidence plus accepted policy |

Code proves implementation reality, not product correctness. If implementation contradicts accepted product or technical authority, preserve that authority and expose the contradiction instead of silently rewriting it to match code.

## Scope Boundary

Inspect only:

1. the observed conflict location or stable ID;
2. the canonical owner of the conflicting meaning;
3. the minimum direct references, locators, or derived indexes that will become wrong when the owner changes;
4. the minimum code, test, config, environment, Requirement, ADR, history, or Human Decision evidence needed to decide the conflict.

Do not inventory or ask the human to review:

- unchanged memory files;
- all paths from historical snapshots;
- file hashes unrelated to an actual rewrite;
- meaningful absence across the whole memory root;
- mechanical `保留` decisions;
- speculative drift outside the conflict's dependency boundary.

If targeted inspection notices unrelated drift, report it separately as a possible Recovery item. Do not expand the current merge reconciliation unless that drift is necessary to understand the observed conflict.

## Agent Resolution Rules

The Agent owns semantic reconciliation before asking the human:

| Situation | Agent action |
|---|---|
| One claim is stale and facts prove the current claim | rewrite the stale current-state claim |
| Both claims are compatible and independently useful | combine or retain them without Human Review |
| Both claims are stale but a third verified fact is authoritative | rewrite to that verified fact |
| A directly affected derived index or locator is stale | recalculate only that index or locator |
| Implementation conflicts with accepted Requirement / ADR / Human Decision | preserve accepted meaning and report implementation drift |
| Customer or release context proves one claim is branch-local | keep it isolated from the standard Target memory |
| Multiple meanings remain legitimate or evidence is missing | present concrete alternatives to the human |

Every automatic rewrite records the conflict, evidence, changed owner/reference, targeted verification, and rollback. It does not require a separate reconciliation Human Gate when it is deterministic, bounded to the conflict, reversible, and verified.

Only unresolved semantic choices require Human Review. Present the smallest set of real options, one recommendation, the evidence gap, and the consequence of each choice. For a small conflict, conduct this review directly in the conversation; do not create a file merely to ask or record one bounded answer. Do not ask the human to approve unchanged files or an all-path plan.

## Conflict Report

Create `<memory-root>/memory-merges/MM-<merged-code-short-sha>-<conflict-topic>/README.md` only when:

- several coupled conflicts or rewrites need a durable shared review surface;
- the work must survive context/session handoff;
- recovery/rollback evidence is too substantial to remain safely in the owning Feature/Change/submit record; or
- the human explicitly asks to retain a report.

Use `templates/memory-merge-report.md`. The report contains only observed conflicts, minimum direct evidence, actual rewrites, directly affected references/indexes, targeted verification, rollback, unresolved choices, and unrelated drift noticed incidentally.

A small conflict is reviewed in the conversation. A small deterministic correction may be recorded in the owning Feature/Change/submit evidence when that already provides durable conflict, diff, verification, and rollback context. Do not create a report merely because a merge occurred or one Human answer was needed.

## Safe Rewrite And Verification

Before a targeted rewrite:

- confirm the accepted memory root and current merged HEAD;
- preserve immutable human sources, accepted authorities, and append-only history;
- avoid symlink traversal, path escape, implicit root migration, customer leakage, and unrelated dirty work;
- capture the exact preimage of only the files to be changed;
- compute the exact intended postimage bytes before mutation;
- keep a bounded backup of only the changed preimages until targeted verification passes;
- write through a same-directory temporary file and atomically replace the owner file.

After the rewrite:

- verify the changed files match the intended postimages byte-for-byte;
- re-read the resolved owner and directly affected references/indexes;
- run the smallest relevant structural and semantic checks;
- prove the original observed conflict no longer exists;
- confirm no unrelated file changed;
- restore only this rewrite from captured preimages if verification fails.

Memory Reconciliation scripts never execute commands or hooks stored in a report or memory artifact.

## Git And Lifecycle Separation

The ordering remains:

```text
Code Merge Gate -> Post-Merge Memory Reconciliation -> Memory Commit Gate -> Push Gate -> Release Gate -> Source Branch Cleanup Gate
```

`reconciliation-not-needed` and a successfully verified targeted resolution allow only presentation of the next independent gate. They do not authorize commit, push, PR, merge, tag, release, publish, branch deletion, or cleanup.

An unresolved observed conflict or failed restore blocks later mutation because Target memory is not trustworthy. A speculative conflict or missing full audit is not a blocker.

## Full Memory Audit / Recovery

The historical four-snapshot, all-path, exact-plan workflow remains available only as **Full Memory Audit / Recovery**. Use it when:

- the human explicitly asks for a full memory audit or forensic reconciliation;
- corruption is broad and the conflict boundary cannot be established;
- a prior reconciliation transaction is incomplete or restore evidence is uncertain;
- memory-root migration, widespread duplicate identities, or systemic index damage requires repository-wide accounting.

Before it runs, obtain explicit Human authorization for that audit scope. The Python scanner also requires `--full-audit-authorized`; without it the command fails before inventory.

Full Memory Audit / Recovery may use:

- `templates/full-memory-audit-report.md`;
- four complete snapshots;
- Target Canonical Memory Spine;
- Path Accounting Ledger;
- Desired Target Memory Snapshot;
- exact normalized Plan Hash;
- Start, exact Apply, post-check, and Restore gates;
- the existing scan/check/apply/restore scripts.

These controls belong to Recovery. They must never be imported into the normal no-conflict or conflict-driven path.

## Ownership Boundaries

- Requirement / Product Definition owns accepted product meaning.
- ADR owns accepted technical landing and compatibility.
- Bug records own Bug identity and lifecycle; Features own repair execution.
- Feature and Change artifacts own execution and verification evidence.
- Branch Management supplies branch/release/customer context but does not perform reconciliation.
- Feature Archive changes location, not identity.
- Project Skill manifests and bodies remain a validated package; a package conflict is unresolved until integrity and authority are proven.
- `project.md` may point to an active unresolved conflict but must not copy conflict matrices, audit ledgers, hashes, or transaction details.

## Anti-patterns

Never:

- run an all-memory scan after every merge;
- infer that different files automatically conflict;
- treat Target memory or Source memory as universally correct;
- ask the human to review hundreds of unchanged or retained records;
- create a report for a small conflict that can be understood and decided in the conversation;
- block push or release because a report was not created when no conflict exists;
- let code silently redefine accepted product or ADR meaning;
- use a normal conflict resolution to authorize a Git or lifecycle action;
- invoke Full Memory Audit / Recovery without its explicit authorization.
