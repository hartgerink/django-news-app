# Running Django News with Docker

This guide walks you through running Django News in a Docker container.
Python and Django News's packages are inside the container, so they do not
need to be installed on your computer.

## Contents

- [What You Need](#what-you-need)
- [Getting Django News](#getting-django-news)
- [Configuring Django News](#configuring-django-news)
- [Building the Image](#building-the-image)
- [Starting the Container](#starting-the-container)
- [Preparing the Database](#preparing-the-database)
- [Creating a Superuser (Optional)](#creating-a-superuser-optional)
- [Opening Django News](#opening-django-news)
- [Stopping and Starting Again](#stopping-and-starting-again)

## What You Need

| Requirement | Details |
|---|---|
| **MariaDB** | Set up as described in [Setting Up MariaDB](setting-up-mariadb.md), including [Letting Django News Connect](setting-up-mariadb.md#letting-django-news-connect), and running |
| **Docker** | Docker Desktop, or Docker Engine on Linux, and running |
| **Git** | To download Django News |
| **A terminal** | Git Bash on Windows, or the terminal on macOS and Linux |

This guide expects Docker to be installed already. If you are new to it,
Docker runs programs in containers: self-contained packages that hold a
program and everything it needs, so it runs the same way on any computer.
[Get Docker](https://docs.docker.com/get-started/get-docker/), Docker's own
guide, covers installing and setting it up on Windows, macOS, and Linux.

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

## Configuring Django News

Django News reads its settings, including its passwords, from a file named
`.env`. The container is given these settings when it starts. Create the
file from the example file:

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

## Building the Image

Build Django News's Docker image, named `django-news-app`. The `.` at the
end is the current folder, which holds Django News's files.

```bash
docker build -t django-news-app .
```

## Starting the Container

Start a container from the image. On Windows and macOS:

```bash
docker run -d --name django-news-app --env-file .env -e DB_HOST=host.docker.internal -p 8000:8000 django-news-app
```

On Linux:

```bash
docker run -d --name django-news-app --env-file .env -e DB_HOST=host.docker.internal --add-host=host.docker.internal:host-gateway -p 8000:8000 django-news-app
```

| Option | What it does |
|---|---|
| `-d` | Runs the container in the background |
| `--name django-news-app` | Names the container, so the commands below can refer to it |
| `--env-file .env` | Gives the container the settings in `.env` when it starts. The `.env` file itself is never copied into the image or the container. |
| `-e DB_HOST=host.docker.internal` | Points Django News at MariaDB on your computer |
| `--add-host=host.docker.internal:host-gateway` | Linux only. Lets the container find your computer, so it can reach MariaDB. Windows and macOS do not need it. |
| `-p 8000:8000` | Makes Django News reachable from your browser, on port 8000 |

## Preparing the Database

These steps expect MariaDB to be set up as described in
[Setting Up MariaDB](setting-up-mariadb.md), and running.

Create Django News's tables in the database:

```bash
docker exec django-news-app python manage.py migrate_all
```

Create the four roles, Reader, Journalist, Editor, and Publisher, with
their rights. Users cannot register until the roles exist.

```bash
docker exec django-news-app python manage.py setup_groups_and_permissions
```

If either command shows "Can't connect to server on
'host.docker.internal'", Django News cannot reach MariaDB. Check that
MariaDB is running, and see
[Letting Django News Connect](setting-up-mariadb.md#letting-django-news-connect).

## Creating a Superuser (Optional)

A superuser can log in to the Django admin at
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). Django News
works without one. The command asks you to choose a username, an email
address, and a password. On the site itself, the superuser has the Reader
role.

```bash
docker exec -it django-news-app python manage.py createsuperuser
```

The `-it` connects your terminal to the container, so you can answer the
command's questions.

## Opening Django News

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. You
should see the Welcome page. Register an account to start using the site.

The container's log shows Django News's output, including the emails it
would send:

```bash
docker logs django-news-app
```

## Stopping and Starting Again

Stop the container:

```bash
docker stop django-news-app
```

Make sure MariaDB is running, then start the container again later:

```bash
docker start django-news-app
```

Use `docker start`, not `docker run`: running `docker run` again fails,
because a container named `django-news-app` already exists.

Your data stays in MariaDB, so there is nothing else to set up again.

---

**The setup guides:**

- [Setting Up MariaDB](setting-up-mariadb.md)
- [Installing Django News Directly](installing-django-news-directly.md)
- **Running Django News with Docker** (this page)

[Back to the README](../README.md)
