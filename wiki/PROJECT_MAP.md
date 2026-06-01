# Project Map

This file is generated or maintained by `agent-wiki/scripts/wiki/build_tree.py`
after `agent-wiki/` is installed inside a host project.

From the host project root, run:

```bash
python agent-wiki/scripts/wiki/build_tree.py --project-root .
```

or in OpenCode:

```text
/wiki-map
```

## Expected Host Layout

```text
project-name/
  opencode.json
  AGENTS.md
  src/
  experiments/
  results/
  figures/
  paper-wiki/
  agent-wiki/
```

## Directory Summary

| Path | Purpose |
|---|---|
| `agent-wiki/` | Curator-owned compact project memory subsystem. |
| `agent-wiki/wiki/` | Compact current truth, routing, topics, decisions, logs, open questions. |
| `agent-wiki/knowledge/` | Structured registries and handoff files. |
| `agent-wiki/sources/` | Raw or long user/agent source material. |
| `src/` | Host project source code, if present. |
| `experiments/` | Host experiment entrypoints, configs, or scripts, if present. |
| `results/` | Host generated experiment outputs, usually linked from run cards. |
| `figures/` | Host generated figures or paper artifacts. |
| `paper-wiki/` | Host paper-writing workspace, if present. |

## Curator Notes

Regenerate this file after the host project structure exists. Keep this map
compact; link to source files or topic hubs instead of pasting code.
