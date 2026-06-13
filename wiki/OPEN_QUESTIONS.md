# Open Questions

Use this file for uncertainty that future agents should not accidentally turn
into truth.

## Active Questions

| ID | Question | Status | Owner | Evidence | Next Step |
|---|---|---|---|---|---|
| OQ-002 | What measurable performance criteria should define success: curator latency, handoff completeness, model error reduction, user friction, or another metric? | open | user / implementer | `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md` | Define acceptance metrics before final evaluation. |
| OQ-003 | Should Git commit trailers become the preferred host-agent handoff format after the first Git-aware implementation works? | open | user / implementer | `scripts/wiki/scan_changes.py`; same source plan | Exercise `--commit` with real trailer-bearing commits, then decide preference. |
| OQ-004 | Should watcher support remain notification-only, or should guarded tmux prompt injection be added? | open | user / implementer | `scripts/wiki/watch_handoffs.py`; same source plan | Keep notification-only until a safe idle/lock signal is designed. |
| OQ-005 | Which semantic lint checks should become hard errors rather than warnings? | open | curator / implementer | `scripts/wiki/lint.py`; same source plan | Review false positives from real curation before enabling strict failures. |
| OQ-006 | Should `curator-auditor` be added immediately or only after deterministic gates are tested? | open | user / curator | same source plan | Defer until deterministic gates show gaps or high-risk diffs justify audit. |

## Resolved Questions

Move resolved questions here with a short answer and evidence link.

| ID | Question | Resolution | Evidence |
|---|---|---|---|
| OQ-001 | What is the first concrete project goal? | The project focus is improving `agent-wiki` performance and reliability through better handoffs, curator wakeups, and semantic safeguards. | User request on 2026-06-06; `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md` |
