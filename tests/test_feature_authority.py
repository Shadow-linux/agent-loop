from __future__ import annotations

import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.checker_test_support import ROOT, combined_output, run_checker


SCRIPT = "scripts/check-feature-context.py"
FIXTURE = ROOT / "tests/fixtures/feature-context/current"
FEATURE = Path(".agent-loop/features/2026-07-25-example/spec.md")
BUG = Path(".agent-loop/bugs/2026-08-10-authority/README.md")


def authority_spec(
    authority_type: str,
    primary: str,
    *,
    supporting: str = "none",
    assessment: str = "current",
) -> str:
    return f"""# Feature Spec: Open Authority Fixture

Status: accepted
Feature Type: normal

## Feature Authority

Authority Type: {authority_type}
Primary Authority Reference: {primary}
Supporting Authority References: {supporting}
Authority Summary: preserve the accepted bounded behavior for this Feature
Agent Authority Assessment: {assessment}

## Problem / Goal

Exercise the declared authority without inventing a Requirement source.
"""


def bug_readme(feature_reference: str) -> str:
    return f"""# Bug: Open authority fixture

Bug ID: BUG-20260810-authority
Created: 2026-08-10
Last Updated: 2026-08-10
Status: in-progress
Resolution: unresolved

## Summary

The accepted behavior regressed.

## Expected Behavior

- Expected Behavior: the accepted bounded behavior remains observable
- Expected Behavior Evidence: human confirmed the existing Feature acceptance on 2026-08-10

## Resolution Path

- Path: linked-feature
- Target: {feature_reference}
- Human Decision: confirmed
- Decision Evidence: human confirmed this exact Fix Feature target on 2026-08-10
- Target Release Context: v1.5.4

## Verification And Close

- Fix Feature: {feature_reference}
- Fix Revision / Commit:
- Verification Evidence:
- Review Evidence:
- Drift Result:
- Resolution: unresolved
- Close Decision:
"""


def canonical_digest(path: Path) -> str:
    raw = path.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(canonical).hexdigest()


class FeatureAuthorityTests(unittest.TestCase):
    def make_project(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        shutil.copytree(FIXTURE / ".agent-loop", root / ".agent-loop")
        return temporary, root

    def run_feature(self, root: Path, feature: Path = FEATURE):
        return run_checker(
            SCRIPT,
            "--project-root",
            str(root),
            str(root / feature),
        )

    def write_authority(
        self,
        root: Path,
        authority_type: str,
        primary: str,
        *,
        supporting: str = "none",
        assessment: str = "current",
        bom_crlf: bool = False,
        feature: Path = FEATURE,
    ) -> None:
        content = authority_spec(
            authority_type,
            primary,
            supporting=supporting,
            assessment=assessment,
        )
        path = root / feature
        path.parent.mkdir(parents=True, exist_ok=True)
        if bom_crlf:
            path.write_bytes(("\ufeff" + content.replace("\n", "\r\n")).encode())
        else:
            path.write_text(content, encoding="utf-8")

    def write_bug(self, root: Path, feature_reference: str) -> None:
        path = root / BUG
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(bug_readme(feature_reference), encoding="utf-8")

    def write_archive_index(
        self,
        root: Path,
        feature_reference: str,
        *,
        state: str = "archived",
    ) -> None:
        feature_id = Path(feature_reference).parent.name
        month = Path(feature_reference).parent.parent.name
        (root / ".agent-loop/features/archive.md").write_text(
            f"""# Feature Archive

This file locates archived or rehydrated features. Feature specs, tests, notes, requirement sources, and accepted decisions remain authoritative.

| Feature ID | Month | Current Path | Archive State | Closed At | Delivered Summary | Source Requirements | Applicable Decisions | Last Moved At |
|---|---|---|---|---|---|---|---|---|
| {feature_id} | {month} | `{Path(feature_reference).parent.as_posix()}/` | {state} | 2026-08-09 | verified fixture | none | none | 2026-08-10 |
""",
            encoding="utf-8",
        )

    def write_snapshot(
        self,
        root: Path,
        authority_type: str,
        adapter: str,
        primary: str,
        *,
        supporting: str = "none",
        digest: str | None = None,
        applicability: str = "applicable",
        facts: str | None = None,
        extra_fields: str = "",
        feature: Path = FEATURE,
    ) -> None:
        if digest is None:
            digest = f"{primary}={canonical_digest(root / Path(primary))}"
        if facts is None:
            resolved_facts = [
                f"Authority Type {authority_type}",
                "Authority Summary preserve the accepted bounded behavior for this Feature",
                f"Primary Authority Reference {primary}",
            ]
            if supporting.casefold() != "none":
                resolved_facts.extend(
                    f"Supporting Authority Reference {item.strip()}"
                    for item in supporting.split(";")
                    if item.strip()
                )
            if adapter == "bug":
                feature_reference = feature.as_posix()
                feature_location = (
                    f"archived:{feature.parent.parent.name}"
                    if len(feature.parts) >= 5
                    else "flat"
                )
                resolved_facts.extend(
                    (
                        "Bug ID BUG-20260810-authority",
                        "Expected Behavior evidence human confirmed the existing Feature acceptance on 2026-08-10",
                        "Resolution Path linked-feature",
                        f"Fix Feature {feature_reference}",
                        f"Feature Location {feature_location}",
                    )
                )
            facts = "; ".join(resolved_facts)
        snapshot = f"""## Feature Context Snapshot

Authority Type: {authority_type}
Authority Adapter: {adapter}
Primary Authority Reference: {primary}
Supporting Authority References: {supporting}
Authority Applicability: {applicability}
Authority Facts: {facts}
Authority Source SHA-256: {digest}
{extra_fields}
Verified At: 2026-08-10T12:00:00+08:00
Freshness: current

"""
        path = root / feature
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace("## Problem / Goal", snapshot + "## Problem / Goal", 1),
            encoding="utf-8",
        )

    def assert_status(self, result, status: str) -> None:
        self.assertEqual(
            result.returncode,
            1 if status == "BLOCKED" else 0,
            combined_output(result),
        )
        self.assertIn(f"{status}:", combined_output(result))

    def test_explicit_requirement_product_definition_authority_is_current(self):
        _, root = self.make_project()
        spec = root / FEATURE
        text = spec.read_text(encoding="utf-8")
        block = authority_spec(
            "Feature Authority / Requirement Product Definition",
            ".agent-loop/requirements/2026-07-25-example/README.md",
            supporting=".agent-loop/decisions/0001-example.md",
        ).split("## Problem / Goal", 1)[0].split("## Feature Authority", 1)[1]
        spec.write_text(
            text.replace(
                "## Product Requirement Source",
                "## Feature Authority" + block + "## Product Requirement Source",
                1,
            ).replace(
                "## Feature Context Snapshot\n\n",
                f"""## Feature Context Snapshot

Authority Type: Feature Authority / Requirement Product Definition
Authority Adapter: requirement-product-definition
Primary Authority Reference: .agent-loop/requirements/2026-07-25-example/README.md
Supporting Authority References: .agent-loop/decisions/0001-example.md
Authority Applicability: applicable
Authority Facts: Authority Type Feature Authority / Requirement Product Definition; Authority Summary preserve the accepted bounded behavior for this Feature; Primary Authority Reference .agent-loop/requirements/2026-07-25-example/README.md; Supporting Authority Reference .agent-loop/decisions/0001-example.md
Authority Source SHA-256: .agent-loop/requirements/2026-07-25-example/README.md={canonical_digest(root / '.agent-loop/requirements/2026-07-25-example/README.md')}

""",
                1,
            ),
            encoding="utf-8",
        )
        self.assert_status(self.run_feature(root), "CURRENT")

    def test_legacy_product_requirement_source_remains_current(self):
        _, root = self.make_project()
        result = self.run_feature(root)
        self.assert_status(result, "CURRENT")

    def test_generic_feature_authority_with_local_evidence_is_current(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/accepted-feature.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Accepted Feature boundary\n", encoding="utf-8")
        self.write_authority(
            root,
            "Feature Authority / accepted existing Feature",
            ".agent-loop/evidence/accepted-feature.md",
        )
        self.write_snapshot(
            root,
            "Feature Authority / accepted existing Feature",
            "feature",
            ".agent-loop/evidence/accepted-feature.md",
        )
        self.assert_status(self.run_feature(root), "CURRENT")

    def test_explicit_feature_authority_is_not_overridden_by_empty_product_section(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/accepted-feature.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Accepted Feature boundary\n", encoding="utf-8")
        self.write_authority(
            root,
            "Feature Authority / accepted existing Feature",
            ".agent-loop/evidence/accepted-feature.md",
        )
        spec = root / FEATURE
        spec.write_text(
            spec.read_text(encoding="utf-8").replace(
                "## Problem / Goal",
                """## Product Requirement Source

Use only when the Requirement Product Definition sub-adapter applies.

## Problem / Goal""",
                1,
            ),
            encoding="utf-8",
        )
        self.write_snapshot(
            root,
            "Feature Authority / accepted existing Feature",
            "feature",
            ".agent-loop/evidence/accepted-feature.md",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CURRENT")
        self.assertNotIn("Requirement Set", combined_output(result))

    def test_generic_feature_authority_without_snapshot_is_changed(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/accepted-feature.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Accepted Feature boundary\n", encoding="utf-8")
        self.write_authority(
            root,
            "Feature Authority / accepted existing Feature",
            ".agent-loop/evidence/accepted-feature.md",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("Snapshot", combined_output(result))

    def test_generic_feature_authority_with_stale_digest_is_changed(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/accepted-feature.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Accepted Feature boundary\n", encoding="utf-8")
        self.write_authority(
            root,
            "Feature Authority / accepted existing Feature",
            ".agent-loop/evidence/accepted-feature.md",
        )
        self.write_snapshot(
            root,
            "Feature Authority / accepted existing Feature",
            "feature",
            ".agent-loop/evidence/accepted-feature.md",
            digest=(
                ".agent-loop/evidence/accepted-feature.md="
                + "0" * 64
            ),
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("SHA-256", combined_output(result))

    def test_changed_authority_summary_invalidates_current_snapshot(self):
        _, root = self.make_project()
        primary = ".agent-loop/evidence/accepted-feature.md"
        authority_type = "Feature Authority / accepted existing Feature"
        evidence = root / primary
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Accepted Feature boundary\n", encoding="utf-8")
        self.write_authority(root, authority_type, primary)
        self.write_snapshot(
            root,
            authority_type,
            "feature",
            primary,
            facts=(
                f"Authority Type {authority_type}; "
                "Authority Summary preserve the accepted bounded behavior for this Feature; "
                f"Primary Authority Reference {primary}"
            ),
        )
        spec = root / FEATURE
        spec.write_text(
            spec.read_text(encoding="utf-8").replace(
                "Authority Summary: preserve the accepted bounded behavior for this Feature",
                "Authority Summary: narrow the accepted behavior to a different boundary",
                1,
            ),
            encoding="utf-8",
        )

        result = self.run_feature(root)

        self.assert_status(result, "CHANGED")
        self.assertIn("Authority Facts", combined_output(result))

    def test_authority_summary_with_semicolon_can_be_current(self):
        _, root = self.make_project()
        primary = ".agent-loop/evidence/accepted-feature.md"
        authority_type = "Feature Authority / accepted existing Feature"
        summary = "preserve accepted behavior; exclude provider migration"
        evidence = root / primary
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Accepted Feature boundary\n", encoding="utf-8")
        self.write_authority(root, authority_type, primary)
        spec = root / FEATURE
        spec.write_text(
            spec.read_text(encoding="utf-8").replace(
                "Authority Summary: preserve the accepted bounded behavior for this Feature",
                f"Authority Summary: {summary}",
                1,
            ),
            encoding="utf-8",
        )
        self.write_snapshot(
            root,
            authority_type,
            "feature",
            primary,
            facts=(
                f"Authority Type {authority_type}; "
                f"Authority Summary {summary}; "
                f"Primary Authority Reference {primary}"
            ),
        )

        result = self.run_feature(root)

        self.assert_status(result, "CURRENT")

    def test_stale_authority_facts_cannot_remain_current(self):
        _, root = self.make_project()
        primary = ".agent-loop/evidence/accepted-feature.md"
        authority_type = "Feature Authority / accepted existing Feature"
        evidence = root / primary
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Accepted Feature boundary\n", encoding="utf-8")
        self.write_authority(root, authority_type, primary)
        self.write_snapshot(
            root,
            authority_type,
            "feature",
            primary,
            facts="Authority Type stale; Authority Summary stale; Primary Authority Reference stale",
        )

        result = self.run_feature(root)

        self.assert_status(result, "CHANGED")
        self.assertIn("Authority Facts", combined_output(result))

    def test_bug_authority_with_flat_feature_locator_is_current(self):
        _, root = self.make_project()
        feature_reference = FEATURE.as_posix()
        self.write_bug(root, feature_reference)
        self.write_authority(root, "Bug Authority", BUG.as_posix())
        self.write_snapshot(
            root,
            "Bug Authority",
            "bug",
            BUG.as_posix(),
            extra_fields=f"""Bug ID: BUG-20260810-authority
Expected Behavior Evidence Locator: human confirmed the existing Feature acceptance on 2026-08-10
Resolution Path / Fix Feature Locator: linked-feature / {feature_reference}
Feature Location: flat
""",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CURRENT")
        self.assertIn("BUG-20260810-authority", combined_output(result))

    def test_bug_authority_with_archived_feature_locator_is_current(self):
        _, root = self.make_project()
        archived = Path(
            ".agent-loop/features/2026-07/2026-07-25-example/spec.md"
        )
        feature_reference = archived.as_posix()
        self.write_bug(root, feature_reference)
        shutil.rmtree((root / FEATURE).parent)
        self.write_archive_index(root, feature_reference)
        self.write_authority(
            root,
            "Bug Authority",
            BUG.as_posix(),
            feature=archived,
        )
        self.write_snapshot(
            root,
            "Bug Authority",
            "bug",
            BUG.as_posix(),
            extra_fields=f"""Bug ID: BUG-20260810-authority
Expected Behavior Evidence Locator: human confirmed the existing Feature acceptance on 2026-08-10
Resolution Path / Fix Feature Locator: linked-feature / {feature_reference}
Feature Location: archived:2026-07
""",
            feature=archived,
        )
        result = self.run_feature(root, archived)
        self.assert_status(result, "CURRENT")
        self.assertIn(feature_reference, combined_output(result))

    def test_archived_bug_authority_rejects_rehydrated_month_locator(self):
        _, root = self.make_project()
        archived = Path(
            ".agent-loop/features/2026-07/2026-07-25-example/spec.md"
        )
        feature_reference = archived.as_posix()
        self.write_bug(root, feature_reference)
        shutil.rmtree((root / FEATURE).parent)
        self.write_archive_index(root, feature_reference, state="rehydrated")
        self.write_authority(
            root,
            "Bug Authority",
            BUG.as_posix(),
            feature=archived,
        )
        result = self.run_feature(root, archived)
        self.assert_status(result, "BLOCKED")
        self.assertIn("archive", combined_output(result).lower())

    def test_bug_authority_preserves_internal_memory_alias_logical_paths(self):
        _, root = self.make_project()
        memory_root = root / ".agent-loop"
        real_memory = root / "real-memory"
        memory_root.rename(real_memory)
        try:
            memory_root.symlink_to("real-memory", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink unavailable: {error}")
        feature_reference = FEATURE.as_posix()
        self.write_bug(root, feature_reference)
        self.write_authority(root, "Bug Authority", BUG.as_posix())
        self.write_snapshot(
            root,
            "Bug Authority",
            "bug",
            BUG.as_posix(),
            extra_fields=f"""Bug ID: BUG-20260810-authority
Expected Behavior Evidence Locator: human confirmed the existing Feature acceptance on 2026-08-10
Resolution Path / Fix Feature Locator: linked-feature / {feature_reference}
Feature Location: flat
""",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CURRENT")
        self.assertIn(feature_reference, combined_output(result))

    def test_human_authority_is_advisory_without_invented_file(self):
        _, root = self.make_project()
        self.write_authority(
            root,
            "Human Authority / current conversation",
            "human-decision:conversation/2026-08-10#message-1",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("Human Authority / current conversation", combined_output(result))
        self.assertNotIn("Requirement Set pointer is missing", combined_output(result))

    def test_human_authority_declared_local_escape_is_blocked(self):
        _, root = self.make_project()
        self.write_authority(
            root,
            "Human Authority / preserved decision",
            "../outside-human-decision.md",
        )
        result = self.run_feature(root)
        self.assert_status(result, "BLOCKED")
        self.assertIn("escapes project root", combined_output(result))

    def test_external_bug_authority_is_advisory(self):
        _, root = self.make_project()
        self.write_authority(
            root,
            "Bug Authority / external tracker",
            "ticket:BUG-431",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("Expected Behavior", combined_output(result))

    def test_plain_external_ticket_locator_is_advisory_not_a_local_path(self):
        _, root = self.make_project()
        self.write_authority(
            root,
            "External Compliance Obligation",
            "COMPLIANCE-431",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertNotIn("missing or unreadable", combined_output(result))

    def test_lowercase_external_ticket_locator_is_advisory_not_a_local_path(self):
        _, root = self.make_project()
        self.write_authority(
            root,
            "External Compliance Obligation",
            "jira-431",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertNotIn("missing or unreadable", combined_output(result))

    def test_external_feature_authority_is_advisory_not_current(self):
        _, root = self.make_project()
        self.write_authority(
            root,
            "Feature Authority / accepted external contract",
            "https://example.invalid/contracts/accepted-431",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("external", combined_output(result).lower())

    def test_unknown_local_authority_is_advisory_and_preserves_type(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/obligation.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Accepted operational obligation\n", encoding="utf-8")
        self.write_authority(
            root,
            "Operational Obligation v2",
            ".agent-loop/evidence/obligation.md",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("Operational Obligation v2", combined_output(result))

    def test_debug_evidence_is_custom_not_bug_authority(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/debug.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("# Debug evidence\n", encoding="utf-8")
        self.write_authority(
            root,
            "Debug Evidence",
            ".agent-loop/evidence/debug.md",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertNotIn("Bug ID", combined_output(result))
        self.assertNotIn("Resolution Path", combined_output(result))

    def test_unknown_external_authority_is_advisory_not_a_local_path(self):
        _, root = self.make_project()
        self.write_authority(
            root,
            "External Compliance Ticket",
            "ticket:COMPLIANCE-431",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("ticket:COMPLIANCE-431", combined_output(result))
        self.assertNotIn("is missing:", combined_output(result).lower())

    def test_mixed_bug_primary_and_requirement_decision_support_is_non_blocking(self):
        _, root = self.make_project()
        self.write_bug(root, FEATURE.as_posix())
        self.write_authority(
            root,
            "Bug Authority",
            BUG.as_posix(),
            supporting=(
                ".agent-loop/requirements/2026-07-25-example/README.md; "
                ".agent-loop/decisions/0001-example.md"
            ),
        )
        result = self.run_feature(root)
        self.assertEqual(result.returncode, 0, combined_output(result))
        self.assertNotIn("BLOCKED:", combined_output(result))

    def test_supporting_authority_semantic_conflict_is_advisory(self):
        _, root = self.make_project()
        first = root / ".agent-loop/evidence/allow.md"
        second = root / ".agent-loop/evidence/deny.md"
        first.parent.mkdir(parents=True)
        first.write_text("Retry is required.\n", encoding="utf-8")
        second.write_text("Retry is forbidden.\n", encoding="utf-8")
        self.write_authority(
            root,
            "Operational Obligation",
            ".agent-loop/evidence/allow.md",
            supporting=".agent-loop/evidence/deny.md",
            assessment="changed",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("support", combined_output(result).lower())

    def test_duplicate_supporting_locator_is_advisory_not_blocked(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/allow.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_text("Retry is required.\n", encoding="utf-8")
        locator = ".agent-loop/evidence/allow.md"
        self.write_authority(
            root,
            "Operational Obligation",
            locator,
            supporting=f"{locator}; {locator}",
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("duplicate", combined_output(result).lower())

    def test_two_contradictory_primary_authorities_are_blocked(self):
        _, root = self.make_project()
        first = authority_spec("Bug Authority", BUG.as_posix())
        second = authority_spec(
            "Human Authority",
            "human-decision:conversation/2026-08-10#message-2",
        )
        (root / FEATURE).write_text(first + "\n" + second, encoding="utf-8")
        result = self.run_feature(root)
        self.assert_status(result, "BLOCKED")
        self.assertIn("primary", combined_output(result).lower())
        self.assertIn("authorit", combined_output(result).lower())

    def test_duplicate_primary_fields_in_one_authority_block_are_blocked(self):
        _, root = self.make_project()
        first = root / ".agent-loop/evidence/first.md"
        second = root / ".agent-loop/evidence/second.md"
        first.parent.mkdir(parents=True)
        first.write_text("first\n", encoding="utf-8")
        second.write_text("second\n", encoding="utf-8")
        spec = authority_spec(
            "Operational Obligation",
            ".agent-loop/evidence/first.md",
        ).replace(
            "Primary Authority Reference: .agent-loop/evidence/first.md",
            """Primary Authority Reference: .agent-loop/evidence/first.md
Primary Authority Reference: .agent-loop/evidence/second.md""",
            1,
        )
        (root / FEATURE).write_text(spec, encoding="utf-8")
        result = self.run_feature(root)
        self.assert_status(result, "BLOCKED")
        self.assertIn("primary", combined_output(result).lower())
        self.assertIn("multiple", combined_output(result).lower())

    def test_missing_declared_local_primary_is_blocked(self):
        _, root = self.make_project()
        self.write_authority(
            root,
            "Operational Evidence",
            ".agent-loop/evidence/missing.md",
        )
        result = self.run_feature(root)
        self.assert_status(result, "BLOCKED")
        self.assertIn("missing", combined_output(result).lower())
        self.assertIn("evidence/missing.md", combined_output(result))

    def test_unreadable_declared_local_primary_is_blocked(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/unreadable.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b"\xff\xfe\xfa")
        self.write_authority(
            root,
            "Operational Evidence",
            ".agent-loop/evidence/unreadable.md",
        )
        result = self.run_feature(root)
        self.assert_status(result, "BLOCKED")
        self.assertIn("unreadable", combined_output(result).lower())
        self.assertIn("evidence/unreadable.md", combined_output(result))

    def test_local_primary_path_escape_is_blocked(self):
        _, root = self.make_project()
        self.write_authority(root, "Operational Evidence", "../outside.md")
        result = self.run_feature(root)
        self.assert_status(result, "BLOCKED")
        self.assertIn("escapes project root", combined_output(result))

    def test_local_primary_symlink_escape_is_blocked(self):
        _, root = self.make_project()
        outside = root.parent / f"{root.name}-outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        self.addCleanup(outside.unlink, missing_ok=True)
        link = root / ".agent-loop/evidence/link.md"
        link.parent.mkdir(parents=True)
        try:
            link.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"symlink unavailable: {error}")
        self.write_authority(
            root,
            "Operational Evidence",
            ".agent-loop/evidence/link.md",
        )
        result = self.run_feature(root)
        self.assert_status(result, "BLOCKED")
        self.assertIn("escapes project root", combined_output(result))

    def test_bom_crlf_and_windows_style_local_authority_are_equivalent(self):
        _, root = self.make_project()
        evidence = root / ".agent-loop/evidence/windows.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b"\xef\xbb\xbf# Evidence\r\n")
        self.write_authority(
            root,
            "Operational Obligation v2",
            ".agent-loop\\evidence\\windows.md",
            bom_crlf=True,
        )
        result = self.run_feature(root)
        self.assert_status(result, "CHANGED")
        self.assertIn("Operational Obligation v2", combined_output(result))


if __name__ == "__main__":
    unittest.main()
