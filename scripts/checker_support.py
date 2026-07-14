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
