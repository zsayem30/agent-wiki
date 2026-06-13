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

The root `opencode.json` configures the built-in OpenCode `build` agent as a
host implementer and defines the `wiki-curator` agent. Project-specific research,
reporting, or domain agents should live in the host project, not inside
`agent-wiki/`.

Use `/contextualize` in Build mode to refresh compact implementer context from
`agent-wiki/wiki/START_HERE.md`, `agent-wiki/wiki/CURRENT_STATE.md`, and
`agent-wiki/wiki/ROUTING_TABLE.md`.

## Host Agent Memory Rules

The template already includes agent-wiki memory rules in the `build` agent. After
defining additional host agents in root `opencode.json`, inject the rules into
the agents that should contribute to project memory.

Default: all non-curator host agents.

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root .
```

Selective: only named agents.

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --agent implementer --agent reporter
```

Exclude scratch agents.

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --exclude scratch
```

The injector is idempotent; rerunning it will not duplicate the rules.
