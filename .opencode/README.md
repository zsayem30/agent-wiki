# OpenCode Usage

OpenCode agents should read `AGENTS.md` and the relevant `.agents/<role>.md`
file at startup.

Recommended startup:

```bash
python scripts/wiki/contextualize.py --role <role>
```

Use the same storage rules as Codex and Claude Code:

- raw or long material in `sources/`;
- compact truth in `wiki/`;
- structured registries in `knowledge/`;
- generated artifacts in `results/`.

