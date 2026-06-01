# agent-wiki

`agent-wiki` is a curator-owned project memory scaffold for research coding
projects. It is designed to live as an `agent-wiki/` subfolder inside a host
project, while the host project keeps its own code, experiments, results,
paper workspace, and root OpenCode configuration.

The first version focuses on OpenCode-native use:

- a root `opencode.json` template for host projects;
- one bundled active agent, `wiki-curator`;
- optional example prompts for host implementer/research/reporter agents;
- a memory-rule injector so host agents can preserve durable work and submit
  curator handoffs;
- compact wiki and structured registries to prevent Markdown sprawl.

```{toctree}
:maxdepth: 2
:caption: Start Here

installation
getting-started
opencode-workflow
prompting-guide
```

```{toctree}
:maxdepth: 2
:caption: Design

memory-design
project-layout
curator-workflow
host-agent-rules
```

```{toctree}
:maxdepth: 2
:caption: Reference

reference/scripts
reference/templates
readthedocs
faq
roadmap
```
