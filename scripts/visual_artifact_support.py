from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass
from pathlib import Path


ARCHIFY_TYPES = frozenset(
    {"architecture", "workflow", "sequence", "dataflow", "lifecycle"}
)
RENDER_SUFFIXES = frozenset({".html", ".svg", ".png", ".jpeg", ".jpg", ".webp"})
DIAGRAM_ID = re.compile(r"D-[A-Z0-9-]+")
GENERATOR = re.compile(r"archify@[0-9]+(?:\.[0-9]+)+")
LOWER_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True)
class DurableVisualArtifact:
    diagram_id: str
    diagram_type: str
    source_path: Path
    render_path: Path
    source_sha256: str
    render_sha256: str
    generator: str


class VisualArtifactError(ValueError):
    pass


def normalized(raw: str | None) -> str:
    text = (raw or "").strip()
    if len(text) >= 2 and text[0] == text[-1] == "`":
        text = text[1:-1].strip()
    return text


def _owned_file(root: Path, raw: str, *, label: str) -> Path:
    value = normalized(raw).replace("\\", "/")
    if not value:
        raise VisualArtifactError(f"{label} is required")
    candidate = Path(value)
    if candidate.is_absolute() or re.match(r"^[A-Za-z]:/", value):
        raise VisualArtifactError(f"{label} must be relative")
    if ".." in candidate.parts:
        raise VisualArtifactError(f"{label} escapes owning root")
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as error:
        raise VisualArtifactError(f"{label} escapes owning root") from error
    if not resolved.is_file():
        raise VisualArtifactError(f"{label} file is missing: {value}")
    return resolved


def _actual_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_durable_visual(
    root: Path,
    *,
    diagram_id: str,
    source_definition: str,
    render: str,
    diagram_type: str,
    source_sha256: str,
    render_sha256: str,
    generator: str,
    validation_evidence: str,
) -> DurableVisualArtifact:
    normalized_diagram_id = normalized(diagram_id)
    if DIAGRAM_ID.fullmatch(normalized_diagram_id) is None:
        raise VisualArtifactError("Diagram ID must match D-[A-Z0-9-]+")

    kind = normalized(diagram_type)
    if kind not in ARCHIFY_TYPES:
        raise VisualArtifactError(f"unsupported Archify Type: {kind}")

    source_path = _owned_file(root, source_definition, label="source definition")
    render_path = _owned_file(root, render, label="render")
    if source_path == render_path:
        raise VisualArtifactError("source definition and render must differ")
    if not source_path.name.endswith(f".{kind}.json"):
        raise VisualArtifactError(
            "source definition filename must include Type and .json"
        )
    if render_path.suffix.lower() not in RENDER_SUFFIXES:
        raise VisualArtifactError("unsupported render suffix")

    try:
        payload = json.loads(source_path.read_bytes().decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VisualArtifactError("source definition must be UTF-8 JSON") from error
    if not isinstance(payload, dict):
        raise VisualArtifactError("source definition root must be an object")
    if payload.get("schema_version") != 1:
        raise VisualArtifactError("source definition schema_version must be 1")
    if payload.get("diagram_type") != kind:
        raise VisualArtifactError("diagram_type does not match manifest Type")
    meta = payload.get("meta")
    if not isinstance(meta, dict) or not isinstance(meta.get("output"), str):
        raise VisualArtifactError("source definition meta.output is required")
    output_name = Path(meta["output"].replace("\\", "/")).name
    if output_name != render_path.name:
        raise VisualArtifactError("meta.output does not match render")

    expected_source = normalized(source_sha256)
    expected_render = normalized(render_sha256)
    if LOWER_SHA256.fullmatch(expected_source) is None:
        raise VisualArtifactError("source SHA-256 must be 64 lowercase hex")
    if LOWER_SHA256.fullmatch(expected_render) is None:
        raise VisualArtifactError("render SHA-256 must be 64 lowercase hex")
    if not hmac.compare_digest(_actual_sha256(source_path), expected_source):
        raise VisualArtifactError("source SHA-256 is stale")
    if not hmac.compare_digest(_actual_sha256(render_path), expected_render):
        raise VisualArtifactError("render SHA-256 is stale")

    generator_value = normalized(generator)
    if GENERATOR.fullmatch(generator_value) is None:
        raise VisualArtifactError("generator must be archify@version")
    evidence = normalized(validation_evidence).lower()
    if "validate=pass" not in evidence or "check=pass" not in evidence:
        raise VisualArtifactError(
            "validation evidence requires validate=pass and check=pass"
        )

    return DurableVisualArtifact(
        diagram_id=normalized_diagram_id,
        diagram_type=kind,
        source_path=source_path,
        render_path=render_path,
        source_sha256=expected_source,
        render_sha256=expected_render,
        generator=generator_value,
    )
