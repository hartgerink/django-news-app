# Django News User Guide

Django News is a news website that brings together articles from news
publications and from independent journalists. Readers can subscribe to the
publications and journalists they follow, and are emailed each of their new
articles.

## How Django News Works

A complete tour of what Django News can do, role by role: from writing a
first article, through an editor's approval, to the email that lands in a
subscriber's inbox.

[How Django News Works](guide/how-django-news-works.md)

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
