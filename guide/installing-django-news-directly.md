# Installing Django News Directly

This guide walks you through installing Django News on your computer, in
its own Python environment, and starting it.

## Contents

- [What You Need](#what-you-need)
- [Getting Django News](#getting-django-news)
- [Installing the Python Packages](#installing-the-python-packages)
- [Configuring Django News](#configuring-django-news)
- [Preparing the Database](#preparing-the-database)
- [Creating a Superuser (Optional)](#creating-a-superuser-optional)
- [Starting Django News](#starting-django-news)
- [Stopping and Starting Again](#stopping-and-starting-again)

## What You Need

| Requirement | Details |
|---|---|
| **MariaDB** | Set up as described in [Setting Up MariaDB](setting-up-mariadb.md), and running |
| **Python** | Version 3.13 or later |
| **Git** | To download Django News |
| **A terminal** | Git Bash on Windows, or the terminal on macOS and Linux |

Run every command in this guide in the terminal.

## Getting Django News

Download Django News, then move into its folder. Run the rest of the
commands in this guide from that folder.

```bash
git clone https://github.com/hartgerink/django-news-app.git
```

```bash
cd django-news-app
```

## Installing the Python Packages

Django News's Python packages are installed in a virtual environment, a
folder named `venv` that keeps them separate from the rest of your computer.

Create the virtual environment. On macOS and Linux, use `python3` in place
of `python`.

```bash
python -m venv venv
```

Activate it. On Windows:

```bash
source venv/Scripts/activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

The terminal's prompt should now start with `(venv)`. Activate the virtual
environment again in every new terminal you use for Django News.

Then install the packages. On macOS and Linux, first install the files the
`mysqlclient` package needs to build, following
[mysqlclient's install instructions](https://github.com/PyMySQL/mysqlclient#install)
for your system.

```bash
pip install -r requirements.txt
```

## Configuring Django News

Django News reads its settings, including its passwords, from a file named
`.env`. Create it from the example file:

```bash
cp .env.example .env
```

Generate a secret key, a long random string that Django uses to keep logins
secure:

```bash
openssl rand -hex 32
```

Open `.env` in a text editor, and replace the values in angle brackets:

| Setting | Value |
|---|---|
| `DJANGO_SECRET_KEY` | The key you just generated |
| `DB_USER` | `administrator` |
| `DB_PASSWORD` | The `administrator` user's password, from [Setting Up MariaDB](setting-up-mariadb.md) |
| `THIRD_PARTY_API_KEY` | Any text you choose |

Write each value as it is, with no quotes and no spaces around `=`. Leave
the other settings as they are.

## Preparing the Database

These steps expect MariaDB to be set up as described in
[Setting Up MariaDB](setting-up-mariadb.md), and running.

Create Django News's tables in the database:

```bash
python manage.py migrate_all
```

Create the four roles, Reader, Journalist, Editor, and Publisher, with
their rights. Users cannot register until the roles exist.

```bash
python manage.py setup_groups_and_permissions
```

If either command shows "Can't connect to server on 'localhost'", Django
News cannot reach MariaDB. Check that MariaDB is running.

## Creating a Superuser (Optional)

A superuser can log in to the Django admin at
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). Django News
works without one. The command asks you to choose a username, an email
address, and a password. On the site itself, the superuser has the Reader
role.

```bash
python manage.py createsuperuser
```

## Starting Django News

Start Django News:

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
You should see the Welcome page. Register an account to start using the site.

The terminal shows Django News's output while it runs, including the emails
it would send.

## Stopping and Starting Again

To stop Django News, press **Ctrl+C** in the terminal where it runs.

To start it again later, open a terminal in the `django-news-app` folder,
make sure MariaDB is running, and activate the virtual environment. On
Windows:

```bash
source venv/Scripts/activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

Then start Django News:

```bash
python manage.py runserver
```

Your data stays in MariaDB, so there is nothing else to set up again.

---

**The setup guides:**

- [Setting Up MariaDB](setting-up-mariadb.md)
- **Installing Django News Directly** (this page)
- [Running Django News with Docker](running-django-news-with-docker.md)

[Back to the README](../README.md)
