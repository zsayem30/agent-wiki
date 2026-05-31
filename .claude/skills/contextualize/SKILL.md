# Contextualize Skill

Use this skill when a Claude Code agent starts work in an `agent-wiki`
repository or switches roles.

Run:

```bash
python scripts/wiki/contextualize.py --role <role>
```

Valid roles:

- `implementer`
- `wiki-curator`
- `deep-research`
- `reporter`

Then follow:

1. `AGENTS.md`
2. `wiki/START_HERE.md`
3. `wiki/CURRENT_STATE.md`
4. `wiki/ROUTING_TABLE.md`
5. `.agents/<role>.md`

Do not bulk-read `sources/` or `results/`.

