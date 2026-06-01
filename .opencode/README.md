# OpenCode Usage

OpenCode is the primary harness, but its active `opencode.json` should live at
the host project root, not inside `agent-wiki/`.

Copy or adapt:

```text
agent-wiki/templates/project-root/opencode.json -> ./opencode.json
agent-wiki/templates/project-root/AGENTS.md -> ./AGENTS.md
```

Then start OpenCode from the host project root:

```bash
opencode
```

Use the native curator commands:

| Command | Purpose |
|---|---|
| `/context-curator` | Load the curator context pack from `agent-wiki/`. |
| `/wiki-lint` | Run `agent-wiki/scripts/wiki/lint.py`. |
| `/wiki-scan` | Record a handoff from host-project git changes. |
| `/wiki-map` | Regenerate `agent-wiki/wiki/PROJECT_MAP.md` from the host project tree. |
| `/wiki-rollover` | Check whether active logs should split or close. |

Project-specific implementer, deep-research, or reporter agents should be
defined in the host project root. Optional example prompts live in
`agent-wiki/templates/optional-agents/`.
