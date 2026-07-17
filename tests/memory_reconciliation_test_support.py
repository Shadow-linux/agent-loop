from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class MemoryMergeWorkspace:
    project_root: Path
    merge_base_sha: str
    source_sha: str
    target_before_sha: str
    merged_code_sha: str

    @property
    def memory_root(self) -> Path:
        return self.project_root / ".agent-loop"

    def write(
        self, relative: str, content: str | bytes, *, executable: bool = False
    ) -> Path:
        path = self.project_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        value = content.encode("utf-8") if isinstance(content, str) else content
        path.write_bytes(value)
        path.chmod(0o755 if executable else 0o644)
        return path

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.project_root), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def render_report(self, payload: dict[str, object]) -> Path:
        rendered_payload = dict(payload)
        report_status = str(rendered_payload.pop("_report_status", "待确认"))
        report_id = str(rendered_payload.get("report_id", "MM-not-ready"))
        report = self.memory_root / "memory-merges" / report_id / "README.md"
        report.parent.mkdir(parents=True, exist_ok=True)
        template = (ROOT / "templates/memory-merge-report.md").read_text(encoding="utf-8")
        start = "<!-- memory-reconciliation-plan:start -->"
        end = "<!-- memory-reconciliation-plan:end -->"
        prefix, remainder = template.split(start, 1)
        _, suffix = remainder.split(end, 1)
        block = json.dumps(
            rendered_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        rendered = f"{prefix}{start}\n```json\n{block}\n```\n{end}{suffix}"
        rendered = rendered.replace(
            "Memory Merge ID: MM-<collision-safe-merged-code-short-sha>",
            f"Memory Merge ID: {report_id}",
        )
        rendered = rendered.replace(
            "状态: 待确认 | 已完成 | 已恢复", f"状态: {report_status}"
        )
        report.write_text(rendered, encoding="utf-8")
        return report


def _run(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise AssertionError(f"git {' '.join(arguments)} failed: {result.stderr}")
    return result.stdout.strip()


def create_four_snapshot_workspace(root: Path) -> MemoryMergeWorkspace:
    root.mkdir(parents=True, exist_ok=True)
    _run(root, "init", "-q", "-b", "main")
    _run(root, "config", "user.name", "Agent Loop Test")
    _run(root, "config", "user.email", "agent-loop-test@example.invalid")

    memory = root / ".agent-loop"
    memory.mkdir()
    (memory / "project.md").write_text(
        "# Project\n\nStatus: base\nTarget Release Context: v1.4.0\n",
        encoding="utf-8",
    )
    (memory / "shared").mkdir()
    (memory / "shared/common.md").write_text("common\n", encoding="utf-8")
    (root / "app.txt").write_text("base\n", encoding="utf-8")
    _run(root, "add", ".")
    _run(root, "commit", "-q", "-m", "base")
    merge_base_sha = _run(root, "rev-parse", "HEAD")

    _run(root, "switch", "-q", "-c", "feature/v1.4.0/source-memory")
    (memory / "domain-snapshots").mkdir()
    (memory / "domain-snapshots/FLOW-01.md").write_text(
        "# Source-only future flow\n", encoding="utf-8"
    )
    (memory / "source-only.md").write_text("source only\n", encoding="utf-8")
    (memory / "source.bin").write_bytes(b"\x00\xffsource-binary\x10\n")
    (root / "source.txt").write_text("source code\n", encoding="utf-8")
    _run(root, "add", ".")
    _run(root, "commit", "-q", "-m", "source")
    source_sha = _run(root, "rev-parse", "HEAD")

    _run(root, "switch", "-q", "main")
    (memory / "target-only.md").write_text("target only\n", encoding="utf-8")
    (memory / "target-spine").mkdir()
    (memory / "target-spine/INDEX.md").write_text("# Target spine\n", encoding="utf-8")
    (root / "target.txt").write_text("target code\n", encoding="utf-8")
    _run(root, "add", ".")
    _run(root, "commit", "-q", "-m", "target")
    target_before_sha = _run(root, "rev-parse", "HEAD")

    _run(root, "merge", "-q", "--no-ff", "feature/v1.4.0/source-memory", "-m", "merge")
    merged_code_sha = _run(root, "rev-parse", "HEAD")
    return MemoryMergeWorkspace(
        project_root=root,
        merge_base_sha=merge_base_sha,
        source_sha=source_sha,
        target_before_sha=target_before_sha,
        merged_code_sha=merged_code_sha,
    )


def run_memory_command(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def tree_snapshot(
    root: Path, *, exclude_report_txn: bool = True
) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        if relative == ".git" or relative.startswith(".git/"):
            continue
        if exclude_report_txn and "/.memory-reconciliation-txn/" in f"/{relative}/":
            continue
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            value = f"symlink:{os.readlink(path)}".encode("utf-8")
        elif stat.S_ISDIR(mode):
            value = b"directory"
        elif stat.S_ISREG(mode):
            value = path.read_bytes()
        else:
            value = f"other:{mode}".encode("ascii")
        snapshot[relative] = hashlib.sha256(value).hexdigest()
    return snapshot
