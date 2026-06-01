# Host Project Integration Templates

Copy these files to the root of a project that contains `agent-wiki/` as a
subfolder.

Recommended host layout:

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

The root `opencode.json` defines only the `wiki-curator` agent. Project-specific
implementer, research, or reporting agents should live in the host project, not
inside `agent-wiki/`.
