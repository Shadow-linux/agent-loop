# Conflict-Driven Memory Reconciliation Proposal

**Version:** v1.5.x
**Status:** accepted
**Human Review:** accepted in conversation on 2026-07-23
**Supersedes after implementation:** the normal-path all-snapshot / all-path behavior designed in `docs/proposal/v1.4.x/post-merge-memory-reconciliation.md`
**Does not rewrite history:** the v1.4.x Proposal and its validation reports remain historical evidence

## 1. Problem

The current Post-Merge Memory Reconciliation design treats every path under the Agent Loop memory root as an item that must be inventoried, semantically classified, assigned an authority, given an action, included in an exact plan, and globally post-checked.

That model protects filesystem transactions, but it does not behave like human memory:

- Git has already merged the files.
- A clean merge does not need a second document merge engine.
- Unchanged memories do not need to be reconsidered.
- Independent Source and Target history does not need a semantic ruling.
- Mechanical completeness does not prove semantic correctness.
- Forcing every path to have a decision encourages unnecessary and incorrect rewrites.
- A local merge can expand into an unrelated full-memory audit.

The normal capability must return to the human-approved principle:

> Start from the Target's current understanding, absorb relevant new experience, correct only facts contradicted by current evidence, and ask the human only when the correct meaning cannot be determined.

## 2. Accepted Human Principle

Memory reconciliation follows this mental model:

```text
Target current understanding
+ Source changes already merged by Git
+ latest verified implementation / environment facts
+ durable accepted Requirement / ADR / Human Decision constraints
= updated Target understanding
```

The unit of reasoning is a **fact, identity, relationship, or current state**, not a filesystem path.

Files are storage containers. Git integrates file bytes. Agent Loop only resolves remaining memory meaning when a real conflict exists.

## 3. Approaches Considered

### A. Keep the all-path ledger and simplify its presentation

This reduces visible noise but leaves the wrong reasoning model intact. The Agent would still classify and verify unrelated memory to satisfy the machine contract.

**Rejected.**

### B. Conflict-driven reconciliation with targeted safety checks

Normal merge handling begins only from an observed Git or semantic conflict. The Agent reads the conflicting facts and their direct owners, resolves them from current evidence, and asks the human only when evidence cannot select one correct result.

The old full-tree transaction machinery becomes an explicitly requested Recovery Audit, not the default merge path.

**Recommended and selected.**

### C. Remove Agent Loop memory reconciliation and rely only on Git

This is simple, but Git cannot detect contradictions spread across different files, such as two current-state claims or an outdated locator after a directory move.

**Rejected.**

## 4. Goals

1. Do nothing after a clean merge when no memory conflict is observed.
2. Inspect only the conflict and the smallest set of directly affected owners or references.
3. Let the Agent resolve conflicts that current facts determine.
4. Present concise alternatives to the human only when the correct state cannot be determined.
5. Preserve human sources, accepted product meaning, accepted technical decisions, and append-only history.
6. Keep targeted preimage checks, bounded writes, rollback, and post-checks for files that are actually rewritten.
7. Separate ordinary conflict resolution from exceptional full-memory recovery.

## 5. Non-Goals

Normal Memory Reconciliation does not:

- scan every memory path looking for hidden problems;
- reconstruct a complete Desired Target Memory Snapshot;
- classify every unchanged file;
- hash every unchanged path;
- treat absence as a normal semantic claim;
- rebuild every index;
- audit the entire `.agent-loop/` tree;
- repair unrelated historical drift;
- repeat the Git merge;
- create a report when no conflict exists;
- block push merely because Source and Target both contain memory changes.

## 6. New Normal Flow

```text
Code and memory files merged by Git
-> Is a memory conflict actually observed?
   -> no: reconciliation-not-needed; stop
   -> yes: identify the conflicting fact and its direct owners
-> inspect current evidence for that conflict
-> can one correct result be determined?
   -> yes: Agent rewrites only the affected memory
   -> no: Agent presents concrete alternatives to the human
-> targeted reference / invariant check
-> complete
```

There is no mandatory four-snapshot inventory or all-path ledger in this flow.

## 7. Reconciliation Entry

Normal reconciliation starts only when at least one of these signals exists:

1. Git reports a conflict in an Agent Loop memory file.
2. The merge result contains two incompatible claims for the same stable identity or current state.
3. A changed memory artifact directly invalidates a changed locator, index, mapping, or current pointer.
4. The Agent or human identifies a concrete contradiction between merged implementation reality and a current Agent-maintained memory claim.
5. A targeted post-merge check for changed memory paths finds a broken direct reference or duplicate stable identity.

These are not entry signals:

- Source and Target both changed different memory files.
- Source added an independent Requirement, Feature, Bug, Decision, Change, or evidence record.
- A memory file exists only on one side and Git included it cleanly.
- An unchanged file has not been recently audited.
- Historical memory might contain unrelated drift.
- A full memory root has not been hashed.

## 8. No-Conflict Result

When no entry signal exists:

```text
Memory Reconciliation: not-needed
Reason: no observed Git or semantic memory conflict
Writes: none
Report: none
Human Gate: none
```

The Agent may record this conclusion in the normal Submit / Integrate summary. It does not create `.agent-loop/memory-merges/`.

## 9. Human-Like Fact Model

### 9.1 Current understanding

The Target's current memory is the starting understanding, not an unquestioned authority.

Current understanding includes:

- current work and next action;
- current capability and lifecycle projections;
- current environment facts;
- current locators, indexes, and mappings.

### 9.2 New experience

Source memory already integrated by Git is new experience:

- independent artifacts and history remain as merged;
- new evidence is absorbed without rejudging unrelated history;
- branch-local Current Work is promoted only when it is still true for the merged Target.

### 9.3 Durable meaning

The following constrain current understanding and are not rewritten in place:

- original human sources;
- accepted Requirement / PRD meaning;
- accepted ADR;
- explicit durable Human Decisions;
- append-only verification, review, close, reopen, and submit history.

### 9.4 Latest facts

For present-tense claims, use the latest sufficiently reliable evidence:

- merged code and fresh tests for implementation reality;
- current bounded environment evidence for environment reality;
- canonical lifecycle owners for current lifecycle;
- actual artifact identity and location for locators;
- accepted product or technical authority for intended meaning.

“Latest” means current and applicable evidence, not the newest Markdown timestamp.

## 10. Conflict Resolution Rules

| Observed conflict | Agent action |
|---|---|
| One side is stale and current evidence proves the other | rewrite the affected current claim |
| Both sides contain compatible independent facts | combine them without Human Review |
| Both sides are stale but current facts prove a third result | rewrite to the proven current result |
| A derived index or locator no longer matches changed canonical artifacts | recalculate only that index or locator |
| Branch-local current work is no longer current after merge | rewrite only the current-work projection |
| Implementation conflicts with accepted Requirement / ADR / Human Decision | preserve the authority and report the implementation conflict |
| Evidence supports multiple legitimate meanings | ask the human which meaning is correct |
| Evidence is missing or not fresh enough | show the alternatives and missing evidence to the human |

The Agent never asks the human to choose `ours` or `theirs` without first translating both into product or project meaning.

## 11. Affected Scope

The normal conflict scope contains only:

1. the file or fact where the conflict was observed;
2. the canonical owner of that fact;
3. directly referenced indexes, locators, mappings, or current pointers;
4. the minimum code, test, configuration, environment, Requirement, ADR, or Human Decision evidence needed to resolve it.

Unchanged and unrelated memory stays untouched.

If investigation reveals unrelated drift, report it separately as a later Recovery / Drift candidate. It does not expand or block the current reconciliation unless it directly prevents the current conflict from being resolved safely.

## 12. Human Review

The Agent resolves every fact-determined item before asking the human.

For a small conflict, Human Review happens directly in the conversation. It does not need a new file.

Human Review contains only unresolved conflicts:

| Conflict | Current evidence | Option A | Option B | Agent recommendation | Consequence |
|---|---|---|---|---|---|

The Agent asks:

> Which description should be the project's current memory?

It does not show:

- unchanged files;
- retained independent history;
- all-path ledger rows;
- absence claims;
- directory hashes;
- transaction internals;
- hundreds of green “keep” items.

Multiple conflicts may be grouped only when they depend on the same human decision.

## 13. Writes And Safety

For each file actually changed, keep:

- safe relative path validation;
- exact preimage hash;
- exact intended postimage;
- atomic write;
- bounded backup;
- rollback limited to this reconciliation;
- targeted format and reference validation;
- targeted semantic verification.

Do not require:

- hashes for every unchanged path;
- a complete memory-tree postimage;
- a zero-change scan of the entire memory root;
- a full-tree transaction journal.

Post-check proves only:

- every planned changed file has the intended bytes;
- directly affected references and invariants are valid;
- immutable and append-only inputs touched by the conflict remain preserved;
- no new conflict was introduced in the affected scope;
- rollback remains possible for this run.

## 14. Report Rules

No report is created for `not-needed`. A small conflict and one bounded Human Decision also stay in the conversation.

Create one concise report only when several coupled conflicts need a shared review surface, work must survive session/context handoff, rollback/recovery evidence is substantial, or the human explicitly requests a report:

```text
<memory-root>/memory-merges/MM-<merged-code-short-sha>-<conflict-topic>/README.md
```

The report contains only:

- merge identity;
- observed conflicts;
- evidence used;
- Agent resolutions;
- Human Decisions when needed;
- changed paths;
- targeted verification;
- rollback and remaining risk.

It is not an all-path inventory or a complete memory snapshot.

## 15. Full Memory Audit / Recovery

The existing all-snapshot, all-path, exact-plan machinery is retained only as an exceptional **Full Memory Audit / Recovery** capability.

It requires explicit human authorization when:

- memory-root corruption is suspected;
- a prior reconciliation transaction is incomplete;
- stable identities or locators are broadly inconsistent;
- branch evidence is missing or unreliable;
- large-scale manual memory edits occurred;
- the human explicitly requests a full audit.

Normal merge, clean memory changes, or an isolated conflict never auto-escalates to Full Memory Audit.

Full Memory Audit has its own scope, report, plan, and restore gate. Its existence does not make it a prerequisite for commit, push, release, or branch cleanup when normal reconciliation is `not-needed` or completed.

## 16. Runtime And Artifact Impact

Implementation must update the coordinated workflow surfaces:

- `references/design.md`
- `references/runtime.md`
- `references/memory-reconciliation.md`
- `references/submit-and-integrate.md`
- `references/stage-guides.md`
- `references/human-review-summary.md`
- `references/project-memory-mode.md`
- `references/recovery-and-backfill.md`
- `references/artifact-rules.md`
- `references/validation-scenarios.md`
- `templates/memory-merge-report.md`
- `templates/root-AGENTS.md` only if its compact gateway currently exposes the old mandatory behavior
- `README.md`
- `Usage.md`
- `CHANGELOG.md`
- focused reconciliation scripts and tests

The v1.4.x Proposal remains unchanged as historical evidence.

## 17. Required RED Scenarios

Implementation begins by proving the old behavior is wrong:

1. Clean merge with independent memory changes returns `not-needed` and creates no report.
2. Source-only independent Feature already present in Result is not imported or reclassified again.
3. Unchanged unrelated memory is absent from the semantic resolution plan.
4. One changed current-state claim reads only its direct owner and evidence.
5. Two compatible facts combine without Human Review.
6. One stale side is rewritten from current verified facts without Human Review.
7. Both sides stale but current facts prove a third value.
8. Ambiguous product meaning produces a concise human choice table.
9. Unrelated drift is reported separately and does not expand the reconciliation scope.
10. Targeted Apply verifies changed preimages, postimages, references, and rollback without hashing every unchanged path.
11. Full Memory Audit is unavailable from the normal path without explicit human authorization.
12. A `not-needed` result does not block a separately authorized push or release.

## 18. Acceptance Criteria

The correction is accepted only when:

1. normal reconciliation has no all-path ledger;
2. normal reconciliation has no mandatory four-snapshot full-tree scan;
3. no observed conflict creates no report and no Human Gate;
4. the Agent starts from the Target's current understanding and reasons over affected facts;
5. latest applicable facts correct current Agent-maintained memory;
6. accepted meaning and human originals remain protected;
7. fact-determined conflicts are resolved by the Agent;
8. only genuinely ambiguous meaning reaches the human;
9. a small conflict is reviewed in the conversation without mandatory file creation;
10. writes and verification are limited to the affected scope;
11. unrelated drift does not silently expand the merge;
12. full audit exists only as an explicitly authorized Recovery capability;
13. focused and full validation include semantic scenarios, not only filesystem mechanics.

## 19. Human Review Decision

The human confirmed this behavior:

> After Git merge, Agent Loop does nothing unless a real memory conflict is observed. When a conflict exists, the Agent inspects only that conflict and the facts needed to resolve it, rewrites the correct current memory when evidence is sufficient, and presents concrete alternatives to the human only when the correct result cannot be determined. Full-tree audit is a separate explicit Recovery capability.

The human explicitly rejected any normal merge flow that asks them to review unchanged files, unrelated artifacts, full-tree inventories, hashes, or mechanically generated “keep” decisions.

The human also confirmed that small conflict review should stay in the conversation; a durable report is optional and reserved for coupled, cross-session, recovery-heavy, or explicitly requested cases.
