# Host Agent Memory Rules

Host agents are project-specific agents such as implementers, reviewers,
researchers, reporters, planners, or paper-writing assistants. They are defined
by the host project, not bundled as active defaults inside `agent-wiki/`.

The memory-rule system makes those host agents cooperate with the wiki without
forcing every agent to become a curator.

## Injection Model

Host agents that should contribute to project memory include this prompt
reference in `opencode.json`:

```text
{file:./agent-wiki/.opencode/host-agent-memory-rules.md}
```

The injector appends that reference automatically to selected OpenCode agent
prompts.

```{mermaid}
flowchart LR
    Config[host opencode.json] --> Injector[inject_host_agent_rules.py]
    Rules[host-agent-memory-rules.md] --> Injector
    Injector --> Agents[host agent prompts]
    Agents --> Behavior[ask, preserve, hand off]
    Behavior --> Inbox[knowledge/change_inbox.jsonl]
    Inbox --> Curator[wiki-curator]
```

The injected rules do not make host agents edit the compact wiki directly. They
make host agents notice durable material and leave the curator enough context to
process it.

## Default Injection

Inject all non-curator host agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root .
```

OpenCode:

```text
/wiki-inject-rules
```

This is appropriate when most host agents are expected to do serious project
work.

## Selective Injection

Inject only selected agents:

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --agent implementer --agent reporter
```

OpenCode:

```text
/wiki-inject-rules --agent implementer --agent reporter
```

Use selective injection when some agents are intentionally scratch, exploratory,
or unsafe to let near durable memory.

## Excluding Scratch Agents

```bash
python agent-wiki/scripts/wiki/inject_host_agent_rules.py --project-root . --exclude scratch
```

OpenCode:

```text
/wiki-inject-rules --exclude scratch
```

Scratch agents can still do useful work, but they should not pollute project
memory unless the user explicitly asks for preservation.

## Behavior After Injection

Injected host agents follow a simple decision loop:

```{mermaid}
flowchart TD
    Work[Agent does task] --> D{Durable project memory?}
    D -- user already specified --> P[Preserve as requested]
    D -- no --> S[Leave in conversation or scratch files]
    D -- unclear --> A[Ask concise follow-up]
    A -->|preserve| P
    A -->|do not preserve| S
    P --> E[Write source/report/result reference]
    E --> H[Run wiki-scan or scan_changes.py]
    H --> C[Curator handles compact wiki update]
```

The default follow-up should be short:

```text
Should I preserve this in agent-wiki project memory, or leave it only in the conversation?
```

If the user says yes, the host agent should preserve evidence in the correct
source location and run `/wiki-scan` or `scan_changes.py` with explicit
`--truth-impact`, `--evidence`, and, when available, `--verification` details.

## What Host Agents Should Preserve

| Session output | Preserve where | Handoff summary should include |
|---|---|---|
| implementation plan | `sources/inbox/` or `sources/plans/` | scope, assumptions, next step |
| debug investigation | `sources/reports/` | symptom, root cause, fix, verification |
| experiment result | host `results/` plus registry candidate | run path, command/config, status, key metric |
| literature notes | `sources/papers/` plus paper card | citation, relevance, caveats |
| design decision | `sources/decisions/` | decision, alternatives, reopen gate |
| project status report | `sources/reports/` | date, scope, evidence links |
| new uncertainty | `OPEN_QUESTIONS.md` handoff | question, why it blocks work, likely route |

Host agents should not paste long logs into `CURRENT_STATE.md`. They should
preserve the evidence and let the curator summarize.

## Checking Coverage

```bash
python agent-wiki/scripts/wiki/check_host_agent_rules.py --project-root .
```

OpenCode:

```text
/wiki-check-rules
```

The checker reports which agents include the memory rules and which are missing
them. If an agent is missing by design, exclude it explicitly so future users do
not interpret the gap as drift.

## Safety Properties

The injection design gives the project three useful safety properties:

- users can opt scratch agents out;
- host agents can preserve evidence without restructuring the wiki;
- the curator remains the final gate for compact truth.

That separation is what keeps multi-agent documentation useful instead of noisy.
