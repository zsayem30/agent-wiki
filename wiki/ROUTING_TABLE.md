# Routing Table

Use this table to choose the smallest useful context. Do not bulk-read
`agent-wiki/sources/` or host-project `results/`.

| Task | Read First | Then Read If Needed |
|---|---|---|
| Understand current project state | `agent-wiki/wiki/CURRENT_STATE.md` | `agent-wiki/wiki/topics/project_overview.md`, `agent-wiki/knowledge/project_graph.yaml` |
| Understand host project layout | `agent-wiki/wiki/PROJECT_MAP.md` | relevant host source files, `agent-wiki/knowledge/project_graph.yaml` |
| Curate a starting idea | `agent-wiki/sources/ideas/` or `agent-wiki/sources/inbox/` | `agent-wiki/wiki/topics/project_overview.md`, `agent-wiki/wiki/OPEN_QUESTIONS.md` |
| Curate an implementation plan | `agent-wiki/sources/plans/` or `agent-wiki/sources/inbox/` | `agent-wiki/wiki/plans/active_plan.md`, decisions if needed |
| Curate paper/literature notes | `agent-wiki/wiki/topics/literature.md` | `agent-wiki/sources/papers/`, `agent-wiki/knowledge/paper_registry.yaml` |
| Curate experiment results | `agent-wiki/knowledge/experiment_registry.yaml` | host `results/`, source reports, claim registry |
| Update current truth | `.agents/wiki-curator.md`, `agent-wiki/wiki/CURRENT_STATE.md` | relevant topic hub, evidence sources |
| Record or review a handoff | `agent-wiki/scripts/wiki/handoff_queue.py` | `agent-wiki/knowledge/change_inbox.jsonl`, `agent-wiki/knowledge/events.jsonl`, changed files, suggested routes |
| Use OpenCode workflow | `agent-wiki/docs/opencode-workflow.md` | `agent-wiki/templates/project-root/opencode.json`, `agent-wiki/.opencode/instructions.md` |
| Use Codex workflow | `agent-wiki/docs/codex-workflow.md` | `agent-wiki/.codex/README.md`, `agent-wiki/USER_PROMPT_GUIDE.md` |
| Close a branch | relevant topic hub, active log | decision record, claim/run registries |
| Add a decision | `agent-wiki/templates/decision.md` | related source reports, open questions |
| Check wiki health | `.agents/wiki-curator.md` | `python agent-wiki/scripts/wiki/lint.py` output |
| Configure host OpenCode | `agent-wiki/templates/project-root/opencode.json` | host `opencode.json`, `agent-wiki/templates/project-root/README.md`, `agent-wiki/docs/opencode-workflow.md`, `.opencode/README.md` |
| Add host-specific agents | host `opencode.json` | `agent-wiki/templates/optional-agents/` examples |

If a task does not match a row, read `agent-wiki/wiki/CURRENT_STATE.md` and
the closest topic hub, then add a route after the task is understood.
