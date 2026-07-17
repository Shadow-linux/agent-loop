from __future__ import annotations

import base64
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import sys
import unicodedata
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Literal, Mapping, Sequence

from checker_support import atomic_write_bytes, canonical_json_bytes, sha256_bytes


SemanticRole = Literal[
    "human-source",
    "accepted-authority",
    "append-only-evidence",
    "current-semantic-state",
    "derived-index",
    "validated-package",
    "transaction-temporary",
    "unclassified",
]
Attention = Literal["🟢", "🟡", "🔴"]
Action = Literal["保留", "引入", "重写", "重算", "移除过时声明", "暂不处理"]
ReportStatus = Literal["待确认", "已完成", "已恢复"]
PathKind = Literal["missing", "directory", "file", "symlink", "gitlink"]
ContentSourceKind = Literal["none", "git-blob", "inline-base64"]

SNAPSHOT_KEYS = ("base", "source", "target_before", "result")
SEMANTIC_ROLES = {
    "human-source",
    "accepted-authority",
    "append-only-evidence",
    "current-semantic-state",
    "derived-index",
    "validated-package",
    "transaction-temporary",
    "unclassified",
}
ACTIONS = {"保留", "引入", "重写", "重算", "移除过时声明", "暂不处理"}
ATTENTION_LEVELS = {"🟢", "🟡", "🔴"}
REPORT_STATUSES = {"待确认", "已完成", "已恢复"}
PLAN_START = "<!-- memory-reconciliation-plan:start -->"
PLAN_END = "<!-- memory-reconciliation-plan:end -->"
LOWER_SHA256 = re.compile(r"^[0-9a-f]{64}$")
FULL_GIT_SHA = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")


@dataclass(frozen=True)
class MemoryReconciliationError(Exception):
    category: str
    detail: str = ""

    def __str__(self) -> str:
        return f"{self.category}: {self.detail}" if self.detail else self.category


@dataclass(frozen=True)
class MergeContext:
    merge_base_sha: str
    source_sha: str
    target_before_sha: str
    merged_code_sha: str
    source_branch: str
    target_branch: str
    target_release_context: str
    customer_boundary: str
    memory_root: str


@dataclass(frozen=True)
class SnapshotEntry:
    state: Literal["present", "absent"]
    kind: PathKind
    git_mode: str | None
    git_oid: str | None
    sha256: str | None


@dataclass(frozen=True)
class PathLedgerRow:
    path: str
    snapshots: Mapping[str, SnapshotEntry]
    semantic_role: SemanticRole
    stable_identity: str
    owner: str
    attention: Attention
    action: Action
    fact_sources: Sequence[str]
    desired_value: str
    operation_id: str | None


@dataclass(frozen=True)
class ContentSource:
    kind: ContentSourceKind
    git_sha: str | None
    git_path: str | None
    inline_base64: str | None


@dataclass(frozen=True)
class RewriteOperation:
    operation_id: str
    sequence: int
    path: str
    action: Literal["引入", "重写", "重算", "移除过时声明"]
    preimage_sha256: str | None
    postimage_sha256: str | None
    post_mode: Literal["100644", "100755", "absent"]
    content_source: ContentSource


@dataclass(frozen=True)
class ReconciliationPlan:
    schema_version: int
    report_id: str
    context: MergeContext
    scan_sha256: str
    ledger: Sequence[PathLedgerRow]
    operations: Sequence[RewriteOperation]
    expected_unchanged_paths: Mapping[str, str]
    human_decisions: Sequence[Mapping[str, str]]
    post_check_expectations: Sequence[str]
    plan_sha256: str


@dataclass(frozen=True)
class ValidationResult:
    context: MergeContext
    ledger: Sequence[PathLedgerRow]
    operations: Sequence[RewriteOperation]
    report_status: ReportStatus
    current_hashes: Mapping[str, str]
    blockers: Sequence[str]
    zero_change: bool


def absent_entry() -> SnapshotEntry:
    return SnapshotEntry(
        state="absent", kind="missing", git_mode=None, git_oid=None, sha256=None
    )


def validate_merge_context_text(values: Mapping[str, str]) -> None:
    for field in (
        "source_branch",
        "target_branch",
        "target_release_context",
        "customer_boundary",
    ):
        value = values.get(field)
        if not isinstance(value, str) or not value.strip():
            raise MemoryReconciliationError("merge context", f"{field} must be non-empty")


def _git_bytes(repo_root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *arguments],
        check=False,
        capture_output=True,
        text=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="strict").strip()
        raise MemoryReconciliationError("git command failed", detail)
    return result.stdout


def resolve_commit(repo_root: Path, value: str) -> str:
    try:
        resolved = _git_bytes(repo_root, "rev-parse", "--verify", f"{value}^{{commit}}")
    except (MemoryReconciliationError, UnicodeDecodeError) as error:
        raise MemoryReconciliationError("invalid commit", value) from error
    full = resolved.decode("ascii").strip()
    if not FULL_GIT_SHA.fullmatch(full):
        raise MemoryReconciliationError("invalid resolved commit", value)
    return full


def resolve_memory_root(project_root: Path) -> str:
    roots = [name for name in (".agent-loop", "agent-loop") if (project_root / name).is_dir()]
    if len(roots) != 1:
        reason = "both roots exist" if len(roots) > 1 else "no memory root exists"
        raise MemoryReconciliationError("memory root", reason)
    return roots[0]


def git_memory_roots(repo_root: Path, sha: str) -> tuple[str, ...]:
    roots: list[str] = []
    for name in (".agent-loop", "agent-loop"):
        result = subprocess.run(
            ["git", "-C", str(repo_root), "cat-file", "-e", f"{sha}:{name}"],
            check=False,
            capture_output=True,
            text=False,
        )
        if result.returncode == 0:
            roots.append(name)
    return tuple(roots)


def _path_collision_key(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def _validate_collision_free(paths: Sequence[str]) -> None:
    seen: dict[str, str] = {}
    for value in paths:
        key = _path_collision_key(value)
        previous = seen.get(key)
        if previous is not None and previous != value:
            raise MemoryReconciliationError(
                "path collision", f"{previous!r} conflicts with {value!r}"
            )
        seen[key] = value


def safe_relative_path(value: str, memory_root: Path) -> Path:
    if not value or "\x00" in value or "\\" in value:
        raise MemoryReconciliationError("unsafe path", value)
    if value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise MemoryReconciliationError("unsafe path", value)
    pure = PurePosixPath(value)
    if value != pure.as_posix() or any(part in ("", ".", "..") for part in pure.parts):
        raise MemoryReconciliationError("unsafe path", value)
    candidate = memory_root.joinpath(*pure.parts)
    current = memory_root
    for part in pure.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise MemoryReconciliationError("symlink parent", value)
    try:
        candidate.parent.resolve(strict=False).relative_to(memory_root.resolve())
    except ValueError as error:
        raise MemoryReconciliationError("path escapes memory root", value) from error
    return candidate


def inventory_worktree(
    memory_root: Path, *, excluded_prefixes: Sequence[str] = ()
) -> dict[str, SnapshotEntry]:
    if not memory_root.is_dir() or memory_root.is_symlink():
        raise MemoryReconciliationError("memory root", "worktree root is missing or unsafe")
    prefixes = tuple(prefix.strip("/") for prefix in excluded_prefixes if prefix.strip("/"))
    inventory: dict[str, SnapshotEntry] = {}
    for path in sorted(memory_root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(memory_root).as_posix()
        if any(relative == prefix or relative.startswith(f"{prefix}/") for prefix in prefixes):
            continue
        safe_relative_path(relative, memory_root)
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            target = os.readlink(path).encode("utf-8")
            entry = SnapshotEntry("present", "symlink", "120000", None, sha256_bytes(target))
        elif stat.S_ISDIR(mode):
            entry = SnapshotEntry("present", "directory", "040000", None, None)
        elif stat.S_ISREG(mode):
            executable = bool(mode & stat.S_IXUSR)
            entry = SnapshotEntry(
                "present",
                "file",
                "100755" if executable else "100644",
                None,
                sha256_bytes(path.read_bytes()),
            )
        else:
            raise MemoryReconciliationError("unsupported path kind", relative)
        inventory[relative] = entry
    _validate_collision_free(tuple(inventory))
    return inventory


def inventory_git_tree(
    repo_root: Path, sha: str, memory_root_name: str
) -> dict[str, SnapshotEntry]:
    if memory_root_name not in (".agent-loop", "agent-loop"):
        raise MemoryReconciliationError("memory root", memory_root_name)
    raw = _git_bytes(repo_root, "ls-tree", "-r", "-t", "-z", sha, "--", memory_root_name)
    inventory: dict[str, SnapshotEntry] = {}
    for record in raw.split(b"\x00"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode_bytes, type_bytes, oid_bytes = metadata.split(b" ", 2)
            full_path = raw_path.decode("utf-8", errors="strict")
            mode = mode_bytes.decode("ascii")
            object_type = type_bytes.decode("ascii")
            oid = oid_bytes.decode("ascii")
        except (ValueError, UnicodeDecodeError) as error:
            raise MemoryReconciliationError("invalid git tree record", repr(record)) from error
        if full_path == memory_root_name:
            continue
        prefix = f"{memory_root_name}/"
        if not full_path.startswith(prefix):
            raise MemoryReconciliationError("git path outside memory root", full_path)
        relative = full_path[len(prefix) :]
        safe_relative_path(relative, repo_root / memory_root_name)
        if object_type == "tree":
            kind: PathKind = "directory"
            digest = None
        elif mode == "120000" and object_type == "blob":
            kind = "symlink"
            digest = sha256_bytes(_git_bytes(repo_root, "cat-file", "blob", oid))
        elif mode == "160000" and object_type == "commit":
            kind = "gitlink"
            digest = None
        elif object_type == "blob" and mode in ("100644", "100755"):
            kind = "file"
            digest = sha256_bytes(_git_bytes(repo_root, "cat-file", "blob", oid))
        else:
            raise MemoryReconciliationError(
                "unsupported git path kind", f"{mode} {object_type} {relative}"
            )
        inventory[relative] = SnapshotEntry("present", kind, mode, oid, digest)
    _validate_collision_free(tuple(inventory))
    return inventory


def union_inventories(
    snapshots: Mapping[str, Mapping[str, SnapshotEntry]],
) -> list[dict[str, object]]:
    if set(snapshots) != set(SNAPSHOT_KEYS):
        raise MemoryReconciliationError("snapshot keys", ", ".join(sorted(snapshots)))
    paths = sorted({path for inventory in snapshots.values() for path in inventory})
    _validate_collision_free(paths)
    rows: list[dict[str, object]] = []
    for path in paths:
        row: dict[str, object] = {"path": path}
        for key in SNAPSHOT_KEYS:
            row[key] = snapshots[key].get(path, absent_entry())
        rows.append(row)
    return rows


def _plain_payload(value: object) -> object:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    return value


def canonical_plan_hash(plan: object) -> str:
    payload = _plain_payload(plan)
    if not isinstance(payload, dict):
        raise MemoryReconciliationError("invalid plan", "expected object")
    normalized = dict(payload)
    normalized.pop("plan_sha256", None)
    return sha256_bytes(canonical_json_bytes(normalized))


def extract_plan_payload(text: str) -> dict[str, object]:
    if text.count(PLAN_START) != 1 or text.count(PLAN_END) != 1:
        raise MemoryReconciliationError("plan block", "expected exactly one sentinel pair")
    start = text.index(PLAN_START) + len(PLAN_START)
    end = text.index(PLAN_END, start)
    body = text[start:end].strip()
    match = re.fullmatch(r"```json\s*\n(.*?)\n```", body, re.DOTALL)
    if not match:
        raise MemoryReconciliationError("plan block", "expected one fenced JSON object")
    try:
        payload = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise MemoryReconciliationError("plan JSON", str(error)) from error
    if not isinstance(payload, dict):
        raise MemoryReconciliationError("plan JSON", "expected object")
    return payload


def decode_inline_payload(value: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except (ValueError, TypeError) as error:
        raise MemoryReconciliationError("invalid inline base64", "payload") from error


def snapshot_entry_payload(entry: SnapshotEntry) -> dict[str, str | None]:
    return asdict(entry)


def _require_string(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str):
        raise MemoryReconciliationError("invalid plan field", key)
    return value


def _optional_string(payload: Mapping[str, object], key: str) -> str | None:
    value = payload.get(key)
    if value is not None and not isinstance(value, str):
        raise MemoryReconciliationError("invalid plan field", key)
    return value


def _snapshot_from(payload: object) -> SnapshotEntry:
    if not isinstance(payload, dict):
        raise MemoryReconciliationError("invalid snapshot", "expected object")
    state = _require_string(payload, "state")
    kind = _require_string(payload, "kind")
    if state not in ("present", "absent") or kind not in (
        "missing",
        "directory",
        "file",
        "symlink",
        "gitlink",
    ):
        raise MemoryReconciliationError("invalid snapshot", f"{state}/{kind}")
    return SnapshotEntry(
        state=state,  # type: ignore[arg-type]
        kind=kind,  # type: ignore[arg-type]
        git_mode=_optional_string(payload, "git_mode"),
        git_oid=_optional_string(payload, "git_oid"),
        sha256=_optional_string(payload, "sha256"),
    )


def _context_from(payload: object) -> MergeContext:
    if not isinstance(payload, dict):
        raise MemoryReconciliationError("invalid context", "expected object")
    return MergeContext(
        merge_base_sha=_require_string(payload, "merge_base_sha"),
        source_sha=_require_string(payload, "source_sha"),
        target_before_sha=_require_string(payload, "target_before_sha"),
        merged_code_sha=_require_string(payload, "merged_code_sha"),
        source_branch=_require_string(payload, "source_branch"),
        target_branch=_require_string(payload, "target_branch"),
        target_release_context=_require_string(payload, "target_release_context"),
        customer_boundary=_require_string(payload, "customer_boundary"),
        memory_root=_require_string(payload, "memory_root"),
    )


def _ledger_row_from(payload: object) -> PathLedgerRow:
    if not isinstance(payload, dict):
        raise MemoryReconciliationError("invalid ledger row", "expected object")
    raw_snapshots = payload.get("snapshots")
    if not isinstance(raw_snapshots, dict) or set(raw_snapshots) != set(SNAPSHOT_KEYS):
        raise MemoryReconciliationError("invalid ledger snapshots", _require_string(payload, "path"))
    role = _require_string(payload, "semantic_role")
    attention = _require_string(payload, "attention")
    action = _require_string(payload, "action")
    raw_sources = payload.get("fact_sources")
    if not isinstance(raw_sources, list) or not all(isinstance(item, str) for item in raw_sources):
        raise MemoryReconciliationError("invalid fact sources", _require_string(payload, "path"))
    operation_id = payload.get("operation_id")
    if operation_id is not None and not isinstance(operation_id, str):
        raise MemoryReconciliationError("invalid operation id", _require_string(payload, "path"))
    return PathLedgerRow(
        path=_require_string(payload, "path"),
        snapshots={key: _snapshot_from(raw_snapshots[key]) for key in SNAPSHOT_KEYS},
        semantic_role=role,  # type: ignore[arg-type]
        stable_identity=_require_string(payload, "stable_identity"),
        owner=_require_string(payload, "owner"),
        attention=attention,  # type: ignore[arg-type]
        action=action,  # type: ignore[arg-type]
        fact_sources=tuple(raw_sources),
        desired_value=_require_string(payload, "desired_value"),
        operation_id=operation_id,
    )


def _operation_from(payload: object) -> RewriteOperation:
    if not isinstance(payload, dict):
        raise MemoryReconciliationError("invalid operation", "expected object")
    raw_source = payload.get("content_source")
    if not isinstance(raw_source, dict):
        raise MemoryReconciliationError("invalid content source", "expected object")
    sequence = payload.get("sequence")
    if not isinstance(sequence, int) or isinstance(sequence, bool):
        raise MemoryReconciliationError("invalid operation sequence", repr(sequence))
    source = ContentSource(
        kind=_require_string(raw_source, "kind"),  # type: ignore[arg-type]
        git_sha=_optional_string(raw_source, "git_sha"),
        git_path=_optional_string(raw_source, "git_path"),
        inline_base64=_optional_string(raw_source, "inline_base64"),
    )
    return RewriteOperation(
        operation_id=_require_string(payload, "operation_id"),
        sequence=sequence,
        path=_require_string(payload, "path"),
        action=_require_string(payload, "action"),  # type: ignore[arg-type]
        preimage_sha256=_optional_string(payload, "preimage_sha256"),
        postimage_sha256=_optional_string(payload, "postimage_sha256"),
        post_mode=_require_string(payload, "post_mode"),  # type: ignore[arg-type]
        content_source=source,
    )


def plan_from_payload(payload: Mapping[str, object]) -> ReconciliationPlan:
    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, int) or isinstance(schema_version, bool):
        raise MemoryReconciliationError("invalid schema version", repr(schema_version))
    raw_ledger = payload.get("ledger")
    raw_operations = payload.get("operations")
    raw_unchanged = payload.get("expected_unchanged_paths")
    raw_decisions = payload.get("human_decisions")
    raw_expectations = payload.get("post_check_expectations")
    if not isinstance(raw_ledger, list) or not isinstance(raw_operations, list):
        raise MemoryReconciliationError("invalid plan collections", "ledger/operations")
    if not isinstance(raw_unchanged, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in raw_unchanged.items()
    ):
        raise MemoryReconciliationError("invalid expected unchanged paths", "mapping")
    if not isinstance(raw_decisions, list) or not all(
        isinstance(item, dict)
        and all(isinstance(key, str) and isinstance(value, str) for key, value in item.items())
        for item in raw_decisions
    ):
        raise MemoryReconciliationError("invalid human decisions", "sequence")
    if not isinstance(raw_expectations, list) or not all(
        isinstance(item, str) for item in raw_expectations
    ):
        raise MemoryReconciliationError("invalid post-check expectations", "sequence")
    return ReconciliationPlan(
        schema_version=schema_version,
        report_id=_require_string(payload, "report_id"),
        context=_context_from(payload.get("context")),
        scan_sha256=_require_string(payload, "scan_sha256"),
        ledger=tuple(_ledger_row_from(item) for item in raw_ledger),
        operations=tuple(_operation_from(item) for item in raw_operations),
        expected_unchanged_paths=dict(raw_unchanged),
        human_decisions=tuple(dict(item) for item in raw_decisions),
        post_check_expectations=tuple(raw_expectations),
        plan_sha256=_require_string(payload, "plan_sha256"),
    )


def load_plan_from_report(report_path: Path) -> ReconciliationPlan:
    try:
        text = report_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise MemoryReconciliationError("cannot read report", str(report_path)) from error
    return plan_from_payload(extract_plan_payload(text))


def compute_plan_sha256(plan: ReconciliationPlan) -> str:
    return canonical_plan_hash(plan)


def _syntactic_safe_path(value: str) -> None:
    safe_relative_path(value, Path("/__agent_loop_memory_contract_root__"))


def _validate_operation_semantics(
    row: PathLedgerRow, operation: RewriteOperation
) -> None:
    current = row.snapshots["result"]
    present_file = (
        current.state == "present"
        and current.kind == "file"
        and current.git_mode in ("100644", "100755")
        and current.sha256 is not None
    )
    writes_file = (
        operation.post_mode in ("100644", "100755")
        and operation.postimage_sha256 is not None
        and operation.content_source.kind != "none"
    )

    if operation.action == "引入":
        valid = current.state == "absent" and operation.preimage_sha256 is None and writes_file
    elif operation.action == "重写":
        valid = (
            present_file
            and operation.preimage_sha256 == current.sha256
            and writes_file
        )
    elif operation.action == "重算":
        valid = writes_file and (
            (current.state == "absent" and operation.preimage_sha256 is None)
            or (present_file and operation.preimage_sha256 == current.sha256)
        )
    else:
        valid = (
            operation.action == "移除过时声明"
            and present_file
            and operation.preimage_sha256 == current.sha256
            and operation.post_mode == "absent"
            and operation.postimage_sha256 is None
            and operation.content_source.kind == "none"
        )
    if not valid:
        raise MemoryReconciliationError(
            "operation semantics", f"{operation.action}: {operation.path}"
        )

    if row.semantic_role in ("human-source", "accepted-authority"):
        source = operation.content_source
        if (
            operation.action != "引入"
            or source.kind != "git-blob"
            or source.git_path != row.path
        ):
            raise MemoryReconciliationError(
                f"{row.semantic_role} import",
                f"requires an exact same-path recorded Git blob: {row.path}",
            )


def validate_plan_contract(plan: ReconciliationPlan) -> None:
    if plan.schema_version != 1:
        raise MemoryReconciliationError("schema version", str(plan.schema_version))
    if not LOWER_SHA256.fullmatch(plan.scan_sha256):
        raise MemoryReconciliationError("scan hash", plan.scan_sha256)
    if not LOWER_SHA256.fullmatch(plan.plan_sha256):
        raise MemoryReconciliationError("plan hash", plan.plan_sha256)
    if not FULL_GIT_SHA.fullmatch(plan.context.merged_code_sha):
        raise MemoryReconciliationError("Merged Code SHA", plan.context.merged_code_sha)
    validate_merge_context_text(asdict(plan.context))
    report_sha_prefix = plan.report_id.removeprefix("MM-")
    if (
        not re.fullmatch(r"[0-9a-f]{12,64}", report_sha_prefix)
        or len(report_sha_prefix) > len(plan.context.merged_code_sha)
        or plan.context.merged_code_sha[: len(report_sha_prefix)] != report_sha_prefix
    ):
        raise MemoryReconciliationError(
            "report identity", f"{plan.report_id} does not match full Merged Code SHA"
        )
    if plan.context.memory_root not in (".agent-loop", "agent-loop"):
        raise MemoryReconciliationError("memory root", plan.context.memory_root)
    if not plan.post_check_expectations:
        raise MemoryReconciliationError("post-check expectations", "empty")

    paths = [row.path for row in plan.ledger]
    if len(paths) != len(set(paths)):
        raise MemoryReconciliationError("ledger", "duplicate path")
    _validate_collision_free(paths)
    operation_by_id: dict[str, RewriteOperation] = {}
    total_inline = 0
    for operation in plan.operations:
        _syntactic_safe_path(operation.path)
        if operation.operation_id in operation_by_id:
            raise MemoryReconciliationError("operation", "duplicate operation id")
        operation_by_id[operation.operation_id] = operation
        if operation.action not in ("引入", "重写", "重算", "移除过时声明"):
            raise MemoryReconciliationError("operation action", operation.action)
        if operation.post_mode not in ("100644", "100755", "absent"):
            raise MemoryReconciliationError("operation mode", operation.post_mode)
        for digest in (operation.preimage_sha256, operation.postimage_sha256):
            if digest is not None and not LOWER_SHA256.fullmatch(digest):
                raise MemoryReconciliationError("operation hash", operation.operation_id)
        source = operation.content_source
        if source.kind == "inline-base64":
            if source.inline_base64 is None or source.git_sha is not None or source.git_path is not None:
                raise MemoryReconciliationError("inline payload", operation.operation_id)
            content = decode_inline_payload(source.inline_base64)
            if len(content) > 2 * 1024 * 1024:
                raise MemoryReconciliationError("inline payload size", operation.operation_id)
            total_inline += len(content)
            if operation.postimage_sha256 != sha256_bytes(content):
                raise MemoryReconciliationError("inline payload hash", operation.operation_id)
        elif source.kind == "git-blob":
            if source.git_sha is None or source.git_path is None or source.inline_base64 is not None:
                raise MemoryReconciliationError("git-blob source", operation.operation_id)
            if source.git_sha not in {
                plan.context.merge_base_sha,
                plan.context.source_sha,
                plan.context.target_before_sha,
                plan.context.merged_code_sha,
            }:
                raise MemoryReconciliationError("git-blob context", operation.operation_id)
            try:
                _syntactic_safe_path(source.git_path)
            except MemoryReconciliationError as error:
                raise MemoryReconciliationError("git-blob path", source.git_path) from error
        elif source.kind == "none":
            if any((source.git_sha, source.git_path, source.inline_base64)):
                raise MemoryReconciliationError("none content source", operation.operation_id)
            if operation.post_mode != "absent" or operation.postimage_sha256 is not None:
                raise MemoryReconciliationError("none content source", operation.operation_id)
        else:
            raise MemoryReconciliationError("content source kind", str(source.kind))
    if total_inline > 8 * 1024 * 1024:
        raise MemoryReconciliationError("inline payload total size", str(total_inline))
    sequences = [operation.sequence for operation in plan.operations]
    if sequences != list(range(1, len(sequences) + 1)):
        raise MemoryReconciliationError("operation sequence", repr(sequences))

    owner_count: dict[str, int] = {key: 0 for key in operation_by_id}
    for row in plan.ledger:
        _syntactic_safe_path(row.path)
        if set(row.snapshots) != set(SNAPSHOT_KEYS):
            raise MemoryReconciliationError("ledger snapshots", row.path)
        if row.semantic_role not in SEMANTIC_ROLES:
            raise MemoryReconciliationError("semantic role", row.path)
        if row.semantic_role == "unclassified":
            raise MemoryReconciliationError("unclassified ledger row", row.path)
        if row.attention not in ATTENTION_LEVELS or row.attention == "🔴":
            raise MemoryReconciliationError("unresolved red row", row.path)
        if row.action not in ACTIONS:
            raise MemoryReconciliationError("ledger action", row.path)
        if row.action == "暂不处理":
            raise MemoryReconciliationError("暂不处理", row.path)
        if row.semantic_role in ("human-source", "accepted-authority") and row.action not in (
            "保留",
            "引入",
        ):
            raise MemoryReconciliationError(row.semantic_role, f"rewrite forbidden: {row.path}")
        if row.semantic_role == "append-only-evidence" and row.action not in (
            "保留",
            "引入",
            "重写",
        ):
            raise MemoryReconciliationError("append-only", f"action forbidden: {row.path}")
        if row.semantic_role == "derived-index" and row.action not in ("保留", "引入", "重算"):
            raise MemoryReconciliationError("derived-index", f"action forbidden: {row.path}")
        if row.action == "移除过时声明" and row.semantic_role not in (
            "current-semantic-state",
            "derived-index",
        ):
            raise MemoryReconciliationError("stale removal role", row.path)
        result_entry = row.snapshots["result"]
        if result_entry.kind == "directory" and row.operation_id is not None:
            raise MemoryReconciliationError("directory operation", row.path)
        if row.action == "保留":
            if row.operation_id is not None:
                raise MemoryReconciliationError("retain operation", row.path)
        elif row.operation_id is None:
            raise MemoryReconciliationError("missing operation", row.path)
        if row.operation_id is not None:
            operation = operation_by_id.get(row.operation_id)
            if operation is None or operation.path != row.path or operation.action != row.action:
                raise MemoryReconciliationError("operation owner", row.path)
            _validate_operation_semantics(row, operation)
            owner_count[row.operation_id] += 1
            if row.semantic_role == "append-only-evidence" and row.action == "重写":
                if operation.preimage_sha256 is None or operation.content_source.kind != "inline-base64":
                    raise MemoryReconciliationError("append-only", row.path)
                current = row.snapshots["result"]
                if current.sha256 != operation.preimage_sha256:
                    raise MemoryReconciliationError("append-only preimage", row.path)
    if any(count != 1 for count in owner_count.values()):
        raise MemoryReconciliationError("operation without ledger owner", repr(owner_count))

    for path, digest in plan.expected_unchanged_paths.items():
        _syntactic_safe_path(path)
        if not LOWER_SHA256.fullmatch(digest):
            raise MemoryReconciliationError("unchanged path hash", path)
    if compute_plan_sha256(plan) != plan.plan_sha256:
        raise MemoryReconciliationError("self-inconsistent plan hash", plan.report_id)


def _report_text_and_status(report_path: Path) -> tuple[str, ReportStatus]:
    text = report_path.read_text(encoding="utf-8")
    matches = re.findall(r"(?m)^状态:\s*(待确认|已完成|已恢复)\s*$", text)
    if len(matches) != 1:
        raise MemoryReconciliationError("report status", "expected exactly one")
    return text, matches[0]  # type: ignore[return-value]


def _validate_report_identity(
    project_root: Path, report_path: Path, plan: ReconciliationPlan
) -> Path:
    memory_root = project_root / plan.context.memory_root
    try:
        relative = report_path.resolve().relative_to(memory_root.resolve())
    except ValueError as error:
        raise MemoryReconciliationError("report path", "outside memory root") from error
    if relative.parts != ("memory-merges", plan.report_id, "README.md"):
        raise MemoryReconciliationError("report identity", relative.as_posix())
    text = report_path.read_text(encoding="utf-8")
    ids = re.findall(r"(?m)^Memory Merge ID:\s*(MM-[0-9a-f]+)\s*$", text)
    if ids != [plan.report_id]:
        raise MemoryReconciliationError("report identity", "metadata/path/plan mismatch")
    return memory_root


def _validate_unique_merged_code_report(
    memory_root: Path, report_path: Path, plan: ReconciliationPlan
) -> None:
    reports_root = memory_root / "memory-merges"
    if not reports_root.exists():
        return
    if reports_root.is_symlink() or not reports_root.is_dir():
        raise MemoryReconciliationError("memory merge reports", "unsafe container")
    current_report = report_path.resolve()
    for directory in sorted(reports_root.iterdir(), key=lambda item: item.name):
        if directory.is_symlink() or not directory.is_dir():
            continue
        candidate = directory / "README.md"
        if not candidate.is_file() or candidate.is_symlink():
            continue
        if candidate.resolve() == current_report:
            continue
        try:
            candidate_plan = load_plan_from_report(candidate)
        except MemoryReconciliationError:
            continue
        if candidate_plan.context.merged_code_sha == plan.context.merged_code_sha:
            raise MemoryReconciliationError(
                "merged code report uniqueness",
                f"{candidate_plan.report_id} already owns {plan.context.merged_code_sha}",
            )


def _scan_for_plan(
    project_root: Path, report_path: Path, context: MergeContext
) -> dict[str, object]:
    command = [
        sys.executable,
        str(Path(__file__).with_name("scan-memory-reconciliation.py")),
        "--project-root",
        str(project_root),
        "--merge-base-sha",
        context.merge_base_sha,
        "--source-sha",
        context.source_sha,
        "--target-before-sha",
        context.target_before_sha,
        "--merged-code-sha",
        context.merged_code_sha,
        "--source-branch",
        context.source_branch,
        "--target-branch",
        context.target_branch,
        "--target-release-context",
        context.target_release_context,
        "--customer-boundary",
        context.customer_boundary,
        "--report",
        str(report_path),
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode:
        raise MemoryReconciliationError("scan validation", result.stderr.strip())
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise MemoryReconciliationError("scan validation", "invalid JSON") from error
    if not isinstance(payload, dict):
        raise MemoryReconciliationError("scan validation", "expected object")
    return payload


def _ledger_snapshot_payload(row: PathLedgerRow) -> dict[str, object]:
    return {
        "path": row.path,
        "snapshots": {
            key: snapshot_entry_payload(row.snapshots[key]) for key in SNAPSHOT_KEYS
        },
    }


def _validate_context(project_root: Path, plan: ReconciliationPlan) -> None:
    validate_merge_context_text(asdict(plan.context))
    for value in (
        plan.context.merge_base_sha,
        plan.context.source_sha,
        plan.context.target_before_sha,
        plan.context.merged_code_sha,
    ):
        if resolve_commit(project_root, value) != value:
            raise MemoryReconciliationError("non-full commit SHA", value)
    if resolve_commit(project_root, "HEAD") != plan.context.merged_code_sha:
        raise MemoryReconciliationError("HEAD mismatch", plan.context.merged_code_sha)
    if resolve_memory_root(project_root) != plan.context.memory_root:
        raise MemoryReconciliationError("memory root mismatch", plan.context.memory_root)


def _read_regular_git_blob(
    project_root: Path, memory_root: str, git_sha: str, git_path: str
) -> bytes:
    full_path = f"{memory_root}/{git_path}"
    raw = _git_bytes(project_root, "ls-tree", "-z", git_sha, "--", full_path)
    records = [record for record in raw.split(b"\x00") if record]
    if len(records) != 1:
        raise MemoryReconciliationError("regular git blob", f"missing or ambiguous: {git_path}")
    try:
        metadata, encoded_path = records[0].split(b"\t", 1)
        mode, object_type, oid = metadata.split(b" ", 2)
        recorded_path = encoded_path.decode("utf-8", errors="strict")
    except (ValueError, UnicodeDecodeError) as error:
        raise MemoryReconciliationError("regular git blob", git_path) from error
    if (
        recorded_path != full_path
        or mode not in (b"100644", b"100755")
        or object_type != b"blob"
    ):
        raise MemoryReconciliationError(
            "regular git blob",
            f"requires 100644/100755 blob, got {mode.decode(errors='replace')} "
            f"{object_type.decode(errors='replace')}: {git_path}",
        )
    return _git_bytes(project_root, "cat-file", "blob", oid.decode("ascii"))


def _validate_git_blob_sources(project_root: Path, plan: ReconciliationPlan) -> None:
    for operation in plan.operations:
        source = operation.content_source
        if source.kind != "git-blob":
            continue
        assert source.git_sha is not None and source.git_path is not None
        content = _read_regular_git_blob(
            project_root, plan.context.memory_root, source.git_sha, source.git_path
        )
        if sha256_bytes(content) != operation.postimage_sha256:
            raise MemoryReconciliationError("git-blob content", operation.operation_id)


def _validate_append_only_bytes(memory_root: Path, plan: ReconciliationPlan) -> None:
    rows = {row.operation_id: row for row in plan.ledger if row.operation_id}
    for operation in plan.operations:
        row = rows[operation.operation_id]
        if row.semantic_role != "append-only-evidence" or operation.action != "重写":
            continue
        path = safe_relative_path(operation.path, memory_root)
        preimage = path.read_bytes()
        source = operation.content_source
        assert source.inline_base64 is not None
        postimage = decode_inline_payload(source.inline_base64)
        if not postimage.startswith(preimage) or len(postimage) <= len(preimage):
            raise MemoryReconciliationError("append-only truncation", operation.path)


def _validate_preimages(memory_root: Path, plan: ReconciliationPlan) -> None:
    current = inventory_worktree(
        memory_root,
        excluded_prefixes=(f"memory-merges/{plan.report_id}",),
    )
    for operation in plan.operations:
        entry = current.get(operation.path, absent_entry())
        if entry.sha256 != operation.preimage_sha256:
            raise MemoryReconciliationError("preimage mismatch", operation.path)
    for path, digest in plan.expected_unchanged_paths.items():
        entry = current.get(path, absent_entry())
        if entry.sha256 != digest:
            raise MemoryReconciliationError("unchanged path mismatch", path)


def _validate_postimages(memory_root: Path, plan: ReconciliationPlan) -> None:
    current = inventory_worktree(
        memory_root,
        excluded_prefixes=(f"memory-merges/{plan.report_id}",),
    )
    for operation in plan.operations:
        entry = current.get(operation.path, absent_entry())
        if operation.post_mode == "absent":
            if entry.state != "absent":
                raise MemoryReconciliationError("postimage mismatch", operation.path)
        elif entry.sha256 != operation.postimage_sha256 or entry.git_mode != operation.post_mode:
            raise MemoryReconciliationError("postimage mismatch", operation.path)
    _validate_retained_postimages(current, plan, after_apply=True)
    for path, digest in plan.expected_unchanged_paths.items():
        if current.get(path, absent_entry()).sha256 != digest:
            raise MemoryReconciliationError("unchanged path mismatch", path)


def _validate_retained_postimages(
    current: Mapping[str, SnapshotEntry],
    plan: ReconciliationPlan,
    *,
    after_apply: bool = False,
    allow_transitional_directories: bool = False,
) -> None:
    for row in plan.ledger:
        if row.operation_id is not None:
            continue
        entry = current.get(row.path, absent_entry())
        result_entry = row.snapshots["result"]
        desired_entry = result_entry
        creates_directory = (
            result_entry.state == "absent"
            and any(
                snapshot.state == "present" and snapshot.kind == "directory"
                for snapshot in row.snapshots.values()
            )
            and any(
                operation.post_mode != "absent"
                and operation.path.startswith(f"{row.path}/")
                for operation in plan.operations
            )
        )
        if after_apply and creates_directory:
            desired_entry = SnapshotEntry(
                "present", "directory", "040000", None, None
            )
        allowed = (desired_entry,)
        if allow_transitional_directories and creates_directory:
            allowed = (result_entry, desired_entry)
        if entry not in allowed:
            raise MemoryReconciliationError("retained postimage mismatch", row.path)


def _validate_ledger_against_scan(
    plan: ReconciliationPlan, scan: Mapping[str, object], *, exact_result: bool
) -> None:
    raw_paths = scan.get("paths")
    if not isinstance(raw_paths, list):
        raise MemoryReconciliationError("scan paths", "missing")
    scanned = {str(row.get("path")): row for row in raw_paths if isinstance(row, dict)}
    planned = {row.path: row for row in plan.ledger}
    if set(scanned) != set(planned):
        raise MemoryReconciliationError(
            "ledger path accounting / unexpected dirty memory",
            f"scan-only={sorted(set(scanned)-set(planned))}, plan-only={sorted(set(planned)-set(scanned))}",
        )
    for path, row in planned.items():
        scanned_snapshots = scanned[path].get("snapshots")
        expected = _ledger_snapshot_payload(row)["snapshots"]
        if not isinstance(scanned_snapshots, dict):
            raise MemoryReconciliationError("scan snapshots", path)
        keys = SNAPSHOT_KEYS if exact_result else SNAPSHOT_KEYS[:-1]
        for key in keys:
            if scanned_snapshots.get(key) != expected[key]:
                raise MemoryReconciliationError(
                    "ledger snapshot / unexpected dirty memory", f"{path}:{key}"
                )


def _base_validation(
    project_root: Path, report_path: Path, expected_hash: str
) -> tuple[ReconciliationPlan, Path, str, ReportStatus, dict[str, object]]:
    if not LOWER_SHA256.fullmatch(expected_hash):
        raise MemoryReconciliationError("expected plan hash", expected_hash)
    plan = load_plan_from_report(report_path)
    validate_plan_contract(plan)
    if plan.plan_sha256 != expected_hash:
        raise MemoryReconciliationError("expected plan hash mismatch", expected_hash)
    memory_root = _validate_report_identity(project_root, report_path, plan)
    _validate_unique_merged_code_report(memory_root, report_path, plan)
    text, status = _report_text_and_status(report_path)
    _validate_context(project_root, plan)
    _validate_git_blob_sources(project_root, plan)
    scan = _scan_for_plan(project_root, report_path, plan.context)
    return plan, memory_root, text, status, scan


def _result(
    plan: ReconciliationPlan,
    status: ReportStatus,
    memory_root: Path,
    *,
    zero_change: bool,
) -> ValidationResult:
    inventory = inventory_worktree(
        memory_root, excluded_prefixes=(f"memory-merges/{plan.report_id}",)
    )
    return ValidationResult(
        context=plan.context,
        ledger=plan.ledger,
        operations=plan.operations,
        report_status=status,
        current_hashes={path: entry.sha256 or entry.kind for path, entry in inventory.items()},
        blockers=(),
        zero_change=zero_change,
    )


def validate_pre_apply(
    project_root: Path, report_path: Path, expected_hash: str
) -> ValidationResult:
    plan, memory_root, _text, status, scan = _base_validation(
        project_root, report_path, expected_hash
    )
    if status != "待确认":
        raise MemoryReconciliationError("report status", f"pre-apply requires 待确认, got {status}")
    _validate_ledger_against_scan(plan, scan, exact_result=True)
    if scan.get("scan_sha256") != plan.scan_sha256:
        raise MemoryReconciliationError("stale scan hash", plan.report_id)
    _validate_preimages(memory_root, plan)
    _validate_append_only_bytes(memory_root, plan)
    return _result(plan, status, memory_root, zero_change=bool(scan.get("zero_change")))


def validate_post_apply(
    project_root: Path, report_path: Path, expected_hash: str
) -> ValidationResult:
    plan, memory_root, text, status, scan = _base_validation(
        project_root, report_path, expected_hash
    )
    if status != "待确认":
        raise MemoryReconciliationError("report status", f"post-apply requires 待确认, got {status}")
    _validate_ledger_against_scan(plan, scan, exact_result=False)
    _validate_postimages(memory_root, plan)
    if "Machine check: pass" not in text:
        raise MemoryReconciliationError("post-check evidence", "machine check missing")
    if "Zero-change rescan: pass" not in text or scan.get("zero_change") is not True:
        raise MemoryReconciliationError("zero-change evidence", "missing or false")
    match = re.search(r"(?m)^Domain / semantic verification:\s*(.+)$", text)
    if not match or not match.group(1).strip().startswith("PASS:"):
        raise MemoryReconciliationError("semantic evidence", "missing bounded PASS record")
    return _result(plan, status, memory_root, zero_change=True)


def validate_restore_state(
    project_root: Path, report_path: Path, expected_hash: str
) -> ValidationResult:
    plan, memory_root, _text, status, scan = _base_validation(
        project_root, report_path, expected_hash
    )
    if status != "已恢复":
        raise MemoryReconciliationError("report status", f"restore requires 已恢复, got {status}")
    _validate_ledger_against_scan(plan, scan, exact_result=True)
    _validate_preimages(memory_root, plan)
    return _result(plan, status, memory_root, zero_change=bool(scan.get("zero_change")))


def _replace_report_status(report_path: Path, status: ReportStatus) -> None:
    text = report_path.read_text(encoding="utf-8")
    replaced, count = re.subn(
        r"(?m)^状态:\s*(?:待确认|已完成|已恢复)\s*$", f"状态: {status}", text
    )
    if count != 1:
        raise MemoryReconciliationError("report status", "expected exactly one mutable line")
    atomic_write_bytes(report_path, replaced.encode("utf-8"))


def _update_apply_evidence(report_path: Path, plan_hash: str) -> None:
    text = report_path.read_text(encoding="utf-8")
    text = text.replace("Status: not-run | applied-checking | failed", "Status: applied-checking")
    text = re.sub(
        r"(?m)^Applied Plan Hash:\s*$", f"Applied Plan Hash: {plan_hash}", text, count=1
    )
    atomic_write_bytes(report_path, text.encode("utf-8"))


def _transaction_root(report_path: Path) -> Path:
    return report_path.parent / ".memory-reconciliation-txn"


def _journal_path(report_path: Path, transaction_id: str) -> Path:
    if not re.fullmatch(r"\d{8}T\d{6}Z-[0-9a-f]{12}", transaction_id):
        raise MemoryReconciliationError("transaction id", transaction_id)
    return _transaction_root(report_path) / transaction_id / "journal.json"


def existing_transaction_journals(report_path: Path) -> list[Path]:
    root = _transaction_root(report_path)
    if not root.exists():
        return []
    if root.is_symlink() or not root.is_dir():
        raise MemoryReconciliationError("transaction root", "unsafe path kind")
    unexpected = [path for path in root.iterdir() if not path.is_dir() or path.is_symlink()]
    if unexpected:
        raise MemoryReconciliationError("transaction root", f"unexpected entries: {unexpected}")
    journals: list[Path] = []
    for directory in sorted(root.iterdir()):
        journal = directory / "journal.json"
        if not journal.is_file() or journal.is_symlink():
            raise MemoryReconciliationError("transaction", f"missing safe journal in {directory.name}")
        journals.append(journal)
    return journals


def _write_journal(path: Path, payload: Mapping[str, object]) -> None:
    atomic_write_bytes(path, canonical_json_bytes(payload) + b"\n")


def _read_journal(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise MemoryReconciliationError("transaction journal", str(path)) from error
    if not isinstance(payload, dict):
        raise MemoryReconciliationError("transaction journal", "expected object")
    return payload


def _mode_for_path(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "100755" if mode & stat.S_IXUSR else "100644"
    if stat.S_ISLNK(mode):
        return "120000"
    if stat.S_ISDIR(mode):
        return "040000"
    return "other"


def _current_state(path: Path) -> tuple[str, str | None, str | None]:
    if not path.exists() and not path.is_symlink():
        return "absent", None, None
    mode = _mode_for_path(path)
    if mode in ("100644", "100755"):
        return "present", mode, sha256_bytes(path.read_bytes())
    if mode == "120000":
        return "present", mode, sha256_bytes(os.readlink(path).encode("utf-8"))
    return "present", mode, None


def _materialize_operation(
    project_root: Path,
    memory_root: Path,
    operation: RewriteOperation,
    destination: Path,
    context: MergeContext,
) -> bytes | None:
    source = operation.content_source
    if source.kind == "none":
        return None
    if source.kind == "inline-base64":
        assert source.inline_base64 is not None
        content = decode_inline_payload(source.inline_base64)
    elif source.kind == "git-blob":
        assert source.git_sha is not None and source.git_path is not None
        safe_relative_path(source.git_path, memory_root)
        content = _read_regular_git_blob(
            project_root, context.memory_root, source.git_sha, source.git_path
        )
    else:
        raise MemoryReconciliationError("content source", str(source.kind))
    if sha256_bytes(content) != operation.postimage_sha256:
        raise MemoryReconciliationError("materialized postimage hash", operation.operation_id)
    atomic_write_bytes(destination, content)
    if sha256_bytes(destination.read_bytes()) != operation.postimage_sha256:
        raise MemoryReconciliationError("materialized verification", operation.operation_id)
    return content


def _test_failure_value() -> str | None:
    value = os.environ.get("AGENT_LOOP_TEST_FAILURE")
    if value and os.environ.get("AGENT_LOOP_ALLOW_TEST_HOOKS") != "1":
        raise MemoryReconciliationError(
            "test hook forbidden", "AGENT_LOOP_TEST_FAILURE requires explicit test-only enablement"
        )
    return value


def _created_parents(memory_root: Path, target: Path) -> list[str]:
    missing: list[Path] = []
    current = target.parent
    while current != memory_root and not current.exists():
        missing.append(current)
        current = current.parent
    if current.is_symlink():
        raise MemoryReconciliationError("symlink parent", str(target))
    created: list[str] = []
    for directory in reversed(missing):
        directory.mkdir()
        created.append(directory.relative_to(memory_root).as_posix())
    return created


def apply_reconciliation(
    project_root: Path, report_path: Path, expected_hash: str
) -> str:
    if existing_transaction_journals(report_path):
        raise MemoryReconciliationError("existing unrestored transaction", str(report_path.parent))
    plan = load_plan_from_report(report_path)
    _text, status = _report_text_and_status(report_path)
    if status == "已完成":
        raise MemoryReconciliationError("completed report replay", plan.report_id)
    if status == "已恢复":
        raise MemoryReconciliationError("restored report requires new reviewed plan", plan.report_id)
    validate_pre_apply(project_root, report_path, expected_hash)
    failure = _test_failure_value()
    memory_root = project_root / plan.context.memory_root
    transaction_id = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "-"
        + secrets.token_hex(6)
    )
    journal_path = _journal_path(report_path, transaction_id)
    transaction_dir = journal_path.parent
    backup_dir = transaction_dir / "backups"
    materialized_dir = transaction_dir / "materialized"
    backup_dir.mkdir(parents=True)
    materialized_dir.mkdir()
    journal_operations: list[dict[str, object]] = []
    try:
        for operation in plan.operations:
            target = safe_relative_path(operation.path, memory_root)
            state, mode, digest = _current_state(target)
            if mode not in (None, "100644", "100755"):
                raise MemoryReconciliationError("unsupported operation target", operation.path)
            backup_relative: str | None = None
            if state == "present":
                backup = backup_dir / f"{operation.sequence:04d}.bin"
                atomic_write_bytes(backup, target.read_bytes())
                if sha256_bytes(backup.read_bytes()) != digest:
                    raise MemoryReconciliationError("backup verification", operation.path)
                backup_relative = backup.relative_to(transaction_dir).as_posix()
            journal_operations.append(
                {
                    "operation_id": operation.operation_id,
                    "sequence": operation.sequence,
                    "path": operation.path,
                    "action": operation.action,
                    "original_state": state,
                    "original_mode": mode,
                    "original_sha256": digest,
                    "backup_relative": backup_relative,
                    "post_mode": operation.post_mode,
                    "post_sha256": operation.postimage_sha256,
                }
            )
        journal: dict[str, object] = {
            "schema_version": 1,
            "transaction_id": transaction_id,
            "report_id": plan.report_id,
            "plan_sha256": plan.plan_sha256,
            "merged_code_sha": plan.context.merged_code_sha,
            "memory_root": plan.context.memory_root,
            "state": "prepared",
            "operations": journal_operations,
            "completed_operations": [],
            "created_directories": [],
        }
        _write_journal(journal_path, journal)
        journal["state"] = "applying"
        _write_journal(journal_path, journal)
        operations = {operation.operation_id: operation for operation in plan.operations}
        for raw in journal_operations:
            operation = operations[str(raw["operation_id"])]
            target = safe_relative_path(operation.path, memory_root)
            state, _mode, digest = _current_state(target)
            expected_state = "absent" if operation.preimage_sha256 is None else "present"
            if state != expected_state or digest != operation.preimage_sha256:
                raise MemoryReconciliationError("preimage drift", operation.path)
            created = _created_parents(memory_root, target)
            journal["created_directories"] = [
                *journal["created_directories"],  # type: ignore[misc]
                *created,
            ]
            if created:
                _write_journal(journal_path, journal)
            materialized = materialized_dir / f"{operation.sequence:04d}.bin"
            content = _materialize_operation(
                project_root, memory_root, operation, materialized, plan.context
            )
            if operation.post_mode == "absent":
                if target.is_dir() or target.is_symlink():
                    raise MemoryReconciliationError("unsafe removal target", operation.path)
                target.unlink()
            else:
                assert content is not None
                atomic_write_bytes(target, content)
                target.chmod(0o755 if operation.post_mode == "100755" else 0o644)
            if failure == f"crash-after-write-{operation.sequence}":
                os._exit(91)
            post_state, post_mode, post_hash = _current_state(target)
            expected_post_state = "absent" if operation.post_mode == "absent" else "present"
            if (
                post_state != expected_post_state
                or post_mode != (None if operation.post_mode == "absent" else operation.post_mode)
                or post_hash != operation.postimage_sha256
            ):
                raise MemoryReconciliationError("postimage verification", operation.path)
            journal["completed_operations"] = [
                *journal["completed_operations"],  # type: ignore[misc]
                operation.operation_id,
            ]
            _write_journal(journal_path, journal)
            if failure == f"fail-after-{operation.sequence}":
                raise MemoryReconciliationError("injected mid-apply failure", operation.operation_id)
        journal["state"] = "checking"
        _write_journal(journal_path, journal)
        _update_apply_evidence(report_path, plan.plan_sha256)
        return transaction_id
    except BaseException as error:
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            raise
        try:
            if journal_path.exists():
                restore_transaction(project_root, report_path, transaction_id)
        except BaseException as restore_error:
            raise MemoryReconciliationError(
                "apply failed and restore incomplete", f"{error}; restore: {restore_error}"
            ) from error
        if isinstance(error, MemoryReconciliationError):
            raise
        raise MemoryReconciliationError("apply failure", str(error)) from error


def _validate_transaction_identity(
    report_path: Path, journal: Mapping[str, object], transaction_id: str
) -> ReconciliationPlan:
    if journal.get("schema_version") != 1:
        raise MemoryReconciliationError("transaction schema", transaction_id)
    if journal.get("transaction_id") != transaction_id:
        raise MemoryReconciliationError("transaction identity", transaction_id)
    plan = load_plan_from_report(report_path)
    validate_plan_contract(plan)
    if (
        journal.get("report_id") != plan.report_id
        or journal.get("plan_sha256") != plan.plan_sha256
        or journal.get("merged_code_sha") != plan.context.merged_code_sha
        or journal.get("memory_root") != plan.context.memory_root
    ):
        raise MemoryReconciliationError("transaction/report/plan identity", transaction_id)

    raw_operations = journal.get("operations")
    if not isinstance(raw_operations, list) or len(raw_operations) != len(plan.operations):
        raise MemoryReconciliationError("transaction operations", "plan cardinality mismatch")
    for raw, operation in zip(raw_operations, plan.operations, strict=True):
        if not isinstance(raw, dict):
            raise MemoryReconciliationError("transaction operation", "invalid")
        expected = {
            "operation_id": operation.operation_id,
            "sequence": operation.sequence,
            "path": operation.path,
            "action": operation.action,
            "post_mode": operation.post_mode,
            "post_sha256": operation.postimage_sha256,
        }
        if any(raw.get(key) != value for key, value in expected.items()):
            raise MemoryReconciliationError(
                "transaction operation/plan mismatch", operation.operation_id
            )
        if operation.preimage_sha256 is None:
            original = {
                "original_state": "absent",
                "original_mode": None,
                "original_sha256": None,
                "backup_relative": None,
            }
        else:
            original_mode = raw.get("original_mode")
            if original_mode not in ("100644", "100755"):
                raise MemoryReconciliationError(
                    "transaction original mode", operation.operation_id
                )
            original = {
                "original_state": "present",
                "original_mode": original_mode,
                "original_sha256": operation.preimage_sha256,
                "backup_relative": f"backups/{operation.sequence:04d}.bin",
            }
        if any(raw.get(key) != value for key, value in original.items()):
            raise MemoryReconciliationError(
                "transaction original/plan mismatch", operation.operation_id
            )

    completed = journal.get("completed_operations")
    operation_ids = [operation.operation_id for operation in plan.operations]
    if (
        not isinstance(completed, list)
        or not all(isinstance(item, str) for item in completed)
        or completed != operation_ids[: len(completed)]
    ):
        raise MemoryReconciliationError("transaction completion ledger", transaction_id)

    created = journal.get("created_directories")
    if not isinstance(created, list) or not all(isinstance(item, str) for item in created):
        raise MemoryReconciliationError("transaction created directories", transaction_id)
    if len(created) != len(set(created)):
        raise MemoryReconciliationError("transaction created directories", "duplicates")
    ledger_by_path = {row.path: row for row in plan.ledger}
    for relative in created:
        _syntactic_safe_path(relative)
        if not any(
            operation.path.startswith(f"{relative}/") for operation in plan.operations
        ):
            raise MemoryReconciliationError(
                "transaction created directory outside plan", relative
            )
        row = ledger_by_path.get(relative)
        if row is not None and row.snapshots["result"].state != "absent":
            raise MemoryReconciliationError(
                "transaction created directory existed before apply", relative
            )
    return plan


def _finish_restored_transaction(
    project_root: Path,
    report_path: Path,
    transaction_dir: Path,
    plan: ReconciliationPlan,
) -> None:
    _text, report_status = _report_text_and_status(report_path)
    if report_status not in ("待确认", "已恢复"):
        raise MemoryReconciliationError(
            "restore report status", f"cannot finish restored transaction from {report_status}"
        )
    memory_root = project_root / plan.context.memory_root
    restored_scan = _scan_for_plan(project_root, report_path, plan.context)
    _validate_ledger_against_scan(plan, restored_scan, exact_result=True)
    _validate_preimages(memory_root, plan)
    restored_inventory = inventory_worktree(
        memory_root, excluded_prefixes=(f"memory-merges/{plan.report_id}",)
    )
    _validate_retained_postimages(restored_inventory, plan)
    if report_status == "待确认":
        _replace_report_status(report_path, "已恢复")
    validate_restore_state(project_root, report_path, plan.plan_sha256)
    shutil.rmtree(transaction_dir)
    root = _transaction_root(report_path)
    if root.exists() and not any(root.iterdir()):
        root.rmdir()


def restore_transaction(
    project_root: Path, report_path: Path, transaction_id: str
) -> None:
    journal_path = _journal_path(report_path, transaction_id)
    if not journal_path.is_file() or journal_path.is_symlink():
        raise MemoryReconciliationError("transaction journal", transaction_id)
    transaction_dir = journal_path.parent
    journal = _read_journal(journal_path)
    plan = _validate_transaction_identity(report_path, journal, transaction_id)
    _text, report_status = _report_text_and_status(report_path)
    if journal.get("state") == "restored":
        _finish_restored_transaction(
            project_root, report_path, transaction_dir, plan
        )
        return
    if report_status != "待确认":
        raise MemoryReconciliationError(
            "restore report status", f"requires 待确认, got {report_status}"
        )
    if journal.get("state") not in ("prepared", "applying", "checking", "restoring"):
        raise MemoryReconciliationError(
            "restore transaction state", str(journal.get("state"))
        )
    memory_root = project_root / plan.context.memory_root
    pre_restore_scan = _scan_for_plan(project_root, report_path, plan.context)
    _validate_ledger_against_scan(plan, pre_restore_scan, exact_result=False)
    pre_restore_inventory = inventory_worktree(
        memory_root, excluded_prefixes=(f"memory-merges/{plan.report_id}",)
    )
    _validate_retained_postimages(
        pre_restore_inventory,
        plan,
        after_apply=True,
        allow_transitional_directories=True,
    )
    raw_operations = journal.get("operations")
    if not isinstance(raw_operations, list):
        raise MemoryReconciliationError("transaction operations", "missing")
    checked: list[tuple[dict[str, object], Path, bytes | None]] = []
    for raw in raw_operations:
        if not isinstance(raw, dict):
            raise MemoryReconciliationError("transaction operation", "invalid")
        path_value = raw.get("path")
        if not isinstance(path_value, str):
            raise MemoryReconciliationError("transaction path", repr(path_value))
        target = safe_relative_path(path_value, memory_root)
        original_state = raw.get("original_state")
        original_mode = raw.get("original_mode")
        original_hash = raw.get("original_sha256")
        post_mode = raw.get("post_mode")
        post_hash = raw.get("post_sha256")
        if original_state not in ("present", "absent"):
            raise MemoryReconciliationError("transaction original state", path_value)
        backup_bytes: bytes | None = None
        backup_relative = raw.get("backup_relative")
        if original_state == "present":
            if not isinstance(backup_relative, str):
                raise MemoryReconciliationError("backup path", path_value)
            backup = transaction_dir / backup_relative
            try:
                backup.resolve().relative_to(transaction_dir.resolve())
            except ValueError as error:
                raise MemoryReconciliationError("backup path escape", backup_relative) from error
            if not backup.is_file() or backup.is_symlink():
                raise MemoryReconciliationError("backup missing", path_value)
            backup_bytes = backup.read_bytes()
            if sha256_bytes(backup_bytes) != original_hash:
                raise MemoryReconciliationError("tampered backup", path_value)
        elif backup_relative is not None:
            raise MemoryReconciliationError("unexpected backup", path_value)
        current_state, current_mode, current_hash = _current_state(target)
        matches_original = (
            current_state == original_state
            and current_mode == original_mode
            and current_hash == original_hash
        )
        expected_post_state = "absent" if post_mode == "absent" else "present"
        expected_post_mode = None if post_mode == "absent" else post_mode
        matches_post = (
            current_state == expected_post_state
            and current_mode == expected_post_mode
            and current_hash == post_hash
        )
        if not matches_original and not matches_post:
            raise MemoryReconciliationError("post-crash unrelated drift", path_value)
        checked.append((raw, target, backup_bytes))
    for path, digest in plan.expected_unchanged_paths.items():
        _state, _mode, current_hash = _current_state(safe_relative_path(path, memory_root))
        if current_hash != digest:
            raise MemoryReconciliationError("post-crash unrelated drift", path)

    journal["state"] = "restoring"
    _write_journal(journal_path, journal)
    for raw, target, backup_bytes in reversed(checked):
        original_state = raw["original_state"]
        current_state, current_mode, current_hash = _current_state(target)
        if (
            current_state == original_state
            and current_mode == raw["original_mode"]
            and current_hash == raw["original_sha256"]
        ):
            continue
        if original_state == "absent":
            if target.is_dir() or target.is_symlink():
                raise MemoryReconciliationError("restore collision", str(raw["path"]))
            target.unlink()
        else:
            assert backup_bytes is not None
            if target.is_dir() or target.is_symlink():
                raise MemoryReconciliationError("restore collision", str(raw["path"]))
            atomic_write_bytes(target, backup_bytes)
            target.chmod(0o755 if raw["original_mode"] == "100755" else 0o644)

    created = journal.get("created_directories", [])
    if not isinstance(created, list) or not all(isinstance(item, str) for item in created):
        raise MemoryReconciliationError("created directory ledger", "invalid")
    for relative in reversed(created):
        directory = safe_relative_path(relative, memory_root)
        if directory.exists() and directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    for raw, target, _backup_bytes in checked:
        state, mode, digest = _current_state(target)
        if (
            state != raw["original_state"]
            or mode != raw["original_mode"]
            or digest != raw["original_sha256"]
        ):
            raise MemoryReconciliationError("restore verification", str(raw["path"]))
    journal["state"] = "restored"
    _write_journal(journal_path, journal)
    _finish_restored_transaction(project_root, report_path, transaction_dir, plan)


def _validate_finalize(
    project_root: Path, report_path: Path, expected_hash: str, *, allow_completed: bool
) -> ValidationResult:
    plan, memory_root, text, status, scan = _base_validation(
        project_root, report_path, expected_hash
    )
    allowed = {"待确认", "已完成"} if allow_completed else {"待确认"}
    if status not in allowed:
        raise MemoryReconciliationError("report status", f"cannot finalize {status}")
    _validate_ledger_against_scan(plan, scan, exact_result=False)
    _validate_postimages(memory_root, plan)
    if "Machine check: pass" not in text:
        raise MemoryReconciliationError("post-check evidence", "machine check missing")
    if "Zero-change rescan: pass" not in text or scan.get("zero_change") is not True:
        raise MemoryReconciliationError("zero-change evidence", "missing or false")
    match = re.search(r"(?m)^Domain / semantic verification:\s*(.+)$", text)
    if not match or not match.group(1).strip().startswith("PASS:"):
        raise MemoryReconciliationError("semantic evidence", "missing bounded PASS record")
    return _result(plan, status, memory_root, zero_change=True)


def finalize_reconciliation(
    project_root: Path, report_path: Path, expected_hash: str
) -> str:
    journals = existing_transaction_journals(report_path)
    if len(journals) != 1:
        raise MemoryReconciliationError(
            "completed report without own residual transaction"
            if "状态: 已完成" in report_path.read_text(encoding="utf-8")
            else "finalize transaction",
            f"expected one journal, got {len(journals)}",
        )
    journal_path = journals[0]
    journal = _read_journal(journal_path)
    transaction_id = journal_path.parent.name
    plan = _validate_transaction_identity(report_path, journal, transaction_id)
    if plan.plan_sha256 != expected_hash:
        raise MemoryReconciliationError("expected plan hash mismatch", expected_hash)
    state = journal.get("state")
    if state not in ("checking", "verified"):
        raise MemoryReconciliationError("finalize journal state", str(state))
    result = _validate_finalize(
        project_root, report_path, expected_hash, allow_completed=state == "verified"
    )
    if state == "checking":
        journal["state"] = "verified"
        _write_journal(journal_path, journal)
    if result.report_status == "待确认":
        _replace_report_status(report_path, "已完成")
    shutil.rmtree(journal_path.parent)
    root = _transaction_root(report_path)
    if root.exists() and not any(root.iterdir()):
        root.rmdir()
    return transaction_id
