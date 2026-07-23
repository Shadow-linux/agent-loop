# Agent Loop Workflow Checklists

Use the relevant checklist before entering a stage.

Before fallback stage guidance:

- [ ] Run Stage Helper Capability Scan against the current runtime's available skills/plugins/helpers.
- [ ] If a matching helper exists for the current stage, load `skill-routing.md` and `external-skill-adapters.md`.
- [ ] Prefer the matching helper as the method quality bar, while keeping agent-loop artifact paths, gates, task status, project memory, submit, and close control.
- [ ] If no matching helper exists or it cannot be loaded, continue with the fallback stage guide.

Before human approval for non-trivial stage output:

- [ ] Load `human-review-summary.md`.
- [ ] Present a table-first approval view.
- [ ] Include artifacts, evidence, risk/blockers, human decision, and next stage.
- [ ] Keep full source-of-truth content in artifact files.

Before using an external skill or plugin inside a stage:

- [ ] Load `skill-routing.md` and `external-skill-adapters.md`.
- [ ] Confirm the external skill is improving the current agent-loop stage, not replacing the stage controller.
- [ ] Treat external default artifact paths as advisory only.
- [ ] Write results to the owning agent-loop artifact.
- [ ] Do not create external default directories such as `docs/superpowers/*` unless the human explicitly requests native external output and then confirms after the agent explains the agent-loop path override.
- [ ] Do not let the external skill mark tasks `done`, close a feature, submit code, update project memory, accept Delivery Contracts, approve breaking changes, or skip human gates.

## Optional Visual Communication

- [ ] Confirm a real Visual Trigger; installed capability alone is not a reason to generate.
- [ ] Resolve a matching active project-local visual skill before installed Archify.
- [ ] If Archify is unavailable and would materially improve review, recommend its exact installation/use before offering Markdown/table/Mermaid/ASCII; use fallback directly only when unjustified, declined, unsupported, unavailable after recommendation, or failed.
- [ ] Before installation, disclose exact source/revision/command/target/network-file-global effects/doctor/fallback and obtain a separate Installation Authorization.
- [ ] Before generation, obtain one Visual Scope Grant naming stage, question, semantic source/IDs, type, working output, and iteration boundary.
- [ ] Use `render to converge, text to record`; rewrite accepted feedback into the owning semantic artifact.
- [ ] For a durable visual, obtain separate confirmation and validate the `source-render-v1` typed source plus derived render and both digests.
- [ ] Keep installation, generation, durable recording, semantic acceptance, Feature, project-skill execution, Git, and release gates independent.

## Requirement/Product Grill Method

- [ ] Load `requirement-product-grill.md` when Requirements Discussion or its Brainstorm / Clarify work has ambiguous terminology, business rules, flows, boundaries, exception paths, historical Feature behavior, or decision signals.
- [ ] Before asking a grill question, inspect project memory, human sources, current Effective Product Definition, code/docs/tests, and targeted prior Feature artifacts when relevant.
- [ ] Ask one blocking question at a time and include the agent's recommended answer.
- [ ] If prior feature artifacts conflict with the current statement, state the conflict and ask whether to reuse, override, or treat it as new scope.
- [ ] Do not turn a grill design signal into an accepted ADR; record Design Readiness evidence and route required shared design to Decision & Design.
- [ ] Do not create external `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/` paths.
- [ ] Keep ownership explicit: Requirements Discussion drafts Requirement `product.md`; README owns pointer/lifecycle/phase/mapping; Feature Spec owns Product Slice/implementation behavior; legacy Feature Product Brief is read-only.
- [ ] Keep Requirement README limited to source pointer, lifecycle, Delivery Phase, Feature Mapping, and decision-link summaries rather than duplicating Product Definition.
- [ ] If Requirement/Product Grill was used, verify Standard `product.md` carries the applicable terminology, flows, exceptions, fact ownership, historical conflicts, acceptance direction, and Decision Candidates.

## Concept Foundation Gate

- [ ] Classify `Concept Foundation Status` before detailed requirement-level Business Flow, Product State Model, or Requirement Product Model work.
- [ ] Trigger `candidate` for overloaded terms, identity/lifecycle/state changes, multi-actor/tenant/system flows, cross-feature work, hard-to-reverse fact semantics, or conflicts with Domain Language/code/tests/history.
- [ ] Use `concept-foundation-not-needed` only with a concrete reason showing no product-semantic, identity, lifecycle, ownership, state, relationship, cross-role, cross-feature, or data-meaning change.
- [ ] Follow the Human Grill Contract in order: inspect evidence; extract and display candidate concepts; present one recommended definition with Concept ID, evidence, boundary, and accept/reject impact; ask exactly one downstream-blocking question.
- [ ] Keep status `candidate` or `reopened` while any unresolved meaning can change downstream flow, state, product data, terminal behavior, or invariants.
- [ ] Do not draft Business Flow, Product State Model, or Requirement Product Model as assumptions plus open questions while the gate is blocked.
- [ ] Set `accepted` only after the human confirms every blocking concept definition.
- [ ] Before Product Review confirmation, load `human-review-summary.md` and present cumulative Product Definition Approval; keep the one-question-per-turn Grill as the method for resolving blockers.
- [ ] After internal acceptance, derive only applicable Concept Relationships, Role / Permission Matrix, Commands / Events, Primary Business Flow, Product State Model, Requirement Product Model, invariants, exceptions, and recovery from stable Concept IDs.
- [ ] Record Concept-To-Product Traceability and reject any derived row whose Concept ID is undefined or unaccepted.
- [ ] After record/archive, preserve human sources and prior Product Definitions; route `reopened` through Requirement Conflict Review, `YYYY-MM-DD-product-follow-up-<slug>.md` or a linked replacement set, and README `Effective Product Definition` update after Human Review.
- [ ] Keep Concept Foundation inside Requirements Discussion / Requirement Product Grill; do not add a canonical stage, `.agent-loop/concepts/`, YAML/JSON schema, ADR, Design Skill, or E2E Skill output.

## Design Readiness Check

- [ ] Run before an accepted Requirement enters Feature construction, and repeat when Product Definition, Technical Design, or Drift reveals new shared design needs.
- [ ] Check for multiple features, end-to-end business closure, shared domain/state/source-of-truth rules, consistency/concurrency/recovery needs, measurable non-functional goals, and cross-system or durable boundaries.
- [ ] Do not bypass Decision & Design merely because no technology choice is disputed.
- [ ] Record `design-not-needed`, `candidate`, `required`, or `completed` plus signals, shared design needs, recommended next stage, decision records, and coverage status in the requirement README.
- [ ] Route `required` to Decision & Design If Needed before Feature Spec construction.

## Decision Scan / Placement

- [ ] Load `project-decisions.md` when a requirement/product/spec/technical design/drift signal may affect multiple features or long-term project direction.
- [ ] Confirm whether the candidate belongs in product.md, spec.md Design Decisions, tests.md, notes.md, or `.agent-loop/decisions/*.md`.
- [ ] Do not create or accept a decision file without explicit human confirmation.
- [ ] Do not mark a decision file `accepted` unless the human explicitly accepted that decision.
- [ ] Do not create ADR files from ordinary chat or early fuzzy requirements discussion.
- [ ] Before Feature Spec for complex accepted requirements, verify whether shared business-flow or architecture direction is needed.
- [ ] Treat Decision Scan / Placement as a method inside Decision & Design, not the whole design stage.
- [ ] When shared design is required and no accepted decision already covers it, keep Feature Spec blocked until a Human-gated Decision & Design record is accepted.
- [ ] Before Feature Spec, verify every required design slice has at least one planned owning feature and no required slice is unassigned.
- [ ] If a project-level decision is required but unresolved, stop before Feature Spec or Plan Gate.
- [ ] Verify requirement README, product.md, and spec.md decision references stay aligned.
- [ ] Remember that `.agent-loop/decisions/` is available in simple and enterprise memory modes and does not trigger enterprise mode by itself.

## ADR Requirement Model Technical Landing

- [ ] Resolve README `Effective Product Definition` or legacy `Effective Concept Foundation` and record the dual-reader Effective Requirement Snapshot before technical landing.
- [ ] Require new Product Review `confirmed` and any triggered internal Concept Foundation accepted; return pending / `candidate` / `reopened` to Requirements Discussion.
- [ ] Declare accepted Concept IDs and in-scope Requirement Model IDs without copying or redefining product meaning.
- [ ] Inventory every stable source model ID (`REL-*`, `PERM-*`, `CMD-*`, `EVT-*`, `FLOW-*`, `STATE-*`, `PM-*`, `EX-*`) and give every out-of-scope ID an accepted-decision, feature-local, proposed-decision, or reasoned not-applicable owner.
- [ ] Give every in-scope accepted Requirement Model ID exactly one Requirement Model Technical Landing Trace disposition.
- [ ] Apply the Coverage Hard Gate: every `landed` row has Technical Landing, Preserved Invariant, Design Slice, and Verification; non-landed dispositions name an owner or concrete reason.
- [ ] Treat `Applicable Decisions` as awareness only, never as a substitute for Requirement Model coverage or Design Slice ownership.
- [ ] Keep `Upstream Compatibility: review-required` separate from ADR lifecycle status and block dependent Feature Spec, Plan, and implementation.
- [ ] When an accepted decision no longer holds, create a Human-gated superseding ADR instead of rewriting accepted decision meaning.
- [ ] Assess operational landing triggers; expand Migration / Backfill, Compatibility, Rollout / Cutover, or Rollback / Reversibility only when triggered, otherwise record a concrete `not-triggered` reason.
- [ ] Keep the ADR `proposed` for structural preflight; after it passes, present the Human Review Summary and wait for explicit acceptance before recording Human Review Evidence and rerunning accepted-mode validation.
- [ ] For Brief or a legacy reasoned `concept-foundation-not-needed` source with no applicable stable IDs, use trace-not-applicable and do not invent Concept or Requirement Model rows.
- [ ] Load `human-review-summary.md` and present the Decision & Design Human Review Summary before creating, accepting, superseding, or materially updating the record.
- [ ] If `Optional Visual Evidence` exists, validate its concrete Review Question, accepted semantic references, typed source/render pair, digests, generator, validation evidence, and `current` status; never treat it as ADR acceptance.

## Human-Guided Branch Management

- [ ] Run Branch Strategy Check during Project Entry, Project Entry Scan, Re-Adopt, versioned delivery planning, Drift Check, and Submit / Integrate.
- [ ] Inspect human-confirmed policy, native repo guidance/config, current Git reality/history, and feature/plan/submit evidence in that order.
- [ ] Preserve a simple project or clear existing strategy; do not force migration to the optional profile.
- [ ] When rules are confused, Target Release Context is unclear, or customer isolation is risky, load `branch-management.md` and present one recommendation.
- [ ] Record `accepted | declined | not-needed` only from an explicit human decision; an unconfirmed recommendation is not accepted.
- [ ] Keep durable strategy and current Target Release Context pointer in `project.md`; keep mutable Current Branch Context in feature notes, plan, or Submit / Integrate evidence.
- [ ] Block same-version work against a `released / sealed` target; repair uses a new patch version and new capability uses a human-confirmed new version.
- [ ] Do not flow a customer release branch wholesale into `main` or a standard release line.
- [ ] Do not treat recommendation, adoption, plan acceptance, or auto mode as permission to create, switch, merge, delete, push, tag, release, or publish.
- [ ] Require a Branch Action Gate before creating or switching one exact development branch.
- [ ] Require merge evidence plus separate human confirmation before deleting a temporary development branch; retain release aggregation branches.
- [ ] Do not create a default `.agent-loop/branches/` directory.

## Message Intent

- [ ] Classify the latest human message intent before project state classification.
- [ ] If message intent is `chat`, answer or discuss only; do not create a requirement set or feature workspace.
- [ ] Reclassify chat when the conversation turns into requirements discussion, feature implementation, operational support, follow-up, or deferred requirement intake.
- [ ] Reclassify as `project-skill-management` when the human asks to make a repeatable project workflow into a skill or manage an existing project skill.
- [ ] Reclassify chat as `proposal-doc` when the human asks for a proposal/design note without implementation.
- [ ] Keep intent as `chat` when the human explicitly wants discussion without documentation.
- [ ] If message intent is `requirements-discussion`, route to Requirements Discussion before Feature Spec.
- [ ] During Requirements Discussion, use Brainstorm / Clarify plus Product Definition Depth Scan and produce a Human-reviewed Brief/Standard Requirement `product.md` before Record / Archive.
- [ ] Write the reviewed Product Definition under `.agent-loop/requirements/<record-date>-<topic>/` only after exact source/output disclosure and human confirmation.
- [ ] Preserve human original bytes and do not move Product Definition into Feature docs; new Feature `spec.md` consumes Product Slice and no new Feature `product.md` is created.
- [ ] If unclear whether this is chat or requirements discussion, ask whether to keep discussing or shape the topic into a requirements document.
- [ ] If unclear whether this is requirements discussion or feature implementation, ask whether to form a requirements document first or start feature construction.

## Workflow Gateway Routing

- [ ] After Message Intent and project-state classification, select exactly one next stage.
- [ ] Workflow Gateway Map routes the current signal to exactly one first hop and the exact published reference set.
- [ ] Confirm every Gateway reference exists in the installed package and load the owning reference before action.
- [ ] Use `references/runtime.md` for routing precedence and complete leaf-stage order; a Gateway never removes or reorders downstream stages.
- [ ] Reclassify and select a new stage only when the latest human intent or project evidence changes.

## Lightweight Change Lane

- [ ] Confirm Project Entry classification and perform only the minimum root-guidance, Git/dirty-state, scope, nearby-reference, safety, branch/sealed, and verification-entry checks needed for the route.
- [ ] Check explicit Bug Management and active Feature ownership before lightweight eligibility.
- [ ] Require every eligibility condition; treat any Feature hard trigger as decisive.
- [ ] If uncertain, stop with few real options, evidence, one Agent recommendation, and zero writes before the human answer.
- [ ] After clearly-eligible routing and before the first target write, create one parser-valid card at `<memory-root>/changes/YYYY-MM/YYYY-MM-DD-<topic>.md` with all metadata, required sections, and initial Memory fields.
- [ ] Reuse the one accepted root, fail closed on dual roots, treat changes-only as not initialized, and allocate the first unused same-day topic suffix without overwrite.
- [ ] Keep a Plan in every card and adapt depth to risk; never use No-Plan Decision.
- [ ] When a reliable memory root exists, run Project Skill Discovery Guard and preserve the matched Project Skill Execution Gate.
- [ ] Record why the change uses targeted verification or the smallest meaningful RED/GREEN.
- [ ] Stop before broader edits on scope expansion and recommend exactly one Bug Management, Requirements Discussion, or Feature Construction route.
- [ ] Before completion, close/explain Plan items, replace initial Memory markers, run fresh targeted verification, and review diff, disclosed scope, durable-memory impact, sensitive evidence, and rollback.
- [ ] After completion, run `scripts/scan-lightweight-changes.py`; keep `human-review` visible and start Agent semantic consolidation for three pending or oldest age greater than seven days.
- [ ] Allow accidental resume only after branch/full-HEAD/dirty-diff/Scope/Plan/eligibility/verification/rollback revalidation; route planned cross-session/handoff/Subagent/long-observation work to Feature.
- [ ] Before high-evidence memory sync, require an existing reliable owner and disclose exact target path, fact, evidence, impact, and rollback; restore only this Agent's memory edit on failure.
- [ ] Confirm branch, submit, production, external, paid, configuration-write, destructive, Feature/Bug lifecycle, and Git gates remain separate.
- [ ] Report completed/cancelled Plan steps, result, residuals, verification, rollback, and any route promotion.
- [ ] Do not create Change README/INDEX/archive/move/rehydrate/restore lifecycle, shared counter, recursive consolidation Change, another lightweight backlog, or a Feature substitute.

## Project Skill Discovery Guard

- [ ] Run only after the Agent Loop controller and reliable memory root are established.
- [ ] Before a new actionable intent uses a generic helper, Operational Support method, or built-in fallback, inspect `.agent-loop/skills/INDEX.md` metadata when present.
- [ ] Match only `active` bootstrap/on-demand rows by current intent, stage, task context, Triggers, and Scope.
- [ ] Verify only the matched exact INDEX row, path, instruction-bearing/executable files, and manifest before reliance.
- [ ] Load only the matched Skill body; do not scan all Project Skill bodies when no row matches.
- [ ] Treat runtime/global Skill inventory as a separate source that cannot prove no Project Skill exists.
- [ ] Permit generic fallback only for `index-absent | no-active-match`.
- [ ] Treat missing target, invalid row/manifest, unsafe path/symlink, or conflicting owner as `project-skill-drift` and fail closed.
- [ ] Emit the existing Execution Gate summary before following the matched workflow or causing side effects.
- [ ] Keep ordinary chat response-only and do not create a discovery cache, Feature, Requirement, or log artifact.

## Project Entry

- [ ] Inspect whether `.agent-loop/` exists.
- [ ] If `.agent-loop/` is missing, inspect whether legacy `agent-loop/` exists.
- [ ] If `.agent-loop/` or legacy `agent-loop/` is present, read `project.md`.
- [ ] If `.agent-loop/skills/INDEX.md` exists, read its metadata, verify referenced active paths and SHA-256 manifests, and exclude missing/mismatched/proposed/disabled/deprecated entries from normal routing.
- [ ] For each applicable actionable intent after entry, use Project Skill Discovery Guard before a generic helper, Operational Support method, built-in fallback, command, tool call, temporary resource, or environment action.
- [ ] If legacy `agent-loop/` is present, use it for the current run and ask before migration or renaming.
- [ ] If `project.md` says `Memory Mode: enterprise`, read only the needed linked project-memory detail files.
- [ ] Locate active or paused feature.
- [ ] If an Active Feature exists, consider Feature Completion Check before starting new feature work.
- [ ] Check whether memory appears stale compared with obvious repo reality.
- [ ] If the human says re-adopt, re-sync, 重新接管, resume after outside-loop work, or says recent work bypassed `agent-loop`, route to Reconcile Project Context / Re-Adopt Agent Loop Project before new feature work.
- [ ] Check whether local directory is empty/ambiguous or appears to be a remote entry point.
- [ ] If human says remote project, SSH, devcontainer, container, tunnel, or remote workspace, route to Remote Project Discovery.
- [ ] Operational Support Guard: if the human asks to test, run, deploy, switch account/config/model/provider, check quota/rate limits, diagnose production, arrange rollout, or solve an operational problem using existing code, route to Code-Guided Operational Support.
- [ ] Classify operational support before Feature Spec, Plan Gate, or Execute.
- [ ] Default to read-only code/process analysis and checklist/runbook output.
- [ ] Confirm before code/config/deploy/destructive operations, paid-quota external calls, credential rotation, or feature/fix escalation.
- [ ] Check root `AGENTS.md` / `CLAUDE.md` and any obvious directory-level guidance.
- [ ] Treat root `AGENTS.md` as stale if it lacks Bootstrap Protocol, project-outcome Agent Ownership, Message Intent Guard, Workflow Gateway Map, Gate Modes, all six Required Stop classes with Auto Mode non-bypass, Completion Rules, Submit And Commit Rules, Artifact Authority, root/directory guidance boundaries, or exact published-reference first hops.
- [ ] If `scripts/check-root-agents-blocks.py` is available, run it with Python 3.10+ as a read-only drift check against the current root AGENTS template and target root `AGENTS.md`; use the report as Human Review Summary evidence.
- [ ] Compare each managed block `section` and `block-version` against the current root AGENTS template.
- [ ] Treat missing block-version, older block-version, or missing managed sections as stale even when other sections look current.
- [ ] Do not write bare `block-version:<agent-loop-version>` values; copy the full template block revision such as `block-version:1.5.0-20260723.2`.
- [ ] Treat date-only, malformed, or different block-version values as stale; exact full template block-version match is required.
- [ ] Do not require a separate Managed Block Rule prose section in target root `AGENTS.md`; managed block maintenance rules live in `references/project-guidance.md` and refresh tooling.
- [ ] When refreshing a managed block, copy the current template marker metadata for the same `section`; adjust only `source` if the target project uses a different active memory root or artifact source.
- [ ] Treat root `CLAUDE.md` as stale if it duplicates independent long-lived rules or does not clearly point to `AGENTS.md`.
- [ ] If root guidance will be created, refreshed, or repaired, run AGENTS Cleanup / Migration Review for conflicting workflow rules and long-term project memory outside managed blocks.
- [ ] Root guidance refresh may update only human-approved managed blocks. Preserve content outside managed blocks unless each cleanup, replacement, or migration item is listed in Human Review Summary and separately approved.
- [ ] Never treat "refresh AGENTS.md quickly" or similar wording as blanket approval to replace the whole file with `templates/root-AGENTS.md`.
- [ ] Determine guidance language from existing docs or human preference; default to English only if unclear.
- [ ] For old or large projects, record directory guidance status in `project.md`.
- [ ] Summarize state and recommend one next action.
- [ ] Ask human confirmation before proceeding.

## Project Skill Creation / Update

- [ ] Confirm reliable Project Entry/memory exists; otherwise route to Project Entry or recovery first.
- [ ] Classify entry mode: explicit request resolves helpers before Candidate/Gate 1; accepted proactive Candidate resolves helpers after the already-satisfied Gate 1 and before authoring.
- [ ] Load `project-skills.md`, `skill-routing.md`, and `external-skill-adapters.md`.
- [ ] Resolve `superpowers:writing-skills` / `writing-skills` before authoring actions.
- [ ] Independently resolve `skill-creator`; use both helpers when available.
- [ ] Inspect successful workflow evidence, repeatability, failures, rollback, secrets, environment, and external effects.
- [ ] Present Project Skill Candidate, exact `.agent-loop/skills/<skill-name>/` tree, load policy, risks, validation plan, and any bounded independent authoring-pressure subagent lanes, per-agent briefs, boundaries, stop conditions, main-agent review, and authorization lifecycle.
- [ ] Pass Gate 1 before creating `.agent-loop/skills/`, INDEX, a skill directory, or materially updating an active skill.
- [ ] Record `proposed` during authoring.
- [ ] Run and record RED scenarios without the skill.
- [ ] Write minimum GREEN content and required resources.
- [ ] Re-run scenarios with the skill, capture rationalizations, REFACTOR, and re-test.
- [ ] Validate frontmatter, trigger description, scripts/resources, secrets, symlinks, and path boundaries.
- [ ] Finalize the active INDEX row, then record and verify its exact-row SHA-256 plus current file manifest before activation.
- [ ] Mark `active` automatically only when every required check passes; otherwise keep `proposed`.
- [ ] Do not load proposed, disabled, or deprecated skills into normal routing.
- [ ] Override helper output paths to `.agent-loop/skills/<skill-name>/`; do not default to global or external helper directories.
- [ ] Before one invocation executes an active skill, present scope, actions, effects, risks, rollback, and verification through the Execution Gate.
- [ ] Accept a human message naming the skill and concrete scope as the current one invocation grant only after emitting the execution summary and confirming planned actions/effects stay entirely inside the disclosed scope.
- [ ] End the invocation after outcome report, abort/pause, context loss, manifest change, or material plan/scope change; retry only inside pre-confirmed retry bounds.
- [ ] Combine other applicable operational/risk gates into one confirmation only when every gate fact is explicit in the summary.
- [ ] Do not reuse a prior grant across invocation, task, session, environment, expanded scope, or another skill.
- [ ] Do not treat active/bootstrap, previous success, Feature Auto-Loop, or Task Auto-Run as execution authorization.
- [ ] Report helper resolution, files, lifecycle, RED/GREEN/REFACTOR evidence, project-memory/guidance impact, and one next stage.

## Remote Project Discovery

- [ ] Load `remote-project-discovery.md`.
- [ ] Check existing local `.agent-loop/remote.md` and thin `project.md`.
- [ ] Inspect local connection docs or remote hints.
- [ ] Confirm Remote Host, Remote Path, and Access Method.
- [ ] Confirm whether the agent may read remote files.
- [ ] Confirm whether the agent may write remote files.
- [ ] Confirm whether the agent may run install/build/test/dev-server commands.
- [ ] Decide where durable `agent-loop` docs live: remote, local-shadow, or undecided.
- [ ] Record command locations for install, build, unit tests, API tests, E2E tests, and dev server.
- [ ] Record browser URL, port forwards, tunnel, and auth when applicable.
- [ ] Record sync model and stale risk.
- [ ] Write local `.agent-loop/remote.md` only after confirmation.
- [ ] Write thin local `project.md` with `Status: remote-entry` only after confirmation.
- [ ] Create remote `.agent-loop/`, `AGENTS.md`, or `CLAUDE.md` only after explicit confirmation.
- [ ] If local-shadow mode is used, label every code fact and command evidence with remote location.

## Project Entry Scan For Existing Projects

- [ ] Load `project-entry-scan.md`.
- [ ] Load `project-architecture-init.md`.
- [ ] Explain that Project Entry Scan is safe-entry memory only, not newcomer documentation.
- [ ] Do not offer Quick / Deep / Targeted onboarding modes.
- [ ] Update or propose project memory, root guidance status, commands, boundaries, capabilities, and uncertainties only.
- [ ] If the human wants durable onboarding docs, newcomer handoff docs, or a focused understanding artifact, recommend Evidence-Graph + DDD Onboarding after Project Entry Scan or reliable project memory.
- [ ] Read startup docs first.
- [ ] Inspect shallow repo shape.
- [ ] Decide whether large-project triggers apply.
- [ ] If large and subagents are available, recommend bounded subagent scan.
- [ ] Ask human confirmation before using subagents.
- [ ] If subagents are unavailable or declined, continue single-agent scan.
- [ ] Detect runtime/tooling manifests.
- [ ] Classify project shape: frontend | backend | fullstack | worker | cli/library.
- [ ] Identify language adapter and framework adapter.
- [ ] Identify DDD intensity: light | standard | enterprise.
- [ ] For existing projects, map actual directories to DDD-inspired roles without proposing moves.
- [ ] Detect test/build/lint/typecheck commands from scripts or CI.
- [ ] Build capability map from routes/pages/actions/schema/tests/docs.
- [ ] Build boundary map from durable directories.
- [ ] Inventory root and directory-level guidance files.
- [ ] Check whether root `AGENTS.md` exists, is stale, or must be created.
- [ ] If root `AGENTS.md` exists, verify it contains Bootstrap Protocol, project-outcome Agent Ownership, Message Intent Guard, Workflow Gateway Map, Gate Modes, all six Required Stop classes with Auto Mode non-bypass, Completion Rules, Submit And Commit Rules, and Artifact Authority.
- [ ] If `scripts/check-root-agents-blocks.py` is available, run it with Python 3.10+ as a read-only drift check against the current root AGENTS template and target root `AGENTS.md`; use the report as Human Review Summary evidence.
- [ ] Compare each managed block `section` and `block-version` against the current root AGENTS template.
- [ ] Treat missing block-version, older block-version, or missing managed sections as stale even when other sections look current.
- [ ] Do not write bare `block-version:<agent-loop-version>` values; copy the full template block revision such as `block-version:1.5.0-20260723.2`.
- [ ] Treat date-only, malformed, or different block-version values as stale; exact full template block-version match is required.
- [ ] Do not require a separate Managed Block Rule prose section in target root `AGENTS.md`; managed block maintenance rules live in `references/project-guidance.md` and refresh tooling.
- [ ] When refreshing a managed block, copy the current template marker metadata for the same `section`; adjust only `source` if the target project uses a different active memory root or artifact source.
- [ ] Check whether root `CLAUDE.md` exists and loads or points to `AGENTS.md`; if it duplicates or diverges, propose converting it to a pointer.
- [ ] Run AGENTS Cleanup / Migration Review when existing root guidance has conflicting workflow rules, duplicated agent-loop rules, or long-term project memory that belongs in `.agent-loop/project.md` or enterprise `.agent-loop/project/*.md`.
- [ ] Root guidance refresh may update only human-approved managed blocks. Preserve content outside managed blocks unless each cleanup, replacement, or migration item is listed in Human Review Summary and separately approved.
- [ ] Never treat "refresh AGENTS.md quickly" or similar wording as blanket approval to replace the whole file with `templates/root-AGENTS.md`.
- [ ] Record guidance language and evidence in `project.md`.
- [ ] Record root guidance status in `project.md`: `AGENTS.md` present/created/stale/missing/human-deferred and `CLAUDE.md` points-to-AGENTS/created-pointer/stale/missing/human-deferred.
- [ ] Attach evidence and confidence to commands, capabilities, and boundaries.
- [ ] Do not create onboarding-db detail docs, module docs, flow docs, onboarding diagrams, onboarding-spec, or onboarding-tasks during Project Entry Scan.
- [ ] Decide whether Project Memory Mode should be `simple` or `enterprise`.
- [ ] Recommend enterprise when any hard trigger applies, including about 200k+ LOC, 5+ durable boundaries, 2+ test systems, 3+ execution environments, `project.md` above about 600 lines, repeated re-scans, or 5+ directory-level guidance files.
- [ ] List Project Entry uncertainties and follow-up scans.
- [ ] Summarize proposed `project.md` before writing.
- [ ] When Project Entry Scan discovers stable project facts missing from project memory, propose or perform project memory backfill after human confirmation.
- [ ] Use Batch Human Review before writing multiple project memory facts, root guidance, or directory guidance.
- [ ] Ask human confirmation before writing `.agent-loop/`, root guidance, or directory guidance.
- [ ] Do not mark Project Entry Scan complete until root `AGENTS.md` is present/created/human-deferred and root `CLAUDE.md` is points-to-AGENTS/created-pointer/human-deferred.

## Evidence-Graph + DDD Onboarding Knowledge Base

- [ ] Load `onboarding-knowledge-base.md`.
- [ ] Confirm Project Entry Scan is complete or reliable project memory exists.
- [ ] If memory is missing, stale, or too thin, route to Project Entry Scan or recovery before writing onboarding-db.
- [ ] Do not run Quick / Deep / Targeted onboarding modes.
- [ ] Do not generate directory-first module/flow/runtime docs from the removed legacy flow.
- [ ] Treat old onboarding-db files as legacy evidence unless an Onboarding Spec migration is accepted.
- [ ] State that Markdown is source of truth and website generation is out of scope.
- [ ] Build `08-review/evidence-graph.md` before formal onboarding docs.
- [ ] Build Core Flow Inventory from entries, state writes, async handlers, recovery paths, tests/contracts/logs/config, and verified business outcomes.
- [ ] Give every `critical` / `important` flow a stable Flow ID, business success/failure terminals, variants, owners, side effects, recovery responsibility, evidence chain, and planned/deferred decision.
- [ ] Do not treat `accepted` / `pending` / `processing` as a business terminal when callback, consumer, job, or reconciler owns the final state.
- [ ] Draft `onboarding-spec.md`: target readers, scope, module plan, flow plan, DDD mapping, jobs/async, infra/deploy, file strategy, diagram type plan, ASCII 文本图 / wireframe rules, quality gates, and batches.
- [ ] Add Flow Slice Coverage for every planned critical/important flow; map each critical Slice ID to evidence, Diagram IDs, and a narrative section.
- [ ] Ask human confirmation for the Onboarding Spec only.
- [ ] Write `onboarding-tasks.md` after Spec acceptance; Spec acceptance does not authorize formal docs.
- [ ] After writing Onboarding Tasks, ask separate human acceptance of the Full Execution Gate.
- [ ] Only after Full Execution Gate acceptance may Agent create and complete all planned onboarding-db docs in one continuous execution pass.
- [ ] batch is not a human gate; batch is an Agent organization/review unit unless the plan changes, evidence is insufficient, permissions/environment block progress, or the human explicitly asks to pause.
- [ ] Do not create empty directories, thin README files, planned/later placeholders, or files that only say TBD/待补充.
- [ ] If a topic cannot be written meaningfully, track it in `coverage-matrix.md` / `onboarding-tasks.md` instead of creating a thin file.
- [ ] Module docs default to single long files: `02-modules/<module-name>.md`.
- [ ] Flow docs default to single long files: `03-flows/<flow-name>.md`.
- [ ] Critical/important flows require Core Flow Overview / Boundary, Timeline / Sequence as the primary per-flow narrative, and ASCII State Machine / Decision views.
- [ ] Complexity-triggered diagrams cover recovery timing, data lineage, transaction/concurrency, async topology, decisions, ERD, runtime topology, or troubleshooting only when the corresponding signal exists.
- [ ] Module and other content docs select diagrams that explain real semantics; stateless glossary, static config lists, and pure indexes do not invent state diagrams.
- [ ] module docs use architecture/boundary, state, and timeline/sequence diagrams when real boundary/state/timing/data-movement semantics exist, plus core-principle explanation and diagrammed examples when internal behavior is not obvious.
- [ ] critical/important flow docs require architecture/boundary + state + timeline/sequence diagrams by default; supporting flow docs stay lightweight unless they own core state, side effects, or recovery.
- [ ] Mermaid flowchart / sequenceDiagram can be the main expression for normal flow and timing; ASCII remains preferred for state-machine / decision diagrams and complex principle/example diagrams.
- [ ] ASCII 泳道图 is optional supporting detail for ownership lanes; do not use it to replace the required Timeline / 时序图 in module/flow docs.
- [ ] Use Timeline Diagram when recovery/timing matters; avoid stacked box diagram as the main explanation.
- [ ] Plain flowcharts are only supporting detail.
- [ ] Reject outline-only onboarding: critical/important module/flow docs must include use cases, domain/data objects, information transfer, state transitions, failure modes, verification/troubleshooting, and code evidence where applicable; supporting topics include only applicable semantics and evidence.
- [ ] 全部正式文档默认使用中文；推断内容要标明“推断”、证据、置信度和待验证点。
- [ ] Use coverage matrix to track topic readiness and score, not file count.
- [ ] Run Completeness Hard Gate before quality scoring; any missing/blocked critical slice prevents `newcomer-ready` and cannot be averaged away.
- [ ] Below 4/5 score cannot be marked `newcomer-ready`.
- [ ] Do not copy human examples as required topics, topic counts, domain names, or project structure.
- [ ] Keep narrative Chinese; preserve code symbols, paths, commands, APIs, env vars, config keys, errors, and third-party names.
- [ ] Record batch review with changed files, evidence read, coverage changes, gaps, and next batch.
- [ ] Recommend exactly one next action: next onboarding batch, focused update, Project Memory Update, Code-Guided Operational Support, Requirements Discussion / Product Definition, Decision & Design If Needed, Feature Spec, Pause, or Close Onboarding Work.

## Requirement Archive

- [ ] Load `requirement-management.md`.
- [ ] Identify requirement and prototype source materials.
- [ ] Ask before copying, moving, or renaming human files.
- [ ] Explain that requirement archive dates mean archive date only.
- [ ] Use `.agent-loop/requirements/YYYY-MM-DD-<topic>/` requirement set directory for new archives.
- [ ] Group all same-topic intake materials in the requirement set: requirements, prototypes, screenshots, feedback, recordings, links, and notes.
- [ ] Create or update requirement-set `README.md`.
- [ ] Record exactly one `Effective Product Definition` pointer for new work; preserve legacy `Effective Concept Foundation` without adding both.
- [ ] Write Agent-authored `product.md` only after Product Human Review; keep Product Review separate from Requirement lifecycle.
- [ ] Run Phase Scan: recommend `Delivery Phases` when the requirement is too large for one feature, has MVP/later scope, crosses multiple boundaries, or uses staged-delivery language.
- [ ] If Delivery Phases are used, write or update the README phase table only after human confirmation.
- [ ] Old requirement set README files remain valid; do not force migration only because lifecycle fields are missing.
- [ ] Do not edit `requirement.md`, external PRDs, prototypes, or other human originals; do not edit confirmed `product.md` in place for semantic changes.
- [ ] Future / Deferred Requirement Intake: when the human says "先记一下", "后面做", "之后补", "下一轮做", "暂时不做", "以后加", "backlog", "defer this", "follow-up later", or "not in this feature", recommend a requirement set instead of project memory.
- [ ] Do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`.
- [ ] Large follow-up conflicts get a Requirement Conflict Review before appending, rebuilding, or superseding requirements.
- [ ] Normalize names only after confirmation.
- [ ] When archiving during an already-confirmed feature, record exact source paths in the existing `spec.md`; do not create a feature or `spec.md` from Requirement Archive only to hold the link.
- [ ] Do not overwrite old requirement materials.
- [ ] Recommend `requirements/INDEX.md` only if index triggers apply.

## Adaptive Product Definition

- [ ] Load `product-definition.md` inside Requirements Discussion.
- [ ] Inspect preserved sources and project evidence before choosing `brief | standard`.
- [ ] Require every Brief eligibility condition; any Standard trigger or uncertainty selects Standard.
- [ ] For Standard, scan every Product View and record `included | not-applicable` with concrete evidence/reason; do not create placeholder IDs.
- [ ] Keep Human Grill evidence-first and ask exactly one blocking question at a time with the Agent recommendation.
- [ ] Run Product Completeness Scan and present cumulative Product Definition Approval.
- [ ] Keep Product Review, Requirement lifecycle, Feature start, ADR acceptance, code execution, and Git actions as separate decisions.
- [ ] Preserve human originals byte-for-byte; use an append-only Product Definition follow-up for confirmed semantic changes.
- [ ] Use PRD helpers only as methods; translate their output into Requirement `product.md` and forbid native PRD/Feature List/prototype deployment outputs.
- [ ] Generate derived visuals only after scoped Human confirmation and record source IDs/digest/freshness; capability absence uses a non-blocking fallback.
- [ ] New Feature work does not create Feature `product.md`; load `product-brief.md` only for legacy reader compatibility.

## Brainstorm / Clarify

- [ ] Resolve and load `superpowers:brainstorming` or `brainstorming` before clarification actions; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `brainstorming` or another product-discovery helper is available, use it through `external-skill-adapters.md` while writing accepted output to the current stage artifact.
- [ ] Use Requirement/Product Grill for domain terminology, business flow, prior feature conflict, or decision-signal clarification.
- [ ] Use only when goal is unstable, scope unclear, or meaningful approaches differ.
- [ ] Check project docs, code, tests, source requirements, Product Context, and Domain Language before asking.
- [ ] Ask 1-5 high-impact questions.
- [ ] Prefer one question at a time unless a short batch is clearer.
- [ ] Questions must affect scope, UX, data, architecture, testing, or acceptance.
- [ ] Write accepted Requirements Discussion output to the Requirement `product.md` draft, keep only source, lifecycle, phase, mapping, and decision-link summaries in Requirement `README.md`, and write Feature-local clarification to `spec.md` or `notes.md`; do not create a new Feature `product.md`.

## Feature Monthly Archive

- [ ] Classify only an explicit archive/rehydrate request as `feature-archive-maintenance` and require reliable project memory.
- [ ] Check `features/archive.md`, flat/month uniqueness, active/paused memory, and incomplete `.archive-txn` before planning.
- [ ] Run scan read-only with explicit operation, selected months or Feature IDs, and `--as-of`.
- [ ] Confirm every eligible archive candidate is `closed` with concrete `Archive Readiness`, complete close/tasks/verification/review/drift/memory evidence, and `Open Follow-up: none`.
- [ ] Keep active / blocked / paused features flat and show blocked candidates without suppressing eligible candidates in the same month.
- [ ] Show exact moves, archive-index rows, reference edits, immutable requirement sources, historical evidence, unsupported references, and unchanged content.
- [ ] Stop for the expected plan SHA-256 Batch Human Gate before apply; auto modes do not authorize archive or rehydrate.
- [ ] Reject malformed/stale hashes, ambiguous references, path collisions/escapes, and any manual-move or `--force` request.
- [ ] Create the transaction journal and backups before mutation; use exact precomputed edits only.
- [ ] Run post-check after archive/rehydrate; on failure restore exact bytes and every confined journal move whose source/target state shows the rename occurred, including the pre-record crash window.
- [ ] Route incomplete restore to Recovery with the exact transaction ID and keep the journal fail-closed.
- [ ] Rehydrate before reopened execution and keep lifecycle `closed` until Feature Follow-up separately confirms flow-back.
- [ ] Confirm scope remains directory-only: no per-feature archive summary, no `historical/`, no Deep Archive, deletion, packing, or scheduled archive.

## Feature Follow-up And Flow-back

- [ ] Load `feature-follow-up.md`.
- [ ] For explicit bug-record/manage/investigate/fix intent, load `bug-management.md`; keep Bug Management internal to Feature Follow-up and do not add a canonical stage/message intent.
- [ ] Treat generic adjustment wording as assessment input only; require explicit Bug/defect evidence, changed accepted behavior, or clear Feature ownership before entering Feature Follow-up.
- [ ] Ordinary Chat/read-only error explanation does not create a Bug artifact; missing reliable memory preserves intake and routes through Project Entry first.
- [ ] Scan complete Bug Index metadata for duplicate/reopen identity before creating an explicit Bug or scanning Feature ownership; Bug identity has no time cutoff, but non-Bug Follow-up does not create or update a Bug Record.
- [ ] Inspect Active/Paused pointers and Feature metadata/summaries in the default 90-day window, then deep-read evidence-ranked candidates and run `outside-default-window` extended scan when evidence points beyond 90 days.
- [ ] Calculate Feature age from `Last Updated / Closed`, not archive month, directory mtime, or archive operation time.
- [ ] Inspect code/test/API/data/UI paths mentioned by the report.
- [ ] If an explicit Bug report/title is generic, keep the Bug `triaging` and recommend `investigate-first`; do not merge/reopen the nearest record or Feature by recency/title alone.
- [ ] Present a Candidate Match Matrix with match evidence and match strength.
- [ ] When multiple candidates have medium/high match because evidence is incomplete, recommend `investigate-first`; ask the human only when evidence is sufficient and the remaining choice is product/ownership.
- [ ] Classify the report as same-feature-bug, same-feature-adjustment, regression-from-feature, new-feature, maintenance-fix, or unclear.
- [ ] Resolve Expected Behavior evidence. Ambiguity/conflict routes to Requirements Discussion / Requirement Reconciliation / Decision & Design instead of a guessed repair.
- [ ] Validate Status/Resolution independently; stop on `closed+unresolved`, `deferred=closed`, duplicate cycles, expired-only evidence, or `in-progress` without one valid Resolution Path/Target.
- [ ] An `in-progress` Bug requires `flow-back | linked-feature | maintenance-fix` plus one Human-confirmed Fix Feature Target. Reject `investigate-first | requirement | no-fix` with `Status: in-progress`.
- [ ] Recommend exactly one `investigate-first | flow-back | linked-feature | maintenance-fix | requirement | no-fix` path and request the Resolution Path Gate.
- [ ] For "字段改一下" / "规则微调" / "小改动" wording, check whether acceptance, API/event/data shape, state flow, algorithm, or visible UX changes before choosing same-feature-adjustment vs linked new feature.
- [ ] If a closed Feature is the likely owner, recommend `flow-back`; Feature reopen remains a separate Human Gate.
- [ ] Resolve/read an archived owner through `features/archive.md` without rehydrate during discovery/Human Review; after confirmed flow-back, require verified Human-gated rehydrate before lifecycle change or execution.
- [ ] If the human declines reopen/flow-back, preserve the old feature close state and require the new linked feature or maintenance-fix to record `Related Feature`, declined reason, inherited acceptance/tests/evidence, and affected paths.
- [ ] If no Feature owns the report and this is a narrow internal fix, recommend a new `Feature Type: maintenance-fix` Feature workspace; do not perform a naked code edit.
- [ ] If the report is durable source material, ask before archiving it under `.agent-loop/requirements/`.
- [ ] Keep Bug-to-Requirement links optional `0..N`; do not rewrite source or auto-change lifecycle.
- [ ] Ask separately before Feature create/reopen, Requirement create/reconciliation, Bug close/reopen, Delivery Contract action, archive apply, or any Git action; one approval cannot be reused.
- [ ] Write Bug identity/evidence/lifecycle to Bug README + Index; write all repair spec/tasks/tests/plan/code to Feature artifacts.
- [ ] Record Follow-up Intake in `notes.md`.
- [ ] Route to exactly one next stage: Requirements Discussion/Archive/Reconciliation, Feature Spec update, Work Breakdown, Test Design, Targeted Feature Scan, Plan Gate, Diagnose Failure, Verify, or Recovery.

## Feature Spec

- [ ] If `project.md` declares a Decisions index, read decision links already named by the Effective Product Definition, legacy Product Brief when present, or active Feature Spec, then inspect other likely relevant accepted decisions by domain/boundary overlap.
- [ ] Propose missing Applicable Decision references for human confirmation; do not create a duplicate ADR because a link is missing.
- [ ] Confirm Design Readiness is `design-not-needed` or `completed`; run Decision & Design before Feature Spec when shared design is required.
- [ ] Resolve new `Effective Product Definition` or legacy `Effective Concept Foundation`; require confirmed/accepted source and block pending, ambiguous, stale, `candidate`, or `reopened` input.
- [ ] Add Product Requirement Source and Product Slice from the effective source; cite Concept/Model IDs and Product Rule anchors without a Feature Product Brief intermediary.
- [ ] Reject feature-local redefinition of accepted concept name, identity, owner, lifecycle, relationship, invariant, state, terminal meaning, or product fact.
- [ ] Feature Spec visuals may explain only the accepted Product Slice and its feature-local implementation or acceptance path; rewrite feature-local clarification into `spec.md`, and return any new product meaning to Requirements Discussion.
- [ ] Do not enter Feature Spec while required shared design is unresolved or any required design slice is unassigned.
- [ ] For each applicable requirement-driven ADR, require a current Effective Requirement Snapshot, complete Requirement Model Technical Landing Trace, and `Upstream Compatibility: current`.
- [ ] Run Stage Helper Capability Scan before fallback spec writing.
- [ ] If a spec-writing, brainstorming, or product-discovery helper is available, use it through `external-skill-adapters.md` while writing accepted output to agent-loop `spec.md`.
- [ ] Create or update feature workspace.
- [ ] Set `Feature Type: normal | maintenance-fix | follow-up`.
- [ ] If the source requirement uses `Delivery Phases`, record the specific phase or single-phase slice in `Source Requirements`.
- [ ] If the feature scope is broader than one accepted phase or one slice inside a single phase, stop and recommend phase/scope split.
- [ ] For maintenance-fix, record why it is not flow-back, why it is not a new product feature, regression/safety risk, and long-term project memory impact.
- [ ] Write problem, goal, scope, stories, acceptance criteria.
- [ ] Record added, modified, and removed behavior.
- [ ] Record `Applicable Decisions`, assigned Design Slice IDs in `Implements Decisions`, and feature-local `Design Decisions` without restating the full project decision.
- [ ] Record out of scope and open questions.
- [ ] Route the completed draft to Requirement Checklist; do not accept the spec or enable Feature Auto-Loop before that recorded gate passes.

## Requirement Checklist

- [ ] Confirm the Feature Spec references an accepted requirement set and its exact Delivery Phase or phase slice when applicable.
- [ ] Confirm Design Readiness is `design-not-needed` or `completed`.
- [ ] Confirm no major ambiguity remains.
- [ ] Confirm stories are independently testable.
- [ ] Confirm acceptance criteria are measurable.
- [ ] Confirm added, modified, and removed behavior is explicit.
- [ ] Confirm edge cases and out-of-scope boundaries are recorded.
- [ ] Record the result in `tests.md` or `notes.md` before Work Breakdown.
- [ ] If the checklist changes requirement intent or Feature Spec scope, stop for human confirmation and rerun Design Readiness when shared design changed.
- [ ] Present the checked Feature Spec with Human Review Summary and ask the human to accept or revise it.
- [ ] After acceptance, ask whether to stay in Strict Mode or enable Feature Auto-Loop.
- [ ] Before Feature Auto-Loop, list assumptions, Human-gated items, risk points, and stop conditions.

## Targeted Feature Scan

- [ ] Use only after Project Entry Scan or stale-memory recovery.
- [ ] Identify feature keywords and likely boundaries.
- [ ] Read related routes/controllers/pages/actions.
- [ ] Read related domain/core modules.
- [ ] Read related schema/model/migration files.
- [ ] Read related tests and E2E specs.
- [ ] Read related directory guidance.
- [ ] Record feature-specific findings in feature docs.
- [ ] Propose `project.md` updates only for lasting project facts.
- [ ] Ask human confirmation before writing lasting project memory.

## Work Breakdown

- [ ] Confirm the spec is accepted and a passed Requirement Checklist record exists.
- [ ] Run Stage Helper Capability Scan before fallback Work Breakdown.
- [ ] Default to vertical slices / tracer bullets.
- [ ] Each normal task forms a narrow verifiable loop through necessary layers.
- [ ] Use horizontal foundation tasks only when a product slice is not yet possible.
- [ ] For each horizontal task, explain why and which future vertical slices prove it.
- [ ] Prefer small, verifiable tasks.
- [ ] Mark each task `Agent-ready` or `Human-gated`.
- [ ] Use only linear, parallel, and barrier structure.
- [ ] Record dependencies and verification hints.
- [ ] If a task creates a long-lived boundary directory, mark whether directory-level `AGENTS.md` should be proposed.
- [ ] Load `complex-artifacts.md` when stories > 3 or the work appears cross-boundary / hard to scan.
- [ ] If stories > 3, pause for a Complex Artifact assessment.
- [ ] Do not recommend Complex Artifact Mode from story count, task count, test count, or ordinary file count alone.
- [ ] Recommend Complex Artifact Mode only when the feature spans multiple collaborating modules, services, workflows, ownership lanes, or release/operation concerns.
- [ ] Treat ordinary cross-module work as a soft signal unless the feature is no longer locally understandable or executable inside one cohesive area.
- [ ] Create only the `tasks/`, `tests/`, or `plans/` detail directories that are actually needed; do not create the full complex layout by default.
- [ ] Detect likely durable producer-consumer boundaries: API, service, event, async workflow, public data, UI state/behavior, SDK/library, or runtime.
- [ ] Recommend Delivery Contract If Needed before downstream implementation relies on assumptions.
- [ ] Do not use roadmap graph in v1.
- [ ] Present task breakdown approval with Human Review Summary table.
- [ ] Ask human to approve task granularity.

## Delivery Contract If Needed

- [ ] Load `delivery-contracts.md`.
- [ ] Confirm that work crosses a durable producer-consumer boundary.
- [ ] Confirm this is not a simple internal change with no downstream consumer.
- [ ] Identify producer and named consumers.
- [ ] Ask human confirmation before creating or updating contract files.
- [ ] Create or update `contracts.md`.
- [ ] Create `contracts/<ID>-<slug>.md` detail when schema, examples, errors, history, or multiple consumers need more space.
- [ ] Record interface shape, inputs, outputs, errors, side effects, permissions, compatibility, producer verification, and consumer notes.
- [ ] Keep temporary subagent assignments in `handoffs/`, not Delivery Contracts.
- [ ] In all modes, including Feature Auto-Loop and Task Auto-Run, ask before writing contract files.
- [ ] Ask human confirmation before status becomes `accepted`.
- [ ] Ask human confirmation and list affected consumers before a breaking contract change.

## Test Design

- [ ] Run Stage Helper Capability Scan before fallback Test Design.
- [ ] Separate requirement checklist from real test execution.
- [ ] Define functional test cases.
- [ ] Define module/core tests.
- [ ] Define API tests when applicable.
- [ ] Define Web E2E/browser cases when applicable.
- [ ] If Web E2E/browser behavior exists, load `e2e-discovery.md` before defining executable E2E cases.
- [ ] Treat API/integration verification as applicable when HTTP/API behavior, service behavior, events, background jobs, auth, persistence, or integration boundaries change.
- [ ] Treat E2E/browser/manual verification as applicable when user-visible Web behavior changes.
- [ ] If substituting for applicable API/E2E verification, record missing capability, risk, substitute proof, and human approval.
- [ ] Discover real E2E sources: scripts, configs, docs, seed/fixture files, env docs, CI, existing E2E directories.
- [ ] Record stable project-level E2E capability in `project.md` with evidence and confidence.
- [ ] Record feature-specific E2E cases in `tests.md` or linked `tests/e2e/*` details.
- [ ] Classify each E2E path as `existing-framework`, `browser`, `chrome`, `computer-use`, `manual`, or `blocked`.
- [ ] Stop or mark Human-gated when URL, app start, auth/session, seed data, external service, or browser tool cannot be safely determined.
- [ ] Define regression tests for bugs or changed behavior.
- [ ] Record test commands and manual verification needs.
- [ ] Present Test Design approval with Human Review Summary table.

## E2E Discovery if Web

- [ ] Run Stage Helper Capability Scan before fallback E2E Discovery if Web.
- [ ] Load `e2e-discovery.md`.
- [ ] Discover real scripts, configs, docs, seed/fixture files, env docs, CI, existing E2E directories, browser URLs, auth/session requirements, and safe execution constraints.
- [ ] Classify the E2E path as `existing-framework`, `browser`, `chrome`, `computer-use`, `manual`, or `blocked`.
- [ ] Record durable E2E capability in `project.md` and feature-specific cases in `tests.md` or `tests/e2e/*`.
- [ ] Run Branch Strategy Check; preserve clear existing rules or recommend the optional profile only when trigger evidence exists.

## Technical Design / Code Context

- [ ] Run Stage Helper Capability Scan before fallback Technical Design / Code Context.
- [ ] Load `implementation-planning.md`.
- [ ] Inspect exact files likely to change.
- [ ] Inspect nearby tests and fixtures.
- [ ] Identify existing functions, classes, endpoints, components, schemas, hooks, or commands.
- [ ] Identify call chain, data flow, authorization, validation, errors, side effects, and existing callers.
- [ ] Record existing signatures, parameters, return shapes, and local patterns.
- [ ] Define new/changed interfaces before implementation.
- [ ] Read relevant accepted or verified Delivery Contracts before changing producer or consumer code.
- [ ] If a durable interface is new or changed, route to Delivery Contract If Needed.
- [ ] Stop or mark `Human-gated` if signatures, parameters, return shapes, or file paths cannot be discovered or safely defined.
- [ ] Update task detail or plan with the discovered context.
- [ ] When adopted branch policy applies, resolve Current Branch Context from Target Release Context and Git evidence; stop on missing version/customer/source/target facts.

## Plan Gate / Plan If Needed

Before Execute Task / Story:

- [ ] Do not execute immediately after task creation.
- [ ] Decide whether this task/story requires construction-grade `plan.md`.

Create `plan.md` when:

- [ ] task/story touches multiple files or modules
- [ ] task/story changes behavior, tests, interfaces, data, API, async, security, deployment, or cross-module behavior
- [ ] TDD steps need explicit design
- [ ] subagent execution is planned
- [ ] human asks to review a plan first
- [ ] function signatures, parameters, data contracts, or call chains need to be fixed before coding

No-Plan Decision is allowed only when:

- [ ] task is trivial, low-risk, single-file or documentation-only
- [ ] acceptance is clear
- [ ] exact file(s) and exact verification command are known
- [ ] no plan trigger above applies
- [ ] decision is recorded in `notes.md` and the selected task row/detail
- [ ] Strict Mode asks human confirmation before execution, or Feature Auto-Loop records why the Agent-ready task can proceed

Checklist:

- [ ] Load `implementation-planning.md`.
- [ ] Resolve and load `superpowers:writing-plans` or `writing-plans` before planning actions; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `writing-plans` or another plan-writing helper is available, use it through `external-skill-adapters.md` while writing to agent-loop `plan.md` / `plans/*`.
- [ ] Plan scope is `task` or `story`.
- [ ] Technical context and real source structure are recorded.
- [ ] Files and commands are exact.
- [ ] Existing APIs and local patterns are recorded.
- [ ] New or changed interfaces include signatures, parameters, return values, errors, and side effects.
- [ ] Data/API contracts are defined when applicable.
- [ ] RED/GREEN verification is defined with actual test code when possible.
- [ ] Expected RED/GREEN command output is recorded.
- [ ] Steps are bite-sized and executable.
- [ ] Placeholder scan is clean: no TBD/TODO/fill-in/add proper/write tests/similar language.
- [ ] Type/signature consistency is checked.
- [ ] Risks or rollback notes are recorded.
- [ ] When an adopted Branch Strategy or versioned/customer delivery applies, `Branch Context Evidence` cites the complete Current Branch Context in `notes.md` and repeats only strategy status/profile, Target Release Context, Target Branch, sealed/customer-isolation results, and `Git actions authorized by this plan: none`.
- [ ] When that branch context applies, the plan does not target a sealed release, cross customer isolation, or assume an unauthorized Git action.
- [ ] For a confirmed simple `not-needed` path, record branch-specific Plan and Submit checks as `not-applicable`; do not require Target Release Context or Target Branch and do not block ordinary non-versioned work.
- [ ] Present plan approval with Human Review Summary table.
- [ ] Human approves plan before execution.
- [ ] After approval, ask whether to stay in Strict Mode or enable Task Auto-Run for this task/story.
- [ ] Do not offer Task Auto-Run without an accepted plan.
- [ ] If the human seems slowed by confirmations, explain Task Auto-Run as a safe task/story-level option.
- [ ] Before Task Auto-Run, list assumptions, risk points, verification commands, and stop conditions.

## Analyze Consistency

- [ ] Run before Execute Task / Story, including after plan approval and before subagent dispatch.
- [ ] Compare accepted `spec.md` and, when present, the legacy Feature `product.md` against `tasks.md`, `tests.md`, and the active `plan.md`; resolve the current Requirement `product.md` through Product Requirement Source.
- [ ] Confirm each planned implementation step maps to an accepted task/story and acceptance criterion.
- [ ] Confirm each changed behavior has a test or explicit substitute verification path.
- [ ] Trace every accepted Decision & Design slice assigned to this feature through `spec.md`, tasks, tests, and the active plan.
- [ ] Confirm every applicable ADR remains compatible with the current effective requirement source and every assigned Design Slice originates from a covered Requirement Model trace row.
- [ ] Stop when an assigned design slice has no implementation or verification path, even if each local story is independently testable.
- [ ] Confirm no plan step changes human original requirements, product scope, acceptance criteria, public interfaces, Delivery Contracts, or project memory without a human gate.
- [ ] Confirm file paths, commands, function signatures, parameters, return shapes, data contracts, and side effects match code reality.
- [ ] Record findings in `notes.md` under `Analyze Consistency`.
- [ ] If gaps exist, stop and recommend exactly one next action: update spec, update tasks/tests, revise plan, ask clarification, or investigate first.

## Subagent Execution If Approved

- [ ] Confirm the human explicitly approved this subagent dispatch.
- [ ] Do not treat Feature Auto-Loop or Task Auto-Run approval as subagent approval.
- [ ] If using one approval for a bounded task group, list included task/story IDs or scan lanes, allowed boundaries, one brief per subagent, stop conditions, and main-agent review responsibility before asking.
- [ ] Load `skill-routing.md`.
- [ ] Load `external-skill-adapters.md`.
- [ ] After explicit bounded dispatch approval, resolve and load `superpowers:subagent-driven-development` or `subagent-driven-development` before dispatch; record Stage Helper Resolution.
- [ ] Record approval date, exact IDs/lanes, allowed boundaries, and stop conditions; require new confirmation for expanded scope.
- [ ] Confirm authorization status is `active` immediately before dispatch; reject consumed/revoked/expired records and mark the record `consumed` after the approved dispatch group returns or stops.
- [ ] If Superpowers `subagent-driven-development` or another subagent helper is available, use it through `external-skill-adapters.md` after human approval while keeping briefs and returned summaries under agent-loop `handoffs/*`.
- [ ] Verify tasks or scan lanes are independent, bounded, and reviewable.
- [ ] Create one `templates/subagent-brief.md`-style brief per subagent.
- [ ] Store briefs and returned summaries under `handoffs/*`.
- [ ] Require returned changed files, commands, evidence, drift, open questions, and next step.
- [ ] Main agent reviews returned work before updating `tasks.md`, `tests.md`, `notes.md`, or proposed `project.md`.
- [ ] Prevent subagents from closing features, submitting code, updating project memory directly, accepting Delivery Contracts, approving breaking changes, or marking tasks `done`.
- [ ] If independence or review responsibility is unclear, do not dispatch; continue single-agent execution or mark `Human-gated`.

## Execute Task / Story

- [ ] Confirm execution scope: task by default, story only by explicit choice.
- [ ] Confirm Plan Gate passed: accepted `plan.md` / `plans/*`, or recorded No-Plan Decision for a trivial task.
- [ ] If Task Auto-Run is enabled, confirm an accepted plan exists; No-Plan Decision is insufficient.
- [ ] If Feature Auto-Loop is enabled, execute only Agent-ready tasks.
- [ ] If Task Auto-Run is enabled, execute only the selected task/story and stop after evidence/review/drift updates and Task Done Gate status update.
- [ ] Stop at Human-gated tasks or any stop condition.
- [ ] Resolve and load `superpowers:test-driven-development` or `test-driven-development` before every Execute Task / Story invocation; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] Use TDD for behavior-changing execution; for non-behavior work record TDD as `not-applicable` with a reason after helper resolution.
- [ ] If Superpowers `test-driven-development` or another TDD helper is available, use it through `external-skill-adapters.md` while keeping evidence and task status under agent-loop.
- [ ] Verify RED before implementation.
- [ ] Write minimal GREEN implementation.
- [ ] Verify GREEN with fresh command output.
- [ ] Refactor only while green.
- [ ] Record TDD cycle and evidence in `notes.md`.
- [ ] Move task to `review` after implementation and fresh verification.
- [ ] Keep task `in-progress` or `blocked` if applicable verification is missing and no human-approved substitute verification exists.
- [ ] Do not mark task `done` until Task Done Gate passes.

## Diagnose Failure

- [ ] Resolve and load `superpowers:systematic-debugging` or `systematic-debugging` before proposing a fix; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `systematic-debugging` or another debugging helper is available, use it through `external-skill-adapters.md` while recording root cause and fix evidence in agent-loop `notes.md`.
- [ ] Reproduce consistently or gather more evidence.
- [ ] Read error output fully.
- [ ] Check recent changes.
- [ ] Form a specific hypothesis.
- [ ] Test one variable at a time.
- [ ] Write a failing regression test when possible.
- [ ] Fix root cause, not symptom.
- [ ] Record diagnosis in `notes.md`.

## Verify

- [ ] Resolve and load `superpowers:verification-before-completion` or `verification-before-completion` before any completion claim; record Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `verification-before-completion` or another verification helper is available, use it through `external-skill-adapters.md` while recording evidence in agent-loop `notes.md`.
- [ ] Identify what command or action proves the claim.
- [ ] Run it fresh.
- [ ] Read full output and exit status.
- [ ] Record evidence in `notes.md`.
- [ ] When Bugs are related, execute the Bug Verification Matrix against original reproduction/substitute and regression/safety paths; update the Bug README and Index row.
- [ ] Feature evidence may move `in-progress -> verifying`; do not set `closed` without the Bug Close Gate.
- [ ] Failed Bug-specific verification returns to `in-progress` or `triaging` with append-only evidence.
- [ ] Do not claim completion without evidence.

## Review

- [ ] Resolve and load `superpowers:requesting-code-review` or `requesting-code-review` before each task, submit, or feature-close review scope; record a fresh Stage Helper Resolution, or record `unavailable` / `load-failed` before fallback.
- [ ] If Superpowers `requesting-code-review` or another review helper is available, use it through `external-skill-adapters.md` while recording findings in agent-loop `notes.md`.
- [ ] Perform lightweight Spec Review for every task before marking it `done`.
- [ ] Perform Spec Review before Submit / Integrate.
- [ ] Compare implementation against `product.md` when present, `spec.md`, acceptance criteria, scope, and out-of-scope.
- [ ] Review implementation against accepted Decision & Design records and the design slices assigned to this feature.
- [ ] Perform Standards Review for large projects, broad diffs, directory or durable boundary changes, security/data changes, architecture changes, or human request.
- [ ] Compare implementation against root/directory `AGENTS.md`, `project.md`, testing rules, directory boundaries, and local conventions.
- [ ] Record findings, accepted fixes, and rejected fixes in `notes.md`.
- [ ] Compare producer code and tests against relevant Delivery Contracts.
- [ ] Keep task status as `review` if required review is missing.
- [ ] Ask human confirmation before applying review-driven changes that alter behavior, scope, architecture, data, or public interfaces.

## Task Done Gate

- [ ] Implementation scope complete.
- [ ] Required tests or substitute verification ran fresh.
- [ ] Evidence recorded in `notes.md`.
- [ ] Lightweight Spec Review recorded.
- [ ] Standards Review recorded when triggered.
- [ ] Drift decision recorded, including `no drift` when applicable.
- [ ] `tasks.md` or task detail names the evidence location.
- [ ] Only now mark task `done`; otherwise keep `review`, `in-progress`, or `blocked`.

## Drift Check

- [ ] Compare implementation against `spec.md`.
- [ ] During Drift Check, compare assigned Design Slice IDs with implementation and verification evidence.
- [ ] Compare each applicable ADR Effective Requirement Snapshot and Requirement Model Technical Landing Trace with the current effective source; route `review-required` to Decision & Design before close.
- [ ] Route any divergence from an accepted Decision & Design record back to Decision & Design before close; do not accept local-story success as a substitute.
- [ ] If accepted decision meaning or technical conclusions no longer hold, propose a superseding ADR after Human Review; never rewrite accepted meaning in place.
- [ ] Compare completed work against `tasks.md` and `tests.md`.
- [ ] Compare producer-consumer interfaces against `contracts.md` and linked `contracts/*` details when present.
- [ ] List affected consumers and ask human confirmation before accepting a breaking contract change.
- [ ] If behavior changed, update feature docs.
- [ ] If long-term project facts changed, load `project-memory-mode.md` and route updates to `project.md` or enterprise `project/*.md`.
- [ ] Do not rewrite original human requirements.
- [ ] If the feature references a Delivery Phase, propose phase status / Feature Mapping updates for human confirmation.
- [ ] Compare related Bug Expected Behavior, Resolution Path, Fix Feature, Status/Resolution, and close evidence; route semantic conflicts to Requirements Discussion / Reconciliation / Decision & Design.
- [ ] Record drift decisions in `notes.md`.
- [ ] Do not route directly to Close from Drift Check.
- [ ] Next stage is Project Memory Update / Requirement Reconciliation when long-term project facts, requirement lifecycle, Delivery Phase status, or Feature Mapping changed; otherwise Feature Completion Check.
- [ ] Present drift decisions with Human Review Summary table.
- [ ] When an adopted Branch Strategy or versioned/customer delivery applies, compare accepted Branch Strategy and Target Release Context with Current Branch Context and Git reality; stop on sealed target, isolation violation, or unapproved cleanup/action. For a confirmed simple `not-needed` path, record this branch-specific drift check as `not-applicable`.

## Project Memory Update

- [ ] Load `project-memory-mode.md`.
- [ ] Confirm current Project Memory Mode: simple | enterprise.
- [ ] If hard or soft enterprise triggers apply, recommend a mode switch before adding lots of detail to `project.md`.
- [ ] Confirm the change affects future work, not only current task history.
- [ ] Do not write future TODO, backlog, deferred requirements, or unimplemented planned capability details into `project.md`.
- [ ] Do not write Bug backlog, triage/evidence, Status/Resolution rows, or assignment-like data into project memory; use `bugs/INDEX.md` and Bug README files.
- [ ] Update Current Work and Next Suggested Action.
- [ ] In simple mode, update the matching `project.md` section.
- [ ] In enterprise mode, keep `project.md` as index/current state and update the matching `project/*.md` detail file.
- [ ] Update Capabilities if a durable capability changed.
- [ ] Update Directory Map, Boundaries, or Directory Guidance if boundaries changed.
- [ ] Update Architecture Profile if project shape, language/framework adapter, DDD intensity, or durable dependency direction changed.
- [ ] Update Test Commands or Testing if commands or test systems changed.
- [ ] Update Domain Language, Product Context, Known Constraints, or Long-Term Decisions if future agents need them.
- [ ] Resolve or add Project Entry Uncertainties when confidence changes.
- [ ] Run Requirement Reconciliation when the feature references or creates requirement sets.
- [ ] A Bug link alone does not change Requirement lifecycle; reconcile only when current evidence invalidates delivery truth and the human confirms the transition.
- [ ] Apply Delivery Phase Status Roll-up; do not mark a multi-phase requirement `implemented` from one completed feature while unimplemented phases remain.
- [ ] Do not edit `requirement.md` or other source files for lifecycle/status updates.
- [ ] Update requirement set README / optional requirements INDEX for lifecycle status, Delivery Phase status, and Feature Mapping only after human confirmation.
- [ ] Ask before changing root or directory-level `AGENTS.md`.
- [ ] Present proposed memory updates with Human Review Summary table.
- [ ] Record durable Branch Strategy / Target Release Context only after human confirmation; do not copy mutable feature branch lifecycle into long-term policy.

## Submit / Integrate

- [ ] Load `submit-and-integrate.md`.
- [ ] Run Stage Helper Capability Scan before fallback submit/integrate preparation.
- [ ] If Superpowers `finishing-a-development-branch` or another finishing/branch helper is available, use it through `external-skill-adapters.md`.
- [ ] Use external finishing skills only for completion options and branch hygiene.
- [ ] Inspect diff and untracked files.
- [ ] Separate product code from `agent-loop` artifact changes.
- [ ] Identify unrelated dirty work.
- [ ] Review feature artifacts (`product.md` when present, `spec.md`, `tasks.md`, `tests.md`, `plan.md`, `notes.md`) against the submitted code.
- [ ] Review linked requirement records for lifecycle, Delivery Phase status, Feature Mapping, and approved deferrals when the feature references requirement sets.
- [ ] Confirm project memory and root/directory guidance impact is completed, explicitly not needed, or human-approved to defer.
- [ ] Confirm fresh verification evidence exists.
- [ ] Confirm drift check result and known drift.
- [ ] Confirm required review has passed or record why submit must stop.
- [ ] When the Feature resolves Bugs, show Bug IDs, current Status, Bug-specific evidence, unresolved Bug Close Decisions, Target Release Context, and isolation.
- [ ] Do not reuse submit/commit/push approval as Bug close, or Bug close as submit authorization.
- [ ] After code integration yields a stable verified Merged Code SHA, run the Post-Merge Memory Reconciliation check by looking for an observed semantic memory conflict rather than mere file differences.
- [ ] With no conflict, use `reconciliation-not-needed`; do not scan all memory, create a report, add a Human Gate, or block the next independent action.
- [ ] With a conflict, inspect only its owner, direct references/indexes, and minimum evidence; preserve accepted product/ADR meaning and protected history.
- [ ] Let the Agent rewrite and target-verify fact-determined current meaning; ask the human only when multiple meanings remain legitimate.
- [ ] Treat an unresolved observed conflict or failed targeted restore as blocking; a speculative conflict or missing full audit is not blocking.
- [ ] Use four-snapshot accounting, exact Plan Hash, and transactional Apply/Restore only after explicit Full Memory Audit / Recovery authorization.
- [ ] Treat resolution only as permission to offer the next independent Memory Commit / Push / Release / Cleanup Human Gate; never inherit code-merge or submit authorization.
- [ ] When an adopted Branch Strategy or versioned/customer delivery applies, verify Source Branch, Branch Class, Target Release Context, Target Branch, sealed state, customer isolation, and requested action.
- [ ] Require merge evidence and a separate cleanup decision before deleting a temporary development branch; never treat a retained release aggregation branch as temporary cleanup.
- [ ] Treat each create/switch/merge/delete/push/tag/release/publish action as separately Human-gated even when the strategy and plan are accepted; create/switch uses the Branch Action Gate.
- [ ] Present submit/integrate decision with Human Review Summary table.
- [ ] Ask human which action to take: prepare only, commit, PR text, merge note, release note, publish/release note, or skip.
- [ ] Only commit, publish, release, merge, or create final PR text after explicit human confirmation.
- [ ] Record submit/integrate result in `notes.md`.
- [ ] Apply the ordered exit decision: prepare-only not performed -> Pause; explicitly skipped -> Feature Completion Check if done or next task/story; performed and done -> Feature Completion Check; performed with work remaining -> next task/story; failed/blocked -> one unblock stage.

## Feature Completion Check

- [ ] Load `feature-completion-check.md`.
- [ ] Run Stage Helper Capability Scan before fallback completion analysis.
- [ ] If verification, review, finishing, or close-decision helpers are available, use them through `external-skill-adapters.md` while keeping close under agent-loop control.
- [ ] Run after likely completion, before starting a new feature with an Active Feature, or on resume with an Active Feature.
- [ ] Confirm accepted spec exists.
- [ ] Confirm all remaining in-scope tasks are `done`; skipped/deferred work must already be removed through human-approved scope reconciliation.
- [ ] Confirm required tests or substitute verification are recorded.
- [ ] Confirm fresh verification evidence exists.
- [ ] Confirm Feature Close Review completed.
- [ ] Feature close is blocked until all assigned design slices have implementation and verification evidence, or a human-approved decision reassigns, defers, removes, or supersedes the slice.
- [ ] Confirm feature-level Spec Review covers `product.md` when present, `spec.md`, `tasks.md`, `tests.md`, acceptance criteria, and out-of-scope boundaries.
- [ ] Confirm feature-level Standards Review completed when large project, broad diff, directory or durable boundary change, security/data change, architecture change, or human request applies.
- [ ] Confirm Drift Check completed.
- [ ] Confirm Delivery Contracts are implemented and verified when downstream consumers rely on them.
- [ ] Confirm accepted Delivery Contracts match producer code/tests and have no unapproved breaking changes.
- [ ] Confirm long-term facts are reflected in `project.md`.
- [ ] Confirm submit/integration status is recorded if requested.
- [ ] Confirm every related Bug expected to be fixed is `verifying` with fresh evidence; passing Feature tests do not auto-close it.
- [ ] Present `Bug Close Decision: confirm | revise | keep-verifying` separately from `Feature Close Decision: confirm | continue | pause | revise-scope`.
- [ ] Record the check in `notes.md`.
- [ ] If blockers prevent completion, record Result: blocked and recommend exactly one unblock stage.
- [ ] Recommend Close, Continue, Pause before new feature, or Scope Update.
- [ ] Present completion status with Human Review Summary table.
- [ ] Ask explicit human confirmation before close.

## Pause / Close

- [ ] Run Stage Helper Capability Scan before fallback pause/close preparation.
- [ ] If verification, finishing, or handoff helpers are available, use them through `external-skill-adapters.md` only for evidence discipline, close options, or handoff structure.

Pause:

- [ ] Record current state.
- [ ] Record next suggested action.
- [ ] Record blockers and files touched.
- [ ] Move the feature from `Active Feature` to `Paused Features`, record its resume point, and set `Active Feature: none`.
- [ ] Set feature lifecycle status to `paused`.
- [ ] Clear feature-scoped Feature Auto-Loop or Task Auto-Run authorization.

Close:

- [ ] Fresh verification evidence exists.
- [ ] Drift check completed.
- [ ] Feature Close Review completed.
- [ ] Submit/integration status recorded if requested.
- [ ] `project.md` updated for long-term changes.
- [ ] Requirement Reconciliation completed when the feature references or creates requirement sets.
- [ ] `notes.md` has close record.
- [ ] Human explicitly confirms close.
- [ ] After confirmation, set feature lifecycle status to `closed`, remove it from Active/Paused pointers, set `Active Feature: none`, and clear feature-scoped auto-mode authorization.
