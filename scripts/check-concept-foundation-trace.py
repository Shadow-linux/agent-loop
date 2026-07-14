#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from checker_support import (
    CheckFailure,
    metadata,
    read_text,
    require_supported_python,
    section,
    table,
)


CONCEPT_ID = re.compile(r"\bC-[A-Z0-9-]+\b")
ACTION_ID = re.compile(r"\b(?:CMD|EVT)-[A-Z0-9-]+\b")
MODEL_ID = re.compile(r"\b(?:REL|PERM|CMD|EVT|FLOW|STATE|PM|EX)-[A-Z0-9-]+\b")


class TraceError(Exception):
    pass


def ids(text: str, pattern: re.Pattern[str]) -> set[str]:
    return set(pattern.findall(text or ""))


def assert_defined(used: set[str], defined: set[str], context: str) -> None:
    missing = used - defined
    if missing:
        raise TraceError(f"undefined IDs in {context}: {', '.join(sorted(missing))}")


def assert_unique_ids(values: list[str], context: str, pattern: re.Pattern[str]) -> None:
    invalid = sorted(set(value for value in values if not pattern.fullmatch(value)))
    if invalid:
        raise TraceError(f"invalid IDs in {context}: {', '.join(invalid)}")
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise TraceError(f"duplicate IDs in {context}: {', '.join(duplicates)}")


def assert_confirmed(used: set[str], confirmed: set[str], context: str) -> None:
    unconfirmed = used - confirmed
    if unconfirmed:
        raise TraceError(
            f"unconfirmed Concept IDs in {context}: {', '.join(sorted(unconfirmed))}"
        )


def reject_placeholders(content: str, path: Path) -> None:
    placeholders = ("<topic>", "C-EXAMPLE", "C-OTHER", "TBD", "TODO", "待补充")
    found = [placeholder for placeholder in placeholders if placeholder in content]
    if found:
        raise TraceError(f"placeholder content in {path}: {', '.join(found)}")


def joined_values(row: dict[str, str]) -> str:
    return " ".join(row.values())


def validate(requirement: str, product: str, spec: str) -> str:
    status = metadata(requirement, "Concept Foundation Status")
    allowed = {"accepted", "concept-foundation-not-needed"}
    if status not in allowed:
        raise TraceError(
            "Concept Foundation must be accepted or reasoned not-needed, got: "
            f"{status or 'missing'}"
        )

    if metadata(product, "Concept Foundation Status") != status:
        raise TraceError("product Concept Foundation status mismatch")
    if metadata(spec, "Concept Foundation Status") != status:
        raise TraceError("spec Concept Foundation status mismatch")

    product_source = metadata(product, "Effective Concept Source")
    spec_source = metadata(spec, "Effective Concept Source")
    if not product_source:
        raise TraceError("product Effective Concept Source is missing")
    if not spec_source:
        raise TraceError("spec Effective Concept Source is missing")
    if product_source != spec_source:
        raise TraceError("effective Concept Foundation source mismatch")

    if status == "concept-foundation-not-needed":
        reason = metadata(requirement, "Not-Needed Reason")
        placeholders = {"n/a", "na", "none", "not applicable", "unknown", "tbd", "todo"}
        if not reason or len(reason.strip()) < 12 or reason.strip().lower() in placeholders:
            raise TraceError(
                "concept-foundation-not-needed requires a concrete reason"
            )
        return "PASS: reasoned concept-foundation-not-needed trace"

    required_order = (
        "## Concept Foundation",
        "## Concept Definitions",
        "## Concept Relationships",
        "## Role / Permission Matrix",
        "## Commands / Events",
        "## Primary Business Flow",
        "## Product State Model",
        "## Requirement Product Model",
        "## Exception Paths",
        "## Concept-To-Product Traceability",
    )
    positions: list[int] = []
    for heading in required_order:
        position = requirement.find(heading)
        if position < 0:
            raise TraceError(f"missing required heading: {heading}")
        positions.append(position)
    if positions != sorted(positions):
        raise TraceError("requirement product sections are out of order")

    candidate_rows = table(requirement, "Concept Candidate Inventory")
    candidate_values = [row.get("Concept ID", "") for row in candidate_rows]
    assert_unique_ids(
        candidate_values, "Concept Candidate Inventory", re.compile(r"C-[A-Z0-9-]+")
    )
    candidate_ids = set(candidate_values)

    concept_rows = table(requirement, "Concept Definitions")
    concept_values = [row.get("Concept ID", "") for row in concept_rows]
    assert_unique_ids(concept_values, "Concept Definitions", re.compile(r"C-[A-Z0-9-]+"))
    concept_ids = set(concept_values)
    assert_defined(concept_ids, candidate_ids, "Concept Definitions inventory")
    canonical_names = {
        row.get("Concept ID", ""): row.get("Canonical Name", "") for row in concept_rows
    }
    if any(not value for value in canonical_names.values()):
        raise TraceError("Concept Definitions contains empty Canonical Name")

    confirmed = ids(section(requirement, "Human Confirmation", level=3), CONCEPT_ID)
    assert_defined(confirmed, concept_ids, "Human Confirmation")
    if not confirmed:
        raise TraceError("Human Confirmation must name accepted Concept IDs")
    candidate_status = {
        row.get("Concept ID", ""): row.get("Status", "") for row in candidate_rows
    }
    not_accepted = sorted(
        concept_id
        for concept_id in confirmed
        if candidate_status.get(concept_id, "") != "accepted"
    )
    if not_accepted:
        raise TraceError(
            "Human Confirmation includes non-accepted inventory IDs: "
            + ", ".join(not_accepted)
        )

    ambiguity_rows = table(requirement, "Blocking Ambiguities", level=3)
    if any(
        row.get("Status", "").lower() not in {"resolved", "not-applicable"}
        for row in ambiguity_rows
    ):
        raise TraceError("Blocking Ambiguities contains unresolved rows")

    relationship_rows = table(requirement, "Concept Relationships")
    relationship_values = [row.get("Relationship ID", "") for row in relationship_rows]
    assert_unique_ids(
        relationship_values, "Concept Relationships", re.compile(r"REL-[A-Z0-9-]+")
    )
    relationship_ids = set(relationship_values)
    relationship_concepts = {
        value
        for row in relationship_rows
        for value in (row.get("From Concept ID", ""), row.get("To Concept ID", ""))
    }
    assert_defined(relationship_concepts, concept_ids, "Concept Relationships")
    assert_confirmed(relationship_concepts, confirmed, "Concept Relationships")

    role_rows = table(requirement, "Role / Permission Matrix")
    permission_values = [row.get("Permission Rule ID", "") for row in role_rows]
    assert_unique_ids(
        permission_values, "Role / Permission Matrix", re.compile(r"PERM-[A-Z0-9-]+")
    )
    permission_ids = set(permission_values)
    role_concepts = {
        value
        for row in role_rows
        for value in (
            row.get("Role Concept ID", ""),
            row.get("Product Object Concept ID", ""),
        )
    }
    assert_defined(role_concepts, concept_ids, "Role / Permission Matrix")
    assert_confirmed(role_concepts, confirmed, "Role / Permission Matrix")
    permission_pairs = {
        (row.get("Role Concept ID", ""), row.get("Product Object Concept ID", ""))
        for row in role_rows
    }

    action_rows = table(requirement, "Commands / Events")
    action_values = [row.get("Action ID", "") for row in action_rows]
    assert_unique_ids(
        action_values, "Commands / Events", re.compile(r"(?:CMD|EVT)-[A-Z0-9-]+")
    )
    action_ids = set(action_values)
    action_concepts = {
        concept
        for row in action_rows
        for field in ("Actor / Producer Concept ID", "Target Concept ID")
        for concept in ids(row.get(field, ""), CONCEPT_ID)
    }
    assert_defined(action_concepts, concept_ids, "Commands / Events")
    assert_confirmed(action_concepts, confirmed, "Commands / Events")
    action_pairs = {
        (
            row.get("Actor / Producer Concept ID", ""),
            row.get("Target Concept ID", ""),
        )
        for row in action_rows
    }
    missing_permissions = action_pairs - permission_pairs
    if missing_permissions:
        rendered = sorted(f"{actor}->{target}" for actor, target in missing_permissions)
        raise TraceError(
            "Commands / Events missing Role / Permission Matrix pairs: "
            + ", ".join(rendered)
        )
    action_actors = {
        row.get("Action ID", ""): row.get("Actor / Producer Concept ID", "")
        for row in action_rows
    }

    flow_rows = table(requirement, "Primary Business Flow")
    flow_values = [row.get("Flow Step ID", "") for row in flow_rows]
    assert_unique_ids(flow_values, "Primary Business Flow", re.compile(r"FLOW-[A-Z0-9-]+"))
    flow_ids = set(flow_values)
    flow_concepts = {concept for row in flow_rows for concept in ids(joined_values(row), CONCEPT_ID)}
    flow_actions = {action for row in flow_rows for action in ids(joined_values(row), ACTION_ID)}
    assert_defined(flow_concepts, concept_ids, "Primary Business Flow")
    assert_confirmed(flow_concepts, confirmed, "Primary Business Flow")
    assert_defined(flow_actions, action_ids, "Primary Business Flow actions")
    for row in flow_rows:
        action_id = row.get("Action ID", "")
        if action_actors.get(action_id) != row.get("Actor Concept ID", ""):
            raise TraceError(f"Primary Business Flow actor mismatch for {action_id}")

    state_rows = table(requirement, "Product State Model")
    state_values = [row.get("State Model ID", "") for row in state_rows]
    assert_unique_ids(state_values, "Product State Model", re.compile(r"STATE-[A-Z0-9-]+"))
    state_ids = set(state_values)
    state_concepts = {concept for row in state_rows for concept in ids(joined_values(row), CONCEPT_ID)}
    state_actions = {action for row in state_rows for action in ids(joined_values(row), ACTION_ID)}
    assert_defined(state_concepts, concept_ids, "Product State Model")
    assert_confirmed(state_concepts, confirmed, "Product State Model")
    assert_defined(state_actions, action_ids, "Product State Model actions")

    product_model_rows = table(requirement, "Requirement Product Model")
    product_model_values = [row.get("Product Model ID", "") for row in product_model_rows]
    assert_unique_ids(
        product_model_values, "Requirement Product Model", re.compile(r"PM-[A-Z0-9-]+")
    )
    product_model_ids = set(product_model_values)
    product_model_concepts = {
        concept
        for row in product_model_rows
        for concept in ids(row.get("Concept IDs", ""), CONCEPT_ID)
    }
    assert_defined(product_model_concepts, concept_ids, "Requirement Product Model")
    assert_confirmed(product_model_concepts, confirmed, "Requirement Product Model")

    exception_rows = table(requirement, "Exception Paths")
    exception_values = [row.get("Scenario ID", "") for row in exception_rows]
    assert_unique_ids(exception_values, "Exception Paths", re.compile(r"EX-[A-Z0-9-]+"))
    exception_ids = set(exception_values)
    exception_cells = [row.get("Concept / State / Action IDs", "") for row in exception_rows]
    exception_concepts = {concept for value in exception_cells for concept in ids(value, CONCEPT_ID)}
    exception_states = {
        state
        for value in exception_cells
        for state in ids(value, re.compile(r"\bSTATE-[A-Z0-9-]+\b"))
    }
    exception_actions = {action for value in exception_cells for action in ids(value, ACTION_ID)}
    assert_defined(exception_concepts, concept_ids, "Exception Paths concepts")
    assert_confirmed(exception_concepts, confirmed, "Exception Paths concepts")
    assert_defined(exception_states, state_ids, "Exception Paths states")
    assert_defined(exception_actions, action_ids, "Exception Paths actions")

    trace_rows = table(requirement, "Concept-To-Product Traceability")
    trace_values = [row.get("Trace ID", "") for row in trace_rows]
    assert_unique_ids(
        trace_values,
        "Concept-To-Product Traceability",
        re.compile(r"TRACE-[A-Z0-9-]+"),
    )
    trace_concepts = {
        concept
        for row in trace_rows
        for concept in ids(row.get("Accepted Concept IDs", ""), CONCEPT_ID)
    }
    assert_defined(trace_concepts, concept_ids, "Concept-To-Product Traceability")
    assert_confirmed(trace_concepts, confirmed, "Concept-To-Product Traceability")

    defined_model_ids = (
        relationship_ids
        | permission_ids
        | action_ids
        | flow_ids
        | state_ids
        | product_model_ids
        | exception_ids
    )
    trace_models = {
        model
        for row in trace_rows
        for model in ids(row.get("Derived Model IDs / Sections", ""), MODEL_ID)
    }
    assert_defined(trace_models, defined_model_ids, "Concept-To-Product Traceability models")
    untraced_models = defined_model_ids - trace_models
    if untraced_models:
        raise TraceError(f"untraced product model IDs: {', '.join(sorted(untraced_models))}")

    if "## Concept Definitions" in product:
        raise TraceError("Product Brief must cite rather than redefine Concept Definitions")
    if "## Concept Definitions" in spec:
        raise TraceError("Feature Spec must cite rather than redefine Concept Definitions")
    if "## Requirement Product Model\n" in product:
        raise TraceError("Product Brief must not own Requirement Product Model")
    if "## Requirement Product Model\n" in spec:
        raise TraceError("Feature Spec must not own Requirement Product Model")

    product_refs = table(product, "Accepted Concept References")
    product_concepts = {
        concept
        for row in product_refs
        for concept in ids(row.get("Concept ID", ""), CONCEPT_ID)
    }
    assert_defined(product_concepts, concept_ids, "Product Brief concept references")
    assert_confirmed(product_concepts, confirmed, "Product Brief concept references")
    for row in product_refs:
        concept_id = row.get("Concept ID", "")
        if canonical_names.get(concept_id) != row.get("Canonical Name", ""):
            raise TraceError(f"Product Brief canonical name mismatch for {concept_id}")

    product_coverage = table(product, "Requirement Product Model Coverage")
    product_coverage_ids = {
        model
        for row in product_coverage
        for model in ids(row.get("Requirement Model ID", ""), MODEL_ID)
    }
    assert_defined(product_coverage_ids, defined_model_ids, "Product Brief model coverage")
    assert_defined(product_coverage_ids, trace_models, "Product Brief traced model coverage")

    spec_refs = table(spec, "Accepted Concept References")
    spec_concepts = {
        concept
        for row in spec_refs
        for concept in ids(row.get("Concept ID", ""), CONCEPT_ID)
    }
    assert_defined(spec_concepts, concept_ids, "Feature Spec concept references")
    assert_confirmed(spec_concepts, confirmed, "Feature Spec concept references")
    for row in spec_refs:
        concept_id = row.get("Concept ID", "")
        if canonical_names.get(concept_id) != row.get("Canonical Name", ""):
            raise TraceError(f"Feature Spec canonical name mismatch for {concept_id}")

    spec_trace = table(spec, "Requirement Product Model Trace")
    spec_model_ids = {
        model
        for row in spec_trace
        for field in ("Requirement Model ID", "Concept / Action / Flow / State IDs")
        for model in ids(row.get(field, ""), MODEL_ID)
    }
    spec_trace_concepts = {
        concept
        for row in spec_trace
        for concept in ids(
            row.get("Concept / Action / Flow / State IDs", ""), CONCEPT_ID
        )
    }
    assert_defined(spec_model_ids, defined_model_ids, "Feature Spec model trace")
    assert_defined(spec_model_ids, trace_models, "Feature Spec traced model coverage")
    assert_defined(spec_trace_concepts, concept_ids, "Feature Spec concept trace")
    assert_confirmed(spec_trace_concepts, confirmed, "Feature Spec concept trace")

    return (
        "PASS: accepted Concept Foundation trace is complete "
        f"({len(concept_ids)} concepts, {len(defined_model_ids)} model rows)"
    )


def main() -> int:
    require_supported_python()
    parser = argparse.ArgumentParser(
        description="Validate Concept Foundation and downstream product-model traceability."
    )
    parser.add_argument("requirement", type=Path)
    parser.add_argument("product", type=Path)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    paths = (args.requirement, args.product, args.spec)
    for path in paths:
        if not path.is_file():
            parser.error(f"missing file: {path}")
    try:
        contents = tuple(read_text(path) for path in paths)
        for content, path in zip(contents, paths, strict=True):
            reject_placeholders(content, path)
        print(validate(*contents))
    except (TraceError, CheckFailure) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
