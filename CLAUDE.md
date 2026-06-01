# Claude Code Notes

This directory is intended to live at `project/agent-wiki/`. OpenCode is the
primary harness, but Claude Code can still use the curator workflow.

From the host project root, load curator context with:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

Then follow:

1. host `AGENTS.md`, if present;
2. `agent-wiki/AGENTS.md`;
3. `agent-wiki/wiki/START_HERE.md`;
4. `agent-wiki/wiki/CURRENT_STATE.md`;
5. `agent-wiki/wiki/ROUTING_TABLE.md`;
6. `agent-wiki/.agents/wiki-curator.md`.

Do not bulk-read host `results/` or `agent-wiki/sources/`.
