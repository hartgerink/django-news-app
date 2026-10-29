# How the Django News API Works

Django News has a REST API for its articles. Programs use it to list
articles, write them, change them, and approve them, the same things people
do on the website, under the same rules. This guide covers every part of the
API, with an example request and response for each.

## Contents

- [The Basics](#the-basics)
- [Getting a Token](#getting-a-token)
- [Sending the Token](#sending-the-token)
- [Articles in JSON](#articles-in-json)
- [The Endpoints](#the-endpoints)
- [Listing Articles](#listing-articles)
- [Reading One Article](#reading-one-article)
- [Creating an Article](#creating-an-article)
- [Changing an Article](#changing-an-article)
- [Approving an Article](#approving-an-article)
- [Deleting an Article](#deleting-an-article)
- [Who Can Do What](#who-can-do-what)
- [Errors](#errors)

## The Basics

| | |
|---|---|
| **Address** | Every endpoint starts with `http://127.0.0.1:8000/api/` |
| **Format** | Requests and responses are JSON |
| **Accounts** | The API uses the website's accounts. Each caller acts as one user, with that user's role. |
| **Logging in** | Each request carries the user's token, a long code that stands in for their username and password |

The examples in this guide use `curl`, which comes with Git Bash, macOS,
and Linux. Any tool that sends HTTP requests works the same way, such as
Postman, or Python's `requests` package.

## Getting a Token

Send the user's username and password to `/api/token/`:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "<username>", "password": "<password>"}'
```

The response holds the user's token:

```json
{"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}
```

Each user has one token, created the first time they ask for it. Asking
again returns the same token. A wrong username or password gets
`400 Bad Request`:

```json
{"non_field_errors": ["Unable to log in with provided credentials."]}
```

Keep the token secret: anyone who has it can act as that user.

## Sending the Token

Send the token in the `Authorization` header of every other request, after
the word `Token` and a space:

```bash
curl http://127.0.0.1:8000/api/articles/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

A request without a token, or with one that is not valid, gets
`401 Unauthorized`:

```json
{"detail": "Authentication credentials were not provided."}
```

```json
{"detail": "Invalid token."}
```

The rest of this guide writes the header as
`Authorization: Token <token>`. Put the user's token in place of
`<token>`.

## Articles in JSON

Every endpoint that returns articles returns each one like this:

```json
{
  "id": 428,
  "title": "My Article",
  "content": "Some news.",
  "author": "James",
  "publication": null,
  "approved": false,
  "created_at": "2026-10-29T21:04:36.952950Z"
}
```

| Field | What it is | Who sets it |
|---|---|---|
| `id` | The article's ID, used in the address of a single article | Django News |
| `title` | The title, up to 200 characters | The caller |
| `content` | The article's text | The caller |
| `author` | The author's username | Django News: the caller who created it |
| `publication` | The ID of the article's publication, or `null` for an independent article | The caller, when creating it. It cannot change afterward. |
| `approved` | `false` while pending, `true` once approved | Django News. Approving is described in [Approving an Article](#approving-an-article). |
| `created_at` | When the article was created, in UTC | Django News |

Fields that Django News sets are ignored if a request sends them, except
`approved`, which is how an article is approved.

## The Endpoints

| Method | Address | What it does |
|---|---|---|
| `POST` | `/api/token/` | Returns the user's token, for a username and password |
| `GET` | `/api/articles/` | Lists every approved article |
| `GET` | `/api/articles/subscribed/` | Lists the approved articles from the caller's subscriptions. Readers only. |
| `GET` | `/api/articles/pending/` | Lists the pending articles the caller can approve. Editors and journalists only. |
| `POST` | `/api/articles/` | Creates an article. Journalists only. |
| `GET` | `/api/articles/<id>/` | Returns one article |
| `PUT` | `/api/articles/<id>/` | Changes an article, sending every field |
| `PATCH` | `/api/articles/<id>/` | Changes only the fields sent, or approves the article |
| `DELETE` | `/api/articles/<id>/` | Deletes an article |

In the addresses, `<id>` is an article's `id`.

## Listing Articles

All three lists return a JSON list of articles, which is empty, `[]`, when
there are none. Each list returns every matching article at once.

### Every Approved Article

Anyone can list every approved article on the site, newest first:

```bash
curl http://127.0.0.1:8000/api/articles/ \
  -H "Authorization: Token <token>"
```

### The Articles From Your Subscriptions

A reader can list the approved articles from the publications and
journalists they subscribe to, newest first. These are the same articles as
on their dashboard.

```bash
curl http://127.0.0.1:8000/api/articles/subscribed/ \
  -H "Authorization: Token <token>"
```

Other roles have no subscriptions, and get `403 Forbidden`:

```json
{"detail": "Only readers have subscriptions."}
```

### The Articles Waiting for Your Approval

Editors and journalists can list the pending articles they can approve,
oldest first, so the ones that have waited longest come first:

- for an editor, the pending articles of the publications they work for,
- for a journalist, their own pending independent articles.

```bash
curl http://127.0.0.1:8000/api/articles/pending/ \
  -H "Authorization: Token <token>"
```

Readers and publishers cannot approve articles, and get `403 Forbidden`:

```json
{"detail": "Only editors and journalists can approve articles."}
```

## Reading One Article

```bash
curl http://127.0.0.1:8000/api/articles/428/ \
  -H "Authorization: Token <token>"
```

Anyone can read an approved article. A pending article can be read only by:

- its publication's editors and journalists, for a publication's article,
- its author, for an independent article.

Anyone else gets `404 Not Found`, the same response as for an article that
does not exist, so a pending article's existence stays private:

```json
{"detail": "No Article matches the given query."}
```

## Creating an Article

Journalists create articles. Send the title, the content, and the
publication: the ID of a publication the journalist works for, or `null`
for an independent article.

```bash
curl -X POST http://127.0.0.1:8000/api/articles/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Article", "content": "Some news.", "publication": null}'
```

The response is `201 Created`, with the new article. The caller is its
author, and it starts as pending:

```json
{"id": 428, "title": "My Article", "content": "Some news.", "author": "James", "publication": null, "approved": false, "created_at": "2026-10-29T21:04:36.952950Z"}
```

A publication the journalist does not work for gets `400 Bad Request`:

```json
{"detail": "Some fields are missing or not valid.", "errors": {"publication": ["Choose a publication you work for, or null for an independent article."]}}
```

Other roles get `403 Forbidden`:

```json
{"detail": "Only journalists can create articles."}
```

## Changing an Article

An article's title and content can be changed by:

- its author, for an independent article,
- its publication's editors and journalists, for a publication's article.

There are two ways to change one:

- **`PATCH`** changes only the fields sent. To change the title alone:

  ```bash
  curl -X PATCH http://127.0.0.1:8000/api/articles/428/ \
    -H "Authorization: Token <token>" \
    -H "Content-Type: application/json" \
    -d '{"title": "New Title"}'
  ```

- **`PUT`** replaces the article's fields, so it must send both the title
  and the content:

  ```bash
  curl -X PUT http://127.0.0.1:8000/api/articles/428/ \
    -H "Authorization: Token <token>" \
    -H "Content-Type: application/json" \
    -d '{"title": "New Title", "content": "All new."}'
  ```

Either way, the response is `200 OK`, with the changed article. Changing an
approved article keeps it approved, and the change is not emailed or shared
again.

An article's publication cannot change. Sending a different one gets
`400 Bad Request`:

```json
{"detail": "Some fields are missing or not valid.", "errors": {"publication": ["An article's publication cannot change once it is created."]}}
```

Anyone else who tries gets `403 Forbidden`:

```json
{"detail": "Only the author of an independent article, or the staff of an article's publication, can change or delete it."}
```

## Approving an Article

Approve a pending article by sending `"approved": true`, usually with
`PATCH`:

```bash
curl -X PATCH http://127.0.0.1:8000/api/articles/428/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"approved": true}'
```

The response is `200 OK`, with the article, now `"approved": true`. A `PUT`
or `PATCH` that changes other fields can approve the article at the same
time.

An article can be approved by:

- its publication's editors, for a publication's article,
- its author, for an independent article.

Anyone else gets `403 Forbidden`, including a publication's journalists:

```json
{"detail": "Only a publication's editors can approve its articles, and only the author can approve an independent article."}
```

Approval works just as it does on the website. The moment an article is
approved, it is emailed to its subscribers and shared with Django News's
partner news service. Approval is permanent. Sending `"approved": false`
for an approved article gets `400 Bad Request`:

```json
{"detail": "An approved article cannot be set back to pending."}
```

## Deleting an Article

The people who can change an article can delete it:

```bash
curl -X DELETE http://127.0.0.1:8000/api/articles/428/ \
  -H "Authorization: Token <token>"
```

The response is `204 No Content`, with no body. Deleting an approved
article also removes it from every newsletter that included it.

## Who Can Do What

| Action | Reader | Journalist | Editor | Publisher |
|---|:---:|:---:|:---:|:---:|
| List every approved article | Yes | Yes | Yes | Yes |
| List the articles from their subscriptions | Yes | | | |
| List the articles waiting for their approval | | Own independent ones | Their publications' | |
| Read a pending article | | Own independent ones, and their publications' | Their publications' | |
| Create articles | | Yes | | |
| Change and delete articles | | Own independent ones, and their publications' | Their publications' | |
| Approve articles | | Own independent ones | Their publications' | |

## Errors

Every error response is JSON, with a `detail` message saying what went
wrong.

| Status | Meaning |
|---|---|
| `400 Bad Request` | The request's data is missing or not valid, or asks for something that is not allowed, such as setting an approved article back to pending |
| `401 Unauthorized` | The token is missing or not valid |
| `403 Forbidden` | The caller's role or position does not allow the request |
| `404 Not Found` | The article does not exist, or the caller may not read it |
| `405 Method Not Allowed` | The address does not accept that method, such as `DELETE` on `/api/articles/` |

When fields are missing or not valid, `errors` lists each one, with what
is wrong with it:

```json
{"detail": "Some fields are missing or not valid.", "errors": {"title": ["This field may not be blank."], "content": ["This field is required."]}}
```
