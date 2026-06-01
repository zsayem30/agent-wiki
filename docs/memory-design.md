# Memory Design

`agent-wiki` is built around a separation of memory surfaces.

## Why Separate Surfaces?

Research coding projects produce many kinds of information:

- ideas;
- implementation plans;
- literature notes;
- debugging reports;
- experiment results;
- outdated conclusions;
- paper-writing summaries.

If all of these become startup context, future agents waste time and inherit
stale assumptions. The scaffold separates raw evidence from current truth.

## Surfaces

| Surface | Path | Purpose |
|---|---|---|
| Compact wiki | `agent-wiki/wiki/` | What future agents should read first. |
| Structured knowledge | `agent-wiki/knowledge/` | Registries, manifests, claims, runs, handoffs. |
| Source material | `agent-wiki/sources/` | Long or raw material preserved as evidence. |
| Host outputs | `results/`, `figures/`, etc. | Generated artifacts owned by the host project. |
| Host config | `opencode.json`, `AGENTS.md` | Active project-level agent setup. |

## Promotion Path

```text
Conversation or host work
  -> source material or results
  -> curator handoff
  -> structured registry entries
  -> compact wiki truth
```

A claim should not jump straight from conversation into `CURRENT_STATE.md`
without evidence.

## Current Truth Is Small

`agent-wiki/wiki/CURRENT_STATE.md` should answer:

- What is the project doing now?
- What is currently believed?
- What is the active plan?
- What evidence matters?
- What is next?

It should not be a full history.

## Handoffs

`agent-wiki/knowledge/change_inbox.jsonl` is the handoff channel between host
agents and the curator. Handoffs are cheap and structured; the curator decides
what becomes durable compact truth.
