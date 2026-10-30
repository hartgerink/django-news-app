# Running the Unit Tests

View the unit tests: [`api/tests.py`](../api/tests.py)

Django News's unit tests cover the REST API. They check that:

- a user gets their token with their username and password,
- a request without a valid token is refused,
- every role sees only approved articles in the list of all articles,
- a reader's subscribed articles come only from their subscriptions, and
  only readers can list them,
- a subscription to a journalist leaves out the articles they write for a
  publication,
- the pending list holds only the articles the user can approve, and only
  editors and journalists can see it,
- a journalist can create an article for their publication, and a reader
  cannot create one,
- an editor can approve and delete their publication's articles, but not
  another publication's,
- a journalist can approve their own independent article,
- approving an article emails its subscribers and sends it to the partner
  news service's API,
- changing an approved article does not email it or send it to the
  partner news service's API again.

## Before You Start

MariaDB must be running, and set up as described in
[Setting Up MariaDB](setting-up-mariadb.md), including the `administrator`
user's rights to `test_news_db`.

## What the Tests Do Not Touch

The tests check what Django News would do, without doing it for real:

- **The site's data.** Each run creates a separate database,
  `test_news_db`, runs the tests in it, and deletes it afterward. The
  site's own data, in `news_db`, is not touched.
- **Email.** Django collects the emails in a test outbox instead of
  sending them. The tests check who each email is addressed to.
- **The partner news service.** The request that sends an approved
  article to the partner news service's API is replaced with a stand-in,
  which records the request without sending it. The tests check its
  address, its API key, and the article in it.

## Running Them

Run the tests in the version of Django News you installed. Follow one
option, not both.

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

3. Run the tests:

   ```bash
   python manage.py test
   ```

### Option B: Django News in Docker

1. Make sure the container is running. If it already is, this changes
   nothing:

   ```bash
   docker start django-news-app
   ```

2. Run the tests:

   ```bash
   docker exec django-news-app python manage.py test
   ```

## Reading the Results

When every test passes, the output should end with `OK`, after a line such
as `Ran 16 tests in 2.361s`.

A test that fails is listed by name, with what went wrong. An error such as
"Access denied" before the first test means the `administrator` user lacks
rights to `test_news_db`.
