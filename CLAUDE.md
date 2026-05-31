# Claude Code Instructions

This project uses the `agent-wiki` scaffold.

Claude Code agents should treat `AGENTS.md` as the canonical repository
contract, then load a role-specific context pack:

```bash
python scripts/wiki/contextualize.py --role <role>
```

Claude command shortcut:

```text
/contextualize --role implementer
/contextualize --role wiki-curator
/contextualize --role deep-research
/contextualize --role reporter
```

Role contracts live in `.agents/`.

Do not bulk-read `sources/` or `results/`. Route through:

1. `wiki/START_HERE.md`
2. `wiki/CURRENT_STATE.md`
3. `wiki/ROUTING_TABLE.md`
4. `.agents/<role>.md`

If project truth changes, update the appropriate source/registry/wiki surface
or leave a curator handoff in `knowledge/change_inbox.jsonl`.

