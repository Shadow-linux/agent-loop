#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

from checker_support import (
    CheckFailure,
    confined_path,
    read_text,
    require_supported_python,
)


START_RE = re.compile(r"<!--\s*agent-loop:managed-start\s+([^>]*)-->")
END_RE = re.compile(r"<!--\s*agent-loop:managed-end\s+section:([^\s>]+)\s*-->")


@dataclass
class ManagedBlock:
    section: str
    source: str | None
    version: str | None
    block_version: str | None
    start_line: int
    end_line: int | None = None
    body: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class MarkerError:
    section: str
    status: str
    detail: str


def attr_value(attrs: str, name: str) -> str | None:
    match = re.search(rf"(?:^|\s){re.escape(name)}:([^\s>]+)", attrs)
    return match.group(1) if match else None


def parse_blocks(path: Path) -> tuple[dict[str, ManagedBlock], list[MarkerError]]:
    blocks: dict[str, ManagedBlock] = {}
    errors: list[MarkerError] = []
    active: ManagedBlock | None = None

    for line_no, line in enumerate(read_text(path).splitlines(), start=1):
        if len(re.findall(r"agent-loop:managed-(?:start|end)", line)) > 1:
            errors.append(
                MarkerError(
                    "(unknown)",
                    "malformed-marker",
                    f"multiple managed markers on one line at line {line_no}",
                )
            )
            continue

        start_match = START_RE.search(line)
        if start_match:
            attrs = start_match.group(1)
            section_name = attr_value(attrs, "section")
            if not section_name:
                errors.append(
                    MarkerError(
                        "(unknown)",
                        "malformed-marker",
                        f"start marker at line {line_no} is missing section",
                    )
                )
                continue
            if active:
                errors.append(
                    MarkerError(
                        active.section,
                        "broken-markers",
                        f"section {active.section} starts at line {active.start_line} "
                        f"but is not closed before line {line_no}",
                    )
                )
                errors.append(
                    MarkerError(
                        active.section,
                        "nested-managed-block",
                        f"section {active.section} starts at line {active.start_line} "
                        f"but a nested section starts at line {line_no}",
                    )
                )
            if section_name in blocks:
                errors.append(
                    MarkerError(
                        section_name,
                        "duplicate-section",
                        f"section {section_name} appears more than once",
                    )
                )
            active = ManagedBlock(
                section=section_name,
                source=attr_value(attrs, "source"),
                version=attr_value(attrs, "version"),
                block_version=attr_value(attrs, "block-version"),
                start_line=line_no,
            )
            continue

        if "agent-loop:managed-start" in line:
            errors.append(
                MarkerError(
                    "(unknown)",
                    "malformed-marker",
                    f"malformed managed-start marker at line {line_no}",
                )
            )
            continue

        end_match = END_RE.search(line)
        if end_match:
            end_section = end_match.group(1)
            if not active:
                errors.append(
                    MarkerError(
                        end_section,
                        "broken-markers",
                        f"orphan end marker at line {line_no}",
                    )
                )
                continue
            if active.section != end_section:
                errors.append(
                    MarkerError(
                        active.section,
                        "broken-markers",
                        f"section {active.section} starts at line {active.start_line} "
                        f"but ends as {end_section} at line {line_no}",
                    )
                )
                active = None
                continue
            active.end_line = line_no
            blocks[active.section] = active
            active = None
            continue

        if "agent-loop:managed-end" in line:
            errors.append(
                MarkerError(
                    "(unknown)",
                    "malformed-marker",
                    f"malformed managed-end marker at line {line_no}",
                )
            )
            continue

        if active:
            active.body.append(line)

    if active:
        errors.append(
            MarkerError(
                active.section,
                "broken-markers",
                f"section {active.section} starts at line {active.start_line} "
                "but has no end marker",
            )
        )
    return blocks, errors


def local_source(source: str | None) -> bool:
    return bool(
        source
        and source != "agent-loop-skill"
        and not source.startswith(("http://", "https://"))
        and ("/" in source or source.endswith(".md"))
    )


def escape_cell(value: object) -> str:
    return str(value).replace("|", r"\|")


def normalized_body(block: ManagedBlock) -> str:
    lines = [line.rstrip() for line in block.body]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only checker for agent-loop root AGENTS managed blocks. "
            "Verifies marker structure, required sections, and block versions."
        )
    )
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--no-source-check", action="store_true")
    return parser


def main() -> int:
    require_supported_python()
    parser = build_parser()
    args = parser.parse_args()
    template: Path = args.template
    target: Path = args.target
    if not template.is_file():
        parser.error(f"Template not found: {template}")
    if not target.is_file():
        parser.error(f"Target not found: {target}")

    template_blocks, template_errors = parse_blocks(template)
    target_blocks, target_errors = parse_blocks(target)
    findings: list[tuple[str, list[object]]] = []

    def add(severity: str, row: list[object]) -> None:
        findings.append((severity, row))

    for error in template_errors:
        add(
            "invalid",
            [error.section, error.status, "-", "-", error.detail, "fix template markers"],
        )

    for error in target_errors:
        expected = template_blocks.get(error.section)
        add(
            "invalid",
            [
                error.section,
                error.status,
                expected.block_version if expected else "-",
                "-",
                error.detail,
                "repair target managed markers before refresh",
            ],
        )

    for section_name, expected in template_blocks.items():
        actual = target_blocks.get(section_name)
        if not actual:
            add(
                "changed",
                [
                    section_name,
                    "missing",
                    expected.block_version,
                    "none",
                    "template section is absent from target AGENTS.md",
                    "add managed block after human review",
                ],
            )
            continue
        if not actual.block_version:
            add(
                "changed",
                [
                    section_name,
                    "missing-block-version",
                    expected.block_version,
                    "none",
                    f"expected {expected.block_version}",
                    "refresh marker metadata after human review",
                ],
            )
        elif actual.block_version != expected.block_version:
            add(
                "changed",
                [
                    section_name,
                    "stale-block-version",
                    expected.block_version,
                    actual.block_version,
                    f"expected {expected.block_version}, found {actual.block_version}",
                    "refresh managed block after human review",
                ],
            )

        if expected.source == "agent-loop-skill":
            if actual.source != "agent-loop-skill":
                add(
                    "changed",
                    [
                        section_name,
                        "source-drift",
                        expected.block_version,
                        actual.block_version,
                        f"expected source agent-loop-skill, found {actual.source or 'none'}",
                        "review and refresh the Agent Loop-owned block",
                    ],
                )
            elif normalized_body(actual) != normalized_body(expected):
                add(
                    "changed",
                    [
                        section_name,
                        "body-drift",
                        expected.block_version,
                        actual.block_version,
                        "Agent Loop-owned block body differs from the template",
                        "Agent reviews the diff before proposing refresh",
                    ],
                )

        if args.no_source_check or not local_source(actual.source):
            continue
        try:
            source_path = confined_path(target.parent, str(actual.source))
        except CheckFailure:
            add(
                "invalid",
                [
                    section_name,
                    "source-outside-workspace",
                    expected.block_version,
                    actual.block_version,
                    f"source {actual.source} escapes {target.parent}",
                    "move source inside the project before human review",
                ],
            )
            continue
        if not source_path.exists():
            add(
                "changed",
                [
                    section_name,
                    "source-missing",
                    expected.block_version,
                    actual.block_version,
                    f"source {actual.source} does not exist relative to {target.parent}",
                    "verify source path or update block source after human review",
                ],
            )

    for section_name, actual in target_blocks.items():
        if section_name not in template_blocks:
            add(
                "changed",
                [
                    section_name,
                    "unexpected-managed-section",
                    "none",
                    actual.block_version,
                    "target section is not present in template",
                    "ask whether to keep, migrate, or remove",
                ],
            )

    if not findings:
        print(
            "STRUCTURAL_CURRENT: root AGENTS markers, revisions, sources, and "
            "Agent Loop-owned block bodies align"
        )
        return 0

    invalid = any(severity == "invalid" for severity, _ in findings)
    if invalid:
        print("STRUCTURAL_INVALID: root AGENTS structure requires repair\n")
    else:
        print(
            "STRUCTURAL_CHANGED: root AGENTS facts changed; "
            "Agent review is required before any refresh\n"
        )
    print("| Section | Status | Template Block | Target Block | Detail | Action |")
    print("|---|---|---|---|---|---|")
    for _, row in findings:
        print(f"| {' | '.join(escape_cell(cell) for cell in row)} |")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
