#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from checker_support import configure_utf8_stdio, require_supported_python
from lightweight_change_support import (
    LightweightChangeContractError,
    build_scan,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan persistent Lightweight Change cards without mutation"
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--as-of", required=True)
    return parser


def main() -> int:
    configure_utf8_stdio()
    require_supported_python()
    arguments = build_parser().parse_args()
    try:
        as_of = date.fromisoformat(arguments.as_of)
    except ValueError:
        print("usage: --as-of must be YYYY-MM-DD", file=sys.stderr)
        return 2
    try:
        scan = build_scan(Path(arguments.project_root), as_of=as_of)
    except LightweightChangeContractError as error:
        if error.exit_code == 2:
            print(f"usage error: {error.detail}", file=sys.stderr)
        else:
            print(
                json.dumps(
                    error.to_payload(), ensure_ascii=False, sort_keys=True, indent=2
                )
            )
        return error.exit_code
    print(json.dumps(scan.to_payload(), ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
