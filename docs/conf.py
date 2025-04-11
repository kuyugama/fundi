# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "FunDI"
copyright = "2025, Kuyugama"
author = "Kuyugama"
release = "0.0.8"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
html_sidebars = {"**": ["about.html", "navigation.html", "searchbox.html"]}
html_theme_options = {
    "github_user": "kuyugama",
    "github_repo": "fundi",
    "github_type": "star",
    "fixed_sidebar": True,
    "github_banner": True,
    "github_button": False,
    "logo": "FunDI.png",
    "extra_nav_links": {
        "Overview": "index.html",
        "Installation": "installation.html",
        "Basic Usage": "usage.html",
        "Advanced Usage": "advanced.html",
        "Testing": "testing.html",
        "API Reference": "api.html",
    },
}

myst_enable_extensions = ["colon_fence"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
