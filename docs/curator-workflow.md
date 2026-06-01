# Wiki Curator Workflow

The `wiki-curator` is the only active agent bundled by default.

## Responsibilities

The curator owns:

- compact current truth;
- routing;
- source manifests;
- claim, paper, experiment, report, and idea registries;
- open questions;
- branch closure summaries and reopen gates.

The curator does not own host implementation, experiment execution, or paper
writing unless the user explicitly asks it to leave its role.

## Startup

From the host project root:

```text
/context-curator
```

or:

```bash
python agent-wiki/scripts/wiki/contextualize.py --role wiki-curator --project-root .
```

## Handoff Review

After a host agent runs `/wiki-scan`, the curator should inspect:

```text
agent-wiki/knowledge/change_inbox.jsonl
```

Then it should answer:

1. Did active project truth change?
2. Is this only provenance?
3. Which topic hub should route to it?
4. Does a registry need updating?
5. Should uncertainty become an open question?

## Before Finishing

Run:

```bash
python agent-wiki/scripts/wiki/lint.py
```

A clean handoff should say what changed, what evidence supports it, and what
remains unresolved.
