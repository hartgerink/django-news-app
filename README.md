# Django News

## Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Demo Accounts](#demo-accounts)
- [REST API](#rest-api)
- [Running the Tests](#running-the-tests)
- [Management Commands](#management-commands)
- [Project Structure](#project-structure)

## About

Django News is a news website built with Django. It brings together articles
from news publications and from independent journalists. Every article is
approved before readers can see it.

Every user has one of four roles, chosen when they register:

| Role | What they do |
|---|---|
| Reader | Reads articles and newsletters, and subscribes to publications and journalists. |
| Journalist | Writes articles and newsletters, independently or for the publications they work for. Approves their own independent articles. |
| Editor | Reviews, edits, approves, and deletes the articles and newsletters of the publications they work for. |
| Publisher | Creates publications, and chooses the editors and journalists who work for them. |

When an article is approved:

- It is emailed to the readers who subscribe to its publication, or, for an
  independent article, to its journalist.
- It is shared with a third-party service through that service's API. The
  third party is simulated within this project, by the `third_party` app.

Django News also has a REST API for articles, with token authentication.

## Prerequisites

- Python 3.13 or later.
- Git.
- MariaDB Server, installed directly or in Docker Desktop.
- Basic knowledge of the command line and Git.

The commands in this README are for Git Bash.

## Installation

1. **Get the project** by cloning the repository, then move into its folder,
   which contains `manage.py`:

   ```bash
   git clone https://github.com/hartgerink/django-news-app.git
   ```

   ```bash
   cd django-news-app
   ```

2. **Create the virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   ```bash
   source venv/Scripts/activate
   ```

   Activate it again in every new terminal before running the commands
   below.

4. **Install the required Python packages** into the virtual environment:

   ```bash
   pip install -r requirements.txt
   ```

   **Note:** `requirements.txt` installs Django 6.1.1, the version Django
   News is built and tested with. Older versions of Django are not
   supported.

## Database Setup

Django News stores its data in MariaDB. The database is not included in the
project and must be set up before the project is run. Follow one of the two
options below.

Either way, the database user also needs rights to a second database,
`test_news_db`. The unit tests create it each time they run, and delete it
afterward. Without these rights, the tests cannot run.

The steps below use `administrator` as the database user's name. You choose
the passwords yourself. Wherever `<your-database-password>` or
`<your-root-password>` appears, replace it, including the angle brackets,
with the password you chose. Keep the database user's password for
[Configuration](#configuration), where it goes in the `.env` file.

### Option A: MariaDB Installed Directly (Recommended)

1. **Install MariaDB Server.** Download it from
   [mariadb.org/download](https://mariadb.org/download/) and install it with
   the default settings. Choose a root password during installation, and
   keep the default port, 3306.

2. **Open the MariaDB command line**, using the "Command Prompt (MariaDB)"
   shortcut installed with MariaDB, and run the following command. Enter the
   root password when prompted.

   ```bash
   mariadb -u root -p
   ```

3. **Create the database and the database user** by pasting the following
   SQL into the MariaDB command line:

   ```sql
   CREATE DATABASE news_db CHARACTER SET utf8mb4;
   CREATE USER 'administrator'@'localhost' IDENTIFIED BY '<your-database-password>';
   GRANT ALL PRIVILEGES ON news_db.* TO 'administrator'@'localhost';
   GRANT ALL PRIVILEGES ON test_news_db.* TO 'administrator'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

### Option B: MariaDB in Docker Desktop (Alternative)

1. **Pull the MariaDB image.** In Docker Desktop, pull the LTS (Long Term
   Support) version of the MariaDB image, `mariadb:lts`.

2. **Create a container** from the image with the following settings:

   ```
   Container name ----------: news-mariadb
   Host port ---------------: 3306
   Host path ---------------: news_data
   Container path ----------: /var/lib/mysql
   MARIADB_ROOT_PASSWORD ---: <your-root-password>
   MARIADB_DATABASE --------: news_db
   MARIADB_USER ------------: administrator
   MARIADB_PASSWORD --------: <your-database-password>
   ```

3. **Start the container.** The database and the database user are created
   automatically from the settings above.

4. **Give the database user rights to the test database.** With the container
   running, run this command in Git Bash:

   ```bash
   docker exec news-mariadb sh -c 'mariadb -u root -p"$MARIADB_ROOT_PASSWORD" -e "GRANT ALL PRIVILEGES ON test_news_db.* TO '"'"'administrator'"'"'@'"'"'%'"'"';"'
   ```

   The command reads the root password from the container's own
   `MARIADB_ROOT_PASSWORD` setting, so the password is not typed, and does
   not end up in your shell history. The container creates the database
   user as `'administrator'@'%'`, so the command uses `'%'` too.

## Configuration

Django News reads its secrets, and the settings that change from one
computer to another, from a file named `.env` in the folder that contains
`manage.py`. The file is not part of the repository, because Git is told to
ignore it, so each person who installs the project creates their own.

1. **Create the `.env` file** from the example file in the repository:

   ```bash
   cp .env.example .env
   ```

2. **Generate a secret key** for Django. With the virtual environment
   active, run:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Fill in the placeholders.** Open `.env` in a text editor, and replace
   each value in angle brackets:

   | Setting | Value |
   |---|---|
   | `DJANGO_SECRET_KEY` | The key generated in step 2 |
   | `DB_USER` | `administrator`, the database user from [Database Setup](#database-setup) |
   | `DB_PASSWORD` | That user's password |
   | `THIRD_PARTY_API_KEY` | Any string you choose. The simulated third party accepts whatever is set here. |

   Write each value as it is, with no quotes and no spaces around `=`.

The other settings already have values that work for the setup in this
README. Change them only if your setup is different:

| Setting | Default | What it is |
|---|---|---|
| `DJANGO_DEBUG` | `True` | Development mode. Set to `False` on a live site. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | The host names the site may be served from, separated by commas |
| `DB_NAME` | `news_db` | The database's name |
| `DB_HOST` | `localhost` | Where the database server runs |
| `DB_PORT` | `3306` | The database server's port |
| `THIRD_PARTY_API_URL` | `http://127.0.0.1:8000/third-party/articles/` | Where approved articles are sent |

If a required setting is missing, Django stops with an error that names the
setting.

## Running the Project

Run these commands from the folder that contains `manage.py`, with the
virtual environment active.

1. **Build the tables:**

   ```bash
   python manage.py migrate_all
   ```

2. **Create the role groups and their permissions.** Users cannot be saved
   until the groups exist:

   ```bash
   python manage.py setup_groups_and_permissions
   ```

3. **Load the demo data** (optional and recommended), with sample users,
   publications, articles, and newsletters:

   ```bash
   python manage.py seed_demo_data
   ```

   The demo data includes a superuser for the Django admin, with the
   username `admin` and the password `newspaper`.

   If you skip the demo data, create a superuser yourself instead. The
   command asks for a username, email address, and password:

   ```bash
   python manage.py createsuperuser
   ```

4. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

   The server is expected to run at its default address,
   `http://127.0.0.1:8000`, which is where `THIRD_PARTY_API_URL` in `.env`
   sends approved articles.

5. **Open the site** in your browser:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

   Log in with a [demo account](#demo-accounts), or register a new account
   and choose its role.

### Emails

During development, emails are not sent. They are printed in the terminal
running the server instead. These include:

- Approved articles, emailed to subscribers.
- Password reset links. Long lines are split, each first part ending in `=`,
  and the Check Your Email page has a box that joins the link back together.

### Django Admin

The Django admin is at
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). Log in with the
superuser from step 3. It is not part of the site's normal use, and it can
bypass the site's rules, such as changing an article's author or undoing its
approval.

## Demo Accounts

`seed_demo_data` creates these accounts. **Every demo account's password is
`newspaper`.**

| Username | Role | Notes |
|---|---|---|
| Paul | Publisher | Owns The Lamplight Gazette |
| Penny | Publisher | Owns The Copper Kettle Courier |
| James | Journalist | Works for The Lamplight Gazette |
| Julia | Journalist | Works for The Copper Kettle Courier |
| Jonah | Journalist | Works for both publications |
| Jade | Journalist | Works for neither; writes independently |
| Elena | Editor | Works for The Lamplight Gazette |
| Edward | Editor | Works for The Copper Kettle Courier |
| Ezra | Editor | Works for both publications |
| Esther | Editor | Works for neither |
| Richard | Reader | Subscribes to The Lamplight Gazette and to Julia |
| Rhonda | Reader | Subscribes to The Copper Kettle Courier, James, and Julia |
| Rosa | Reader | Subscribes to nothing |
| admin | Superuser | For the Django admin; has the Reader role on the site |

Some of each journalist's articles are pending, so editors and journalists
have articles to approve.

## REST API

The API covers articles. Every request needs a token, sent in the
`Authorization` header:

```
Authorization: Token <your token>
```

### Endpoints

| Method | Address | What it does |
|---|---|---|
| POST | `/api/token/` | Returns the user's token, for a `username` and `password` |
| GET | `/api/articles/` | Lists every approved article, newest first |
| POST | `/api/articles/` | Creates an article, which starts as pending. Journalists only. |
| GET | `/api/articles/subscribed/` | Lists the approved articles from the user's subscriptions. Readers only. |
| GET | `/api/articles/pending/` | Lists the pending articles the user can approve, oldest first. Editors and journalists only. |
| GET | `/api/articles/<id>/` | Returns one article |
| PUT | `/api/articles/<id>/` | Updates an article, sending every field |
| PATCH | `/api/articles/<id>/` | Updates only the fields sent. Sending `"approved": true` approves the article. |
| DELETE | `/api/articles/<id>/` | Deletes an article |

The API follows the same rules as the website. A request the user may not
make is refused, usually with a message saying why. A pending article the
user may not read gets 404 Not Found, so its existence is not revealed.

- Readers can only read.
- Journalists create articles, for themselves or for a publication they work
  for.
- A publication's editors and journalists can update and delete its articles.
  Only its editors can approve them.
- A journalist can update, delete, and approve their own independent
  articles.
- An approved article cannot be set back to pending.

### Examples

Each example lists the parts of a request. Fill them in to the tool you use,
such as Postman, curl, or Python's requests library. In the examples:

- `<token>` is the token returned by [Get a Token](#get-a-token).
- `<id>` is an article's ID, from the `id` field of an article in a list.

#### Get a Token

Here for the demo journalist James.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/api/token/`
- **Headers:** `Content-Type: application/json`
- **Body:**

  ```json
  {"username": "James", "password": "newspaper"}
  ```

- **Response:** `200 OK`, with the token: `{"token": "..."}`

#### List the Approved Articles

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/api/articles/`
- **Headers:** `Authorization: Token <token>`
- **Body:** none
- **Response:** `200 OK`, with a list of articles

#### Create an Independent Article

As a journalist. A `publication` of `null` makes the article independent. To
write for a publication the journalist works for, send its ID instead.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/api/articles/`
- **Headers:**
  - `Authorization: Token <token>`
  - `Content-Type: application/json`
- **Body:**

  ```json
  {"title": "My Article", "content": "Some news.", "publication": null}
  ```

- **Response:** `201 Created`, with the new article, which starts as pending

#### Approve an Article

As the article's publication's editor, or, for an independent article, as
its journalist.

- **Method:** `PATCH`
- **URL:** `http://127.0.0.1:8000/api/articles/<id>/`
- **Headers:**
  - `Authorization: Token <token>`
  - `Content-Type: application/json`
- **Body:**

  ```json
  {"approved": true}
  ```

- **Response:** `200 OK`, with the article, now approved

### Third-Party Endpoint

`POST /third-party/articles/` is the simulated third party's endpoint, which
receives each approved article. It is not part of the article API. Instead
of a token, it needs the third party's API key, in an `X-API-Key` header. The
key is `THIRD_PARTY_API_KEY` in the `.env` file.

## Running the Tests

> **Important:** The tests only run if the database is set up as described
> in [Database Setup](#database-setup), and the `.env` file is filled in as
> described in [Configuration](#configuration). The database user must have
> rights to a second database, `test_news_db`, as well as to `news_db`. Each
> test run creates `test_news_db`, runs the tests in it, and deletes it
> afterward. Without these rights, the tests do not run at all: Django stops
> with an error, such as "Access denied", before the first test. MariaDB must
> also be running.

Because the tests use their own database, running them does not change
`news_db` or the site's data.

The unit tests cover the REST API, including access for each role, subscribed
articles, approval, and the emails and third-party sharing that approval
triggers. Email and third-party sharing are replaced by test stand-ins, so
nothing is sent.

Run them from the folder that contains `manage.py`, with the virtual
environment active:

```bash
python manage.py test
```

### Code Style

The code follows PEP 8. It is formatted with black and checked with flake8,
both installed from `requirements.txt`:

```bash
black --check .
```

```bash
flake8
```

## Management Commands

> **Note:** This section is reference, not more steps to follow. The setup
> has already used the commands it needs: `migrate_all`,
> `setup_groups_and_permissions`, and `seed_demo_data`, in
> [Running the Project](#running-the-project). Come back here to learn what a
> command does, or to reset the database later.

Django News adds these commands to `manage.py`. Run each one as
`python manage.py <command>`.

| Command | What it does |
|---|---|
| `migrate_all` | Runs `makemigrations`, then `migrate`, to build or update every table |
| `setup_groups_and_permissions` | Creates the Readers, Publishers, Editors, and Journalists groups, with their permissions. Safe to run again. |
| `seed_demo_data` | Loads the [demo accounts](#demo-accounts) and their publications, subscriptions, articles, and newsletters. Runs only on an empty database. |
| `delete_all_data` | Deletes every user, publication, article, newsletter, third-party article, and login session. Keeps the tables and the groups. |
| `drop_all_tables` | Deletes every table in the database, keeping the database itself |
| `remove_groups_and_permissions` | Deletes the four role groups |

The three commands that delete things ask you to type `yes` first, unless
`--no-input` is added. They only run while `DJANGO_DEBUG` is `True` in the
`.env` file, so they cannot change a live site.

### Common Tasks

Each task deletes data, and logs everyone out of the site. Run the commands
in order, with the virtual environment active.

#### Reset the Site to Fresh Demo Data

Use this to undo changes made while trying out the site. It deletes all the
data, keeps the tables and the groups, then loads the demo data again.

```bash
python manage.py delete_all_data --no-input
```

```bash
python manage.py seed_demo_data
```

#### Empty the Site, with No Demo Data

Use this to start using the site with your own accounts and content only. It
deletes all the data, including every user, and keeps the tables and the
groups. Then create a superuser for the Django admin, and register the site's
accounts from its Register page.

```bash
python manage.py delete_all_data --no-input
```

```bash
python manage.py createsuperuser
```

#### Rebuild the Database from Nothing

Use this if the tables themselves are broken or out of date. It deletes
every table, then builds them again and sets up the groups.

```bash
python manage.py drop_all_tables --no-input
```

```bash
python manage.py migrate_all
```

```bash
python manage.py setup_groups_and_permissions
```

Then either load the demo data:

```bash
python manage.py seed_demo_data
```

Or, for an empty site with no demo data, create a superuser instead:

```bash
python manage.py createsuperuser
```

## Project Structure

```
django-news-app/
|-- README.md                  # The file you are reading now
|-- .env.example               # Example settings, copied to .env
|-- .gitignore                 # Files Git leaves out, such as .env and venv
|-- manage.py                  # Django: runs commands and the server
|-- requirements.txt           # Python packages, with exact versions
|-- pyproject.toml             # Settings for black
|-- .flake8                    # Settings for flake8
|-- django_news/               # Django: settings and main URLs
|   |-- settings.py
|   |-- urls.py
|   |-- static/                # The site's stylesheet
|   `-- templates/             # Shared templates, such as base.html
|-- accounts/                  # The custom User model, registration, roles
|   `-- management/commands/   # Group and permission commands
|-- news/                      # Publications, articles, newsletters, pages
|   |-- access.py              # Who may read, change, and approve what
|   |-- approval.py            # Emailing and sharing approved articles
|   |-- signals.py             # Runs approval.py when an article is approved
|   |-- views/                 # One file per area of the site
|   |-- templates/news/
|   `-- management/commands/   # Data and table commands
|-- api/                       # The REST API
|   `-- tests.py               # Unit tests
`-- third_party/               # The simulated third-party service
```
