#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from checker_support import require_supported_python
from feature_archive_support import (
    ArchiveContractError,
    apply_archive_plan,
    build_archive_plan,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Apply a reviewed Feature Monthly Archive plan"
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument(
        "--operation", required=True, choices=("archive", "rehydrate")
    )
    parser.add_argument("--month", action="append", default=[])
    parser.add_argument("--feature-id", action="append", default=[])
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--expected-plan-sha256", required=True)
    return parser


def main() -> int:
    require_supported_python()
    arguments = build_parser().parse_args()
    try:
        as_of = date.fromisoformat(arguments.as_of)
    except ValueError:
        print("usage: --as-of must be YYYY-MM-DD", file=sys.stderr)
        return 2
    try:
        project_root = Path(arguments.project_root)
        plan = build_archive_plan(
            project_root,
            operation=arguments.operation,
            selected_months=arguments.month,
            selected_feature_ids=arguments.feature_id,
            as_of=as_of,
        )
        transaction_id = apply_archive_plan(
            project_root,
            plan,
            expected_plan_sha256=arguments.expected_plan_sha256,
        )
    except ArchiveContractError as error:
        print(f"{error.category}: {error.detail}", file=sys.stderr)
        return error.exit_code
    print(
        f"PASS: Feature Monthly Archive {arguments.operation} applied; "
        f"transaction_id={transaction_id}; plan_sha256={plan.computed_sha256()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
