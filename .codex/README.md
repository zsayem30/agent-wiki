# Codex Usage

`agent-wiki/` bundles only the wiki-curator role. Host-project Codex agents
should use the host project instructions for implementation and use this
subfolder for memory handoff.

From the host project root:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

After durable work:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root .
```
