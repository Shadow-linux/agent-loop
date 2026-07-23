# Conflict-Driven Memory Reconciliation Implementation Plan

> **For agentic workers:** execute inline in the Agent Loop source repository. Do not create a target-project `.agent-loop/` workspace. Use RED/GREEN and stop at Human Review before commit.

**Goal:** Replace mandatory all-path post-merge reconciliation with conflict-driven semantic repair: no observed conflict means no action; observed conflicts are resolved from the smallest necessary fact set; only unresolved meaning reaches the human.

**Architecture:** Runtime guidance selects a lightweight conflict path by default and reserves the existing four-snapshot transaction tools for explicitly authorized Full Memory Audit / Recovery. The normal report becomes conflict-only. Existing deterministic audit/apply/restore code remains available behind an explicit full-audit CLI acknowledgement.

**Tech Stack:** Markdown workflow contracts, Python 3.10+ standard library CLI, shell/Python regression tests.

**Design Source:** `docs/proposal/v1.5.x/conflict-driven-memory-reconciliation.md`

**Human Authorization:** The human explicitly approved inline correction on 2026-07-23 and rejected review of unchanged or unrelated memory.

---

## File Structure

### Canonical workflow

- Modify `SKILL.md`: route only observed memory conflicts; remove all-path / Desired Snapshot requirements.
- Modify `references/design.md`: replace the global all-path invariant with the human-like current-understanding model.
- Modify `references/runtime.md`: add `not-needed`, targeted conflict resolution, and explicit Recovery escalation.
- Rewrite `references/memory-reconciliation.md`: own the normal conflict-driven procedure and link Full Audit only as an exceptional fallback.
- Modify `references/submit-and-integrate.md`: do not block later Git gates when reconciliation is `not-needed`.

### Stage and artifact projections

- Modify `references/stage-guides.md`
- Modify `references/human-review-summary.md`
- Modify `references/project-memory-mode.md`
- Modify `references/recovery-and-backfill.md`
- Modify `references/artifact-rules.md`
- Modify `references/document-templates.md`
- Modify `references/validation-scenarios.md`
- Modify `references/workflow-checklists.md` when it projects the old normal flow.
- Modify `templates/root-AGENTS.md`
- Replace `templates/memory-merge-report.md` with the concise conflict report.
- Create `templates/full-memory-audit-report.md` from the existing deterministic audit report.

### Recovery tooling

- Modify `scripts/scan-memory-reconciliation.py`: identify itself as Full Memory Audit / Recovery and require `--full-audit-authorized`.
- Keep `scripts/check-memory-reconciliation.py`, `scripts/apply-memory-reconciliation.py`, `scripts/restore-memory-reconciliation.py`, and `scripts/memory_reconciliation_support.py` as deterministic Full Audit transaction tooling.
- Modify `tests/memory_reconciliation_test_support.py` to use `templates/full-memory-audit-report.md` and pass the explicit audit flag.

### Human docs and release record

- Modify `README.md`
- Modify `Usage.md`
- Modify `CHANGELOG.md`

### Validation

- Modify `tests/validate-post-merge-memory-reconciliation.sh`
- Modify `tests/test_memory_reconciliation_scan.py`
- Update other reconciliation tests only where the explicit Recovery flag/template location changes.
- Create a full validation report under `docs/reports/`.

---

## Task 1: Establish RED for the wrong normal behavior

**Files:**

- Modify: `tests/validate-post-merge-memory-reconciliation.sh`
- Modify: `tests/test_memory_reconciliation_scan.py`

- [x] Add assertions that normal runtime says:
  - no observed conflict -> `not-needed`;
  - no report or Human Gate for `not-needed`;
  - only conflicting facts and direct owners are inspected;
  - unresolved choices alone reach the human;
  - all-path audit is Recovery-only.
- [x] Add negative assertions forbidding normal-route wording:
  - `all-path Path Accounting Ledger`;
  - mandatory Desired Target Memory Snapshot;
  - “memory changed or may differ” as sufficient entry;
  - mandatory full-tree zero-change post-check.
- [x] Add a Python test that invokes `scan-memory-reconciliation.py` without `--full-audit-authorized` and expects a controlled failure naming Full Memory Audit / Recovery.
- [x] Run:

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
python3 -m unittest tests.test_memory_reconciliation_scan -v
```

Expected: both contain RED failures because current runtime still requires all-path reconciliation and the scanner still runs without explicit Recovery acknowledgement.

## Task 2: Fix canonical design and runtime semantics

**Files:**

- Modify: `SKILL.md`
- Modify: `references/design.md`
- Modify: `references/runtime.md`
- Rewrite: `references/memory-reconciliation.md`
- Modify: `references/submit-and-integrate.md`

- [x] Replace normal entry with:

```text
verified Git merge
-> observed Agent Loop memory conflict?
   -> no: reconciliation-not-needed
   -> yes: inspect conflict + minimum direct evidence
```

- [x] Define the Target memory as current understanding, Source changes as new experience already integrated by Git, current verified facts as the correction source for present-tense Agent claims, and accepted authorities as immutable constraints.
- [x] Remove normal all-path/four-snapshot/Desired Snapshot/Exact Plan requirements.
- [x] Define conflict scope as the conflicting fact, canonical owner, direct derived references, and minimum evidence only.
- [x] Let the Agent resolve fact-determined conflicts without a separate Human Gate.
- [x] Require a concise choice table only when evidence cannot determine the correct memory.
- [x] Keep a small conflict and bounded Human choice in the conversation without mandatory file creation.
- [x] Make `not-needed` sufficient to continue to separately authorized Git actions.
- [x] Preserve action-specific Git gates.

Run:

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
```

Expected: reference assertions advance toward GREEN; template/tool assertions may still fail until later tasks.

## Task 3: Split normal conflict reports from Full Audit reports

**Files:**

- Create: `templates/full-memory-audit-report.md`
- Rewrite: `templates/memory-merge-report.md`
- Modify: `references/document-templates.md`
- Modify: `references/artifact-rules.md`
- Modify: `references/project-memory-mode.md`
- Modify: `references/human-review-summary.md`

- [x] Preserve the old ledger/plan sentinels only in `templates/full-memory-audit-report.md`.
- [x] Make the normal report optional: use conversation review for small conflicts, and create a report only for coupled conflicts, cross-session handoff, substantial recovery/rollback evidence, or an explicit Human request.
- [x] When created, make the normal report contain only merge identity, observed conflicts, evidence, Agent resolutions, unresolved Human Decisions, changed paths, targeted checks, rollback, and remaining risk.
- [x] Specify no report for `not-needed`.
- [x] Remove unchanged-path, absence-claim, full inventory, all-green item, and exact full-tree Plan Hash review from normal Human Review.
- [x] Keep Full Audit report status/transaction details isolated from normal project memory.

Run:

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
ruby -e 'ARGV.each { |f| abort f if File.readlines(f).grep(/^`{3}/).length.odd? }' templates/memory-merge-report.md templates/full-memory-audit-report.md
```

Expected: GREEN for report ownership and balanced fences.

## Task 4: Guard Full Audit tooling behind explicit Recovery authorization

**Files:**

- Modify: `scripts/scan-memory-reconciliation.py`
- Modify: `tests/memory_reconciliation_test_support.py`
- Modify: `tests/test_memory_reconciliation_scan.py`

- [x] Add:

```python
value.add_argument(
    "--full-audit-authorized",
    action="store_true",
    help="explicitly acknowledge Full Memory Audit / Recovery scope",
)
```

- [x] Fail before inventory when the flag is absent with a deterministic message:

```text
Full Memory Audit / Recovery requires explicit authorization
```

- [x] Update test helpers and existing successful scanner tests to pass the flag.
- [x] Keep scan read-only and preserve current cross-platform safety behavior.

Run:

```bash
python3 -m unittest \
  tests.test_memory_reconciliation_scan \
  tests.test_memory_reconciliation_check \
  tests.test_memory_reconciliation_apply \
  tests.test_memory_reconciliation_restore \
  tests.test_memory_reconciliation_support -v
```

Expected: all reconciliation Python tests PASS, including the new missing-authorization RED turned GREEN.

## Task 5: Align stage, root, recovery, and human routing

**Files:**

- Modify: `references/stage-guides.md`
- Modify: `references/recovery-and-backfill.md`
- Modify: `references/validation-scenarios.md`
- Modify: `references/workflow-checklists.md`
- Modify: `templates/root-AGENTS.md`

- [x] Change root signal to “verified merge has an observed Agent Loop memory conflict”.
- [x] Remove “memory may differ” and “any memory changes” as mandatory entry.
- [x] Add clean independent merge and source-only artifact scenarios that finish `not-needed`.
- [x] Add targeted stale/current conflict and ambiguous meaning scenarios.
- [x] Add unrelated drift scenario that reports separately without expanding the merge.
- [x] Route corruption, incomplete transactions, broad identity failure, or explicit human request to Full Memory Audit / Recovery.
- [x] Keep recovery transactions and restore requirements unchanged for Full Audit.
- [x] Refresh every root managed block and live revision consumer to `block-version:1.5.0-20260723.2` after changing the Gateway/stop contract.

Run:

```bash
bash tests/validate-post-merge-memory-reconciliation.sh
bash tests/validate-root-agents-block-refresh.sh
python3 -m unittest tests.test_root_agents_lossless_slimming tests.test_project_guidance_consistency -v
```

Expected: all PASS.

## Task 6: Update human-facing docs and changelog

**Files:**

- Modify: `README.md`
- Modify: `Usage.md`
- Modify: `CHANGELOG.md`

- [x] README explains:

```text
no conflict -> no memory work
conflict -> Agent resolves only the affected fact
ambiguous -> human chooses
```

- [x] Usage uses one natural human phrase:

```text
代码合并时记忆有冲突，帮我看看冲突在哪里，按最新事实理顺；你判断不了的再列给我。
```

- [x] Changelog records the correction under v1.5.0 without a version bump.
- [x] Do not expose Full Audit mechanics as normal usage.

Run:

```bash
bash tests/validate-human-help-version-docs.sh
bash tests/validate-post-merge-memory-reconciliation.sh
```

Expected: PASS.

## Task 7: Focused and full validation

**Files:**

- Read: `docs/maintenance/full-validation-method.md`
- Create: `docs/reports/agent-loop-1.5.0-conflict-driven-memory-reconciliation-validation-2026-07-23.md`

- [x] Run the focused reconciliation Python and shell suites.
- [x] Run root guidance validators.
- [x] Run YAML, JSON, shell syntax, Python compile, Markdown fence, and `git diff --check`.
- [x] Run the repository's complete full-validation method because canonical routing, Submit ordering, Human Gates, and root Stage Map changed.
- [x] Perform the required semantic audit, including:
  - clean merge does nothing;
  - independent history remains untouched;
  - only affected facts are read;
  - latest facts update current memory;
  - accepted meaning is preserved;
  - ambiguity reaches the human as concrete alternatives;
  - Full Audit cannot start without explicit authorization.
- [x] Record exact commands, results, failures repaired, residual risk, and recommendation in the Chinese report.

## Task 8: Final review

- [x] Search runtime surfaces for obsolete normal-path phrases:

```bash
rg -n 'all-path Path Accounting Ledger|Desired Target Memory Snapshot|memory changed or may differ|expected unchanged paths' \
  SKILL.md references templates/root-AGENTS.md README.md Usage.md
```

Only explicitly labelled Full Memory Audit / Recovery references may remain.

- [x] Review `git diff` and `git status`, exclude `.tmp/` and `__pycache__/`.
- [x] Confirm no target-project `.agent-loop/` artifacts were created.
- [x] Stop at Human Review. Do not commit or push without a new explicit instruction.
