---
status: draft
kind: implementation_plan
created: 2026-06-06
last_reviewed: 2026-06-06
topic: git-backed handoffs, curator wakeups, semantic reliability gates
summary: Improve agent-wiki handoffs with Git provenance, curator wake-up events, and stricter semantic safeguards for cheaper models.
---

# Implementation Plan: Git-Backed Handoffs, Curator Wakeups, And Semantic Gates

## Purpose

This plan preserves the 2026-06-06 design discussion about improving
`agent-wiki` handoffs, curator activation, and lower-cost model reliability.
It is source material for future implementation, not current project truth until
the user accepts it and a curator distills it into compact wiki state.

## Better Structured Original Prompt

The project uses `agent-wiki/` as a curator-owned memory subsystem for host
research projects. Host agents perform implementation, research, debugging,
experiments, and reporting. The `wiki-curator` distills durable evidence into
compact wiki truth and structured registries.

I want to improve three parts of the system:

1. Git-backed handoffs. Today curator handoffs are tracked through Markdown or
   JSONL files such as `knowledge/change_inbox.jsonl`. I want handoffs to behave
   more like structured Git commit messages. After an implementer or
   project-specific agent finishes work, the handoff should say what files were
   modified, why they changed, where evidence lives, whether current truth may
   have changed, and what the curator should inspect next. This should make
   version control, diffs, rollback, and debugging easier.

2. Curator wake-up mechanism. If a curator agent is running in another terminal,
   then when a handoff is initiated by a host agent or Python script, the
   curator should be notified or safely woken so it can process the handoff.

3. Better rule enforcement for cheaper models. Lower-cost models such as
   DeepSeek or Qwen sometimes make semantic mistakes, including recording
   planned work as completed, promoting unverified claims to current truth, or
   failing to verify evidence. I want stronger enforcement of curator rules. I
   am considering whether two curator agents are needed, where one audits the
   other, but this may be inefficient.

Core design question: how can `agent-wiki` make correct memory maintenance the
default behavior without making the workflow too heavy?

## Distilled Recommendation

Use Git as provenance, not as the only handoff queue in the first
implementation.

Keep `knowledge/change_inbox.jsonl` as the portable machine-readable handoff
queue, but enrich each handoff with Git metadata: branch, HEAD SHA, changed
files, diff stat, optional commit SHA, optional commit trailers, evidence paths,
verification, truth impact, suggested routes, and open questions.

Do not make handoff-only Git commits the default. They can pollute history and
risk committing unrelated dirty files. Prefer this lifecycle:

1. Host agent performs work.
2. Host agent optionally makes a normal implementation commit if the user asked
   for commits.
3. Host agent runs `scan_changes.py`.
4. `scan_changes.py` records Git metadata and appends a structured handoff.
5. Curator reviews the handoff and makes a separate curator commit if wiki truth
   changes and the user requested commits.

For wakeups, implement a safe event notification system first. Do not inject
keystrokes into another terminal by default. Use `events.jsonl`, a watcher
script, terminal bell, macOS notification, and command hints. Add tmux or
OpenCode prompt injection only as an explicit advanced option.

For cheaper model reliability, prefer deterministic gates over a permanent
second curator. Add semantic lint checks, stricter schemas, explicit status
enums, required evidence fields, and high-risk audit only when truth-bearing
files change.

## Goals

1. Make handoffs auditable through Git metadata and structured records.
2. Allow the curator to notice new handoffs without constant polling by a human.
3. Prevent unsupported truth promotion and status inflation.
4. Preserve the current lightweight `agent-wiki` workflow.
5. Keep the solution compatible with existing `change_inbox.jsonl` entries.

## Non-Goals

1. Do not automatically stage, commit, revert, reset, or otherwise modify user
   Git history.
2. Do not replace the curator with two always-on agents.
3. Do not make Git notes, custom refs, or commit trailers the only source of
   handoff truth in the first version.
4. Do not blindly inject keystrokes into a terminal session that may be busy.
5. Do not promote this plan into `CURRENT_STATE.md` until the user accepts it.

## Design Principles

1. Git should provide provenance, diffs, rollback context, and commit-level
   evidence.
2. JSONL should remain the local, portable queue because it is easy for agents
   and scripts to append and inspect.
3. Curator updates should remain conservative: evidence first, truth second.
4. Wake-up mechanisms should be advisory and safe before they become automated.
5. Semantic correctness should be enforced with schemas and lint before adding
   more agent roles.
6. A reviewer agent should be optional, narrow, and triggered only for risky
   diffs.

## Proposed Architecture

The handoff pipeline should become:

```text
Host agent work
  -> optional normal Git commit
  -> scan_changes.py records Git-aware handoff
  -> knowledge/change_inbox.jsonl receives structured record
  -> knowledge/events.jsonl receives handoff_created event
  -> watch_handoffs.py notifies curator terminal
  -> curator reviews evidence and routes
  -> curator updates compact wiki or registries only when evidence supports it
  -> lint verifies syntax and semantic guardrails
  -> optional audit checks high-risk curator diff
```

This keeps the existing memory model but improves auditability and activation.

## Handoff Schema

Add fields for new handoffs while accepting older JSONL entries for
compatibility.

Recommended new record shape:

```json
{
  "id": "handoff_20260606_120000_ab12cd3",
  "timestamp": "2026-06-06T12:00:00-07:00",
  "timestamp_utc": "2026-06-06T19:00:00+00:00",
  "kind": "manual_scan",
  "summary": "Short human-readable handoff summary.",
  "project_root": "/path/to/host",
  "agent_wiki_root": "/path/to/host/agent-wiki",
  "git": {
    "branch": "main",
    "head": "abc123",
    "commit": null,
    "is_dirty": true,
    "changed": [],
    "diff_stat": []
  },
  "evidence": [],
  "verification": [],
  "suggested_routes": [],
  "current_truth_changed": "unknown",
  "open_questions": [],
  "curator_status": "pending"
}
```

Allowed values:

| Field | Values |
|---|---|
| `current_truth_changed` | `yes`, `no`, `unknown` |
| `curator_status` | `pending`, `acknowledged`, `curated`, `deferred`, `rejected` |
| `kind` | `manual_scan`, `implementation`, `research`, `debug`, `experiment`, `report`, `audit`, `other` |

## Git Commit Trailer Support

Support commit trailers as optional structured hints. Do not require them for
all handoffs at first.

Example trailer block:

```text
Agent-Wiki-Handoff: true
Truth-Change: unknown
Evidence: results/run_2026_06_06
Routes: agent-wiki/wiki/topics/project_overview.md
Verification: pytest tests/test_core.py passed
Open-Question: Does this result supersede claim C-003?
```

Implementation details:

1. Add `--commit <sha>` to `scripts/wiki/scan_changes.py`.
2. If `--commit` is present, collect changed files with `git show --name-status`.
3. Collect diff stats with `git show --stat --oneline` or a safer structured
   variant.
4. Parse trailers from the commit message using `git interpret-trailers` when
   available.
5. If no commit is provided, keep worktree-based scanning behavior.
6. Do not create commits inside `scan_changes.py`.

## Wake-Up Mechanism

Implement safe notification first.

New behavior:

1. `scan_changes.py` appends a handoff to `knowledge/change_inbox.jsonl`.
2. `scan_changes.py` appends a `handoff_created` event to
   `knowledge/events.jsonl`.
3. `scripts/wiki/watch_handoffs.py` watches `events.jsonl` or
   `change_inbox.jsonl`.
4. The watcher prints the new handoff summary, rings the terminal bell, and
   optionally sends a macOS notification.
5. The watcher prints the recommended command, such as `/wiki-review-next`.

Avoid terminal prompt injection by default. Add tmux pane injection only behind
an explicit flag such as `--tmux-pane`.

Recommended watcher CLI:

```bash
python scripts/wiki/watch_handoffs.py --project-root .
python scripts/wiki/watch_handoffs.py --project-root . --once
python scripts/wiki/watch_handoffs.py --project-root . --notify macos
python scripts/wiki/watch_handoffs.py --project-root . --tmux-pane %2
```

The `--tmux-pane` mode should check an idle or lock file before injecting text.
If no safe idle signal exists, it should print instructions instead of injecting.

## Handoff Queue Helper

Add an optional helper script to make handoff consumption less ambiguous.

Recommended commands:

```bash
python scripts/wiki/handoff_queue.py list --project-root .
python scripts/wiki/handoff_queue.py next --project-root .
python scripts/wiki/handoff_queue.py show <handoff_id> --project-root .
python scripts/wiki/handoff_queue.py ack <handoff_id> --project-root . --status curated
```

Implementation approach:

1. Keep `change_inbox.jsonl` append-only.
2. Store acknowledgement events in `knowledge/events.jsonl`.
3. Compute pending handoffs by subtracting acknowledged, curated, deferred, or
   rejected handoff IDs from created handoff IDs.
4. Avoid rewriting old handoff entries.

## Semantic Reliability Gates

Add deterministic checks before adding a second curator.

Rules:

1. A current-truth claim must have evidence.
2. A completed or verified status must have verification evidence.
3. Planned work must not be marked completed.
4. Ambiguous or unsupported claims must become open questions.
5. Handoffs must explicitly say `current_truth_changed: yes`, `no`, or
   `unknown`.
6. Curator edits to truth-bearing files should be linted before completion.

Truth-bearing files:

| Path | Why It Is Truth-Bearing |
|---|---|
| `wiki/CURRENT_STATE.md` | Startup truth and active state. |
| `wiki/topics/*.md` | Topic-level synthesized truth. |
| `wiki/plans/active_plan.md` | Current plan and task status. |
| `wiki/OPEN_QUESTIONS.md` | Known uncertainty. |
| `wiki/decisions/*.md` | Project decisions and reopen gates. |
| `knowledge/claim_registry.yaml` | Evidence-linked claims. |
| `knowledge/experiment_registry.yaml` | Experiment status and results. |
| `knowledge/paper_registry.yaml` | Literature relevance and caveats. |
| `knowledge/report_registry.yaml` | Durable report index. |

Start semantic lint as warnings where false positives are likely. Add a
`--strict` mode after the workflow stabilizes.

## Curator Prompt Updates

Update `.agents/wiki-curator.md` with a truth-promotion checklist:

```text
Before promoting any statement to current truth, verify:

1. What exact evidence supports it?
2. Is it completed, verified, active, planned, attempted, failed, or superseded?
3. Has the evidence been opened or is it only referenced by a handoff?
4. Does the claim belong in CURRENT_STATE, a topic hub, a registry, or OPEN_QUESTIONS?
5. Is there any uncertainty that should stay explicit?
6. Did lint pass after edits?
```

Also update host-agent memory rules so host agents provide evidence and
verification explicitly instead of relying on the curator to infer them.

## Optional Curator Auditor

Do not run two full curators by default.

Add an optional `curator-auditor` only for high-risk diffs. Its role should be
narrow:

1. Review only the curator diff.
2. Check whether claims have evidence.
3. Check whether statuses are justified.
4. Check whether planned work was accidentally marked completed.
5. Check whether uncertain items belong in `OPEN_QUESTIONS.md`.
6. Do not redo curation.

Trigger audit manually or when truth-bearing files changed.

Potential OpenCode command:

```text
/wiki-audit
```

The command should show the auditor the curator diff, relevant handoff, and
evidence paths. It should return findings only.

## OpenCode Command Updates

Add or update commands in `templates/project-root/opencode.json`.

Candidate commands:

| Command | Purpose |
|---|---|
| `/wiki-scan` | Create Git-aware handoff from current changes. |
| `/wiki-review-next` | Load next pending handoff for curator review. |
| `/wiki-watch` | Explain or start the watcher workflow. |
| `/wiki-audit` | Optional high-risk curator diff audit. |

The active command behavior should remain simple enough for host users to adopt.

## Implementation Steps

1. Create this plan file under `sources/plans/`.
2. Register it in `knowledge/source_manifest.yaml` with `ingest_source.py`.
3. Extend `scan_changes.py` with helpers for branch, HEAD SHA, dirty state,
   changed files, diff stats, and optional commit metadata.
4. Add handoff IDs and the expanded handoff schema.
5. Add CLI arguments: `--evidence`, `--verification`, `--truth-impact`,
   `--open-question`, `--commit`, and `--no-event`.
6. Preserve compatibility with existing minimal JSONL handoffs.
7. Add `knowledge/events.jsonl` emission after handoff creation.
8. Add `watch_handoffs.py` with polling, terminal bell, optional macOS
   notification, and `--once`.
9. Add optional `handoff_queue.py` with `list`, `next`, `show`, and `ack`
   subcommands.
10. Update `lint.py` to validate new handoff fields.
11. Add semantic lint warnings for unsupported verified, completed, and
   current-truth wording.
12. Update `templates/handoff.json`.
13. Update `.agents/wiki-curator.md` with the truth-promotion checklist.
14. Update `.opencode/host-agent-memory-rules.md` so host agents provide
   evidence and verification explicitly.
15. Update `templates/project-root/opencode.json` with new commands.
16. Update docs and routing table.
17. Run verification commands.
18. Leave a curator handoff for the scaffold change if project memory may need
   compact wiki updates.

## Tests And Verification

Run these commands from the scaffold repository root:

```bash
python scripts/wiki/scan_changes.py --dry-run
python scripts/wiki/scan_changes.py --dry-run --truth-impact unknown --evidence sources/plans/2026-06-06_git_backed_handoffs_curator_wakeup_semantic_gates.md
python scripts/wiki/lint.py
python -m py_compile scripts/wiki/*.py
```

If watcher support is added:

```bash
python scripts/wiki/watch_handoffs.py --once
```

Acceptance criteria:

1. New handoffs include Git branch, HEAD SHA, changed files, diff stat,
   evidence, verification, truth impact, routes, and status.
2. Old handoff entries still lint successfully.
3. Running `scan_changes.py` does not stage, commit, or revert anything.
4. A new handoff emits a wake-up event.
5. Watcher notices the event and gives the curator an actionable route.
6. Lint warns or fails on unsupported truth promotion.
7. Docs explain the safer Git-plus-JSONL model.

## Risks

1. Over-strict semantic lint could block legitimate edits.
2. Notification behavior may differ across macOS, Linux, tmux, and plain
   terminals.
3. Git diffs can be large, so store diff stats by default and full patches only
   by opt-in.
4. Commit trailers may be inconsistently written by cheaper models.
5. Prompt injection into active terminal sessions can corrupt agent work if not
   guarded by an idle or lock signal.

## Rollback

1. Revert the scripts and docs changed for this feature.
2. Keep existing `change_inbox.jsonl` entries because the old curator can still
   read them.
3. Disable watcher by not running it.
4. Disable strict semantic lint by leaving checks as warnings or adding
   `--strict` opt-in only.
5. Do not require Git trailers until the workflow is stable.

## Curator Handoff

Current truth changes: no. This is a proposed implementation plan until accepted
and distilled by the curator.

Claims to update: none yet.

Open questions:

1. Should Git commit trailers become the preferred host-agent handoff format
   after the first implementation works?
2. Should watcher support tmux prompt injection, or remain notification-only?
3. Which semantic lint checks should become hard errors rather than warnings?
4. Should `curator-auditor` be added immediately or only after deterministic
   gates are tested?
