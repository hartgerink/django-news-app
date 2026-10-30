# Django News User Guide

Django News is a news website that brings together articles from news
publications and from independent journalists. Readers can subscribe to the
publications and journalists they follow, and are emailed each of their new
articles.

## How the Django News Web Interface Works

A complete tour of what the Django News website can do, role by role: from
writing a first article, through an editor's approval, to the email that
lands in a subscriber's inbox.

[How the Django News Web Interface Works](guide/how-the-django-news-web-interface-works.md)

## How the Django News API Works

Django News also has a REST API, for programs that work with its articles:
listing them, writing them, and approving them, under the same rules as the
website.

[How the Django News API Works](guide/how-the-django-news-api-works.md)

## Setting Up the Required MariaDB Server

Django News keeps its users, publications, articles, and newsletters in
MariaDB, a database server that runs separately from the application and is
not included with it. Set it up once, before running Django News, by
installing it on the same computer.

[Setting Up MariaDB](guide/setting-up-mariadb.md)

## Setting Up the Django News App

Django News comes in two versions.

- **Installed directly:** Django News runs on your computer, in its own
  Python environment.

  [Installing Django News Directly](guide/installing-django-news-directly.md)

- **The Docker version:** Django News runs in a Docker container, with
  Python and its packages already inside. A good choice if you already use
  Docker on your computer.

  [Running Django News with Docker](guide/running-django-news-with-docker.md)

## Running the Unit Tests

Django News's unit tests check that the REST API follows the site's rules
for every role. Run them after changing the code.

[Running the Unit Tests](guide/running-the-unit-tests.md)

## The Code Documentation

The code documentation, built with Sphinx, describes Django News's
modules, classes, and functions, for anyone working on the code.

- **Reading It**

  Open the pages in a web browser with one command, and find your way
  around them.

  [Reading the Code Documentation](guide/reading-the-code-documentation.md)

- **Writing Good Docstrings**

  How docstrings become the pages, with an example from Django News for
  each kind of code: modules, classes, functions, methods, and constants.

  [Creating Good Documentation with Sphinx](guide/creating-good-documentation-with-sphinx.md)

- **Keeping It Up to Date**

  Add new Python files to the documentation, change its front page, and
  rebuild the pages after a change.

  [Maintaining the Code Documentation](guide/maintaining-the-code-documentation.md)
