# Getting Started

This page assumes the scaffold is already installed. If it is not, start with
[Installation](installation.md).

## First Session Shape

A clean host project keeps active work and durable project memory separate:

```text
constrained-planning/
|-- opencode.json          # active OpenCode config for the host project
|-- AGENTS.md              # host-level agent contract
|-- src/                   # research code
|-- experiments/           # experiment scripts and configs
|-- results/               # generated outputs owned by the host project
|-- figures/               # plots and paper figures
|-- paper-wiki/            # optional paper-writing workspace
`-- agent-wiki/            # compact agent memory subsystem
    |-- wiki/              # small current-truth pages
    |-- knowledge/         # structured registries and handoffs
    `-- sources/           # long evidence, plans, papers, reports
```

## Start The Curator

Launch OpenCode from the host root:

```bash
opencode
```

Then load the curator context:

```text
/context-curator
```

The bundled `wiki-curator` reads the compact startup route and maintains
`agent-wiki/wiki/` and `agent-wiki/knowledge/`. It should not bulk-read the
host repository unless the route or user request calls for it.

## Add Starting Material

Put plans, ideas, papers, or notes in `agent-wiki/sources/`:

```text
agent-wiki/sources/
|-- inbox/
|   `-- implementation_plan.md
|-- ideas/
|   `-- idea.md
|-- papers/
|   |-- paper1.md
|   `-- paper2.md
`-- reports/
```

Register a source when you want it to become visible to the curator:

```bash
python agent-wiki/scripts/wiki/ingest_source.py agent-wiki/sources/inbox/implementation_plan.md --kind plan
```

Then ask the curator to distill only durable, evidence-backed truth into the
compact wiki:

```text
Please review the newly ingested implementation plan. Update compact project
memory only where the source supports durable truth, and put unresolved points
in OPEN_QUESTIONS.md.
```

## Run The Work Loop

The normal loop is:

```text
Host agents do work
  -> durable evidence goes to agent-wiki/sources/ or host results/
  -> host agent runs /wiki-scan or scan_changes.py
  -> wiki-curator distills compact truth
  -> /wiki-lint keeps memory clean
```

The point is not to stop agents from writing. The point is to keep raw work,
structured state, and current truth in separate places.

## Continue With OpenCode

For the detailed two-agent OpenCode pattern, command list, and memory-rule
injection workflow, continue to [OpenCode Workflow](opencode-workflow.md).
