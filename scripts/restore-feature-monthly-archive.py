#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from checker_support import require_supported_python
from feature_archive_support import ArchiveContractError, restore_transaction


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Restore one Feature Monthly Archive transaction"
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--transaction-id", required=True)
    return parser


def main() -> int:
    require_supported_python()
    arguments = build_parser().parse_args()
    try:
        restore_transaction(Path(arguments.project_root), arguments.transaction_id)
    except ArchiveContractError as error:
        print(f"{error.category}: {error.detail}", file=sys.stderr)
        return error.exit_code
    print(
        f"PASS: Feature Monthly Archive transaction restored; "
        f"transaction_id={arguments.transaction_id}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
