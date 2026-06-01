# Documentation Source

This directory contains the Sphinx/MyST documentation source for the
`agent-wiki` Read the Docs site.

Build locally with:

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -b html docs docs/_build/html
```

Read the Docs uses `.readthedocs.yaml` at the repository root and
`docs/conf.py` as the Sphinx configuration.

Primary pages:

- `index.md`
- `getting-started.md`
- `installation.md`
- `opencode-workflow.md`
- `memory-design.md`
- `host-agent-rules.md`
- `prompting-guide.md`
- `reference/scripts.md`
- `reference/templates.md`
