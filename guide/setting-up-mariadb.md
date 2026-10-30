# Setting Up MariaDB

Django News stores everything it knows, from user accounts to articles, in a
MariaDB database. MariaDB is a separate program, a database server, which
you install and look after yourself. This guide sets out what Django News
needs from it, so you can set it up in whatever way suits your computer.

## Contents

- [What Django News Needs](#what-django-news-needs)
- [Installing MariaDB](#installing-mariadb)
- [Creating the Database and the User](#creating-the-database-and-the-user)
- [Letting Django News Connect](#letting-django-news-connect)
- [Checking That It Works](#checking-that-it-works)

## What Django News Needs

| Requirement | Details |
|---|---|
| **MariaDB Server** | Version 10.11 or later, running whenever Django News runs |
| **A database** | Named `news_db`, using the `utf8mb4` character set |
| **A database user** | Named `administrator`, with a password you choose |
| **The user's rights** | Full rights on `news_db`, and on `test_news_db`, a second database the unit tests create and delete each time they run |
| **A way to connect** | MariaDB must accept the user's connections from wherever Django News runs. See [Letting Django News Connect](#letting-django-news-connect). |

Use these names exactly as they are: `news_db`, `test_news_db`, and
`administrator`.

## Installing MariaDB

Install MariaDB Server on the computer that runs Django News, following
MariaDB's own instructions:

- [Download MariaDB Server](https://mariadb.org/download/)
- [Installing MariaDB](https://mariadb.com/docs/server/server-management/install-and-upgrade-mariadb/installing-mariadb),
  MariaDB's guide for every system, including macOS with Homebrew.

On Windows, installation asks you to choose a password for MariaDB's
**root** account, its built-in administrator. On Linux and macOS, root is
reached with `sudo mariadb` instead. Root is used only to set up the
database and the user. Django News never uses it.

## Creating the Database and the User

Open the MariaDB command line as root. On most systems, that is
`mariadb -u root -p`, entering the root password, or `sudo mariadb` on Linux
and macOS. Then copy the whole block below, comments included, and paste it
in, with your own password in place of `<your-database-password>`. MariaDB
skips the comment lines, the ones that start with `--`.

```sql
-- Create the database that holds the site's data.
-- utf8mb4 lets it store every Unicode character.
CREATE DATABASE news_db CHARACTER SET utf8mb4;

-- Create the user Django News logs in as, with your own password.
-- '%' lets the user connect from any computer, including this one.
CREATE USER 'administrator'@'%' IDENTIFIED BY '<your-database-password>';

-- Give the user full rights to the site's database.
GRANT ALL PRIVILEGES ON news_db.* TO 'administrator'@'%';

-- And to the test database, which the unit tests create and delete.
GRANT ALL PRIVILEGES ON test_news_db.* TO 'administrator'@'%';

-- Apply the new rights, then leave the MariaDB command line.
FLUSH PRIVILEGES;
EXIT;
```

## Letting Django News Connect

Django News comes in two versions, and they reach MariaDB in different ways.

### Django News Installed Directly

Django News runs on the same computer as MariaDB, and connects to it as
`localhost`. A standard MariaDB installation accepts that as it is.

### The Docker Version of Django News

Django News runs in a Docker container, which reaches MariaDB over Docker's
network, as if from another computer. For that to work:

- **MariaDB must accept network connections,** not only connections from
  the computer itself. On some systems, Linux in particular, MariaDB accepts
  local connections only, by default. Its `bind-address` setting controls
  this.
- **Nothing in between may block the connection,** such as a firewall rule
  for MariaDB's port, 3306.
- **The user must be allowed to connect from the container's address.** The
  `'%'` in the SQL above allows any address.

When the container starts, it is told where to find MariaDB. The
instructions for running the Docker version cover that.

## Checking That It Works

Open the MariaDB command line again, this time as the `administrator` user
you created in
[Creating the Database and the User](#creating-the-database-and-the-user).
In a terminal, run this command, and enter that user's password when asked:

```bash
mariadb -u administrator -p
```

Then, in the MariaDB command line, list the databases the user can see. The
list should include `news_db`:

```sql
SHOW DATABASES;
```

Next, confirm the user's rights. The list should include `ALL PRIVILEGES` on
`news_db` and on `test_news_db`:

```sql
SHOW GRANTS;
```

Type `EXIT;` to leave the MariaDB command line.

---

**The setup guides:**

- **Setting Up MariaDB** (this page)
- [Installing Django News Directly](installing-django-news-directly.md)
- [Running Django News with Docker](running-django-news-with-docker.md)

[Back to the README](../README.md)
