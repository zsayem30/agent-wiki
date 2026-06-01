from __future__ import annotations

import os
from datetime import datetime

project = "agent-wiki"
author = "agent-wiki contributors"
copyright = f"{datetime.now().year}, {author}"
release = "0.1"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
]

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
html_js_files = ["theme-toggle.js"]
html_title = "agent-wiki"
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")
html_show_sourcelink = False

html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "sticky_navigation": True,
}

html_context = {
    "github_url": "https://github.com/zsayem30/agent-wiki",
}

copybutton_prompt_text = r"^(\$ |>>> |\.\.\. )"
copybutton_prompt_is_regexp = True
copybutton_remove_prompts = True
copybutton_copy_empty_lines = False
