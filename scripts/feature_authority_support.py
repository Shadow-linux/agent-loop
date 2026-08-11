from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from checker_support import (
    CheckFailure,
    discover_memory_root_authority,
    optional_section,
    read_text,
)
from feature_archive_support import ArchiveContractError, resolve_feature_location


REQUIREMENT_ADAPTER = "requirement-product-definition"
BUG_ADAPTER = "bug"
HUMAN_ADAPTER = "human"
FEATURE_ADAPTER = "feature"
CUSTOM_ADAPTER = "custom"


class AuthorityResolutionError(ValueError):
    """Objective ambiguity that prevents selecting one Feature authority."""


@dataclass(frozen=True)
class AuthorityShape:
    authority_type: str
    adapter: str
    explicit: bool
    compatibility_shape: str


@dataclass(frozen=True)
class AuthorityResolution:
    authority_type: str
    adapter: str
    primary_reference: str
    supporting_references: tuple[str, ...]
    compatibility_shape: str
    applicability: str
    status: str
    facts: tuple[str, ...]
    reasons: tuple[str, ...]


def _field(text: str, name: str) -> str:
    match = re.search(
        rf"(?mi)^\s*(?:-\s*)?{re.escape(name)}\s*:\s*(.*?)\s*$",
        text,
    )
    return match.group(1).strip() if match else ""


def _fields(text: str, name: str) -> tuple[str, ...]:
    return tuple(
        match.strip()
        for match in re.findall(
            rf"(?mi)^\s*(?:-\s*)?{re.escape(name)}\s*:\s*(.*?)\s*$",
            text,
        )
    )


def _clean_reference(value: str) -> str:
    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] == "`":
        cleaned = cleaned[1:-1].strip()
    return cleaned


def _authority_sections(spec_text: str) -> list[str]:
    matches = list(
        re.finditer(r"(?m)^##\s+Feature Authority\s*$", spec_text)
    )
    sections: list[str] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(spec_text)
        next_heading = re.search(r"(?m)^#{1,2}\s+", spec_text[start:end])
        if next_heading:
            end = start + next_heading.start()
        sections.append(spec_text[start:end])
    return sections


def authority_shape(spec_text: str) -> AuthorityShape:
    sections = _authority_sections(spec_text)
    if len(sections) > 1:
        raise AuthorityResolutionError(
            "multiple Feature Authority blocks create contradictory primary authority pointers"
        )
    product_source = optional_section(spec_text, "Product Requirement Source")
    if not sections:
        if product_source is not None:
            return AuthorityShape(
                authority_type="Requirement Product Definition (legacy Product Requirement Source)",
                adapter=REQUIREMENT_ADAPTER,
                explicit=False,
                compatibility_shape="legacy-product-requirement-source",
            )
        raise AuthorityResolutionError(
            "Feature spec has no Feature Authority or compatible Product Requirement Source"
        )

    authority_types = _fields(sections[0], "Authority Type")
    if len(authority_types) > 1:
        raise AuthorityResolutionError(
            "multiple Feature Authority Type fields create ambiguous adapter evidence"
        )
    primary_references = _fields(sections[0], "Primary Authority Reference")
    if len(primary_references) > 1:
        raise AuthorityResolutionError(
            "multiple Primary Authority Reference fields create contradictory primary authority pointers"
        )
    authority_type = authority_types[0] if authority_types else ""
    if not authority_type:
        raise AuthorityResolutionError("Feature Authority Type is missing")
    lowered = authority_type.casefold()
    if re.search(r"\brequirement product definition\b", lowered):
        adapter = REQUIREMENT_ADAPTER
    elif re.search(r"\bbug\b", lowered):
        adapter = BUG_ADAPTER
    elif re.search(r"\bhuman\b", lowered):
        adapter = HUMAN_ADAPTER
    elif re.search(r"\bfeature authority\b", lowered):
        adapter = FEATURE_ADAPTER
    else:
        adapter = CUSTOM_ADAPTER
    return AuthorityShape(
        authority_type=authority_type,
        adapter=adapter,
        explicit=True,
        compatibility_shape="explicit-feature-authority",
    )


def requirement_product_applicability(spec_text: str) -> tuple[bool, str]:
    """Return whether a Requirement/Product-specific Checker owns this Feature."""

    try:
        shape = authority_shape(spec_text)
    except AuthorityResolutionError as error:
        if str(error) == (
            "Feature spec has no Feature Authority or compatible "
            "Product Requirement Source"
        ):
            # Older specialized-checker fixtures may omit the handoff section.
            # Absence is not evidence that another adapter owns the artifact;
            # preserve the specialized validation and its original diagnostics.
            return True, "no explicit non-Requirement authority is declared"
        raise
    if shape.adapter == REQUIREMENT_ADAPTER:
        return True, f"{shape.authority_type} uses the Requirement Product Definition sub-adapter"
    return (
        False,
        f"{shape.authority_type} uses the {shape.adapter} adapter, not Requirement Product Definition",
    )


def _split_supporting(value: str) -> tuple[tuple[str, ...], bool]:
    cleaned = value.strip()
    if not cleaned or cleaned.casefold() == "none":
        return (), False
    references = tuple(
        _clean_reference(item) for item in cleaned.split(";") if item.strip()
    )
    if not references:
        return (), False
    duplicate = len(references) != len(set(references))
    return tuple(dict.fromkeys(references)), duplicate


def is_external_locator(value: str, adapter: str) -> bool:
    if re.match(r"^[A-Za-z]:[\\/]", value):
        return False
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return True
    if re.fullmatch(
        r"[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*-\d+",
        value,
    ):
        return True
    if adapter == HUMAN_ADAPTER:
        normalized = value.replace("\\", "/")
        return not (
            normalized.startswith(".")
            or "/" in normalized
            or normalized.casefold().endswith((".md", ".txt", ".json"))
        )
    return False


def _local_authority_path(
    project_root: Path,
    reference: str,
    *,
    required: bool,
) -> tuple[Path | None, str | None]:
    cleaned = _clean_reference(reference).replace("\\", "/")
    if not cleaned or cleaned.casefold() == "none":
        if required:
            raise AuthorityResolutionError(
                "declared local primary authority reference is missing"
            )
        return None, "supporting authority reference is empty"
    if cleaned.startswith("/") or re.match(r"^[A-Za-z]:/", cleaned):
        raise AuthorityResolutionError(
            f"authority path must be project-root-relative: {reference}"
        )
    candidate = Path(cleaned)
    resolved = (project_root / candidate).resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError as error:
        raise AuthorityResolutionError(
            f"authority path escapes project root: {reference}"
        ) from error
    if not resolved.is_file():
        message = f"declared local authority is missing or unreadable: {reference}"
        if required:
            raise AuthorityResolutionError(message)
        return resolved, message
    try:
        read_text(resolved)
    except (OSError, UnicodeError) as error:
        message = f"declared local authority is unreadable: {reference}: {error}"
        if required:
            raise AuthorityResolutionError(message) from error
        return resolved, message
    return resolved, None


def _concrete(value: str) -> bool:
    cleaned = value.strip()
    return bool(cleaned) and not re.fullmatch(
        r"(?:-|none|n/a|na|not applicable|unknown|pending|unresolved)",
        cleaned,
        re.IGNORECASE,
    )


def _feature_reference(project_root: Path, feature_spec: Path) -> str:
    try:
        authority = discover_memory_root_authority(project_root)
    except CheckFailure as error:
        raise AuthorityResolutionError(error.detail) from error
    if authority is None:
        raise AuthorityResolutionError("no accepted memory root for Feature locator")
    try:
        feature_relative = feature_spec.resolve().relative_to(authority.resolved)
        logical_root = authority.logical.relative_to(project_root.resolve())
    except ValueError as error:
        raise AuthorityResolutionError(
            "current Feature is outside the accepted logical memory root"
        ) from error
    return (logical_root / feature_relative).as_posix()


def _same_feature_locator(recorded: str, feature_reference: str) -> bool:
    cleaned = _clean_reference(recorded).replace("\\", "/").rstrip("/")
    expected = feature_reference.rstrip("/")
    return cleaned in {expected, expected.removesuffix("/spec.md")}


def _bug_facts(
    project_root: Path,
    feature_spec: Path,
    bug_path: Path,
) -> tuple[list[str], list[str], list[str]]:
    facts: list[str] = []
    changed: list[str] = []
    blocked: list[str] = []
    content = read_text(bug_path)
    bug_id = _field(content, "Bug ID")
    if _concrete(bug_id):
        facts.append(f"Bug ID {bug_id}")
    else:
        changed.append("Bug Authority is missing a concrete Bug ID")

    expected_section = optional_section(content, "Expected Behavior") or ""
    expected_evidence = _field(expected_section, "Expected Behavior Evidence")
    if _concrete(expected_evidence):
        facts.append(f"Expected Behavior evidence {expected_evidence}")
    else:
        changed.append("Bug Authority lacks accepted Expected Behavior evidence")

    resolution_section = optional_section(content, "Resolution Path") or ""
    resolution_path = _field(resolution_section, "Path")
    target = _field(resolution_section, "Target")
    human_decision = _field(resolution_section, "Human Decision")
    decision_evidence = _field(resolution_section, "Decision Evidence")
    if resolution_path not in {"flow-back", "linked-feature", "maintenance-fix"}:
        changed.append(
            "Bug Authority has no repair Resolution Path for Feature execution"
        )
    else:
        facts.append(f"Resolution Path {resolution_path}")
    if human_decision.casefold() not in {"confirmed", "accepted"} or not _concrete(
        decision_evidence
    ):
        changed.append("Bug Authority Resolution Path lacks confirmed Human evidence")

    close_section = optional_section(content, "Verification And Close") or ""
    fix_feature = _field(close_section, "Fix Feature")
    locators = [value for value in (target, fix_feature) if _concrete(value)]
    if not locators:
        changed.append("Bug Authority lacks a Fix Feature locator")
    elif len({_clean_reference(value) for value in locators}) > 1:
        blocked.append("Bug Authority has contradictory current Fix Feature pointers")

    try:
        feature_reference = _feature_reference(project_root, feature_spec)
        authority = discover_memory_root_authority(project_root)
        if authority is None:
            raise AuthorityResolutionError("no accepted memory root for Bug Feature")
        relative = feature_spec.resolve().relative_to(authority.resolved)
        if len(relative.parts) < 3 or relative.parts[0] != "features":
            raise AuthorityResolutionError(
                "current Bug Feature is outside the memory-root features directory"
            )
        feature_id = relative.parent.name
        location = resolve_feature_location(authority.logical, feature_id)
        logical_root = authority.logical.relative_to(project_root.resolve())
        expected_reference = (
            logical_root / location.relative_path / feature_spec.name
        ).as_posix()
        if expected_reference != feature_reference:
            raise AuthorityResolutionError(
                "Feature archive locator does not match the current Bug Feature path"
            )
    except (ArchiveContractError, AuthorityResolutionError, CheckFailure, ValueError) as error:
        blocked.append(f"Bug Fix Feature locator is unsafe: {error}")
        feature_reference = _feature_reference(project_root, feature_spec)
        location = None
    if locators:
        if all(_same_feature_locator(value, feature_reference) for value in locators):
            facts.append(f"Fix Feature {feature_reference}")
        else:
            changed.append(
                f"Bug Fix Feature locator does not name current Feature {feature_reference}"
            )

    if location is not None and location.layout == "archived":
        facts.append(f"Feature Location archived:{location.month}")
    elif location is not None:
        facts.append("Feature Location flat")
    return facts, changed, blocked


def resolve_feature_authority(
    project_root: Path,
    feature_spec: Path,
    spec_text: str,
) -> AuthorityResolution:
    try:
        shape = authority_shape(spec_text)
    except AuthorityResolutionError as error:
        return AuthorityResolution(
            authority_type="unresolved",
            adapter=CUSTOM_ADAPTER,
            primary_reference="",
            supporting_references=(),
            compatibility_shape="unresolved",
            applicability="unresolved",
            status="blocked",
            facts=(),
            reasons=(str(error),),
        )

    if not shape.explicit:
        return AuthorityResolution(
            authority_type=shape.authority_type,
            adapter=shape.adapter,
            primary_reference="",
            supporting_references=(),
            compatibility_shape=shape.compatibility_shape,
            applicability="applicable",
            status="current",
            facts=("legacy Product Requirement Source compatibility adapter",),
            reasons=(),
        )

    section = _authority_sections(spec_text)[0]
    primary = _clean_reference(_field(section, "Primary Authority Reference"))
    summary = _field(section, "Authority Summary")
    assessment = _field(section, "Agent Authority Assessment").casefold()
    try:
        supporting, duplicate_supporting = _split_supporting(
            _field(section, "Supporting Authority References")
        )
    except AuthorityResolutionError as error:
        return AuthorityResolution(
            shape.authority_type,
            shape.adapter,
            primary,
            (),
            shape.compatibility_shape,
            "unresolved",
            "blocked",
            (),
            (str(error),),
        )

    facts = [f"Authority Type {shape.authority_type}"]
    changed: list[str] = []
    blocked: list[str] = []
    if _concrete(summary):
        facts.append(f"Authority Summary {summary}")
    else:
        changed.append("Feature Authority is missing a concrete Authority Summary")
    if duplicate_supporting:
        changed.append("Supporting Authority References contains duplicate locators")
    if not primary:
        blocked.append("Feature Authority primary reference is missing")
    elif is_external_locator(primary, shape.adapter):
        facts.append(f"Primary Authority Reference {primary}")
    else:
        try:
            primary_path, issue = _local_authority_path(
                project_root, primary, required=True
            )
            if issue:
                blocked.append(issue)
            elif primary_path is not None:
                facts.append(f"Primary Authority Reference {primary}")
        except AuthorityResolutionError as error:
            blocked.append(str(error))

    for reference in supporting:
        if is_external_locator(reference, CUSTOM_ADAPTER):
            facts.append(f"Supporting Authority Reference {reference}")
            continue
        try:
            _, issue = _local_authority_path(
                project_root, reference, required=False
            )
            if issue:
                changed.append(issue)
            else:
                facts.append(f"Supporting Authority Reference {reference}")
        except AuthorityResolutionError as error:
            blocked.append(str(error))

    if assessment not in {"current", "changed", "unresolved"}:
        changed.append("Agent Authority Assessment is missing or unsupported")
    elif assessment != "current":
        changed.append(
            "supporting authority meaning requires Agent assessment: "
            f"{assessment}"
        )

    if not blocked and shape.adapter == BUG_ADAPTER:
        if is_external_locator(primary, shape.adapter):
            changed.append(
                "external Bug Authority requires Agent review of Expected Behavior and Fix Feature facts"
            )
        else:
            try:
                bug_path, _ = _local_authority_path(
                    project_root, primary, required=True
                )
                if bug_path is not None:
                    bug_facts, bug_changed, bug_blocked = _bug_facts(
                        project_root, feature_spec, bug_path
                    )
                    facts.extend(bug_facts)
                    changed.extend(bug_changed)
                    blocked.extend(bug_blocked)
            except (AuthorityResolutionError, OSError, UnicodeError, ValueError) as error:
                blocked.append(str(error))

    if shape.adapter == FEATURE_ADAPTER and is_external_locator(primary, shape.adapter):
        changed.append(
            "external Feature Authority requires Agent review of current source facts"
        )

    if shape.adapter in {HUMAN_ADAPTER, CUSTOM_ADAPTER}:
        changed.append(
            f"{shape.authority_type} is inspectable advisory evidence for Agent judgment"
        )

    if blocked:
        status = "blocked"
        applicability = "unresolved"
        reasons = tuple(sorted(set(blocked)))
    elif changed:
        status = "changed"
        applicability = "advisory"
        reasons = tuple(sorted(set(changed + facts)))
    else:
        status = "current"
        applicability = "applicable"
        reasons = tuple(facts) or ("authority facts match",)

    return AuthorityResolution(
        authority_type=shape.authority_type,
        adapter=shape.adapter,
        primary_reference=primary,
        supporting_references=supporting,
        compatibility_shape=shape.compatibility_shape,
        applicability=applicability,
        status=status,
        facts=tuple(facts),
        reasons=reasons,
    )
