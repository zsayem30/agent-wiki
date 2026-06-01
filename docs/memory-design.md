# Memory Design

`agent-wiki` is a memory subsystem for research coding projects. Its job is not
to store every thought. Its job is to preserve the smallest set of durable,
routable facts that lets future agents restart work without rereading the whole
project history.

The design assumes that agent context is expensive, stale conclusions are
harmful, and research projects branch often. It therefore separates raw evidence,
structured state, current truth, and active routing.

## System Model

```{mermaid}
flowchart LR
    User[User or project owner]
    Host[Host project agents]
    Sources[agent-wiki/sources<br/>long evidence]
    Results[Host results and artifacts]
    Inbox[knowledge/change_inbox.jsonl<br/>handoff queue]
    Curator[wiki-curator]
    Registries[knowledge/*.yaml<br/>structured state]
    Wiki[wiki/*.md<br/>compact truth]
    Future[Future agents]

    User --> Host
    Host --> Sources
    Host --> Results
    Host --> Inbox
    Inbox --> Curator
    Sources --> Curator
    Results --> Curator
    Curator --> Registries
    Curator --> Wiki
    Wiki --> Future
    Registries --> Future
```

The host project remains the place where code, experiments, figures, and paper
work happen. `agent-wiki/` is the memory layer that tells agents what matters,
where evidence lives, and which path to read next.

## Memory Surfaces

| Surface | Path | Primary reader | Update owner | Retention policy |
|---|---|---|---|---|
| Startup route | `wiki/START_HERE.md` | every agent | curator | tiny, stable, read first |
| Current truth | `wiki/CURRENT_STATE.md` | every active agent | curator | short, evidence-backed, no full history |
| Routing table | `wiki/ROUTING_TABLE.md` | task-specific agents | curator | maps task types to exact files |
| Topic hubs | `wiki/topics/*.md` | agents entering a domain | curator | compact synthesis plus source links |
| Active plan | `wiki/plans/active_plan.md` | implementers and planners | curator with user direction | current plan only |
| Open questions | `wiki/OPEN_QUESTIONS.md` | all agents | curator | unresolved uncertainty with owner/route |
| Project map | `wiki/PROJECT_MAP.md` | navigators and reviewers | generated, curator-reviewed | host tree overview |
| Source manifest | `knowledge/source_manifest.yaml` | curator and researchers | scripts plus curator | index of durable sources |
| Claim registry | `knowledge/claim_registry.yaml` | reporters/reviewers | curator | durable claims and evidence links |
| Experiment registry | `knowledge/experiment_registry.yaml` | implementers/reporters | curator | run cards and artifact paths |
| Paper registry | `knowledge/paper_registry.yaml` | research/report agents | curator/researcher | paper cards and relevance |
| Change inbox | `knowledge/change_inbox.jsonl` | curator | host agents/scripts | append-only handoff queue |
| Source material | `sources/` | curator on demand | user/host agents | long plans, papers, reports, debug logs |

The central invariant is that no single surface tries to do everything. Long
material can stay long because it is not part of default startup. Current truth
can stay short because provenance lives elsewhere.

## Evidence Promotion

`agent-wiki` uses a promotion path rather than letting conversation text become
canonical memory directly.

```{mermaid}
flowchart TD
    A[Conversation, implementation, research, or experiment] --> B{Durable?}
    B -- no --> Z[Leave in conversation or scratch notes]
    B -- yes --> C[Preserve evidence<br/>sources/ or host results/]
    C --> D[Append handoff<br/>knowledge/change_inbox.jsonl]
    D --> E[Curator reviews evidence]
    E --> F{Changes active truth?}
    F -- no --> G[Registry or source manifest only]
    F -- yes --> H[Update compact wiki]
    H --> I[Update routing table if future agents need a new path]
    H --> J[Update registries for claims, runs, papers, reports]
    I --> K[Run wiki lint]
    J --> K
```

A claim should not jump straight from a chat into `CURRENT_STATE.md`. The curator
should first ask: what evidence supports this, where is it preserved, how stable
is it, and which future agent needs it?

## What Agents Track

Agents should track different kinds of information at different levels of
durability.

| Information type | Example | Durable location | Why it is tracked |
|---|---|---|---|
| Current objective | active benchmark or paper goal | `wiki/CURRENT_STATE.md` | prevents agents from optimizing stale goals |
| Active plan | ordered implementation tasks | `wiki/plans/active_plan.md` | coordinates multi-session implementation |
| Claims | “method X improves metric Y under condition Z” | `knowledge/claim_registry.yaml` | separates evidence-backed claims from impressions |
| Experiments | run ID, command, config, result path, status | `knowledge/experiment_registry.yaml` | makes results discoverable without rereading logs |
| Literature | paper, relevance, key idea, caveats | `knowledge/paper_registry.yaml` and `sources/papers/` | supports related work and design decisions |
| Decisions | chosen architecture, rejected alternative, reopen gate | `sources/decisions/` plus topic hub summary | prevents repeating settled debates |
| Debug history | symptoms, root cause, fix, verification | `sources/reports/` or debug report template | keeps failure knowledge without bloating startup |
| Open questions | unresolved ambiguity or missing evidence | `wiki/OPEN_QUESTIONS.md` | gives future agents explicit uncertainty |
| Routes | task type to files to read | `wiki/ROUTING_TABLE.md` | limits context loading |

The wiki tracks *state*, not vibes. A useful entry normally has a timestamp,
status, source link, and a clear reason it matters to future work.

## Routing As Memory Compression

Routing is the main compression mechanism. Instead of asking every agent to read
all docs, `agent-wiki` gives each task a path.

```{mermaid}
flowchart TD
    Start[Agent starts task] --> Core[Read START_HERE, CURRENT_STATE, ROUTING_TABLE]
    Core --> Classify{What kind of task?}
    Classify -->|Implement| Impl[Read active plan + relevant topic hub + code route]
    Classify -->|Analyze result| Exp[Read experiment registry + run source/report]
    Classify -->|Research| Lit[Read idea/topic hub + paper registry + paper notes]
    Classify -->|Report| Report[Read current state + registries + dated reports]
    Classify -->|Curate| Curate[Read change inbox + routed evidence]
    Impl --> Work[Do focused work]
    Exp --> Work
    Lit --> Work
    Report --> Work
    Curate --> Work
    Work --> Handoff{Durable change?}
    Handoff -- yes --> Inbox[Append curator handoff]
    Handoff -- no --> Done[No wiki update]
```

The route lets the agent answer: “What is the smallest set of files I need to
read to do this task correctly?” That is why routing tables and topic hubs are
first-class documentation, not afterthoughts.

## Current Truth Rules

`wiki/CURRENT_STATE.md` should answer five questions:

1. What is the project trying to do now?
2. What is currently believed to be true?
3. What has been verified?
4. What is blocked, uncertain, or pending?
5. What should the next agent do first?

It should not contain:

- full experiment logs;
- raw brainstorms;
- copied papers;
- long implementation plans;
- stale claims without status labels;
- details that only matter to one closed branch.

When a topic grows too large, the curator should split it into a topic hub,
archive closed branches in `sources/`, and keep only the current operational
summary in `CURRENT_STATE.md`.

## Failure Modes The Design Prevents

| Failure mode | Design response |
|---|---|
| Markdown sprawl | Separate compact wiki, structured registries, and long sources. |
| Agents reread everything | Startup route plus routing table. |
| Stale conclusions survive | Status labels, open questions, superseded links, curator review. |
| Results become undiscoverable | Experiment registry points to run artifacts and reports. |
| Paper notes mix with implementation truth | Paper registry and `sources/papers/` stay separate from current truth. |
| Brainstorms become fake facts | Promotion requires preserved evidence and curator review. |
| Scratch agents pollute memory | Host-agent rule injection can exclude scratch agents. |
| Multi-agent work loses context | `change_inbox.jsonl` gives host agents a cheap handoff channel. |
