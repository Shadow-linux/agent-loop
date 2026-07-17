#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from checker_support import require_supported_python
from memory_reconciliation_support import (
    MemoryReconciliationError,
    apply_reconciliation,
    finalize_reconciliation,
)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Apply or finalize one exact Human-reviewed memory reconciliation plan"
    )
    value.add_argument("--project-root", required=True)
    value.add_argument("--report", required=True)
    value.add_argument("--mode", required=True, choices=("apply", "finalize"))
    value.add_argument("--expected-plan-sha256", required=True)
    return value


def main() -> int:
    require_supported_python()
    arguments = parser().parse_args()
    project_root = Path(arguments.project_root).resolve()
    report = Path(arguments.report)
    report = (report if report.is_absolute() else project_root / report).resolve()
    try:
        if arguments.mode == "apply":
            transaction_id = apply_reconciliation(
                project_root, report, arguments.expected_plan_sha256
            )
        else:
            transaction_id = finalize_reconciliation(
                project_root, report, arguments.expected_plan_sha256
            )
    except (MemoryReconciliationError, OSError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"PASS: mode={arguments.mode} report={report.parent.name} "
        f"transaction={transaction_id} plan_sha256={arguments.expected_plan_sha256}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
