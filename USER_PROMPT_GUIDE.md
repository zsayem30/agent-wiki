# User Prompt Guide

This guide explains how to use `agent-wiki/` as a subfolder in an OpenCode or
Codex research project without creating documentation sprawl.

The short rule:

```text
Host agents do the work. agent-wiki curates the memory.
Raw evidence goes in agent-wiki/sources/ or host results/.
Compact truth goes in agent-wiki/wiki/. Structured state goes in agent-wiki/knowledge/.
```

## First Setup

From the host project root:

```bash
git clone https://github.com/zsayem30/agent-wiki agent-wiki
cp agent-wiki/templates/project-root/opencode.json ./opencode.json
cp agent-wiki/templates/project-root/AGENTS.md ./AGENTS.md
opencode
```

If `opencode.json` or `AGENTS.md` already exists, merge the template sections.

For Codex-only projects, `opencode.json` is optional. Keep or merge the root
`AGENTS.md` instructions so Codex starts from the host root and follows the
agent-wiki startup route.

```bash
git clone https://github.com/zsayem30/agent-wiki agent-wiki
cp agent-wiki/templates/project-root/AGENTS.md ./AGENTS.md
```

If the host already has `AGENTS.md`, merge the startup and handoff sections
instead of overwriting it.

## Inject Memory Rules Into Host Agents

After you define project-specific agents in root `opencode.json`, inject
agent-wiki memory behavior into the agents that should preserve durable work.

Default: all non-curator host agents.

```text
/wiki-inject-rules
```

Selective: only agents you name.

```text
/wiki-inject-rules --agent implementer --agent deep-research
```

Exclude scratch agents.

```text
/wiki-inject-rules --exclude scratch
```

Injected agents will ask whether meaningful brainstorms, plans, implementations,
debug findings, experiment analyses, or reports should be preserved if you did
not already specify that.

## Start The Curator

Inside OpenCode from the host root:

```text
/context-curator
```

Good first prompt:

```text
You are the wiki-curator. Load the agent-wiki context, inspect only routed
startup files, and tell me what source material is needed before project memory
can be initialized. Do not bulk-read the host repo.
```

Codex equivalent:

```text
You are the wiki-curator. Follow the host AGENTS.md if present, then
agent-wiki/AGENTS.md. Run:

python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .

Inspect only routed startup files and tell me what source material is needed
before project memory can be initialized. Do not bulk-read the host repo.
```

## Add Starting Material

Put user material in:

```text
agent-wiki/sources/inbox/implementation_plan.md
agent-wiki/sources/ideas/idea.md
agent-wiki/sources/papers/paper1.md
```

Then prompt:

```text
Please register these source files with agent-wiki/scripts/wiki/ingest_source.py.
Distill a compact project overview, active plan, and open questions. Keep long
source content in sources/ and put only current truth in wiki/.
```

## Working With Host Agents

Your host project can define any implementer, research, or reporter agents it
needs. After durable work, ask them:

```text
Please leave an agent-wiki curator handoff. Run /wiki-scan or
python agent-wiki/scripts/wiki/scan_changes.py --project-root . --truth-impact unknown
--evidence <path-or-note> and summarize what changed, where evidence lives,
what verification ran, and whether current truth may need updating.
```

For Codex, use the same protocol with explicit shell commands instead of
OpenCode slash commands:

```text
You are a host-project implementer using agent-wiki for memory. Run:

python agent-wiki/scripts/wiki/contextualize.py --role implementer --project-root . --max-lines 180

Choose the smallest route from agent-wiki/wiki/ROUTING_TABLE.md before opening
long sources. After durable work, run:

python agent-wiki/scripts/wiki/scan_changes.py --project-root . --truth-impact unknown --evidence <path-or-note>

Include verification, suggested routes, and open questions when useful.
```

Then ask the curator:

```text
Please review the latest handoff. Update agent-wiki/wiki and agent-wiki/knowledge
only where evidence supports a durable change. Put ambiguity in OPEN_QUESTIONS.md.
Run /wiki-lint before finishing.
```

## Brainstorming

```text
Let's brainstorm this idea in the conversation. Do not write files yet. At the
end, summarize the strongest version of the idea, assumptions, open questions,
possible implementation tracks, and what should be preserved.
```

If the brainstorm becomes durable:

```text
Please preserve the useful part in agent-wiki/sources/ideas/<short_name>.md,
register it, and leave a curator handoff. Do not promote it to CURRENT_STATE
until the curator reviews it.
```

## Implementation Planning

```text
Please write a detailed implementation plan in the conversation first. Include
scope, files likely to change, expected behavior, tests, risks, rollback notes,
and what should be logged for the curator. Do not create a new file yet.
```

To preserve it:

```text
Please save this as agent-wiki/sources/plans/<topic>_implementation_plan.md,
register it, and ask the wiki-curator to distill only the active plan summary
into agent-wiki/wiki/plans/active_plan.md.
```

## Experiment Results

```text
Please analyze these results. Keep artifacts in host results/. Create or update
a run card in agent-wiki/knowledge/experiment_registry.yaml. Put detailed
interpretation in agent-wiki/sources/reports/<date>_<run>_analysis.md. Then
leave a curator handoff saying whether CURRENT_STATE.md or claims should change.
```

## Reports

Reports may live in host `paper-wiki/` or in `agent-wiki/sources/reports/`, but
they should cite compact wiki, registries, decisions, source reports, and result
paths.

```text
Please generate a dated project report from cited evidence only. Do not invent
project truth. After writing it, leave a curator handoff for any compact wiki
updates.
```

## Maintenance Commands

From OpenCode:

```text
/wiki-scan
/wiki-review-next
/wiki-watch
/wiki-lint
/wiki-map
/wiki-rollover
```

From the host shell:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role implementer --project-root . --max-lines 180
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
python agent-wiki/scripts/wiki/scan_changes.py --project-root . --truth-impact unknown --evidence <path-or-note>
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . next
python agent-wiki/scripts/wiki/watch_handoffs.py --project-root . --once
python agent-wiki/scripts/wiki/lint.py
python agent-wiki/scripts/wiki/build_tree.py --project-root .
```

## Anti-Patterns

Avoid:

```text
Create a new Markdown file for every idea we discussed.
Summarize the whole project by rereading every file.
Update CURRENT_STATE.md with all historical details.
Treat this experimental result as final without evidence.
```

Prefer:

```text
Keep brainstorming in the conversation, preserve durable evidence in sources/,
record uncertainty in OPEN_QUESTIONS.md, and let the curator decide what becomes
current truth.
```
