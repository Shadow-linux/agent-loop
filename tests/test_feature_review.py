from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FEATURE_GATE_AUTHORITIES = (
    "SKILL.md",
    "README.md",
    "Usage.md",
    "references/design.md",
    "references/runtime.md",
    "references/artifact-rules.md",
    "references/concepts.md",
    "references/document-templates.md",
    "references/human-review-summary.md",
    "references/implementation-planning.md",
    "references/project-guidance.md",
    "references/stage-guides.md",
    "references/validation-scenarios.md",
    "references/workflow-checklists.md",
    "templates/notes.md",
    "templates/root-AGENTS.md",
)

REMOVED_FEATURE_GATE_MECHANICS = (
    "check-feature-review.py",
    "Gate 1 Spec Digest",
    "Gate 2 Package Digest",
    "Gate 2 Stable Files",
    "Gate 2 Stable Digest",
    "EVIDENCE_MATCH",
    "EVIDENCE_CHANGED",
    "EVIDENCE_INVALID",
    "review-definition-v2",
)


def markdown_h2_section(content: str, heading: str) -> str:
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


def assert_section_contract(
    testcase: unittest.TestCase,
    content: str,
    heading: str,
    *,
    required: tuple[str, ...] = (),
    forbidden: tuple[str, ...] = (),
) -> None:
    section = markdown_h2_section(content, heading)
    for text in required:
        testcase.assertIn(text, section, f"{heading} must contain {text!r}")
    for text in forbidden:
        testcase.assertNotIn(text, section, f"{heading} must reject {text!r}")


def replace_in_h2_section(content: str, heading: str, old: str, new: str) -> str:
    section = markdown_h2_section(content, heading)
    if old not in section:
        raise AssertionError(f"{old!r} not found in owning section {heading!r}")
    return content.replace(section, section.replace(old, new, 1), 1)


def bounded_text(content: str, start_marker: str, end_marker: str) -> str:
    try:
        start = content.index(start_marker)
        end = content.index(end_marker, start + len(start_marker))
    except ValueError as exc:
        raise AssertionError(
            f"missing bounded owner markers: {start_marker!r} -> {end_marker!r}"
        ) from exc
    return content[start:end]


def assert_bounded_contract(
    testcase: unittest.TestCase,
    content: str,
    start_marker: str,
    end_marker: str,
    *,
    required: tuple[str, ...] = (),
    forbidden: tuple[str, ...] = (),
) -> None:
    owner = bounded_text(content, start_marker, end_marker)
    for text in required:
        testcase.assertIn(text, owner)
    for text in forbidden:
        testcase.assertNotIn(text, owner)


class FeatureReviewContractTests(unittest.TestCase):
    def test_feature_gate_checker_is_removed(self) -> None:
        self.assertFalse((ROOT / "scripts/check-feature-review.py").exists())

    def test_active_feature_gate_authorities_do_not_require_digest_mechanics(self) -> None:
        for relative in FEATURE_GATE_AUTHORITIES:
            content = (ROOT / relative).read_text(encoding="utf-8")
            for removed in REMOVED_FEATURE_GATE_MECHANICS:
                with self.subTest(relative=relative, removed=removed):
                    self.assertNotIn(removed, content)

    def test_runtime_keeps_two_human_reviews_and_agent_owned_package_review(self) -> None:
        runtime = (ROOT / "references/runtime.md").read_text(encoding="utf-8")
        for required in (
            "Gate 1: Feature Definition Review",
            "Gate 2: Implementation Readiness Review",
            "Gate 1 acceptance authorizes package preparation only",
            "The Agent verifies the complete implementation package",
            "Approve package only",
            "Approve package and start implementation",
            "without a third generic Feature Auto-Loop prompt",
            "new Task ID does not by itself repeat Gate 2",
            "Human authorization provenance is an Agent responsibility",
        ):
            with self.subTest(required=required):
                self.assertIn(required, runtime)

    def test_only_approval_choices_set_readiness_accepted(self) -> None:
        stage_guides = (ROOT / "references/stage-guides.md").read_text(encoding="utf-8")
        checklist = (ROOT / "references/workflow-checklists.md").read_text(
            encoding="utf-8"
        )
        for content in (stage_guides, checklist):
            self.assertIn("Only the two approval choices set `Implementation Readiness: accepted`", content)
            self.assertIn("`Revise package` returns readiness to `preparing`", content)
            self.assertIn("`Pause` does not mark readiness accepted", content)

    def test_later_start_is_agent_reviewed_without_a_local_preflight(self) -> None:
        runtime = (ROOT / "references/runtime.md").read_text(encoding="utf-8")
        assert_section_contract(
            self,
            runtime,
            "Human Gate Modes",
            required=(
                "re-read the recorded package files and current Feature artifacts",
                "compare their meaning with the accepted execution boundary",
                "No local script result is required to continue",
            ),
            forbidden=("local Feature Gate preflight is required",),
        )

    def test_later_start_preserves_gate2_baseline_and_uses_separate_transition(self) -> None:
        runtime = (ROOT / "references/runtime.md").read_text(encoding="utf-8")
        notes = (ROOT / "templates/notes.md").read_text(encoding="utf-8")
        assert_section_contract(
            self,
            runtime,
            "Human Gate Modes",
            required=(
                "Later Start Decision",
                "Later Start Authorized At",
                "Later Start Evidence",
                "preserving the original Gate 2 review baseline",
            ),
            forbidden=(
                "atomically record Gate 2 Decision `approve-and-start`, Feature Auto-Loop `enabled`, and the timezone-aware start time",
            ),
        )
        for field in (
            "Later Start Decision: none | approved",
            "Later Start Authorized At: none | <ISO-8601>",
            "Later Start Evidence: none | <Human instruction evidence>",
        ):
            self.assertIn(field, notes)

        assert_bounded_contract(
            self,
            runtime,
            "After the human explicitly says start and those Agent-owned checks pass",
            "Available control modes:",
            required=(
                "Preserve `Gate 2 Decision: package-only`",
                "the Gate 2 `Feature Auto-Loop: disabled` review value",
                "`Gate 2 Reviewed At` as the original Gate 2 review baseline",
            ),
            forbidden=(
                "overwrite",
                "Gate 2 Decision: approve-and-start",
                "Feature Auto-Loop: enabled",
            ),
        )

    def test_package_only_acceptance_cannot_execute_target_work(self) -> None:
        runtime = (ROOT / "references/runtime.md").read_text(encoding="utf-8")
        assert_bounded_contract(
            self,
            runtime,
            "Only the two approval choices set `Implementation Readiness: accepted`",
            "If the human later explicitly says to start implementation after package-only acceptance",
            required=(
                "`Approve package only` records accepted readiness and does not execute.",
            ),
            forbidden=(
                "package only` records accepted readiness and starts target implementation",
                "package-only acceptance authorizes execution",
            ),
        )

    def test_root_guidance_projects_later_start_without_rewriting_gate2(self) -> None:
        root_guidance = (ROOT / "templates/root-AGENTS.md").read_text(encoding="utf-8")
        assert_section_contract(
            self,
            root_guidance,
            "Gate Modes",
            required=(
                "valid separate later-start transition",
                "preserves the package-only Gate 2 baseline",
            ),
            forbidden=(
                "later start rewrites Gate 2",
                "Gate 2 Decision: approve-and-start",
            ),
        )

    def test_project_template_retains_current_gate_mode_owner(self) -> None:
        project = (ROOT / "templates/project.md").read_text(encoding="utf-8")
        current_work = markdown_h2_section(project, "Current Work")
        self.assertIn(
            "Gate Mode: Strict Mode | Feature Auto-Loop | Task Auto-Run",
            current_work,
        )

    def test_gate1_does_not_require_an_unlanded_spec_sha(self) -> None:
        stage_guides = (ROOT / "references/stage-guides.md").read_text(encoding="utf-8")
        requirement_checklist = markdown_h2_section(stage_guides, "Requirement Checklist")
        self.assertNotIn("Spec SHA-256", requirement_checklist)
        self.assertIn("Gate 1 Decision: accepted", requirement_checklist)

    def test_legacy_notes_without_later_start_fields_are_reader_compatible_only(self) -> None:
        runtime = (ROOT / "references/runtime.md").read_text(encoding="utf-8")
        assert_section_contract(
            self,
            runtime,
            "Human Gate Modes",
            required=(
                "Existing Feature notes without Later Start fields remain reader-compatible",
                "absence means no recorded later-start transition",
                "never authorizes execution",
            ),
        )

    def test_owning_section_contract_rejects_masked_gate_regressions(self) -> None:
        runtime = (ROOT / "references/runtime.md").read_text(encoding="utf-8")
        stage_guides = (ROOT / "references/stage-guides.md").read_text(encoding="utf-8")

        assert_section_contract(
            self,
            runtime,
            "Human Gate Modes",
            required=(
                "Delivery Contract creation and acceptance",
                "subagent dispatch",
                "commit, push, PR, merge, tag, release, publish",
                "Submit / Integrate",
                "Pause / Close",
            ),
        )
        assert_section_contract(
            self,
            stage_guides,
            "Analyze Consistency",
            required=(
                "Only the two approval choices set `Implementation Readiness: accepted`",
                "no local Feature Gate preflight is required",
            ),
            forbidden=("Any Gate 2 choice sets `Implementation Readiness: accepted`",),
        )

        independent_stops = (
            "Delivery Contract creation and acceptance",
            "subagent dispatch",
            "external mutation",
            "Submit / Integrate",
            "commit, push, PR, merge, tag, release, publish",
            "Pause / Close",
        )
        auto_loop_start = "In this mode, the agent may continue through Analyze Consistency"
        auto_loop_end = "For multiple Agent-ready tasks"
        auto_loop_owner = bounded_text(runtime, auto_loop_start, auto_loop_end)
        for stop in independent_stops:
            self.assertIn(stop, auto_loop_owner)
            weakened_owner = auto_loop_owner.replace(stop, "removed-independent-stop", 1)
            with self.subTest(stop=stop), self.assertRaises(AssertionError):
                self.assertIn(stop, weakened_owner)

        local_preflight = replace_in_h2_section(
            runtime,
            "Human Gate Modes",
            "No local script result is required to continue.",
            "No local script result is required to continue. A local Feature Gate preflight is required.",
        )
        with self.assertRaises(AssertionError):
            assert_section_contract(
                self,
                local_preflight,
                "Human Gate Modes",
                forbidden=("local Feature Gate preflight is required",),
            )

        legacy_authority = replace_in_h2_section(
            runtime,
            "Human Gate Modes",
            "Current top-level fields are authoritative; fenced examples and later history sections never supply current Gate evidence.",
            "Legacy fields and history may supply current Gate evidence.",
        )
        with self.assertRaises(AssertionError):
            assert_section_contract(
                self,
                legacy_authority,
                "Human Gate Modes",
                required=(
                    "Current top-level fields are authoritative; fenced examples and later history sections never supply current Gate evidence.",
                ),
                forbidden=("Legacy fields and history may supply current Gate evidence",),
            )

        package_only_execution = runtime.replace(
            "`Approve package only` records accepted readiness and does not execute.",
            "`Approve package only` records accepted readiness and starts target implementation immediately.",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_bounded_contract(
                self,
                package_only_execution,
                "Only the two approval choices set `Implementation Readiness: accepted`",
                "If the human later explicitly says to start implementation after package-only acceptance",
                required=("`Approve package only` records accepted readiness and does not execute.",),
                forbidden=("starts target implementation",),
            )

        later_start_overwrite = runtime.replace(
            "Preserve `Gate 2 Decision: package-only`, the Gate 2 `Feature Auto-Loop: disabled` review value, and `Gate 2 Reviewed At` as the original Gate 2 review baseline.",
            "Atomically overwrite `Gate 2 Decision: approve-and-start`, `Feature Auto-Loop: enabled`, and `Gate 2 Reviewed At` with the later-start time.",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_bounded_contract(
                self,
                later_start_overwrite,
                "After the human explicitly says start and those Agent-owned checks pass",
                "Available control modes:",
                required=("Preserve `Gate 2 Decision: package-only`",),
                forbidden=("overwrite", "Gate 2 Decision: approve-and-start"),
            )

        weakened_stage = replace_in_h2_section(
            stage_guides,
            "Analyze Consistency",
            "Only the two approval choices set `Implementation Readiness: accepted`.",
            "Any Gate 2 choice sets `Implementation Readiness: accepted`.",
        )
        with self.assertRaises(AssertionError):
            assert_section_contract(
                self,
                weakened_stage,
                "Analyze Consistency",
                required=("Only the two approval choices set `Implementation Readiness: accepted`",),
                forbidden=("Any Gate 2 choice sets `Implementation Readiness: accepted`",),
            )

    def test_later_start_contract_is_aligned_across_owning_surfaces(self) -> None:
        required_by_file = {
            "SKILL.md": ("separate Later Start", "original accepted"),
            "README.md": ("preserves the original Gate 2 baseline", "separate start transition"),
            "Usage.md": ("Later Start", "保留原 Gate 2 字段"),
            "references/design.md": ("separate decision/time/Human-evidence transition", "without rewriting the Gate 2 baseline"),
            "references/runtime.md": ("Later Start Decision", "preserving the original Gate 2 review baseline"),
            "references/artifact-rules.md": ("separate Later Start", "original durable accepted-review baseline"),
            "references/concepts.md": ("separate valid later-start transition", "does not create a third Gate"),
            "references/feature-completion-check.md": ("any Later Start evidence", "project `Gate Mode`"),
            "references/implementation-planning.md": ("separate Later Start", "preserves the package-only baseline"),
            "references/human-review-summary.md": ("separate Later Start", "preserves the original Gate 2 values"),
            "references/stage-guides.md": ("Later Start Decision: approved", "Preserve the original `package-only`"),
            "references/workflow-checklists.md": ("Later Start decision/time/Human evidence", "preserve the original Gate 2 baseline"),
            "references/validation-scenarios.md": ("Later Start Is A Transition, Not A Second Gate 2", "original `Gate 2 Decision: package-only`"),
            "templates/notes.md": ("Later Start Decision: none | approved", "original durable review baseline"),
            "references/document-templates.md": ("Later Start Decision: none | approved", "original durable review baseline"),
            "CHANGELOG.md": ("Later Start", "保留原 Gate 2 评审基线"),
        }
        for relative, required in required_by_file.items():
            content = (ROOT / relative).read_text(encoding="utf-8")
            for text in required:
                with self.subTest(relative=relative, text=text):
                    self.assertIn(text, content)

        forbidden_overwrites = (
            "records approve-and-start/enabled/time",
            "record approve-and-start/enabled/time",
            "atomically record Gate 2 Decision `approve-and-start`",
        )
        for relative in required_by_file:
            content = (ROOT / relative).read_text(encoding="utf-8")
            for text in forbidden_overwrites:
                with self.subTest(relative=relative, forbidden=text):
                    self.assertNotIn(text, content)


if __name__ == "__main__":
    unittest.main()
