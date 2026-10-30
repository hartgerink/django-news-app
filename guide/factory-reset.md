# Factory Reset

A factory reset is a full reset of Django News's database. Every table is
deleted and built again, and the four roles are set up again, returning
the database to the state of a new installation. Every user, publication,
article, and newsletter is deleted, and everyone is logged out.

The reset is then finished in one of two ways:

- **Blank:** with no data, ready for new accounts.
- **With sample data:** filled with sample users, publications, articles,
  and newsletters, for trying out every part of the site.

The commands below are shown in the installed-directly form. How to run
them, in either version of Django News, is described in
[Running Management Commands](running-management-commands.md).

> **This cannot be undone.** The first command asks for `yes` before it
> deletes anything, and runs only while `DJANGO_DEBUG` is `True` in the
> `.env` file.

## Contents

- [Resetting the Database](#resetting-the-database)
- [Finishing the Reset](#finishing-the-reset)
  - [Option A: Blank](#option-a-blank)
  - [Option B: With Sample Data](#option-b-with-sample-data)

## Resetting the Database

1. Delete every table:

   ```bash
   python manage.py drop_all_tables
   ```

   The command says how many tables it will delete, and asks for
   confirmation. Type `yes`, then press **Enter**. Any other answer cancels
   it, and nothing is deleted. The output should end with a line such as:

   ```
   Deleted all 20 tables in news_db.
   ```

2. Build the tables again:

   ```bash
   python manage.py migrate_all
   ```

   The output should end with `Migrations complete.`

3. Set up the four roles, Reader, Journalist, Editor, and Publisher, with
   their rights:

   ```bash
   python manage.py setup_groups_and_permissions
   ```

   The output should list the four roles' groups:

   ```
   Created Readers with 3 permissions.
   Created Publishers with 6 permissions.
   Created Editors with 8 permissions.
   Created Journalists with 10 permissions.
   ```

The database is now in the state of a new installation.

## Finishing the Reset

Follow one option, not both.

### Option A: Blank

Nothing more is needed. The site is ready for new accounts, which are
registered from its **Register** page.

A superuser, for the Django admin at
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/), can be added
now. The command asks for a username, an email address, and a password:

```bash
python manage.py createsuperuser
```

### Option B: With Sample Data

Load the sample content:

```bash
python manage.py seed_demo_data
```

The output should be:

```
Created 14 users, 2 publications, 5 subscriptions, 15 articles, and 5 newsletters.
Every demo account's password is "newspaper".
```

The sample users, the publications they work for, and their articles and
newsletters are described in [The Sample Data](the-sample-data.md).

The sample data includes a superuser, `admin`. Another superuser can be
added after loading it, with a username other than `admin` and an email
address other than `admin@djangonews.local`:

```bash
python manage.py createsuperuser
```

---

**The management command guides:**

- [Running Management Commands](running-management-commands.md)
- **Factory Reset** (this page)
- [The Sample Data](the-sample-data.md)

[Back to the README](../README.md)
