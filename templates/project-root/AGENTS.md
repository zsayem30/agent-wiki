# Project Agent Rules

This project uses `agent-wiki/` as a curator-owned project memory subsystem.

## Startup

For OpenCode, use the root `opencode.json` copied from
`agent-wiki/templates/project-root/opencode.json`.

For any agent harness:

1. Read this file.
2. Read `agent-wiki/AGENTS.md`.
3. Read `agent-wiki/wiki/START_HERE.md`.
4. Read `agent-wiki/wiki/CURRENT_STATE.md`.
5. Read `agent-wiki/wiki/ROUTING_TABLE.md`.

## Role Boundary

Project agents own implementation, research, reports, tests, and experiments.
The `wiki-curator` owns compact durable memory under `agent-wiki/`.

Do not dump long plans, reports, or experiment analyses directly into
`agent-wiki/wiki/`. Preserve long material under `agent-wiki/sources/` or
project `results/`, then let the curator distill it.

## Handoff

After durable work, run from the project root:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root . --truth-impact unknown --evidence <path-or-note>
```

Use `--truth-impact yes`, `no`, or `unknown` explicitly. Add repeated
`--evidence`, `--verification`, `--suggested-route`, and `--open-question`
arguments when useful.

Then ask the `wiki-curator` to update compact truth only if evidence supports
it.
