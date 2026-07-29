# Proposal: Feature Archive Reference Scan Soft Gate

**Version:** 1.5.3
**Status:** implemented and validated; awaiting Human Review
**Human Review:** approved in conversation on 2026-07-28
**Scope:** Feature Monthly Archive / Rehydrate reference discovery only

## 1. Problem

Feature Monthly Archive and Rehydrate build a deterministic plan by scanning project Markdown references. The current scanner rejects every symlinked directory or Markdown file before a plan can be produced, even when the link is only a project-local compatibility alias such as `.claude -> .agents`.

This makes the checker the semantic Gate owner. A repository layout fact that may be harmless prevents the Agent from inspecting the target, judging reference coverage, presenting the real risk, or reaching the existing exact-plan Human Gate.

## 2. Accepted Principle

> Reference discovery reports objective symlink findings. The Agent decides whether those findings leave reference coverage safe enough to offer Archive / Rehydrate. Mechanical mutation boundaries remain hard checks.

This follows the same responsibility split as the lightweight Feature Gate: scripts provide deterministic facts; the Agent owns semantic completeness and boundary judgment; the human retains the action authorization.

## 3. Approaches Considered

### A. Structured findings plus Agent judgment

Do not follow symlinked directories or Markdown files. Record deterministic project-relative findings in the scan plan, continue scanning the ordinary tree, and let the Agent inspect the canonical project structure and decide whether coverage is sufficient.

Keep source, destination, reference-edit, journal, restore, stale-plan, collision, and project-boundary checks hard.

**Selected.**

### B. Whitelist `.claude` and other known compatibility names

This fixes one layout but creates an expanding name list and fails on equivalent aliases.

**Rejected.**

### C. Remove symlink handling

Following links can duplicate traversal, create cycles, escape the project, or mutate an unintended file.

**Rejected.**

## 4. Scope And Ownership

The soft behavior applies only while discovering Markdown reference impact.

The scanner owns:

- deterministic enumeration of non-symlink project files;
- never following directory or file symlinks;
- recording every skipped symlink as a project-relative structured finding;
- classifying only mechanically observable facts such as `internal`, `external`, `broken`, `cycle`, or `unresolved` when determinable without traversing linked contents;
- including findings in the deterministic plan hash;
- preserving read-only behavior.

The Agent owns:

- inspecting the real canonical directory when it exists inside the project;
- checking whether it is already covered by the ordinary scan;
- deciding whether the skipped alias can hide a relevant old Feature path or cross-boundary reference;
- classifying the result response-locally as safe to continue, a reference-coverage risk, or unresolved;
- offering the existing Batch Human Gate only when it can explain why coverage is sufficient;
- asking one blocking question when evidence cannot establish safety.

The human owns the existing exact plan SHA-256 Archive / Rehydrate authorization. Human approval of a plan does not authorize any other Feature lifecycle, Git, release, or external action.

## 5. Executor Physical Boundaries (Not Gate Judgments)

The Checker no longer uses the following facts to decide whether Archive / Rehydrate may proceed. The executor still enforces them only where needed to guarantee that one exact reviewed plan cannot write outside its declared transaction:

- Feature archive/rehydrate source and destination confinement;
- Feature source/destination and archive locator confinement at mutation time;
- regular-file and project-boundary confinement for every precomputed Markdown file Apply will rewrite;
- path collision, Unicode/case collision, stale plan, or plan SHA-256 mismatch;
- transaction journal identity and confinement;
- backup integrity, post-check, restore, and stranded transaction handling;
- immutable human requirement sources;
- the prohibition on `--force`, deletion, packing, or scheduled archive;
- the independent Archive / Rehydrate Batch Human Gate.

These are executor correctness conditions, not Archive eligibility, reference completeness, or Human Gate decisions. Apply and restore may act only on regular, project-confined paths named by the exact reviewed plan. A soft scan finding can never widen a write path.

## 6. Scan Plan Contract

The plan reuses the existing `skipped_references` collection instead of adding a second finding schema. A symlink row uses `classification: reference-scan-symlink` and contains only the minimum stable evidence needed for review:

```text
path: project-relative symlink path
matched_value: <directory|markdown-file|entry>:<internal|external|broken|cycle|unresolved>[:<project-relative-target>]
reason: not-followed
```

`entry` is used when a broken or cyclic link cannot truthfully be identified as a directory or Markdown file. The scanner must not expose an external absolute target in normal output. These rows use the existing deterministic sort and participate in `plan_sha256`. A change to the link, target resolution, or finding set therefore makes an earlier reviewed plan stale.

No new lifecycle status, canonical stage, Auto Mode, executable schema, or persistent Agent-decision artifact is introduced.

## 7. Agent Review Contract

Before presenting the existing Batch Human Gate, the Agent reports:

- each reference-scan finding;
- whether an internal canonical target was scanned through a normal path;
- the evidence used to conclude that relevant references are covered or not covered;
- any remaining risk;
- one recommendation: continue to Batch Human Gate or stop for one blocking question.

The scanner does not print `approved`, `safe`, or another authorization result. The Agent must not treat an empty or advisory-only finding list as proof that semantic reference coverage is complete.

## 8. Validation

Focused RED/GREEN coverage must include:

1. `.claude -> .agents` produces a finding instead of `path-escape` and does not follow the alias;
2. Markdown under the real `.agents` directory is still scanned through its canonical path;
3. external, broken, cyclic, and unresolved links produce deterministic findings without traversal;
4. symlinked Markdown files are not read or edited;
5. changing a link or its resolution changes the plan SHA-256 and makes an old plan stale;
6. a reviewed plan never causes Apply or restore to write through a symlink or outside the project, while the Agent—not the scan Checker—owns the decision to proceed;
7. scan and check remain read-only;
8. archive and rehydrate retain exact-plan, transaction, post-check, and restore guarantees;
9. macOS behavior is verified locally and Windows behavior remains covered by standard-library tests and CI.

Because this changes an Archive Human Gate input and cross-file workflow invariant, implementation requires focused RED/GREEN, all Shell/Python tests, mechanical checks, six-domain full validation, and a new Chinese report.

## 9. Coordinated Surfaces

Implementation must review and align at least:

- `SKILL.md`
- `references/design.md`
- `references/runtime.md`
- `references/artifact-rules.md`
- `references/stage-guides.md`
- `references/human-review-summary.md`
- `references/workflow-checklists.md`
- `references/validation-scenarios.md`
- `templates/root-AGENTS.md`
- `scripts/feature_archive_support.py`
- archive scan/check/apply/restore tests
- `README.md`
- `Usage.md`
- `CHANGELOG.md`
- version-bearing files for approved version `1.5.3`

## 10. Stop Conditions

Stop and return to Human Review if implementation would require:

- following symlinks during the scan;
- allowing Apply or restore to write through a symlink;
- removing deterministic plan hashing or the Batch Human Gate;
- introducing a manual bypass or `--force` option;
- rewriting human source requirements;
- adding a new canonical stage, lifecycle, or authorization status;
- changing unrelated Checker, Feature Gate, or Project Skill semantics.

## 11. Implementation Result

Implemented on 2026-07-28 in the v1.5.3 development worktree.

- Scanner records internal, external, broken, cyclic, and unresolved symlink facts without traversal.
- Advisory findings remain inside the deterministic plan SHA-256 and no longer authorize or reject check/apply.
- Agent review, the exact-plan Batch Human Gate, transaction journal, project/plan confinement, post-check, and rollback remain distinct.
- Focused GREEN: 61 / 61 Archive support/scan/apply/restore tests plus the cross-surface contract.
- Full GREEN: 47 / 47 Shell tests and 327 / 327 Python tests.
- Platform status: `macOS-verified / Windows-test-defined`; no Windows runner was available in this local session.
- No commit, push, tag, release, publish, or installed-Skill synchronization has been performed.
