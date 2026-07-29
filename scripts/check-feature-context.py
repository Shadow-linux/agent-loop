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
    discover_memory_root_authority,
    optional_section,
    read_text,
    require_supported_python,
    table,
)
from requirement_product_support import (
    CONCEPT_ID_PATTERN,
    EffectiveProductSource,
    MODEL_ID_PATTERN,
    ProductDefinitionError,
    normalized,
    resolve_effective_product_definition,
)


CURRENT = 0
BLOCKED = 1
CHANGED = 0
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
            "changed": CHANGED,
            "blocked": BLOCKED,
        }[self.status]


class AuthorityFailure(ValueError):
    """Physical or uniqueness contradiction that prevents safe source resolution."""


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
        raise AuthorityFailure(f"path must be project-root-relative: {value}")
    resolved = (project_root / candidate).resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError as error:
        raise AuthorityFailure(f"path escapes project root: {value}") from error
    return resolved


def compatible_text_digests(path: Path) -> frozenset[str]:
    raw = path.read_bytes()
    canonical = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    crlf = canonical.replace(b"\n", b"\r\n")
    return frozenset(
        hashlib.sha256(content).hexdigest()
        for content in (raw, canonical, crlf)
    )


def heading_anchors(content: str) -> set[str]:
    values = re.findall(r"^#{2,3}\s+(.+?)\s*$", content, re.MULTILINE)
    anchors = set()
    for value in values:
        cleaned = re.sub(r"[^a-z0-9 -]", "", value.lower())
        anchors.add(re.sub(r"[ -]+", "-", cleaned).strip("-"))
    return anchors


def memory_root_for(project_root: Path, feature_spec: Path) -> Path:
    try:
        authority = discover_memory_root_authority(project_root)
    except CheckFailure as error:
        raise AuthorityFailure(error.detail) from error
    if authority is None:
        raise AuthorityFailure("project must contain exactly one accepted memory root")
    try:
        feature_relative = feature_spec.resolve().relative_to(authority.resolved)
    except ValueError as error:
        raise AuthorityFailure(
            "Feature spec is outside the accepted memory root"
        ) from error
    if len(feature_relative.parts) < 3 or feature_relative.parts[0] != "features":
        raise AuthorityFailure(
            "Feature spec must be inside the memory root features directory"
        )
    return authority.logical


def require_within(path: Path, boundary: Path, label: str) -> None:
    try:
        path.resolve().relative_to(boundary.resolve())
    except ValueError as error:
        raise AuthorityFailure(f"{label} escapes accepted boundary") from error


def relative_project_path(project_root: Path, path: Path) -> str:
    resolved = path.resolve()
    try:
        authority = discover_memory_root_authority(project_root)
    except CheckFailure:
        authority = None
    if authority is not None:
        try:
            within_memory = resolved.relative_to(authority.resolved)
        except ValueError:
            pass
        else:
            return (
                authority.logical.relative_to(project_root) / within_memory
            ).as_posix()
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return resolved.relative_to(project_root.resolve()).as_posix()


def effective_source_path(readme_path: Path, readme_text: str) -> Path:
    new_pointer = optional_section(readme_text, "Effective Product Definition")
    legacy_pointer = optional_section(readme_text, "Effective Concept Foundation")
    if new_pointer is not None and legacy_pointer is not None:
        raise AuthorityFailure("multiple effective product source pointers")
    if new_pointer is not None:
        source_value = field(new_pointer, "Source")
    elif legacy_pointer is not None:
        source_value = field(legacy_pointer, "Effective Source")
    else:
        raise AuthorityFailure("missing effective product source pointer")
    if not normalized(source_value):
        raise AuthorityFailure("effective product source pointer is missing")
    cleaned = normalized(source_value).replace("\\", "/")
    candidate = Path(cleaned)
    if candidate.is_absolute():
        raise AuthorityFailure(
            "effective product source must be Requirement-relative"
        )
    source_path = (readme_path.parent / candidate).resolve()
    require_within(source_path, readme_path.parent, "effective product source")
    return source_path


def best_effort_source_facts(
    readme_path: Path,
    source_path: Path,
) -> tuple[EffectiveProductSource, str | None]:
    """Read objective source facts even when strict product semantics need review."""

    try:
        return resolve_effective_product_definition(readme_path, source_path), None
    except (CheckFailure, ProductDefinitionError) as error:
        content = read_text(source_path)
        readme_text = read_text(readme_path)
        legacy = optional_section(readme_text, "Effective Concept Foundation") is not None
        profile = None if legacy else normalized(field(content, "Product Definition Profile"))
        review = normalized(
            field(
                content,
                "Concept Foundation Status" if legacy else "Product Review",
            )
        )
        return (
            EffectiveProductSource(
                path=source_path.resolve(),
                content=content,
                kind="concept-foundation" if legacy else "product-definition",
                profile=profile or None,
                review=review,
                legacy=legacy,
                concept_ids=frozenset(CONCEPT_ID_PATTERN.findall(content)),
                model_ids=frozenset(MODEL_ID_PATTERN.findall(content)),
            ),
            str(error),
        )


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
            raise AuthorityFailure(f"Applicable Decision is not Markdown: {value}")
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
    changed_reasons: list[str] = []

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
        changed_reasons.append("Feature Context Snapshot is missing")
        snapshot_fields: dict[str, str | None] = {}
    else:
        snapshot_fields = {
            name: normalized(field(snapshot, name)) or None
            for name in REQUIRED_SNAPSHOT_FIELDS
        }
        for name, value in snapshot_fields.items():
            if value is None:
                changed_reasons.append(f"Snapshot field is missing: {name}")
        for heading in REQUIRED_SNAPSHOT_SECTIONS:
            content = optional_section(snapshot, heading, level=3)
            if content is None or not content.strip():
                changed_reasons.append(f"Snapshot section is incomplete: {heading}")

    source_requirement = normalized(field(source_section, "Requirement Set"))
    snapshot_requirement = snapshot_fields.get("Requirement Set")
    if snapshot_requirement and source_requirement:
        if snapshot_requirement.replace("\\", "/") != source_requirement.replace("\\", "/"):
            changed_reasons.append("Feature contains ambiguous Requirement Set pointers")
    requirement_value = source_requirement
    if not source_requirement:
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
                raise AuthorityFailure("Requirement Set must point to README.md")
            if not readme_path.is_file():
                raise AuthorityFailure(
                    f"Requirement README is missing: {requirement_value}"
                )
            readme_text = read_text(readme_path)
            actual_lifecycle = normalized(field(readme_text, "Status"))
            if actual_lifecycle not in COMPATIBLE_REQUIREMENT_STATUS:
                changed_reasons.append(
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
            if not resolved_source.is_file():
                raise AuthorityFailure(
                    f"resolved Product Definition is missing: {resolved_source}"
                )
            source, source_issue = best_effort_source_facts(
                readme_path,
                resolved_source,
            )
            if source_issue:
                changed_reasons.append(
                    f"Product authority needs Agent review: {source_issue}"
                )
        except (
            AuthorityFailure,
            OSError,
            UnicodeError,
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
                        changed_reasons.append(
                            "Feature contains ambiguous "
                            "Effective Product Definition pointers"
                        )
                if source_product_path != source.path:
                    changed_reasons.append(
                        "Product Requirement Source Product Definition changed"
                    )
            except AuthorityFailure as error:
                changed_reasons.append(
                    "Product Requirement Source Effective Product Definition "
                    f"is invalid cached evidence: {error}"
                )
        else:
            changed_reasons.append(
                "Product Requirement Source Effective Product Definition is missing"
            )

        expected_profile = source.profile or ("legacy" if source.legacy else "unknown")
        source_profile = normalized(
            field(source_section, "Product Definition Profile")
        )
        if source_profile:
            if recorded_profile and source_profile != recorded_profile:
                changed_reasons.append(
                    "Feature contains ambiguous Product Definition Profile values"
                )
            if source_profile != expected_profile:
                changed_reasons.append(
                    "Product Requirement Source Product Definition Profile changed"
                )
        else:
            changed_reasons.append(
                "Product Requirement Source Product Definition Profile is missing"
            )

        source_review_evidence = normalized(
            field(source_section, "Product Review Evidence")
        )
        expected_review = source.review
        if not source_review_evidence:
            changed_reasons.append(
                "Product Requirement Source Product Review Evidence is missing"
            )
        elif recorded_review and not re.search(
            rf"(?i)(?<![a-z]){re.escape(recorded_review)}(?![a-z])",
            source_review_evidence,
        ):
            changed_reasons.append(
                "Product Requirement Source Product Review Evidence "
                f"does not confirm {recorded_review}"
            )

        recorded_lifecycle = snapshot_fields.get("Requirement Lifecycle")
        if recorded_lifecycle and recorded_lifecycle != actual_lifecycle:
            changed_reasons.append("Requirement Lifecycle changed")

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
                if recorded_source.resolve() != source.path.resolve():
                    changed_reasons.append("Resolved Product Source changed")
            except AuthorityFailure as error:
                changed_reasons.append(
                    f"recorded Product Source is invalid cached evidence: {error}"
                )
        elif snapshot is not None:
            changed_reasons.append("Resolved Product Source is missing")

        if recorded_profile and recorded_profile != expected_profile:
            changed_reasons.append("Product Definition Profile changed")
        if recorded_review and recorded_review != source.review:
            changed_reasons.append("Product Review evidence changed")

        product_digest = snapshot_fields.get("Product Source SHA-256")
        if product_digest:
            if not SHA256.fullmatch(product_digest):
                changed_reasons.append("Product Source SHA-256 is malformed")
            elif product_digest not in compatible_text_digests(source.path):
                changed_reasons.append("Product Source SHA-256 changed")

        verified_at = snapshot_fields.get("Verified At")
        if verified_at and not valid_verified_at(verified_at):
            changed_reasons.append(
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
                    changed_reasons.append(
                        "Product Slice References contains no resolvable reference"
                    )
        except (CheckFailure, ValueError) as error:
            changed_reasons.append(str(error))

        source_decisions = (
            normalized(field(source_section, "Applicable Decisions")) or "none"
        )
        raw_decisions = snapshot_fields.get("Applicable Decisions") or source_decisions
        try:
            source_decision_paths = decision_paths(
                project_root,
                memory_root,
                source_decisions,
            )
            snapshot_decision_paths = decision_paths(
                project_root,
                memory_root,
                raw_decisions,
            )
            if snapshot_fields.get("Applicable Decisions") is not None and {
                display_path for display_path, _ in snapshot_decision_paths
            } != {
                display_path for display_path, _ in source_decision_paths
            }:
                changed_reasons.append(
                    "Feature contains ambiguous Applicable Decisions pointers"
                )
            decisions = source_decision_paths
            for display_path, decision_path in decisions:
                if not decision_path.is_file():
                    raise AuthorityFailure(
                        f"Applicable Decision is missing: {display_path}"
                    )
                decision_text = read_text(decision_path)
                status = normalized(field(decision_text, "Status"))
                compatibility = normalized(
                    field(decision_text, "Upstream Compatibility")
                )
                if status != "accepted":
                    changed_reasons.append(
                        f"Applicable Decision is not accepted: {display_path}"
                    )
                if compatibility != "current":
                    changed_reasons.append(
                        "Applicable Decision Upstream Compatibility is not current: "
                        f"{display_path}"
                    )

            raw_evidence = snapshot_fields.get("Decision Source SHA-256")
            if raw_evidence:
                evidence = recorded_decision_digests(raw_evidence)
                decision_names = {display for display, _ in decisions}
                if set(evidence) != decision_names:
                    changed_reasons.append(
                        "Decision Source SHA-256 paths differ from Applicable Decisions"
                    )
                for display_path, decision_path in decisions:
                    if display_path in evidence and evidence[display_path] not in compatible_text_digests(decision_path):
                        changed_reasons.append(
                            f"Decision Source SHA-256 changed: {display_path}"
                        )
            elif snapshot is not None:
                changed_reasons.append("Decision Source SHA-256 is missing")
        except AuthorityFailure as error:
            blocked_reasons.append(str(error))
        except (OSError, UnicodeError) as error:
            blocked_reasons.append(str(error))
        except ValueError as error:
            changed_reasons.append(str(error))

        if resolved_value and resolved_value.replace("\\", "/") != resolved_relative:
            changed_reasons.append("recorded Product Source path is stale")

    recorded_freshness = snapshot_fields.get("Freshness")
    if recorded_freshness == "blocked":
        changed_reasons.append("Snapshot Freshness records legacy blocked")
    elif recorded_freshness in {"refresh-required", "changed"}:
        changed_reasons.append("Snapshot Freshness records changed facts")
    elif recorded_freshness not in {None, "current"}:
        changed_reasons.append("Snapshot Freshness value is unsupported")

    if blocked_reasons:
        return ContextResult("blocked", tuple(sorted(set(blocked_reasons))))
    if changed_reasons:
        return ContextResult(
            "changed",
            tuple(sorted(set(changed_reasons))),
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
        "changed": "CHANGED",
        "blocked": "BLOCKED",
    }[result.status]
    print(f"{prefix}: {'; '.join(result.reasons)}")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
