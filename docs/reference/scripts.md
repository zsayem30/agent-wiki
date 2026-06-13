# Script Reference

All scripts live in `agent-wiki/scripts/wiki/`.

## contextualize.py

Load a role-aware context pack:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

## scan_changes.py

Record a Git-aware curator handoff from host-project changes:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root . --truth-impact unknown --evidence <path-or-note>
```

Use `--dry-run` to inspect without writing. Useful metadata arguments include
`--commit`, `--verification`, `--suggested-route`, `--open-question`, and
`--no-event`.

## handoff_queue.py

Inspect or acknowledge queued handoffs:

```bash
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . next
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . list
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . ack <handoff_id> --status curated
```

Acknowledgements append status events instead of rewriting old handoff entries.

## watch_handoffs.py

Show or watch safe handoff wake-up events:

```bash
python agent-wiki/scripts/wiki/watch_handoffs.py --project-root . --once
python agent-wiki/scripts/wiki/watch_handoffs.py --project-root . --notify macos
```

The watcher prints summaries, can ring the terminal bell, and does not inject
text into another terminal by default.

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

```text
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
