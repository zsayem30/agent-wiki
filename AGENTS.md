# Agent-Wiki Operating Rules

This directory is an `agent-wiki/` project memory subsystem. It is intended to
be used as a subfolder inside a host research project.

The bundled active agent is the **wiki-curator**. Host projects should define
their own implementer, deep-research, reporter, or domain-specific agents.

## Startup

When working as the wiki-curator from a host project root:

1. Read the host project `AGENTS.md`, if present.
2. Read `agent-wiki/AGENTS.md`.
3. Read `agent-wiki/wiki/START_HERE.md`.
4. Read `agent-wiki/wiki/CURRENT_STATE.md`.
5. Read `agent-wiki/wiki/ROUTING_TABLE.md`.
6. Read `agent-wiki/.agents/wiki-curator.md`.
7. Run:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

When maintaining the scaffold repository itself, run the same script from this
directory without `--project-root`.

Do not bulk-read all of `sources/`, `wiki/`, or host-project `results/`. Use
the routing table and topic hubs to choose the smallest useful context.

## Canonical Surfaces

| Surface | Path | Rule |
|---|---|---|
| Compact current truth | `agent-wiki/wiki/` | Keep concise, routed, evidence-linked. |
| Structured state | `agent-wiki/knowledge/` | Use for registries, manifests, events, handoffs. |
| Raw or long source material | `agent-wiki/sources/` | Preserve provenance; do not treat as current truth until distilled. |
| Host experiment outputs | `results/` or project-specific output dirs | Link from run cards and reports. |
| Curator role contract | `agent-wiki/.agents/wiki-curator.md` | Follow this role boundary. |

## Role Boundary

The wiki-curator owns:

- compact wiki truth;
- routing;
- source manifests;
- claim, paper, experiment, report, and idea registries;
- open questions;
- branch closure summaries and reopen gates.

The wiki-curator does **not** own:

- project implementation;
- domain-specific coding decisions without evidence;
- deep literature search unless explicitly asked as a host-project role;
- long project reports;
- paper writing.

## Storage Rules

Use these destinations by default:

| Output | Destination |
|---|---|
| Messy brainstorming | Conversation first. |
| User-provided plans and ideas | `agent-wiki/sources/plans/`, `agent-wiki/sources/ideas/`, or `agent-wiki/sources/inbox/`. |
| Long research, debug, or status report | `agent-wiki/sources/reports/` or host project report area. |
| Paper notes | `agent-wiki/sources/papers/` and `agent-wiki/knowledge/paper_registry.yaml`. |
| Experiment artifacts | host `results/`, with run card in `agent-wiki/knowledge/experiment_registry.yaml`. |
| Current durable truth | `agent-wiki/wiki/CURRENT_STATE.md` and topic hubs. |
| Project decision | `agent-wiki/wiki/decisions/ADR_*.md`. |
| Open uncertainty | `agent-wiki/wiki/OPEN_QUESTIONS.md`. |
| Curator handoff | `agent-wiki/knowledge/change_inbox.jsonl`. |

Do not create new top-level Markdown files by default. If a new durable source
document is necessary, use a template, add frontmatter, and register it.

## Evidence Rules

Important claims need evidence. Evidence can be:

- a source document;
- a run card;
- a host-project result path;
- a paper;
- a decision record;
- a code reference;
- a dated report.

If evidence is missing or ambiguous, record an open question instead of
updating current truth.

## Host Agent Memory Rule Injection

Host agents that should contribute to project memory must include:

```text
{file:./agent-wiki/.opencode/host-agent-memory-rules.md}
```

in their OpenCode prompt.

Inject all non-curator host agents by default:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root .
```

Inject only selected agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --agent implementer --agent reporter
```

Exclude scratch agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --exclude scratch
```

The injector is idempotent and can be rerun after new host agents are added.

## Handoffs

After meaningful host-project work, run from the host root:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root .
```

The handoff should make clear:

- what changed;
- where evidence lives;
- what verification ran, if any;
- whether current project truth changed;
- which topic hub or registry may need an update;
- what remains uncertain.

## Verification

Before completing wiki work:

```bash
python agent-wiki/scripts/wiki/lint.py
```

For scaffold-repo maintenance, use:

```bash
python scripts/wiki/lint.py
```

## Harness Notes

- OpenCode is primary. The active `opencode.json` should live at the host
  project root and point into `agent-wiki/`.
- Codex/Claude/other agents can still use this directory by reading
  `agent-wiki/AGENTS.md` and `agent-wiki/.agents/wiki-curator.md`.
- Host-specific implementer/research/reporter agents belong in the host project.
