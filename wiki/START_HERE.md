# Start Here

This is the compact entry point for agents. Read this before opening long
source documents.

## Project Status

This repository is using the `agent-wiki` scaffold. Replace this starter text
with your project-specific summary once the first plan or idea is accepted.

Current project truth lives in:

- `wiki/CURRENT_STATE.md`
- `wiki/topics/project_overview.md`
- `wiki/plans/active_plan.md`
- `knowledge/project_graph.yaml`

## Read Order

Every agent should start with:

1. `AGENTS.md`
2. `wiki/START_HERE.md`
3. `wiki/CURRENT_STATE.md`
4. `wiki/ROUTING_TABLE.md`
5. `.agents/<role>.md`

Then open only the routed source files needed for the task.

## Core Surfaces

| Surface | Path | Purpose |
|---|---|---|
| Current truth | `wiki/CURRENT_STATE.md` | What is true and active now. |
| Task routing | `wiki/ROUTING_TABLE.md` | Smallest useful context per task. |
| Topic hubs | `wiki/topics/` | Compact summaries by area. |
| Plans | `wiki/plans/` | Active and deferred plans. |
| Decisions | `wiki/decisions/` | ADRs with reopen gates. |
| Open questions | `wiki/OPEN_QUESTIONS.md` | Known uncertainty. |
| Sources | `sources/` | Long or raw user/agent material. |
| Registries | `knowledge/` | Structured machine-readable state. |

## Default Roles

- `wiki-curator`: maintains compact project memory.
- `implementer`: implements, debugs, tests, reviews.
- `deep-research`: finds and summarizes credible papers.
- `reporter`: creates dated evidence-linked project reports.

## First Project Setup

If the user provides a starting idea, implementation plan, or papers:

1. Put them in `sources/inbox/`, `sources/ideas/`, `sources/plans/`, or
   `sources/papers/`.
2. Register them with `scripts/wiki/ingest_source.py`.
3. Ask the curator to distill them into topic hubs, active plan, open
   questions, and registries.

## Human Guide

Read `README.md` for the scaffold overview and `USER_PROMPT_GUIDE.md` for
recommended prompting patterns.

