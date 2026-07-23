from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal, Sequence

from checker_support import read_text


ChangeStatus = Literal["in-progress", "completed", "stopped"]
MemoryReview = Literal["pending", "complete"]
MemoryResult = Literal["pending", "none", "synced", "human-review"]

MONTH_RE = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")
CHANGE_FILE_RE = re.compile(
    r"^(?P<date>\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))-"
    r"(?P<topic>[a-z0-9][a-z0-9-]*)\.md$"
)
REQUIRED_SECTIONS = (
    "Background",
    "Goal / Completion Criteria",
    "Scope",
    "Lane Rationale",
    "Impact / Risk",
    "Plan",
    "Current Progress",
    "Verification",
    "Rollback",
    "Human Gates",
    "Result / Residuals",
    "Memory",
)

MAX_CHANGE_BYTES = 1024 * 1024
HEADER_FIELDS = (
    "Record Version",
    "Status",
    "Created At",
    "Updated At",
    "Completed At",
    "Git Context",
)
MEMORY_FIELDS = (
    "Memory Review",
    "Memory Result",
    "Memory Evidence",
    "Memory Target",
)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
H2_RE = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.MULTILINE)
AUTHORING_MARKER_RE = re.compile(r"<replace(?:[-\s][^>\n]*)?>", re.IGNORECASE)
OPEN_FENCE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")


@dataclass(frozen=True)
class LightweightChangeContractError(Exception):
    category: str
    detail: str
    exit_code: int = 1

    def __str__(self) -> str:
        return f"{self.category}: {self.detail}"

    def to_payload(self) -> dict[str, object]:
        return {
            "error": {"category": self.category, "detail": self.detail},
            "result": "invalid",
            "schema_version": 1,
        }


@dataclass(frozen=True)
class LightweightChange:
    path: str
    topic: str
    status: ChangeStatus
    created_at: date
    updated_at: date
    completed_at: date | None
    memory_review: MemoryReview
    memory_result: MemoryResult


@dataclass(frozen=True)
class LightweightChangeScan:
    schema_version: int
    as_of: date
    memory_root: str | None
    changes_root: str | None
    changes: Sequence[LightweightChange]

    def to_payload(self) -> dict[str, object]:
        ordered = tuple(sorted(self.changes, key=lambda item: item.path))
        pending = tuple(
            item
            for item in ordered
            if item.status == "completed" and item.memory_review == "pending"
        )
        human_review = tuple(
            item
            for item in ordered
            if item.status == "completed" and item.memory_result == "human-review"
        )
        pending_rows = [self._pending_row(item) for item in pending]
        human_review_rows = [self._human_review_row(item) for item in human_review]
        oldest = min(
            pending,
            key=lambda item: (self._completed(item), item.path),
            default=None,
        )
        reasons: list[str] = []
        if len(pending) >= 3:
            reasons.append("pending-count")
        if oldest is not None and (self.as_of - self._completed(oldest)).days > 7:
            reasons.append("pending-age")
        reasons.sort()
        counts = {
            "completed": sum(item.status == "completed" for item in ordered),
            "human_review": len(human_review),
            "in_progress": sum(item.status == "in-progress" for item in ordered),
            "pending": len(pending),
            "stopped": sum(item.status == "stopped" for item in ordered),
            "total": len(ordered),
        }
        return {
            "as_of": self.as_of.isoformat(),
            "changes_root": self.changes_root,
            "counts": counts,
            "human_review_changes": human_review_rows,
            "memory_root": self.memory_root,
            "oldest_pending": self._pending_row(oldest) if oldest is not None else None,
            "pending_changes": pending_rows,
            "result": "triggered" if reasons else "not-triggered",
            "schema_version": self.schema_version,
            "trigger_reasons": reasons,
        }

    def _completed(self, item: LightweightChange) -> date:
        if item.completed_at is None:
            raise AssertionError(f"pending Change lacks Completed At: {item.path}")
        return item.completed_at

    def _pending_row(self, item: LightweightChange) -> dict[str, object]:
        completed = self._completed(item)
        return {
            "age_days": (self.as_of - completed).days,
            "completed_at": completed.isoformat(),
            "path": item.path,
            "topic": item.topic,
        }

    @staticmethod
    def _human_review_row(item: LightweightChange) -> dict[str, object]:
        if item.completed_at is None:
            raise AssertionError(f"human-review Change lacks Completed At: {item.path}")
        return {
            "completed_at": item.completed_at.isoformat(),
            "path": item.path,
            "topic": item.topic,
        }


def _error(category: str, path: str, rule: str) -> LightweightChangeContractError:
    return LightweightChangeContractError(category, f"{path}: {rule}")


def _relative(project_root: Path, path: Path) -> str:
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError as error:
        raise _error("layout", path.name, "path escapes project root") from error


def _real_directory(path: Path) -> bool:
    return path.exists() and path.is_dir() and not path.is_symlink()


def _sorted_directory_entries(path: Path, relative: str) -> tuple[Path, ...]:
    try:
        return tuple(sorted(path.iterdir(), key=lambda item: item.name))
    except OSError as error:
        raise _error("layout", relative, "directory cannot be enumerated") from error


def discover_memory_root(project_root: Path) -> Path | None:
    if not project_root.exists() or not project_root.is_dir():
        raise LightweightChangeContractError(
            "memory-root", "project root must exist and be a directory", exit_code=2
        )
    if project_root.is_symlink():
        raise LightweightChangeContractError(
            "memory-root", "project root symlink is outside the requested boundary", exit_code=2
        )
    project_root = project_root.resolve()
    candidates = (project_root / ".agent-loop", project_root / "agent-loop")
    present: list[Path] = []
    for candidate in candidates:
        if candidate.is_symlink():
            raise _error("memory-root", candidate.name, "accepted root must not be a symlink")
        if candidate.exists() and not candidate.is_dir():
            raise _error("memory-root", candidate.name, "accepted root must be a directory")
        if _real_directory(candidate):
            present.append(candidate)
    if len(present) == 2:
        raise LightweightChangeContractError(
            "memory-root", "both .agent-loop and agent-loop exist; root ownership is ambiguous"
        )
    return present[0] if present else None


def _parse_date(value: str, path: str, field: str) -> date:
    if not ISO_DATE_RE.fullmatch(value):
        raise _error("date", path, f"{field} must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise _error("date", path, f"{field} is not a real calendar date") from error


def _mask_fenced_code(text: str) -> str:
    masked: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        mask_line = fence_character is not None
        if fence_character is None:
            opening = OPEN_FENCE_RE.fullmatch(body)
            if opening is not None:
                marker = opening.group("fence")
                info = opening.group("info")
                if marker[0] != "`" or "`" not in info:
                    fence_character = marker[0]
                    fence_length = len(marker)
                    mask_line = True
        else:
            closing = re.fullmatch(
                rf" {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*",
                body,
            )
            if closing is not None:
                fence_character = None
                fence_length = 0
        if mask_line:
            masked.append(
                "".join(
                    character if character in "\r\n" else " " for character in line
                )
            )
        else:
            masked.append(line)
    return "".join(masked)


def _metadata_values(text: str, fields: Sequence[str]) -> dict[str, str]:
    structural_text = _mask_fenced_code(text)
    values: dict[str, str] = {}
    for field in fields:
        matches = re.findall(
            rf"(?m)^{re.escape(field)}:[ \t]*(.*?)[ \t]*$", structural_text
        )
        if len(matches) != 1:
            raise LightweightChangeContractError(
                "metadata", f"{field}: expected exactly one value, found {len(matches)}"
            )
        value = matches[0].strip()
        if not value:
            raise LightweightChangeContractError("metadata", f"{field}: value must not be blank")
        values[field] = value
    return values


def _sections(text: str, path: str, structural_text: str) -> dict[str, str]:
    matches = list(H2_RE.finditer(structural_text))
    by_name: dict[str, list[str]] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        by_name.setdefault(name, []).append(text[start:end].strip())
    result: dict[str, str] = {}
    for name in REQUIRED_SECTIONS:
        bodies = by_name.get(name, [])
        if len(bodies) != 1:
            raise _error("metadata", path, f"section {name} must occur exactly once")
        body = bodies[0]
        if not body:
            raise _error("metadata", path, f"section {name} must not be blank")
        if body == "none":
            raise _error("metadata", path, f"section {name} requires a concrete none reason")
        result[name] = body
    return result


def _validate_no_authoring_markers(text: str, path: str) -> None:
    if AUTHORING_MARKER_RE.search(text):
        raise _error("metadata", path, "authoring placeholder must be replaced")


def _valid_git_context(value: str) -> bool:
    if value == "no-git":
        return True
    branch, separator, full_sha = value.rpartition("@")
    return bool(
        separator
        and branch
        and not any(character.isspace() for character in branch)
        and FULL_SHA_RE.fullmatch(full_sha)
    )


def _validate_memory(
    *,
    path: str,
    status: str,
    review: str,
    result: str,
    evidence: str,
    target: str,
) -> None:
    if review not in {"pending", "complete"}:
        raise _error("state", path, "Memory Review is invalid")
    if result not in {"pending", "none", "synced", "human-review"}:
        raise _error("state", path, "Memory Result is invalid")
    if review == "pending" and result != "pending":
        raise _error("state", path, "pending Memory Review requires pending result")
    if review == "complete" and result == "pending":
        raise _error("state", path, "complete Memory Review cannot use pending result")
    if result == "none":
        if not evidence.startswith("none: ") or len(evidence.removeprefix("none: ").strip()) < 3:
            raise _error("metadata", path, "Memory Evidence none requires a concrete reason")
        if not target.startswith("none: ") or len(target.removeprefix("none: ").strip()) < 3:
            raise _error("metadata", path, "Memory Target none requires a concrete reason")

    initial_evidence = "pending: verification not complete"
    initial_target = "pending: classify at completion"
    if status == "in-progress":
        if (review, result) != ("pending", "pending"):
            raise _error("state", path, "in-progress requires pending/pending memory")
        if evidence != initial_evidence or target != initial_target:
            raise _error("state", path, "in-progress requires initial pending markers")
    elif status == "stopped":
        if (review, result) != ("complete", "none"):
            raise _error("state", path, "stopped requires complete/none memory")
    elif status == "completed":
        if evidence in {initial_evidence, initial_target} or target in {
            initial_evidence,
            initial_target,
        }:
            raise _error("state", path, "completed cannot retain initial pending markers")
        if result == "pending" and (
            evidence.startswith(("pending:", "none:"))
            or target.startswith(("pending:", "none:"))
        ):
            raise _error(
                "state",
                path,
                "completed pending memory requires actual verification and candidate target evidence",
            )
        if result in {"synced", "human-review"} and (
            evidence.startswith(("pending:", "none:"))
            or target.startswith(("pending:", "none:"))
        ):
            raise _error(
                "state",
                path,
                f"{result} requires concrete evidence and target",
            )


def parse_change(
    memory_root: Path, path: Path, *, as_of: date
) -> LightweightChange:
    project_root = memory_root.parent.resolve()
    relative = _relative(project_root, path)
    if path.is_symlink() or not path.is_file():
        raise _error("layout", relative, "Change must be a regular non-symlink file")
    try:
        size = path.stat().st_size
    except OSError as error:
        raise _error("metadata", relative, "cannot read Change metadata") from error
    if size > MAX_CHANGE_BYTES:
        raise _error("size", relative, "Change exceeds 1 MiB")
    try:
        text = read_text(path)
    except (OSError, UnicodeError) as error:
        raise _error("metadata", relative, "Change must be readable UTF-8 text") from error
    structural_text = _mask_fenced_code(text)
    _validate_no_authoring_markers(structural_text, relative)

    filename_match = CHANGE_FILE_RE.fullmatch(path.name)
    if filename_match is None:
        raise _error("layout", relative, "invalid Change filename")
    if path.parent.parent.name != "changes" or path.parent.parent.parent != memory_root:
        raise _error("layout", relative, "Change must be exactly below one month directory")
    month = path.parent.name
    if MONTH_RE.fullmatch(month) is None:
        raise _error("layout", relative, "invalid month directory")

    first_h2 = H2_RE.search(structural_text)
    header = structural_text[: first_h2.start()] if first_h2 else structural_text
    h1_matches = re.findall(r"(?m)^# Lightweight Change: ([a-z0-9][a-z0-9-]*)[ \t]*$", header)
    if len(h1_matches) != 1:
        raise _error("metadata", relative, "H1 must occur exactly once with a valid topic")
    topic = filename_match.group("topic")
    if h1_matches[0] != topic:
        raise _error("metadata", relative, "H1 topic must equal filename topic")

    try:
        header_values = _metadata_values(header, HEADER_FIELDS)
    except LightweightChangeContractError as error:
        raise _error(error.category, relative, error.detail) from error
    sections = _sections(text, relative, structural_text)
    try:
        memory_values = _metadata_values(sections["Memory"], MEMORY_FIELDS)
    except LightweightChangeContractError as error:
        raise _error(error.category, relative, error.detail) from error

    if header_values["Record Version"] != "1":
        raise _error("metadata", relative, "Record Version must be 1")
    status = header_values["Status"]
    if status not in {"in-progress", "completed", "stopped"}:
        raise _error("state", relative, "Status is invalid")

    created = _parse_date(header_values["Created At"], relative, "Created At")
    updated = _parse_date(header_values["Updated At"], relative, "Updated At")
    completed_value = header_values["Completed At"]
    completed = (
        None
        if completed_value == "none"
        else _parse_date(completed_value, relative, "Completed At")
    )
    filename_date = _parse_date(filename_match.group("date"), relative, "filename date")
    if filename_date != created:
        raise _error("date", relative, "filename date must equal Created At")
    if month != created.strftime("%Y-%m"):
        raise _error("date", relative, "month directory must equal Created At month")
    if created > updated or updated > as_of:
        raise _error("date", relative, "requires Created At <= Updated At <= as-of")
    if status == "completed":
        if completed is None:
            raise _error("state", relative, "completed requires Completed At")
        if not created <= completed <= updated:
            raise _error(
                "date", relative, "requires Created At <= Completed At <= Updated At"
            )
    elif completed is not None:
        raise _error("state", relative, f"{status} requires Completed At: none")
    if completed is not None and completed > as_of:
        raise _error("date", relative, "Completed At must not be after as-of")

    git_context = header_values["Git Context"]
    if not _valid_git_context(git_context):
        raise _error("metadata", relative, "Git Context must be no-git or branch@full-sha")

    review = memory_values["Memory Review"]
    memory_result = memory_values["Memory Result"]
    _validate_memory(
        path=relative,
        status=status,
        review=review,
        result=memory_result,
        evidence=memory_values["Memory Evidence"],
        target=memory_values["Memory Target"],
    )

    return LightweightChange(
        path=relative,
        topic=topic,
        status=status,
        created_at=created,
        updated_at=updated,
        completed_at=completed,
        memory_review=review,
        memory_result=memory_result,
    )


def build_scan(project_root: Path, *, as_of: date) -> LightweightChangeScan:
    memory_root = discover_memory_root(project_root)
    resolved_project = project_root.resolve()
    if memory_root is None:
        return LightweightChangeScan(1, as_of, None, None, ())

    memory_relative = _relative(resolved_project, memory_root)
    changes_root = memory_root / "changes"
    if changes_root.is_symlink():
        raise _error("layout", f"{memory_relative}/changes", "changes root must not be a symlink")
    if not changes_root.exists():
        return LightweightChangeScan(1, as_of, memory_relative, None, ())
    if not changes_root.is_dir():
        raise _error("layout", f"{memory_relative}/changes", "changes root must be a directory")

    records: list[LightweightChange] = []
    for month_path in _sorted_directory_entries(changes_root, f"{memory_relative}/changes"):
        month_relative = _relative(resolved_project, month_path)
        if month_path.is_symlink() or not month_path.is_dir():
            raise _error("layout", month_relative, "changes root may contain only real month directories")
        if MONTH_RE.fullmatch(month_path.name) is None:
            raise _error("layout", month_relative, "invalid month directory")
        for candidate in _sorted_directory_entries(month_path, month_relative):
            candidate_relative = _relative(resolved_project, candidate)
            if candidate.is_symlink():
                raise _error("layout", candidate_relative, "symlinked Change artifacts are forbidden")
            if candidate.is_dir():
                raise _error("layout", candidate_relative, "extra Change directory depth is forbidden")
            if not candidate.is_file():
                raise _error("layout", candidate_relative, "unsupported Change artifact kind")
            if candidate.suffix.lower() != ".md":
                continue
            if CHANGE_FILE_RE.fullmatch(candidate.name) is None:
                raise _error("layout", candidate_relative, "invalid Change Markdown filename")
            records.append(parse_change(memory_root, candidate, as_of=as_of))

    return LightweightChangeScan(
        schema_version=1,
        as_of=as_of,
        memory_root=memory_relative,
        changes_root=_relative(resolved_project, changes_root),
        changes=tuple(sorted(records, key=lambda item: item.path)),
    )
