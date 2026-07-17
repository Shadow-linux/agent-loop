#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from dataclasses import asdict
from pathlib import Path

from checker_support import canonical_json_bytes, require_supported_python, sha256_bytes
from memory_reconciliation_support import (
    MemoryReconciliationError,
    absent_entry,
    extract_plan_payload,
    git_memory_roots,
    inventory_git_tree,
    inventory_worktree,
    resolve_commit,
    resolve_memory_root,
    safe_relative_path,
    snapshot_entry_payload,
    union_inventories,
    validate_merge_context_text,
)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Read-only four-snapshot Agent Loop memory reconciliation scan"
    )
    value.add_argument("--project-root", required=True)
    value.add_argument("--merge-base-sha", required=True)
    value.add_argument("--source-sha", required=True)
    value.add_argument("--target-before-sha", required=True)
    value.add_argument("--merged-code-sha", required=True)
    value.add_argument("--source-branch", required=True)
    value.add_argument("--target-branch", required=True)
    value.add_argument("--target-release-context", required=True)
    value.add_argument("--customer-boundary", required=True)
    value.add_argument("--report")
    return value


def _role_hint(path: str) -> dict[str, str]:
    lower = path.casefold()
    if "/.memory-reconciliation-txn/" in f"/{lower}/":
        return {
            "role": "transaction-temporary",
            "confidence": "high",
            "evidence": "report-local transaction path pattern only; Agent must confirm",
        }
    if lower.endswith(("/index.md", "/archive.md")) or lower in (
        "bugs/index.md",
        "features/archive.md",
        "requirements/index.md",
        "skills/index.md",
    ):
        return {
            "role": "derived-index",
            "confidence": "medium",
            "evidence": "canonical locator/index path pattern; content ownership still requires review",
        }
    if lower.startswith("requirements/") and lower.endswith(
        ("requirement.md", "prototype.png", "feedback.md")
    ):
        return {
            "role": "human-source",
            "confidence": "medium",
            "evidence": "requirement package source filename pattern; provenance must be verified",
        }
    if lower.startswith("decisions/") and lower.endswith(".md"):
        return {
            "role": "accepted-authority",
            "confidence": "low",
            "evidence": "decision path only; accepted status and supersession must be verified",
        }
    if lower.startswith("skills/") and lower not in ("skills", "skills/index.md"):
        return {
            "role": "validated-package",
            "confidence": "low",
            "evidence": "Project Skill path only; current manifest must be verified",
        }
    if lower.endswith("notes.md") or "/evidence/" in f"/{lower}":
        return {
            "role": "append-only-evidence",
            "confidence": "low",
            "evidence": "history/evidence path pattern; Agent must inspect actual section ownership",
        }
    return {
        "role": "unclassified",
        "confidence": "low",
        "evidence": "no safe semantic classification from path alone",
    }


def _inventory_hash(inventory: dict[str, object]) -> str:
    payload = [
        {"path": path, **snapshot_entry_payload(entry)}
        for path, entry in sorted(inventory.items())
    ]
    return sha256_bytes(canonical_json_bytes(payload))


def _current_file_state(memory_root: Path, relative: str) -> tuple[str | None, str]:
    path = safe_relative_path(relative, memory_root)
    if not path.exists() and not path.is_symlink():
        return None, "absent"
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return sha256_bytes(os.readlink(path).encode("utf-8")), "120000"
    if not stat.S_ISREG(mode):
        return None, "directory" if stat.S_ISDIR(mode) else "other"
    return sha256_bytes(path.read_bytes()), "100755" if mode & stat.S_IXUSR else "100644"


def _zero_change(
    memory_root: Path,
    plan: dict[str, object],
    current_inventory: dict[str, object],
) -> bool:
    operations = plan.get("operations", [])
    unchanged = plan.get("expected_unchanged_paths", {})
    ledger = plan.get("ledger", [])
    if (
        not isinstance(operations, list)
        or not isinstance(unchanged, dict)
        or not isinstance(ledger, list)
    ):
        raise MemoryReconciliationError(
            "invalid report plan", "operations, ledger, or unchanged paths"
        )
    for raw in operations:
        if not isinstance(raw, dict):
            raise MemoryReconciliationError("invalid report plan", "operation")
        path = raw.get("path")
        post_mode = raw.get("post_mode")
        expected = raw.get("postimage_sha256")
        if not isinstance(path, str) or not isinstance(post_mode, str):
            raise MemoryReconciliationError("invalid report plan", "operation path/mode")
        current_hash, current_mode = _current_file_state(memory_root, path)
        if post_mode == "absent":
            if current_mode != "absent" or expected is not None:
                return False
        elif current_mode != post_mode or current_hash != expected:
            return False
    for path, expected in unchanged.items():
        if not isinstance(path, str) or not isinstance(expected, str):
            raise MemoryReconciliationError("invalid report plan", "expected unchanged path")
        current_hash, current_mode = _current_file_state(memory_root, path)
        if current_mode in ("absent", "directory", "other") or current_hash != expected:
            return False
    for raw in ledger:
        if not isinstance(raw, dict):
            raise MemoryReconciliationError("invalid report plan", "ledger row")
        if raw.get("operation_id") is not None:
            continue
        path = raw.get("path")
        snapshots = raw.get("snapshots")
        if not isinstance(path, str) or not isinstance(snapshots, dict):
            raise MemoryReconciliationError("invalid report plan", "retained ledger row")
        expected = snapshots.get("result")
        if not isinstance(expected, dict):
            raise MemoryReconciliationError("invalid report plan", "retained result snapshot")
        creates_directory = (
            expected.get("state") == "absent"
            and any(
                isinstance(snapshot, dict)
                and snapshot.get("state") == "present"
                and snapshot.get("kind") == "directory"
                for snapshot in snapshots.values()
            )
            and any(
                isinstance(operation, dict)
                and operation.get("post_mode") != "absent"
                and isinstance(operation.get("path"), str)
                and str(operation["path"]).startswith(f"{path}/")
                for operation in operations
            )
        )
        if creates_directory:
            expected = {
                "state": "present",
                "kind": "directory",
                "git_mode": "040000",
                "git_oid": None,
                "sha256": None,
            }
        actual = snapshot_entry_payload(current_inventory.get(path, absent_entry()))
        if actual != expected:
            return False
    return True


def run(arguments: argparse.Namespace) -> dict[str, object]:
    project_root = Path(arguments.project_root).resolve()
    if not project_root.is_dir():
        raise MemoryReconciliationError("project root", str(project_root))
    validate_merge_context_text(
        {
            "source_branch": arguments.source_branch,
            "target_branch": arguments.target_branch,
            "target_release_context": arguments.target_release_context,
            "customer_boundary": arguments.customer_boundary,
        }
    )

    resolved = {
        "merge_base_sha": resolve_commit(project_root, arguments.merge_base_sha),
        "source_sha": resolve_commit(project_root, arguments.source_sha),
        "target_before_sha": resolve_commit(project_root, arguments.target_before_sha),
        "merged_code_sha": resolve_commit(project_root, arguments.merged_code_sha),
    }
    head = resolve_commit(project_root, "HEAD")
    if head != resolved["merged_code_sha"]:
        raise MemoryReconciliationError(
            "HEAD mismatch", f"HEAD {head} != Merged Code SHA {resolved['merged_code_sha']}"
        )

    memory_root_name = resolve_memory_root(project_root)
    for key in ("merge_base_sha", "source_sha", "target_before_sha", "merged_code_sha"):
        roots = git_memory_roots(project_root, resolved[key])
        if len(roots) != 1 or roots[0] != memory_root_name:
            raise MemoryReconciliationError(
                "memory root migration",
                f"{key} has {roots or ('none',)}; Result uses {memory_root_name}",
            )

    report_path: Path | None = None
    excluded_prefixes: tuple[str, ...] = ()
    plan: dict[str, object] | None = None
    memory_root = project_root / memory_root_name
    if arguments.report:
        report_path = Path(arguments.report)
        report_path = (
            report_path if report_path.is_absolute() else project_root / report_path
        ).resolve()
        try:
            report_relative = report_path.relative_to(memory_root.resolve())
        except ValueError as error:
            raise MemoryReconciliationError("report outside memory root", str(report_path)) from error
        if not report_path.is_file():
            raise MemoryReconciliationError("cannot read report", str(report_path))
        if report_path.name != "README.md":
            raise MemoryReconciliationError("invalid report path", str(report_path))
        excluded_prefixes = (report_relative.parent.as_posix(),)
        plan = extract_plan_payload(report_path.read_text(encoding="utf-8"))

    snapshots = {
        "base": inventory_git_tree(project_root, resolved["merge_base_sha"], memory_root_name),
        "source": inventory_git_tree(project_root, resolved["source_sha"], memory_root_name),
        "target_before": inventory_git_tree(
            project_root, resolved["target_before_sha"], memory_root_name
        ),
        "result": inventory_worktree(memory_root, excluded_prefixes=excluded_prefixes),
    }
    if report_path is not None:
        # The on-demand report may create the shared container after the original scan.
        # Exclude that row only when no pre-existing report descendants remain visible.
        if not any(
            path.startswith("memory-merges/") for path in snapshots["result"]
        ):
            snapshots["result"].pop("memory-merges", None)
    union = union_inventories(snapshots)
    rows: list[dict[str, object]] = []
    for row in union:
        path = str(row["path"])
        rows.append(
            {
                "path": path,
                "snapshots": {
                    key: snapshot_entry_payload(row[key])
                    for key in ("base", "source", "target_before", "result")
                },
                "role_hint": _role_hint(path),
            }
        )

    context = {
        **resolved,
        "source_branch": arguments.source_branch,
        "target_branch": arguments.target_branch,
        "target_release_context": arguments.target_release_context,
        "customer_boundary": arguments.customer_boundary,
        "memory_root": memory_root_name,
    }
    payload: dict[str, object] = {
        "schema_version": 1,
        "context": context,
        "target_spine": {
            "snapshot": "target_before",
            "sha": resolved["target_before_sha"],
            "memory_root": memory_root_name,
            "paths": sorted(snapshots["target_before"]),
        },
        "snapshot_sha256": {
            key: _inventory_hash(value) for key, value in snapshots.items()
        },
        "paths": rows,
        "blockers": [],
    }
    payload["scan_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    if plan is not None:
        payload["zero_change"] = _zero_change(memory_root, plan, snapshots["result"])
    return payload


def main() -> int:
    require_supported_python()
    arguments = parser().parse_args()
    try:
        payload = run(arguments)
    except (MemoryReconciliationError, OSError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
