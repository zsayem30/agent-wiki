# Codex Usage

Codex can use `agent-wiki/` without OpenCode. Start Codex from the host project
root so it can see both host code and the `agent-wiki/` memory subsystem.

## Host Implementer Context

For implementation, debugging, research, reporting, or review work, start with:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role implementer --project-root . --max-lines 180
```

Then use `agent-wiki/wiki/ROUTING_TABLE.md` to choose the smallest useful
context. Do not bulk-read `agent-wiki/sources/` or host `results/`.

After durable work, leave a curator handoff:

```bash
python agent-wiki/scripts/wiki/scan_changes.py --project-root . \
  --summary "Short summary for the curator." \
  --truth-impact unknown \
  --evidence <path-or-note> \
  --verification "<command or check that ran>"
```

## Wiki Curator Context

For curation, ask Codex to act as `wiki-curator` and run:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

Then review queued handoffs as needed:

```bash
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . next
python agent-wiki/scripts/wiki/handoff_queue.py --project-root . show <handoff_id>
python agent-wiki/scripts/wiki/lint.py
```

The curator should update compact truth only when evidence supports it and put
uncertainty in `agent-wiki/wiki/OPEN_QUESTIONS.md`.

See `docs/codex-workflow.md` and `USER_PROMPT_GUIDE.md` for ready-to-use Codex
prompts.
