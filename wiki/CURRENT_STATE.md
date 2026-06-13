# Current State

Last curated: 2026-06-06.

## Active Project

This repository is focused on improving the performance and reliability of the
`agent-wiki` memory subsystem itself. The first implementation pass for better
handoffs, safer curator wakeups, queue helpers, semantic lint guardrails, and
host-agent OpenCode integration now exists; the active stage is hardening,
measuring, and deciding which optional or stricter gates should be enabled.

## Current Truth

- `claim_scaffold_separates_memory_surfaces`: `agent-wiki` separates compact
  wiki truth, structured registries, raw sources, and host/project artifacts.
- `claim_active_focus_agent_wiki_performance`: the accepted project focus is
  improving `agent-wiki` handoff auditability, curator activation, and semantic
  reliability.
- `claim_plan_git_provenance_jsonl_queue`: `scan_changes.py` now records
  Git-aware handoff metadata while keeping `knowledge/change_inbox.jsonl` as the
  portable queue and avoiding Git mutations.
- `claim_wakeup_queue_helpers_implemented`: safe handoff wakeups and queue
  review helpers now exist through `knowledge/events.jsonl`,
  `scripts/wiki/watch_handoffs.py`, and `scripts/wiki/handoff_queue.py`.
- `claim_semantic_lint_warnings_implemented`: `lint.py` now validates handoff
  and event JSONL and warns about unsupported truth/status promotion patterns.
- `claim_opencode_build_agent_context_memory_rules`: the project-root OpenCode
  template configures the built-in `build` agent as a host implementer with
  `/contextualize` context refresh and host-agent memory rules by default.

## Active Plan

Current active plan: `agent-wiki/wiki/plans/active_plan.md`

Next action:

- Harden the implemented handoff and OpenCode host-agent workflow, define
  performance metrics, and decide which semantic warnings should become strict
  failures.

## Important Evidence

- `agent-wiki/sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md`
- `agent-wiki/knowledge/change_inbox.jsonl` handoff `handoff_20260606_205931_716368a`
- `agent-wiki/knowledge/change_inbox.jsonl` handoff `handoff_20260606_233526_a2b28ab`
- `agent-wiki/scripts/wiki/scan_changes.py`
- `agent-wiki/scripts/wiki/watch_handoffs.py`
- `agent-wiki/scripts/wiki/handoff_queue.py`
- `agent-wiki/scripts/wiki/lint.py`
- `agent-wiki/templates/project-root/opencode.json`
- `agent-wiki/.opencode/instructions.md`
- `agent-wiki/knowledge/source_manifest.yaml`
- `agent-wiki/AGENTS.md`

## Active Branches Or Variants

| Branch | Status | Route | Notes |
|---|---|---|---|
| main | active | `agent-wiki/wiki/topics/project_overview.md` | Agent-wiki performance and reliability improvement track. |
| handoff-reliability | implemented / hardening | `agent-wiki/wiki/topics/method.md` | Git-backed handoffs, curator wakeups, queue helpers, and semantic lint warnings. |

## Recent Updates

Newest first.

- 2026-06-06: Curated implementation handoff `handoff_20260606_233526_a2b28ab`;
  the project-root OpenCode template now gives the default `build` agent
  implementer context guidance, `/contextualize`, and agent-wiki host-agent
  memory rules by default.
- 2026-06-06: Curated implementation handoff `handoff_20260606_205931_716368a`;
  Git-aware scanning, safe handoff events, watcher, queue helper, expanded
  handoff template, and semantic lint warnings are now implemented and verified
  by the handoff's listed commands plus curator re-run.
- 2026-06-06: Consolidated the Git-backed handoffs / curator wakeups /
  semantic gates source plan into the compact wiki, active plan, routes, open
  questions, and registries.

## Do Not Treat As Current Truth Yet

- Semantic lint currently provides checks and warnings; no strict hard-error
  policy is accepted yet.
- Commit trailers are supported as optional hints, but they are not the
  preferred or required handoff format yet.
- Guarded tmux prompt injection is not implemented; wakeups are notification /
  instruction based by default.
- Additional host-specific agents are not automatically covered unless they use
  the template or run the host-agent rule injector/checker workflow.
- A permanent second curator is not accepted; an optional high-risk auditor is
  only a possible future gate.
