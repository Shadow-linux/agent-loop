#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from checker_support import (
    CheckFailure,
    optional_section,
    read_text,
    require_supported_python,
    table,
)
from visual_artifact_support import VisualArtifactError, normalized, validate_durable_visual


FLOW_ID = re.compile(r"CF-[A-Z0-9-]+")
SLICE_ID_TEMPLATE = r"{flow}/S\d{{2}}"
DIAGRAM_ID = re.compile(r"D-[A-Z0-9-]+")
ONBOARDING_VISUAL_COLUMNS = (
    "Diagram ID",
    "Evidence References",
    "Source Definition",
    "Render",
    "Type",
    "Source SHA-256",
    "Render SHA-256",
    "Generator",
    "Validation Evidence",
    "Status",
)
RECOGNIZABLE_PATHS = (
    "08-review/evidence-graph.md",
    "evidence-graph.md",
    "onboarding-spec.md",
    "onboarding-tasks.md",
    "coverage-matrix.md",
    "batch-review.md",
    "flow.md",
    "03-flows",
)


@dataclass(frozen=True, order=True)
class CoverageFinding:
    scope: str
    category: str
    detail: str

    def line(self) -> str:
        return f"FINDING: {self.scope} | {self.category} | {self.detail}"


@dataclass(frozen=True)
class CoverageReport:
    applicable: bool
    planned: int
    deferred: int
    findings: tuple[CoverageFinding, ...]


class CoverageBlocked(Exception):
    pass


class CoreFlowCoverage:
    def __init__(self, root: Path) -> None:
        self.requested_root = root
        self.root = root
        self.findings: set[CoverageFinding] = set()
        self.durable_diagram_ids: set[str] = set()

    def validate(self) -> CoverageReport:
        self._validate_root()
        if not self._is_applicable():
            return CoverageReport(False, 0, 0, ())

        evidence = self._read_required(
            "onboarding", "08-review/evidence-graph.md", "evidence-graph.md"
        )
        spec = self._read_required("onboarding", "onboarding-spec.md")
        tasks = self._read_required("onboarding", "onboarding-tasks.md")
        coverage = self._read_required("onboarding", "coverage-matrix.md")
        review = self._read_required("onboarding", "batch-review.md")
        core_flow_rows = []
        if evidence is not None:
            core_flow_rows = [
                line
                for line in evidence.splitlines()
                if line.startswith("|")
                and FLOW_ID.search(line)
                and re.search(r"\|\s*(critical|important)\s*\|", line)
            ]
            if not core_flow_rows:
                self._finding(
                    "onboarding", "flow-inventory", "no critical/important core flow rows found"
                )

        if any(re.search(r"\|\s*planned\s*\|", row) for row in core_flow_rows):
            self.durable_diagram_ids = self._validate_visual_manifests()

        planned_count = 0
        deferred_count = 0
        for row in core_flow_rows:
            flow_match = FLOW_ID.search(row)
            if flow_match is None:
                continue
            flow_id = flow_match.group(0)
            for content, artifact in (
                (spec, "onboarding-spec.md"),
                (tasks, "onboarding-tasks.md"),
                (coverage, "coverage-matrix.md"),
                (review, "batch-review.md"),
            ):
                self._require_token(content, flow_id, artifact, flow_id)

            if re.search(r"\|\s*deferred\s*\|", row):
                self._validate_deferred(row, flow_id)
                deferred_count += 1
            elif re.search(r"\|\s*planned\s*\|", row):
                planned_count += 1
                self._validate_planned(flow_id, spec, tasks, coverage, review)
            else:
                self._finding(
                    flow_id,
                    "selection",
                    f"core flow selection must be planned or deferred: {flow_id}",
                )

        return CoverageReport(
            True,
            planned_count,
            deferred_count,
            tuple(sorted(self.findings)),
        )

    def _validate_root(self) -> None:
        if self.requested_root.is_symlink():
            raise CoverageBlocked("onboarding root must not be a symlink")
        if not self.requested_root.exists() or not self.requested_root.is_dir():
            raise CoverageBlocked(f"onboarding root not found: {self.requested_root}")
        try:
            tuple(self.requested_root.iterdir())
            self.root = self.requested_root.resolve(strict=True)
        except OSError as error:
            raise CoverageBlocked("onboarding root is unreadable") from error

    def _is_applicable(self) -> bool:
        return any(
            (self.root / relative).exists() or (self.root / relative).is_symlink()
            for relative in RECOGNIZABLE_PATHS
        )

    def _finding(self, scope: str, category: str, detail: str) -> None:
        self.findings.add(CoverageFinding(scope, category, detail))

    def _safe_read(self, path: Path, label: str) -> str:
        if path.is_symlink():
            raise CoverageBlocked(f"unsafe local path is a symlink: {label}")
        if not path.is_file():
            raise CoverageBlocked(f"declared local artifact is not a readable file: {label}")
        try:
            return read_text(path)
        except (OSError, UnicodeError) as error:
            raise CoverageBlocked(f"declared local artifact is unreadable: {label}") from error

    def _read_required(self, scope: str, *candidates: str) -> str | None:
        for candidate in candidates:
            path = self.root / candidate
            if path.exists() or path.is_symlink():
                return self._safe_read(path, candidate)
        self._finding(scope, "artifact", f"missing artifact: {candidates[0]}")
        return None

    def _flow_docs(self) -> list[tuple[Path, str]]:
        flow_root = self.root / "03-flows"
        paths: list[Path] = []
        if flow_root.exists() or flow_root.is_symlink():
            if flow_root.is_symlink() or not flow_root.is_dir():
                raise CoverageBlocked("unsafe local path for 03-flows")
            try:
                entries = sorted(flow_root.iterdir(), key=lambda item: item.name)
            except OSError as error:
                raise CoverageBlocked("03-flows cannot be enumerated") from error
            for entry in entries:
                if entry.is_symlink():
                    raise CoverageBlocked(f"unsafe local path is a symlink: 03-flows/{entry.name}")
                if entry.is_file() and entry.suffix.lower() == ".md":
                    paths.append(entry)
        fallback = self.root / "flow.md"
        if not paths and (fallback.exists() or fallback.is_symlink()):
            paths = [fallback]
        if not paths:
            self._finding("onboarding", "artifact", "missing artifact: 03-flows/*.md")
            return []
        return [
            (path, self._safe_read(path, path.relative_to(self.root).as_posix()))
            for path in paths
        ]

    def _validate_deferred(self, row: str, flow_id: str) -> None:
        for field in ("impact", "missing", "next"):
            if not re.search(rf"\b{field}\s*=", row, re.IGNORECASE):
                self._finding(
                    flow_id,
                    "deferred",
                    f"deferred flow missing {field}: {flow_id}",
                )

    def _validate_planned(
        self,
        flow_id: str,
        spec: str | None,
        tasks: str | None,
        coverage: str | None,
        review: str | None,
    ) -> None:
        slice_pattern = re.compile(SLICE_ID_TEMPLATE.format(flow=re.escape(flow_id)))
        required_slices = sorted(set(slice_pattern.findall(spec or "")))
        if not required_slices:
            self._finding(flow_id, "slice", f"no required slices declared: {flow_id}")
        for slice_id in required_slices:
            self._require_token(tasks, slice_id, "onboarding-tasks.md", flow_id)

        flow_docs = self._flow_docs()
        flow_texts = [text for _, text in flow_docs if flow_id in text]
        flow_text = "\n".join(flow_texts)
        if not flow_text:
            self._finding(flow_id, "artifact", f"missing flow document: {flow_id}")
            return
        if re.search(r"<\.\.\.|TBD|TODO|待补充|看代码|see code", flow_text, re.IGNORECASE):
            self._finding(
                flow_id,
                "placeholder",
                f"unresolved placeholder in flow document: {flow_id}",
            )

        slice_rows: list[tuple[str, str]] = []
        flow_lines = flow_text.splitlines()
        for slice_id in required_slices:
            row = next(
                (line for line in flow_lines if line.startswith("|") and slice_id in line),
                None,
            )
            if row is None:
                self._finding(flow_id, "slice", f"missing required slice: {slice_id}")
                continue
            if not re.search(r"\|\s*covered\s*\|", row):
                self._finding(flow_id, "declared-status", f"slice is not covered: {slice_id}")
            if not DIAGRAM_ID.search(row):
                self._finding(flow_id, "diagram-id", f"slice missing Diagram ID: {slice_id}")
            if not re.search(r"§\d+", row):
                self._finding(flow_id, "section-locator", f"slice missing document section: {slice_id}")
            if not re.search(r"`[^`]+#[^`]+`", row):
                self._finding(
                    flow_id,
                    "evidence-reference",
                    f"slice missing symbol/config evidence: {slice_id}",
                )
            slice_rows.append((slice_id, row))

        required_diagrams = set(DIAGRAM_ID.findall(spec or "")) | set(
            DIAGRAM_ID.findall(tasks or "")
        )
        for _, row in slice_rows:
            required_diagrams.update(DIAGRAM_ID.findall(row))
        for diagram_id in sorted(required_diagrams):
            defined = diagram_id in self.durable_diagram_ids or any(
                diagram_id in line
                and not line.startswith("|")
                and (line.startswith("#") or re.search(r"Diagram ID", line, re.IGNORECASE))
                for line in flow_lines
            )
            if not defined:
                self._finding(
                    flow_id,
                    "diagram-id",
                    f"missing diagram definition: {diagram_id}",
                )

        for slice_id, row in slice_rows:
            for section_number in re.findall(r"§(\d+)", row):
                heading = re.compile(
                    rf"^#{{2,6}}\s+{re.escape(section_number)}(?:\.|\s)",
                    re.MULTILINE,
                )
                if not heading.search(flow_text):
                    self._finding(
                        flow_id,
                        "section-locator",
                        f"missing document section: {slice_id} -> §{section_number}",
                    )

        self._record_gate_facts(coverage, flow_id, "coverage-matrix.md")
        self._record_gate_facts(review, flow_id, "batch-review.md")

    def _validate_visual_manifests(self) -> set[str]:
        seen: set[str] = set()
        source_to_render: dict[Path, Path] = {}
        render_to_source: dict[Path, Path] = {}
        for path, content in self._flow_docs():
            relative = path.relative_to(self.root).as_posix()
            manifest = optional_section(content, "Diagram Artifact Manifest")
            representation = "Representation: archify-source-render" in content
            if not representation and manifest is None:
                continue
            if not representation:
                self._finding(
                    relative,
                    "visual-manifest",
                    "Diagram Artifact Manifest requires Representation: archify-source-render",
                )
                continue
            if manifest is None:
                self._finding(
                    relative,
                    "visual-manifest",
                    "archify-source-render requires Diagram Artifact Manifest",
                )
                continue
            if "Visual Manifest Contract: source-render-v1" not in manifest:
                self._finding(
                    relative,
                    "visual-manifest",
                    "Diagram Artifact Manifest must declare source-render-v1",
                )
            try:
                rows = table(content, "Diagram Artifact Manifest")
            except CheckFailure as error:
                self._finding(relative, "visual-manifest", str(error))
                continue
            for row in rows:
                if tuple(row.keys()) != ONBOARDING_VISUAL_COLUMNS:
                    self._finding(relative, "visual-manifest", "Onboarding source-render-v1 columns mismatch")
                    continue
                diagram_id = normalized(row.get("Diagram ID"))
                scope = diagram_id if diagram_id else relative
                if DIAGRAM_ID.fullmatch(diagram_id) is None:
                    self._finding(scope, "diagram-id", "Diagram ID must match D-[A-Z0-9-]+")
                    continue
                if diagram_id in seen:
                    raise CoverageBlocked(
                        f"mechanically ambiguous source/render authority: duplicate Diagram ID {diagram_id}"
                    )
                seen.add(diagram_id)
                evidence = row.get("Evidence References", "")
                if not re.search(r"`[^`]+#[^`]+`", evidence):
                    self._finding(scope, "evidence-reference", f"Onboarding visual {diagram_id} needs symbol/config evidence")
                if normalized(row.get("Status")) != "current":
                    self._finding(scope, "declared-status", f"Onboarding visual {diagram_id} status is not current")

                source_raw = normalized(row.get("Source Definition"))
                render_raw = normalized(row.get("Render"))
                self._validate_visual_path_authority(source_raw, "source definition")
                self._validate_visual_path_authority(render_raw, "render")
                if source_raw and render_raw:
                    source_path = (self.root / Path(source_raw.replace("\\", "/"))).resolve()
                    render_path = (self.root / Path(render_raw.replace("\\", "/"))).resolve()
                    if source_path == render_path:
                        raise CoverageBlocked("source definition and render must differ")
                    if source_path in source_to_render and source_to_render[source_path] != render_path:
                        raise CoverageBlocked("mechanically ambiguous source/render authority for source definition")
                    if render_path in render_to_source and render_to_source[render_path] != source_path:
                        raise CoverageBlocked("mechanically ambiguous source/render authority for render")
                    source_to_render[source_path] = render_path
                    render_to_source[render_path] = source_path
                try:
                    validate_durable_visual(
                        self.root,
                        diagram_id=diagram_id,
                        source_definition=source_raw,
                        render=render_raw,
                        diagram_type=row.get("Type", ""),
                        source_sha256=row.get("Source SHA-256", ""),
                        render_sha256=row.get("Render SHA-256", ""),
                        generator=row.get("Generator", ""),
                        validation_evidence=row.get("Validation Evidence", ""),
                    )
                except VisualArtifactError as error:
                    detail = str(error)
                    if self._visual_error_is_hard(detail):
                        raise CoverageBlocked(detail) from error
                    category = "digest" if "SHA-256" in detail else "source-render"
                    self._finding(scope, category, detail)
        return seen

    def _validate_visual_path_authority(self, raw: str, label: str) -> None:
        value = raw.replace("\\", "/")
        candidate = Path(value)
        if not value:
            return
        if candidate.is_absolute() or re.match(r"^[A-Za-z]:/", value) or ".." in candidate.parts:
            raise CoverageBlocked(f"{label} escapes owning root")
        current = self.root
        for part in candidate.parts:
            current = current / part
            if current.is_symlink():
                raise CoverageBlocked(f"unsafe local path is a symlink: {value}")

    @staticmethod
    def _visual_error_is_hard(detail: str) -> bool:
        return any(
            token in detail
            for token in (
                "escapes owning root",
                "must be relative",
                "source definition and render must differ",
            )
        )

    def _require_token(
        self, text: str | None, token: str, artifact: str, scope: str
    ) -> None:
        if text is not None and token not in text:
            self._finding(scope, "reference", f"missing {token} in {artifact}")

    def _record_gate_facts(
        self, text: str | None, flow_id: str, artifact: str
    ) -> None:
        if text is None:
            return
        gate_index = text.find("Completeness Hard Gate")
        if gate_index < 0:
            self._finding(flow_id, "declared-gate", f"missing Completeness Hard Gate in {artifact}")
            return
        score_index = text.find("## Score")
        if score_index >= 0 and gate_index > score_index:
            self._finding(
                flow_id,
                "declared-gate",
                f"Completeness Hard Gate must precede score in {artifact}",
            )
        row = next(
            (
                line
                for line in text.splitlines()
                if line.startswith("|") and flow_id in line
            ),
            None,
        )
        if row is None:
            self._finding(flow_id, "declared-gate", f"missing gate row in {artifact}")
        elif not re.search(r"\|\s*PASS\s*\|", row):
            self._finding(
                flow_id,
                "declared-gate",
                f"recorded Completeness Hard Gate is not PASS for {flow_id} in {artifact}",
            )


def main() -> int:
    require_supported_python()
    parser = argparse.ArgumentParser(
        description="Report onboarding core-flow coverage facts."
    )
    parser.add_argument("onboarding_root", type=Path)
    args = parser.parse_args()
    try:
        report = CoreFlowCoverage(args.onboarding_root).validate()
    except CoverageBlocked as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    if not report.applicable:
        print("NOT_APPLICABLE: no recognizable Evidence-Graph + DDD Onboarding scope")
        return 0
    counts = f"{report.planned} planned, {report.deferred} deferred"
    if report.findings:
        print(
            f"CHANGED: core-flow coverage has {len(report.findings)} objective finding(s) "
            f"({counts})"
        )
        for finding in report.findings:
            print(finding.line())
        return 0
    print(f"CURRENT: core-flow coverage objective facts are current ({counts})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
