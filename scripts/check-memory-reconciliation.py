#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from checker_support import require_supported_python
from memory_reconciliation_support import (
    MemoryReconciliationError,
    validate_post_apply,
    validate_pre_apply,
    validate_restore_state,
)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Validate an exact Agent Loop memory reconciliation plan without writes"
    )
    value.add_argument("--project-root", required=True)
    value.add_argument("--report", required=True)
    value.add_argument(
        "--phase", required=True, choices=("pre-apply", "post-apply", "restore")
    )
    value.add_argument("--expected-plan-sha256", required=True)
    return value


def main() -> int:
    require_supported_python()
    arguments = parser().parse_args()
    project_root = Path(arguments.project_root).resolve()
    report = Path(arguments.report)
    report = (report if report.is_absolute() else project_root / report).resolve()
    validators = {
        "pre-apply": validate_pre_apply,
        "post-apply": validate_post_apply,
        "restore": validate_restore_state,
    }
    try:
        result = validators[arguments.phase](
            project_root, report, arguments.expected_plan_sha256
        )
    except (MemoryReconciliationError, OSError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "PASS: "
        f"report={report.parent.name} phase={arguments.phase} "
        f"plan_sha256={arguments.expected_plan_sha256} "
        f"paths={len(result.ledger)} operations={len(result.operations)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
