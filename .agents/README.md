# Agent Role Contracts

These role contracts are harness-neutral. Use them with Codex, Claude Code,
OpenCode, or any other agent runtime.

Default roles:

- `wiki-curator.md`
- `implementer.md`
- `deep-research.md`
- `reporter.md`

At startup, every agent should read:

1. `AGENTS.md`
2. `wiki/START_HERE.md`
3. `wiki/CURRENT_STATE.md`
4. `wiki/ROUTING_TABLE.md`
5. its role contract

Then run:

```bash
python scripts/wiki/contextualize.py --role <role>
```

