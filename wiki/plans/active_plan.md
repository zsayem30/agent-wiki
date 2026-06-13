# Active Plan

Status: implemented / hardening

## Current Plan

Improve `agent-wiki` performance and reliability by hardening the implemented
Git-backed handoff, curator wakeup, handoff queue, and semantic lint workflow.

Source: `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md`

Working direction:

- Keep `knowledge/change_inbox.jsonl` as the portable handoff queue.
- Use `knowledge/events.jsonl` for safe wake-up and handoff status events.
- Keep wakeups notification-oriented unless an explicit safe idle/lock signal is
  designed.
- Promote semantic lint warnings to hard errors only after false positives are
  understood.

## Completed In First Implementation Pass

| Item | Evidence |
|---|---|
| Git-aware handoff records and optional commit/trailer parsing in `scan_changes.py` | `scripts/wiki/scan_changes.py`; handoff `handoff_20260606_205931_716368a` |
| Handoff event emission to `knowledge/events.jsonl` | `scripts/wiki/scan_changes.py`; `knowledge/events.jsonl` |
| Safe watcher CLI for handoff notifications | `scripts/wiki/watch_handoffs.py` |
| Append-only queue helper for list/next/show/ack | `scripts/wiki/handoff_queue.py` |
| Expanded handoff template | `templates/handoff.json` |
| Semantic lint warnings for handoffs, events, evidence, and statuses | `scripts/wiki/lint.py` |
| Default OpenCode `build` agent with implementer context guidance, `/contextualize`, and host-agent memory rules | `templates/project-root/opencode.json`; handoff `handoff_20260606_233526_a2b28ab` |

## Next Actions

| Priority | Action | Owner | Evidence / Source |
|---|---|---|---|
| P0 | Define measurable performance/reliability criteria for the new workflow. | user / implementer | `wiki/OPEN_QUESTIONS.md` OQ-002 |
| P0 | Exercise Git-aware scanning on clean worktrees, dirty worktrees, staged changes, and explicit commits with trailers. | implementer | `scripts/wiki/scan_changes.py`; source plan |
| P1 | Exercise the copied project-root OpenCode template in a host project and confirm `/contextualize` plus memory handoff behavior works in the default `build` agent. | implementer | `templates/project-root/opencode.json`; `docs/opencode-workflow.md` |
| P1 | Review semantic lint warnings for false positives and decide which should become strict failures. | curator / implementer | `scripts/wiki/lint.py`; OQ-005 |
| P1 | Decide whether Git trailers should become preferred, optional, or discouraged. | user / implementer | OQ-003 |
| P2 | Decide whether guarded tmux prompt injection or a `curator-auditor` is worth adding. | user / curator | OQ-004, OQ-006 |

## Deferred Plans

- Git-only handoff storage through notes, refs, trailers, or forced commits.
- Handoff-only Git commits as the default workflow.
- Prompt injection into active terminals without an explicit safety mechanism.
- A permanent second curator for every wiki update.
