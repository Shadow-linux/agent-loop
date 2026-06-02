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

Never commit, open a PR, merge, or claim submission readiness without human confirmation.

## Entry Conditions

Enter this stage only after:

- implementation for the selected task/story/feature is complete
- fresh verification evidence exists in `notes.md`
- required Review is complete: Spec Review always, Standards Review when triggered
- drift check is complete or the human explicitly chooses to submit with known drift
- long-term project facts are updated in `project.md`, or no long-term project facts changed
- `tasks.md` reflects current task status
- `plan.md` is closed, superseded, or points to the next active unit

If any item is missing, recommend the missing upstream stage first.

## Submit Options

Ask the human which submit action they want:

```text
prepare only
commit
pull request text
merge note
release note
skip submit for now
```

Default to `prepare only` when the human has not explicitly asked to commit.

## Required Checks

Before submit:

1. Inspect current diff and untracked files.
2. Separate agent-loop documentation changes from product code changes in the summary.
3. Identify unrelated dirty work and do not include or revert it without human instruction.
4. Confirm verification evidence is fresh enough for the submit claim.
5. Confirm required Review is complete and recorded.
6. Confirm drift check result and remaining known drift.
7. Confirm project memory update status.
8. Ask human confirmation for the submit action.

## Two-Stage Submit Confirmation

A human request such as `commit this` or `prepare PR` authorizes entry into Submit / Integrate only. It is not final approval to commit, publish PR text, merge, release, or mark submission ready.

After diff inspection, verification check, review check, drift check, and unrelated-change check, present a Human Review Summary and ask again for the exact submit action.

## Commit Behavior

Only create a commit when the human explicitly confirms.

When committing:

- include only the intended files
- avoid unrelated workspace changes
- use a concise message tied to the feature/task
- record commit hash in `notes.md`

If unrelated changes exist, stop and ask whether to exclude them, split commits, or pause.

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
- Action: prepare only | commit | PR text | merge note | release note | skipped
- Diff Summary:
- Verification:
- Drift Check:
- Review:
- Commit:
- PR:
- Remaining Risk:
```

## Exit

After submit:

- recommend `Close` if the feature is done
- recommend the next task/story if work remains
- recommend `Pause` if submission is prepared but not performed
