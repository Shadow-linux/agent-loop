#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from checker_support import (
    CheckFailure,
    configure_utf8_stdio,
    optional_section,
    read_text,
    require_supported_python,
    table,
)
from requirement_product_support import (
    CONCEPT_ID_PATTERN,
    MODEL_ID_PATTERN,
    ProductDefinitionError,
    normalized,
    resolve_effective_product_definition,
)


CURRENT = 0
BLOCKED = 1
REFRESH_REQUIRED = 3
COMPATIBLE_REQUIREMENT_STATUS = {
    "accepted",
    "in-progress",
    "partially-implemented",
    "implemented",
}
SHA256 = re.compile(r"[0-9a-f]{64}")
REQUIRED_SNAPSHOT_FIELDS = (
    "Requirement Set",
    "Requirement Lifecycle",
    "Resolved Product Source",
    "Product Definition Profile",
    "Product Review",
    "Product Source SHA-256",
    "Applicable Decisions",
    "Decision Source SHA-256",
    "Product Slice References",
    "Verified At",
    "Freshness",
)
REQUIRED_SNAPSHOT_SECTIONS = (
    "Product Outcome",
    "Actors And Core Journey",
    "Applicable Product Rules And Invariants",
    "Applicable States, Exceptions, And Recovery",
    "Feature Boundary And Acceptance Context",
)


@dataclass(frozen=True)
class ContextResult:
    status: str
    reasons: tuple[str, ...]

    @property
    def exit_code(self) -> int:
        return {
            "current": CURRENT,
            "refresh-required": REFRESH_REQUIRED,
            "blocked": BLOCKED,
        }[self.status]


def field(text: str, name: str) -> str | None:
    match = re.search(
        rf"(?mi)^\s*(?:-\s*)?{re.escape(name)}\s*:\s*(.*?)\s*$",
        text,
    )
    return match.group(1).strip() if match else None


def project_path(project_root: Path, value: str) -> Path:
    cleaned = normalized(value).replace("\\", "/")
    candidate = Path(cleaned)
    if candidate.is_absolute():
        raise ValueError(f"path must be project-root-relative: {value}")
    resolved = (project_root / candidate).resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError as error:
        raise ValueError(f"path escapes project root: {value}") from error
    return resolved


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def heading_anchors(content: str) -> set[str]:
    values = re.findall(r"^#{2,3}\s+(.+?)\s*$", content, re.MULTILINE)
    anchors = set()
    for value in values:
        cleaned = re.sub(r"[^a-z0-9 -]", "", value.lower())
        anchors.add(re.sub(r"[ -]+", "-", cleaned).strip("-"))
    return anchors


def memory_root_for(project_root: Path, feature_spec: Path) -> Path:
    roots = [
        project_root / name
        for name in (".agent-loop", "agent-loop")
        if (project_root / name).exists()
    ]
    if len(roots) != 1:
        raise ValueError("project must contain exactly one accepted memory root")
    memory_root_entry = roots[0]
    if memory_root_entry.is_symlink() or not memory_root_entry.is_dir():
        raise ValueError("accepted memory root must be one real directory")
    memory_root = memory_root_entry.resolve()
    try:
        feature_relative = feature_spec.resolve().relative_to(memory_root)
    except ValueError as error:
        raise ValueError("Feature spec is outside the accepted memory root") from error
    if len(feature_relative.parts) < 3 or feature_relative.parts[0] != "features":
        raise ValueError("Feature spec must be inside the memory root features directory")
    return memory_root


def require_within(path: Path, boundary: Path, label: str) -> None:
    try:
        path.resolve().relative_to(boundary.resolve())
    except ValueError as error:
        raise ValueError(f"{label} escapes accepted boundary") from error


def relative_project_path(project_root: Path, path: Path) -> str:
    return path.resolve().relative_to(project_root.resolve()).as_posix()


def effective_source_path(readme_path: Path, readme_text: str) -> Path:
    new_pointer = optional_section(readme_text, "Effective Product Definition")
    legacy_pointer = optional_section(readme_text, "Effective Concept Foundation")
    if new_pointer is not None and legacy_pointer is not None:
        raise ProductDefinitionError("multiple effective product source pointers")
    if new_pointer is not None:
        source_value = field(new_pointer, "Source")
    elif legacy_pointer is not None:
        source_value = field(legacy_pointer, "Effective Source")
    else:
        raise ProductDefinitionError("missing effective product source pointer")
    if not normalized(source_value):
        raise ProductDefinitionError("effective product source pointer is missing")
    cleaned = normalized(source_value).replace("\\", "/")
    candidate = Path(cleaned)
    if candidate.is_absolute():
        raise ProductDefinitionError("effective product source must be Requirement-relative")
    source_path = (readme_path.parent / candidate).resolve()
    require_within(source_path, readme_path.parent, "effective product source")
    return source_path


def validate_references(
    value: str,
    known_ids: set[str],
    known_anchors: set[str],
    *,
    label: str,
) -> None:
    ids = set(CONCEPT_ID_PATTERN.findall(value))
    ids.update(MODEL_ID_PATTERN.findall(value))
    anchors = set(re.findall(r"product\.md#([a-z0-9-]+)", value))
    unknown_ids = sorted(ids - known_ids)
    unknown_anchors = sorted(anchors - known_anchors)
    if unknown_ids:
        raise ValueError(f"{label} contains unknown source IDs: {', '.join(unknown_ids)}")
    if unknown_anchors:
        raise ValueError(
            f"{label} contains unknown source anchors: {', '.join(unknown_anchors)}"
        )


def decision_paths(
    project_root: Path,
    memory_root: Path,
    raw_value: str,
) -> list[tuple[str, Path]]:
    if normalized(raw_value).lower() == "none":
        return []
    values = [normalized(item) for item in raw_value.split(",")]
    if any(not value for value in values):
        raise ValueError("Applicable Decisions contains an empty path")
    if len(values) != len(set(values)):
        raise ValueError("Applicable Decisions contains duplicate paths")
    result: list[tuple[str, Path]] = []
    decisions_root = memory_root / "decisions"
    for value in values:
        path = project_path(project_root, value)
        require_within(path, decisions_root, "Applicable Decision")
        if path.suffix.lower() != ".md":
            raise ValueError(f"Applicable Decision is not Markdown: {value}")
        result.append((relative_project_path(project_root, path), path))
    return result


def recorded_decision_digests(raw_value: str) -> dict[str, str]:
    if normalized(raw_value).lower() == "none":
        return {}
    result: dict[str, str] = {}
    for item in raw_value.split(";"):
        if "=" not in item:
            raise ValueError("Decision Source SHA-256 contains a malformed entry")
        raw_path, raw_digest = item.split("=", 1)
        path_value = normalized(raw_path).replace("\\", "/")
        digest_value = normalized(raw_digest)
        if not path_value or not SHA256.fullmatch(digest_value):
            raise ValueError("Decision Source SHA-256 contains malformed evidence")
        if path_value in result:
            raise ValueError("Decision Source SHA-256 contains duplicate paths")
        result[path_value] = digest_value
    return result


def valid_verified_at(value: str) -> bool:
    candidate = normalized(value)
    if candidate.endswith("Z"):
        candidate = f"{candidate[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def classify(
    project_root: Path,
    feature_spec: Path,
) -> ContextResult:
    blocked_reasons: list[str] = []
    refresh_reasons: list[str] = []

    try:
        require_within(feature_spec, project_root, "Feature spec")
        if not feature_spec.is_file():
            raise ValueError(f"missing Feature spec: {feature_spec}")
        memory_root = memory_root_for(project_root, feature_spec)
        spec_text = read_text(feature_spec)
    except (OSError, UnicodeError, ValueError) as error:
        return ContextResult("blocked", (str(error),))

    snapshot = optional_section(spec_text, "Feature Context Snapshot")
    source_section = optional_section(spec_text, "Product Requirement Source")
    if source_section is None:
        return ContextResult(
            "blocked",
            ("Feature spec is missing Product Requirement Source",),
        )
    if snapshot is None:
        refresh_reasons.append("Feature Context Snapshot is missing")
        snapshot_fields: dict[str, str | None] = {}
    else:
        snapshot_fields = {
            name: normalized(field(snapshot, name)) or None
            for name in REQUIRED_SNAPSHOT_FIELDS
        }
        for name, value in snapshot_fields.items():
            if value is None:
                refresh_reasons.append(f"Snapshot field is missing: {name}")
        for heading in REQUIRED_SNAPSHOT_SECTIONS:
            content = optional_section(snapshot, heading, level=3)
            if content is None or not content.strip():
                refresh_reasons.append(f"Snapshot section is incomplete: {heading}")

    source_requirement = normalized(field(source_section, "Requirement Set"))
    snapshot_requirement = snapshot_fields.get("Requirement Set")
    if snapshot_requirement and source_requirement:
        if snapshot_requirement.replace("\\", "/") != source_requirement.replace("\\", "/"):
            blocked_reasons.append("Feature contains ambiguous Requirement Set pointers")
    requirement_value = snapshot_requirement or source_requirement
    if not requirement_value:
        blocked_reasons.append("Requirement Set pointer is missing")

    readme_path: Path | None = None
    source = None
    readme_text = ""
    actual_lifecycle = ""
    if requirement_value:
        try:
            readme_path = project_path(project_root, requirement_value)
            require_within(readme_path, memory_root / "requirements", "Requirement Set")
            if readme_path.name != "README.md":
                raise ValueError("Requirement Set must point to README.md")
            if not readme_path.is_file():
                raise ValueError(f"Requirement README is missing: {requirement_value}")
            readme_text = read_text(readme_path)
            actual_lifecycle = normalized(field(readme_text, "Status"))
            if actual_lifecycle not in COMPATIBLE_REQUIREMENT_STATUS:
                raise ValueError(
                    "Requirement lifecycle is incompatible: "
                    f"{actual_lifecycle or 'missing'}"
                )
            resolved_source = effective_source_path(readme_path, readme_text)
            require_within(
                resolved_source,
                readme_path.parent,
                "resolved Product Definition",
            )
            require_within(
                resolved_source,
                memory_root,
                "resolved Product Definition",
            )
            source = resolve_effective_product_definition(
                readme_path,
                resolved_source,
            )
        except (
            CheckFailure,
            OSError,
            ProductDefinitionError,
            UnicodeError,
            ValueError,
        ) as error:
            blocked_reasons.append(str(error))

    if source is not None and readme_path is not None:
        resolved_value = snapshot_fields.get("Resolved Product Source")
        recorded_profile = snapshot_fields.get("Product Definition Profile")
        recorded_review = snapshot_fields.get("Product Review")

        source_product_value = normalized(
            field(source_section, "Effective Product Definition")
        )
        if source_product_value:
            try:
                source_product_path = project_path(
                    project_root,
                    source_product_value,
                )
                require_within(
                    source_product_path,
                    readme_path.parent,
                    "Product Requirement Source Product Definition",
                )
                if resolved_value:
                    snapshot_product_path = project_path(
                        project_root,
                        resolved_value,
                    )
                    if source_product_path != snapshot_product_path:
                        blocked_reasons.append(
                            "Feature contains ambiguous "
                            "Effective Product Definition pointers"
                        )
                if source_product_path != source.path:
                    refresh_reasons.append(
                        "Product Requirement Source Product Definition changed"
                    )
            except ValueError as error:
                blocked_reasons.append(str(error))
        else:
            refresh_reasons.append(
                "Product Requirement Source Effective Product Definition is missing"
            )

        expected_profile = source.profile or "legacy"
        source_profile = normalized(
            field(source_section, "Product Definition Profile")
        )
        if source_profile:
            if recorded_profile and source_profile != recorded_profile:
                blocked_reasons.append(
                    "Feature contains ambiguous Product Definition Profile values"
                )
            if source_profile != expected_profile:
                refresh_reasons.append(
                    "Product Requirement Source Product Definition Profile changed"
                )
        else:
            refresh_reasons.append(
                "Product Requirement Source Product Definition Profile is missing"
            )

        source_review_evidence = normalized(
            field(source_section, "Product Review Evidence")
        )
        expected_review = source.review
        if not source_review_evidence:
            refresh_reasons.append(
                "Product Requirement Source Product Review Evidence is missing"
            )
        elif recorded_review and not re.search(
            rf"(?i)(?<![a-z]){re.escape(recorded_review)}(?![a-z])",
            source_review_evidence,
        ):
            blocked_reasons.append(
                "Product Requirement Source Product Review Evidence "
                f"does not confirm {recorded_review}"
            )

        recorded_lifecycle = snapshot_fields.get("Requirement Lifecycle")
        if recorded_lifecycle and recorded_lifecycle != actual_lifecycle:
            refresh_reasons.append("Requirement Lifecycle changed")

        resolved_relative = relative_project_path(project_root, source.path)
        if resolved_value:
            try:
                recorded_source = project_path(project_root, resolved_value)
                require_within(
                    recorded_source,
                    readme_path.parent,
                    "recorded Product Source",
                )
                require_within(
                    recorded_source,
                    memory_root,
                    "recorded Product Source",
                )
                if recorded_source != source.path:
                    refresh_reasons.append("Resolved Product Source changed")
            except ValueError as error:
                blocked_reasons.append(str(error))
        elif snapshot is not None:
            refresh_reasons.append("Resolved Product Source is missing")

        if recorded_profile and recorded_profile != expected_profile:
            refresh_reasons.append("Product Definition Profile changed")
        if recorded_review and recorded_review != source.review:
            refresh_reasons.append("Product Review evidence changed")

        product_digest = snapshot_fields.get("Product Source SHA-256")
        if product_digest:
            if not SHA256.fullmatch(product_digest):
                refresh_reasons.append("Product Source SHA-256 is malformed")
            elif product_digest != digest(source.path):
                refresh_reasons.append("Product Source SHA-256 changed")

        verified_at = snapshot_fields.get("Verified At")
        if verified_at and not valid_verified_at(verified_at):
            refresh_reasons.append(
                "Verified At must be an ISO-8601 timestamp with a timezone"
            )

        known_ids = set(source.concept_ids) | set(source.model_ids)
        known_anchors = heading_anchors(source.content)
        try:
            for row in table(spec_text, "Product Slice"):
                validate_references(
                    row.get("Source Section / Model ID", ""),
                    known_ids,
                    known_anchors,
                    label="Product Slice",
                )
            snapshot_references = snapshot_fields.get("Product Slice References")
            if snapshot_references:
                validate_references(
                    snapshot_references,
                    known_ids,
                    known_anchors,
                    label="Product Slice References",
                )
                if not (
                    CONCEPT_ID_PATTERN.search(snapshot_references)
                    or MODEL_ID_PATTERN.search(snapshot_references)
                    or re.search(r"product\.md#[a-z0-9-]+", snapshot_references)
                ):
                    refresh_reasons.append(
                        "Product Slice References contains no resolvable reference"
                    )
        except (CheckFailure, ValueError) as error:
            blocked_reasons.append(str(error))

        source_decisions = (
            normalized(field(source_section, "Applicable Decisions")) or "none"
        )
        raw_decisions = snapshot_fields.get("Applicable Decisions") or source_decisions
        try:
            decisions = decision_paths(project_root, memory_root, raw_decisions)
            source_decision_paths = decision_paths(
                project_root,
                memory_root,
                source_decisions,
            )
            if snapshot_fields.get("Applicable Decisions") is not None and {
                display_path for display_path, _ in decisions
            } != {
                display_path for display_path, _ in source_decision_paths
            }:
                raise ValueError(
                    "Feature contains ambiguous Applicable Decisions pointers"
                )
            for display_path, decision_path in decisions:
                if not decision_path.is_file():
                    raise ValueError(f"Applicable Decision is missing: {display_path}")
                decision_text = read_text(decision_path)
                status = normalized(field(decision_text, "Status"))
                compatibility = normalized(
                    field(decision_text, "Upstream Compatibility")
                )
                if status != "accepted":
                    raise ValueError(
                        f"Applicable Decision is not accepted: {display_path}"
                    )
                if compatibility != "current":
                    raise ValueError(
                        "Applicable Decision Upstream Compatibility is not current: "
                        f"{display_path}"
                    )

            raw_evidence = snapshot_fields.get("Decision Source SHA-256")
            if raw_evidence:
                evidence = recorded_decision_digests(raw_evidence)
                decision_names = {display for display, _ in decisions}
                if set(evidence) != decision_names:
                    raise ValueError(
                        "Decision Source SHA-256 paths differ from Applicable Decisions"
                    )
                for display_path, decision_path in decisions:
                    if evidence[display_path] != digest(decision_path):
                        refresh_reasons.append(
                            f"Decision Source SHA-256 changed: {display_path}"
                        )
            elif snapshot is not None:
                refresh_reasons.append("Decision Source SHA-256 is missing")
        except (OSError, UnicodeError, ValueError) as error:
            blocked_reasons.append(str(error))

        if resolved_value and resolved_value.replace("\\", "/") != resolved_relative:
            refresh_reasons.append("recorded Product Source path is stale")

    recorded_freshness = snapshot_fields.get("Freshness")
    if recorded_freshness == "blocked":
        blocked_reasons.append("Snapshot Freshness is blocked")
    elif recorded_freshness == "refresh-required":
        refresh_reasons.append("Snapshot Freshness requires refresh")
    elif recorded_freshness not in {None, "current"}:
        refresh_reasons.append("Snapshot Freshness value is unsupported")

    if blocked_reasons:
        return ContextResult("blocked", tuple(sorted(set(blocked_reasons))))
    if refresh_reasons:
        return ContextResult(
            "refresh-required",
            tuple(sorted(set(refresh_reasons))),
        )
    return ContextResult("current", ("authority and digests match",))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Feature Context Snapshot authority and freshness."
    )
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("feature_spec", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_utf8_stdio()
    require_supported_python()
    args = parse_args(argv)
    project_root = args.project_root.resolve()
    feature_spec = (
        args.feature_spec.resolve()
        if args.feature_spec.is_absolute()
        else (project_root / args.feature_spec).resolve()
    )
    result = classify(project_root, feature_spec)
    prefix = {
        "current": "CURRENT",
        "refresh-required": "REFRESH_REQUIRED",
        "blocked": "BLOCKED",
    }[result.status]
    print(f"{prefix}: {'; '.join(result.reasons)}")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
