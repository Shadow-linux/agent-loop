from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckFailure(Exception):
    category: str
    detail: str

    def __str__(self) -> str:
        return f"{self.category}: {self.detail}"


@dataclass(frozen=True)
class MemoryRootAuthority:
    logical: Path
    resolved: Path
    alias_target: str | None


def discover_memory_root_authority(
    project_root: Path, *, allow_missing: bool = False
) -> MemoryRootAuthority | None:
    """Resolve one accepted memory root while preserving its logical project path."""
    if not project_root.exists() or not project_root.is_dir():
        raise CheckFailure("memory-root", "project root must be an existing directory")
    boundary = project_root.resolve()
    candidates = (boundary / ".agent-loop", boundary / "agent-loop")
    present = [path for path in candidates if path.exists() or path.is_symlink()]
    if len(present) > 1:
        raise CheckFailure(
            "memory-root", "both .agent-loop and legacy agent-loop exist"
        )
    if not present:
        if allow_missing:
            return None
        raise CheckFailure("memory-root", "no agent-loop memory root exists")

    logical = present[0]
    if logical.is_symlink():
        try:
            resolved = logical.resolve(strict=True)
        except RuntimeError as error:
            raise CheckFailure("memory-root", f"{logical.name} alias is cyclic") from error
        except FileNotFoundError as error:
            raise CheckFailure("memory-root", f"{logical.name} alias is broken") from error
        except OSError as error:
            raise CheckFailure(
                "memory-root", f"{logical.name} alias cannot be resolved"
            ) from error
        try:
            target = resolved.relative_to(boundary)
        except ValueError as error:
            raise CheckFailure(
                "memory-root", f"{logical.name} alias resolves outside project"
            ) from error
        if resolved == boundary or not resolved.is_dir():
            raise CheckFailure(
                "memory-root", f"{logical.name} alias must resolve to an internal directory"
            )
        return MemoryRootAuthority(logical, resolved, target.as_posix())

    if not logical.is_dir():
        raise CheckFailure("memory-root", f"{logical.name} must be a directory")
    return MemoryRootAuthority(logical, logical.resolve(), None)


def configure_utf8_stdio() -> None:
    """Make CLI output deterministic on hosts with a non-UTF-8 console code page."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="strict")


def require_supported_python(version: tuple[int, int] | None = None) -> None:
    current = version or sys.version_info[:2]
    if current < (3, 10):
        print("usage error: Python 3.10+ is required", file=sys.stderr)
        raise SystemExit(2)


def read_text(path: Path) -> str:
    """Read deterministic Markdown text, accepting UTF-8 BOM and CRLF input."""
    with path.open("r", encoding="utf-8-sig", newline=None) as handle:
        return handle.read()


def strip_code_span(value: str) -> str:
    cleaned = value.strip()
    return (
        cleaned[1:-1].strip()
        if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] == "`"
        else cleaned
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_bytes(payload: object) -> bytes:
    return json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def metadata(text: str, name: str) -> str | None:
    match = re.search(rf"(?mi)^\s*{re.escape(name)}\s*:\s*(.*?)\s*$", text)
    return match.group(1).strip() if match else None


def optional_section(text: str, heading: str, *, level: int = 2) -> str | None:
    marker = "#" * level
    pattern = re.compile(
        rf"^{re.escape(marker)}\s+{re.escape(heading)}\s*$\n"
        rf"(.*?)(?=^#{{1,{level}}}\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else None


def section(text: str, heading: str, *, level: int = 2) -> str:
    value = optional_section(text, heading, level=level)
    if value is None:
        raise CheckFailure("missing section", f"{'#' * level} {heading}")
    return value


def split_row(line: str) -> list[str]:
    value = line.strip()
    if not value.startswith("|") or not value.endswith("|"):
        raise CheckFailure("invalid-table-row", line)
    return [cell.strip() for cell in value[1:-1].split("|")]


def table(text: str, heading: str, *, level: int = 2) -> list[dict[str, str]]:
    raw_lines = [line.strip() for line in section(text, heading, level=level).splitlines()]
    try:
        table_start = next(index for index, line in enumerate(raw_lines) if line.startswith("|"))
    except StopIteration as error:
        raise CheckFailure("missing table in section", heading) from error
    lines: list[str] = []
    for line in raw_lines[table_start:]:
        if not line.startswith("|"):
            break
        lines.append(line)
    if len(lines) < 3:
        raise CheckFailure("missing table in section", heading)
    headers = split_row(lines[0])
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = split_row(line)
        if len(cells) != len(headers):
            raise CheckFailure("column count mismatch in section", heading)
        rows.append(dict(zip(headers, cells, strict=True)))
    if not rows:
        raise CheckFailure("empty table in section", heading)
    return rows


def confined_path(root: Path, value: str) -> Path:
    candidate = Path(value)
    resolved = (candidate if candidate.is_absolute() else root / candidate).resolve()
    boundary = root.resolve()
    try:
        resolved.relative_to(boundary)
    except ValueError as error:
        raise CheckFailure("reference escapes workspace root", value) from error
    return resolved
