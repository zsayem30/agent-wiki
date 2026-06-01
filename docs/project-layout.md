# Project Layout

`agent-wiki` is not meant to own the host project. It is a memory subsystem.

## Recommended Host Layout

```text
project-name/
|-- opencode.json
|-- AGENTS.md
|-- src/
|-- experiments/
|-- results/
|-- figures/
|-- paper-wiki/
`-- agent-wiki/
```

## The agent-wiki Subfolder

```text
agent-wiki/
|-- .agents/
|   `-- wiki-curator.md
|-- .opencode/
|   |-- host-agent-memory-rules.md
|   `-- instructions.md
|-- wiki/
|-- knowledge/
|-- sources/
|-- templates/
`-- scripts/wiki/
```

## Host-Owned Areas

| Path | Owner | Notes |
|---|---|---|
| `src/` | Host project | Main source code. |
| `experiments/` | Host project | Experiment scripts/configs. |
| `results/` | Host project | Generated outputs linked from run cards. |
| `figures/` | Host project | Generated figures and paper artifacts. |
| `paper-wiki/` | Host project | Paper-writing workspace if desired. |
| `opencode.json` | Host project | Active OpenCode config. |

## Agent-Wiki-Owned Areas

| Path | Purpose |
|---|---|
| `wiki/` | Compact current truth and routing. |
| `knowledge/` | Registries and handoff files. |
| `sources/` | Long evidence and raw user/agent material. |
| `templates/` | Templates for source docs, host config, and optional agents. |
| `scripts/wiki/` | Context, lint, scan, map, and injection tools. |
