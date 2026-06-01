# Script Reference

All scripts live in `agent-wiki/scripts/wiki/`.

## contextualize.py

Load a role-aware context pack:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

## scan_changes.py

Record a curator handoff from host-project Git changes:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root .
```

Use `--dry-run` to inspect without writing.

## ingest_source.py

Register a source file in `knowledge/source_manifest.yaml`:

```bash
python agent-wiki/scripts/wiki/ingest_source.py agent-wiki/sources/ideas/idea.md --kind idea
```

## lint.py

Check required scaffold files, links, JSONL, config JSON, and active log size:

```bash
python agent-wiki/scripts/wiki/lint.py
```

## build_tree.py

Regenerate `wiki/PROJECT_MAP.md` from the host project tree:

```bash
python agent-wiki/scripts/wiki/build_tree.py --project-root .
```

## rollover_logs.py

Check active logs for rollover:

```bash
python agent-wiki/scripts/wiki/rollover_logs.py --threshold 800
```

Use `--apply` to archive long logs.

## inject_host_agent_rules.py

Inject shared memory rules into host OpenCode agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root .
```

Useful options:

```bash
--agent implementer
--exclude scratch
--list
--check
--dry-run
```

## check_host_agent_rules.py

Thin checker wrapper around the injector:

```bash
python agent-wiki/scripts/wiki/check_host_agent_rules.py --project-root .
```

## timestamp.py

Emit a local ISO-8601 timestamp:

```bash
python agent-wiki/scripts/wiki/timestamp.py
```
