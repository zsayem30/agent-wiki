# Codex Usage

Codex agents should use `AGENTS.md` as the canonical instruction file.

Start with:

```bash
python scripts/wiki/contextualize.py --role implementer
```

For other roles:

```bash
python scripts/wiki/contextualize.py --role wiki-curator
python scripts/wiki/contextualize.py --role deep-research
python scripts/wiki/contextualize.py --role reporter
```

Role contracts are in `.agents/`.

