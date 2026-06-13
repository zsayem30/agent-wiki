# Method

Status: implemented / hardening

This topic summarizes the implemented handoff reliability method and remaining
hardening decisions. Keep detailed sequencing in `wiki/plans/active_plan.md`
and source rationale in `sources/plans/`.

## Current Method

For OpenCode host work, start from the project-root template: the built-in
`build` agent is configured as a host implementer, can refresh compact context
with `/contextualize`, and inherits agent-wiki host-agent memory rules by
default.

Use a Git-plus-JSONL handoff model:

1. Host agents perform work and optionally create normal implementation commits
   only when the user asks.
2. `scan_changes.py` records a structured handoff in
   `knowledge/change_inbox.jsonl` with Git provenance, evidence, verification,
   truth impact, suggested routes, open questions, and curator status.
3. `scan_changes.py` emits `handoff_created` events to `knowledge/events.jsonl`
   unless `--no-event` is used.
4. `watch_handoffs.py` can alert a running curator with a terminal bell,
   optional macOS notification, and `/wiki-review-next` instructions without
   blindly injecting text into a busy terminal.
5. `handoff_queue.py` lists, shows, selects, and acknowledges handoffs using
   append-only status events.
6. The curator promotes only evidence-backed truth and runs lint after edits.
7. Semantic lint warnings guard against unsupported truth promotion,
   completed/verified status inflation, invalid handoff/event records, and
   missing evidence.

## Design Constraints

- Do not make handoff-only Git commits the default.
- Do not make Git trailers, notes, or refs the only handoff source in the first
  version.
- Do not stage, commit, reset, revert, or otherwise mutate Git history from
  handoff scanning.
- Do not inject keystrokes into another terminal unless an explicit advanced
  option and safety signal exist.
- Prefer deterministic schemas and lint before adding another always-on curator.

## Implementation Hooks

| Concept | Code Path | Source |
|---|---|---|
| Git-aware scan | `scripts/wiki/scan_changes.py` | `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md` |
| Handoff queue | `knowledge/change_inbox.jsonl` | `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md` |
| Wake-up events | `knowledge/events.jsonl`, `scripts/wiki/watch_handoffs.py` | `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md` |
| Queue helper | `scripts/wiki/handoff_queue.py` | `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md` |
| Semantic lint | `scripts/wiki/lint.py` | `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md` |
| Prompt safeguards | `.agents/wiki-curator.md`, `.opencode/host-agent-memory-rules.md` | `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md` |
| Host-agent context refresh | `templates/project-root/opencode.json`, `.opencode/instructions.md` | `knowledge/change_inbox.jsonl` handoff `handoff_20260606_233526_a2b28ab` |

## Related Decisions

- No ADR yet. The current implementation follows the accepted plan; create an
  ADR if Git-plus-JSONL handoffs, notification behavior, or semantic gates
  become a stable project decision that should have a reopen gate.

## Claims

See `knowledge/claim_registry.yaml`.
