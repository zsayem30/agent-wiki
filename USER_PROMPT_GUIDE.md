# User Prompt Guide

This guide explains how to use `agent-wiki` with coding and research agents
without creating a new documentation mess.

The short rule:

```text
Ask agents to think freely, but ask them to store durable outputs deliberately.
Raw evidence goes in sources/ or results/. Compact truth goes in wiki/.
Structured state goes in knowledge/.
```

## First Session In A New Project

After cloning the scaffold, start with one implementer agent:

```text
Please read AGENTS.md, then run:
python scripts/wiki/contextualize.py --role implementer

After that, inspect sources/inbox/ and wiki/START_HERE.md. Do not bulk-read
all source documents. Tell me what context you need before implementation.
```

If you already have a plan or idea, put it in `sources/inbox/` first:

```text
I placed sources/inbox/implementation_plan.md and sources/ideas/idea.md.
Please register them with scripts/wiki/ingest_source.py, read them, and produce
a compact proposed active plan in the conversation. Do not update CURRENT_STATE
until we agree on the plan.
```

Then start a curator agent in another terminal:

```text
Please read AGENTS.md, then run:
python scripts/wiki/contextualize.py --role wiki-curator

You are responsible for keeping wiki/ and knowledge/ compact. Watch for source
documents, reports, code changes, experiment results, and handoffs. Distill
only verified or explicitly marked provisional project truth.
```

## Good Default Prompts

### Brainstorming

Use this when you are exploring an idea:

```text
Let's brainstorm this idea in the conversation. Do not write files yet.
At the end, summarize:
1. the strongest version of the idea;
2. assumptions;
3. open questions;
4. possible implementation tracks;
5. what should be preserved, if anything.
```

If the brainstorm becomes durable:

```text
Please convert the useful part into sources/ideas/<short_name>.md using the
research memo template. Then register it with ingest_source.py and leave a
curator handoff with scan_changes.py.
```

### Implementation Planning

Ask for a plan before code when the work is risky:

```text
Please write a detailed implementation plan in the conversation first. Include:
scope, files likely to change, expected behavior, tests, risks, rollback notes,
and what should be logged for the curator. Do not create a new file yet.
```

To preserve the plan:

```text
Please save this as sources/plans/<topic>_implementation_plan.md using the
implementation plan template, register it, and add a compact pointer in
wiki/plans/active_plan.md only if this is now the active plan.
```

### Coding And Debugging

For implementer agents:

```text
Please implement this change. Follow the implementer role contract. Before
editing, identify the relevant wiki route and files. After editing, run focused
tests. If project truth changed, write a source report or handoff for the
wiki-curator.
```

For debugging:

```text
Please debug this failure end to end. Keep transient exploration in the
conversation. If the diagnosis is durable, write
sources/reports/<date>_<topic>_debug_report.md with evidence, root cause,
fix, tests, and remaining risks. Then register it and leave a curator handoff.
```

### Code Review

```text
Please review this diff as the implementer/reviewer. Focus on bugs, behavioral
regressions, missing tests, and stale wiki implications. Findings first with
file/line references. If the review changes project truth, leave a curator
handoff instead of editing the wiki directly.
```

### Deep Research

Use this when you want papers:

```text
Please act as the deep-research agent. Search for credible papers relevant to
this idea. Prioritize primary sources, surveys, and papers with strong
implementation relevance. For each paper, capture citation metadata, link,
why it matters, limitations, and implementation hooks. Put the long research
memo in sources/reports/ and paper cards in sources/papers/ or
wiki/literature/ only after registration.
```

For related work:

```text
Please produce a related-work research memo. Separate foundational papers,
direct competitors, useful methods, and papers to cite only for context.
Do not claim a paper supports our method unless the evidence is clear.
```

### Experiment Results

```text
Please analyze these results. Create or update a run card in
knowledge/experiment_registry.yaml. Put detailed interpretation in
sources/reports/<date>_<run>_analysis.md. Then leave a curator handoff saying
whether CURRENT_STATE.md or any claims should change.
```

Avoid this:

```text
Write a new docs/report.md with everything.
```

Prefer this:

```text
Write the detailed evidence as a source report, update the run card, and let
the curator distill compact truth into the wiki.
```

### Reporter

Use the reporter when you need a paper-prep reference:

```text
Please act as the reporter. Generate a dated project report using
templates/report.md. It should summarize current status, code map, implemented
features, important experiments, verified claims, failed/superseded branches,
open questions, and evidence links. Store it in sources/reports/ and register
it in knowledge/report_registry.yaml.
```

A good reporter does not invent project truth. It cites:

- `wiki/CURRENT_STATE.md`;
- topic hubs;
- decisions;
- run cards;
- source reports;
- result paths;
- claim registry entries;
- code paths.

## Working With The Curator

The curator should be asked to distill, not to ideate freely:

```text
Please review knowledge/change_inbox.jsonl and recent source documents. Update
only compact wiki truth that is supported by evidence. If anything is ambiguous,
put it in wiki/OPEN_QUESTIONS.md instead of making a claim.
```

After a major implementation:

```text
Please run python scripts/wiki/scan_changes.py and summarize for the curator:
what changed, where the evidence is, whether current truth changed, which topic
hub might need an update, and what remains uncertain.
```

## Clean Memory Practices

### Do Not Promote Too Early

New ideas should usually start in the conversation or `sources/ideas/`.
Promote them to `wiki/CURRENT_STATE.md` only when they become active project
truth.

### Keep Current State Small

`wiki/CURRENT_STATE.md` should answer:

- What is the project doing now?
- What is the current active plan?
- What claims are currently believed?
- What experiments or branches matter now?
- What is the next action?

It should not contain full history.

### Use Closed Branches

When a topic is no longer active, ask the curator:

```text
Please close this branch. Add a closure summary, evidence, and reopen gate.
Move active log details to wiki/logs/closed/ if needed, and keep only a compact
pointer in the relevant topic hub.
```

### Split Long Logs

When an active log gets too long:

```text
Please run python scripts/wiki/rollover_logs.py --threshold 800. If a log
should split, create a closed or archive log and leave the newest active
entries in the active log.
```

### Demand Evidence Links

For every important conclusion, ask:

```text
Please add the evidence source: run card, result path, source report, decision,
paper, or code reference. If evidence is missing, mark it as an open question.
```

## Where User Files Should Go

| User Material | Put It Here |
|---|---|
| Starting implementation plan | `sources/plans/` or `sources/inbox/` |
| Fleshed-out research idea | `sources/ideas/` |
| Paper notes or converted PDFs | `sources/papers/` |
| Lab notes or external documents | `sources/external/` |
| One-off long report | `sources/reports/` |
| Experiment output files | `results/` |

Then run:

```bash
python scripts/wiki/ingest_source.py <path> --kind <kind>
```

## Anti-Patterns

Avoid prompts like:

```text
Create a new Markdown file for every idea we discussed.
```

```text
Summarize the whole project by rereading every file in docs/.
```

```text
Update CURRENT_STATE.md with all historical details.
```

```text
Treat this experimental result as final without comparing it to prior claims.
```

Better prompts:

```text
Keep the brainstorm in the conversation, then preserve only the decision and
open questions.
```

```text
Use ROUTING_TABLE.md to pick the smallest context route.
```

```text
Put detailed history in a source report and compact truth in the wiki.
```

```text
Mark this as provisional until the run card and evidence are verified.
```

## Practical Two-Terminal Pattern

Terminal 1:

```text
/contextualize --role implementer
Please implement the next active plan item. Keep evidence and tests focused.
```

Terminal 2:

```text
/contextualize --role wiki-curator
Please review handoffs and keep wiki/ compact. Do not do implementation work.
```

Optional Terminal 3:

```text
/contextualize --role reporter
Please generate a dated paper-prep status report from the current wiki,
registries, run cards, and source reports.
```

## Final Rule

Agents should be allowed to think in detail. The scaffold controls where that
thinking lands.

The durable chain is:

```text
Conversation -> sources/results -> registries -> compact wiki -> reports
```

When in doubt, preserve evidence in `sources/`, record uncertainty in
`OPEN_QUESTIONS.md`, and let the curator decide what becomes current truth.

