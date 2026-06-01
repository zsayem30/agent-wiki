# Agent Role Contracts

`agent-wiki` bundles only one active role by default: `wiki-curator`.

The host project should define its own implementer, deep-research, reporter,
or domain-specific agents in root-level OpenCode config or project instructions.
Optional examples are available in `templates/optional-agents/`, but they are
not active defaults.

At startup, the wiki-curator should read:

1. host-project `AGENTS.md`, if present;
2. `agent-wiki/AGENTS.md`;
3. `agent-wiki/wiki/START_HERE.md`;
4. `agent-wiki/wiki/CURRENT_STATE.md`;
5. `agent-wiki/wiki/ROUTING_TABLE.md`;
6. `agent-wiki/.agents/wiki-curator.md`.

Then run, from the host project root:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```
