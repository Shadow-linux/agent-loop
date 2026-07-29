from __future__ import annotations

import errno
import json
import os
import re
import secrets
import shutil
import unicodedata
from dataclasses import asdict, dataclass, replace
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Literal, Mapping, Sequence
from urllib.parse import unquote, urlsplit, urlunsplit

from checker_support import (
    atomic_write_bytes,
    canonical_json_bytes,
    CheckFailure,
    discover_memory_root_authority,
    metadata,
    optional_section,
    read_text,
    sha256_bytes,
    strip_code_span,
)


FEATURE_ID_RE = re.compile(
    r"^(?P<month>\d{4}-(?:0[1-9]|1[0-2]))-(?P<day>0[1-9]|[12]\d|3[01])-[a-z0-9][a-z0-9-]*$"
)
MONTH_RE = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
ARCHIVE_COLUMNS = (
    "Feature ID",
    "Month",
    "Current Path",
    "Archive State",
    "Closed At",
    "Delivered Summary",
    "Source Requirements",
    "Applicable Decisions",
    "Last Moved At",
)
ARCHIVE_STATES = frozenset({"archived", "rehydrated"})
UTF8_BOM = b"\xef\xbb\xbf"
MAX_MARKDOWN_BYTES = 2 * 1024 * 1024
EXCLUDED_SCAN_DIRS = frozenset(
    {".git", ".archive-txn", "node_modules", "vendor", ".venv", "dist", "build"}
)
TRANSACTION_ID_RE = re.compile(r"^\d{8}T\d{6}Z-[0-9a-f]{12}$")
JOURNAL_STATES = frozenset(
    {
        "prepared",
        "moving",
        "references-updated",
        "checking",
        "restoring",
        "restored",
        "verified",
    }
)
ARCHIVE_TEMPLATE = """# Feature Archive

This file locates archived or rehydrated features. Feature specs, tests, notes, requirement sources, and accepted decisions remain authoritative.

| Feature ID | Month | Current Path | Archive State | Closed At | Delivered Summary | Source Requirements | Applicable Decisions | Last Moved At |
|---|---|---|---|---|---|---|---|---|
"""


@dataclass(frozen=True)
class ArchiveContractError(Exception):
    category: str
    detail: str
    exit_code: int = 1

    def __str__(self) -> str:
        return f"{self.category}: {self.detail}"


@dataclass(frozen=True)
class FeatureLocation:
    feature_id: str
    relative_path: str
    layout: Literal["flat", "archived"]
    month: str | None


@dataclass(frozen=True)
class ArchiveEntry:
    feature_id: str
    month: str
    current_path: str
    archive_state: Literal["archived", "rehydrated"]
    closed_at: str
    delivered_summary: str
    source_requirements: str
    applicable_decisions: str
    last_moved_at: str


@dataclass(frozen=True)
class ReferenceEdit:
    path: str
    kind: Literal["literal-path", "relative-link", "archive-index"]
    old: str
    new: str
    occurrences: int
    before_sha256: str
    after_sha256: str


@dataclass(frozen=True)
class SkippedReference:
    path: str
    classification: Literal[
        "immutable-requirement-source",
        "historical-evidence",
        "unsupported",
        "reference-scan-symlink",
        "feature-entry-symlink",
        "memory-root-alias",
    ]
    matched_value: str
    reason: str


@dataclass(frozen=True)
class Move:
    feature_id: str
    month: str
    source: str
    target: str


@dataclass(frozen=True)
class ArchiveCandidate:
    feature_id: str
    month: str
    current_path: str
    lifecycle: str
    close_evidence: Literal["complete", "incomplete"]
    open_follow_up: str
    delivered_summary: str
    source_requirements: str
    applicable_decisions: str
    blockers: Sequence[str]

    def __post_init__(self) -> None:
        object.__setattr__(self, "blockers", tuple(sorted(self.blockers)))


@dataclass(frozen=True)
class ArchivePlan:
    schema_version: int
    operation: Literal["archive", "rehydrate"]
    as_of: str
    selected_months: Sequence[str]
    selected_feature_ids: Sequence[str]
    candidates: Sequence[ArchiveCandidate]
    moves: Sequence[Move]
    archive_entries: Sequence[ArchiveEntry]
    reference_edits: Sequence[ReferenceEdit]
    skipped_references: Sequence[SkippedReference]
    snapshots: Mapping[str, str]

    def __post_init__(self) -> None:
        object.__setattr__(self, "selected_months", tuple(self.selected_months))
        object.__setattr__(self, "selected_feature_ids", tuple(self.selected_feature_ids))
        object.__setattr__(self, "candidates", tuple(self.candidates))
        object.__setattr__(self, "moves", tuple(self.moves))
        object.__setattr__(self, "archive_entries", tuple(self.archive_entries))
        object.__setattr__(self, "reference_edits", tuple(self.reference_edits))
        object.__setattr__(self, "skipped_references", tuple(self.skipped_references))
        object.__setattr__(
            self,
            "snapshots",
            MappingProxyType(dict(sorted(self.snapshots.items()))),
        )

    def to_payload(self, include_hash: bool = True) -> dict[str, object]:
        payload: dict[str, object] = {
            "schema_version": self.schema_version,
            "operation": self.operation,
            "as_of": self.as_of,
            "selected_months": sorted(set(self.selected_months)),
            "selected_feature_ids": sorted(set(self.selected_feature_ids)),
            "candidates": [
                asdict(item)
                for item in sorted(
                    self.candidates, key=lambda item: (item.month, item.feature_id)
                )
            ],
            "moves": [
                asdict(item)
                for item in sorted(
                    self.moves,
                    key=lambda item: (
                        item.month,
                        item.feature_id,
                        item.source,
                        item.target,
                    ),
                )
            ],
            "archive_entries": [
                asdict(item)
                for item in sorted(
                    self.archive_entries,
                    key=lambda item: (item.month, item.feature_id),
                )
            ],
            "reference_edits": [
                asdict(item)
                for item in sorted(
                    self.reference_edits,
                    key=lambda item: (item.path, item.kind, item.old, item.new),
                )
            ],
            "skipped_references": [
                asdict(item)
                for item in sorted(
                    self.skipped_references,
                    key=lambda item: (
                        item.path,
                        item.classification,
                        item.matched_value,
                    ),
                )
            ],
            "snapshots": dict(sorted(self.snapshots.items())),
        }
        if include_hash:
            payload["plan_sha256"] = self.computed_sha256()
        return payload

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.to_payload(include_hash=False))

    def computed_sha256(self) -> str:
        return sha256_bytes(self.canonical_bytes())

    def assert_hash(self, expected: str) -> None:
        if not HASH_RE.fullmatch(expected):
            raise ArchiveContractError(
                "usage", "expected plan SHA-256 must be 64 lowercase hex characters", 2
            )
        actual = self.computed_sha256()
        if actual != expected:
            raise ArchiveContractError(
                "stale-plan", f"expected {expected}, rebuilt {actual}"
            )


def discover_memory_root(project_root: Path) -> Path:
    try:
        authority = discover_memory_root_authority(project_root)
    except CheckFailure as error:
        exit_code = 2 if "no agent-loop memory root" in error.detail else 1
        raise ArchiveContractError("memory-root", error.detail, exit_code) from error
    if authority is None:
        raise AssertionError("required memory root discovery returned none")
    return authority.logical


def _split_row(line: str) -> list[str]:
    value = line.strip()
    if not value.startswith("|") or not value.endswith("|"):
        raise ArchiveContractError("archive-index", f"invalid table row: {line}")
    return [cell.strip() for cell in value[1:-1].split("|")]


def _feature_month(feature_id: str) -> str:
    match = FEATURE_ID_RE.fullmatch(feature_id)
    if not match:
        raise ArchiveContractError("feature-id", f"invalid Feature ID: {feature_id}")
    return match.group("month")


def _memory_relative_from_current_path(value: str) -> str:
    cleaned = strip_code_span(value).strip().rstrip("/")
    if "\\" in cleaned:
        raise ArchiveContractError(
            "archive-index", f"Current Path must use POSIX separators: {value}"
        )
    pure = PurePosixPath(cleaned)
    if pure.is_absolute() or ".." in pure.parts:
        raise ArchiveContractError("path-escape", f"unsafe Current Path: {value}")
    parts = pure.parts
    if parts and parts[0] in {".agent-loop", "agent-loop"}:
        parts = parts[1:]
    relative = PurePosixPath(*parts).as_posix()
    if not relative.startswith("features/"):
        raise ArchiveContractError(
            "archive-index", f"Current Path must locate features/: {value}"
        )
    return relative


def _validate_entry(entry: ArchiveEntry) -> str:
    feature_month = _feature_month(entry.feature_id)
    if not MONTH_RE.fullmatch(entry.month) or entry.month != feature_month:
        raise ArchiveContractError(
            "month",
            f"Feature ID {entry.feature_id} requires month {feature_month}, got {entry.month}",
        )
    if entry.archive_state not in ARCHIVE_STATES:
        raise ArchiveContractError(
            "archive-index", f"unknown Archive State: {entry.archive_state}"
        )
    relative = _memory_relative_from_current_path(entry.current_path)
    archived = f"features/{entry.month}/{entry.feature_id}"
    flat = f"features/{entry.feature_id}"
    if entry.archive_state == "archived" and relative != archived:
        path_parts = PurePosixPath(relative).parts
        if len(path_parts) >= 3 and MONTH_RE.fullmatch(path_parts[1]):
            raise ArchiveContractError(
                "month", f"archived path month does not match {entry.feature_id}: {relative}"
            )
        raise ArchiveContractError(
            "archive-index", f"archived row must point to {archived}: {relative}"
        )
    if entry.archive_state == "rehydrated" and relative != flat:
        raise ArchiveContractError(
            "archive-index", f"rehydrated row must point to {flat}: {relative}"
        )
    return relative


def parse_archive_index(memory_root: Path) -> Sequence[ArchiveEntry]:
    index = memory_root / "features" / "archive.md"
    if not index.exists():
        return ()
    if not index.is_file():
        raise ArchiveContractError("archive-index", f"not a file: {index}")
    lines = read_text(index).splitlines()
    header_at = None
    for position, line in enumerate(lines):
        if line.strip().startswith("|") and tuple(_split_row(line)) == ARCHIVE_COLUMNS:
            header_at = position
            break
    if header_at is None or header_at + 1 >= len(lines):
        raise ArchiveContractError("archive-index", "missing accepted archive table header")
    separator = _split_row(lines[header_at + 1])
    if len(separator) != len(ARCHIVE_COLUMNS) or not all(
        re.fullmatch(r":?-{3,}:?", cell) for cell in separator
    ):
        raise ArchiveContractError("archive-index", "invalid archive table separator")

    entries: list[ArchiveEntry] = []
    for line in lines[header_at + 2 :]:
        if not line.strip():
            continue
        if not line.strip().startswith("|"):
            break
        cells = _split_row(line)
        if len(cells) != len(ARCHIVE_COLUMNS):
            raise ArchiveContractError("archive-index", "archive row column mismatch")
        row = dict(zip(ARCHIVE_COLUMNS, cells, strict=True))
        entry = ArchiveEntry(
            feature_id=strip_code_span(row["Feature ID"]),
            month=strip_code_span(row["Month"]),
            current_path=strip_code_span(row["Current Path"]),
            archive_state=strip_code_span(row["Archive State"]),
            closed_at=strip_code_span(row["Closed At"]),
            delivered_summary=row["Delivered Summary"].strip(),
            source_requirements=strip_code_span(row["Source Requirements"]),
            applicable_decisions=strip_code_span(row["Applicable Decisions"]),
            last_moved_at=strip_code_span(row["Last Moved At"]),
        )
        _validate_entry(entry)
        entries.append(entry)

    feature_ids: set[str] = set()
    normalized_paths: set[str] = set()
    for entry in entries:
        if entry.feature_id in feature_ids:
            raise ArchiveContractError(
                "archive-index", f"duplicate Feature ID: {entry.feature_id}"
            )
        feature_ids.add(entry.feature_id)
        relative = _memory_relative_from_current_path(entry.current_path)
        normalized = unicodedata.normalize("NFKC", relative).casefold()
        if normalized in normalized_paths:
            raise ArchiveContractError(
                "archive-index", f"duplicate normalized Current Path: {relative}"
            )
        normalized_paths.add(normalized)
    return tuple(sorted(entries, key=lambda item: (item.month, item.feature_id)))


def _one_line(value: str) -> str:
    return " ".join(value.replace("|", "&#124;").split())


def _locator(value: str) -> str:
    cleaned = _one_line(value)
    return cleaned if cleaned.lower() == "none" else f"`{cleaned}`"


def render_archive_index(entries: Sequence[ArchiveEntry]) -> str:
    rows: list[str] = []
    seen: list[ArchiveEntry] = []
    for entry in sorted(entries, key=lambda item: (item.month, item.feature_id)):
        _validate_entry(entry)
        seen.append(entry)
        rows.append(
            "| "
            + " | ".join(
                (
                    entry.feature_id,
                    entry.month,
                    f"`{_one_line(entry.current_path)}`",
                    entry.archive_state,
                    _one_line(entry.closed_at),
                    _one_line(entry.delivered_summary),
                    _locator(entry.source_requirements),
                    _locator(entry.applicable_decisions),
                    _one_line(entry.last_moved_at),
                )
            )
            + " |"
        )
    if len({item.feature_id for item in seen}) != len(seen):
        raise ArchiveContractError("archive-index", "duplicate Feature ID while rendering")
    return ARCHIVE_TEMPLATE + (("\n".join(rows) + "\n") if rows else "")


def _project_root_for(memory_root: Path) -> Path:
    return (
        memory_root.parent
        if memory_root.name in {".agent-loop", "agent-loop"}
        else memory_root
    )


def _confined_path(root: Path, relative: str) -> Path:
    if not relative or "\\" in relative:
        raise ArchiveContractError("path-escape", f"unsafe workspace path: {relative}")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise ArchiveContractError("path-escape", f"unsafe workspace path: {relative}")
    boundary = root.resolve()
    candidate = root / pure
    try:
        candidate.resolve().relative_to(boundary)
    except ValueError as error:
        raise ArchiveContractError("path-escape", f"unsafe workspace path: {relative}") from error
    return candidate


def _confined_existing_directory(memory_root: Path, relative: str) -> Path:
    candidate = memory_root / PurePosixPath(relative)
    boundary = _project_root_for(memory_root).resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(boundary)
    except ValueError as error:
        raise ArchiveContractError("path-escape", relative) from error
    if not candidate.is_dir():
        raise ArchiveContractError("archive-index", f"missing directory: {relative}")
    return candidate


def resolve_feature_location(memory_root: Path, feature_id: str) -> FeatureLocation:
    expected_month = _feature_month(feature_id)
    features_root = memory_root / "features"
    flat = features_root / feature_id
    month_locations = tuple(
        child / feature_id
        for child in sorted(features_root.iterdir() if features_root.is_dir() else ())
        if child.is_dir() and MONTH_RE.fullmatch(child.name) and (child / feature_id).exists()
    )
    entries = parse_archive_index(memory_root)
    matching = tuple(entry for entry in entries if entry.feature_id == feature_id)

    if flat.exists():
        conflicting_rows = tuple(
            entry
            for entry in matching
            if entry.archive_state != "rehydrated"
            or _memory_relative_from_current_path(entry.current_path)
            != f"features/{feature_id}"
        )
        if month_locations or conflicting_rows:
            raise ArchiveContractError(
                "path-collision", f"flat and archived locations exist for {feature_id}"
            )
        _confined_existing_directory(memory_root, f"features/{feature_id}")
        return FeatureLocation(feature_id, f"features/{feature_id}", "flat", None)

    if len(month_locations) > 1:
        raise ArchiveContractError(
            "path-collision", f"multiple archived locations exist for {feature_id}"
        )
    if month_locations and month_locations[0].parent.name != expected_month:
        raise ArchiveContractError(
            "month",
            f"Feature ID {feature_id} is under {month_locations[0].parent.name}",
        )
    if len(matching) != 1:
        raise ArchiveContractError(
            "archive-index", f"expected one locator row for {feature_id}, got {len(matching)}"
        )
    entry = matching[0]
    relative = _validate_entry(entry)
    if entry.archive_state != "archived":
        raise ArchiveContractError(
            "archive-index", f"rehydrated feature is missing flat path: {feature_id}"
        )
    _confined_existing_directory(memory_root, relative)
    if not month_locations:
        raise ArchiveContractError(
            "archive-index", f"locator row target is not discoverable: {relative}"
        )
    expected_relative = f"features/{expected_month}/{feature_id}"
    if relative != expected_relative:
        raise ArchiveContractError(
            "archive-index", f"locator path mismatch: {relative}"
        )
    return FeatureLocation(feature_id, relative, "archived", expected_month)


def _read_optional(path: Path) -> str:
    return read_text(path) if path.is_file() else ""


def _read_utf8_preserving(path: Path) -> tuple[str, bool]:
    content = path.read_bytes()
    has_bom = content.startswith(UTF8_BOM)
    payload = content[len(UTF8_BOM) :] if has_bom else content
    return payload.decode("utf-8"), has_bom


def _encode_utf8_preserving(content: str, has_bom: bool) -> bytes:
    encoded = content.encode("utf-8")
    return UTF8_BOM + encoded if has_bom else encoded


def _concrete_summary(value: str) -> bool:
    cleaned = strip_code_span(value).strip()
    if not cleaned or re.fullmatch(
        r"(?:none|n/a|na|tbd|todo|unknown|-)", cleaned, re.IGNORECASE
    ):
        return False
    return not re.search(r"<[^>]+>", cleaned)


def _readiness_values(notes: str) -> dict[str, str]:
    body = optional_section(notes, "Archive Readiness")
    if body is None:
        return {}
    names = (
        "Closed At",
        "Delivered Summary",
        "Verification",
        "Feature Close Review",
        "Drift",
        "Project Memory Impact",
        "Open Follow-up",
    )
    return {name: (metadata(body, name) or "").strip() for name in names}


def inspect_feature(
    memory_root: Path, feature_id: str, as_of: date
) -> ArchiveCandidate:
    month = _feature_month(feature_id)
    location = resolve_feature_location(memory_root, feature_id)
    root = memory_root / PurePosixPath(location.relative_path)
    spec = _read_optional(root / "spec.md")
    tasks = _read_optional(root / "tasks.md")
    notes = _read_optional(root / "notes.md")
    project = _read_optional(memory_root / "project.md")
    lifecycle = (metadata(spec, "Status") or "missing").strip()
    blockers: list[str] = []
    if root.is_symlink():
        blockers.append("feature-entry-symlink")
    if (memory_root / "features").is_symlink():
        blockers.append("features-container-symlink")
    if lifecycle != "closed":
        blockers.append(f"lifecycle:{lifecycle}")
    if month == as_of.strftime("%Y-%m"):
        blockers.append("current-month")

    close_record = optional_section(notes, "Close Record")
    close_at = metadata(close_record or "", "Closed At") or ""
    task_statuses = re.findall(r"(?mi)^\s*-?\s*Status\s*:\s*([^\n]+)", tasks)
    task_complete = bool(task_statuses) and all(
        status.strip() in {"done", "skipped"} for status in task_statuses
    )
    readiness = _readiness_values(notes)
    if not readiness:
        blockers.append("missing-archive-readiness")
    delivered_summary = readiness.get("Delivered Summary", "")
    if readiness and not _concrete_summary(delivered_summary):
        blockers.append("non-concrete-delivered-summary")
    required_values = {
        "Verification": {"complete"},
        "Feature Close Review": {"complete"},
        "Drift": {"resolved"},
        "Project Memory Impact": {"complete", "none"},
    }
    for name, allowed in required_values.items():
        actual = readiness.get(name, "")
        if readiness and actual not in allowed:
            blockers.append(
                f"archive-readiness-{name.lower().replace(' ', '-')}:{actual or 'missing'}"
            )
    readiness_closed_at = readiness.get("Closed At", "")
    if readiness and (
        not re.fullmatch(r"\d{4}-\d{2}-\d{2}", readiness_closed_at)
        or readiness_closed_at != close_at
    ):
        blockers.append("archive-readiness-closed-at")
    open_follow_up = readiness.get("Open Follow-up", "") or "unknown"
    if readiness and open_follow_up != "none":
        blockers.append(f"open-follow-up:{open_follow_up}")

    close_complete = bool(
        close_record
        and re.fullmatch(r"\d{4}-\d{2}-\d{2}", close_at)
        and task_complete
        and readiness
        and not any(
            blocker.startswith("archive-readiness")
            or blocker in {
                "missing-archive-readiness",
                "non-concrete-delivered-summary",
            }
            for blocker in blockers
        )
    )
    if not close_complete:
        blockers.append("incomplete-close-evidence")

    active = strip_code_span(metadata(project, "Active Feature") or "")
    paused = strip_code_span(metadata(project, "Paused Features") or "")
    if active and active.lower() != "none" and feature_id in active:
        blockers.append("project-memory-active")
    if paused and paused.lower() != "none" and feature_id in paused:
        blockers.append("project-memory-paused")

    return ArchiveCandidate(
        feature_id=feature_id,
        month=month,
        current_path=location.relative_path,
        lifecycle=lifecycle,
        close_evidence="complete" if close_complete else "incomplete",
        open_follow_up=open_follow_up,
        delivered_summary=delivered_summary,
        source_requirements=strip_code_span(
            metadata(spec, "Source Requirements") or "none"
        ),
        applicable_decisions=strip_code_span(
            metadata(spec, "Applicable Decisions") or "none"
        ),
        blockers=tuple(sorted(set(blockers))),
    )


def discover_flat_features(memory_root: Path) -> Sequence[FeatureLocation]:
    root = memory_root / "features"
    if not root.is_dir():
        return ()
    locations: list[FeatureLocation] = []
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        if child.is_dir() and FEATURE_ID_RE.fullmatch(child.name):
            locations.append(
                FeatureLocation(child.name, f"features/{child.name}", "flat", None)
            )
    return tuple(locations)


def _resolve_link_target_after_platform_error(candidate: Path) -> Path:
    """Resolve a relative link target without relying on the link's own resolve().

    Windows can raise an ``OSError`` while resolving a valid relative symlink.
    Read each link target from its containing directory first so factual scan output
    stays deterministic across platforms.
    """

    current = candidate
    seen: set[str] = set()
    while True:
        marker = os.path.normcase(os.path.normpath(os.path.abspath(current)))
        if marker in seen:
            raise RuntimeError(f"symlink cycle: {candidate}")
        seen.add(marker)
        raw_target = os.readlink(current)
        target = Path(raw_target)
        current = target if target.is_absolute() else current.parent / target
        if current.is_symlink():
            continue
        if not current.exists():
            raise FileNotFoundError(current)
        return current.resolve(strict=True)


def _symlink_reference_finding(
    project_root: Path,
    candidate: Path,
    kind: str,
    *,
    memory_root: Path | None = None,
) -> SkippedReference:
    relative = candidate.relative_to(project_root).as_posix()
    try:
        resolved = candidate.resolve(strict=True)
    except RuntimeError:
        resolved = None
        resolution, target = "cycle", ""
    except FileNotFoundError:
        resolved = None
        resolution, target = "broken", ""
    except OSError as error:
        if error.errno == errno.ELOOP:
            resolved = None
            resolution, target = "cycle", ""
        else:
            try:
                resolved = _resolve_link_target_after_platform_error(candidate)
            except RuntimeError:
                resolved = None
                resolution, target = "cycle", ""
            except FileNotFoundError:
                resolved = None
                resolution, target = "broken", ""
            except OSError:
                resolved = None
                resolution, target = "unresolved", ""
    if resolved is not None:
        try:
            target = resolved.relative_to(project_root.resolve()).as_posix()
        except ValueError:
            resolution, target = "external", ""
        else:
            resolution = "internal"
    matched = f"{kind}:{resolution}" + (f":{target}" if target else "")
    classification = "reference-scan-symlink"
    reason = "not-followed"
    if memory_root is not None and candidate == memory_root and resolution == "internal":
        classification = "memory-root-alias"
        reason = "verified-logical-alias"
    else:
        parts = PurePosixPath(relative).parts
        offset = 1 if parts and parts[0] in {".agent-loop", "agent-loop"} else 0
        feature_parts = parts[offset:]
        if (
            len(feature_parts) == 2
            and feature_parts[0] == "features"
            and FEATURE_ID_RE.fullmatch(feature_parts[1])
        ) or (
            len(feature_parts) == 3
            and feature_parts[0] == "features"
            and MONTH_RE.fullmatch(feature_parts[1])
            and FEATURE_ID_RE.fullmatch(feature_parts[2])
        ):
            classification = "feature-entry-symlink"
            reason = "not-a-movable-directory-entry"
    return SkippedReference(relative, classification, matched, reason)


def _markdown_files(
    project_root: Path, memory_root: Path
) -> tuple[Sequence[Path], Sequence[SkippedReference]]:
    files: list[Path] = []
    findings: list[SkippedReference] = []
    boundary = project_root.resolve()
    memory_target = memory_root.resolve()

    def collect(scan_root: Path, *, logical_memory_walk: bool) -> None:
        for current, directories, names in os.walk(scan_root, followlinks=False):
            current_path = Path(current)
            kept: list[str] = []
            for name in sorted(directories):
                candidate = current_path / name
                if name in EXCLUDED_SCAN_DIRS:
                    continue
                if candidate.is_symlink():
                    findings.append(
                        _symlink_reference_finding(
                            project_root,
                            candidate,
                            "directory",
                            memory_root=memory_root,
                        )
                    )
                    continue
                if (
                    memory_root.is_symlink()
                    and not logical_memory_walk
                    and candidate.resolve() == memory_target
                ):
                    continue
                kept.append(name)
            directories[:] = kept
            for name in sorted(names):
                candidate = current_path / name
                if candidate.is_symlink():
                    findings.append(
                        _symlink_reference_finding(
                            project_root,
                            candidate,
                            "markdown-file" if name.lower().endswith(".md") else "entry",
                            memory_root=memory_root,
                        )
                    )
                    continue
                if not name.lower().endswith(".md"):
                    continue
                try:
                    candidate.resolve().relative_to(boundary)
                except ValueError as error:
                    raise ArchiveContractError(
                        "path-escape", candidate.relative_to(project_root).as_posix()
                    ) from error
                files.append(candidate)

    collect(project_root, logical_memory_walk=False)
    if memory_root.is_symlink():
        collect(memory_root, logical_memory_walk=True)
    return tuple(sorted(files)), tuple(
        sorted(
            findings,
            key=lambda item: (
                item.path,
                item.classification,
                item.matched_value,
                item.reason,
            ),
        )
    )


def _preserved_reference_class(relative: str) -> str | None:
    parts = PurePosixPath(relative).parts
    if "requirements" in parts:
        requirement_at = parts.index("requirements")
        tail = parts[requirement_at + 1 :]
        if tail and not (
            len(tail) == 1 and tail[0] == "INDEX.md"
        ) and PurePosixPath(relative).name != "README.md":
            return "immutable-requirement-source"
    if len(parts) >= 2 and parts[0] == "docs" and parts[1] in {
        "proposal",
        "reports",
    }:
        return "historical-evidence"
    return None


LINK_TARGET_RE = re.compile(
    r"!?\[[^\]]*\]\(\s*(?P<inline><[^>]+>|[^\s)]+)|"
    r"^\s*\[[^\]]+\]:\s*(?P<definition><[^>]+>|\S+)",
    re.MULTILINE,
)


def _relative_link_replacements(
    project_root: Path, file: Path, move: Move, content: str
) -> tuple[list[tuple[str, str]], list[SkippedReference]]:
    source_root = project_root / PurePosixPath(move.source)
    target_root = project_root / PurePosixPath(move.target)
    try:
        within = file.relative_to(source_root)
        file_moves = True
    except ValueError:
        within = None
        file_moves = False
    target_file = target_root / within if within is not None else file
    replacements: list[tuple[str, str]] = []
    skipped: list[SkippedReference] = []
    for match in LINK_TARGET_RE.finditer(content):
        raw = match.group("inline") or match.group("definition") or ""
        wrapped = raw.startswith("<") and raw.endswith(">")
        target = raw[1:-1] if wrapped else raw
        parsed = urlsplit(target)
        if parsed.scheme in {"http", "https", "mailto"} or parsed.netloc:
            continue
        if not parsed.path or (not parsed.path and parsed.fragment):
            continue
        decoded = unquote(parsed.path)
        resolved = (file.parent / decoded).resolve()
        try:
            resolved.relative_to(project_root.resolve())
        except ValueError:
            skipped.append(
                SkippedReference(
                    file.relative_to(project_root).as_posix(),
                    "unsupported",
                    target,
                    "relative Markdown link escapes project root",
                )
            )
            continue
        try:
            target_within_source = resolved.relative_to(source_root.resolve())
            target_is_in_source = True
        except ValueError:
            target_within_source = None
            target_is_in_source = False
        if not resolved.exists() and (file_moves or target_is_in_source):
            skipped.append(
                SkippedReference(
                    file.relative_to(project_root).as_posix(),
                    "unsupported",
                    target,
                    "broken cross-boundary Markdown link target does not exist",
                )
            )
            continue
        if not resolved.exists():
            continue
        if file_moves and target_is_in_source:
            continue
        if not file_moves and not target_is_in_source:
            continue
        destination = (
            target_root / target_within_source
            if target_is_in_source and target_within_source is not None
            else resolved
        )
        relative_target = os.path.relpath(destination, target_file.parent).replace(
            os.sep, "/"
        )
        rebuilt = urlunsplit(
            ("", "", relative_target, parsed.query, parsed.fragment)
        )
        if wrapped:
            rebuilt = f"<{rebuilt}>"
        if rebuilt != raw:
            replacements.append((raw, rebuilt))
    return replacements, skipped


def _discover_reference_impact(
    project_root: Path, moves: Sequence[Move], memory_root: Path
) -> tuple[Sequence[ReferenceEdit], Sequence[SkippedReference]]:
    planned: dict[str, list[tuple[str, str, str]]] = {}
    markdown_files, symlink_findings = _markdown_files(project_root, memory_root)
    skipped: list[SkippedReference] = list(symlink_findings)
    for path in markdown_files:
        relative = path.relative_to(project_root).as_posix()
        if relative in {
            ".agent-loop/features/archive.md",
            "agent-loop/features/archive.md",
        }:
            continue
        if path.stat().st_size > MAX_MARKDOWN_BYTES:
            skipped.append(
                SkippedReference(
                    relative,
                    "unsupported",
                    "file-size",
                    "Markdown file exceeds 2 MiB reference-scan limit",
                )
            )
            continue
        try:
            content, _ = _read_utf8_preserving(path)
        except UnicodeDecodeError:
            skipped.append(
                SkippedReference(
                    relative,
                    "unsupported",
                    "utf-8",
                    "Markdown file is not valid UTF-8",
                )
            )
            continue
        preserved = _preserved_reference_class(relative)
        for move in moves:
            old_prefix = move.source.rstrip("/") + "/"
            new_prefix = move.target.rstrip("/") + "/"
            if move.source not in content:
                link_replacements, link_skipped = _relative_link_replacements(
                    project_root, path, move, content
                )
                skipped.extend(link_skipped)
                for old, new in link_replacements:
                    planned.setdefault(relative, []).append(
                        ("relative-link", old, new)
                    )
                continue
            if preserved:
                skipped.append(
                    SkippedReference(
                        relative,
                        preserved,
                        move.source,
                        "preserved source or historical evidence retains the original path",
                    )
                )
                continue
            if old_prefix in content:
                planned.setdefault(relative, []).append(
                    ("literal-path", old_prefix, new_prefix)
                )
            remaining = content.replace(old_prefix, "")
            if move.source in remaining:
                skipped.append(
                    SkippedReference(
                        relative,
                        "unsupported",
                        move.source,
                        "old feature path appears in an unsupported or ambiguous form",
                    )
                )
            link_replacements, link_skipped = _relative_link_replacements(
                project_root, path, move, content
            )
            skipped.extend(link_skipped)
            for old, new in link_replacements:
                planned.setdefault(relative, []).append(("relative-link", old, new))

    edits: list[ReferenceEdit] = []
    for relative, replacements in sorted(planned.items()):
        path = project_root / PurePosixPath(relative)
        current, has_bom = _read_utf8_preserving(path)
        for kind, old, new in sorted(set(replacements)):
            occurrences = current.count(old)
            if not occurrences:
                continue
            before = _encode_utf8_preserving(current, has_bom)
            current = current.replace(old, new)
            after = _encode_utf8_preserving(current, has_bom)
            edits.append(
                ReferenceEdit(
                    path=relative,
                    kind=kind,
                    old=old,
                    new=new,
                    occurrences=occurrences,
                    before_sha256=sha256_bytes(before),
                    after_sha256=sha256_bytes(after),
                )
            )
    unique_skipped = {
        (item.path, item.classification, item.matched_value, item.reason): item
        for item in skipped
    }
    return (
        tuple(sorted(edits, key=lambda item: (item.path, item.kind, item.old, item.new))),
        tuple(unique_skipped[key] for key in sorted(unique_skipped)),
    )


def discover_reference_impacts(
    project_root: Path, moves: Sequence[Move]
) -> Sequence[ReferenceEdit]:
    edits, _ = _discover_reference_impact(
        project_root, moves, discover_memory_root(project_root)
    )
    return edits


def _project_relative_prefix(project_root: Path, memory_root: Path) -> str:
    try:
        return memory_root.relative_to(project_root.resolve()).as_posix()
    except ValueError as error:
        raise ArchiveContractError(
            "path-escape", "memory root is outside project root"
        ) from error


def _candidate_closed_at(memory_root: Path, candidate: ArchiveCandidate) -> str:
    notes = _read_optional(
        memory_root / PurePosixPath(candidate.current_path) / "notes.md"
    )
    return _readiness_values(notes).get("Closed At", "")


def _snapshot_plan_inputs(
    project_root: Path,
    memory_root: Path,
    candidates: Sequence[ArchiveCandidate],
    reference_edits: Sequence[ReferenceEdit],
    skipped_references: Sequence[SkippedReference],
) -> Mapping[str, str]:
    paths: set[Path] = set()
    for candidate in candidates:
        root = memory_root / PurePosixPath(candidate.current_path)
        if root.is_symlink():
            continue
        if root.is_dir():
            for path in root.rglob("*"):
                if path.is_symlink():
                    raise ArchiveContractError(
                        "path-escape",
                        path.relative_to(project_root).as_posix(),
                    )
                if path.is_file():
                    paths.add(path)
    for relative in ("project.md", "features/archive.md"):
        path = memory_root / PurePosixPath(relative)
        if path.is_file():
            paths.add(path)
    for item in reference_edits:
        paths.add(project_root / PurePosixPath(item.path))
    for item in skipped_references:
        path = project_root / PurePosixPath(item.path)
        if (
            not path.is_symlink()
            and path.is_file()
            and path.stat().st_size <= MAX_MARKDOWN_BYTES
        ):
            paths.add(path)
    return MappingProxyType(
        {
            path.relative_to(project_root).as_posix(): sha256_bytes(path.read_bytes())
            for path in sorted(paths)
        }
    )


def build_archive_plan(
    project_root: Path,
    *,
    operation: Literal["archive", "rehydrate"],
    selected_months: Sequence[str],
    selected_feature_ids: Sequence[str],
    as_of: date,
) -> ArchivePlan:
    project_root = project_root.resolve()
    memory_root = discover_memory_root(project_root)
    _assert_no_stranded_transactions(memory_root)
    months = tuple(sorted(set(selected_months)))
    feature_ids = tuple(sorted(set(selected_feature_ids)))
    if operation not in {"archive", "rehydrate"}:
        raise ArchiveContractError("usage", f"unsupported operation: {operation}", 2)
    if any(not MONTH_RE.fullmatch(month) for month in months):
        raise ArchiveContractError("usage", "month must be YYYY-MM", 2)
    if operation == "archive" and (not months or feature_ids):
        raise ArchiveContractError(
            "usage", "archive requires --month and forbids --feature-id", 2
        )
    if operation == "rehydrate" and (not feature_ids or months):
        raise ArchiveContractError(
            "usage", "rehydrate requires --feature-id and forbids --month", 2
        )

    existing_entries = tuple(parse_archive_index(memory_root))
    candidates: list[ArchiveCandidate] = []
    moves: list[Move] = []
    memory_prefix = _project_relative_prefix(project_root, memory_root)

    if operation == "archive":
        for location in discover_flat_features(memory_root):
            month = _feature_month(location.feature_id)
            if month not in months:
                continue
            resolve_feature_location(memory_root, location.feature_id)
            candidate = inspect_feature(memory_root, location.feature_id, as_of)
            candidates.append(candidate)
            if not candidate.blockers:
                moves.append(
                    Move(
                        candidate.feature_id,
                        candidate.month,
                        f"{memory_prefix}/features/{candidate.feature_id}",
                        f"{memory_prefix}/features/{candidate.month}/{candidate.feature_id}",
                    )
                )
        known = {candidate.feature_id for candidate in candidates}
        for entry in existing_entries:
            if (
                entry.month in months
                and entry.archive_state == "archived"
                and entry.feature_id not in known
            ):
                candidate = inspect_feature(memory_root, entry.feature_id, as_of)
                candidates.append(
                    replace(
                        candidate,
                        blockers=tuple(candidate.blockers) + ("already-archived",),
                    )
                )
    else:
        for feature_id in feature_ids:
            location = resolve_feature_location(memory_root, feature_id)
            candidate = inspect_feature(memory_root, feature_id, as_of)
            if location.layout != "archived":
                candidate = replace(
                    candidate,
                    blockers=tuple(candidate.blockers) + ("already-rehydrated",),
                )
            candidates.append(candidate)
            if not candidate.blockers and location.layout == "archived":
                moves.append(
                    Move(
                        feature_id,
                        _feature_month(feature_id),
                        f"{memory_prefix}/{location.relative_path}",
                        f"{memory_prefix}/features/{feature_id}",
                    )
                )

    entries_by_id = {entry.feature_id: entry for entry in existing_entries}
    candidates_by_id = {candidate.feature_id: candidate for candidate in candidates}
    for move in moves:
        candidate = candidates_by_id[move.feature_id]
        entries_by_id[move.feature_id] = ArchiveEntry(
            feature_id=move.feature_id,
            month=move.month,
            current_path=move.target.rstrip("/") + "/",
            archive_state="archived" if operation == "archive" else "rehydrated",
            closed_at=_candidate_closed_at(memory_root, candidate),
            delivered_summary=candidate.delivered_summary,
            source_requirements=candidate.source_requirements,
            applicable_decisions=candidate.applicable_decisions,
            last_moved_at=as_of.isoformat(),
        )

    reference_edits, skipped_references = _discover_reference_impact(
        project_root, moves, memory_root
    )
    snapshots = _snapshot_plan_inputs(
        project_root,
        memory_root,
        candidates,
        reference_edits,
        skipped_references,
    )
    return ArchivePlan(
        schema_version=1,
        operation=operation,
        as_of=as_of.isoformat(),
        selected_months=months,
        selected_feature_ids=feature_ids,
        candidates=tuple(candidates),
        moves=tuple(moves),
        archive_entries=tuple(entries_by_id.values()),
        reference_edits=reference_edits,
        skipped_references=skipped_references,
        snapshots=snapshots,
    )


def archive_plan_from_payload(payload: Mapping[str, object]) -> ArchivePlan:
    expected_keys = {
        "schema_version",
        "operation",
        "as_of",
        "selected_months",
        "selected_feature_ids",
        "candidates",
        "moves",
        "archive_entries",
        "reference_edits",
        "skipped_references",
        "snapshots",
        "plan_sha256",
    }
    if set(payload) != expected_keys:
        raise ArchiveContractError("usage", "archive plan fields do not match schema", 2)
    try:
        plan = ArchivePlan(
            schema_version=int(payload["schema_version"]),
            operation=str(payload["operation"]),
            as_of=str(payload["as_of"]),
            selected_months=tuple(payload["selected_months"]),
            selected_feature_ids=tuple(payload["selected_feature_ids"]),
            candidates=tuple(
                ArchiveCandidate(**item) for item in payload["candidates"]
            ),
            moves=tuple(Move(**item) for item in payload["moves"]),
            archive_entries=tuple(
                ArchiveEntry(**item) for item in payload["archive_entries"]
            ),
            reference_edits=tuple(
                ReferenceEdit(**item) for item in payload["reference_edits"]
            ),
            skipped_references=tuple(
                SkippedReference(**item) for item in payload["skipped_references"]
            ),
            snapshots=dict(payload["snapshots"]),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ArchiveContractError("usage", f"invalid archive plan: {error}", 2) from error
    if plan.schema_version != 1:
        raise ArchiveContractError("usage", "unsupported archive plan schema", 2)
    plan.assert_hash(str(payload["plan_sha256"]))
    return plan


def _hash_at(path: Path) -> str:
    if not path.is_file():
        raise ArchiveContractError("post-check", f"missing file: {path}")
    return sha256_bytes(path.read_bytes())


def _assert_pre_transaction_move_paths(
    project_root: Path, memory_root: Path, moves: Sequence[Move]
) -> None:
    memory_prefix = PurePosixPath(
        _project_relative_prefix(project_root, memory_root)
    ).parts
    required_prefix = memory_prefix + ("features",)
    for move in moves:
        source_relative = PurePosixPath(move.source)
        target_relative = PurePosixPath(move.target)
        for label, relative in (("source", source_relative), ("target", target_relative)):
            if relative.parts[: len(required_prefix)] != required_prefix:
                raise ArchiveContractError(
                    "stale-plan",
                    f"move {label} is outside logical Feature storage: {relative.as_posix()}",
                )
            cursor = memory_root / "features"
            if cursor.is_symlink():
                raise ArchiveContractError(
                    "stale-plan", "features container became a symlink"
                )
            for part in relative.parts[len(required_prefix) :]:
                cursor = cursor / part
                if cursor.is_symlink():
                    raise ArchiveContractError(
                        "stale-plan",
                        f"move {label} became a symlink: {relative.as_posix()}",
                    )
                if not cursor.exists():
                    break

        source = _confined_path(project_root, move.source)
        target = _confined_path(project_root, move.target)
        if source.is_symlink() or not source.is_dir():
            raise ArchiveContractError(
                "stale-plan", f"move source is not a real directory: {move.source}"
            )
        if target.exists() or target.is_symlink():
            raise ArchiveContractError(
                "stale-plan", f"move target is no longer absent: {move.target}"
            )


def validate_archive_plan_state(
    project_root: Path, plan: ArchivePlan, operation: str
) -> str:
    project_root = project_root.resolve()
    if operation not in {plan.operation, "restore"}:
        raise ArchiveContractError(
            "usage", f"plan operation is {plan.operation}, requested {operation}", 2
        )
    sources = [_confined_path(project_root, move.source) for move in plan.moves]
    targets = [_confined_path(project_root, move.target) for move in plan.moves]
    pre = not plan.moves or (
        all(path.is_dir() for path in sources)
        and all(not path.exists() for path in targets)
    )
    post = bool(plan.moves) and all(not path.exists() for path in sources) and all(
        path.is_dir() for path in targets
    )
    if not pre and not post:
        raise ArchiveContractError(
            "post-check", "source/target paths are in a mixed or unexpected state"
        )

    if pre:
        memory_root = discover_memory_root(project_root)
        _assert_pre_transaction_move_paths(project_root, memory_root, plan.moves)
        try:
            rebuilt = build_archive_plan(
                project_root,
                operation=plan.operation,
                selected_months=plan.selected_months,
                selected_feature_ids=plan.selected_feature_ids,
                as_of=date.fromisoformat(plan.as_of),
            )
        except ValueError as error:
            raise ArchiveContractError("usage", "plan as_of must be YYYY-MM-DD", 2) from error
        if rebuilt.computed_sha256() != plan.computed_sha256():
            raise ArchiveContractError(
                "stale-plan",
                f"stored {plan.computed_sha256()}, rebuilt {rebuilt.computed_sha256()}",
            )
        return "restore-check" if operation == "restore" else "pre-check"

    if operation == "restore":
        raise ArchiveContractError(
            "restore", "project does not match the plan's pre-transaction state"
        )

    final_hashes = {
        item.path: item.after_sha256 for item in plan.reference_edits
    }
    memory_root = discover_memory_root(project_root)
    memory_prefix = _project_relative_prefix(project_root, memory_root)
    index_relative = f"{memory_prefix}/features/archive.md"
    rendered_index_hash = sha256_bytes(
        render_archive_index(plan.archive_entries).encode("utf-8")
    )
    for relative, expected in plan.snapshots.items():
        mapped = relative
        for move in plan.moves:
            source = move.source.rstrip("/")
            if relative == source or relative.startswith(source + "/"):
                mapped = move.target.rstrip("/") + relative[len(source) :]
                break
        actual_path = _confined_path(project_root, mapped)
        actual = _hash_at(actual_path)
        required = (
            rendered_index_hash
            if mapped == index_relative
            else final_hashes.get(relative, final_hashes.get(mapped, expected))
        )
        if actual != required:
            raise ArchiveContractError(
                "post-check", f"content hash mismatch: {mapped}"
            )
    actual_entries = tuple(parse_archive_index(memory_root))
    if actual_entries != tuple(
        sorted(plan.archive_entries, key=lambda item: (item.month, item.feature_id))
    ):
        raise ArchiveContractError("post-check", "archive index does not match plan")
    return "post-check"


def _transaction_root(project_root: Path, transaction_id: str) -> Path:
    if not TRANSACTION_ID_RE.fullmatch(transaction_id):
        raise ArchiveContractError(
            "usage", "transaction ID must match YYYYMMDDTHHMMSSZ-12hex", 2
        )
    memory_root = discover_memory_root(project_root.resolve())
    root = memory_root / "features" / ".archive-txn" / transaction_id
    boundary = (memory_root / "features" / ".archive-txn").resolve()
    try:
        root.resolve().relative_to(boundary)
    except ValueError as error:
        raise ArchiveContractError("path-escape", transaction_id) from error
    return root


def _assert_no_stranded_transactions(memory_root: Path) -> None:
    transaction_root = memory_root / "features" / ".archive-txn"
    if not transaction_root.exists():
        return
    if transaction_root.is_symlink() or not transaction_root.is_dir():
        raise ArchiveContractError(
            "transaction", "stranded-transaction: unsafe .archive-txn path"
        )
    stranded = sorted(path.name for path in transaction_root.iterdir())
    if stranded:
        raise ArchiveContractError(
            "transaction",
            "stranded-transaction: restore required for " + ", ".join(stranded),
        )


def _write_journal(transaction_root: Path, journal: Mapping[str, object]) -> None:
    atomic_write_bytes(
        transaction_root / "journal.json",
        json.dumps(
            journal, ensure_ascii=False, sort_keys=True, indent=2
        ).encode("utf-8")
        + b"\n",
    )


def _load_journal(transaction_root: Path) -> dict[str, object]:
    path = transaction_root / "journal.json"
    if not path.is_file():
        raise ArchiveContractError("restore", f"missing journal: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ArchiveContractError("restore", f"invalid journal: {error}") from error
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ArchiveContractError("restore", "unsupported journal schema")
    if value.get("state") not in JOURNAL_STATES:
        raise ArchiveContractError("restore", "invalid journal state")
    return value


def _journal_index_relative(project_root: Path) -> str:
    memory_root = discover_memory_root(project_root)
    return f"{_project_relative_prefix(project_root, memory_root)}/features/archive.md"


def _validate_journal_scope(
    project_root: Path, journal: Mapping[str, object]
) -> tuple[ArchivePlan, tuple[Move, ...], tuple[Mapping[str, object], ...]]:
    expected_keys = {
        "schema_version",
        "transaction_id",
        "operation",
        "plan_sha256",
        "plan",
        "state",
        "moves",
        "backups",
        "completed_operations",
        "snapshots",
        "created_directories",
    }
    if set(journal) != expected_keys:
        raise ArchiveContractError("restore", "journal fields do not match schema")
    plan_payload = journal.get("plan")
    if not isinstance(plan_payload, dict):
        raise ArchiveContractError("restore", "journal plan is missing or invalid")
    try:
        plan = archive_plan_from_payload(plan_payload)
    except ArchiveContractError as error:
        raise ArchiveContractError(
            "restore", f"journal plan is invalid: {error}"
        ) from error
    if not plan.moves:
        raise ArchiveContractError("restore", "journal plan has no moves")
    if journal.get("plan_sha256") != plan.computed_sha256():
        raise ArchiveContractError("restore", "journal plan SHA-256 mismatch")
    if journal.get("operation") != plan.operation:
        raise ArchiveContractError("restore", "journal operation does not match plan")

    expected_moves = [asdict(move) for move in plan.moves]
    if journal.get("moves") != expected_moves:
        raise ArchiveContractError("restore", "journal move scope does not match plan")
    if journal.get("snapshots") != dict(plan.snapshots):
        raise ArchiveContractError("restore", "journal snapshots do not match plan")

    reference_hashes: dict[str, str] = {}
    for edit in sorted(
        plan.reference_edits,
        key=lambda item: (item.path, item.kind, item.old, item.new),
    ):
        expected_before = reference_hashes.get(
            edit.path, plan.snapshots.get(edit.path, "")
        )
        if (
            not expected_before
            or edit.before_sha256 != expected_before
            or not HASH_RE.fullmatch(edit.after_sha256)
            or edit.occurrences < 1
            or not edit.old
            or edit.old == edit.new
        ):
            raise ArchiveContractError(
                "restore",
                f"journal reference-edit chain does not match snapshots: {edit.path}",
            )
        reference_hashes[edit.path] = edit.after_sha256

    index_relative = _journal_index_relative(project_root)
    expected_backup_paths = {index_relative} | {
        edit.path for edit in plan.reference_edits
    }
    raw_backups = journal.get("backups")
    if not isinstance(raw_backups, list) or not all(
        isinstance(item, dict) for item in raw_backups
    ):
        raise ArchiveContractError("restore", "journal backups are invalid")
    backups = tuple(raw_backups)
    actual_paths = [str(item.get("path", "")) for item in backups]
    if (
        len(actual_paths) != len(set(actual_paths))
        or set(actual_paths) != expected_backup_paths
    ):
        raise ArchiveContractError("restore", "journal backup scope does not match plan")
    for item in backups:
        relative = str(item.get("path", ""))
        expected_state = "existing" if relative in plan.snapshots else "missing-before"
        if item.get("state") != expected_state:
            raise ArchiveContractError(
                "restore", f"journal backup state does not match plan: {relative}"
            )
        if expected_state == "existing":
            expected_item_keys = {"path", "state", "backup", "sha256"}
            if set(item) != expected_item_keys:
                raise ArchiveContractError(
                    "restore", f"journal backup fields are invalid: {relative}"
                )
            if item.get("backup") != f"backups/{relative}":
                raise ArchiveContractError(
                    "restore", f"journal backup path does not match plan: {relative}"
                )
            if item.get("sha256") != plan.snapshots[relative]:
                raise ArchiveContractError(
                    "restore", f"journal backup hash does not match plan: {relative}"
                )
        elif set(item) != {"path", "state"}:
            raise ArchiveContractError(
                "restore", f"journal missing-before fields are invalid: {relative}"
            )

    allowed_operations: set[tuple[tuple[str, str], ...]] = set()
    for move in plan.moves:
        allowed_operations.add(
            tuple(
                sorted(
                    {
                        "kind": "move",
                        "source": move.source,
                        "target": move.target,
                    }.items()
                )
            )
        )
    allowed_operations.add(
        tuple(sorted({"kind": "archive-index", "path": index_relative}.items()))
    )
    for edit in plan.reference_edits:
        allowed_operations.add(
            tuple(
                sorted(
                    {
                        "kind": "reference-edit",
                        "path": edit.path,
                        "mapped_path": _mapped_after_moves(edit.path, plan.moves),
                    }.items()
                )
            )
        )
    completed = journal.get("completed_operations")
    if not isinstance(completed, list) or not all(
        isinstance(item, dict) for item in completed
    ):
        raise ArchiveContractError("restore", "journal completed operations are invalid")
    if any(tuple(sorted(item.items())) not in allowed_operations for item in completed):
        raise ArchiveContractError(
            "restore", "journal completed operation exceeds plan scope"
        )

    allowed_directories = {
        PurePosixPath(move.target).parent.as_posix() for move in plan.moves
    }
    created = journal.get("created_directories")
    if not isinstance(created, list) or len(created) != len(set(created)) or any(
        not isinstance(item, str) or item not in allowed_directories for item in created
    ):
        raise ArchiveContractError(
            "restore", "journal created-directory scope does not match plan"
        )
    return plan, tuple(plan.moves), backups


def _restore_allowed_hashes(
    project_root: Path, plan: ArchivePlan, relative: str
) -> frozenset[str]:
    hashes = {plan.snapshots[relative]} if relative in plan.snapshots else set()
    for edit in plan.reference_edits:
        if edit.path == relative:
            hashes.add(edit.before_sha256)
            hashes.add(edit.after_sha256)
    if relative == _journal_index_relative(project_root):
        hashes.add(
            sha256_bytes(render_archive_index(plan.archive_entries).encode("utf-8"))
        )
    return frozenset(hashes)


def _restore_move_states(
    project_root: Path, moves: Sequence[Move]
) -> Mapping[str, str]:
    states: dict[str, str] = {}
    for move in moves:
        source = _confined_path(project_root, move.source)
        target = _confined_path(project_root, move.target)
        source_ready = source.is_dir() and not target.exists()
        target_ready = target.is_dir() and not source.exists()
        if source_ready:
            states[move.source] = "source"
        elif target_ready:
            states[move.source] = "target"
        else:
            raise ArchiveContractError(
                "restore",
                f"source/target drift blocks restore: {move.source} -> {move.target}",
            )
    return MappingProxyType(states)


def _restore_current_relative(
    relative: str, moves: Sequence[Move], states: Mapping[str, str]
) -> str:
    for move in moves:
        source = move.source.rstrip("/")
        if relative == source or relative.startswith(source + "/"):
            if states[move.source] == "target":
                return move.target.rstrip("/") + relative[len(source) :]
            return relative
    return relative


def _validate_restore_current_state(
    project_root: Path,
    transaction_root: Path,
    plan: ArchivePlan,
    moves: Sequence[Move],
    backups: Sequence[Mapping[str, object]],
    states: Mapping[str, str],
) -> None:
    for item in backups:
        if item.get("state") != "existing":
            continue
        relative = str(item["path"])
        backup = _confined_path(transaction_root, str(item["backup"]))
        if (
            not backup.is_file()
            or sha256_bytes(backup.read_bytes()) != item.get("sha256")
        ):
            raise ArchiveContractError(
                "restore", f"backup preflight failed for {relative}"
            )
    for relative in plan.snapshots:
        current_relative = _restore_current_relative(relative, moves, states)
        path = _confined_path(project_root, current_relative)
        if not path.is_file():
            raise ArchiveContractError(
                "restore", f"drift: missing transaction file {current_relative}"
            )
        if sha256_bytes(path.read_bytes()) not in _restore_allowed_hashes(
            project_root, plan, relative
        ):
            raise ArchiveContractError(
                "restore", f"drift: unexpected transaction bytes at {current_relative}"
            )
    for item in backups:
        if item.get("state") != "missing-before":
            continue
        relative = str(item["path"])
        path = _confined_path(project_root, relative)
        if not path.exists():
            continue
        if (
            not path.is_file()
            or sha256_bytes(path.read_bytes())
            not in _restore_allowed_hashes(project_root, plan, relative)
        ):
            raise ArchiveContractError(
                "restore", f"drift: unexpected file at {relative}"
            )


def _mapped_after_moves(relative: str, moves: Sequence[Move]) -> str:
    for move in moves:
        source = move.source.rstrip("/")
        if relative == source or relative.startswith(source + "/"):
            return move.target.rstrip("/") + relative[len(source) :]
    return relative


def _remove_transaction_tree(transaction_root: Path) -> None:
    parent = transaction_root.parent
    shutil.rmtree(transaction_root)
    try:
        parent.rmdir()
    except OSError:
        pass


def _failure_limit() -> int | None:
    raw = os.environ.get("AGENT_LOOP_ARCHIVE_FAIL_AFTER")
    if raw is None:
        return None
    if os.environ.get("AGENT_LOOP_ARCHIVE_TEST_MODE") != "1":
        raise ArchiveContractError(
            "transaction",
            "AGENT_LOOP_ARCHIVE_FAIL_AFTER is test-only and requires AGENT_LOOP_ARCHIVE_TEST_MODE=1",
        )
    try:
        value = int(raw)
    except ValueError as error:
        raise ArchiveContractError(
            "transaction", "AGENT_LOOP_ARCHIVE_FAIL_AFTER must be a positive integer"
        ) from error
    if value < 1:
        raise ArchiveContractError(
            "transaction", "AGENT_LOOP_ARCHIVE_FAIL_AFTER must be a positive integer"
        )
    return value


def _new_transaction_id(features_root: Path) -> str:
    for _ in range(100):
        value = (
            datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
            + secrets.token_hex(6)
        )
        if not (features_root / ".archive-txn" / value).exists():
            return value
    raise ArchiveContractError("transaction", "could not allocate transaction ID")


def apply_archive_plan(
    project_root: Path,
    plan: ArchivePlan,
    *,
    expected_plan_sha256: str,
) -> str:
    project_root = project_root.resolve()
    plan.assert_hash(expected_plan_sha256)
    memory_root = discover_memory_root(project_root)
    _assert_no_stranded_transactions(memory_root)
    validate_archive_plan_state(project_root, plan, plan.operation)
    failure_limit = _failure_limit()
    if not plan.moves:
        return "no-op"

    _assert_pre_transaction_move_paths(project_root, memory_root, plan.moves)

    features_root = memory_root / "features"
    transaction_id = _new_transaction_id(features_root)
    transaction_root = _transaction_root(project_root, transaction_id)
    transaction_root.mkdir(parents=True)
    memory_prefix = _project_relative_prefix(project_root, memory_root)
    index_relative = f"{memory_prefix}/features/archive.md"
    backup_paths = sorted(
        {item.path for item in plan.reference_edits} | {index_relative}
    )
    journal: dict[str, object] = {
        "schema_version": 1,
        "transaction_id": transaction_id,
        "operation": plan.operation,
        "plan_sha256": plan.computed_sha256(),
        "plan": plan.to_payload(),
        "state": "prepared",
        "moves": [asdict(move) for move in plan.moves],
        "backups": [],
        "completed_operations": [],
        "snapshots": dict(plan.snapshots),
        "created_directories": [],
    }
    _write_journal(transaction_root, journal)
    try:
        backups: list[dict[str, str]] = []
        for relative in backup_paths:
            source = _confined_path(project_root, relative)
            if source.is_file():
                backup_relative = f"backups/{relative}"
                atomic_write_bytes(
                    transaction_root / PurePosixPath(backup_relative), source.read_bytes()
                )
                backups.append(
                    {
                        "path": relative,
                        "state": "existing",
                        "backup": backup_relative,
                        "sha256": sha256_bytes(source.read_bytes()),
                    }
                )
            elif source.exists():
                raise ArchiveContractError(
                    "transaction", f"backup target is not a file: {relative}"
                )
            else:
                backups.append({"path": relative, "state": "missing-before"})
        journal["backups"] = backups
        _write_journal(transaction_root, journal)

        completed: list[dict[str, str]] = []
        created_directories: list[str] = []
        operation_count = 0

        def record_mutation(kind: str, **details: str) -> None:
            nonlocal operation_count
            operation_count += 1
            completed.append({"kind": kind, **details})
            journal["completed_operations"] = completed
            journal["created_directories"] = created_directories
            _write_journal(transaction_root, journal)
            if failure_limit is not None and operation_count >= failure_limit:
                raise RuntimeError(
                    f"injected archive failure after operation {operation_count}"
                )

        journal["state"] = "moving"
        _write_journal(transaction_root, journal)
        for move in plan.moves:
            source = _confined_path(project_root, move.source)
            target = _confined_path(project_root, move.target)
            if not source.is_dir() or target.exists():
                raise ArchiveContractError(
                    "transaction", f"move precondition failed: {move.source} -> {move.target}"
                )
            if not target.parent.exists():
                target.parent.mkdir(parents=True)
                created_directories.append(
                    target.parent.relative_to(project_root).as_posix()
                )
                journal["created_directories"] = created_directories
                _write_journal(transaction_root, journal)
            source.rename(target)
            record_mutation("move", source=move.source, target=move.target)

        index = memory_root / "features" / "archive.md"
        atomic_write_bytes(
            index, render_archive_index(plan.archive_entries).encode("utf-8")
        )
        record_mutation("archive-index", path=index_relative)

        for edit in plan.reference_edits:
            mapped = _mapped_after_moves(edit.path, plan.moves)
            target = _confined_path(project_root, mapped)
            current, has_bom = _read_utf8_preserving(target)
            current_bytes = _encode_utf8_preserving(current, has_bom)
            if sha256_bytes(current_bytes) != edit.before_sha256:
                raise ArchiveContractError(
                    "stale-plan", f"reference changed before apply: {edit.path}"
                )
            if current.count(edit.old) != edit.occurrences:
                raise ArchiveContractError(
                    "stale-plan", f"reference occurrence drift: {edit.path}"
                )
            updated = current.replace(edit.old, edit.new)
            updated_bytes = _encode_utf8_preserving(updated, has_bom)
            if sha256_bytes(updated_bytes) != edit.after_sha256:
                raise ArchiveContractError(
                    "transaction", f"reference edit hash mismatch: {edit.path}"
                )
            atomic_write_bytes(target, updated_bytes)
            record_mutation("reference-edit", path=edit.path, mapped_path=mapped)

        journal["state"] = "references-updated"
        _write_journal(transaction_root, journal)
        journal["state"] = "checking"
        _write_journal(transaction_root, journal)
        validate_archive_plan_state(project_root, plan, plan.operation)
        journal["state"] = "verified"
        _write_journal(transaction_root, journal)
        _remove_transaction_tree(transaction_root)
        return transaction_id
    except Exception as error:
        try:
            restore_transaction(project_root, transaction_id)
        except ArchiveContractError as restore_error:
            raise ArchiveContractError(
                "transaction",
                f"{error}; restore=failed: {restore_error.detail}",
            ) from error
        raise ArchiveContractError(
            "transaction", f"{error}; restore=complete"
        ) from error


def restore_transaction(project_root: Path, transaction_id: str) -> None:
    project_root = project_root.resolve()
    transaction_root = _transaction_root(project_root, transaction_id)
    journal = _load_journal(transaction_root)
    if journal.get("transaction_id") != transaction_id:
        raise ArchiveContractError("restore", "journal transaction ID mismatch")
    plan, moves, backups = _validate_journal_scope(project_root, journal)
    journal["state"] = "restoring"
    _write_journal(transaction_root, journal)
    states = _restore_move_states(project_root, moves)
    _validate_restore_current_state(
        project_root, transaction_root, plan, moves, backups, states
    )
    try:
        for move in reversed(moves):
            source = _confined_path(project_root, move.source)
            target = _confined_path(project_root, move.target)
            if source.exists() and target.exists():
                raise ArchiveContractError(
                    "restore", f"source collision blocks restore: {move.source}"
                )
            if source.is_dir() and not target.exists():
                continue
            if source.exists():
                raise ArchiveContractError(
                    "restore", f"restored source is not a directory: {move.source}"
                )
            if not target.is_dir():
                raise ArchiveContractError(
                    "restore", f"moved target is missing: {move.target}"
                )
            source.parent.mkdir(parents=True, exist_ok=True)
            target.rename(source)

        for item in backups:
            relative = str(item.get("path", ""))
            target = _confined_path(project_root, relative)
            state = item.get("state")
            if state == "existing":
                backup = _confined_path(
                    transaction_root, str(item.get("backup", ""))
                )
                if not backup.is_file():
                    raise ArchiveContractError(
                        "restore", f"missing backup for {relative}"
                    )
                content = backup.read_bytes()
                if sha256_bytes(content) != item.get("sha256"):
                    raise ArchiveContractError(
                        "restore", f"backup hash mismatch for {relative}"
                    )
                atomic_write_bytes(target, content)
            elif state == "missing-before":
                if target.is_dir():
                    raise ArchiveContractError(
                        "restore", f"cannot remove directory backup target: {relative}"
                    )
                target.unlink(missing_ok=True)
            else:
                raise ArchiveContractError(
                    "restore", f"invalid backup state for {relative}"
                )

        for relative, expected in dict(journal.get("snapshots", {})).items():
            actual = _hash_at(_confined_path(project_root, str(relative)))
            if actual != expected:
                raise ArchiveContractError(
                    "restore", f"restored content hash mismatch: {relative}"
                )
        for relative in reversed(list(journal.get("created_directories", []))):
            directory = _confined_path(project_root, str(relative))
            try:
                directory.rmdir()
            except OSError:
                pass
        journal["state"] = "restored"
        _write_journal(transaction_root, journal)
        _remove_transaction_tree(transaction_root)
    except ArchiveContractError:
        journal["state"] = "restoring"
        _write_journal(transaction_root, journal)
        raise
    except Exception as error:
        journal["state"] = "restoring"
        _write_journal(transaction_root, journal)
        raise ArchiveContractError("restore", str(error)) from error
