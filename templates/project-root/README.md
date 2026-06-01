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

## Host Agent Memory Rules

After defining host agents in root `opencode.json`, inject agent-wiki memory
rules into the agents that should contribute to project memory.

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
