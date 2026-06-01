# FAQ

## Why is `opencode.json` not inside `agent-wiki/`?

OpenCode is launched from the host project root. The active config should live
there so it can configure all host agents and see the host project. `agent-wiki`
ships a root config template instead.

## Why only bundle `wiki-curator`?

Implementation, literature search, and reporting are project-specific. The
reusable part is memory hygiene and curation. Optional example prompts are
provided, but host projects should own their active agents.

## Can scratch agents skip memory rules?

Yes. Use:

```text
/wiki-inject-rules --exclude scratch
```

or selectively inject only the agents you want:

```text
/wiki-inject-rules --agent implementer --agent reporter
```

## Should host agents edit `CURRENT_STATE.md` directly?

Usually no. They should preserve evidence and leave a curator handoff. The
curator decides what compact truth changes.

## Where should long reports go?

Use `agent-wiki/sources/reports/` or a host paper/report area. The compact wiki
should link to the report and summarize only durable truth.
