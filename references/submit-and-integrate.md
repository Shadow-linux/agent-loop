# Submit And Integrate

Use this file before creating a commit, pull request, merge note, release note, or any claim that work is ready to submit.

## Core Rule

Submit is not the same as close.

```text
Verify proves behavior.
Drift Check aligns memory.
Project Memory Update captures lasting facts.
Submit packages code for integration.
Close ends the feature in agent-loop.
```

Never commit, open a PR, merge, release, publish, or claim submission readiness without human confirmation.

A completed Lightweight Execution Card authorizes no submit or integration action.

At Submit / Integrate, re-read the persisted card's fresh verification, diff, scope, memory result, sensitive-evidence review, and rollback evidence as input only. Run the read-only Change scanner and surface pending or `human-review` memory candidates before a release recommendation. Card execution approval cannot become commit, push, PR, merge, tag, release, or publish approval; every requested action keeps the existing two-stage confirmation and Branch Strategy checks.

Code integration completes and is verified before Target memory reconciliation consumes Change evidence. Source-branch cards, including `Memory Result: synced`, cannot update Target memory or authorize a later Git action by themselves.

## Entry Conditions

Enter this stage only after:

- implementation for the selected task/story/feature is complete
- fresh verification evidence exists in `notes.md`
- required Review is complete: Spec Review always, Standards Review when triggered
- drift check is complete
- long-term project facts are updated in `project.md`, or no long-term project facts changed
- `tasks.md` reflects current task status
- `plan.md` is closed, superseded, or points to the next active unit
- Branch Strategy Check has resolved the current Source Branch, Branch Class, Target Release Context, Target Branch, sealed state, and customer boundary when branch policy applies
- when the Feature resolves Bugs, every related Bug expected to be fixed has fresh Bug-specific verification and is `verifying`; any unresolved Bug Close Decision is explicitly shown rather than rationalized as complete

If any item is missing, recommend the missing upstream stage first.

If the human explicitly chooses to submit with known drift, still perform and record a minimum Drift Check before submit. The record must state the known drift, affected artifacts, risk, and the human decision to submit despite the unresolved drift. Human choice can accept known risk; it cannot skip drift inspection.

## Submit Options

Ask the human which submit action they want:

```text
prepare only
commit
pull request text
merge note
release note
publish/release action
skip submit for now
```

Default to `prepare only` when the human has not explicitly asked to commit.

## Required Checks

Before submit:

1. Inspect current diff and untracked files.
2. Separate agent-loop documentation changes from product code changes in the summary.
3. Identify unrelated dirty work and do not include or revert it without human instruction.
4. Review feature artifacts (`product.md` when present, `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`) against the submitted code.
5. Review linked requirement records for lifecycle, Delivery Phase status, Feature Mapping, and approved deferrals when the feature references requirement sets.
6. Confirm project memory and root/directory guidance impact is completed, explicitly not needed, or human-approved to defer.
7. Confirm verification evidence is fresh enough for the submit claim.
8. Confirm required Review is complete and recorded.
9. Confirm drift check result and remaining known drift.
10. When an adopted Branch Strategy or versioned/customer delivery applies, compare accepted Branch Strategy and Target Release Context with current Git reality and feature Current Branch Context.
11. In that applicable context, fail closed when the target is `released / sealed`, customer isolation would be violated, or the requested action/scope is ambiguous.
12. For a confirmed simple `not-needed` path, record branch-specific checks as `not-applicable`; do not require Target Release Context or Target Branch and do not block ordinary non-versioned submit preparation.
13. For development-branch cleanup, require merge evidence and ask separately; never delete retained standard/customer release aggregation branches as cleanup.
14. When the Feature resolves Bugs, review Bug IDs, current Status, candidate Resolution, Fix Feature, reproduction/substitute evidence, regression/safety evidence, unresolved Bug Close Decisions, Target Release Context, and branch isolation.
15. Ask human confirmation for the exact submit action.

## Two-Stage Submit Confirmation

A human request such as `commit this` or `prepare PR` authorizes entry into Submit / Integrate only. It is not final approval to commit, publish PR text, merge, release, or mark submission ready.

After diff inspection, feature/requirement artifact review, verification check, review check, drift check, project-memory/guidance impact check, and unrelated-change check, present a Human Review Summary and ask again for the exact submit action.

Strategy adoption and plan approval are context only. They never authorize branch creation, switching, merge, deletion, push, tag, release, or publish. List every requested action and every explicitly non-authorized action in the Branch Strategy And Action Review.

Bug confirmation, Resolution Path, successful tests, Feature close, and Bug Close decisions are also context only. Submit/commit/push approval must not be reused as Bug close, and Bug Close approval must not authorize Submit / Integrate or any Git mutation.

## Post-Merge Memory Reconciliation Ordering

After a Human-gated code merge produces one stable verified Merged Code SHA, inspect changed memory and merge evidence for an observed semantic conflict. Do not treat mere difference, Source-only files, unchanged memory, or possible drift as a conflict.

Use this fail-closed order:

```text
Code Merge Gate
-> no observed conflict: reconciliation-not-needed
   OR observed conflict: targeted fact resolution
      -> Human Review only if semantic alternatives remain
      -> targeted verification / restore if needed
-> Memory Commit Gate
-> Push Gate
-> Release Gate
-> Source Branch Cleanup Gate
```

| Observed state | Submit / Integrate action |
|---|---|
| no observed memory conflict | record `reconciliation-not-needed` when useful; offer the next independent gate |
| fact-determined conflict | Agent rewrites only the owner/direct references, verifies, then offers the next independent gate |
| unresolved semantic alternatives | block later mutation and ask one bounded Human decision |
| targeted rewrite verification or restore fails | block later mutation and enter Recovery |
| broad corruption or explicit forensic request | offer Full Memory Audit / Recovery; run it only after explicit authorization |

Unresolved observed memory conflicts block push, release, publish, and Source cleanup because Target memory is not trustworthy. `reconciliation-not-needed` does not block a separately authorized later action. Code commit/merge authorization cannot be reused as a Memory Human Decision, Memory Commit, Push, Release, publish, or Cleanup authorization. A Memory Conflict Report or Full Memory Audit report authorizes no Git mutation.

## Commit Behavior

Only create a commit when the human explicitly confirms.

When committing:

- include only the intended files
- avoid unrelated workspace changes
- use the repository's commit message rules when present, such as `AGENTS.md`
- if root guidance has no commit message style, use the fallback format below and recommend whether to add commit guidance to `AGENTS.md`
- for `agent-loop` skill repository commits, prefer Chinese and use type + version scope with a multi-line body
- record commit hash in `notes.md`

If unrelated changes exist, stop and ask whether to exclude them, split commits, or pause.

## Commit Message Format

For meaningful commits, do not use one-line-only messages.

Preferred format:

```text
<type>: <summary>

- <concrete change>
- <verification evidence>
- <docs or project-memory update>
```

Allowed types:

```text
feat, fix, docs, refactor, test, chore
```

For the `agent-loop` skill repository:

- prefer Chinese in the summary and body
- include the current skill version scope, for example `docs(v1.5.1): 调整 Project Entry Scan 文档结构`
- use 3-7 concrete bullet lines for behavior, gate, artifact, template, reference, validation scenario, or documentation changes
- keep version numbers unchanged unless the human explicitly approves a version bump

Example:

```text
docs(v1.5.1): 调整 Project Entry Scan 文档结构

- 移除旧 onboarding-db 生成入口
- 统一旧项目入口为 Project Entry Scan
- 更新验证场景和引用文件
- 增加 Evidence Chain 与图索引要求
```

## Pull Request Text

If asked for PR text, include:

- summary
- linked feature/task IDs
- implementation notes
- verification evidence
- drift/backfill notes
- risks or follow-up work

Record the final PR text or a reference to it in `notes.md`.

## Notes Record

Append to `notes.md`:

```md
## Submit / Integrate

- Date:
- Scope:
- Action: prepare only | commit | PR text | merge note | release note | publish/release action | skipped
- Diff Summary:
- Verification:
- Drift Check:
- Review:
- Commit:
- PR:
- Remaining Risk:
- Source Branch:
- Branch Class:
- Target Release Context:
- Target Branch:
- Sealed Check:
- Customer Isolation Check:
- Requested Authorization:
- Explicitly Not Authorized:
- Merge Evidence / Cleanup Decision:
- Related Bugs / Current Status:
- Bug Verification Evidence:
- Unresolved Bug Close Decisions:
- Memory Merge Report / Status / Blocker:
- Memory Commit Gate Decision:
```

## Ordered Exit Decision

Submit / Integrate does not route directly to Close. Apply the first matching row so prepare-only and completion cannot recommend different next stages.

| Priority | Condition | Exactly One Next Stage |
|---:|---|---|
| 1 | submission is prepare-only and was not performed | `Pause`, with the pending submit action and resume point |
| 2 | submission action is explicitly `skipped` | record the human decision; `Feature Completion Check` if done, otherwise next task/story |
| 3 | submit succeeded and the feature appears done | `Feature Completion Check` |
| 4 | submit succeeded and work remains | next task/story |
| 5 | submit failed or an external blocker remains | one unblock stage from the blocked routing matrix |
