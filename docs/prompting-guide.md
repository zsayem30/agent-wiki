# Prompting Guide

The user should not have to repeat memory hygiene instructions in every prompt.
Use the injector so host agents naturally ask about project memory when needed.
Every fenced block on this site has a copy button.

## First Curator Prompt

```text
/context-curator
You are the wiki-curator. Load the agent-wiki context, inspect only routed
startup files, and tell me what source material is needed before project memory
can be initialized. Do not bulk-read the host repo.
```

## Brainstorming

```text
Let's brainstorm this idea in the conversation. Do not write files yet. At the
end, summarize the strongest version of the idea, assumptions, open questions,
possible implementation tracks, and what should be preserved.
```

If the host agent has memory rules injected, it should ask whether to preserve
meaningful brainstorm output when the user did not specify.

## Implementation

```text
Please implement the next active plan item. Before editing, identify the route
from agent-wiki/wiki/ROUTING_TABLE.md. After editing, run focused verification
and leave a curator handoff if durable truth may have changed.
```

## Experiment Analysis

```text
Please analyze these results. Keep artifacts in host results/. Create or update
a run-card candidate for agent-wiki/knowledge/experiment_registry.yaml, preserve
long interpretation in agent-wiki/sources/reports/, and leave a curator handoff.
```

## Curator Review

```text
Please review the latest handoff. Update compact wiki truth only where evidence
supports a durable change. Put ambiguity in OPEN_QUESTIONS.md. Run /wiki-lint
before finishing.
```

## Scratch Work

For scratch sessions, say so explicitly:

```text
This is scratch exploration. Do not preserve it in project memory unless I ask.
```

Scratch agents can also be excluded from injection:

```text
/wiki-inject-rules --exclude scratch
```
