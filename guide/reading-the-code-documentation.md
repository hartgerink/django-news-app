# Reading the Code Documentation

Django News's code documentation is a set of web pages that describe the
modules, classes, and functions in its code. Open them in your web browser in
one step.

## Open It from the Terminal

In the `django-news-app` folder, run the command for your system. The
documentation's front page opens in your web browser.

```bash
# On Windows, in Git Bash:
start docs/build/html/index.html
```

```bash
# On macOS:
open docs/build/html/index.html
```

```bash
# On Linux:
xdg-open docs/build/html/index.html
```

## Or Open It from Your Browser

Paste the address for your system into your browser's address bar.

These addresses assume Django News is in your home folder. Put your
username in place of `<your-username>`, and change the rest of the path if
you downloaded Django News somewhere else.

**Windows:**

```
file:///C:/Users/<your-username>/django-news-app/docs/build/html/index.html
```

**macOS:**

```
file:///Users/<your-username>/django-news-app/docs/build/html/index.html
```

**Linux:**

```
file:///home/<your-username>/django-news-app/docs/build/html/index.html
```

## Finding Your Way Around

- **The front page** links to one page for each of Django News's apps:
  Accounts, News, API, and Third party.
- **Each app's page** lists its Python files, and the classes and
  functions in them.
- **Search docs,** at the top of the sidebar, finds anything by name.
- **[source],** beside each entry, shows the code it describes. The links
  come from the `viewcode` extension, turned on in
  [`docs/source/conf.py`](../docs/source/conf.py#L33-L38) when Sphinx was
  first set up for Django News, in lines 33 to 38 of the file:

  ```python
  extensions = [
      # Builds pages from the docstrings in the project's modules.
      "sphinx.ext.autodoc",
      # Adds a link from each documented item to its highlighted source.
      "sphinx.ext.viewcode",
  ]
  ```

---

**The code documentation guides:**

- **Reading the Code Documentation** (this page)
- [Creating Good Documentation with Sphinx](creating-good-documentation-with-sphinx.md)
- [Maintaining the Code Documentation](maintaining-the-code-documentation.md)

[Back to the README](../README.md)
