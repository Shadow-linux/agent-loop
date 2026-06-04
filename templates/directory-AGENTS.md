# AGENTS.md — <Directory> Guidance

This directory owns <long-lived responsibility>.

## Boundary

- `<path>/` contains <allowed content>.
- Do not place <forbidden content> here.
- Interact with <other module> through <public interface/protocol>.

## Commands

```bash
<focused verification command>
```

## Agent Loop Notes

- Agents entering this directory should read this file after the root `AGENTS.md`.
- Keep temporary task status in `.agent-loop/features/*`, not in this file.
- Update this file only when this directory's long-term rules change.
- If creating a durable child boundary with distinct rules, propose a child `AGENTS.md` and ask for human confirmation before writing it.
