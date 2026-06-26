# Codex Workflow

Codex can use `agent-wiki` without OpenCode. The difference is that Codex does
not consume the project-root `opencode.json` commands or agent definitions.
Instead, use `AGENTS.md` instructions, explicit prompts, and the same Python
helper scripts that OpenCode commands wrap.

## Start From The Host Root

Run Codex from the host project root:

```text
project-root/
|-- AGENTS.md
|-- src/
|-- results/
`-- agent-wiki/
```

Codex should read the host `AGENTS.md` first, then the agent-wiki startup route:

```text
agent-wiki/AGENTS.md
agent-wiki/wiki/START_HERE.md
agent-wiki/wiki/CURRENT_STATE.md
agent-wiki/wiki/ROUTING_TABLE.md
```

The helper command is:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role implementer --project-root . --max-lines 180
```

For curator work:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

## Two Codex Roles

Use the same role boundary as OpenCode:

| Role | Owns |
|---|---|
| Host implementer / researcher / reporter | Host code, experiments, reports, and long source material. |
| `wiki-curator` | Compact truth in `agent-wiki/wiki/` and structured state in `agent-wiki/knowledge/`. |

You can use one Codex session and explicitly switch roles, but two sessions are
cleaner for larger work:

```text
Terminal 1: Codex host implementer
Terminal 2: Codex wiki-curator
```

## Host Work Prompt

Use this when asking Codex to implement, debug, research, or analyze host work:

```text
You are a host-project implementer using agent-wiki for project memory.
Start by running:

python agent-wiki/scripts/wiki/contextualize.py --role implementer --project-root . --max-lines 180

Use agent-wiki/wiki/ROUTING_TABLE.md to choose the smallest useful context.
Do not bulk-read agent-wiki/sources/ or host results/. After durable work,
leave a curator handoff with scan_changes.py and include evidence, verification,
truth impact, suggested routes, and open questions.
```

After meaningful work, run:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root . \
  --summary "Short summary for the curator." \
  --truth-impact unknown \
  --evidence <path-or-note> \
  --verification "<command or check that ran>"
```

Set `--truth-impact yes`, `no`, or `unknown` explicitly.

## Curator Prompt

Use this when asking Codex to curate memory:

```text
You are the wiki-curator. Follow the host AGENTS.md if present, then
agent-wiki/AGENTS.md. Run:

python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .

Review only routed evidence. Update agent-wiki/wiki and agent-wiki/knowledge
only where evidence supports durable truth. Put ambiguity in
agent-wiki/wiki/OPEN_QUESTIONS.md. Run python agent-wiki/scripts/wiki/lint.py
before finishing.
```

To review queued handoffs:

```bash
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . next
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . show <handoff_id>
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . ack <handoff_id> --status curated
```

## Codex Branch Hygiene

For scaffold maintenance, keep `main` releasable and use a development branch
for experimental project-wiki work. A typical flow is:

```bash
git switch main
python scripts/wiki/lint.py
git push origin main
git switch -c dev
git push -u origin dev
```

When the scaffold is installed inside another host project, branch policy belongs
to the host project; `agent-wiki` only records evidence and curator handoffs.

## Codex Anti-Patterns

Avoid asking Codex to summarize the whole repository by reading every Markdown
file. Prefer a routed prompt:

```text
Read the startup route, choose the matching route from ROUTING_TABLE.md, and
open only the files needed for this task.
```

Avoid asking host-agent Codex sessions to edit `CURRENT_STATE.md` directly after
implementation. Prefer preserving evidence and leaving a handoff for a curator
review.
