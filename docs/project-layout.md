# Project Layout

`agent-wiki` is designed as a subfolder memory subsystem. It does not own the
host project, and it should not become a parallel source tree. The host project
owns implementation artifacts; `agent-wiki/` owns durable agent memory.

## Host Repository Boundary

```{mermaid}
flowchart TB
    subgraph Host[Host research repository]
        Code[src/, experiments/, configs]
        Outputs[results/, figures/, checkpoints]
        Paper[paper-wiki/ or manuscript workspace]
        Config[opencode.json and AGENTS.md]
        subgraph Wiki[agent-wiki/]
            W[wiki/ compact truth]
            K[knowledge/ registries]
            S[sources/ long evidence]
            T[templates/ reusable scaffolds]
            Scripts[scripts/wiki/ tooling]
        end
    end

    Code --> Outputs
    Outputs --> K
    Paper --> S
    Config --> Scripts
    Scripts --> W
    Scripts --> K
    S --> W
```

This boundary matters because research projects need freedom to organize code
and experiments however the domain requires. The reusable part is the memory
protocol, not a universal source layout.

## Recommended Host Layout

```text
project-name/
|-- opencode.json          # active OpenCode config for this host project
|-- AGENTS.md              # host-level agent contract
|-- src/                   # implementation code
|-- experiments/           # experiment launchers, configs, analysis scripts
|-- results/               # generated outputs, logs, checkpoints, metrics
|-- figures/               # plots and paper-ready artifacts
|-- paper-wiki/            # optional manuscript and related-work workspace
`-- agent-wiki/            # memory subsystem
```

`opencode.json` lives at the host root because OpenCode configures the whole
project from there. `agent-wiki/` ships templates for that root config, but the
active file belongs to the host.

## agent-wiki Internal Layout

```text
agent-wiki/
|-- .agents/
|   `-- wiki-curator.md
|-- .opencode/
|   |-- instructions.md
|   `-- host-agent-memory-rules.md
|-- wiki/
|   |-- START_HERE.md
|   |-- CURRENT_STATE.md
|   |-- ROUTING_TABLE.md
|   |-- OPEN_QUESTIONS.md
|   |-- PROJECT_MAP.md
|   |-- plans/
|   `-- topics/
|-- knowledge/
|   |-- change_inbox.jsonl
|   |-- source_manifest.yaml
|   |-- project_graph.yaml
|   |-- claim_registry.yaml
|   |-- experiment_registry.yaml
|   |-- paper_registry.yaml
|   `-- report_registry.yaml
|-- sources/
|   |-- inbox/
|   |-- ideas/
|   |-- papers/
|   |-- reports/
|   |-- decisions/
|   `-- archive/
|-- templates/
`-- scripts/wiki/
```

## Ownership Model

| Area | Owner | Editable by | Notes |
|---|---|---|---|
| `src/`, `experiments/` | host project | implementers | normal research code workflow |
| `results/`, `figures/` | host project | experiment/report agents | generated artifacts, not startup context |
| `paper-wiki/` | host project | reporter/human | can cite `agent-wiki` reports and registries |
| `agent-wiki/wiki/` | wiki-curator | curator by default | compact current truth and routes |
| `agent-wiki/knowledge/` | wiki-curator | curator plus scripts | structured state and inbox |
| `agent-wiki/sources/` | user/agents | host agents and curator | long evidence preserved by type |
| `agent-wiki/templates/` | scaffold | scaffold maintainers | copied/adapted into host projects |
| `agent-wiki/scripts/wiki/` | scaffold | scaffold maintainers | context, lint, scan, map, injection tools |

Host agents may write sources and handoffs. The curator decides what becomes
compact truth.

## File Role Taxonomy

```{mermaid}
flowchart LR
    Raw[Raw or long material] --> Sources[sources/]
    Sources --> Manifest[source_manifest.yaml]
    Manifest --> Topic[wiki/topics/*.md]
    Topic --> Current[CURRENT_STATE.md]

    Runs[Experiment artifacts] --> Results[host results/]
    Results --> ExpReg[experiment_registry.yaml]
    ExpReg --> Current

    Claims[Evidence-backed claims] --> ClaimReg[claim_registry.yaml]
    ClaimReg --> Report[dated reports]
    ClaimReg --> Current

    Questions[Ambiguity] --> Open[OPEN_QUESTIONS.md]
    Open --> Routing[ROUTING_TABLE.md]
```

This taxonomy gives agents a predictable answer to “where should this go?” Raw
material goes to `sources/`; structured facts go to `knowledge/`; distilled
operational truth goes to `wiki/`.

## Why Not Put Everything In `docs/`?

A flat `docs/` directory tends to become a chronological pile. It is easy to add
a new Markdown file and hard for future agents to know whether that file is
current, superseded, evidence, speculation, or instructions.

`agent-wiki` replaces the pile with explicit surfaces:

- `wiki/` is small and read often;
- `knowledge/` is structured and machine-checkable;
- `sources/` is long and read only when routed;
- host outputs remain in the host project and are linked from registries.

The result is a documentation system that can grow without making startup
context grow at the same rate.
