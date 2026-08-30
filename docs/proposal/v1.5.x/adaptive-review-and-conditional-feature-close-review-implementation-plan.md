# Inline Task Review, Final Review Subagent, And Agent-Owned Delegation Implementation Plan

**Implementation status:** Phase 1 implemented and independently re-reviewed; Phase 2 version synchronization, focused validation, six-domain semantic review, one preserved failed full-run RED, its repairs, and the freshly confirmed repaired-input full GREEN are complete; final scope review is complete and the work is waiting at the independent Human Git/release gates.

> **For implementation Agents:** use `subagent-driven-development` when independent tasks can be delegated safely, or `executing-plans` when proceeding serially. Subagent dispatch itself does not grant implementation authority: this plan must first pass its implementation Human Review, and every delegated worker inherits only the current task scope and write boundary.

**Goal:** implement Agent Loop `1.5.9` so each Task receives a lightweight internal completion review, the completed Feature receives one independent read-only Final Review, close does not repeat review, and the owning Agent may delegate within authority that already exists.

**Architecture:** remove standalone `Review`, `Subagent Execution If Approved`, and `Feature Close Review` from the active workflow without weakening their underlying evidence and Human Gates. Move task-scoped review into Task Done Gate, introduce one Feature-wide Final Review Subagent after current verification, make the controller responsible for findings and repairs, and migrate completion/archive contracts to Final Review evidence while retaining read compatibility for legacy records.

**Tech stack:** Markdown runtime contracts and templates, Python 3 standard library, Bash contract tests, Python `unittest`, Ruby/YAML and JSON mechanical validation, Git read-only inspection.

---

## 1. Authority And Planning Boundary

- Repository worktree: `/Users/shaodowyd/.config/superpowers/worktrees/agent-loop/alpha-v1.5.9`
- Branch: `alpha/v1.5.9`
- Planning baseline HEAD: `eee51f0dd72568ec5711567d6c7bc66d9b61797e`
- Base release: `v1.5.8`
- Target skill version: `1.5.9`
- Accepted Proposal: `docs/proposal/v1.5.x/adaptive-review-and-conditional-feature-close-review.md`
- Parallel `alpha/v2.0.0` checkout and its dirty work are out of scope.
- This plan authorized no implementation by itself. The Human separately authorized Phase 1 implementation on 2026-08-29; that grant does not authorize Phase 2.
- Full-suite execution, version synchronization, Git operations, release, publish, and installed-Skill synchronization remain separate gates described below.

Planning-time dirty boundary:

```text
M  tests/validate-lightweight-change-lane.sh
M  tests/validate-repair-first-verification.sh
?? docs/proposal/v1.5.x/adaptive-review-and-conditional-feature-close-review.md
?? docs/proposal/v1.5.x/adaptive-review-and-conditional-feature-close-review-implementation-plan.md
```

The two tracked test edits are the Human-approved v1.5.8 release-date baseline repair recorded by the Proposal. Preserve them. Do not delete, restore, stage, overwrite, or silently absorb any later unrelated dirty work.

## 2. Non-Negotiable Invariants

Implementation must preserve all of the following:

1. Task Completion Review is mandatory but is not a new canonical stage, status, Human Gate, helper invocation, or artifact family.
2. Final Review is mandatory once per current Feature completion boundary and is performed by a read-only Subagent when capability exists.
3. A Final Review Subagent may report findings only. It cannot write, repair, mark status, create permission, accept a Gate, or perform Git/external actions.
4. The owning Agent validates findings, repairs only inside existing authority, reruns affected evidence, and owns routing.
5. Subagent dispatch needs no separate Human approval, but delegated authority is the intersection of current stage scope, current write grant, and disclosed assignment boundary.
6. A Subagent cannot create, infer, transfer, cache, or widen authorization.
7. If Subagent capability is unavailable, the controller performs and records an isolated whole-Feature review as `Final Reviewer: controller-fallback`; review may not be omitted.
8. Ordinary bounded Review Repair does not automatically rerun Final Review. Material boundary, risk, coverage, authority, rollback, or safety change expires review and requires a fresh reviewer.
9. Feature Completion Check consumes current review/finding evidence; it is not another review.
10. Feature Close Review is removed from active close and archive prerequisites. Human Close Gate remains mandatory.
11. Normal Submit may reuse current Final Review evidence only while reviewed inputs remain unchanged. Full-Worktree Git Fast Path remains packaging-only and review-free.
12. Product, Requirement, ADR, Delivery Contract, Feature Gate 1/2, Human-gated Task, Pause, Close, Git, branch/worktree, release, production, destructive, credential, paid, and external-action Human Gates remain intact.
13. Legacy `Review` and `Feature Close Review` records remain readable; no bulk artifact migration is required.
14. Do not add a canonical stage, lifecycle status, message intent, Auto Mode, checker outcome, default artifact directory, mandatory review file, or general force/skip parameter.

## 3. Expected File Impact

The following list is the implementation boundary discovered from current source references. Task 0 must refresh it with `rg`; a newly discovered active owner is added only when it enforces the same accepted semantics.

### Core runtime and routing

- `SKILL.md` — concise canonical flow, stage/help routing, and version in Phase 2.
- `references/runtime.md` — canonical Stage Order, controller routing, Task Done/Final Review entry, Subagent authority, and preserved Human Gates.
- `references/design.md` — design rationale, ownership boundaries, invariants, and fallback.
- `references/concepts.md` — define Task Completion Review, Final Review, delegated authority, and legacy terms.
- `references/stage-guides.md` — remove active standalone Review/Subagent-approval stages; define Task Done, Final Review, repair, drift, memory, completion, submit, and close sequence.
- `references/workflow-checklists.md` — executable checklists for the same flow.
- `references/skill-routing.md` — helper selection for automatic review/delegation without making helper loading a Gate.
- `references/external-skill-adapters.md` — Subagent adapter authority inheritance, read-only reviewer contract, optional brief, and owning-Agent responsibility.

### Completion, submit, Human evidence, and compatibility

- `references/feature-completion-check.md` — require current Final Review and resolved/routed findings instead of Feature Close Review.
- `references/submit-and-integrate.md` — reuse/expire Final Review evidence based on reviewed inputs.
- `references/human-review-summary.md` — retain Feature Gate 1/2 and Human Close summaries while removing dispatch approval and duplicate close review.
- `references/repair-first-verification.md` — update only if its active Review Repair wording conflicts with the accepted owner/freshness rules.
- `references/artifact-rules.md` — update only active artifact/evidence ownership; retain legacy readability.
- `references/document-templates.md` — mirror the new notes, completion, archive, and delegation template fields.
- `references/project-guidance.md` — project-facing Stage Map and root guidance refresh behavior.
- `references/onboarding-knowledge-base.md` and `references/product-brief.md` — update only verified active flow references; do not expand scope into onboarding or product redesign.

### Templates, scripts, examples, and human docs

- `templates/notes.md` — Task Completion Review and Final Review/finding/freshness evidence; remove active Feature Close Review requirement.
- `templates/subagent-brief.md` — replace dispatch approval with inherited authority and explicit reviewer/write boundaries; keep the template optional.
- `templates/tasks.md` and `templates/task-detail.md` — align Task Done evidence only where current fields project standalone Review.
- `templates/root-AGENTS.md` — all 13 managed blocks; Stage Map and completion/gate wording, then one common Phase 2 revision.
- `scripts/feature_archive_support.py` — accept new `Final Review: complete` archive readiness while reading legacy `Feature Close Review: complete` safely.
- `examples/login-feature/notes.md` and any other active example found by Task 0 — demonstrate new evidence without rewriting unrelated historical examples.
- `README.md` and `Usage.md` — explain the simpler review flow and Agent-owned delegation; Phase 2 version labels.
- `CHANGELOG.md` — Phase 2 `1.5.9` entry.
- `plugin.json` — Phase 2 version metadata only.

### Tests and validation evidence

- Add `tests/test_final_review_agent_owned_delegation.py` — section-aware semantic, authority, freshness, compatibility, and mutation contract.
- Add `tests/validate-final-review-agent-owned-delegation.sh` — focused cross-surface executable contract.
- Update `tests/test_feature_review.py` — preserve Feature Gate 1/2 and repair tests while removing assertions that Subagent dispatch is an independent stop.
- Update `tests/validate-feature-construction-two-gate-review.sh` — retain two Feature construction Gates; update completion/review ownership.
- Update `tests/validate-mandatory-helper-routing.sh` — Final Review helper routing and Agent-owned dispatch.
- Update `tests/validate-repair-first-verification.sh` — move Review Repair assertions to the new owning section and retain the accepted date repair.
- Update `tests/test_root_agents_lossless_slimming.py` — expected Stage Map/managed-block semantics and Phase 2 revision.
- Update `tests/feature_archive_test_support.py` plus archive tests using it — new readiness field and legacy compatibility.
- Update root/version assertion tests found by `rg -n '1\.5\.8|block-version:1\.5\.8' tests` during Phase 2.
- Update `references/validation-scenarios.md` — positive, negative, fallback, freshness, authority, close, Submit, Auto Mode, and compatibility scenarios.
- Add `docs/reports/agent-loop-1.5.9-full-validation-2026-08-30.md` after the Human-confirmed Phase 2 run records real evidence, including a failed run without hiding its RED result.
- `docs/maintenance/full-validation-method.md` — change only if its maintainer audit vocabulary becomes factually wrong; it is not a user-runtime owner.

## 4. Strict Task Order

## Phase 1 — Runtime Contract, Compatibility, And Focused GREEN

Phase 1 implements behavior and focused evidence but does not bump versions or run the final broad suite. It ends at an independent Human Review checkpoint.

### Task 0: Re-establish the worktree boundary and obtain test authority

**Files:** read-only inspection; no source edits.

- [x] Confirm branch, HEAD, worktree root, remotes, and complete dirty state.
- [x] Confirm the Proposal remains `accepted` and its digest/content did not change unexpectedly.
- [x] Verify the two v1.5.8 date fixes are exactly the approved one-line assertion changes.
- [x] Search active owners before editing:

```bash
git status --short --branch
git rev-parse HEAD
git diff -- tests/validate-lightweight-change-lane.sh tests/validate-repair-first-verification.sh
rg -n '(^|[^A-Za-z])(Review|Feature Close Review|Subagent Execution If Approved|subagent approval|unapproved Subagent|unapproved subagent)' SKILL.md references templates scripts examples tests README.md Usage.md
rg -n '1\.5\.8|block-version:1\.5\.8' SKILL.md plugin.json README.md Usage.md CHANGELOG.md templates tests references
```

- [x] Record the immutable starting boundary in the implementation log.
- [x] Record that no exact pre-change broad-run confirmation was received; do not run it and keep the later comparison focused. The command signature below remains the unexecuted broad baseline proposal.

```bash
set -o pipefail
overall=0
for test_file in tests/*.sh; do bash "$test_file" || overall=1; done
python3 -m unittest discover -s tests -p 'test_*.py' || overall=1
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")' || overall=1
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))' || overall=1
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n || overall=1
python3 - <<'PY' || overall=1
from pathlib import Path
bad = []
for path in Path('.').rglob('*.md'):
    if '.git' in path.parts:
        continue
    fences = sum(
        line.startswith('```')
        for line in path.read_text(encoding='utf-8').splitlines()
    )
    if fences % 2:
        bad.append(path.as_posix())
if bad:
    raise SystemExit('unbalanced Markdown fences: ' + ', '.join(bad))
PY
git diff --check
```

Expected claim: all pre-existing Shell/Python/mechanical contracts pass on macOS, establishing that subsequent RED failures are introduced only by the new v1.5.9 assertions. If the Human declines this broad baseline, use the focused current evidence recorded in Proposal section 15 and explicitly narrow the later comparison; do not claim a live all-test pre-change baseline.

**Stop conditions:** branch/HEAD mismatch, new dirty overlap, a failing unrelated baseline, changed Proposal semantics, or inability to distinguish existing work. Do not clean/reset/stash/checkout.

### Task 1: Create a real focused RED contract

**Files:**

- Create `tests/test_final_review_agent_owned_delegation.py`.
- Create `tests/validate-final-review-agent-owned-delegation.sh`.
- Modify only conflicting expectations in `tests/test_feature_review.py`, `tests/validate-feature-construction-two-gate-review.sh`, and `tests/validate-mandatory-helper-routing.sh` after the new contract demonstrates the old behavior.

- [x] Add section-aware assertions for canonical stage ownership rather than global word absence.
- [x] Assert the old v1.5.8 sources fail because they still contain standalone Review, approval-gated Subagent execution, and mandatory Feature Close Review.
- [x] Add positive/negative cases for Task Completion Review, Final Review entry, read-only findings, controller fallback, inherited authority, repair freshness, Submit reuse, Human Close, Git Fast Path, and legacy records.
- [x] Add mutation fixtures that delete or invert each critical invariant and prove the test rejects the mutation.
- [x] Avoid tests that merely count phrases or forbid historical/compatibility text.
- [x] Run only the new focused RED:

```bash
python3 -m unittest tests.test_final_review_agent_owned_delegation -v
bash tests/validate-final-review-agent-owned-delegation.sh
```

Expected RED: failures identify active old workflow owners, not release dates, missing tools, malformed fixtures, or unrelated dirty files. Save concise failure excerpts in the implementation log/plan progress section.

**Stop conditions:** the test unexpectedly passes, fails for unrelated reasons, requires a new checker/artifact/stage to express the contract, or cannot distinguish legacy-readable text from active authority.

### Task 2: Change the canonical runtime and design owners

**Files:** `SKILL.md`, `references/runtime.md`, `references/design.md`, `references/concepts.md`.

- [x] Replace the active Feature path with:

```text
Execute Task
-> Verify
-> Task Done Gate (includes Task Completion Review)
-> repeat remaining Tasks
-> Feature-wide Required Verification
-> Final Review Subagent
-> Review Repair / affected verification when needed
-> Drift Check
-> Project Memory Update
-> Feature Completion Check
-> Submit / Integrate or Pause / Close
```

- [x] Remove standalone `Review` and `Subagent Execution If Approved` from canonical stage order and routing.
- [x] Define Final Review entry blockers: incomplete/unapproved Task disposition, stale Feature-wide verification, unresolved authority, ambiguous dirty work, missing rollback/verification evidence, or changed reviewed inputs.
- [x] Define the read-only finding contract and owning-Agent validation/repair responsibility.
- [x] Define authority inheritance for read-only and write-capable Subagents without adding dispatch authorization.
- [x] Preserve every underlying Human Gate listed in section 2.
- [x] Define ordinary repair freshness and material-change re-review precisely.
- [x] Define `controller-fallback` without claiming independent process isolation that the runtime cannot provide.
- [x] Keep `SKILL.md` concise and defer detail to references.

Run:

```bash
python3 -m unittest tests.test_final_review_agent_owned_delegation -v
bash tests/validate-final-review-agent-owned-delegation.sh
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
git diff --check
```

Expected: core-owner assertions turn GREEN; template/archive/docs assertions may remain RED and must point to later Tasks.

### Task 3: Align stage execution, helper routing, and Subagent delegation

**Files:** `references/stage-guides.md`, `references/workflow-checklists.md`, `references/skill-routing.md`, `references/external-skill-adapters.md`, and conditionally `references/repair-first-verification.md`.

- [x] Embed the quick review inside Task Done Gate: accepted authority/scope, diff, current verification, rollback, drift, unresolved findings, and task status.
- [x] Add one Final Review procedure after all Tasks and Feature-wide verification.
- [x] Make the reviewer read-only and require structured findings: severity, claim, evidence, affected boundary, recommendation, and confidence/unknowns.
- [x] Require the owning Agent to reproduce/validate findings and record disposition.
- [x] Remove “Human approval to dispatch” and replace it with “existing authority required for delegated actions.”
- [x] Keep helper resolution a capability-loading mechanism, not an authorization mechanism.
- [x] Make the subagent brief optional; when used, it records inherited authority and prohibited actions.
- [x] Route ordinary repair through Repair-First Verification and route semantic/boundary/safety/authorization drift back to the appropriate owner.
- [x] Ensure Auto Modes may dispatch within authority but still stop at all underlying Human Gates.

Focused checks:

```bash
bash tests/validate-mandatory-helper-routing.sh
bash tests/validate-feature-construction-two-gate-review.sh
bash tests/validate-repair-first-verification.sh
python3 -m unittest tests.test_feature_review tests.test_final_review_agent_owned_delegation -v
```

Expected: helper and repair contracts pass without resurrecting a dispatch Gate or removing Feature Gate 1/2.

### Task 4: Migrate notes, completion, archive, and legacy compatibility

**Files:** `templates/notes.md`, `templates/subagent-brief.md`, `templates/tasks.md`, `templates/task-detail.md`, `references/document-templates.md`, `references/feature-completion-check.md`, `references/artifact-rules.md`, `scripts/feature_archive_support.py`, `tests/feature_archive_test_support.py`, affected archive tests, and active examples.

- [x] Replace active notes fields with:
  - Task Completion Reviews;
  - Final Reviewer and reviewed-input identity/digest;
  - Final Review Findings and owning-Agent dispositions;
  - post-repair freshness assessment or fresh-review requirement;
  - Feature Completion Check consuming current review evidence;
  - Archive Readiness `Final Review: complete`.
- [x] Remove active Feature Close Review fields and duplicate close-review helper records.
- [x] Update the optional Subagent brief from `Dispatch Authorization` to inherited stage/write/task authority, allowed writes, forbidden actions, expiry, and read-only reviewer flag.
- [x] Update `feature_archive_support.py` to prefer `Final Review` for new records while accepting legacy `Feature Close Review` records as read-only compatibility evidence.
- [x] Reject missing current review evidence for new-format Features; do not let the legacy alias allow a newly created Feature to bypass Final Review.
- [x] Preserve closed historical Features without bulk migration.
- [x] Update fixtures/examples intentionally; do not rewrite historical proposals or reports.

Focused checks:

```bash
python3 -m unittest tests.test_final_review_agent_owned_delegation -v
python3 -m unittest discover -s tests -p 'test_*archive*.py'
bash tests/validate-final-review-agent-owned-delegation.sh
```

Expected: new-format archive readiness uses Final Review; legacy fixtures remain readable; missing/forged/expired current evidence blocks completion/archive.

### Task 5: Align completion, Submit, Human summaries, root guidance, scenarios, and human docs

**Files:** `references/submit-and-integrate.md`, `references/human-review-summary.md`, `references/project-guidance.md`, `references/validation-scenarios.md`, conditionally `references/onboarding-knowledge-base.md` and `references/product-brief.md`, `templates/root-AGENTS.md` behavior text only, `README.md`, and `Usage.md` behavior text only.

- [x] Feature Completion Check requires a current Final Review record and disposition of every supported finding, then checks drift/memory/status without performing another review.
- [x] Human Close Gate remains explicit and receives current completion evidence.
- [x] Normal Submit reuses Final Review only when authority, diff, verification, risk, coverage, and residuals are unchanged; otherwise expire/reroute.
- [x] Full-Worktree Git Fast Path remains packaging-only, review-free, and unable to claim Task/Feature completion.
- [x] Root Stage Map projects the simplified flow without becoming the detailed runtime owner.
- [x] Remove “unapproved Subagent dispatch” as a stop; retain stops for unapproved delegated actions.
- [x] Add validation scenarios for every Proposal GREEN and pressure case, including overlapping Subagent writes.
- [x] Explain the Human-facing outcome concisely in README/Usage without changing version labels yet.
- [x] Do not change the 13 managed-block revision values until Phase 2.

Focused checks:

```bash
bash tests/validate-feature-construction-two-gate-review.sh
bash tests/validate-mandatory-helper-routing.sh
python3 -m unittest tests.test_root_agents_lossless_slimming -v
python3 -m unittest tests.test_feature_review tests.test_final_review_agent_owned_delegation -v
```

Expected: active runtime, root projection, Human summaries, and scenarios agree; Human Close and all underlying action Gates remain present.

### Task 6: Complete focused GREEN and Phase 1 semantic audit

**Files:** all Phase 1 files and the feature-scoped validation reports; no version synchronization or full-validation report.

- [x] Run the focused contract and every affected existing suite:

```bash
python3 -m unittest tests.test_final_review_agent_owned_delegation -v
python3 -m unittest tests.test_feature_review tests.test_root_agents_lossless_slimming -v
python3 -m unittest discover -s tests -p 'test_*archive*.py'
bash tests/validate-final-review-agent-owned-delegation.sh
bash tests/validate-feature-construction-two-gate-review.sh
bash tests/validate-mandatory-helper-routing.sh
bash tests/validate-repair-first-verification.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
```

- [x] Execute all mutation cases and confirm each fails for its intended missing/inverted invariant.
- [x] Pressure-test:
  - read-only reviewer attempts a patch;
  - implementation Subagent attempts an unapproved path/branch/external action;
  - stale verification or changed Task after review;
  - tiny repair with current proof versus material boundary/risk/coverage change;
  - no Subagent runtime;
  - stale historical dispatch approval;
  - overlapping Subagent writes;
  - normal Submit input drift;
  - Git Fast Path packaging without completion claim;
  - legacy close evidence versus new Feature evidence.
- [x] Run minimum mechanical checks:

```bash
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))'
bash -n tests/validate-final-review-agent-owned-delegation.sh
python3 -m py_compile scripts/feature_archive_support.py tests/test_final_review_agent_owned_delegation.py tests/feature_archive_test_support.py
python3 - <<'PY'
from pathlib import Path
bad = []
for path in Path('.').rglob('*.md'):
    if '.git' in path.parts:
        continue
    fences = sum(
        line.startswith('```')
        for line in path.read_text(encoding='utf-8').splitlines()
    )
    if fences % 2:
        bad.append(path.as_posix())
if bad:
    raise SystemExit('unbalanced Markdown fences: ' + ', '.join(bad))
PY
git diff --check
```

- [x] Inspect full diff, file modes, untracked files, generated caches, placeholders, and scope:

```bash
git status --short --branch
git diff --stat
git diff --summary
rg -n 'TODO|TBD|PLACEHOLDER|Feature Close Review|Subagent Execution If Approved' SKILL.md references templates scripts examples tests README.md Usage.md
find . -type d -name '__pycache__' -prune -print
```

Expected: active occurrences of retired terms are absent or explicitly marked legacy/compatibility; focused tests and mechanical checks pass; no version mismatch is introduced.

### Phase 1 Implementation Progress — 2026-08-30

- Worktree, branch, baseline HEAD, Proposal semantics, and the complete starting dirty boundary were revalidated before implementation. The two approved `2026-08-27` assertion repairs remain preserved as starting input.
- The optional pre-change broad baseline was not run because no exact broad-run confirmation was requested or received. The comparison is therefore limited to the Proposal's focused baseline and the recorded focused RED/GREEN evidence; no all-test baseline or release-readiness claim is made.
- Focused RED was real: the first new contract produced `14/14` failures against the v1.5.8 workflow owners, covering standalone Review, approval-gated Subagent dispatch, mandatory Feature Close Review, template/root/archive, and documentation gaps.
- Tasks 2-5 implemented the accepted runtime, delegation, completion, Submit, archive, template, root-guidance, scenario, example, and Human-document changes without changing the active version or any managed-block revision.
- Initial independent read-only Subagent review found one Critical archive bypass and three Important contract/test gaps. The owning Agent repaired them by requiring concrete Final Review record evidence, requiring pre-1.5.9 `Created` and `Closed At` dates plus the real retired readiness shape for legacy compatibility, removing active dispatch-approval remnants, adding rollback entry evidence, and adding archive/Human Close/Git/fallback/overlap mutation coverage.
- Earlier focused GREEN after the initial implementation repair was `52` selected cross-owner Python tests, `80` archive-discovery tests, the dedicated focused wrapper (`18` contract + `38` monthly-archive scan tests), and all `14` then-selected Shell contracts.
- At that earlier checkpoint, the same read-only reviewer returned `Ready for Phase 1 Human Review: Yes`. A later three-agent Feature review superseded that readiness claim with `77/100` and identified four High, three Medium, and two Low findings; its immutable timepoint report is `docs/reports/inline-task-final-review-agent-delegation-feature-validation-2026-08-30.md`.
- Human-authorized Review Repair added a second real focused RED with seven contract failures, then repaired Task review currentness, Task Auto-Run terminal routing, helper-versus-dispatch fallback, same-file concurrency, finding dispositions, active routing, Submit freshness, exact archive cutoff coverage, and Plan status truth.
- The proposal-blind follow-up then exposed two additional RED cases: non-verification Final Review prerequisites were still over-routed to Verify, and a failed runtime dispatch could still be read as permission for controller fallback. Both focused tests failed for those exact missing rules before implementation, then passed after exact-owner routing and Diagnose Failure retry/fallback exclusion were coordinated across runtime, stage, adapter, checklist, root guidance, and scenarios.
- Final Task 6 focused GREEN is: `61/61` cross-owner Python tests, `40/40` focused archive tests, the dedicated wrapper `67/67`, seven affected Shell contract scripts, YAML/JSON/Shell syntax/Python compile/Markdown fence balance, and `git diff --check`. No file-mode change or mixed version value was introduced; the 13 managed blocks remain on the common `1.5.8-20260826.1` revision.
- Final independent proposal-blind pressure re-review reports Critical 0 / High 0 / Medium 0 / Low 1 and `24.5/25` for Pressure Resistance. The Low observation is limited to test-entry isolation: the whole feature test module includes one Implementation Plan status test, so proposal-blind review must select the six runtime-only methods rather than call the whole wrapper. It does not alter runtime semantics or block Phase 1 Human Review.
- The immutable repaired timepoint report is `docs/reports/inline-task-final-review-agent-delegation-feature-validation-2026-08-30-r2.md`. Phase 1 is ready for its independent Human Review checkpoint; Phase 2 remains not authorized.

### Phase 1 Human Review Checkpoint

Stop after Task 6. Present:

- exact modified/new files and dirty boundary;
- preserved RED output and focused GREEN counts;
- mutation/pressure results;
- canonical flow before/after;
- Human Gate and delegated-authority audit;
- legacy archive compatibility evidence;
- unresolved findings, scope drift, and stop-condition audit;
- Phase 2 version-sync diff preview and exact full-run signature.

Do not start Phase 2 until the Human accepts Phase 1. Phase 1 acceptance does not authorize the broad run, commit, push, tag, release, or installed-Skill sync.

## Phase 2 — Version Synchronization, Full Validation, And Release-Readiness Evidence

### Task 7: Synchronize every active version-bearing surface to 1.5.9

**Files:** `SKILL.md`, `plugin.json`, `README.md`, `Usage.md`, `CHANGELOG.md`, `templates/root-AGENTS.md`, and version assertions in tests.

- [x] Set `SKILL.md` to `Version: 1.5.9`.
- [x] Set `plugin.json` to `"version": "1.5.9"`.
- [x] Set README current version and stable/install wording to the intended pre-release truth. Do not claim a stable tag exists before release.
- [x] Set Usage human-facing version to `1.5.9` and avoid claiming release actions that have not happened.
- [x] Add `CHANGELOG.md` heading `## 1.5.9 — 2026-08-29` with concrete behavior, compatibility, and verification notes; keep prior history unchanged.
- [x] Set all 13 managed blocks in `templates/root-AGENTS.md` to exactly `block-version:1.5.9-20260829.1`.
- [x] Update all active test assertions that intentionally track current version/revision.
- [x] Keep historical Proposal/report/example values when they are factual history.
- [x] Verify exactly 13 identical block revisions and search old values:

```bash
python3 - <<'PY'
from pathlib import Path
import re
text = Path('templates/root-AGENTS.md').read_text(encoding='utf-8')
values = re.findall(r'block-version:([^ ]+) -->', text)
assert len(values) == 13, values
assert set(values) == {'1.5.9-20260829.1'}, values
PY
rg -n 'Version: 1\.5\.8|"version": "1\.5\.8"|Current version:\*\* 1\.5\.8|版本：\*\* 1\.5\.8|block-version:1\.5\.8-20260826\.1' SKILL.md plugin.json README.md Usage.md templates references tests
```

Expected: no stale active version values; historical CHANGELOG/Proposal/report occurrences are explained rather than mass-rewritten.

### Task 8: Re-run focused contracts after version synchronization

- [x] Run all Task 6 focused commands again because root guidance and version assertions changed.
- [x] Run version/root contracts:

```bash
bash tests/validate-lightweight-change-lane.sh
bash tests/validate-direct-edit-fast-path.sh
bash tests/validate-repair-first-verification.sh
bash tests/validate-progressive-verification.sh
bash tests/validate-human-help-version-docs.sh
bash tests/validate-project-local-skills.sh
bash tests/validate-root-agents-block-checker.sh
bash tests/validate-root-agents-block-refresh.sh
python3 -m unittest tests.test_root_agents_blocks tests.test_root_agents_lossless_slimming -v
```

Expected: all focused and version/root contracts pass; the two pre-existing date repairs remain present.

### Phase 2 Version-Sync Progress — 2026-08-30

- Human explicitly authorized changing the active development version to 1.5.9. `SKILL.md`, `plugin.json`, README, Usage, CHANGELOG, all 13 root managed blocks, active guidance examples, and version/root assertions now use the coordinated development truth; stable installation examples remain on the actually released `stable-v1.5.8` and no `stable-v1.5.9` release is claimed.
- The first Task 8 pass exposed a real owner-migration RED: Progressive Verification still required its review-depth invariant, but the old standalone Review owner was retired. The invariant now scales the inline Task Completion Review and single Final Review, and hard-floor contact explicitly exits Review Repair Fast Path; `validate-progressive-verification.sh` passes after repair.
- Root checker validation then exposed a stale-fixture RED whose substitution still targeted the old current revision and therefore produced no drift. The fixture now replaces `1.5.9-20260829.1` with the prior revision and again proves `STRUCTURAL_CHANGED`; root checker and root refresh contracts pass.
- Version-sync focused evidence is GREEN: the 61-test cross-owner Python set, 40 archive tests, 67-test focused wrapper, Task 6 affected Shell contracts, Direct Edit, Progressive Verification, Human Help/version docs, project-local skills, root checker/refresh, YAML/JSON, exact 13-block revision check, and `git diff --check` all pass.
- Task 9 must bind the now-changed dirty inputs. The pre-version full-run signature is expired and was never executed.

### Task 9: Present and obtain exact full-validation authorization

Record immediately before requesting confirmation:

- repository/worktree, branch, current HEAD, complete tracked/untracked input;
- macOS version, shell, Python, Ruby, and external target (`none`);
- exact commands below;
- expected duration/resource effect and intended claim: six-domain 1.5.9 release readiness, not release itself;
- statement that authorization is one run only and any input/HEAD/command/environment change, failure, or interruption requires a fresh confirmation.

Proposed exact full-run signature:

```bash
set -o pipefail
overall=0
for test_file in tests/*.sh; do bash "$test_file" || overall=1; done
python3 -m unittest discover -s tests -p 'test_*.py' || overall=1
ruby -e 'require "yaml"; YAML.load_file("SKILL.md")' || overall=1
ruby -rjson -e 'JSON.parse(File.read("plugin.json"))' || overall=1
find . -name '*.sh' -type f -print0 | xargs -0 -n1 bash -n || overall=1
python3 - <<'PY' || overall=1
from pathlib import Path
bad = []
for path in Path('.').rglob('*.md'):
    if '.git' in path.parts:
        continue
    fences = sum(
        1
        for line in path.read_text(encoding='utf-8').splitlines()
        if line.lstrip().startswith('```')
    )
    if fences % 2:
        bad.append(path.as_posix())
if bad:
    raise SystemExit('unbalanced Markdown fences: ' + ', '.join(bad))
PY
python3 scripts/check-root-agents-blocks.py --template templates/root-AGENTS.md --target templates/root-AGENTS.md --no-source-check || overall=1
git diff --check || overall=1
exit "$overall"
```

Stop and wait for an exact Human confirmation tied to this signature. Do not infer authorization from Phase 1 acceptance, version approval, “run necessary tests,” commit, or release requests.

### Task 10: Execute one full run and perform the six-domain semantic audit

**Files:** create `docs/reports/agent-loop-1.5.9-full-validation-2026-08-30.md` after evidence exists.

- [x] Run the confirmed commands exactly once against the recorded pre-repair input signature.
- [x] The run failed in 3 of 54 Shell scripts; stop automatic rerun, preserve the output, repair inside the accepted implementation boundary, and refresh all inputs before requesting another confirmation.
- [x] Audit the six domains from `docs/maintenance/full-validation-method.md` against the repaired sources with independent read-only reviewers:
  - Logic Correctness;
  - Autonomy;
  - Project Entry / Evidence Graph + DDD Onboarding;
  - Development / Test Workflow;
  - Memory;
  - Recommendation.
- [x] Re-run semantic pressure reasoning against current sources, not old report conclusions.
- [x] Record the first run's actual Shell/Python counts, mechanical results, RED/GREEN evidence, findings by severity, preserved invariants, and repaired-input candidate score without claiming a full GREEN rerun.
- [x] Record macOS as the actual executed platform.
- [x] Treat Windows as test-defined only: Python standard-library portability, path/CRLF-safe fixtures and commands, and no claim of native Windows execution unless it actually occurs.
- [x] Do not rate STRONG with an unexplained High; do not rate above FRAGILE with a Critical.
- [x] State that commit/push/tag/release/publish and installed-Skill sync are not implied.
- [x] Obtain a fresh exact Task 9 confirmation for the repaired input signature and corrected aggregate command, then rerun the full set exactly once.
- [x] Update the report with the rerun's final Shell/Python/mechanical result and only then make a full-GREEN or release-readiness claim.

### Task 11: Final scope, rollback, and release-readiness review

- [x] Compare final diff against the Proposal and this plan task by task.
- [x] Confirm no new canonical stage/status/mode/checker/artifact/force/skip surface.
- [x] Confirm all preserved Human Gates and authority boundaries.
- [x] Confirm new and legacy archive behavior.
- [x] Confirm all 13 managed blocks share the exact revision.
- [x] Confirm no unrelated `.agent-loop/`, cache, temporary, installed-Skill, v2.0.0, or generated artifacts entered the diff.
- [x] Present the Human with implementation summary, validation report, residual risk, and suggested commit message.
- [x] Stop before stage/commit/push/tag/PR/merge/release/publish. Each requires separate authorization.

Proposed commit message only after Human authorization:

```text
feat(v1.5.9): 内联任务审阅并启用 Agent 自主管理最终复核

- 将快速任务审阅内联到 Task Done Gate 并移除独立 Review 阶段
- 在 Feature 完成边界自动派发只读 Final Review Subagent
- 取消重复 Feature Close Review 并保留 Human Close Gate
- 以继承授权约束 Subagent 写入并兼容历史归档证据
- 同步 1.5.9 运行规则、模板、根指引、文档与回归验证
```

## 5. RED / GREEN Evidence Matrix

| Contract | RED evidence on v1.5.8 | GREEN evidence for v1.5.9 |
|---|---|---|
| Task flow | standalone Review is in Stage Order | Verify enters Task Done Gate with internal Task Completion Review |
| Task safety | review/helper ceremony is separate | missing authority/diff/verification/rollback/drift blocks Task Done |
| Final review | no single automatic whole-Feature reviewer | exactly one read-only reviewer after all Tasks/current verification |
| Findings | reviewer/owner boundary is incomplete | reviewer reports; owning Agent validates, repairs, routes, and verifies |
| Delegation | dispatch itself requires Human approval | dispatch is Agent-owned; delegated actions remain within existing authority |
| Repair freshness | duplicate review or vague reuse | bounded repair records freshness; material change requires fresh reviewer |
| Close | Feature Close Review is mandatory | current Final Review feeds completion; Human Close remains mandatory |
| Submit | separate review helper can repeat work | unchanged current review is reusable; changed inputs expire evidence |
| Fallback | no-subagent behavior can be ambiguous | recorded `controller-fallback`; review is not omitted |
| Archive | machine contract requires Feature Close Review | new Final Review readiness plus legacy read compatibility |
| Git fast path | must remain packaging-only | no review/completion claim added |
| Scope | old stages/statuses remain | no new canonical stage/status/mode/artifact/checker/force/skip |

## 6. Rollback Strategy

- Capture `git diff -- <task files>` before each task and keep the task file set explicit.
- Use `apply_patch` to reverse only edits owned by the current task; never use `git reset --hard`, `git checkout --`, `git clean`, or broad stash operations.
- If an unrelated edit overlaps an implementation target, stop and ask the Human rather than guessing ownership.
- If the new archive field breaks compatibility, retain dual-read logic (`Final Review` current, `Feature Close Review` legacy) and roll back only the new-write requirement until tests define a safe discriminator.
- If root managed blocks drift, restore one common pre-task revision across all 13 blocks; never leave mixed revisions.
- If version synchronization is partially applied, stop and restore consistent `1.5.8` active values or complete consistent `1.5.9` values only with Human direction; never leave a mixed skill version.
- A failed or interrupted broad run is evidence, not permission to edit outside the accepted scope or rerun automatically.

## 7. Scope-Drift And Stop Conditions

Stop immediately and report when any of these occurs:

- branch, HEAD, worktree, Proposal, or dirty-input boundary changes unexpectedly;
- another Agent modifies an overlapping file while a task is active;
- the implementation requires a new canonical stage, status, mode, checker, artifact directory, or force/skip option;
- a proposed simplification weakens an existing Human Gate or allows a Subagent to widen authority;
- no real RED can be demonstrated against v1.5.8 behavior;
- a focused test fails for an unrelated baseline defect;
- a legacy archive cannot be read without weakening new-format completion proof;
- controller fallback would silently omit or self-certify review;
- the 13 managed blocks or version-bearing files cannot be synchronized atomically;
- Phase 1 has not passed its Human Review checkpoint;
- a broad-run signature, input, environment, or target changes after confirmation;
- full validation fails or is interrupted and a rerun would be required;
- a requested action would touch `alpha/v2.0.0`, installed Skill state, Git history/remotes, tags, release, publish, production, or external systems without explicit authority.

## 8. Proposal Coverage Map

| Accepted Proposal requirement | Implementation owner |
|---|---|
| Inline mandatory Task review | Tasks 2-4; focused cases 1-3 |
| One automatic read-only Final Review | Tasks 2-5; focused cases 4-8 |
| Agent-owned repair and routing | Tasks 2-5; focused cases 8-12 |
| Remove Feature Close Review | Tasks 2, 4, 5; focused cases 13-14, 21 |
| Agent-owned Subagent dispatch | Tasks 2-3; focused cases 15-18 |
| Inherited authority / no widened permission | Tasks 2-3; focused cases 16-17 and pressure cases |
| Controller fallback | Tasks 2-3; focused case 18 |
| Submit evidence reuse | Task 5; focused cases 19-20 |
| Legacy compatibility | Task 4; focused case 21 |
| No new stage/status/mode/artifact/checker/force | Tasks 1, 6, 11; focused case 22 |
| Root/human/scenario coordination | Task 5 |
| Target version 1.5.9 | Tasks 7-8 |
| Full validation and six-domain report | Tasks 9-10 |
| Human implementation/full/Git/release gates | Phase boundaries and Tasks 0, 9, 11 |

## 9. Completion Boundary For This Plan

This plan artifact is complete when its design and task order are internally consistent and the Proposal is accepted. The live implementation state is recorded by the checked Task items and the Phase progress/checkpoint sections: Phase 1 implementation and Review Repair may be complete while Phase 2 remains pending. Plan completion or Phase 1 completion is not version synchronization, broad/full validation, commit, push, tag, release, publish, or installed-Skill synchronization.
