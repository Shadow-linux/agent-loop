#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from checker_support import require_supported_python
from feature_archive_support import ArchiveContractError, build_archive_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a read-only Feature Monthly Archive plan"
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument(
        "--operation", choices=("archive", "rehydrate"), required=True
    )
    parser.add_argument("--month", action="append", default=[])
    parser.add_argument("--feature-id", action="append", default=[])
    parser.add_argument("--as-of", required=True)
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
        plan = build_archive_plan(
            Path(arguments.project_root),
            operation=arguments.operation,
            selected_months=arguments.month,
            selected_feature_ids=arguments.feature_id,
            as_of=as_of,
        )
    except ArchiveContractError as error:
        print(f"{error.category}: {error.detail}", file=sys.stderr)
        return error.exit_code
    print(
        json.dumps(plan.to_payload(), ensure_ascii=False, sort_keys=True, indent=2)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
