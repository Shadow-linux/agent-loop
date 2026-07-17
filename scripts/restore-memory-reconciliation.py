#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from checker_support import require_supported_python
from memory_reconciliation_support import MemoryReconciliationError, restore_transaction


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Restore one interrupted Agent Loop memory reconciliation transaction"
    )
    value.add_argument("--project-root", required=True)
    value.add_argument("--report", required=True)
    value.add_argument("--transaction-id", required=True)
    return value


def main() -> int:
    require_supported_python()
    arguments = parser().parse_args()
    project_root = Path(arguments.project_root).resolve()
    report = Path(arguments.report)
    report = (report if report.is_absolute() else project_root / report).resolve()
    try:
        restore_transaction(project_root, report, arguments.transaction_id)
    except (MemoryReconciliationError, OSError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"PASS: restored report={report.parent.name} transaction={arguments.transaction_id}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
