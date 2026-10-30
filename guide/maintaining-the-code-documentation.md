# Maintaining the Code Documentation

This guide covers how Django News's code documentation is set up, and how
to keep it up to date: adding Python files, changing the front page, and
rebuilding the pages.

## Contents

- [Sphinx, the Python Documentation Generator](#sphinx-the-python-documentation-generator)
- [How Sphinx Finds the Docstrings](#how-sphinx-finds-the-docstrings)
- [Adding a New Python File](#adding-a-new-python-file)
- [Adding a New App](#adding-a-new-app)
- [Changing the Front Page](#changing-the-front-page)
- [Rebuilding the Pages](#rebuilding-the-pages)

## Sphinx, the Python Documentation Generator

[Sphinx](https://www.sphinx-doc.org/) is free, open-source software that
creates documentation from the docstrings in a program's source code.
Django News's code documentation is built with it.

## How Sphinx Finds the Docstrings

The documentation's pages are laid out in `.rst` files, in `docs/source`.
An `.rst` file is written in reStructuredText, the markup language Sphinx
reads. Like Markdown, it is plain text, with marks for formatting: for
example, a title is underlined with a row of `=` signs. Sphinx's
[reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
explains how to write it:

```
https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
```

Each app has its own `.rst` page, such as
[`news.rst`](../docs/source/news.rst). Only the Python files listed on
these pages are documented. Each file must be added by hand, and a file
that is not listed is left out of the documentation, with no warning.

Each file is listed by one line, which names the file by its path, with
dots in place of the slashes and without `.py`:

```rst
.. automodule:: news.models
```

That line documents `news/models.py`, and every class and function in it
that has a docstring. Sphinx calls each Python file a *module*, which is
why the line says `automodule`.

Sphinx finds the classes and functions on its own, so they do not need
to be listed on the app's page. This is because of one setting in
[`docs/source/conf.py`](../docs/source/conf.py#L40-L47), made when Sphinx
was first set up for Django News. A second setting there shows them in
the order they appear in the code, instead of in alphabetical order. The
two settings are `"members"` and `"member-order"`, in lines 40 to 47 of
the file:

```python
# Document each module's classes and functions, in the order they
# appear in the source. Skip the exceptions that Django adds to every
# model, which are the same on each one.
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "exclude-members": "DoesNotExist, MultipleObjectsReturned, NotUpdated",
}
```

## Adding a New Python File

After adding a `.py` file to an app, add an `automodule` line for it to
the app's page. For example, a new file `news/feeds.py` needs this line in
`news.rst`:

```rst
.. automodule:: news.feeds
```

Then [rebuild the pages](#rebuilding-the-pages).

## Adding a New App

Each app has its own `.rst` page in `docs/source`, named after the app. A
new app needs one too, laid out like the existing ones. The `api` app's
page, [`docs/source/api.rst`](../docs/source/api.rst), is a short example:
a title, a line saying what the app is, and a heading and an
`automodule` line for each of its Python files:

```rst
API
===

The ``api`` app: the REST API for articles, with token
authentication.

api.serializers
---------------

.. automodule:: api.serializers

api.views
---------

.. automodule:: api.views
```

The new app's page must then be added to the front page's list of app
pages, in [`docs/source/index.rst`](../docs/source/index.rst), under
`.. toctree::`. Each page is listed by its file name without `.rst`, so
`api.rst` appears as `api`:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Apps:

   accounts
   news
   api
   third_party
```

A page left off this list is still built, but no other page links to it:
it is missing from the front page and the sidebar, and can be found only
through **Search docs** or by its address. Sphinx warns about it during
the build: `document isn't included in any toctree`.

Then [rebuild the pages](#rebuilding-the-pages).

## Changing the Front Page

The front page's introduction is not built from a docstring. It is written
in [`docs/source/index.rst`](../docs/source/index.rst). Edit the text under
the title, then [rebuild the pages](#rebuilding-the-pages).

## Rebuilding the Pages

After changing a docstring, the front page, or an app's page, rebuild the
pages so they include the change. Sphinx is installed with Django News's
Python packages, so rebuild them in the installed-directly version, with
the virtual environment active. The Docker image leaves out the `docs`
folder.

1. Move into the `docs` folder, from the `django-news-app` folder:

   ```bash
   cd docs
   ```

2. Delete the old pages:

   ```bash
   # On Windows, in Git Bash:
   ./make.bat clean
   ```

   ```bash
   # On macOS and Linux:
   make clean
   ```

3. Build them again:

   ```bash
   # On Windows, in Git Bash:
   ./make.bat html
   ```

   ```bash
   # On macOS and Linux:
   make html
   ```

4. Move back up to the `django-news-app` folder:

   ```bash
   cd ..
   ```

---

**The code documentation guides:**

- [Reading the Code Documentation](reading-the-code-documentation.md)
- [Creating Good Documentation with Sphinx](creating-good-documentation-with-sphinx.md)
- **Maintaining the Code Documentation** (this page)

[Back to the README](../README.md)
