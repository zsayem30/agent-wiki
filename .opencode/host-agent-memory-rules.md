# Agent-Wiki Host Agent Memory Rules

These rules apply to host-project agents that have opted into agent-wiki
project memory. They are intentionally written for implementer, research,
reporting, review, and planning agents outside `agent-wiki/`.

## Core Boundary

You do the host-project work. The `wiki-curator` owns durable compact memory in
`agent-wiki/`.

Do not directly bloat `agent-wiki/wiki/` with long plans, raw reports, full
experiment logs, or speculative brainstorms. Preserve evidence in the right
source location and leave a curator handoff.

## After Meaningful Work

After brainstorming, planning, implementation, debugging, code review, deep
research, experiment analysis, or report writing, decide whether durable
project memory may have changed.

If the user already specified what to preserve and where, follow that request.

If the user did not specify, ask one concise follow-up before ending the
session or moving on:

```text
Should I preserve this in agent-wiki project memory, or leave it only in the conversation?
```

Ask only when there is durable content worth preserving. Do not ask after tiny
status checks, purely transient exploration, failed dead-end commands with no
new diagnosis, or scratch work explicitly marked as scratch.

## If The User Says To Preserve It

Use this storage rule:

| Material | Destination |
|---|---|
| Starting idea, brainstorm, or research direction | `agent-wiki/sources/ideas/` |
| Implementation plan | `agent-wiki/sources/plans/` |
| Paper notes or literature memo | `agent-wiki/sources/papers/` or `agent-wiki/sources/reports/` |
| Debug, audit, analysis, or status report | `agent-wiki/sources/reports/` |
| Experiment outputs | host `results/`, with run-card handoff for `agent-wiki/knowledge/experiment_registry.yaml` |
| Ambiguity or unresolved claim | curator handoff for `agent-wiki/wiki/OPEN_QUESTIONS.md` |
| Current durable truth | curator handoff, not a long direct wiki edit |

Then run or ask to run from the host project root:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root . --truth-impact unknown --evidence <path-or-note>
```

Use repeated `--evidence`, `--verification`, `--suggested-route`, and
`--open-question` arguments when useful. Set `--truth-impact yes`, `no`, or
`unknown` explicitly instead of leaving the curator to infer it.

Summarize for the curator:

- what changed;
- where evidence lives;
- what verification was run, if any;
- whether current truth may need updating;
- which topic hub or registry may need review;
- what remains uncertain.

## If The User Says Not To Preserve It

Keep it in the conversation. Do not create source files, wiki updates, or
handoffs for that content.

## Evidence Discipline

Do not state or preserve a conclusion as project truth unless it has evidence:
source document, code reference, run card, result path, paper, decision record,
or dated report. If evidence is missing, mark it as an open question candidate.

## Existing User Instructions Win

If the user explicitly says not to update memory, not to write files, or that
the session is scratch, obey that.

If the user explicitly asks for a wiki update, source report, registry update,
or handoff, do it without asking the preservation follow-up.
