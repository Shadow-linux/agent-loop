#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

python3 -m unittest \
  tests.test_final_review_agent_owned_delegation \
  tests.test_feature_monthly_archive_scan.FeatureMonthlyArchiveScanTests \
  -v

python3 - "$root" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
runtime = (root / "references/runtime.md").read_text(encoding="utf-8")
stage_order = runtime.split("## Stage Order", 1)[1].split("## Stage Entry And Exit", 1)[0]
assert "\nSubagent Execution If Approved\n" not in stage_order
assert "\nReview\n" not in stage_order
assert "[internal] Task Completion Review inside Task Done Gate" in stage_order
assert "[internal] Feature-wide Required Verification and automatic Final Review Subagent" in stage_order

notes = (root / "templates/notes.md").read_text(encoding="utf-8")
assert "## Task Completion Reviews" in notes
assert "## Final Review" in notes
assert "## Feature Close Review" not in notes

support = (root / "scripts/feature_archive_support.py").read_text(encoding="utf-8")
assert '"Final Review"' in support
assert '"Feature Close Review"' in support

print("PASS: final review and Agent-owned delegation contract")
PY
