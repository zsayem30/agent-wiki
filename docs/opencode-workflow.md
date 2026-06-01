# OpenCode Workflow

OpenCode is the primary harness for the first version of `agent-wiki`.

## Root Config Lives In The Host Project

The active OpenCode config should be at the host project root:

```text
project-root/opencode.json
```

The `agent-wiki/` repository ships a template at:

```text
agent-wiki/templates/project-root/opencode.json
```

This template points OpenCode to the curator prompt and project-memory
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
Terminal 1: host implementer/research/reporter agent
Terminal 2: wiki-curator
```

The host agent does the work. The curator maintains compact memory.

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
