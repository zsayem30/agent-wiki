# Read the Docs Setup

This repository includes a first-version Sphinx documentation site intended for
Read the Docs.

## Files

```text
agent-wiki/
|-- .readthedocs.yaml
`-- docs/
    |-- conf.py
    |-- requirements.txt
    `-- index.md
```

The build uses Sphinx with MyST Markdown, so most documentation can be written
as `.md` files.

## Local Build

Install requirements:

```bash
python -m pip install -r docs/requirements.txt
```

Build HTML:

```bash
python -m sphinx -b html docs docs/_build/html
```

Build with warnings treated as errors:

```bash
python -m sphinx -W -b html docs docs/_build/html
```

## Importing On Read The Docs

1. Push the repository to GitHub.
2. Import the repository on Read the Docs.
3. Ensure Read the Docs uses `.readthedocs.yaml` from the repository root.
4. Build the default branch.

The config pins a supported Ubuntu image and Python version and points Sphinx to
`docs/conf.py`.
