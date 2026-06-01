# Agent-Wiki OpenCode Instructions

`agent-wiki/` is a curator-owned project memory subsystem. It is intended to be
used as a subfolder inside a host research project.

OpenCode should normally be launched from the host project root, using the root
`opencode.json` copied from `agent-wiki/templates/project-root/opencode.json`.
That root config points to this file and to `agent-wiki/.agents/wiki-curator.md`.

## Role Boundary

- The bundled `wiki-curator` maintains compact durable memory in
  `agent-wiki/wiki/` and structured state in `agent-wiki/knowledge/`.
- Host-project agents own implementation, debugging, tests, deep research, and
  paper/report generation.
- Long or raw material goes in `agent-wiki/sources/` or host-project `results/`.
- Current compact truth goes in `agent-wiki/wiki/`.
- Structured state goes in `agent-wiki/knowledge/`.

## Native Commands From Host Root

- `/context-curator`
- `/wiki-lint`
- `/wiki-scan`
- `/wiki-map`
- `/wiki-rollover`
- `/wiki-inject-rules`
- `/wiki-check-rules`

## Memory Rule

If a claim lacks evidence, record it in `agent-wiki/wiki/OPEN_QUESTIONS.md`
instead of promoting it to current truth.

## Host Agent Memory Rule Injection

Host-project agents that should contribute to project memory must include
`agent-wiki/.opencode/host-agent-memory-rules.md` in their prompt.

Default injection applies to all non-curator host agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root .
```

Selective injection:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --agent implementer --agent reporter
```

Scratch or disposable agents can be excluded:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --exclude scratch
```

Injected host agents should ask whether durable brainstorms, plans, debug
findings, implementations, research, or reports should be preserved when the
user has not already specified memory behavior.
