# Agent Operating Rules

This repository uses `agent-wiki` as its project memory scaffold. Every agent
must treat this file as the repo contract.

## Startup

At the start of a session:

1. Read this file.
2. Read `wiki/START_HERE.md`.
3. Read `wiki/CURRENT_STATE.md`.
4. Read `wiki/ROUTING_TABLE.md`.
5. Read your role contract in `.agents/`.
6. Run the role-aware context command when possible:

```bash
python scripts/wiki/contextualize.py --role <role>
```

Do not bulk-read all of `sources/`, `wiki/`, or `results/`. Use the routing
table and topic hubs to choose the smallest useful context.

## Canonical Surfaces

| Surface | Path | Rule |
|---|---|---|
| Compact current truth | `wiki/` | Keep concise, routed, evidence-linked. |
| Structured state | `knowledge/` | Use for registries, manifests, events, handoffs. |
| Raw or long source material | `sources/` | Preserve provenance; do not treat as current truth until distilled. |
| Generated experiment outputs | `results/` | Link from run cards and reports. |
| Role contracts | `.agents/` | Follow your role boundaries. |

## Roles

Default roles:

- `wiki-curator`: maintains compact wiki and structured knowledge.
- `implementer`: changes code, debugs, tests, reviews, writes implementation
  plans and audit/debug reports.
- `deep-research`: finds and summarizes credible papers and related work.
- `reporter`: creates dated, evidence-linked project reports.

Agents may perform more than one role only when explicitly asked. Keep role
outputs separate.

## Storage Rules

Use these destinations by default:

| Output | Destination |
|---|---|
| Messy brainstorming | Conversation first. |
| User-provided plans and ideas | `sources/plans/`, `sources/ideas/`, or `sources/inbox/`. |
| Deep research memo | `sources/reports/`. |
| Paper notes | `sources/papers/` and `knowledge/paper_registry.yaml`. |
| Implementation plan | `sources/plans/`, then compact pointer in `wiki/plans/active_plan.md`. |
| Debug/code audit report | `sources/reports/`. |
| Experiment artifacts | `results/`, with run card in `knowledge/experiment_registry.yaml`. |
| Current durable truth | `wiki/CURRENT_STATE.md` and topic hubs. |
| Project decision | `wiki/decisions/ADR_*.md`. |
| Open uncertainty | `wiki/OPEN_QUESTIONS.md`. |
| Curator handoff | `knowledge/change_inbox.jsonl`. |

Do not create new top-level Markdown files by default. If a new durable source
document is necessary, use a template, add frontmatter, and register it.

## Evidence Rules

Important claims need evidence. Evidence can be:

- a source document;
- a run card;
- a result path;
- a paper;
- a decision record;
- a code reference;
- a dated report.

If evidence is missing or ambiguous, record an open question instead of
updating current truth.

## Logs

Active logs in `wiki/logs/active/` are newest-first. They should contain
compact, evidence-linked entries, not full reports. Split or close logs when
they become too long or when a branch ends.

Use:

```bash
python scripts/wiki/rollover_logs.py --threshold 800
```

## Handoffs

After meaningful work, run:

```bash
python scripts/wiki/scan_changes.py
```

The handoff should make clear:

- what changed;
- where evidence lives;
- whether current project truth changed;
- which topic hub or registry may need an update;
- what remains uncertain.

## Verification

Before completing documentation or wiki work:

```bash
python scripts/wiki/lint.py
```

Before completing code work, run focused tests appropriate to the changed code.

## Harness Notes

- Codex and OpenCode agents should use this `AGENTS.md` plus `.agents/<role>.md`.
- Claude Code agents should read `CLAUDE.md`, which points back to this file.
- Any harness may run `python scripts/wiki/contextualize.py --role <role>`.

