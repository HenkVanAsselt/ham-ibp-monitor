# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path
# sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, str(Path('..', 'src').resolve()))
print(f"{sys.path=}")

project = 'HAM Beacon Monitor'
copyright = '2024, Henk van Asselt'
author = 'Henk van Asselt'
release = '0.2'

master_doc = 'index'    # This is the default.

autosummary_generate = True

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_click",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

autodoc_typehints = "description"
html_theme = "furo"
html_static_path = ['_static']

apidoc_modules = [
    {'path': '../src', 'generated_api_docs': 'source/'},
    {
        'path': 'path/to/another_module',
        'destination': 'source/',
        'exclude_patterns': ['**/test*'],
        'max_depth': 4,
        'follow_links': False,
        'separate_modules': False,
        'include_private': False,
        'no_headings': False,
        'module_first': False,
        'implicit_namespaces': False,
        'automodule_options': {
            'members', 'show-inheritance', 'undoc-members'
        },
    },
]