#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from checker_support import require_supported_python
from feature_archive_support import (
    ArchiveContractError,
    archive_plan_from_payload,
    validate_archive_plan_state,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check a Feature Monthly Archive plan or result"
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument(
        "--operation", required=True, choices=("archive", "rehydrate", "restore")
    )
    parser.add_argument("--plan", required=True)
    return parser


def main() -> int:
    require_supported_python()
    arguments = build_parser().parse_args()
    try:
        plan_path = Path(arguments.plan)
        if not plan_path.is_file():
            raise ArchiveContractError("usage", f"missing plan: {plan_path}", 2)
        payload = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        if not isinstance(payload, dict):
            raise ArchiveContractError("usage", "plan JSON must be an object", 2)
        plan = archive_plan_from_payload(payload)
        phase = validate_archive_plan_state(
            Path(arguments.project_root), plan, arguments.operation
        )
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        print(f"usage: invalid plan JSON: {error}", file=sys.stderr)
        return 2
    except ArchiveContractError as error:
        print(f"{error.category}: {error.detail}", file=sys.stderr)
        return error.exit_code
    print(
        f"PASS: Feature Monthly Archive {arguments.operation} {phase}; "
        f"plan_sha256={plan.computed_sha256()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
