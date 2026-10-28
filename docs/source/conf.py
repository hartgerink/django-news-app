# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

import django

# -- Django setup ------------------------------------------------------
#
# Sphinx imports the project's modules to read their docstrings, and
# Django's models can only be imported once Django is set up. This file
# is in docs/source, so the project root, which holds manage.py, is two
# folders up. Django's settings read the project's .env file as usual.

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.insert(0, PROJECT_ROOT)
os.environ["DJANGO_SETTINGS_MODULE"] = "django_news.settings"
django.setup()

# -- Project information -----------------------------------------------

project = "Django News"
copyright = "2026, Kevin Hartgerink"
author = "Kevin Hartgerink"

# -- General configuration ---------------------------------------------

extensions = [
    # Builds pages from the docstrings in the project's modules.
    "sphinx.ext.autodoc",
    # Adds a link from each documented item to its highlighted source.
    "sphinx.ext.viewcode",
]

# Document each module's classes and functions, in the order they
# appear in the source. Skip the exceptions that Django adds to every
# model, which are the same on each one.
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "exclude-members": "DoesNotExist, MultipleObjectsReturned, NotUpdated",
}

exclude_patterns = []

language = "en"

# -- Options for HTML output -------------------------------------------

# The Read the Docs theme, installed from requirements.txt.
html_theme = "sphinx_rtd_theme"
