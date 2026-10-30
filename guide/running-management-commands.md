# Running Management Commands

A management command is a task run through Django's `manage.py`, such as
`migrate`, which builds the database's tables. This guide describes how any
management command is run, in both versions of Django News and on every
system. The other management command guides show only the shorter,
installed-directly form, described in
[How the Other Guides Show Commands](#how-the-other-guides-show-commands).

## Contents

- [Running a Command](#running-a-command)
- [How the Other Guides Show Commands](#how-the-other-guides-show-commands)
- [Getting Help With a Command](#getting-help-with-a-command)

## Running a Command

Run the command in the version of Django News that is installed. Follow
one option, not both. MariaDB must be running for any command that uses
the database.

### Option A: Django News Installed Directly

1. Move into the `django-news-app` folder:

   ```bash
   cd django-news-app
   ```

2. Activate the virtual environment:

   ```bash
   # On Windows, in Git Bash:
   source venv/Scripts/activate
   ```

   ```bash
   # On macOS and Linux:
   source venv/bin/activate
   ```

   The terminal's prompt should now start with `(venv)`. The virtual
   environment stays active until the terminal is closed.

3. Run the command, with its name in place of `<command>`:

   ```bash
   python manage.py <command>
   ```

   Inside the virtual environment, `python` works on every system,
   including macOS and Linux, where `python3` is needed outside it.

### Option B: Django News in Docker

1. Make sure the container is running. If it already is, this changes
   nothing:

   ```bash
   docker start django-news-app
   ```

2. Run the command from the terminal, with its name in place of
   `<command>`. `docker exec` runs it in the container:

   ```bash
   docker exec -it django-news-app python manage.py <command>
   ```

   The command is the same on every system, and needs no folder or
   virtual environment, because it runs in the container.

   The `-it` connects the terminal to the command, so the command can ask the
   user questions and read the answers typed at the terminal. Some commands
   need it, such as `createsuperuser`, which asks for a username and
   password, and the commands that ask for `yes` before deleting anything.
   Without `-it`, those commands stop with an error before changing anything.
   Commands that ask nothing work with it too, so it is always included here.

## How the Other Guides Show Commands

The other management command guides show each command only in the
installed-directly form:

```bash
python manage.py <command>
```

For the Docker version, put `docker exec -it django-news-app` in front of
it. For example, this installed-directly command:

```bash
python manage.py migrate_all
```

is run in Docker as:

```bash
docker exec -it django-news-app python manage.py migrate_all
```

## Getting Help With a Command

To list every management command, Django's own and Django News's, grouped
by the app each comes from:

```bash
python manage.py help
```

To show what one command does, and the options it takes:

```bash
python manage.py help <command>
```

---

**The management command guides:**

- **Running Management Commands** (this page)
- [Factory Reset](factory-reset.md)
- [The Sample Data](the-sample-data.md)

[Back to the README](../README.md)
