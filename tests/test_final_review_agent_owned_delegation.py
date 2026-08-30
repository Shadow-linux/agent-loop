from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def h2_section(content: str, heading: str) -> str:
    marker = f"## {heading}"
    lines = content.splitlines()
    try:
        start = lines.index(marker)
    except ValueError as exc:
        raise AssertionError(f"missing owning section: {marker}") from exc
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def bounded(content: str, start: str, end: str) -> str:
    try:
        start_at = content.index(start)
        end_at = content.index(end, start_at + len(start))
    except ValueError as exc:
        raise AssertionError(f"missing bounded owner: {start!r} -> {end!r}") from exc
    return content[start_at:end_at]


def active_stage_order(runtime: str) -> str:
    return bounded(runtime, "## Stage Order", "## Stage Entry And Exit")


def assert_ordered(testcase: unittest.TestCase, content: str, tokens: tuple[str, ...]) -> None:
    positions = tuple(content.find(token) for token in tokens)
    testcase.assertNotIn(-1, positions, f"missing ordered token in {tokens!r}")
    testcase.assertEqual(positions, tuple(sorted(positions)))


def assert_task_review_contract(testcase: unittest.TestCase, content: str) -> None:
    section = h2_section(content, "Task Done Gate")
    for required in (
        "Task Completion Review",
        "accepted authority",
        "accepted Task/Story and Feature implementation boundary",
        "Required Verification",
        "Existing Test Obligation",
        "diff",
        "rollback",
        "drift",
        "done",
    ):
        testcase.assertIn(required, section)
    testcase.assertIn("does not require a review helper by default", section)
    testcase.assertNotIn("Task Review helper", section)


def assert_final_review_contract(testcase: unittest.TestCase, content: str) -> None:
    for required in (
        "all in-scope Tasks are `done` or Human-approved `skipped`",
        "Feature-wide Required Verification",
        "current rollback evidence",
        "missing/stale rollback evidence",
        "read-only Final Review Subagent",
        "Final Reviewer: controller-fallback",
        "Controller fallback remains forbidden while any mechanism is exposed",
        "failed runtime dispatch enters Diagnose Failure",
        "reports findings",
        "owning Agent",
        "must not edit",
        "materially changes",
        "fresh Final Review Subagent",
        "otherwise return to the owning Task, Verify, Diagnose Failure, or Human Gate",
    ):
        testcase.assertIn(required, content)


def assert_delegated_authority_contract(
    testcase: unittest.TestCase, content: str
) -> None:
    for required in (
        "Subagent dispatch is not a Human Gate",
        "inherits only",
        "existing authorization",
        "cannot create or widen authorization",
        "read-only",
        "allowed writes",
        "forbidden actions",
    ):
        testcase.assertIn(required, content)
    for preserved in (
        "branch",
        "worktree",
        "commit",
        "push",
        "release",
        "external",
    ):
        testcase.assertIn(preserved, content)
    testcase.assertIn(
        "branch, worktree, commit, push, release, publish, production, destructive, credential, paid, or external actions keep their existing Human Gates",
        content,
    )


def assert_human_close_contract(testcase: unittest.TestCase, content: str) -> None:
    for required in (
        "current Final Review",
        "every finding disposition",
        "Human Close Gate",
        "does not perform another review",
    ):
        testcase.assertIn(required, content)
    testcase.assertNotIn("Feature Close Review", h2_section(content, "Completion Questions"))


def assert_git_fast_path_contract(testcase: unittest.TestCase, content: str) -> None:
    section = h2_section(content, "Full-Worktree Git Fast Path")
    for required in (
        "packages Git state",
        "does not make a completion claim",
        "do not automatically run tests",
        "Task Completion Review",
        "Final Review",
        "one lightweight Commit Confirmation",
        "Ask no second confirmation",
    ):
        testcase.assertIn(required, section)


def assert_overlap_contract(testcase: unittest.TestCase, content: str) -> None:
    for required in (
        "mechanically non-overlapping write sets",
        "known same writable path",
        "must be serialized",
        "already-authorized isolated worktrees",
        "unexpected overlap",
        "Unexpected overlap",
        "stops integration and returns to the owning stage or Human Gate",
    ):
        testcase.assertIn(required, content)


def assert_task_review_currentness_contract(
    testcase: unittest.TestCase, content: str
) -> None:
    for required in (
        "every `done` Task",
        "current Task Completion Review",
        "evidence pointer",
        "stale",
        "refresh",
    ):
        testcase.assertIn(required, content)


def assert_finding_disposition_contract(
    testcase: unittest.TestCase, content: str
) -> None:
    for required in (
        "blocking defect",
        "verification gap",
        "cannot be accepted as residual",
        "semantic/boundary conflict",
        "routed-to-owner",
        "non-blocking improvement",
        "accepted-residual",
        "rejected-as-unsupported",
    ):
        testcase.assertIn(required, content)


def assert_review_repair_exit_contract(
    testcase: unittest.TestCase, content: str
) -> None:
    for required in (
        "Exit to Drift Check only after the current Final Review result exists",
        "every finding has an owning-Agent disposition",
        "otherwise return to the owning Task, Verify, Diagnose Failure, or Human Gate",
    ):
        testcase.assertIn(required, content)


class FinalReviewAndAgentOwnedDelegationTests(unittest.TestCase):
    def test_task_and_final_review_preserve_decision_design_conformance(self) -> None:
        checklist = read("references/workflow-checklists.md")
        task_section = h2_section(checklist, "Task Done Gate")
        final_section = task_section.split("### Final Review after all Tasks", 1)[1]
        self.assertIn(
            "Review implementation against accepted Decision & Design records and the design slices assigned to this feature.",
            task_section,
        )
        for required in (
            "current Product/Requirement authority",
            "accepted Decision & Design records",
            "assigned design slices",
            "applicable Delivery Contracts",
        ):
            self.assertIn(required, final_section)

    def test_canonical_flow_removes_standalone_review_and_dispatch_stage(self) -> None:
        runtime = read("references/runtime.md")
        order = active_stage_order(runtime)
        self.assertNotIn("\nSubagent Execution If Approved\n", order)
        self.assertNotIn("\nReview\n", order)
        self.assertNotIn("Feature Close Review", order)
        assert_ordered(
            self,
            order,
            (
                "Execute Task / Story",
                "Verify",
                "[internal] Task Completion Review inside Task Done Gate",
                "[internal] Feature-wide Required Verification and automatic Final Review Subagent",
                "Drift Check",
                "Project Memory Update",
                "Feature Completion Check",
                "Submit / Integrate",
                "Pause / Close",
            ),
        )
        mutation = runtime.replace(
            "[internal] Feature-wide Required Verification and automatic Final Review Subagent",
            "[internal] Feature-wide Required Verification without automatic review",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_ordered(
                self,
                active_stage_order(mutation),
                (
                    "Execute Task / Story",
                    "Verify",
                    "[internal] Task Completion Review inside Task Done Gate",
                    "[internal] Feature-wide Required Verification and automatic Final Review Subagent",
                    "Drift Check",
                ),
            )

    def test_task_completion_review_is_inline_and_blocks_done_when_incomplete(self) -> None:
        runtime = read("references/runtime.md")
        checklist = read("references/workflow-checklists.md")
        assert_task_review_contract(self, runtime)
        assert_task_review_contract(self, checklist)
        for missing in (
            "accepted authority",
            "Required Verification",
            "rollback",
            "drift",
        ):
            mutated = h2_section(runtime, "Task Done Gate").replace(missing, "removed")
            with self.subTest(missing=missing), self.assertRaises(AssertionError):
                assert_task_review_contract(
                    self, runtime.replace(h2_section(runtime, "Task Done Gate"), mutated, 1)
                )

    def test_final_review_is_one_read_only_feature_wide_review(self) -> None:
        stage_guides = read("references/stage-guides.md")
        assert_final_review_contract(self, stage_guides)
        self.assertIn("exactly one", stage_guides)
        self.assertIn("every finding disposition", stage_guides)
        mutation = stage_guides.replace("must not edit", "may edit", 1)
        with self.assertRaises(AssertionError):
            assert_final_review_contract(self, mutation)

    def test_review_repair_exit_routes_to_evidence_owner(self) -> None:
        stage_guides = read("references/stage-guides.md")
        assert_review_repair_exit_contract(self, stage_guides)
        mutation = stage_guides.replace(
            "otherwise return to the owning Task, Verify, Diagnose Failure, or Human Gate",
            "otherwise continue automatically",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_review_repair_exit_contract(self, mutation)

    def test_final_review_entry_blocks_stale_or_ambiguous_inputs(self) -> None:
        stage_guides = read("references/stage-guides.md")
        for blocker in (
            "incomplete Task",
            "stale verification",
            "unresolved authority",
            "ambiguous dirty work",
            "missing/stale rollback evidence",
        ):
            self.assertIn(blocker, stage_guides)
        mutation = stage_guides.replace(
            "missing/stale rollback evidence", "rollback evidence is optional", 1
        )
        with self.assertRaises(AssertionError):
            assert_final_review_contract(self, mutation)

    def test_final_review_and_completion_require_current_task_review_pointers(self) -> None:
        stage_guides = read("references/stage-guides.md")
        completion = read("references/feature-completion-check.md")
        runtime = read("references/runtime.md")
        combined = "\n".join((stage_guides, completion, runtime))
        assert_task_review_currentness_contract(self, combined)
        completion_gate = h2_section(runtime, "Completion Gate")
        self.assertIn("every `done` Task", completion_gate)
        self.assertIn("current Task Completion Review evidence pointer", completion_gate)
        self.assertIn("returns that Task to `review`", completion_gate)
        self.assertIn(
            "ordinary bounded repair does not reopen the Task or repeat its formal Task Completion Review",
            combined,
        )
        self.assertIn(
            "refreshes the affected Task Completion Review evidence pointer and currentness assessment",
            combined,
        )
        mutation = stage_guides.replace(
            "refreshes the affected Task Completion Review evidence pointer and currentness assessment",
            "leaves the old Task review pointer unchanged",
            1,
        )
        with self.assertRaises(AssertionError):
            self.assertIn(
                "refreshes the affected Task Completion Review evidence pointer and currentness assessment",
                mutation,
            )

    def test_task_auto_run_last_task_has_one_deterministic_terminal_route(self) -> None:
        runtime = read("references/runtime.md")
        stage_guides = read("references/stage-guides.md")
        checklist = read("references/workflow-checklists.md")
        combined = "\n".join((runtime, stage_guides, checklist))
        for required in (
            "must not start another implementation Task",
            "selected Task is the last in-scope Task",
            "all Final Review prerequisites are current",
            "automatically dispatch the read-only Final Review Subagent",
            "exactly one next action: Feature-wide Verify",
            "does not ask for permission to dispatch Final Review",
        ):
            self.assertIn(required, combined)

    def test_task_auto_run_routes_non_verification_prerequisites_to_their_owner(self) -> None:
        runtime = bounded(
            read("references/runtime.md"),
            "Task Auto-Run means:",
            "## Task Done Gate",
        )
        stage_guides = h2_section(read("references/stage-guides.md"), "Execute Task / Story")
        combined = runtime + "\n" + stage_guides
        for required in (
            "only Feature-wide Required Verification is missing/stale",
            "every other Final Review prerequisite is current",
            "Task review pointer -> owning Task",
            "authority -> authority recovery or its Human Gate",
            "dirty work -> workspace owner",
            "rollback -> rollback owner",
            "must not route every prerequisite failure to Verify",
        ):
            self.assertIn(required, combined)
        self.assertNotIn(
            "when Feature-wide Required Verification or another Final Review prerequisite is missing/stale, stop with exactly one next action: Feature-wide Verify",
            runtime,
        )

    def test_helper_fallback_is_distinct_from_runtime_dispatch_fallback(self) -> None:
        adapter = read("references/external-skill-adapters.md")
        stage_guides = read("references/stage-guides.md")
        combined = adapter + "\n" + stage_guides
        for required in (
            "helper is unavailable or load-failed",
            "does not mean the runtime dispatcher is unavailable",
            "dispatch through the runtime mechanism",
            "`controller-fallback` is allowed only when the active runtime genuinely has no Subagent dispatch mechanism",
        ):
            self.assertIn(required, combined)
        self.assertNotIn(
            "When Subagent coordination capability is unavailable, record the helper fallback. For mandatory final review, use `Final Reviewer: controller-fallback`",
            adapter,
        )

    def test_repair_freshness_requires_rereview_only_for_material_change(self) -> None:
        stage_guides = read("references/stage-guides.md")
        for required in (
            "post-repair assessment",
            "original review coverage remains current",
            "does not automatically dispatch another reviewer",
            "boundary",
            "risk",
            "coverage",
            "fresh Final Review Subagent",
        ):
            self.assertIn(required, stage_guides)
        mutation = stage_guides.replace(
            "fresh Final Review Subagent", "reuse stale Final Review", 1
        )
        with self.assertRaises(AssertionError):
            assert_final_review_contract(self, mutation)

    def test_finding_types_have_fail_closed_dispositions(self) -> None:
        stage_guides = read("references/stage-guides.md")
        completion = read("references/feature-completion-check.md")
        assert_finding_disposition_contract(self, stage_guides + "\n" + completion)
        self.assertIn("owner, rationale, and evidence", completion)
        self.assertIn("Human decision", completion)

    def test_subagent_dispatch_is_agent_owned_but_actions_keep_their_gates(self) -> None:
        adapter = read("references/external-skill-adapters.md")
        assert_delegated_authority_contract(self, adapter)
        self.assertNotIn("require explicit human confirmation before dispatch", adapter)
        mutation = adapter.replace(
            "cannot create or widen authorization", "may widen authorization", 1
        )
        with self.assertRaises(AssertionError):
            assert_delegated_authority_contract(self, mutation)
        gate_mutation = adapter.replace(
            "keep their existing Human Gates", "are authorized by dispatch", 1
        )
        with self.assertRaises(AssertionError):
            assert_delegated_authority_contract(self, gate_mutation)

    def test_read_only_reviewer_cannot_write_or_claim_completion(self) -> None:
        stage_guides = read("references/stage-guides.md")
        for forbidden_action in (
            "edit files",
            "mark Tasks or the Feature done",
            "accept a Human Gate",
            "perform Git",
            "perform external actions",
        ):
            self.assertIn(forbidden_action, stage_guides)

    def test_feature_completion_consumes_current_review_without_close_review(self) -> None:
        completion = read("references/feature-completion-check.md")
        assert_human_close_contract(self, completion)
        active = h2_section(completion, "Feature Completion Check")
        self.assertNotIn("Feature Close Review", active)
        mutation = completion.replace("Human Close Gate", "automatic close", 1)
        with self.assertRaises(AssertionError):
            assert_human_close_contract(self, mutation)

    def test_submit_reuses_only_unchanged_current_review_evidence(self) -> None:
        submit = read("references/submit-and-integrate.md")
        for required in (
            "current Final Review",
            "reviewed inputs remain unchanged",
            "authority",
            "diff",
            "verification",
            "risk",
            "consumer boundary",
            "review coverage",
            "finding dispositions",
            "residual risk",
            "merge resolution",
            "generated output",
            "packaging",
            "late edit",
            "expire",
        ):
            self.assertIn(required, submit)
        self.assertIn("Full-Worktree Git Fast Path", submit)
        self.assertIn("does not make a completion claim", submit)
        assert_git_fast_path_contract(self, submit)
        mutation = submit.replace(
            "does not make a completion claim", "makes a completion claim", 1
        )
        with self.assertRaises(AssertionError):
            assert_git_fast_path_contract(self, mutation)

    def test_notes_and_optional_brief_record_new_evidence_without_new_artifact_family(self) -> None:
        notes = read("templates/notes.md")
        brief = read("templates/subagent-brief.md")
        for required in (
            "## Task Completion Reviews",
            "## Final Review",
            "Final Reviewer:",
            "Reviewed Inputs:",
            "Finding Dispositions:",
            "Post-Repair Freshness:",
            "Final Review: complete",
        ):
            self.assertIn(required, notes)
        self.assertNotIn("## Feature Close Review", notes)
        for required in (
            "## Delegated Authority",
            "Owning Stage:",
            "Existing Authorization:",
            "Allowed Writes:",
            "Forbidden Actions:",
            "Read-Only Reviewer:",
            "Rollback Evidence:",
            "Expiry:",
        ):
            self.assertIn(required, brief)
        self.assertNotIn("## Dispatch Authorization", brief)

    def test_archive_prefers_final_review_and_reads_legacy_close_review(self) -> None:
        support = read("scripts/feature_archive_support.py")
        fixture = read("tests/feature_archive_test_support.py")
        self.assertIn('"Final Review"', support)
        self.assertIn('"Feature Close Review"', support)
        self.assertIn("legacy", support.lower())
        self.assertIn("Final Review: complete", fixture)
        self.assertIn("legacy_close_review", fixture)
        example = read("examples/login-feature/notes.md")
        self.assertIn("Final Review Findings: none", example)
        self.assertIn("Finding Dispositions: none", example)

    def test_active_surfaces_do_not_restore_subagent_dispatch_approval(self) -> None:
        active = "\n".join(
            read(path)
            for path in (
                "Usage.md",
                "references/runtime.md",
                "references/design.md",
                "references/workflow-checklists.md",
                "references/validation-scenarios.md",
                "references/project-entry-scan.md",
                "references/large-projects.md",
                "references/product-brief.md",
                "references/direct-edit-fast-path.md",
                "references/human-review-summary.md",
                "references/project-decisions.md",
            )
        )
        for retired in (
            "ask human confirmation before using subagents",
            "ask human confirmation before subagent use",
            "stop and ask human confirmation before subagent use",
            "approved Subagent Execution",
            "Subagents are optional accelerators for large Project Entry Scan only after human confirmation",
            "owning Feature Execute / Review / Gate route",
            "ask before Task Auto-Run or subagent execution",
            "request the exact bounded subagent gate",
            "Human-gated tasks, subagent dispatch",
            "Preserve separate Delivery Contract breaking-change, Human-gated task, subagent",
            "when subagents are available and the human confirms",
            "does not authorize target implementation, Feature Auto-Loop, Delivery Contract action, subagent dispatch",
            "let Later Start authorize Git, Contract, subagent",
        ):
            self.assertNotIn(retired, active)
        self.assertIn("Subagent dispatch itself is not a Human Gate", active)
        self.assertIn("automatic Final Review", active)

    def test_controller_fallback_cannot_weaken_review_evidence(self) -> None:
        stage_guides = read("references/stage-guides.md")
        assert_final_review_contract(self, stage_guides)
        mutation = stage_guides.replace(
            "Controller fallback remains forbidden while any mechanism is exposed",
            "failed dispatch permits controller-fallback",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_final_review_contract(self, mutation)

    def test_failed_dispatch_cannot_select_controller_fallback_while_mechanism_exists(self) -> None:
        stage_guides = h2_section(
            read("references/stage-guides.md"), "Task Done Gate And Final Review"
        )
        adapter = h2_section(read("references/external-skill-adapters.md"), "Subagent Adapter")
        runtime = read("references/runtime.md")
        design = read("references/design.md")
        combined = "\n".join((stage_guides, adapter, runtime, design))
        for required in (
            "failed runtime dispatch enters Diagnose Failure",
            "at most one diagnostic retry",
            "one attempt for each other distinct exposed dispatcher",
            "Controller fallback remains forbidden while any mechanism is exposed",
            "Final Review: blocked",
            "Recovery Owner: runtime dispatcher",
            "do not loop",
            "Only when diagnosis establishes that the runtime exposes no Subagent dispatch mechanism",
        ):
            self.assertIn(required, combined)
        for required in (
            "at most one diagnostic retry for that dispatcher",
            "one attempt for each other distinct exposed dispatcher",
            "Final Review: blocked",
            "Recovery Owner: runtime dispatcher",
            "do not loop or use controller fallback",
        ):
            self.assertIn(required, runtime)
        for required in (
            "one bounded attempt set",
            "runtime-dispatcher recovery blocker",
            "controller fallback only when no mechanism is exposed",
        ):
            self.assertIn(required, design)

    def test_read_only_reviewer_returns_helper_resolution_before_review(self) -> None:
        skill = read("SKILL.md")
        routing = read("references/skill-routing.md")
        adapter = read("references/external-skill-adapters.md")
        guide = read("references/stage-guides.md")
        brief = read("templates/subagent-brief.md")
        notes = read("templates/notes.md")
        combined = "\n".join((skill, routing, adapter, guide))
        for required in (
            "persists coordination-helper resolution before dispatch",
            "response-local Reviewer Helper Resolution",
            "before substantive review",
            "returns the exact evidence",
            "writes no files",
            "persists that returned evidence before validating findings",
        ):
            self.assertIn(required, combined)
        runtime = read("references/runtime.md")
        assert_ordered(
            self,
            runtime,
            (
                "persists Subagent coordination resolution before dispatch",
                "forms a response-local Reviewer Helper Resolution as its first internal action",
                "before substantive review",
                "returns it without writing files",
                "owner persists it before using findings",
            ),
        )
        assert_ordered(
            self,
            routing,
            (
                "persists the Subagent coordination resolution",
                "As the first internal reviewer action",
                "before any substantive review",
                "returns that exact record without writing files",
                "persists the returned Reviewer Helper Resolution",
            ),
        )
        assert_ordered(
            self,
            brief,
            (
                "resolve the requested review helper as the first internal action",
                "before substantive review",
                "return it without persisting any file",
                "Reviewer Helper Resolution (read-only Final Review only)",
            ),
        )
        for required in (
            "Reviewer Helper Resolution (read-only Final Review only)",
            "Candidates Checked:",
            "Status: loaded | unavailable | load-failed",
            "Method Used:",
        ):
            self.assertIn(required, brief)
        self.assertIn("Coordination Helper Resolution:", notes)
        self.assertIn("Reviewer Helper Resolution:", notes)

    def test_one_session_subagent_handoff_is_response_local_by_default(self) -> None:
        active = "\n".join(
            (
                read("SKILL.md"),
                read("references/artifact-rules.md"),
                read("references/external-skill-adapters.md"),
                read("references/skill-routing.md"),
                read("references/stage-guides.md"),
                read("references/workflow-checklists.md"),
                read("references/large-projects.md"),
                read("references/document-templates.md"),
                read("references/validation-scenarios.md"),
            )
        )
        for required in (
            "response-local in one reliable session",
            "cross-session recovery",
            "complex handoff",
            "explicit audit value",
        ):
            self.assertIn(required, active)
        for path in (
            "references/large-projects.md",
            "references/document-templates.md",
        ):
            content = read(path)
            self.assertIn("response-local in one reliable session", content)
            self.assertIn("cross-session recovery", content)
            self.assertIn("complex handoff", content)
            self.assertIn("explicit audit value", content)
        self.assertNotIn(
            "Keep temporary subagent briefs in `handoffs/`",
            read("references/large-projects.md"),
        )
        self.assertNotIn(
            "Keep `handoffs/` for temporary subagent briefs and returned summaries",
            read("references/document-templates.md"),
        )
        for forbidden in (
            "Keep temporary subagent assignment notes in `handoffs/`.",
            "write subagent briefs and returns under `features/<feature>/handoffs/*`",
            "keep briefs/returns under `handoffs/*`",
        ):
            self.assertNotIn(forbidden, active)

    def test_overlapping_subagent_writes_are_not_parallelized(self) -> None:
        scenarios = read("references/validation-scenarios.md")
        adapter = read("references/external-skill-adapters.md")
        assert_overlap_contract(self, adapter)
        section = h2_section(
            scenarios, "85. Inline Task Review, Final Review, And Agent-Owned Delegation"
        )
        for required in (
            "Overlapping Subagent Writes Stay Serialized",
            "same writable file",
            "mechanically non-overlapping paths or serialize the assignments",
            "dispatch overlapping writes concurrently",
        ):
            self.assertIn(required, section)
        mutation = adapter.replace(
            "mechanically non-overlapping write sets",
            "dispatches overlapping writes concurrently",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_overlap_contract(self, mutation)

    def test_active_routes_do_not_reintroduce_standalone_review(self) -> None:
        stage_guides = read("references/stage-guides.md")
        adapter = read("references/external-skill-adapters.md")
        completion = read("references/feature-completion-check.md")
        follow_up = read("references/feature-follow-up.md")
        self.assertNotIn("after Verify, Review, Drift Check", stage_guides)
        self.assertNotIn("return to Execute / Verify / Review", adapter)
        self.assertNotIn("after Verify, Review, Drift Check", follow_up)
        self.assertIn(
            "return to Execute, Verify, Task Done Gate, or Final Review finding assessment",
            adapter,
        )
        self.assertIn(
            "helpers support evidence discipline and close-decision presentation only",
            completion,
        )
        self.assertIn("must not perform another code review", completion)

    def test_currentness_and_concurrency_fields_reach_templates_and_summaries(self) -> None:
        tasks = read("templates/tasks.md")
        task_detail = read("templates/task-detail.md")
        notes = read("templates/notes.md")
        brief = read("templates/subagent-brief.md")
        summary = read("references/human-review-summary.md")
        routing = read("references/skill-routing.md")
        for content in (tasks, task_detail):
            self.assertIn("Task Completion Review Currentness: current | stale", content)
        self.assertIn("Evidence Pointer | Currentness", notes)
        self.assertIn("Affected Task Review Pointer / Currentness", notes)
        self.assertIn("Write Concurrency:", brief)
        self.assertIn("Task Completion Review Pointers | current / stale / missing", summary)
        self.assertIn("mechanically non-overlapping", routing)
        self.assertIn("known same writable path is serialized", routing)

    def test_implementation_plan_status_matches_phase_one_reality(self) -> None:
        plan = read(
            "docs/proposal/v1.5.x/adaptive-review-and-conditional-feature-close-review-implementation-plan.md"
        )
        completed = bounded(plan, "### Task 0:", "### Task 6:")
        self.assertNotIn("- [ ]", completed)
        self.assertIn("Human-authorized Review Repair", plan)
        completion_boundary = h2_section(plan, "9. Completion Boundary For This Plan")
        self.assertNotIn("repository is stopped before implementation", completion_boundary)
        self.assertIn("Phase 2 remains pending", completion_boundary)

    def test_root_projection_keeps_human_close_and_removes_duplicate_review(self) -> None:
        root = read("templates/root-AGENTS.md")
        runtime = read("references/runtime.md")
        self.assertIn("Task Completion Review", root)
        self.assertIn("Final Review", root)
        self.assertIn("Human Close Gate", root)
        self.assertIn("agent-loop controller is unavailable or load-failed", root)
        self.assertIn("agent-loop controller is unavailable/load-failed", runtime)
        self.assertNotIn("controller fallback forces it", root + "\n" + runtime)
        self.assertNotIn("Feature Close Review", root)
        self.assertNotIn("Subagent Execution If Approved", root)

    def test_no_new_stage_status_checker_or_default_review_directory(self) -> None:
        runtime = read("references/runtime.md")
        design = read("references/design.md")
        combined = runtime + "\n" + design
        for required in (
            "does not add a canonical stage",
            "does not add a lifecycle status",
            "does not add an Auto Mode",
            "does not add a checker",
            "does not add a default artifact directory",
        ):
            self.assertIn(required, combined)
        self.assertFalse((ROOT / "scripts/check-final-review.py").exists())
        self.assertFalse((ROOT / "templates/final-review.md").exists())

    def test_legacy_review_records_are_readable_but_not_current_authorization(self) -> None:
        concepts = read("references/concepts.md")
        scenarios = read("references/validation-scenarios.md")
        for content in (concepts, scenarios):
            self.assertIn("legacy Review", content)
            self.assertIn("legacy Feature Close Review", content)
            self.assertIn("does not authorize", content)


if __name__ == "__main__":
    unittest.main()
