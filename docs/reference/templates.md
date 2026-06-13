# Template Reference

Templates live in `agent-wiki/templates/`.

## Project Root Templates

```text
agent-wiki/templates/project-root/
|-- AGENTS.md
`-- opencode.json
```

Copy or merge these into the host project root.

## Optional Host Agent Examples

```text
agent-wiki/templates/optional-agents/
|-- deep-research.md
|-- implementer.md
`-- reporter.md
```

These are examples only. Host projects should adapt them to local code,
experiments, and paper goals.

## Source And Report Templates

| Template | Use |
|---|---|
| `source_doc_frontmatter.md` | Frontmatter for durable source docs. |
| `implementation_plan.md` | Detailed implementation plans. |
| `research_memo.md` | Literature or concept research memos. |
| `debug_report.md` | Debugging and audit reports. |
| `report.md` | Dated project status reports. |
| `paper_card.md` | Compact paper notes. |

## Structured Templates

| Template | Use |
|---|---|
| `claim.yaml` | Durable claim entries. |
| `run_card.yaml` | Experiment/run cards. |
| `handoff.json` | Manual Git-aware curator handoff shape with evidence, verification, truth impact, routes, and curator status. |
| `decision.md` | ADR-style decisions with reopen gates. |
| `log_entry.md` | Newest-first active log entries. |
| `topic.md` | Compact topic hubs. |
