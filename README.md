# agent-wiki

`agent-wiki` is a reusable scaffold for maintaining clean, durable project
memory in research coding projects. It is designed for LLM agents working in
Codex, Claude Code, OpenCode, or any terminal-based coding harness.

The goal is to prevent documentation sprawl: long plans, deep research notes,
experiment reports, and debugging writeups can exist, but they should not
become the default operating memory. Agents should route through a compact
wiki, structured registries, and evidence-linked source material.

## Core Idea

Most research codebases accumulate many Markdown files:

- initial ideas;
- implementation plans;
- paper notes;
- debugging reports;
- experiment logs;
- one-off summaries;
- outdated conclusions.

After a few weeks, future agents waste time rereading stale material and
cannot tell what is current. `agent-wiki` separates these surfaces:

| Surface | Path | Purpose |
|---|---|---|
| Agent contract | `AGENTS.md`, `CLAUDE.md`, `.agents/` | Rules and role prompts for every agent harness. |
| Compact wiki | `wiki/` | Current truth, routing, topic hubs, decisions, open questions. |
| Structured knowledge | `knowledge/` | Machine-readable manifests, registries, events, handoffs. |
| Source material | `sources/` | User-provided plans, ideas, papers, long agent reports, provenance. |
| Experiment outputs | `results/` | Generated data, logs, metrics, artifacts. |
| Templates | `templates/` | Standard shapes for new docs, claims, runs, reports, decisions. |
| Scripts | `scripts/wiki/` | Context loading, linting, source registration, project maps, reports. |

The compact wiki is not a dumping ground. It is the distilled project memory
that tells agents what to read, what is true now, what has been tried, and what
should happen next.

## Default Workflow

Use two agents for serious projects:

```text
Terminal 1: implementer / researcher / reporter
Terminal 2: wiki-curator
```

Terminal 1 can be any working agent. It may write code, debug, search papers,
draft plans, interpret results, or produce reports. Durable outputs go into
`sources/`, `results/`, or a structured registry.

Terminal 2 is the wiki-curator. It watches for durable outputs and distills
them into `wiki/` and `knowledge/`.

The usual flow is:

```text
User ideas, papers, plans, agent work
  -> sources/ or results/
  -> knowledge/change_inbox.jsonl
  -> wiki-curator review
  -> wiki/topics/*, wiki/CURRENT_STATE.md, registries, decisions
```

## Quick Start

Copy or clone this scaffold into a new project:

```bash
git clone <agent-wiki-repo> my-project
cd my-project
```

Start an implementer agent:

```bash
python scripts/wiki/contextualize.py --role implementer
```

Start a curator agent in another terminal:

```bash
python scripts/wiki/contextualize.py --role wiki-curator
python scripts/wiki/scan_changes.py --watch
```

If your harness supports custom commands, use the matching command:

```text
/contextualize --role implementer
/contextualize --role wiki-curator
```

Then work normally. Ask the implementer to write plans, code, tests, or
research notes. Ask the curator to distill durable changes into the wiki.

## Harness Compatibility

`agent-wiki` uses plain files and terminal commands so it can work across
multiple agent harnesses.

| Harness | Entry Point |
|---|---|
| Codex | Read `AGENTS.md`; run `python scripts/wiki/contextualize.py --role <role>`. |
| Claude Code | Read `CLAUDE.md`; use `/contextualize --role <role>` or run the script. |
| OpenCode | Read `AGENTS.md` and `.opencode/README.md`; run the script. |
| Generic terminal agent | Read `AGENTS.md`; run the script. |

The role contracts live in `.agents/` and are intentionally harness-neutral.

## Agent Roles

The scaffold includes four default role contracts:

| Role | Contract | Owns |
|---|---|---|
| Wiki Curator | `.agents/wiki-curator.md` | Compact wiki, registries, source manifest, routing, open questions. |
| Implementer | `.agents/implementer.md` | Research code, debugging, tests, implementation plans, code audits. |
| Deep Research | `.agents/deep-research.md` | Literature search, paper triage, credible sources, paper cards. |
| Reporter | `.agents/reporter.md` | Dated status reports, evidence-linked project summaries, paper-prep reports. |

Roles can be combined in small projects, but the surfaces should remain
separate. For example, an implementer can create a debug report, but the
curator decides which findings belong in `CURRENT_STATE.md`.

## Source Intake

User-provided material should go into `sources/` first:

```text
sources/inbox/implementation_plan.md
sources/ideas/initial_idea.md
sources/papers/paper1.md
sources/reports/deep_research_2026-05-31.md
sources/external/lab_notes.md
```

Then register the source:

```bash
python scripts/wiki/ingest_source.py sources/inbox/implementation_plan.md --kind plan
```

The curator can then distill it into:

```text
wiki/plans/active_plan.md
wiki/topics/project_overview.md
wiki/topics/literature.md
wiki/OPEN_QUESTIONS.md
knowledge/claim_registry.yaml
knowledge/paper_registry.yaml
```

Raw sources may be long, speculative, or messy. The wiki should be short,
routed, status-aware, and evidence-linked.

## What Belongs Where

| Artifact | Default Destination |
|---|---|
| User-provided starting plan | `sources/plans/` or `sources/inbox/` |
| User-provided research idea | `sources/ideas/` |
| Imported paper notes or summaries | `sources/papers/` |
| Deep research memo | `sources/reports/` |
| Implementation plan | `sources/plans/`, then compact plan in `wiki/plans/active_plan.md` |
| Debug or code audit report | `sources/reports/`, then claims/open questions if durable |
| Experiment output | `results/`, plus run card in `knowledge/experiment_registry.yaml` |
| Current project truth | `wiki/CURRENT_STATE.md` |
| Topic overview | `wiki/topics/*.md` |
| Project decision | `wiki/decisions/ADR_*.md` |
| Dated paper-prep report | `sources/reports/YYYY-MM-DD_project_report.md` |

## Wiki Design Principles

1. `START_HERE.md` should remain short.
2. `CURRENT_STATE.md` should contain current truth, not history.
3. `ROUTING_TABLE.md` should tell agents the smallest useful context for each
   task.
4. Every durable claim should point to evidence.
5. Every important experiment should have a run card.
6. Every closed branch should have a closure note and a reopen gate.
7. Every long source document should have a status in `source_manifest.yaml`.
8. Active logs should be newest-first and split when they become too long.
9. The wiki-curator should record ambiguity as open questions, not fake certainty.
10. Reports should cite source files, run cards, decisions, and claims.

## Scripts

| Script | Purpose |
|---|---|
| `contextualize.py` | Print a role-aware context pack for an agent. |
| `scan_changes.py` | Record git changes into `knowledge/change_inbox.jsonl`. |
| `ingest_source.py` | Register a user or agent source document. |
| `lint.py` | Check required files, links, frontmatter, routing, and registries. |
| `build_tree.py` | Regenerate `wiki/PROJECT_MAP.md` from the repository tree. |
| `rollover_logs.py` | Identify active logs that should be split or closed. |
| `new_report.py` | Create a dated reporter document from the report template. |
| `timestamp.py` | Emit a local ISO-8601 timestamp with timezone. |

Run the basic checks with:

```bash
python scripts/wiki/lint.py
```

## Reports And Paper Preparation

The reporter role creates dated, evidence-linked reports in `sources/reports/`.
These reports are allowed to be long because they are source artifacts, not
startup context. A report should explain:

- current project status;
- important code paths;
- verified results;
- failed or superseded branches;
- open questions;
- evidence links;
- what is ready for a paper;
- what still needs validation.

The curator then updates compact wiki pages and registries if the report
changes project truth.

## Adapting This Scaffold

At project start, edit:

- `wiki/CURRENT_STATE.md`;
- `wiki/topics/project_overview.md`;
- `wiki/plans/active_plan.md`;
- `knowledge/project_graph.yaml`;
- `knowledge/source_manifest.yaml`.

Do not delete the role contracts or the storage boundaries unless you replace
them with stricter equivalents. The value of this scaffold is not the exact
file names; it is the discipline that durable knowledge has a home, a status,
and evidence.

