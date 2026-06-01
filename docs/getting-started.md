# Getting Started

This page shows the intended first-session workflow for a new research project.

## The Intended Shape

A host project should look like this:

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

The host project owns implementation and research work. `agent-wiki/` owns
project memory hygiene.

## Install The Scaffold

From the host project root:

```bash
git clone https://github.com/zsayem30/agent-wiki agent-wiki
cp agent-wiki/templates/project-root/opencode.json ./opencode.json
cp agent-wiki/templates/project-root/AGENTS.md ./AGENTS.md
```

If your host project already has `opencode.json` or `AGENTS.md`, merge the
agent-wiki sections instead of overwriting your existing files.

## Start OpenCode

```bash
opencode
```

Then load the curator context:

```text
/context-curator
```

The bundled `wiki-curator` reads the compact startup route and maintains
`agent-wiki/wiki/` and `agent-wiki/knowledge/`.

## Add Starting Material

Put initial plans, ideas, papers, or notes in `agent-wiki/sources/`:

```text
agent-wiki/sources/inbox/implementation_plan.md
agent-wiki/sources/ideas/idea.md
agent-wiki/sources/papers/paper1.md
```

Register a source:

```bash
python agent-wiki/scripts/wiki/ingest_source.py   agent-wiki/sources/inbox/implementation_plan.md   --kind plan
```

Then ask the curator to distill only durable, evidence-backed truth into:

```text
agent-wiki/wiki/CURRENT_STATE.md
agent-wiki/wiki/topics/project_overview.md
agent-wiki/wiki/plans/active_plan.md
agent-wiki/wiki/OPEN_QUESTIONS.md
```

## The Core Loop

```text
Host agents do work
  -> durable evidence goes to agent-wiki/sources/ or host results/
  -> host agent runs /wiki-scan or scan_changes.py
  -> wiki-curator distills compact truth
  -> /wiki-lint keeps memory clean
```

The point is not to stop agents from writing. The point is to keep raw work,
structured state, and current truth in separate places.
