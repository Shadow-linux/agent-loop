#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path, PurePosixPath

from checker_support import (
    CheckFailure,
    confined_path,
    metadata,
    optional_section,
    read_text,
    require_supported_python,
    section,
    table,
)
from feature_archive_support import ArchiveContractError, resolve_feature_location
from requirement_product_support import (
    CONCEPT_ID_PATTERN,
    MODEL_ID_PATTERN,
    ProductDefinitionError,
    product_model_inventory,
    product_rule_references,
    resolve_effective_product_definition,
)
from visual_artifact_support import VisualArtifactError, validate_durable_visual


SLICE_ID_PATTERN = re.compile(r"DS-[A-Z0-9-]+")
FEATURE_SPEC_RE = re.compile(
    r"(?:^|/)features/(?:(?P<month>\d{4}-\d{2})/)?(?P<feature_id>[^/]+)/spec\.md$"
)

REQUIRED_GATE_ITEMS = (
    "Effective Concept Source resolves and matches the reviewed source",
    "Concept Foundation Status is accepted or reasoned `concept-foundation-not-needed`",
    "Upstream Compatibility is `current`",
    "Every source Requirement Model ID has an explicit scope disposition, or trace is reasoned not-applicable",
    "Every in-scope Accepted Requirement Model ID has exactly one disposition",
    "Every `landed` row has Technical Landing, Preserved Invariant, Design Slice, and Verification",
    "Every `covered-by-accepted-decision` and `feature-local` row names an existing or explicitly planned verified owner path",
    "Every `not-applicable`, deferred, and out-of-scope item is visible in Human Review Summary",
    "Every implementation-bearing technical rule is represented in Design Slice Coverage",
    "No required Design Slice is `unassigned`",
    "No unresolved product-semantic blocker remains",
)

NEW_REQUIRED_GATE_ITEMS = (
    "Effective Product Source or legacy Effective Concept Source resolves and matches the reviewed source",
    "Product Review is confirmed, or legacy Concept Foundation Status is accepted or reasoned `concept-foundation-not-needed`",
    "Upstream Compatibility is `current`",
    "Every source Requirement Model ID and accepted Product Rule reference has an explicit scope disposition, or trace is reasoned not-applicable",
    "Every in-scope Accepted Requirement Model ID and Product Rule reference has exactly one disposition",
    "Every `landed` row has Technical Landing, Preserved Invariant, Design Slice, and Verification",
    "Every `covered-by-accepted-decision` and `feature-local` row names an existing or explicitly planned verified owner path",
    "Every `not-applicable`, deferred, and out-of-scope item is visible in Human Review Summary",
    "Every implementation-bearing technical rule is represented in Design Slice Coverage",
    "No required Design Slice is `unassigned`",
    "No unresolved product-semantic blocker remains",
)

PRODUCT_RULE_REF_PATTERN = re.compile(
    r"(?:product\.md|[A-Za-z0-9._/-]+)#(?:[a-z0-9]+(?:-[a-z0-9]+)*)"
)

REQUIRED_OPERATIONAL_CONCERNS = (
    "Migration / Backfill",
    "Compatibility",
    "Rollout / Cutover",
    "Rollback / Reversibility",
)

ADR_VISUAL_COLUMNS = (
    "Diagram ID",
    "Review Question",
    "Semantic References",
    "Source Definition",
    "Render",
    "Type",
    "Source SHA-256",
    "Render SHA-256",
    "Generator",
    "Validation Evidence",
    "Status",
)


class TraceError(Exception):
    pass


def normalized(value: str | None) -> str:
    text = (value or "").strip()
    if text.startswith("`"):
        text = text[1:]
    if text.endswith("`"):
        text = text[:-1]
    return text


def concrete(value: str | None) -> bool:
    text = normalized(value)
    if not text:
        return False
    if re.fullmatch(
        r"(?:-|none|n/a|na|not applicable|tbd|todo|unknown)", text, re.IGNORECASE
    ):
        return False
    return not re.search(r"<[^>]+>", text)


def concrete_reason(value: str | None) -> bool:
    text = normalized(value)
    return concrete(text) and len(text) >= 12


def assert_unique(values: list[str], context: str) -> None:
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise TraceError(f"duplicate IDs in {context}: {', '.join(duplicates)}")


def parse_id_list(
    value: str | None,
    pattern: re.Pattern[str],
    context: str,
    *,
    allow_none: bool = False,
) -> list[str]:
    text = (value or "").strip()
    if allow_none and text.lower() == "none":
        return []
    if not text:
        raise TraceError(f"{context} is missing")
    tokens = [normalized(token) for token in text.split(",")]
    invalid = [token for token in tokens if not pattern.fullmatch(token)]
    if invalid:
        raise TraceError(f"invalid values in {context}: {', '.join(invalid)}")
    assert_unique(tokens, context)
    return tokens


def parse_date(value: str | None, context: str) -> date:
    if not concrete(value):
        raise TraceError(f"{context} is missing")
    text = normalized(value)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise TraceError(f"{context} must be YYYY-MM-DD")
    try:
        return date.fromisoformat(text)
    except ValueError as error:
        raise TraceError(f"{context} must be YYYY-MM-DD") from error


def read_artifact(path: Path) -> str:
    if not path.is_file():
        raise TraceError(f"missing file: {path}")
    return read_text(path)


def markdown_path(value: str) -> str | None:
    match = re.search(r"([A-Za-z0-9._/-]+\.md)\b", normalized(value))
    return match.group(1) if match else None


def validate_decision_reference(
    value: str,
    workspace_root: Path,
    context: str,
    *,
    allow_planned: bool = False,
    allowed_statuses: tuple[str, ...] = ("accepted",),
) -> None:
    planned = normalized(value).startswith("planned:")
    if planned and not allow_planned:
        raise TraceError(f"{context} cannot be planned")
    relative = markdown_path(value)
    if not relative:
        raise TraceError(f"{context} must name a decision Markdown path")
    absolute = confined_path(workspace_root, relative)
    if planned:
        return
    content = read_artifact(absolute)
    status = metadata(content, "Status")
    if status not in allowed_statuses:
        raise TraceError(
            f"{context} decision status must be {' or '.join(allowed_statuses)}"
        )


def validate_feature_reference(value: str, workspace_root: Path, context: str) -> None:
    planned = normalized(value).startswith("planned:")
    relative = markdown_path(value)
    match = FEATURE_SPEC_RE.search(relative or "")
    if not relative or not match:
        raise TraceError(f"{context} must name a Feature Spec path")
    month = match.group("month")
    feature_id = match.group("feature_id")
    absolute = confined_path(workspace_root, relative)
    if planned:
        if month is not None:
            raise TraceError(f"{context} planned Feature Spec path must be flat")
        return
    content = read_artifact(absolute)
    if metadata(content, "Status") not in {"proposed", "accepted", "closed"}:
        raise TraceError(
            f"{context} Feature Spec must be proposed, accepted, or closed"
        )
    if month is None:
        return

    parts = PurePosixPath(relative).parts
    features_at = parts.index("features")
    if features_at and parts[features_at - 1] in {".agent-loop", "agent-loop"}:
        memory_root = workspace_root.joinpath(*parts[:features_at])
    else:
        memory_root = workspace_root
    try:
        location = resolve_feature_location(memory_root, feature_id)
    except ArchiveContractError as error:
        raise TraceError(str(error)) from error
    expected = f"features/{month}/{feature_id}"
    if location.layout != "archived" or location.relative_path != expected:
        raise TraceError(
            f"{context} archive-index does not locate archived Feature Spec: {relative}"
        )


def validate_human_review(decision: str, decision_status: str) -> None:
    if decision_status == "proposed":
        return
    review = section(decision, "Human Review Evidence")
    if metadata(review, "Decision") != "accepted":
        raise TraceError("accepted ADR must record Decision: accepted")
    if not concrete(metadata(review, "Confirmed By")):
        raise TraceError("accepted ADR must record who confirmed it")
    parse_date(metadata(review, "Confirmed At"), "Human Review Confirmed At")
    if not concrete_reason(metadata(review, "Evidence")):
        raise TraceError("accepted ADR must record Human Review evidence")


def heading_anchor(title: str) -> str:
    value = re.sub(r"[^a-z0-9\s-]", "", title.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


def validate_optional_visual_evidence(
    decision: str,
    decision_path: Path,
    source: str,
    *,
    source_rules: set[str],
) -> None:
    visual = optional_section(decision, "Optional Visual Evidence")
    if visual is None:
        return
    if "Visual Manifest Contract: source-render-v1" not in visual:
        raise TraceError(
            "Optional Visual Evidence must declare source-render-v1"
        )
    rows = table(decision, "Optional Visual Evidence")
    for row in rows:
        if tuple(row.keys()) != ADR_VISUAL_COLUMNS:
            raise TraceError("ADR source-render-v1 columns mismatch")
    diagram_ids = [normalized(row.get("Diagram ID")) for row in rows]
    assert_unique(diagram_ids, "Optional Visual Evidence")

    accepted_refs = set(CONCEPT_ID_PATTERN.findall(source))
    accepted_refs.update(MODEL_ID_PATTERN.findall(source))
    accepted_refs.update(source_rules)
    decision_refs = {
        f"{decision_path.name}#{heading_anchor(match.group(1))}"
        for match in re.finditer(r"^##\s+(.+?)\s*$", decision, re.MULTILINE)
    }
    accepted_refs.update(decision_refs)

    for row in rows:
        diagram_id = normalized(row.get("Diagram ID"))
        if not concrete_reason(row.get("Review Question")):
            raise TraceError(f"ADR visual {diagram_id} needs a concrete review question")
        semantic_refs = [
            normalized(value)
            for value in (row.get("Semantic References") or "").split(",")
            if normalized(value)
        ]
        if not semantic_refs:
            raise TraceError(f"ADR visual {diagram_id} needs semantic references")
        unknown = set(semantic_refs) - accepted_refs
        if unknown:
            raise TraceError(
                f"ADR visual {diagram_id} has unknown semantic references: "
                + ", ".join(sorted(unknown))
            )
        if normalized(row.get("Status")) != "current":
            raise TraceError(f"ADR visual {diagram_id} status must be current")
        validate_durable_visual(
            decision_path.parent,
            diagram_id=diagram_id,
            source_definition=row.get("Source Definition", ""),
            render=row.get("Render", ""),
            diagram_type=row.get("Type", ""),
            source_sha256=row.get("Source SHA-256", ""),
            render_sha256=row.get("Render SHA-256", ""),
            generator=row.get("Generator", ""),
            validation_evidence=row.get("Validation Evidence", ""),
        )


def validate_gate(decision: str, *, legacy: bool) -> None:
    gate = section(decision, "Coverage Hard Gate")
    if any(re.match(r"^\s*- \[ \]", line) for line in gate.splitlines()):
        raise TraceError("Coverage Hard Gate contains unchecked items")
    completed = []
    for line in gate.splitlines():
        match = re.match(r"^\s*- \[[xX]\]\s+(.+?)\s*$", line)
        if match:
            completed.append(match.group(1))
    assert_unique(completed, "Coverage Hard Gate")
    allowed_contracts = (
        (REQUIRED_GATE_ITEMS, NEW_REQUIRED_GATE_ITEMS)
        if legacy
        else (NEW_REQUIRED_GATE_ITEMS,)
    )
    if any(
        len(completed) == len(contract) and set(completed) == set(contract)
        for contract in allowed_contracts
    ):
        return
    required = REQUIRED_GATE_ITEMS if legacy else NEW_REQUIRED_GATE_ITEMS
    missing = [item for item in required if item not in completed]
    if missing:
        raise TraceError(
            "Coverage Hard Gate is missing required items: " + "; ".join(missing)
        )
    extra = [item for item in completed if item not in required]
    if extra:
        raise TraceError(
            "Coverage Hard Gate contains unsupported items: " + "; ".join(extra)
        )


def validate_operational(decision: str) -> None:
    rows = table(decision, "Operational Landing Trigger Assessment")
    concerns = [row.get("Concern", "") for row in rows]
    assert_unique(concerns, "Operational Landing Trigger Assessment")
    missing = [item for item in REQUIRED_OPERATIONAL_CONCERNS if item not in concerns]
    extra = [item for item in concerns if item not in REQUIRED_OPERATIONAL_CONCERNS]
    if missing or extra:
        raise TraceError(
            "operational concern inventory mismatch; "
            f"missing={', '.join(missing)} extra={', '.join(extra)}"
        )

    triggered_details: list[str] = []
    for row in rows:
        concern = row.get("Concern", "")
        status = row.get("Status", "")
        reason = row.get("Reason / Trigger Evidence", "")
        detail = row.get("Detail Section If Triggered", "")
        if status not in {"triggered", "not-triggered"}:
            raise TraceError(f"invalid operational trigger status for {concern}")
        if not concrete_reason(reason):
            raise TraceError(f"operational trigger {concern} needs a concrete reason")
        if status == "triggered":
            if not concrete(detail):
                raise TraceError(
                    f"triggered operational concern {concern} needs a detail section"
                )
            triggered_details.append(detail)
        elif normalized(detail).lower() != "none":
            raise TraceError(
                f"not-triggered operational concern {concern} must use Detail Section: none"
            )

    operational = optional_section(decision, "Triggered Operational Landing")
    if not triggered_details:
        if operational is not None:
            raise TraceError(
                "Triggered Operational Landing must be absent when no concern is triggered"
            )
        return
    if operational is None:
        raise TraceError("Triggered Operational Landing is missing")
    for detail in triggered_details:
        if not re.search(rf"^### {re.escape(detail)}\s*$", decision, re.MULTILINE):
            raise TraceError(f"missing triggered operational detail heading: {detail}")


def source_model_inventory(source: str) -> tuple[set[str], set[str]]:
    concept_rows = table(source, "Concept Definitions")
    concept_values = [row.get("Concept ID", "") for row in concept_rows]
    assert_unique(concept_values, "source Concept Definitions")
    if not all(CONCEPT_ID_PATTERN.fullmatch(value) for value in concept_values):
        raise TraceError("source Concept Definitions contains invalid IDs")

    model_tables = (
        ("Concept Relationships", "Relationship ID", re.compile(r"REL-[A-Z0-9-]+")),
        ("Role / Permission Matrix", "Permission Rule ID", re.compile(r"PERM-[A-Z0-9-]+")),
        ("Commands / Events", "Action ID", re.compile(r"(?:CMD|EVT)-[A-Z0-9-]+")),
        ("Primary Business Flow", "Flow Step ID", re.compile(r"FLOW-[A-Z0-9-]+")),
        ("Product State Model", "State Model ID", re.compile(r"STATE-[A-Z0-9-]+")),
        ("Requirement Product Model", "Product Model ID", re.compile(r"PM-[A-Z0-9-]+")),
        ("Exception Paths", "Scenario ID", re.compile(r"EX-[A-Z0-9-]+")),
    )
    model_values: list[str] = []
    for title, column, pattern in model_tables:
        values = [row.get(column, "") for row in table(source, title)]
        assert_unique(values, f"source {title}")
        if not all(pattern.fullmatch(value) for value in values):
            raise TraceError(f"source {title} contains invalid IDs")
        model_values.extend(values)
    assert_unique(model_values, "accepted Requirement Model")
    return set(concept_values), set(model_values)


def validate(
    readme_path: Path,
    source_path: Path,
    decision_path: Path,
    workspace_root: Path,
) -> str:
    effective_source = resolve_effective_product_definition(
        readme_path, source_path
    )
    source = effective_source.content
    decision = read_artifact(decision_path)
    pointer_source = source_path.resolve().relative_to(readme_path.parent.resolve()).as_posix()
    source_status = effective_source.review

    decision_status = metadata(decision, "Status")
    if decision_status not in {"proposed", "accepted"}:
        raise TraceError(
            "decision status must be proposed or accepted for gate validation"
        )
    heading = re.search(r"^#\s+(ADR-[A-Z0-9-]+):", decision, re.MULTILINE)
    if not heading:
        raise TraceError("decision heading must declare an ADR ID")
    decision_id = heading.group(1)
    validate_human_review(decision, decision_status)

    snapshot = section(decision, "Effective Requirement Snapshot")
    compatibility = metadata(snapshot, "Upstream Compatibility")
    last_check = metadata(snapshot, "Last Compatibility Check")
    if effective_source.legacy:
        if any(
            normalized(metadata(snapshot, key))
            for key in (
                "Effective Product Source",
                "Product Definition Profile",
                "Product Review",
                "Accepted Product Rule References",
            )
        ):
            raise TraceError(
                "ADR snapshot must not mix Product Definition and legacy Concept Foundation metadata"
            )
        snapshot_source = normalized(metadata(snapshot, "Effective Concept Source")).replace(
            "\\", "/"
        )
        snapshot_status = metadata(snapshot, "Concept Foundation Status")
        if snapshot_source != pointer_source:
            raise TraceError(
                "ADR Effective Concept Source does not match requirement pointer"
            )
        if snapshot_status != source_status:
            raise TraceError(
                "ADR Concept Foundation status does not match effective source"
            )
    else:
        if any(
            normalized(metadata(snapshot, key))
            for key in ("Effective Concept Source", "Concept Foundation Status")
        ):
            raise TraceError(
                "ADR snapshot must not mix Product Definition and legacy Concept Foundation metadata"
            )
        snapshot_source = normalized(metadata(snapshot, "Effective Product Source")).replace(
            "\\", "/"
        )
        if snapshot_source != pointer_source:
            raise TraceError(
                "ADR Effective Product Source does not match requirement pointer"
            )
        if metadata(snapshot, "Product Definition Profile") != effective_source.profile:
            raise TraceError(
                "ADR Product Definition Profile does not match effective source"
            )
        if metadata(snapshot, "Product Review") != "confirmed":
            raise TraceError("ADR Product Review must match confirmed effective source")
    if compatibility != "current":
        raise TraceError("Upstream Compatibility must be current before acceptance")
    parse_date(last_check, "Last Compatibility Check")
    validate_optional_visual_evidence(
        decision,
        decision_path,
        source,
        source_rules=(
            set() if effective_source.legacy else product_rule_references(effective_source)
        ),
    )

    slice_rows = table(decision, "Design Slice Coverage")
    slice_values = [row.get("Design Slice ID", "") for row in slice_rows]
    invalid_slices = [value for value in slice_values if not SLICE_ID_PATTERN.fullmatch(value)]
    if invalid_slices:
        raise TraceError(f"invalid Design Slice IDs: {', '.join(invalid_slices)}")
    assert_unique(slice_values, "Design Slice Coverage")
    allowed_slice_statuses = {"planned", "implemented", "verified", "deferred", "out-of-scope"}
    slice_statuses: dict[str, str] = {}
    for row in slice_rows:
        slice_id = row.get("Design Slice ID", "")
        capability = row.get("Required Capability / Rule", "")
        owner = row.get("Owning Feature(s)", "")
        verification = row.get("Verification", "")
        status = row.get("Coverage Status", "")
        if not concrete_reason(capability):
            raise TraceError(f"Design Slice {slice_id} has no required capability")
        if not concrete(owner):
            raise TraceError(f"Design Slice {slice_id} has no owner")
        if not concrete(verification):
            raise TraceError(f"Design Slice {slice_id} has no verification")
        if status not in allowed_slice_statuses:
            raise TraceError(
                f"Design Slice {slice_id} has invalid coverage status: {status}"
            )
        slice_statuses[slice_id] = status

    validate_gate(decision, legacy=effective_source.legacy)
    validate_operational(decision)

    reasoned_legacy_not_needed = (
        effective_source.legacy
        and source_status == "concept-foundation-not-needed"
    )
    reasoned_brief_not_applicable = (
        not effective_source.legacy and effective_source.profile == "brief"
    )
    if reasoned_legacy_not_needed or reasoned_brief_not_applicable:
        for forbidden_heading in (
            "Concept Definitions",
            "Requirement Model Scope Inventory",
            "Requirement Model Technical Landing Trace",
        ):
            if optional_section(decision, forbidden_heading) is not None:
                raise TraceError(
                    f"reasoned no-model ADR must omit {forbidden_heading}"
                )
        if reasoned_legacy_not_needed and not concrete_reason(
            metadata(source, "Not-Needed Reason")
        ):
            raise TraceError(
                "concept-foundation-not-needed requires a concrete reason"
            )
        concepts = parse_id_list(
            metadata(snapshot, "Accepted Concept IDs"),
            CONCEPT_ID_PATTERN,
            "ADR Accepted Concept IDs",
            allow_none=True,
        )
        models = parse_id_list(
            metadata(snapshot, "Accepted Requirement Model IDs"),
            MODEL_ID_PATTERN,
            "ADR Accepted Requirement Model IDs",
            allow_none=True,
        )
        if concepts:
            raise TraceError("reasoned not-needed ADR must not declare Concept IDs")
        if models:
            raise TraceError(
                "reasoned not-needed ADR must not declare Requirement Model IDs"
            )
        rules: list[str] = []
        if not effective_source.legacy:
            rules = parse_id_list(
                metadata(snapshot, "Accepted Product Rule References"),
                PRODUCT_RULE_REF_PATTERN,
                "ADR Accepted Product Rule References",
                allow_none=True,
            )
        if rules:
            raise TraceError(
                "reasoned not-applicable ADR must not declare Product Rule references"
            )
        if metadata(snapshot, "Trace Applicability") != "not-applicable":
            raise TraceError(
                "reasoned no-model ADR must set Trace Applicability: not-applicable"
            )
        if not concrete_reason(metadata(snapshot, "Trace Not-Applicable Reason")):
            raise TraceError("reasoned not-applicable ADR needs a concrete trace reason")
        if reasoned_legacy_not_needed:
            return (
                "PASS: reasoned concept-foundation-not-needed ADR "
                f"{decision_status} gate is complete"
            )
        return f"PASS: reasoned confirmed Brief ADR {decision_status} gate is complete"

    if metadata(snapshot, "Trace Applicability") != "required":
        label = "accepted Concept Foundation" if effective_source.legacy else "confirmed Product Definition"
        raise TraceError(f"{label} ADR must set Trace Applicability: required")

    source_concepts, source_models = product_model_inventory(effective_source)
    source_rules = product_rule_references(effective_source)
    snapshot_concepts = set(
        parse_id_list(
            metadata(snapshot, "Accepted Concept IDs"),
            CONCEPT_ID_PATTERN,
            "ADR Accepted Concept IDs",
            allow_none=True,
        )
    )
    snapshot_models = set(
        parse_id_list(
            metadata(snapshot, "Accepted Requirement Model IDs"),
            MODEL_ID_PATTERN,
            "ADR Accepted Requirement Model IDs",
            allow_none=True,
        )
    )
    snapshot_rules: set[str] = set()
    if not effective_source.legacy:
        snapshot_rules = set(
            parse_id_list(
                metadata(snapshot, "Accepted Product Rule References"),
                PRODUCT_RULE_REF_PATTERN,
                "ADR Accepted Product Rule References",
                allow_none=True,
            )
        )
    if source_concepts and not snapshot_concepts:
        raise TraceError("ADR scope must name accepted Concept IDs")
    if source_models and not snapshot_models:
        raise TraceError("ADR scope must name accepted Requirement Model IDs")
    if not snapshot_models and not snapshot_rules:
        raise TraceError("ADR scope must name accepted Requirement Model IDs or Product Rule references")
    unknown_concepts = snapshot_concepts - source_concepts
    if unknown_concepts:
        raise TraceError(
            "ADR snapshot contains unknown Concept IDs: "
            + ", ".join(sorted(unknown_concepts))
        )
    unknown_models = snapshot_models - source_models
    if unknown_models:
        raise TraceError(
            "ADR snapshot contains unknown Requirement Model IDs: "
            + ", ".join(sorted(unknown_models))
        )
    unknown_rules = snapshot_rules - source_rules
    if unknown_rules:
        raise TraceError(
            "ADR snapshot contains unknown Product Rule references: "
            + ", ".join(sorted(unknown_rules))
        )

    scope_rows = table(decision, "Requirement Model Scope Inventory")
    scope_values = [row.get("Requirement Model Ref", "") for row in scope_rows]
    assert_unique(scope_values, "Requirement Model Scope Inventory")
    scope_refs = set(scope_values)
    source_refs = source_models | source_rules
    missing_scope = source_refs - scope_refs
    extra_scope = scope_refs - source_refs
    if missing_scope or extra_scope:
        raise TraceError(
            "Requirement Model Scope Inventory mismatch; "
            f"missing={', '.join(sorted(missing_scope))} "
            f"extra={', '.join(sorted(extra_scope))}"
        )

    allowed_scope_dispositions = {
        "in-scope",
        "covered-by-accepted-decision",
        "feature-local",
        "proposed-decision",
        "not-applicable",
    }
    in_scope: set[str] = set()
    for row in scope_rows:
        ref = row.get("Requirement Model Ref", "")
        disposition = row.get("Scope Disposition", "")
        owner = row.get("Owner / Reason", "")
        if disposition not in allowed_scope_dispositions:
            raise TraceError(f"scope row {ref} has invalid disposition: {disposition}")
        if disposition == "in-scope":
            in_scope.add(ref)
            if normalized(owner) not in {decision_id, "this ADR"}:
                raise TraceError(
                    f"in-scope model {ref} must name {decision_id} or this ADR"
                )
        elif disposition == "covered-by-accepted-decision":
            validate_decision_reference(owner, workspace_root, f"scope row {ref}")
        elif disposition == "feature-local":
            validate_feature_reference(owner, workspace_root, f"scope row {ref}")
        elif disposition == "proposed-decision":
            validate_decision_reference(
                owner,
                workspace_root,
                f"scope row {ref}",
                allow_planned=True,
                allowed_statuses=("proposed",),
            )
        else:
            match = re.match(r"^reason:\s*(.*)$", owner, re.IGNORECASE)
            if not match or not concrete_reason(match.group(1)):
                raise TraceError(
                    f"scope row {ref} needs a concrete not-applicable reason"
                )
    snapshot_refs = snapshot_models | snapshot_rules
    if snapshot_refs != in_scope:
        raise TraceError(
            "ADR Accepted Requirement Model IDs and Product Rule references must equal in-scope inventory references"
        )

    trace_rows = table(decision, "Requirement Model Technical Landing Trace")
    trace_values = [row.get("Requirement Model Ref", "") for row in trace_rows]
    assert_unique(trace_values, "Requirement Model Technical Landing Trace")
    trace_refs = set(trace_values)
    missing_rows = snapshot_refs - trace_refs
    extra_rows = trace_refs - snapshot_refs
    if missing_rows:
        raise TraceError(f"missing trace coverage: {', '.join(sorted(missing_rows))}")
    if extra_rows:
        raise TraceError(
            f"trace rows outside declared ADR scope: {', '.join(sorted(extra_rows))}"
        )

    allowed_dispositions = {
        "landed",
        "covered-by-accepted-decision",
        "feature-local",
        "not-applicable",
    }
    landed_rows: list[dict[str, str]] = []
    for row in trace_rows:
        ref = row.get("Requirement Model Ref", "")
        meaning = row.get("Accepted Meaning / Constraint", "")
        disposition = row.get("Disposition", "")
        if not concrete_reason(meaning):
            raise TraceError(
                f"trace row {ref} has no accepted meaning/constraint reference"
            )
        if disposition not in allowed_dispositions:
            raise TraceError(f"trace row {ref} has invalid disposition: {disposition}")
        landing = row.get("Technical Landing", "")
        invariant = row.get("Preserved Invariant", "")
        slice_value = row.get("Design Slice", "")
        verification = row.get("Verification", "")
        if disposition == "landed":
            required = {
                "Technical Landing": landing,
                "Preserved Invariant": invariant,
                "Design Slice": slice_value,
                "Verification": verification,
            }
            missing = [field for field, value in required.items() if not concrete(value)]
            if missing:
                raise TraceError(
                    f"landed trace row {ref} has empty fields: {', '.join(missing)}"
                )
            landed_rows.append(row)
        elif disposition == "covered-by-accepted-decision":
            validate_decision_reference(landing, workspace_root, f"trace row {ref}")
            if not concrete_reason(verification):
                raise TraceError(
                    f"covered-by-accepted-decision trace row {ref} "
                    "must name verification direction"
                )
        elif disposition == "feature-local":
            validate_feature_reference(landing, workspace_root, f"trace row {ref}")
            if not concrete_reason(verification):
                raise TraceError(
                    f"feature-local trace row {ref} must name verification direction"
                )
        else:
            match = re.match(r"^reason:\s*(.*)$", landing, re.IGNORECASE)
            if not match or not concrete_reason(match.group(1)):
                raise TraceError(
                    f"not-applicable trace row {ref} must give a concrete reason"
                )

    known_slices = set(slice_statuses)
    for row in landed_rows:
        slice_ids = set(
            parse_id_list(
                row.get("Design Slice", ""),
                SLICE_ID_PATTERN,
                "trace Design Slice IDs",
            )
        )
        unknown_slices = slice_ids - known_slices
        if unknown_slices:
            raise TraceError(
                "trace references unknown Design Slices: "
                + ", ".join(sorted(unknown_slices))
            )

    return (
        f"PASS: ADR {decision_status} technical landing trace covers "
        f"{len(snapshot_refs)} in-scope requirement-model/rule references with "
        f"{len(landed_rows)} landed rows"
    )


def main() -> int:
    require_supported_python()
    parser = argparse.ArgumentParser(
        description="Validate ADR requirement-model scope and technical landing trace."
    )
    parser.add_argument("requirement_readme", type=Path)
    parser.add_argument("effective_source", type=Path)
    parser.add_argument("decision", type=Path)
    parser.add_argument("workspace_root", nargs="?", type=Path)
    args = parser.parse_args()
    paths = (args.requirement_readme, args.effective_source, args.decision)
    for path in paths:
        if not path.is_file():
            parser.error(f"missing file: {path}")
    workspace_root = (args.workspace_root or args.requirement_readme.parent).resolve()
    try:
        print(validate(*paths, workspace_root))
    except (TraceError, CheckFailure, ProductDefinitionError, VisualArtifactError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
