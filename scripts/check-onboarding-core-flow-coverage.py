#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from checker_support import read_text, require_supported_python


FLOW_ID = re.compile(r"CF-[A-Z0-9-]+")
SLICE_ID_TEMPLATE = r"{flow}/S\d{{2}}"
DIAGRAM_ID = re.compile(r"D-[A-Z0-9-]+")


class CoverageError(Exception):
    pass


class CoreFlowCoverage:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def validate(self) -> tuple[int, int]:
        if not self.root.is_dir():
            raise CoverageError(f"onboarding root not found: {self.root}")

        evidence = self.read_required("08-review/evidence-graph.md", "evidence-graph.md")
        spec = self.read_required("onboarding-spec.md")
        tasks = self.read_required("onboarding-tasks.md")
        coverage = self.read_required("coverage-matrix.md")
        review = self.read_required("batch-review.md")
        core_flow_rows = [
            line
            for line in evidence.splitlines()
            if line.startswith("|")
            and FLOW_ID.search(line)
            and re.search(r"\|\s*(critical|important)\s*\|", line)
        ]
        if not core_flow_rows:
            raise CoverageError("no critical/important core flow rows found")

        planned_count = 0
        deferred_count = 0
        for row in core_flow_rows:
            flow_match = FLOW_ID.search(row)
            if not flow_match:
                continue
            flow_id = flow_match.group(0)
            self.require_token(spec, flow_id, "onboarding-spec.md")
            self.require_token(tasks, flow_id, "onboarding-tasks.md")
            self.require_token(coverage, flow_id, "coverage-matrix.md")
            self.require_token(review, flow_id, "batch-review.md")

            if re.search(r"\|\s*deferred\s*\|", row):
                self.validate_deferred(row, flow_id)
                deferred_count += 1
                continue
            if not re.search(r"\|\s*planned\s*\|", row):
                raise CoverageError(
                    f"core flow selection must be planned or deferred: {flow_id}"
                )
            planned_count += 1
            self.validate_planned(flow_id, spec, tasks, coverage, review)
        return planned_count, deferred_count

    @staticmethod
    def validate_deferred(row: str, flow_id: str) -> None:
        for field in ("impact", "missing", "next"):
            if not re.search(rf"\b{field}\s*=", row, re.IGNORECASE):
                raise CoverageError(f"deferred flow missing {field}: {flow_id}")

    def validate_planned(
        self, flow_id: str, spec: str, tasks: str, coverage: str, review: str
    ) -> None:
        slice_pattern = re.compile(SLICE_ID_TEMPLATE.format(flow=re.escape(flow_id)))
        required_slices = sorted(set(slice_pattern.findall(spec)))
        if not required_slices:
            raise CoverageError(f"no required slices declared: {flow_id}")
        for slice_id in required_slices:
            self.require_token(tasks, slice_id, "onboarding-tasks.md")

        flow_text = "\n".join(text for text in self.read_flow_docs() if flow_id in text)
        if not flow_text:
            raise CoverageError(f"missing flow document: {flow_id}")
        if re.search(r"<\.\.\.|TBD|TODO|待补充|看代码|see code", flow_text, re.IGNORECASE):
            raise CoverageError(f"unresolved placeholder in flow document: {flow_id}")

        slice_rows: list[tuple[str, str]] = []
        flow_lines = flow_text.splitlines()
        for slice_id in required_slices:
            row = next(
                (line for line in flow_lines if line.startswith("|") and slice_id in line),
                None,
            )
            if row is None:
                raise CoverageError(f"missing required slice: {slice_id}")
            if not re.search(r"\|\s*covered\s*\|", row):
                raise CoverageError(f"slice is not covered: {slice_id}")
            if not DIAGRAM_ID.search(row):
                raise CoverageError(f"slice missing Diagram ID: {slice_id}")
            if not re.search(r"§\d+", row):
                raise CoverageError(f"slice missing document section: {slice_id}")
            slice_rows.append((slice_id, row))

        required_diagrams = set(DIAGRAM_ID.findall(spec)) | set(DIAGRAM_ID.findall(tasks))
        for _, row in slice_rows:
            required_diagrams.update(DIAGRAM_ID.findall(row))
        for diagram_id in sorted(required_diagrams):
            defined = any(
                diagram_id in line
                and not line.startswith("|")
                and (line.startswith("#") or re.search(r"Diagram ID", line, re.IGNORECASE))
                for line in flow_lines
            )
            if not defined:
                raise CoverageError(f"missing diagram definition: {diagram_id}")

        for slice_id, row in slice_rows:
            for section_number in re.findall(r"§(\d+)", row):
                heading = re.compile(
                    rf"^#{{2,6}}\s+{re.escape(section_number)}(?:\.|\s)",
                    re.MULTILINE,
                )
                if not heading.search(flow_text):
                    raise CoverageError(
                        f"missing document section: {slice_id} -> §{section_number}"
                    )
            if not re.search(r"`[^`]+#[^`]+`", row):
                raise CoverageError(f"slice missing symbol/config evidence: {slice_id}")

        if not re.search(
            r"Call / Data Direction|\|\s*Direction\s*\|", flow_text, re.IGNORECASE
        ):
            raise CoverageError(f"flow missing call/data direction evidence: {flow_id}")

        self.require_hard_gate_before_score(coverage, "coverage-matrix.md")
        self.require_hard_gate_before_score(review, "batch-review.md")
        self.require_hard_gate_pass(coverage, flow_id, "coverage-matrix.md")
        self.require_hard_gate_pass(review, flow_id, "batch-review.md")

    def read_required(self, *candidates: str) -> str:
        for candidate in candidates:
            path = self.root / candidate
            if path.is_file():
                return read_text(path)
        raise CoverageError(f"missing artifact: {candidates[0]}")

    def read_flow_docs(self) -> list[str]:
        paths = sorted((self.root / "03-flows").glob("*.md"))
        fallback = self.root / "flow.md"
        if not paths and fallback.is_file():
            paths = [fallback]
        if not paths:
            raise CoverageError("missing artifact: 03-flows/*.md")
        return [read_text(path) for path in paths]

    @staticmethod
    def require_token(text: str, token: str, artifact: str) -> None:
        if token not in text:
            raise CoverageError(f"missing {token} in {artifact}")

    @staticmethod
    def require_hard_gate_pass(text: str, flow_id: str, artifact: str) -> None:
        if not any(
            line.startswith("|")
            and flow_id in line
            and re.search(r"\|\s*PASS\s*\|", line)
            for line in text.splitlines()
        ):
            raise CoverageError(
                f"Completeness Hard Gate is not PASS for {flow_id} in {artifact}"
            )

    @staticmethod
    def require_hard_gate_before_score(text: str, artifact: str) -> None:
        gate_index = text.find("Completeness Hard Gate")
        if gate_index < 0:
            raise CoverageError(f"missing Completeness Hard Gate in {artifact}")
        score_index = text.find("## Score")
        if score_index >= 0 and gate_index > score_index:
            raise CoverageError(f"Completeness Hard Gate must precede score in {artifact}")


def main() -> int:
    require_supported_python()
    parser = argparse.ArgumentParser(
        description="Validate onboarding critical/important core-flow coverage."
    )
    parser.add_argument("onboarding_root", type=Path)
    args = parser.parse_args()
    try:
        planned, deferred = CoreFlowCoverage(args.onboarding_root).validate()
    except CoverageError as error:
        print(error, file=sys.stderr)
        return 1
    print(
        "PASS: core-flow coverage trace is complete "
        f"({planned} planned, {deferred} deferred)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
