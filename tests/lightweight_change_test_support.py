from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from tests.checker_test_support import ROOT


CARD = """# Lightweight Change: {topic}

Record Version: 1
Status: {status}
Created At: {created_at}
Updated At: {updated_at}
Completed At: {completed_at}
Git Context: feature/v1.5.1/example@0123456789abcdef0123456789abcdef01234567

## Background

Bounded internal change with confirmed authority.

## Goal / Completion Criteria

Apply the declared change and pass the declared verification.

## Scope

- `scripts/example.py`

## Lane Rationale

Low risk, enumerable consumers, exact verification, and concrete rollback.

## Impact / Risk

Internal only; no public, data, permission, security, or architecture boundary.

## Plan

- [x] Inspect the exact change point.
- [x] Apply only the disclosed change.
- [x] Run targeted verification and review the diff.

## Current Progress

Implementation and verification complete.

## Verification

`python3 -m py_compile scripts/example.py` exited 0 in this run.

## Rollback

Restore the previous literal in `scripts/example.py` and rerun verification.

## Human Gates

Commit, push, release, and external effects remain separately gated.

## Result / Residuals

Declared internal change completed; no known residual.

## Memory

Memory Review: {memory_review}
Memory Result: {memory_result}
Memory Evidence: {memory_evidence}
Memory Target: {memory_target}
"""


@dataclass
class ChangeWorkspace:
    project_root: Path
    root_name: str = ".agent-loop"

    @property
    def memory_root(self) -> Path:
        return self.project_root / self.root_name

    def change(
        self,
        created_at: str,
        topic: str,
        *,
        status: str = "completed",
        updated_at: str | None = None,
        completed_at: str | None = None,
        memory_review: str = "pending",
        memory_result: str = "pending",
        memory_evidence: str = "verified code and focused test",
        memory_target: str = ".agent-loop/project.md Capabilities",
        month: str | None = None,
        filename: str | None = None,
    ) -> Path:
        updated = updated_at or created_at
        completed = completed_at or (created_at if status == "completed" else "none")
        actual_month = month or created_at[:7]
        name = filename or f"{created_at}-{topic}.md"
        path = self.memory_root / "changes" / actual_month / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            CARD.format(
                topic=topic,
                status=status,
                created_at=created_at,
                updated_at=updated,
                completed_at=completed,
                memory_review=memory_review,
                memory_result=memory_result,
                memory_evidence=memory_evidence,
                memory_target=memory_target,
            ),
            encoding="utf-8",
            newline="\n",
        )
        return path


def run_scan(
    project_root: Path, *, as_of: str = "2026-07-18"
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/scan-lightweight-changes.py"),
            "--project-root",
            str(project_root),
            "--as-of",
            as_of,
        ],
        cwd=str(ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def json_output(result: subprocess.CompletedProcess[str]) -> dict[str, object]:
    return json.loads(result.stdout)


def tree_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }
