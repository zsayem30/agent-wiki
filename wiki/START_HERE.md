# Start Here

This is the compact entry point for future agents. Read this before opening
long source documents or host-project results.

## Project Status

This `agent-wiki/` directory is a reusable memory subsystem. It starts in a
clean scaffold state: no host-project claims, active plans, experiments, or
literature have been promoted yet.

Current starter truth lives in:

- `agent-wiki/wiki/CURRENT_STATE.md`
- `agent-wiki/wiki/topics/project_overview.md`
- `agent-wiki/wiki/plans/active_plan.md`
- `agent-wiki/knowledge/project_graph.yaml`

## Harnesses

OpenCode should normally be launched from the host project root. The active
root `opencode.json` can come from
`agent-wiki/templates/project-root/opencode.json` and point to the bundled
`wiki-curator` agent.

Codex should also start from the host project root and use `AGENTS.md` plus the
Python helper scripts directly.

Useful OpenCode commands:

- `/contextualize`
- `/context-curator`
- `/wiki-scan`
- `/wiki-review-next`
- `/wiki-watch`
- `/wiki-lint`
- `/wiki-map`
- `/wiki-rollover`

Useful shell commands:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role implementer --project-root . --max-lines 180
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
python agent-wiki/scripts/wiki/scan_changes.py --project-root . --truth-impact unknown --evidence <path-or-note>
python agent-wiki/scripts/wiki/lint.py
```

## Read Order

A curator should start with:

1. host `AGENTS.md`, if present;
2. `agent-wiki/AGENTS.md`;
3. `agent-wiki/wiki/START_HERE.md`;
4. `agent-wiki/wiki/CURRENT_STATE.md`;
5. `agent-wiki/wiki/ROUTING_TABLE.md`;
6. `agent-wiki/.agents/wiki-curator.md`.

Then open only the routed source files needed for the task.

## Core Surfaces

| Surface | Path | Purpose |
|---|---|---|
| Current truth | `agent-wiki/wiki/CURRENT_STATE.md` | What is true and active now. |
| Task routing | `agent-wiki/wiki/ROUTING_TABLE.md` | Smallest useful context per task. |
| Topic hubs | `agent-wiki/wiki/topics/` | Compact summaries by area. |
| Plans | `agent-wiki/wiki/plans/` | Active and deferred plans. |
| Decisions | `agent-wiki/wiki/decisions/` | ADRs with reopen gates. |
| Open questions | `agent-wiki/wiki/OPEN_QUESTIONS.md` | Known uncertainty. |
| Sources | `agent-wiki/sources/` | Long or raw user/agent material. |
| Registries | `agent-wiki/knowledge/` | Structured machine-readable state. |

## First Project Setup

If the user provides a starting idea, implementation plan, or papers:

1. Put them in `agent-wiki/sources/inbox/`, `agent-wiki/sources/ideas/`,
   `agent-wiki/sources/plans/`, or `agent-wiki/sources/papers/`.
2. Register them with `agent-wiki/scripts/wiki/ingest_source.py`.
3. Ask the curator to distill them into topic hubs, active plan, open
   questions, and registries.

## Human Guide

Read `agent-wiki/README.md` for the scaffold overview and
`agent-wiki/USER_PROMPT_GUIDE.md` for recommended prompting patterns.
