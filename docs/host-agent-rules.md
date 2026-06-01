# Host Agent Memory Rules

Host agents are project-specific agents such as implementers, reviewers,
researchers, reporters, or planners. They are defined by the host project, not
bundled as active defaults inside `agent-wiki/`.

## Injection Model

Host agents that should contribute to project memory should include:

```text
{file:./agent-wiki/.opencode/host-agent-memory-rules.md}
```

The injector appends that prompt reference automatically.

## Default Injection

Inject all non-curator host agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root .
```

OpenCode:

```text
/wiki-inject-rules
```

## Selective Injection

Inject only selected agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py   --project-root .   --agent implementer   --agent reporter
```

OpenCode:

```text
/wiki-inject-rules --agent implementer --agent reporter
```

## Excluding Scratch Agents

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py   --project-root .   --exclude scratch
```

OpenCode:

```text
/wiki-inject-rules --exclude scratch
```

## Behavior After Injection

Injected host agents should ask a concise follow-up when meaningful durable
content may need memory tracking and the user did not already specify what to
preserve:

```text
Should I preserve this in agent-wiki project memory, or leave it only in the conversation?
```

If the user says yes, the host agent preserves evidence in the correct source
location and runs `/wiki-scan` or `scan_changes.py`. The curator then decides
what compact truth changes.

## Checking Coverage

```bash
python agent-wiki/scripts/wiki/check_host_agent_rules.py --project-root .
```

OpenCode:

```text
/wiki-check-rules
```
