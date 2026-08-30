from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from tests.checker_test_support import ROOT


@dataclass
class ArchiveWorkspace:
    project_root: Path

    @property
    def memory_root(self) -> Path:
        return self.project_root / ".agent-loop"

    @property
    def features_root(self) -> Path:
        return self.memory_root / "features"

    def write(self, relative: str, content: str) -> Path:
        path = self.project_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return path

    def feature(
        self,
        feature_id: str,
        *,
        status: str = "closed",
        close_complete: bool = True,
        legacy_close_review: bool = False,
    ) -> Path:
        root = self.features_root / feature_id
        root.mkdir(parents=True, exist_ok=True)
        self.write(
            f".agent-loop/features/{feature_id}/spec.md",
            f"# Feature Spec\n\nStatus: {status}\n",
        )
        task_status = "done" if close_complete else "in-progress"
        self.write(
            f".agent-loop/features/{feature_id}/tasks.md",
            f"# Tasks\n\n- Status: {task_status}\n",
        )
        review_heading = (
            ""
            if legacy_close_review
            else (
                "## Final Review\n\n- Final Reviewer: controller-fallback\n"
                "- Reviewed Inputs: accepted authority, final diff, verification, rollback\n"
                "- Final Review Findings: no finding\n"
                "- Finding Dispositions: complete\n- Post-Repair Freshness: current\n\n"
            )
        )
        readiness_review = (
            "Feature Close Review: complete\n"
            if legacy_close_review
            else "Final Review: complete\n"
        )
        complete_close = (
            review_heading
            + "## Drift Check\n\nDecision: no-drift\n\n"
            "## Close Record\n\nClosed At: 2026-05-20\nHuman Decision: confirmed\n\n"
            f"## Archive Readiness\n\nClosed At: 2026-05-20\nDelivered Summary: completed {feature_id}\n"
            "Verification: complete\n"
            + readiness_review
            + "Drift: resolved\n"
            "Project Memory Impact: none\nOpen Follow-up: none\n"
        )
        close = complete_close if close_complete else "## Close Record\n\nClosed At:\n"
        self.write(
            f".agent-loop/features/{feature_id}/notes.md",
            f"# Notes\n\nCreated: {feature_id[:10]}\n\n{close}",
        )
        self.write(
            f".agent-loop/features/{feature_id}/tests.md",
            "# Tests\n\nStatus: passing\n",
        )
        self.write(
            f".agent-loop/features/{feature_id}/plan.md",
            "# Plan\n\nStatus: closed\n",
        )
        return root


def run_archive_command(
    script: str, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, **(env or {})},
    )


def tree_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def json_output(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    return json.loads(result.stdout)
