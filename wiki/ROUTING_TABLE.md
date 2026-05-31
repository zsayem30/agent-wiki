# Routing Table

Use this table to choose the smallest useful context. Do not bulk-read
`sources/` or `results/`.

| Task | Read First | Then Read If Needed |
|---|---|---|
| Understand current project state | `wiki/CURRENT_STATE.md` | `wiki/topics/project_overview.md`, `knowledge/project_graph.yaml` |
| Understand the code layout | `wiki/PROJECT_MAP.md` | relevant source files, `knowledge/project_graph.yaml` |
| Work on implementation | `.agents/implementer.md`, `wiki/plans/active_plan.md` | routed topic hub, implementation plan in `sources/plans/` |
| Debug a failure | `.agents/implementer.md`, relevant topic hub | source report, failing logs, code path, run card |
| Review code | `.agents/implementer.md`, `wiki/PROJECT_MAP.md` | changed files, relevant topic hub |
| Research papers | `.agents/deep-research.md`, `wiki/topics/literature.md` | `sources/ideas/`, `knowledge/paper_registry.yaml` |
| Ingest a starting idea | `sources/ideas/` or `sources/inbox/` | `wiki/topics/project_overview.md`, `wiki/OPEN_QUESTIONS.md` |
| Ingest an implementation plan | `sources/plans/` or `sources/inbox/` | `wiki/plans/active_plan.md`, decisions if needed |
| Interpret experiment results | `knowledge/experiment_registry.yaml` | `results/`, source reports, claim registry |
| Update current truth | `.agents/wiki-curator.md`, `wiki/CURRENT_STATE.md` | relevant topic hub, evidence sources |
| Create a project report | `.agents/reporter.md`, `wiki/CURRENT_STATE.md` | topic hubs, registries, decisions, source reports |
| Close a branch | relevant topic hub, active log | decision record, claim/run registries |
| Add a decision | `templates/decision.md` | related source reports, open questions |
| Check wiki health | `.agents/wiki-curator.md` | `python scripts/wiki/lint.py` output |

If a task does not match a row, read `wiki/CURRENT_STATE.md` and the closest
topic hub, then add a route after the task is understood.

