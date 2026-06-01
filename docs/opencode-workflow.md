# OpenCode Workflow

This page extends [Getting Started](getting-started.md) with the practical
OpenCode operating loop.

## Root Config Lives In The Host Project

The active OpenCode config should be at the host project root:

```text
project-root/
|-- opencode.json
`-- agent-wiki/
    `-- templates/project-root/opencode.json
```

The template points OpenCode to the curator prompt and project-memory
instructions inside `agent-wiki/`.

## Curator Commands

Use these commands inside OpenCode:

| Command | Purpose |
|---|---|
| `/context-curator` | Load the wiki-curator context pack. |
| `/wiki-scan` | Record a handoff from current host-project changes. |
| `/wiki-lint` | Run the wiki lint gate. |
| `/wiki-map` | Regenerate the host project map. |
| `/wiki-rollover` | Check whether active logs should split or close. |
| `/wiki-inject-rules` | Inject memory rules into host agents. |
| `/wiki-check-rules` | Check host-agent memory rule coverage. |

## Two-Agent Pattern

For serious work, use two OpenCode sessions:

```text
Terminal 1: host implementer, researcher, reporter, or reviewer
Terminal 2: wiki-curator
```

The host agent does the work. The curator maintains compact memory.

## Load Curator Context

```text
/context-curator
```

Equivalent terminal command:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

## Host Agent Injection

After defining host agents in `opencode.json`, inject memory rules:

```text
/wiki-inject-rules
```

This defaults to all non-curator host agents.

Selective injection:

```text
/wiki-inject-rules --agent implementer --agent reporter
```

Exclude scratch agents:

```text
/wiki-inject-rules --exclude scratch
```

Check coverage:

```text
/wiki-check-rules
```

Injected agents will ask whether durable session content should be preserved
when the user did not already specify memory behavior.

## Handoff From A Host Agent

When implementation, debugging, research, or analysis changes durable project
state, the host agent should run:

```text
/wiki-scan
```

Equivalent terminal command:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root . --summary "Short handoff summary."
```

The curator then reviews `agent-wiki/knowledge/change_inbox.jsonl` and updates
only the compact surfaces that changed.
