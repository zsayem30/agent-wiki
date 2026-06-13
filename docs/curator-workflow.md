# Wiki Curator Workflow

The `wiki-curator` is the only active agent bundled by default. It is a memory
maintainer, not a general implementer. Its job is to convert evidence and
handoffs into compact, routed, durable project memory.

## Curator Responsibilities

The curator owns these surfaces:

| Surface | Curator responsibility |
|---|---|
| `wiki/CURRENT_STATE.md` | keep active truth short, current, and evidence-backed |
| `wiki/ROUTING_TABLE.md` | tell future agents which files to read for each task |
| `wiki/topics/*.md` | maintain topic-level summaries with source links |
| `wiki/plans/active_plan.md` | keep the current plan synchronized with user intent |
| `wiki/OPEN_QUESTIONS.md` | preserve unresolved ambiguity explicitly |
| `knowledge/source_manifest.yaml` | index durable source material |
| `knowledge/project_graph.yaml` | track relationships among ideas, claims, runs, and docs |
| `knowledge/*_registry.yaml` | keep claims, experiments, papers, ideas, and reports searchable |
| `knowledge/change_inbox.jsonl` | consume host-agent handoffs |
| `knowledge/events.jsonl` | inspect handoff wake-up and status events |

The curator does not own host implementation, experiment execution, or paper
writing unless the user explicitly asks it to leave its role.

## Startup Sequence

```{mermaid}
sequenceDiagram
    participant User
    participant Curator as wiki-curator
    participant Route as wiki startup route
    participant Inbox as change_inbox.jsonl
    participant Wiki as compact wiki

    User->>Curator: /context-curator
    Curator->>Route: read START_HERE, CURRENT_STATE, ROUTING_TABLE
    Curator->>Inbox: run /wiki-review-next or inspect pending handoffs if task asks for curation
    Curator->>Wiki: identify relevant topic hubs only
    Curator-->>User: summarize state, routes, pending curation work
```

The curator should begin with the compact route. It should not bulk-read
`sources/`, host `results/`, or the entire repository unless the routing table or
user task justifies that extra context.

## Handoff Consumption

Host agents leave handoffs because they should not need to understand the whole
wiki structure while implementing or researching. The curator turns those
handoffs into durable memory.

```{mermaid}
flowchart TD
    H[Read next inbox entry] --> V{Evidence available?}
    V -- no --> Q[Add or update OPEN_QUESTIONS.md]
    V -- yes --> C[Classify change]
    C --> T{Type}
    T -->|source only| M[Update source_manifest.yaml]
    T -->|experiment| E[Update experiment_registry.yaml]
    T -->|claim| R[Update claim_registry.yaml]
    T -->|paper| P[Update paper_registry.yaml]
    T -->|current truth| W[Update CURRENT_STATE.md]
    W --> RT{Future route changed?}
    RT -- yes --> Route[Update ROUTING_TABLE.md]
    RT -- no --> L[Run lint]
    M --> L
    E --> L
    R --> L
    P --> L
    Q --> L
    Route --> L
```

A good handoff review asks:

1. What changed?
2. What evidence supports the change?
3. What verification was run, if any?
4. Is the change current truth, historical provenance, or only a source index?
5. Which future task should be routed to this information?
6. Did any previous claim become stale or superseded?
7. Does ambiguity need an open question?

## Curation Decision Rules

| Condition | Action |
|---|---|
| New evidence supports active project truth | update `CURRENT_STATE.md` and link evidence |
| New material is useful but not active truth | register source and route through a topic hub |
| Experiment produced artifacts | add or update run card in `experiment_registry.yaml` |
| A claim is made | record claim with evidence, status, and caveats |
| A result contradicts current truth | update current truth and mark old claim superseded |
| A topic is too large | split into topic hub plus source links |
| A branch is closed | summarize closure, archive long details, add reopen gate |
| Evidence is missing | add `OPEN_QUESTIONS.md` entry instead of guessing |

The curator is allowed to be conservative. Under-documenting a weak claim is
better than promoting it into startup context.

## Registry Update Pattern

```{mermaid}
flowchart LR
    Evidence[Evidence link] --> Entry[Registry entry]
    Entry --> Status[Status: planned, active, verified, failed, superseded]
    Entry --> Owner[Owner or agent role]
    Entry --> Timestamp[Reviewed timestamp]
    Entry --> Route[Relevant route/topic]
    Entry --> Summary[One-screen summary]
```

Every registry entry should be enough for an agent to decide whether to open the
source. It should not duplicate the full source.

## Before Finishing

Before handing control back, the curator should run:

```bash
python agent-wiki/scripts/wiki/lint.py
```

A clean curator response should include:

- which wiki or registry files changed;
- which evidence justified the change;
- which routes future agents should use;
- which uncertainty remains unresolved;
- whether lint passed.
