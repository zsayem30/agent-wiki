# OpenCode Primary Instructions

OpenCode is the primary harness for this scaffold. `AGENTS.md` remains the
canonical project contract, and `opencode.json` wires the default OpenCode
agents and commands.

## Native OpenCode Flow

- Use `implementer` as the default primary agent for coding, debugging, tests,
  implementation plans, and code reviews.
- Switch to `wiki-curator` when compact project memory, registries, routes, or
  open questions need maintenance.
- Switch to `deep-research` for literature search, credible paper triage, paper
  cards, and related-work memos.
- Switch to `reporter` for dated, evidence-linked status reports and
  paper-prep reports.

## Startup Commands

Use these OpenCode commands at the start of a role session:

- `/context-implementer`
- `/context-curator`
- `/context-research`
- `/context-reporter`

Use these for maintenance:

- `/wiki-lint`
- `/wiki-scan`
- `/wiki-map`
- `/new-report <short title>`

## Memory Rule

Long or raw material goes in `sources/` or `results/`. Compact current truth
belongs in `wiki/`. Structured state belongs in `knowledge/`. If a claim lacks
evidence, record it in `wiki/OPEN_QUESTIONS.md` instead of promoting it to
current truth.
