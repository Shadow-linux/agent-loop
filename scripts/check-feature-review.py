#!/usr/bin/env python3
"""Validate durable Feature Definition / Implementation Readiness review evidence."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

from checker_support import configure_utf8_stdio, require_supported_python


REQUIRED_FIELDS = (
    "Implementation Readiness",
    "Gate 1 Decision",
    "Gate 1 Spec Digest",
    "Gate 2 Decision",
    "Gate 2 Package Files",
    "Gate 2 Package Digest",
    "Gate 2 Stable Files",
    "Gate 2 Stable Digest Algorithm",
    "Gate 2 Stable Digest",
    "Gate 2 Agent-ready Tasks",
    "Active Plan Scope",
    "Gate 2 Plan Evidence",
    "Feature Auto-Loop",
    "Gate 2 Reviewed At",
)

RAW_STABLE_DIGEST = "raw-v1"
PROJECTED_STABLE_DIGEST = "review-definition-v2"
STABLE_DIGEST_ALGORITHMS = {RAW_STABLE_DIGEST, PROJECTED_STABLE_DIGEST}


def parse_fields(notes: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in notes.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^-?\s*([^:]+):\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1).strip()] = match.group(2).strip()
    return fields


def parse_list(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def resolve_files(feature: Path, names: list[str], errors: list[str]) -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    feature_real = feature.resolve()
    for name in names:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"unsafe package path: {name}")
            continue
        path = feature / relative
        try:
            path_real = path.resolve(strict=True)
        except FileNotFoundError:
            errors.append(f"missing package file: {name}")
            continue
        if path.is_symlink() or feature_real not in path_real.parents:
            errors.append(f"package path escapes Feature root: {name}")
            continue
        if not path_real.is_file():
            errors.append(f"package path is not a file: {name}")
            continue
        resolved[name] = path_real
    return resolved


def _project_task_definition(name: str, text: str, errors: list[str]) -> bytes:
    lines = text.splitlines()
    projected: list[str] = []
    section = ""
    in_task = False
    seen_tasks: set[str] = set()
    seen_runtime_fields: set[str] = set()
    is_root = name == "tasks.md"

    for line_number, line in enumerate(lines, start=1):
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            section = heading.group(1)
            in_task = False

        if not section and re.match(r"^(Updated|Status):\s*", line):
            line = re.sub(r":.*$", ": <runtime>", line)

        if is_root:
            task = re.match(r"^(\s*-\s*)\[[ xX]\](\s+(T\d+)\b.*)$", line)
            if task:
                task_id = task.group(3)
                if task_id in seen_tasks:
                    errors.append(
                        f"ambiguous Stable Digest projection in {name}:{line_number}: "
                        f"duplicate task ID {task_id}"
                    )
                seen_tasks.add(task_id)
                line = f"{task.group(1)}[ ]{task.group(2)}"
                in_task = True
                seen_runtime_fields = set()
            elif in_task and re.match(
                r"^\s+-\s+(Status|Review|Drift):\s*", line
            ):
                field = re.match(r"^\s+-\s+(Status|Review|Drift):", line)
                assert field is not None
                field_name = field.group(1)
                if field_name in seen_runtime_fields:
                    errors.append(
                        f"ambiguous Stable Digest projection in {name}:{line_number}: "
                        f"duplicate runtime field {field_name}"
                    )
                seen_runtime_fields.add(field_name)
                line = re.sub(r":.*$", ": <runtime>", line)
        elif section == "Task Done Gate":
            line = re.sub(r"^(\s*-\s*)\[[ xX]\]", r"\1[ ]", line)
            if re.match(r"^(Evidence|Review|Drift):\s*", line):
                line = re.sub(r":.*$", ": <runtime>", line)

        projected.append(line)
    return ("\n".join(projected) + "\n").encode("utf-8")


def _is_markdown_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\|[\s:|-]+\|", line.strip()))


def _project_test_definition(name: str, text: str, errors: list[str]) -> bytes:
    lines = text.splitlines()
    projected: list[str] = []
    section = ""
    is_root = name == "tests.md"

    for line_number, line in enumerate(lines, start=1):
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            section = heading.group(1)

        if not section and re.match(r"^(Updated|Status):\s*", line):
            line = re.sub(r":.*$", ": <runtime>", line)

        if is_root and line.strip().startswith("|") and not _is_markdown_separator(line):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if section == "Design Slice Verification Matrix":
                if cells and cells[0] == "Design Slice ID":
                    pass
                elif len(cells) != 4:
                    errors.append(
                        f"malformed Design Slice Verification Matrix row in "
                        f"{name}:{line_number}"
                    )
                else:
                    cells[-1] = "<runtime>"
                    line = "| " + " | ".join(cells) + " |"
            elif section == "Bug Verification Matrix":
                if cells and cells[0] == "Bug ID":
                    pass
                elif len(cells) != 6:
                    errors.append(
                        f"malformed Bug Verification Matrix row in {name}:{line_number}"
                    )
                else:
                    cells[-2:] = ["<runtime>", "<runtime>"]
                    line = "| " + " | ".join(cells) + " |"

        projected.append(line)
    return ("\n".join(projected) + "\n").encode("utf-8")


def stable_file_bytes(
    name: str, path: Path, algorithm: str, errors: list[str]
) -> bytes:
    if algorithm == RAW_STABLE_DIGEST:
        return path.read_bytes()
    if algorithm != PROJECTED_STABLE_DIGEST:
        errors.append(f"unsupported Gate 2 Stable Digest Algorithm: {algorithm}")
        return b""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        errors.append(f"Stable Digest projection requires UTF-8 Markdown: {name}")
        return b""
    if name == "tasks.md" or name.startswith("tasks/"):
        return _project_task_definition(name, text, errors)
    if name == "tests.md" or name.startswith("tests/"):
        return _project_test_definition(name, text, errors)
    return path.read_bytes()


def package_digest(
    feature: Path,
    names: list[str],
    errors: list[str],
    *,
    algorithm: str = RAW_STABLE_DIGEST,
) -> str:
    paths = resolve_files(feature, names, errors)
    rows = []
    for name, path in sorted(paths.items()):
        payload = stable_file_bytes(name, path, algorithm, errors)
        digest = hashlib.sha256(payload).hexdigest()
        rows.append(f"{name}\tsha256:{digest}")
    payload = ("\n".join(rows) + "\n").encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def task_metadata(
    tasks_path: Path, errors: list[str]
) -> tuple[dict[str, str | None], dict[str, set[str]]]:
    modes: dict[str, str | None] = {}
    stories: dict[str, set[str]] = {}
    current: str | None = None
    for line in tasks_path.read_text(encoding="utf-8-sig").splitlines():
        task = re.match(
            r"^\s*-\s*\[[ xX]\]\s+(T\d+)\b(?:\s+\[([^\]]+)\])?", line
        )
        if task:
            current = task.group(1)
            if current in modes:
                errors.append(f"duplicate task ID in tasks.md: {current}")
            modes[current] = None
            stories[current] = set(re.findall(r"\bUS\d+\b", task.group(2) or ""))
            continue
        mode = re.match(r"^\s*-\s*Mode:\s*(Agent-ready|Human-gated)\s*$", line)
        if current and mode:
            modes[current] = mode.group(1)
            continue
        covers = re.match(r"^\s*-\s*Covers Stories:\s*(.*?)\s*$", line)
        if current and covers:
            stories[current].update(re.findall(r"\bUS\d+\b", covers.group(1)))
    return modes, stories


def plan_scope(plan_path: Path) -> tuple[str | None, str | None, list[str]]:
    in_scope = False
    scope_type: str | None = None
    scope_id: str | None = None
    included_tasks: list[str] = []
    for line in plan_path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip() in {"Plan Scope:", "Scope:"}:
            in_scope = True
            continue
        if in_scope:
            field = re.match(r"^\s*-\s*([^:]+):\s*(.*?)\s*$", line)
            if field:
                name, value = field.group(1).strip(), field.group(2).strip()
                if name == "Type":
                    scope_type = value
                elif name == "ID":
                    scope_id = value
                elif name == "Included Tasks":
                    included_tasks = parse_list(value)
            if line.startswith("## "):
                break
    return scope_type, scope_id, included_tasks


def discovered_review_artifacts(feature: Path) -> tuple[set[str], set[str]]:
    package = {"spec.md", "tasks.md", "tests.md"}
    stable = {"spec.md", "tasks.md", "tests.md"}
    for name in ("context.md", "contracts.md"):
        if (feature / name).is_file() or (feature / name).is_symlink():
            package.add(name)
            stable.add(name)
    for directory in ("tasks", "tests", "plans", "contracts"):
        root = feature / directory
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() and not path.is_symlink():
                continue
            relative = path.relative_to(feature).as_posix()
            package.add(relative)
            if directory != "plans":
                stable.add(relative)
    return package, stable


def validate(feature: Path, mode: str) -> list[str]:
    errors: list[str] = []
    notes = feature / "notes.md"
    if not notes.is_file():
        return ["missing file: notes.md"]
    fields = parse_fields(notes)
    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            errors.append(f"missing field: {field}")
    if errors:
        return errors

    if fields["Implementation Readiness"] != "accepted":
        errors.append("Implementation Readiness must be accepted")
    if fields["Gate 1 Decision"] != "accepted":
        errors.append("Gate 1 Decision must be accepted")

    spec = feature / "spec.md"
    if not spec.is_file():
        errors.append("missing package file: spec.md")
    else:
        current_spec = "sha256:" + hashlib.sha256(spec.read_bytes()).hexdigest()
        if current_spec != fields["Gate 1 Spec Digest"]:
            errors.append("Gate 1 Spec Digest does not match spec.md")

    decision = fields["Gate 2 Decision"]
    auto_loop = fields["Feature Auto-Loop"]
    if decision not in {"package-only", "approve-and-start"}:
        errors.append("Gate 2 Decision must be package-only or approve-and-start")
    if decision == "package-only" and auto_loop != "disabled":
        errors.append("Feature Auto-Loop must be disabled for package-only")
    if decision == "approve-and-start" and auto_loop != "enabled":
        errors.append("Feature Auto-Loop must be enabled for approve-and-start")
    if mode == "start" and decision != "package-only":
        errors.append("start requires a package-only Gate 2 baseline")

    reviewed_at = fields["Gate 2 Reviewed At"]
    try:
        reviewed_time = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
        if reviewed_time.tzinfo is None:
            raise ValueError
    except ValueError:
        errors.append("Gate 2 Reviewed At must be a timezone-aware ISO-8601 timestamp")

    package_files = parse_list(fields["Gate 2 Package Files"])
    stable_files = parse_list(fields["Gate 2 Stable Files"])
    stable_algorithm = fields["Gate 2 Stable Digest Algorithm"]
    if stable_algorithm not in STABLE_DIGEST_ALGORITHMS:
        errors.append(
            "Gate 2 Stable Digest Algorithm must be raw-v1 or review-definition-v2"
        )
    required = {"spec.md", "tasks.md", "tests.md"}
    if not required.issubset(package_files):
        errors.append("Gate 2 Package Files must include spec.md,tasks.md,tests.md")
    if not {"spec.md", "tasks.md", "tests.md"}.issubset(stable_files):
        errors.append("Gate 2 Stable Files must include spec.md,tasks.md,tests.md")
    if "plan.md" in stable_files:
        errors.append("Gate 2 Stable Files must exclude rotatable plan.md")
    if not set(stable_files).issubset(package_files):
        errors.append("Gate 2 Stable Files must be a subset of Gate 2 Package Files")

    discovered_package, discovered_stable = discovered_review_artifacts(feature)
    if mode in {"review", "start"}:
        for missing in sorted(discovered_package - set(package_files)):
            errors.append(f"reviewed artifact missing from Gate 2 Package Files: {missing}")
    for missing in sorted(discovered_stable - set(stable_files)):
        errors.append(f"stable artifact missing from Gate 2 Stable Files: {missing}")

    package_errors: list[str] = []
    current_package = package_digest(feature, package_files, package_errors)
    errors.extend(package_errors)
    stable_errors: list[str] = []
    current_stable = package_digest(
        feature,
        stable_files,
        stable_errors,
        algorithm=stable_algorithm,
    )
    errors.extend(stable_errors)

    tasks = set(parse_list(fields["Gate 2 Agent-ready Tasks"]))
    active_plan = fields["Active Plan Scope"]
    if not tasks:
        errors.append("Gate 2 Agent-ready Tasks must not be empty")

    tasks_path = feature / "tasks.md"
    task_stories: dict[str, set[str]] = {}
    if tasks_path.is_file():
        modes, task_stories = task_metadata(tasks_path, errors)
        for task_id in sorted(tasks):
            if task_id not in modes:
                errors.append(f"accepted task is missing from tasks.md: {task_id}")
            elif modes[task_id] != "Agent-ready":
                errors.append(f"accepted task is not classified Agent-ready: {task_id}")

    plan_evidence = fields["Gate 2 Plan Evidence"]
    if plan_evidence.startswith("no-plan:"):
        no_plan_scope = plan_evidence.split(":", 1)[1].strip()
        if not no_plan_scope or no_plan_scope != active_plan:
            errors.append("no-plan evidence must name the Active Plan Scope")
        if active_plan not in tasks:
            errors.append("No-Plan Active Plan Scope is outside accepted Agent-ready task set")
        if "plan.md" in package_files:
            errors.append("no-plan evidence must not include plan.md in Gate 2 Package Files")
    else:
        plan_relative = Path(plan_evidence)
        valid_plan_path = (
            plan_evidence == "plan.md"
            or (
                len(plan_relative.parts) == 2
                and plan_relative.parts[0] == "plans"
                and plan_relative.suffix == ".md"
            )
        )
        if not valid_plan_path:
            errors.append(
                "Gate 2 Plan Evidence must be plan.md, plans/<detail>.md, "
                "or no-plan:<accepted task ID>"
            )
        else:
            if "plan.md" not in package_files:
                errors.append("Gate 2 Package Files must include the plan.md entry/pointer")
            if mode in {"review", "start"} and plan_evidence not in package_files:
                errors.append(
                    f"Gate 2 Package Files must include current Plan Evidence: {plan_evidence}"
                )
            resolved_plan = resolve_files(feature, [plan_evidence], errors)
            if plan_evidence in resolved_plan:
                scope_type, actual_plan_scope, included_tasks = plan_scope(
                    resolved_plan[plan_evidence]
                )
                if actual_plan_scope != active_plan:
                    errors.append(
                        f"{plan_evidence} scope {actual_plan_scope or 'missing'} does not "
                        f"match Active Plan Scope {active_plan}"
                    )
                if scope_type == "task":
                    if active_plan not in tasks:
                        errors.append(
                            "Active Plan Scope is outside accepted Agent-ready task set"
                        )
                elif scope_type == "story":
                    if not included_tasks:
                        errors.append("story Plan must name Included Tasks")
                    for task_id in included_tasks:
                        if task_id not in tasks:
                            errors.append(
                                f"story Plan includes task outside accepted "
                                f"Agent-ready task set: {task_id}"
                            )
                        elif active_plan not in task_stories.get(task_id, set()):
                            errors.append(
                                f"story Plan task {task_id} does not cover story {active_plan} "
                                "in tasks.md"
                            )
                else:
                    errors.append(f"{plan_evidence} Plan Scope Type must be task or story")

    if mode in {"review", "start"} and current_package != fields["Gate 2 Package Digest"]:
        errors.append("Gate 2 Package Digest does not match current package")
    if current_stable != fields["Gate 2 Stable Digest"]:
        errors.append("Gate 2 Stable Digest does not match current stable artifacts")
    if mode == "execute" and decision != "approve-and-start":
        errors.append("execute requires Gate 2 Decision approve-and-start")
    return errors


def digest_evidence(feature: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes = feature / "notes.md"
    if not notes.is_file():
        return [], ["missing file: notes.md"]
    fields = parse_fields(notes)
    required = (
        "Gate 2 Package Files",
        "Gate 2 Stable Files",
        "Gate 2 Stable Digest Algorithm",
    )
    for field in required:
        if not fields.get(field):
            errors.append(f"missing field: {field}")
    if errors:
        return [], errors
    algorithm = fields["Gate 2 Stable Digest Algorithm"]
    if algorithm not in STABLE_DIGEST_ALGORITHMS:
        return [], [
            "Gate 2 Stable Digest Algorithm must be raw-v1 or review-definition-v2"
        ]
    package_files = parse_list(fields["Gate 2 Package Files"])
    stable_files = parse_list(fields["Gate 2 Stable Files"])
    package_errors: list[str] = []
    package_value = package_digest(feature, package_files, package_errors)
    stable_errors: list[str] = []
    stable_value = package_digest(
        feature,
        stable_files,
        stable_errors,
        algorithm=algorithm,
    )
    errors.extend(package_errors)
    errors.extend(stable_errors)
    if errors:
        return [], errors
    return [
        f"Gate 2 Package Digest: {package_value}",
        f"Gate 2 Stable Digest Algorithm: {algorithm}",
        f"Gate 2 Stable Digest: {stable_value}",
    ], []


def main() -> int:
    configure_utf8_stdio()
    require_supported_python()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("review", "start", "execute", "digest"), required=True
    )
    parser.add_argument("feature_dir")
    args = parser.parse_args()
    feature = Path(args.feature_dir)
    if args.mode == "digest":
        evidence, errors = digest_evidence(feature)
        if errors:
            for error in errors:
                print(f"FAIL: {error}")
            return 1
        for line in evidence:
            print(line)
        return 0
    errors = validate(feature, args.mode)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: Feature review evidence is valid for mode={args.mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
