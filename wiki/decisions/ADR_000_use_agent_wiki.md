# ADR 000: Use Agent Wiki Scaffold

Status: accepted

Date: TODO

## Context

The project needs a durable memory system for agents that avoids uncontrolled
Markdown sprawl.

## Decision

Use the `agent-wiki` structure:

- compact current truth in `wiki/`;
- structured registries in `knowledge/`;
- raw and long source material in `sources/`;
- generated artifacts in `results/`;
- harness-neutral role contracts in `.agents/`.

## Consequences

- Agents must route through the wiki before opening long sources.
- Durable claims need evidence.
- Long reports are preserved as source material rather than startup context.
- Wiki-curator role is responsible for distillation.

## Reopen Gate

Reconsider this decision only if the scaffold blocks normal project work or a
replacement memory system is adopted with stricter evidence and routing rules.

