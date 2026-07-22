from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path

try:
    from checker_support import CheckFailure, metadata, optional_section, read_text, table
except ModuleNotFoundError:  # package import used by unittest
    from scripts.checker_support import (
        CheckFailure,
        metadata,
        optional_section,
        read_text,
        table,
    )


CONCEPT_ID_PATTERN = re.compile(r"\bC-[A-Z0-9-]+\b")
MODEL_ID_PATTERN = re.compile(
    r"\b(?:REL|PERM|CMD|EVT|FLOW|STATE|PM|EX)-[A-Z0-9-]+\b"
)

VIEW_CONTRACTS: dict[str, tuple[str, re.Pattern[str] | None]] = {
    "Concepts": ("Concept Definitions", CONCEPT_ID_PATTERN),
    "Relationships": ("Concept Relationships", re.compile(r"\bREL-[A-Z0-9-]+\b")),
    "Permissions": ("Role / Permission Matrix", re.compile(r"\bPERM-[A-Z0-9-]+\b")),
    "Actions / Outcomes": ("Commands / Events", re.compile(r"\b(?:CMD|EVT)-[A-Z0-9-]+\b")),
    "Flow": ("Primary Business Flow", re.compile(r"\bFLOW-[A-Z0-9-]+\b")),
    "State": ("Product State Model", re.compile(r"\bSTATE-[A-Z0-9-]+\b")),
    "Product Facts": ("Requirement Product Model", re.compile(r"\bPM-[A-Z0-9-]+\b")),
    "Exceptions / Recovery": ("Exception Paths", re.compile(r"\bEX-[A-Z0-9-]+\b")),
    "Product Rules": ("Product Rules", None),
}

LEGACY_MODEL_TABLES: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    ("Concept Relationships", "Relationship ID", re.compile(r"REL-[A-Z0-9-]+")),
    ("Role / Permission Matrix", "Permission Rule ID", re.compile(r"PERM-[A-Z0-9-]+")),
    ("Commands / Events", "Action ID", re.compile(r"(?:CMD|EVT)-[A-Z0-9-]+")),
    ("Primary Business Flow", "Flow Step ID", re.compile(r"FLOW-[A-Z0-9-]+")),
    ("Product State Model", "State Model ID", re.compile(r"STATE-[A-Z0-9-]+")),
    ("Requirement Product Model", "Product Model ID", re.compile(r"PM-[A-Z0-9-]+")),
    ("Exception Paths", "Scenario ID", re.compile(r"EX-[A-Z0-9-]+")),
)

PLACEHOLDER = re.compile(
    r"^(?:-|none|n/a|na|not applicable|tbd|todo|unknown|pending)$", re.IGNORECASE
)
CONFIRMED_REVIEW_EVIDENCE = re.compile(r"^confirmed(?:\s|$)", re.IGNORECASE)


class ProductDefinitionError(ValueError):
    pass


@dataclass(frozen=True)
class EffectiveProductSource:
    path: Path
    content: str
    kind: str
    profile: str | None
    review: str
    legacy: bool
    concept_ids: frozenset[str]
    model_ids: frozenset[str]


def normalized(value: str | None) -> str:
    text = (value or "").strip()
    if len(text) >= 2 and text[0] == text[-1] == "`":
        return text[1:-1].strip()
    return text


def is_confirmed_review_evidence(value: str | None) -> bool:
    return CONFIRMED_REVIEW_EVIDENCE.match(normalized(value)) is not None


def concrete_reason(value: str | None) -> bool:
    text = normalized(value)
    return (
        len(text) >= 12
        and not PLACEHOLDER.fullmatch(text)
        and re.search(r"<[^>]+>", text) is None
    )


def _assert_unique(values: list[str], context: str) -> None:
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise ProductDefinitionError(
            f"duplicate IDs in {context}: {', '.join(duplicates)}"
        )


def _reference_path(requirement_root: Path, value: str) -> Path:
    normalized_value = normalized(value).replace("\\", "/")
    candidate = Path(normalized_value)
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (requirement_root / candidate).resolve()
    try:
        resolved.relative_to(requirement_root.resolve())
    except ValueError as error:
        raise ProductDefinitionError(
            f"reference escapes Requirement Set: {value}"
        ) from error
    return resolved


def _review_date(value: str | None, context: str) -> str:
    text = normalized(value)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise ProductDefinitionError(f"{context} must be YYYY-MM-DD")
    try:
        parsed = date.fromisoformat(text)
    except ValueError as error:
        raise ProductDefinitionError(f"{context} must be YYYY-MM-DD") from error
    if parsed > date.today():
        raise ProductDefinitionError(f"{context} cannot be in the future")
    return text


def _legacy_inventory(content: str) -> tuple[set[str], set[str]]:
    try:
        concept_values = [
            row.get("Concept ID", "") for row in table(content, "Concept Definitions")
        ]
        _assert_unique(concept_values, "source Concept Definitions")
        if not concept_values or not all(
            CONCEPT_ID_PATTERN.fullmatch(value) for value in concept_values
        ):
            raise ProductDefinitionError(
                "source Concept Definitions contains invalid IDs"
            )

        model_values: list[str] = []
        for heading, column, pattern in LEGACY_MODEL_TABLES:
            values = [row.get(column, "") for row in table(content, heading)]
            _assert_unique(values, f"source {heading}")
            if not values or not all(pattern.fullmatch(value) for value in values):
                raise ProductDefinitionError(f"source {heading} contains invalid IDs")
            model_values.extend(values)
        _assert_unique(model_values, "accepted Requirement Model")
    except CheckFailure as error:
        raise ProductDefinitionError(str(error)) from error
    return set(concept_values), set(model_values)


def _heading_anchor(heading: str) -> str:
    anchor = re.sub(r"[^a-z0-9 -]", "", heading.lower())
    return re.sub(r"[ -]+", "-", anchor).strip("-")


def _new_standard_inventory(content: str) -> tuple[set[str], set[str]]:
    try:
        rows = table(content, "Product View Applicability")
    except CheckFailure as error:
        raise ProductDefinitionError(str(error)) from error

    names = [row.get("View", "") for row in rows]
    _assert_unique(names, "Product View Applicability")
    expected = set(VIEW_CONTRACTS)
    actual = set(names)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise ProductDefinitionError(
            "Product View Applicability mismatch; "
            f"missing={', '.join(missing)} extra={', '.join(extra)}"
        )

    concepts: set[str] = set()
    models: set[str] = set()
    for row in rows:
        view = row.get("View", "")
        applicability = row.get("Applicability", "")
        reason = row.get("Reason / Evidence", "")
        section_ref = normalized(row.get("Section / Stable IDs", ""))
        heading, pattern = VIEW_CONTRACTS[view]

        if applicability not in {"included", "not-applicable"}:
            raise ProductDefinitionError(
                f"unsupported applicability for {view}: {applicability or 'missing'}"
            )
        if applicability == "not-applicable":
            if not concrete_reason(reason):
                raise ProductDefinitionError(
                    f"not-applicable view requires a concrete reason: {view}"
                )
            if section_ref.lower() not in {"none", "not-applicable"}:
                raise ProductDefinitionError(
                    f"not-applicable view must not declare section or stable IDs: {view}"
                )
            continue

        if not concrete_reason(reason):
            raise ProductDefinitionError(
                f"included view requires concrete evidence: {view}"
            )
        section_content = optional_section(content, heading)
        if section_content is None:
            raise ProductDefinitionError(f"included view {view} is missing section")
        if heading not in section_ref:
            raise ProductDefinitionError(
                f"included view {view} does not reference section {heading}"
            )

        if pattern is None:
            anchors = re.findall(r"product\.md#([a-z0-9-]+)", section_ref)
            headings = re.findall(r"^###\s+(.+?)\s*$", section_content, re.MULTILINE)
            known_anchors = {_heading_anchor(value) for value in headings}
            if not anchors or not set(anchors).issubset(known_anchors):
                raise ProductDefinitionError(
                    "included view Product Rules requires resolvable product.md anchors"
                )
            continue

        listed = set(pattern.findall(section_ref))
        defined = set(pattern.findall(section_content))
        if not listed or not defined:
            raise ProductDefinitionError(
                f"included view {view} requires section and stable IDs"
            )
        if listed != defined:
            raise ProductDefinitionError(
                f"included view {view} stable IDs do not match its section"
            )
        if view == "Concepts":
            concepts.update(defined)
        else:
            models.update(defined)

    return concepts, models


def product_model_inventory(source: EffectiveProductSource) -> tuple[set[str], set[str]]:
    """Return accepted concept/model IDs; new views follow applicability."""

    return set(source.concept_ids), set(source.model_ids)


def product_rule_references(source: EffectiveProductSource) -> set[str]:
    """Return accepted Product Rule section anchors for a new Standard source."""

    if source.legacy or source.profile != "standard":
        return set()
    try:
        applicability = next(
            row.get("Applicability", "")
            for row in table(source.content, "Product View Applicability")
            if row.get("View", "") == "Product Rules"
        )
    except (CheckFailure, StopIteration):
        return set()
    if applicability != "included":
        return set()
    rules = optional_section(source.content, "Product Rules")
    if rules is None:
        return set()
    headings = re.findall(r"^###\s+(.+?)\s*$", rules, re.MULTILINE)
    return {f"product.md#{_heading_anchor(heading)}" for heading in headings}


def _inventory(
    content: str, *, legacy: bool, profile: str | None, review: str
) -> tuple[set[str], set[str]]:
    if legacy:
        if review == "concept-foundation-not-needed":
            return set(), set()
        return _legacy_inventory(content)
    if profile == "brief":
        return set(), set()
    return _new_standard_inventory(content)


def resolve_effective_product_definition(
    readme_path: Path,
    supplied_source_path: Path,
) -> EffectiveProductSource:
    """Resolve exactly one new or legacy reviewed product source."""

    if not readme_path.is_file():
        raise ProductDefinitionError(f"missing file: {readme_path}")
    if not supplied_source_path.is_file():
        raise ProductDefinitionError(f"missing file: {supplied_source_path}")

    readme = read_text(readme_path)
    content = read_text(supplied_source_path)
    new_pointer = optional_section(readme, "Effective Product Definition")
    legacy_pointer = optional_section(readme, "Effective Concept Foundation")
    if new_pointer is not None and legacy_pointer is not None:
        raise ProductDefinitionError("multiple effective product source pointers")
    if new_pointer is None and legacy_pointer is None:
        raise ProductDefinitionError("missing effective product source pointer")

    requirement_root = readme_path.parent.resolve()
    try:
        supplied_source_path.resolve().relative_to(requirement_root)
    except ValueError as error:
        raise ProductDefinitionError(
            f"supplied source escapes Requirement Set: {supplied_source_path}"
        ) from error

    if new_pointer is not None:
        pointer_source = metadata(new_pointer, "Source")
        if not normalized(pointer_source):
            raise ProductDefinitionError("effective product source pointer is missing")
        resolved = _reference_path(requirement_root, str(pointer_source))
        if resolved != supplied_source_path.resolve():
            raise ProductDefinitionError(
                "effective product source pointer does not resolve to supplied source"
            )

        pointer_profile = normalized(metadata(new_pointer, "Profile"))
        source_profile = normalized(metadata(content, "Product Definition Profile"))
        candidate_profile = source_profile or pointer_profile
        if candidate_profile not in {"brief", "standard"}:
            raise ProductDefinitionError(
                "unsupported Product Definition Profile: "
                f"{candidate_profile or 'missing'}"
            )
        if pointer_profile != source_profile:
            raise ProductDefinitionError("Product Definition Profile metadata mismatch")

        pointer_review = normalized(metadata(new_pointer, "Product Review"))
        source_review = normalized(metadata(content, "Product Review"))
        if pointer_review != "confirmed" or source_review != "confirmed":
            raise ProductDefinitionError("Product Review must be confirmed")
        if pointer_review != source_review:
            raise ProductDefinitionError("Product Review metadata mismatch")

        review_evidence = optional_section(content, "Product Human Review Evidence")
        if review_evidence is None or normalized(
            metadata(review_evidence, "Decision")
        ) != "confirmed":
            raise ProductDefinitionError(
                "Product Human Review Evidence must record Decision: confirmed"
            )
        source_confirmed_at = _review_date(
            metadata(review_evidence, "Confirmed At"),
            "Product Human Review Confirmed At",
        )
        pointer_confirmed_at = _review_date(
            metadata(new_pointer, "Last Confirmed"),
            "Effective Product Definition Last Confirmed",
        )
        if pointer_confirmed_at != source_confirmed_at:
            raise ProductDefinitionError(
                "Last Confirmed must match Product Human Review Confirmed At"
            )

        previous_source = normalized(metadata(new_pointer, "Previous Source"))
        if not previous_source:
            raise ProductDefinitionError(
                "Effective Product Definition Previous Source is missing"
            )
        if previous_source.lower() != "none":
            previous_path = _reference_path(requirement_root, previous_source)
            if previous_path == supplied_source_path.resolve():
                raise ProductDefinitionError(
                    "Previous Source must not resolve to the current Product Definition"
                )
            if not previous_path.is_file():
                raise ProductDefinitionError(
                    f"Previous Source does not exist: {previous_source}"
                )

        concepts, models = _inventory(
            content,
            legacy=False,
            profile=source_profile,
            review=source_review,
        )
        return EffectiveProductSource(
            path=supplied_source_path.resolve(),
            content=content,
            kind="product-definition",
            profile=source_profile,
            review=source_review,
            legacy=False,
            concept_ids=frozenset(concepts),
            model_ids=frozenset(models),
        )

    pointer_status = normalized(metadata(legacy_pointer or "", "Status"))
    pointer_source = metadata(legacy_pointer or "", "Effective Source")
    if not normalized(pointer_source):
        raise ProductDefinitionError("legacy effective source pointer is missing")
    resolved = _reference_path(requirement_root, str(pointer_source))
    if resolved != supplied_source_path.resolve():
        raise ProductDefinitionError(
            "effective product source pointer does not resolve to supplied source"
        )
    source_status = normalized(metadata(content, "Concept Foundation Status"))
    if (
        pointer_status not in {"accepted", "concept-foundation-not-needed"}
        or source_status != pointer_status
    ):
        raise ProductDefinitionError(
            "legacy effective Concept Foundation must be accepted or reasoned not-needed"
        )
    if source_status == "concept-foundation-not-needed" and not concrete_reason(
        metadata(content, "Not-Needed Reason")
    ):
        raise ProductDefinitionError(
            "concept-foundation-not-needed requires a concrete reason"
        )
    concepts, models = _inventory(
        content,
        legacy=True,
        profile=None,
        review=source_status,
    )
    return EffectiveProductSource(
        path=supplied_source_path.resolve(),
        content=content,
        kind="concept-foundation",
        profile=None,
        review=source_status,
        legacy=True,
        concept_ids=frozenset(concepts),
        model_ids=frozenset(models),
    )


def product_semantic_sha256(content: str) -> str:
    """Hash semantic content excluding Derived Visuals and Human Review Evidence."""

    normalized_content = content.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    for heading in ("Derived Visuals", "Product Human Review Evidence"):
        normalized_content = re.sub(
            rf"^##\s+{re.escape(heading)}\s*$\n.*?(?=^#{{1,2}}\s+|\Z)",
            "",
            normalized_content,
            flags=re.MULTILINE | re.DOTALL,
        )
    canonical = "\n".join(line.rstrip() for line in normalized_content.splitlines()).strip()
    return hashlib.sha256((canonical + "\n").encode("utf-8")).hexdigest()
