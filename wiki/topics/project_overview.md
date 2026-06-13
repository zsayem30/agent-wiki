# Project Overview

Status: implemented / hardening

## Summary

This project improves the `agent-wiki` scaffold as an agent-facing memory
system. The first implementation pass addresses three reliability/performance
bottlenecks: handoffs that lacked Git provenance, curator activation that
depended on humans noticing pending work, and semantic mistakes from cheaper
models that can promote unsupported truth or inflate task status.

The project-root OpenCode template now also makes the default `build` agent a
memory-aware host implementer with compact context refresh.

The compact wiki should track the accepted direction while preserving the long
implementation details in `sources/plans/`.

## Research Goal

Make correct, evidence-linked memory maintenance the default behavior without
making the host-agent workflow heavy.

## Main Components

| Component | Status | Code Path | Notes |
|---|---|---|---|
| Handoff queue | implemented / extended | `knowledge/change_inbox.jsonl`, `scripts/wiki/scan_changes.py` | JSONL remains the portable queue; new records include IDs, Git metadata, evidence, verification, routes, truth impact, open questions, and curator status. |
| Git provenance | implemented | `scripts/wiki/scan_changes.py` | Captures branch, HEAD, dirty state, changed files, diff stats, optional commit metadata, and optional trailers without creating commits. |
| Curator wakeups | implemented safe default | `knowledge/events.jsonl`, `scripts/wiki/watch_handoffs.py` | Emits `handoff_created` events and prints notification-oriented curator prompts; tmux injection is not performed. |
| Handoff review helper | implemented | `scripts/wiki/handoff_queue.py` | Lists, shows, selects, and acknowledges handoffs using append-only status events. |
| Semantic gates | implemented as warnings | `scripts/wiki/lint.py`, curator/host-agent prompts | Checks JSONL schema, handoff truth evidence, event status, current-truth support, and completed/verified evidence patterns. |
| Host OpenCode integration | implemented | `templates/project-root/opencode.json`, `.opencode/instructions.md` | Configures `build` as a host implementer, adds `/contextualize`, and includes host-agent memory rules by default. |
| Optional auditor | deferred / conditional | future OpenCode command | Consider only for high-risk curator diffs after deterministic gates are tested. |

## Evidence

- `sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md`
- `knowledge/change_inbox.jsonl` handoff `handoff_20260606_205931_716368a`
- `knowledge/change_inbox.jsonl` handoff `handoff_20260606_233526_a2b28ab`
- `scripts/wiki/scan_changes.py`
- `scripts/wiki/watch_handoffs.py`
- `scripts/wiki/handoff_queue.py`
- `scripts/wiki/lint.py`
- `templates/project-root/opencode.json`
- `.opencode/instructions.md`
- `knowledge/source_manifest.yaml`

## Current Routes

- Active plan: `wiki/plans/active_plan.md`
- Method / architecture: `wiki/topics/method.md`
- Current state: `wiki/CURRENT_STATE.md`
- Open questions: `wiki/OPEN_QUESTIONS.md`
