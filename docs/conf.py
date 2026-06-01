from __future__ import annotations

import os
from datetime import datetime

project = "agent-wiki"
author = "agent-wiki contributors"
copyright = f"{datetime.now().year}, {author}"
release = "0.1"

extensions = ["myst_parser"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "substitution",
    "tasklist",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

templates_path = ["_templates"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "agent-wiki"
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")

html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "sticky_navigation": True,
}
