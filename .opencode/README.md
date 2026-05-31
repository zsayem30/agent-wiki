# OpenCode Usage

OpenCode is the primary harness for this scaffold.

The root `opencode.json` defines:

- `implementer` as the default primary agent;
- `wiki-curator`, `deep-research`, and `reporter` as additional primary agents;
- project instructions in `.opencode/instructions.md`;
- native commands for context packs, linting, scans, map rebuilds, and reports;
- watcher ignores for generated or noisy directories.

## Start A Session

From the repository root:

```bash
opencode
```

Then run one of:

```text
/context-implementer
/context-curator
/context-research
/context-reporter
```

OpenCode can switch primary agents in the TUI with its normal agent-switching
controls. Use `implementer` for ordinary coding work and `wiki-curator` for
memory maintenance.

## Useful Commands

| Command | Agent | Purpose |
|---|---|---|
| `/context-implementer` | `implementer` | Load implementation/debugging context. |
| `/context-curator` | `wiki-curator` | Load curator context. |
| `/context-research` | `deep-research` | Load literature-search context. |
| `/context-reporter` | `reporter` | Load reporting context. |
| `/wiki-lint` | `wiki-curator` | Run `scripts/wiki/lint.py`. |
| `/wiki-scan` | `wiki-curator` | Append a change handoff to `knowledge/change_inbox.jsonl`. |
| `/wiki-map` | `wiki-curator` | Regenerate `wiki/PROJECT_MAP.md`. |
| `/new-report <title>` | `reporter` | Create a dated report scaffold. |

## Models

`opencode.json` intentionally does not set a model. OpenCode should inherit the
user's global provider/model configuration or a model selected in the TUI/CLI.
This keeps the scaffold portable across Anthropic, OpenAI/Codex, local, and
other OpenCode providers.

## Compatibility

Codex and Claude Code remain supported through `AGENTS.md`, `CLAUDE.md`, and
`.agents/`, but OpenCode is the first-class path.
