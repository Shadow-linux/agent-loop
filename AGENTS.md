# Agent Loop Skill

This repository contains the `agent-loop` skill source.

## Repository Purpose

- Maintain the reusable `agent-loop` skill.
- This is a skill source repository, not a target project using `agent-loop`.
- Do not create target-project `.agent-loop/requirements/` or feature docs here unless editing examples.
- The skill should make agents own workflow diagnosis and sequencing while keeping required human gates explicit.

## Source Of Truth

- `SKILL.md`: concise skill entrypoint loaded by CLI agents.
- `references/`: detailed operational rules loaded by the skill.
- `templates/`: document templates written into target projects.
- `README.md`: human-facing overview and install notes.
- `Usage.md`: human-facing operation guide.
- `CHANGELOG.md`: version history.
- `examples/`: example project states and feature artifacts.
- `agents/openai.yaml`: OpenAI/Codex skill metadata.

## Maintenance Rules

- Prefer `rg` for search and normal shell commands for inspection.
- Use `apply_patch` for manual edits.
- Do not use a global shell wrapper unless this repository explicitly asks for one.
- Keep `SKILL.md` concise; move detailed behavior into `references/`.
- Do not add unsupported frontmatter fields to `SKILL.md`; keep the YAML frontmatter limited to stable loader fields unless the loader requirement changes.
- Keep references and templates consistent with `SKILL.md`, `README.md`, and `Usage.md`.
- Update `CHANGELOG.md` for meaningful behavior, gate, artifact, template, or example changes.
- Do not bump the skill version unless the human explicitly approves the version upgrade.
- If a meaningful skill change is committed without a human-approved version bump, record it under the current unreleased or in-progress changelog section instead of changing version numbers.
- If the human explicitly approves a version bump, update every version-bearing file in the same change so the repository never carries mixed skill versions.
- For this repository, when working on an `alpha-v<x.y.z>` branch, treat `<x.y.z>` as the intended skill version; ignore the `alpha` prefix for version records and changelog headings after the human approves implementation for that version.
- Commit messages for this skill repository should use type + version scope, prefer Chinese, and include a concrete multi-line body for meaningful changes.
- Stable release branches use the exact version name, for example `v1.0.1`, not `release/1.0.1`.

## Version Sync Checklist

When the human explicitly approves a skill version bump, update these files together:

- `SKILL.md`: `Version: <x.y.z>`
- `plugin.json`: `"version": "<x.y.z>"`
- `README.md`: `Current version`
- `Usage.md`: human-facing version label
- `CHANGELOG.md`: new version heading and dated release section
- `templates/root-AGENTS.md`: both the `section:meta` managed block attribute `version:<x.y.z>` and the visible natural-language synced-version text, currently written as `agent-loop` skill version `<x.y.z>`

Also verify whether these files need wording or example updates after a version bump:

- `references/project-guidance.md`: if version-sync rules or root guidance refresh behavior changed
- `references/submit-and-integrate.md`: if commit/version examples mention a concrete version
- `examples/`: only when example docs or generated guidance intentionally show concrete version strings

Rules:

- Do not bump versions in only human-facing docs while leaving templates or metadata behind.
- Do not change the version number in commit examples unless the example is meant to reflect the current skill version.
- After a version bump, run a repository search for the old version string to catch leftover references before commit.

## Commit Message Rules

Use this format for meaningful `agent-loop` repository commits:

```text
<type>(v<version>): <Chinese summary>

- <concrete behavior/template/reference/scenario/doc change>
- <concrete behavior/template/reference/scenario/doc change>
- <concrete behavior/template/reference/scenario/doc change>
```

Allowed types:

```text
feat, fix, docs, refactor, test, chore
```

Rules:

- Prefer Chinese for the summary and body unless the project context requires English.
- Include the current skill version scope, for example `docs(v1.2.3): 调整 Project Entry Scan 文档结构`.
- Do not use one-line-only commit messages for meaningful behavior, gate, artifact, template, reference, validation, or example changes.
- Use 3-7 bullet lines in the commit body, focused on concrete changes and user/agent-facing behavior.
- Use `docs` for proposals, README, Usage, and explanatory docs.
- Use `feat` for new skill capabilities or artifact behavior.
- Use `fix` for rule loopholes, broken routing, incorrect gates, or misleading templates.
- Use `test` for validation scenarios or pressure tests.
- Use `chore` for metadata, formatting, version alignment, or maintenance-only work.
- Keep the version number unchanged unless the human explicitly approves a version bump.

## Hard Red Lines

- Do not make Delivery Contracts default artifacts.
- Do not allow tasks to become `done` without verification, evidence, review, and drift rules in the skill.
- Do not remove human gates for Delivery Contract file creation/acceptance/breaking changes, submit, pause, close, commit, PR, merge, release, or publish.
- Do not add unsupported `SKILL.md` frontmatter fields unless loader support is confirmed.

## Verification

After edits, run at least:

- `ruby -e 'require "yaml"; YAML.load_file("SKILL.md")'`
- a Markdown fence balance check
- `git diff --check`

## Full Skill Validation

When the human asks for a full validation of the `agent-loop` skill, use the following dimensions and methods. This is a logic-level validation, not a "are there enough details" review.

### Validation Dimensions

Validate these six domains. Each domain checks logic correctness, not operational detail completeness.

1. **Logic Correctness**
   - Rule conflicts: file A says "must X", file B says "must not X" or "do not X"
   - Stage dependency deadlocks: stage A requires B, but B requires A
   - Auto Mode vs Stop And Ask consistency: Auto Mode must respect all Stop And Ask conditions; no bypass paths
   - Entry Classification completeness: all realistic project states have a matching classification; overlapping states with different next stages need explicit priority
   - Status state machine consistency: all status transitions are legal; no unreachable or非法 transitions

2. **Autonomy**
   - Agent Ownership is mandatory and executable: every loop must output "Recommended next stage" and "Why"
   - Response Frame sufficiency: current state, recommended next stage, why, artifacts to read/write, human gate
   - Three execution modes (Strict / Feature Auto-Loop / Task Auto-Run) have clear自主 boundaries
   - Stage Helper Capability Scan is agent-initiated; fallback is automatic; external skills are accelerators only
   - No "I don't know what to do next" legal exit — `blocked` still recommends "Ask Human / Diagnose"

3. **Project Entry / Evidence-Graph + DDD Onboarding Logic**
   - Existing projects route to Project Entry Scan only: project memory, root guidance, commands, boundaries, capabilities, uncertainties
   - Old onboarding-db / Deep Onboarding generation is replaced by Evidence-Graph + DDD Onboarding after Project Entry Scan or reliable memory
   - Deleted legacy references and templates are not loaded or recreated
   - Existing legacy onboarding-db paths are evidence only; stale references route to recovery/backfill without regeneration
   - Cross-file consistency: SKILL.md, runtime, stage guides, checklists, Usage, and validation scenarios all require Evidence Graph, Onboarding Spec, Onboarding Tasks, single-file module/flow docs by default, and wireframe architecture flow diagrams as the preferred main flow expression

4. **Dev/Test Workflow Logic**
   - Plan Gate blocks "create tasks then immediately implement"; two exits (accepted plan / No-Plan Decision) cover all scenarios
   - TDD chain (RED → verify RED → GREEN → verify GREEN → refactor) is enforced; no skip-RED path
   - Task Done Gate conditions are all necessary and non-redundant; "drift decision recorded even if no drift" is executable
   - Review → Drift → Memory Update forms a closed loop, not isolated stages
   - Feature Completion Check trigger timing covers all scenarios; no bypass path
   - Feature Follow-up / Flow-back logic covers all bug/change intake patterns

5. **Memory Logic**
   - Simple vs Enterprise switch has clear triggers; human confirmation required; index-detail split is self-consistent
   - Stale Memory detection → Recovery Backfill path is complete; "code reality wins" holds in all scenarios
   - Managed Block version sync logic is sound; semver comparison; human content preserved
   - Cross-feature memory consistency: project memory update is triggered after feature changes; no multi-active-feature memory conflict漏洞
   - Memory and Guidance dependency: Project Entry Scan is incomplete if guidance is missing/stale; no bootstrap gap

6. **Recommendation Logic**
   - All stage completions have明确 exits (Submit / Pause / Close)
   - Vague goals route to Project Entry Scan / resume / clarify
   - Uncompletable tasks route to "Ask Human"
   - Recommendation has uniqueness: agent recommends exactly one next stage

### Validation Method

- Launch parallel sub-agents (using the Task tool with `code-explorer` subagent) to cover all six domains simultaneously.
- Each sub-agent reads the relevant `references/` files, `SKILL.md`, `templates/`, and `references/validation-scenarios.md`.
- Each sub-agent outputs structured results per dimension: result (PASS / CONFLICT / DEADLOCK / GAP / WEAK), findings with file paths and line numbers, severity (Critical / High / Medium / Low), and concrete issues.
- Only report real logic problems: rule conflicts, stage deadlocks, safety bypass paths, state machine inconsistencies, memory loss risks.
- Do not report "I wish it were more detailed" or "I wish it had more hardcoded boundaries" — agent-loop trusts agent intelligence and provides principles, not SOPs.

### Severity Levels

- **Critical**: rule conflict causing unpredictable agent behavior, or safety bypass allowing human gate skip
- **High**: logic gap causing agent to make inconsistent next-stage choices, or memory conflict risk
- **Medium**: missing transition rule or cross-file inconsistency that agent can work around but may cause confusion
- **Low**: minor wording mismatch or edge case not covered, no practical impact

### Output

Summarize all sub-agent results into a single report with:
- Overview table (domain × result × severity)
- High-severity issues first, with file paths and line numbers
- PASS dimensions listed briefly
- Final conclusion: can the skill run? What needs fixing first?

### Commit Pressure Testing

When the human asks to pressure-test specific commits:

- Read each commit's diff (`git show --stat <hash>` and `git show <hash> -- <files>`)
- Launch one sub-agent per commit to design and run pressure test scenarios
- Run any contract test scripts (`tests/*.sh`) if they exist
- Evaluate stability (STABLE / FRAGILE / BROKEN) and effectiveness (EFFECTIVE / WEAK / INEFFECTIVE)
- STABLE = logic is self-consistent, edge cases have clear rules
- FRAGILE = main path works but specific conditions may fail; depends on agent compliance or has uncovered edge cases
- BROKEN = main path has logic conflict or broken chain
- Only report real issues, not "wish it were more detailed"
