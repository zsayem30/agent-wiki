# /contextualize

Load a role-aware context pack for this `agent-wiki` project.

Usage:

```text
/contextualize --role implementer
/contextualize --role wiki-curator
/contextualize --role deep-research
/contextualize --role reporter
```

Equivalent shell command:

```bash
python scripts/wiki/contextualize.py --role <role>
```

After running, follow `AGENTS.md` and `.agents/<role>.md`.

