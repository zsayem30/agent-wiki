# Installation

`agent-wiki` is installed as a subfolder inside a host repository. The host
repository owns the research code; `agent-wiki/` owns project memory.

## New Host Project

```bash
mkdir constrained-planning
cd constrained-planning
git init
git clone https://github.com/zsayem30/agent-wiki agent-wiki
cp agent-wiki/templates/project-root/opencode.json ./opencode.json
cp agent-wiki/templates/project-root/AGENTS.md ./AGENTS.md
```

After installation, the host project should look like this:

```text
constrained-planning/
|-- opencode.json
|-- AGENTS.md
|-- src/
|-- experiments/
|-- results/
|-- figures/
|-- paper-wiki/
`-- agent-wiki/
    |-- .agents/
    |-- .opencode/
    |-- wiki/
    |-- knowledge/
    |-- sources/
    |-- templates/
    `-- scripts/wiki/
```

Then start OpenCode from the host root:

```bash
opencode
```

## Existing Host Project

From the existing project root:

```bash
git clone https://github.com/zsayem30/agent-wiki agent-wiki
```

If the project does not already have OpenCode config:

```bash
cp agent-wiki/templates/project-root/opencode.json ./opencode.json
cp agent-wiki/templates/project-root/AGENTS.md ./AGENTS.md
```

If it already has `opencode.json`, merge these pieces manually:

- `instructions` entry for `agent-wiki/.opencode/instructions.md`;
- `wiki-curator` agent definition;
- `/context-curator`, `/wiki-scan`, `/wiki-lint`, `/wiki-map`,
  `/wiki-rollover`, `/wiki-inject-rules`, and `/wiki-check-rules` commands;
- bash permissions for `agent-wiki/scripts/wiki/*.py`.

## Optional Host Agents

`agent-wiki` bundles only `wiki-curator` as an active default. Host projects can
copy or adapt optional examples from:

```text
agent-wiki/templates/optional-agents/
```

Those examples are starting points only. Host agents should be domain-specific:
they should know the host codebase, test commands, paper goals, experiment
structure, and preferred model/provider choices.

## Update The Scaffold

If installed as a Git subfolder clone:

```bash
cd agent-wiki
git pull
```

Then return to the host root and run:

```bash
cd ..
python agent-wiki/scripts/wiki/lint.py
```

Continue with [Getting Started](getting-started.md) after the scaffold is in
place.
