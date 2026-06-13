# Active Project Log

Newest first. Keep entries compact and evidence-linked. Long reports belong in
`sources/reports/`.

## 2026-06-06T16:36-07:00

Status: implemented / hardening

Summary: Curated pending implementation handoff
`handoff_20260606_233526_a2b28ab`. The project-root OpenCode template now
configures the default `build` agent as a host implementer with compact
`/contextualize` refresh and agent-wiki host-agent memory rules by default.
Future work should exercise the copied template in a real host project and keep
additional host agents covered with the injector/checker workflow.

Evidence:

- `knowledge/change_inbox.jsonl`
- `templates/project-root/opencode.json`
- `.opencode/instructions.md`
- `templates/project-root/README.md`
- `docs/opencode-workflow.md`
- `README.md`

## 2026-06-06T14:04-07:00

Status: implemented / hardening

Summary: Curated pending implementation handoff
`handoff_20260606_205931_716368a`. The project now has Git-aware handoff
records, handoff-created events, safe watcher notifications, an append-only
handoff queue helper, expanded handoff templates, and semantic lint warnings.
Strict semantic errors, preferred trailer policy, tmux injection, performance
metrics, and curator-auditor remain unresolved.

Evidence:

- `knowledge/change_inbox.jsonl`
- `scripts/wiki/scan_changes.py`
- `scripts/wiki/watch_handoffs.py`
- `scripts/wiki/handoff_queue.py`
- `scripts/wiki/lint.py`
- `templates/handoff.json`

## 2026-06-06

Status: active planning

Summary: Consolidated the source plan for Git-backed handoffs, curator wakeups,
and semantic reliability gates into current wiki state, routes, topic hubs,
open questions, and registries. Implementation remains planned until code and
verification evidence exist.

Evidence:

- `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md`
- `wiki/CURRENT_STATE.md`
- `wiki/plans/active_plan.md`
