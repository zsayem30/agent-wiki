# agent-wiki

`agent-wiki` is a curator-owned project memory scaffold for research coding
projects. It is designed to live as a subfolder inside a host project, while
the host project's `opencode.json` remains at the project root.

Recommended host layout:

```text
constrained-planning/
  opencode.json
  AGENTS.md
  src/
  experiments/
  results/
  figures/
  paper-wiki/
  agent-wiki/
```

The host project owns implementation, experiments, papers, figures, and
domain-specific agents. `agent-wiki/` owns compact durable memory and the
`wiki-curator` workflow.

## Core Idea

Research projects often accumulate many long Markdown files: plans, paper
notes, debug reports, experiment logs, and outdated summaries. Future agents
then waste time rereading stale material.

`agent-wiki` separates the surfaces:

| Surface | Path | Purpose |
|---|---|---|
| Host OpenCode config | `opencode.json` at project root | Active OpenCode harness config that points into `agent-wiki/`. |
| Curator contract | `agent-wiki/AGENTS.md`, `agent-wiki/.agents/wiki-curator.md` | Rules for maintaining compact memory. |
| Compact wiki | `agent-wiki/wiki/` | Current truth, routing, topic hubs, decisions, open questions. |
| Structured knowledge | `agent-wiki/knowledge/` | Machine-readable manifests, registries, events, handoffs. |
| Source material | `agent-wiki/sources/` | User-provided plans, ideas, papers, long reports, provenance. |
| Host outputs | `results/`, `figures/`, project-specific dirs | Generated experiment outputs and artifacts. |
| Integration templates | `agent-wiki/templates/project-root/` | Root `opencode.json` and `AGENTS.md` templates. |

The compact wiki is not a dumping ground. It is the distilled project memory
that tells agents what to read, what is true now, what has been tried, and what
should happen next.

## Documentation Site

This repository includes a Sphinx/MyST documentation site configured for Read
the Docs. Source lives in `docs/`; Read the Docs uses `.readthedocs.yaml` and
`docs/conf.py`.

Local build:

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -b html docs docs/_build/html
```

## Install In A Host Project

From the host project root:

```bash
git clone https://github.com/zsayem30/agent-wiki agent-wiki
cp agent-wiki/templates/project-root/opencode.json ./opencode.json
cp agent-wiki/templates/project-root/AGENTS.md ./AGENTS.md
```

If your project already has `opencode.json` or `AGENTS.md`, merge the template
sections instead of overwriting them.

## OpenCode Workflow

Start OpenCode from the host project root:

```bash
opencode
```

The root template configures two primary agents:

| Agent | Owns |
|---|---|
| `build` | Default OpenCode implementation/debugging/review work with agent-wiki context and host-agent memory rules. |
| `wiki-curator` | Compact memory in `agent-wiki/wiki/` and structured registries in `agent-wiki/knowledge/`. |

Use native commands:

| Command | Purpose |
|---|---|
| `/contextualize` | Load compact implementer context for the current host-agent task. |
| `/context-curator` | Load the curator context pack. |
| `/wiki-lint` | Run the wiki lint gate. |
| `/wiki-scan` | Record a handoff from current host-project changes. |
| `/wiki-review-next` | Load the next pending handoff for curator review. |
| `/wiki-watch` | Show the latest handoff wake-up event and watcher instructions. |
| `/wiki-map` | Regenerate `agent-wiki/wiki/PROJECT_MAP.md` from the host tree. |
| `/wiki-rollover` | Check active logs for rollover. |

Host projects can define additional implementer, deep-research, reporter, or
domain-specific agents in the root `opencode.json`. Optional example prompts
are available in `agent-wiki/templates/optional-agents/`.

## Host Agent Memory Rules

`agent-wiki` can inject memory hygiene rules into host OpenCode agents. This is
how project-specific implementers, researchers, and reporters learn to preserve
durable work and leave curator handoffs.

Default injection targets all non-curator host agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root .
```

Selective injection targets only named agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --agent implementer --agent reporter
```

Scratch agents can be excluded:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --exclude scratch
```

The injected rules tell host agents to ask whether durable brainstorms, plans,
implementations, debug findings, research, or reports should be preserved when
the user has not already specified memory behavior.

## Default Flow

```text
Host implementer / researcher / reporter agents do work
  -> durable material goes to agent-wiki/sources/ or host results/
  -> /wiki-scan records a Git-aware handoff with evidence and verification
  -> /wiki-watch or /wiki-review-next helps a curator notice pending work
  -> wiki-curator distills compact truth into agent-wiki/wiki/ and knowledge/
  -> /wiki-lint keeps memory clean
```

## Source Intake

User-provided material should go into `agent-wiki/sources/` first:

```text
agent-wiki/sources/inbox/implementation_plan.md
agent-wiki/sources/ideas/initial_idea.md
agent-wiki/sources/papers/paper1.md
agent-wiki/sources/reports/deep_research_2026-05-31.md
agent-wiki/sources/external/lab_notes.md
```

Register a source from the host root:

```bash
python agent-wiki/scripts/wiki/ingest_source.py agent-wiki/sources/inbox/implementation_plan.md --kind plan
```

The curator can then distill it into:

```text
agent-wiki/wiki/plans/active_plan.md
agent-wiki/wiki/topics/project_overview.md
agent-wiki/wiki/topics/literature.md
agent-wiki/wiki/OPEN_QUESTIONS.md
agent-wiki/knowledge/claim_registry.yaml
agent-wiki/knowledge/paper_registry.yaml
```

Raw sources may be long, speculative, or messy. The wiki should be short,
routed, status-aware, and evidence-linked.

## What Belongs Where

| Artifact | Default Destination |
|---|---|
| User-provided starting plan | `agent-wiki/sources/plans/` or `agent-wiki/sources/inbox/` |
| User-provided research idea | `agent-wiki/sources/ideas/` |
| Imported paper notes or summaries | `agent-wiki/sources/papers/` |
| Long research/debug/status report | `agent-wiki/sources/reports/` or host report area |
| Experiment output | host `results/`, plus run card in `agent-wiki/knowledge/experiment_registry.yaml` |
| Current project truth | `agent-wiki/wiki/CURRENT_STATE.md` |
| Topic overview | `agent-wiki/wiki/topics/*.md` |
| Project decision | `agent-wiki/wiki/decisions/ADR_*.md` |
| Dated paper-prep report | host `paper-wiki/` or `agent-wiki/sources/reports/` |

## Wiki Design Principles

1. `START_HERE.md` should remain short.
2. `CURRENT_STATE.md` should contain current truth, not history.
3. `ROUTING_TABLE.md` should tell agents the smallest useful context for each task.
4. Every durable claim should point to evidence.
5. Every important experiment should have a run card.
6. Every closed branch should have a closure note and a reopen gate.
7. Every long source document should have a status in `source_manifest.yaml`.
8. Active logs should be newest-first and split when they become too long.
9. The wiki-curator should record ambiguity as open questions, not fake certainty.
10. Host agents should hand off durable changes instead of directly bloating the wiki.

## Scripts

From the host project root:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
python agent-wiki/scripts/wiki/scan_changes.py --project-root . --truth-impact unknown --evidence <path-or-note>
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . next
python agent-wiki/scripts/wiki/watch_handoffs.py --project-root . --once
python agent-wiki/scripts/wiki/build_tree.py --project-root .
python agent-wiki/scripts/wiki/lint.py
```

From inside the `agent-wiki/` scaffold repository itself, omit
`agent-wiki/` from the paths.

## Adapting This Scaffold

At project start, edit:

- `agent-wiki/wiki/CURRENT_STATE.md`;
- `agent-wiki/wiki/topics/project_overview.md`;
- `agent-wiki/wiki/plans/active_plan.md`;
- `agent-wiki/knowledge/project_graph.yaml`;
- `agent-wiki/knowledge/source_manifest.yaml`.

Do not make `agent-wiki/` own your whole project. Its job is to preserve clean
memory so host agents can work without rereading stale documents.
