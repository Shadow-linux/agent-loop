#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from checker_support import (
    CheckFailure,
    metadata,
    optional_section,
    read_text,
    require_supported_python,
    section,
    table,
)
from requirement_product_support import (
    CONCEPT_ID_PATTERN,
    MODEL_ID_PATTERN,
    EffectiveProductSource,
    ProductDefinitionError,
    concrete_reason,
    is_confirmed_review_evidence,
    normalized,
    product_semantic_sha256,
    resolve_effective_product_definition,
)
from visual_artifact_support import VisualArtifactError, validate_durable_visual


BRIEF_SECTIONS = (
    "Problem / Background",
    "Target User / Scenario",
    "Goal / Expected Product Outcome",
    "In Scope",
    "Out Of Scope / Non-goals",
    "Acceptance Direction",
    "Source Evidence",
    "Open Questions / Remaining Risk",
    "Product Human Review Evidence",
)

STANDARD_ONLY_SECTIONS = (
    "Product Capability Scope",
    "User Segments / Roles / Scenarios",
    "Product View Applicability",
    "Concept Definitions",
    "Concept Relationships",
    "Role / Permission Matrix",
    "Commands / Events",
    "Primary Business Flow",
    "Product State Model",
    "Requirement Product Model",
    "Exception Paths",
    "Product Rules",
    "Experience / Operations / Measurement",
)

ALLOWED_VISUAL_TYPES = {
    "workflow",
    "lifecycle",
    "sequence",
    "relationship",
    "equivalent",
}

LEGACY_VISUAL_COLUMNS = {
    "Path",
    "Type",
    "Source IDs",
    "Product Semantic SHA-256",
    "Status",
    "Human Confirmed",
}

SOURCE_RENDER_VISUAL_COLUMNS = {
    "Diagram ID",
    "Source Definition",
    "Render",
    "Type",
    "Source IDs",
    "Product Semantic SHA-256",
    "Source SHA-256",
    "Render SHA-256",
    "Generator",
    "Validation Evidence",
    "Status",
    "Human Confirmed",
}


class DefinitionCheckError(ValueError):
    pass


def _concrete(value: str | None, *, allow_none: bool = False) -> bool:
    text = normalized(value)
    if allow_none and text.lower() == "none":
        return True
    return concrete_reason(text)


def _parse_date(value: str | None, context: str) -> date:
    text = normalized(value)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise DefinitionCheckError(f"{context} must be YYYY-MM-DD")
    try:
        parsed = date.fromisoformat(text)
    except ValueError as error:
        raise DefinitionCheckError(f"{context} must be YYYY-MM-DD") from error
    if parsed > date.today():
        raise DefinitionCheckError(f"{context} cannot be in the future")
    return parsed


def _assert_unique(values: list[str], context: str) -> None:
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise DefinitionCheckError(
            f"duplicate values in {context}: {', '.join(duplicates)}"
        )


def _anchor(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9 -]", "", value.lower())
    return re.sub(r"[ -]+", "-", cleaned).strip("-")


def validate_product_profile(source: EffectiveProductSource) -> None:
    if source.legacy:
        return
    for heading in BRIEF_SECTIONS:
        if optional_section(source.content, heading) is None:
            raise DefinitionCheckError(f"missing section: ## {heading}")

    if source.profile != "brief":
        return
    inflated = [
        heading
        for heading in STANDARD_ONLY_SECTIONS
        if optional_section(source.content, heading) is not None
    ]
    if inflated:
        raise DefinitionCheckError(
            "brief product definition contains Standard-only product-model views"
        )


def validate_human_review(content: str) -> None:
    review = section(content, "Product Human Review Evidence")
    if metadata(review, "Decision") != "confirmed":
        raise DefinitionCheckError("Product Review must be confirmed")
    if not _concrete(metadata(review, "Confirmed By")):
        raise DefinitionCheckError("Product Human Review must record who confirmed it")
    _parse_date(metadata(review, "Confirmed At"), "Product Human Review Confirmed At")
    if not _concrete(metadata(review, "Evidence")):
        raise DefinitionCheckError("Product Human Review requires concrete evidence")
    implementation = metadata(review, "Implementation Authorized")
    if implementation not in {"no", "separately-confirmed"}:
        raise DefinitionCheckError(
            "Implementation Authorized must be no or separately-confirmed"
        )


def _assert_visual_columns(
    rows: list[dict[str, str]], expected: set[str], context: str
) -> None:
    actual = set(rows[0])
    if actual != expected:
        missing = ", ".join(sorted(expected - actual)) or "none"
        extra = ", ".join(sorted(actual - expected)) or "none"
        raise DefinitionCheckError(
            f"{context} columns mismatch; missing={missing} extra={extra}"
        )


def validate_legacy_visual_manifest(
    source: EffectiveProductSource, rows: list[dict[str, str]]
) -> None:
    _assert_visual_columns(rows, LEGACY_VISUAL_COLUMNS, "legacy visual")
    paths = [normalized(row.get("Path")) for row in rows]
    _assert_unique(paths, "Derived Visuals Path")
    semantic_digest = product_semantic_sha256(source.content)
    known_ids = set(source.concept_ids) | set(source.model_ids)
    for row in rows:
        path = normalized(row.get("Path"))
        if not path or path.startswith("/") or ".." in Path(path.replace("\\", "/")).parts:
            raise DefinitionCheckError("derived visual path must stay inside Requirement Set")
        visual_type = normalized(row.get("Type"))
        if visual_type not in ALLOWED_VISUAL_TYPES:
            raise DefinitionCheckError(f"unsupported derived visual type: {visual_type}")
        source_ids = set(CONCEPT_ID_PATTERN.findall(row.get("Source IDs", "")))
        source_ids.update(MODEL_ID_PATTERN.findall(row.get("Source IDs", "")))
        if not source_ids:
            raise DefinitionCheckError("derived visual must name source IDs")
        unknown = source_ids - known_ids
        if unknown:
            raise DefinitionCheckError(
                "derived visual contains unknown source IDs: "
                + ", ".join(sorted(unknown))
            )
        digest = normalized(row.get("Product Semantic SHA-256"))
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise DefinitionCheckError("derived visual digest must be 64 lowercase hex")
        if digest != semantic_digest:
            raise DefinitionCheckError("derived visual digest is stale")
        if normalized(row.get("Status")) != "current":
            raise DefinitionCheckError("derived visual status must be current")
        if not _concrete(row.get("Human Confirmed")):
            raise DefinitionCheckError(
                "derived visual requires concrete Human Confirmed evidence"
            )


def validate_source_render_visual_manifest(
    source: EffectiveProductSource, rows: list[dict[str, str]]
) -> None:
    _assert_visual_columns(
        rows, SOURCE_RENDER_VISUAL_COLUMNS, "source-render-v1"
    )
    diagram_ids = [normalized(row.get("Diagram ID")) for row in rows]
    source_paths = [normalized(row.get("Source Definition")) for row in rows]
    render_paths = [normalized(row.get("Render")) for row in rows]
    _assert_unique(diagram_ids, "Derived Visuals Diagram ID")
    _assert_unique(source_paths, "Derived Visuals Source Definition")
    _assert_unique(render_paths, "Derived Visuals Render")

    semantic_digest = product_semantic_sha256(source.content)
    known_ids = set(source.concept_ids) | set(source.model_ids)
    for row in rows:
        source_ids = set(CONCEPT_ID_PATTERN.findall(row.get("Source IDs", "")))
        source_ids.update(MODEL_ID_PATTERN.findall(row.get("Source IDs", "")))
        if not source_ids:
            raise DefinitionCheckError("derived visual must name source IDs")
        unknown = source_ids - known_ids
        if unknown:
            raise DefinitionCheckError(
                "derived visual contains unknown source IDs: "
                + ", ".join(sorted(unknown))
            )
        if normalized(row.get("Product Semantic SHA-256")) != semantic_digest:
            raise DefinitionCheckError("derived visual digest is stale")
        if normalized(row.get("Status")) != "current":
            raise DefinitionCheckError("derived visual status must be current")
        if not _concrete(row.get("Human Confirmed")):
            raise DefinitionCheckError(
                "derived visual requires concrete Human Confirmed evidence"
            )
        try:
            validate_durable_visual(
                source.path.parent,
                diagram_id=row.get("Diagram ID", ""),
                source_definition=row.get("Source Definition", ""),
                render=row.get("Render", ""),
                diagram_type=row.get("Type", ""),
                source_sha256=row.get("Source SHA-256", ""),
                render_sha256=row.get("Render SHA-256", ""),
                generator=row.get("Generator", ""),
                validation_evidence=row.get("Validation Evidence", ""),
            )
        except VisualArtifactError as error:
            raise DefinitionCheckError(str(error)) from error


def validate_visual_manifest(source: EffectiveProductSource) -> None:
    visual_section = optional_section(source.content, "Derived Visuals")
    if visual_section is None:
        return
    rows = table(source.content, "Derived Visuals")
    contract = normalized(metadata(visual_section, "Visual Manifest Contract"))
    if not contract:
        validate_legacy_visual_manifest(source, rows)
        return
    if contract != "source-render-v1":
        raise DefinitionCheckError(f"unsupported Visual Manifest Contract: {contract}")
    validate_source_render_visual_manifest(source, rows)


def validate_product_slice(source: EffectiveProductSource, spec: str) -> None:
    product_source = section(spec, "Product Requirement Source")
    requirement_set = normalized(metadata(product_source, "Requirement Set")).replace(
        "\\", "/"
    )
    if not _concrete(requirement_set) or len(Path(requirement_set).parts) < 2:
        raise DefinitionCheckError("Product Requirement Source requires Requirement Set")
    if normalized(metadata(product_source, "Effective Product Definition")).replace(
        "\\", "/"
    ) != source.path.name:
        raise DefinitionCheckError(
            "Feature Effective Product Definition does not match supplied source"
        )
    if metadata(product_source, "Product Definition Profile") != source.profile:
        raise DefinitionCheckError("Feature Product Definition Profile mismatch")
    if not is_confirmed_review_evidence(
        metadata(product_source, "Product Review Evidence")
    ):
        raise DefinitionCheckError("Feature Product Review Evidence must be confirmed")
    if not normalized(metadata(product_source, "Applicable Decisions")):
        raise DefinitionCheckError("Product Requirement Source requires Applicable Decisions")

    rows = table(spec, "Product Slice")
    allowed_coverage = {"in-scope", "out-of-scope", "not-applicable"}
    known_ids = set(source.concept_ids) | set(source.model_ids)
    source_headings = {
        _anchor(value)
        for value in re.findall(r"^#{2,3}\s+(.+?)\s*$", source.content, re.MULTILINE)
    }
    referenced_ids: set[str] = set()
    for row in rows:
        ref = row.get("Source Section / Model ID", "")
        row_ids = set(CONCEPT_ID_PATTERN.findall(ref))
        row_ids.update(MODEL_ID_PATTERN.findall(ref))
        referenced_ids.update(row_ids)
        anchors = re.findall(r"product\.md#([a-z0-9-]+)", ref)
        unknown_anchors = set(anchors) - source_headings
        if unknown_anchors:
            raise DefinitionCheckError(
                "Product Slice contains unknown source anchors: "
                + ", ".join(sorted(unknown_anchors))
            )
        if not row_ids and not anchors:
            raise DefinitionCheckError(
                "Product Slice row must reference a source ID or product.md anchor"
            )
        if not _concrete(row.get("Feature Responsibility")):
            raise DefinitionCheckError("Product Slice requires Feature Responsibility")
        if not _concrete(row.get("Acceptance Mapping")):
            raise DefinitionCheckError("Product Slice requires Acceptance Mapping")
        coverage = normalized(row.get("Coverage"))
        if coverage not in allowed_coverage:
            raise DefinitionCheckError(f"unsupported Product Slice coverage: {coverage}")
    unknown_ids = referenced_ids - known_ids
    if unknown_ids:
        raise DefinitionCheckError(
            "Product Slice contains unknown source IDs: "
            + ", ".join(sorted(unknown_ids))
        )


def validate_legacy_product_source(
    source: EffectiveProductSource, spec_path: Path | None
) -> str:
    if spec_path is not None and not spec_path.is_file():
        raise DefinitionCheckError(f"missing file: {spec_path}")
    return f"PASS: reviewed legacy {source.kind} product source is valid"


def validate(readme_path: Path, source_path: Path, spec_path: Path | None) -> str:
    source = resolve_effective_product_definition(readme_path, source_path)
    if source.legacy:
        return validate_legacy_product_source(source, spec_path)
    validate_product_profile(source)
    validate_human_review(source.content)
    validate_visual_manifest(source)
    if spec_path is not None:
        validate_product_slice(source, read_text(spec_path))
    return f"PASS: confirmed {source.profile} product definition is valid"


def main() -> int:
    require_supported_python()
    parser = argparse.ArgumentParser(
        description="Validate one effective Requirement Product Definition and optional Product Slice."
    )
    parser.add_argument("requirement_readme", type=Path)
    parser.add_argument("effective_product_source", type=Path)
    parser.add_argument("feature_spec", nargs="?", type=Path)
    args = parser.parse_args()
    required = (args.requirement_readme, args.effective_product_source)
    for path in required:
        if not path.is_file():
            parser.error(f"missing file: {path}")
    if args.feature_spec is not None and not args.feature_spec.is_file():
        parser.error(f"missing file: {args.feature_spec}")
    try:
        print(validate(*required, args.feature_spec))
    except (DefinitionCheckError, ProductDefinitionError, CheckFailure) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
