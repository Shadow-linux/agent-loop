from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

INTENT_FAMILIES = (
    "Chat, Requirements Discussion, already-defined ordinary non-Bug change, "
    "explicit Bug/follow-up, Feature Request, Operational Support, Project Skill, "
    "Archive/Rehydrate, Memory Reconciliation, proposal/deferred, and lifecycle requests"
)

DUAL_ROOT_RULE = (
    "If both `.agent-loop/` and legacy `agent-loop/` exist, fail closed and route to Recovery."
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


class ProjectGuidanceConsistencyTests(unittest.TestCase):
    def test_root_should_contain_matches_stale_intent_contract(self) -> None:
        guidance = read("references/project-guidance.md")
        stale_contract = between(
            guidance,
            "`AGENTS.md` is stale when any of these are missing or contradicted:",
            "`CLAUDE.md` is stale when",
        )
        should_contain = between(
            guidance,
            "## Root `AGENTS.md` Should Contain",
            "## Root `AGENTS.md` Should Not Contain",
        )

        self.assertIn(INTENT_FAMILIES, stale_contract)
        self.assertIn(INTENT_FAMILIES, should_contain)
        for delegated_detail in (
            "Brainstorm / Clarify",
            "Concept Foundation Gate",
            "suggest requirement `Delivery Phases`",
            "do not edit `requirement.md`",
        ):
            self.assertNotIn(delegated_detail, should_contain)

    def test_dual_memory_roots_fail_closed_in_controller_sources(self) -> None:
        for path in (
            "SKILL.md",
            "references/runtime.md",
            "references/design.md",
            "references/project-guidance.md",
        ):
            with self.subTest(path=path):
                self.assertIn(DUAL_ROOT_RULE, read(path))


if __name__ == "__main__":
    unittest.main()
