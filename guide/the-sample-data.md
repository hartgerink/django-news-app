# The Sample Data

The sample data is a small, complete news site: two publications, the
people who run them and write for them, readers with subscriptions, and
articles and newsletters, some approved and some waiting for approval. It
is loaded by a factory reset with sample data, described in
[Factory Reset](factory-reset.md#option-b-with-sample-data).

Every sample account's password is `newspaper`. Each account's email
address is its username, in lowercase, at `djangonews.local`, such as
`james@djangonews.local`.

## Contents

- [The Publications](#the-publications)
- [The Accounts](#the-accounts)
- [The Articles](#the-articles)
- [Articles Waiting for Approval](#articles-waiting-for-approval)
- [The Newsletters](#the-newsletters)
- [What Each Reader Sees](#what-each-reader-sees)

## The Publications

| Publication | Owner | Editors | Journalists |
|---|---|---|---|
| **The Lamplight Gazette** | Paul | Elena, Ezra | James, Jonah |
| **The Copper Kettle Courier** | Penny | Edward, Ezra | Julia, Jonah |

- **The Lamplight Gazette:** "Evening news for night owls: city politics,
  late-breaking stories, and the people who keep the lights on."
- **The Copper Kettle Courier:** "Food, community, and small-town life,
  served warm every morning."

Ezra and Jonah work for both publications, so they show how one person's
rights cover more than one publication.

## The Accounts

### Publishers

| Username | Owns |
|---|---|
| Paul | The Lamplight Gazette |
| Penny | The Copper Kettle Courier |

### Journalists

| Username | Works for |
|---|---|
| James | The Lamplight Gazette, and writes independently |
| Julia | The Copper Kettle Courier, and writes independently |
| Jonah | Both publications |
| Jade | Neither publication. Writes only independently. |

### Editors

| Username | Works for |
|---|---|
| Elena | The Lamplight Gazette |
| Edward | The Copper Kettle Courier |
| Ezra | Both publications |
| Esther | Neither publication, so she has no articles to review |

### Readers

| Username | Subscribes to |
|---|---|
| Richard | The Lamplight Gazette, and the journalist Julia |
| Rhonda | The Copper Kettle Courier, and the journalists James and Julia |
| Rosa | Nothing |

### Superuser

| Username | Notes |
|---|---|
| admin | Logs in to the Django admin. On the site itself, a Reader. |

## The Articles

There are 15 articles. Nine are approved, and six are waiting for
approval.

| Journalist | Article | For | Status |
|---|---|---|---|
| James | Night Market Lanterns Return to Canal Street | The Lamplight Gazette | Approved |
| James | City Council Votes to Keep the Old Clock Tower Ticking | The Lamplight Gazette | Approved |
| James | The Last Tram Driver on Route 9 | The Lamplight Gazette | Pending |
| James | What the Fog Remembers | Independent | Approved |
| James | A Field Guide to Insomniac Pigeons | Independent | Pending |
| Julia | Mrs. Abernathy's Scones Win the County Fair, Again | The Copper Kettle Courier | Approved |
| Julia | The Library Starts Lending Cake Pans | The Copper Kettle Courier | Approved |
| Julia | Firehouse Chili Night Raises Record Sum | The Copper Kettle Courier | Pending |
| Julia | Letters from a Lighthouse Keeper's Garden | Independent | Approved |
| Julia | The Bicycle That Came Home After Forty Years | Independent | Pending |
| Jonah | The Bridge Painters Who Only Work at Night | The Lamplight Gazette | Approved |
| Jonah | The Town's Oldest Oak Gets a Birthday Cake | The Copper Kettle Courier | Approved |
| Jonah | Saturday Soup Swap Outgrows the Church Hall | The Copper Kettle Courier | Pending |
| Jade | Notes from a Rooftop Beekeeper | Independent | Approved |
| Jade | The Umbrella Library at the Number 12 Bus Stop | Independent | Pending |

## Articles Waiting for Approval

Each pending article can be approved by its publication's editors, or, for
an independent article, by its journalist.

| Article | Can be approved by |
|---|---|
| The Last Tram Driver on Route 9 | Elena or Ezra, editors of The Lamplight Gazette |
| Firehouse Chili Night Raises Record Sum | Edward or Ezra, editors of The Copper Kettle Courier |
| Saturday Soup Swap Outgrows the Church Hall | Edward or Ezra, editors of The Copper Kettle Courier |
| A Field Guide to Insomniac Pigeons | James, its journalist |
| The Bicycle That Came Home After Forty Years | Julia, its journalist |
| The Umbrella Library at the Number 12 Bus Stop | Jade, its journalist |

Approving one of these emails it to its subscribers. During development,
those emails are printed in the server's output instead of being sent.

## The Newsletters

| Newsletter | Journalist | For | Articles |
|---|---|---|---|
| Lamplight After Dark | James | The Lamplight Gazette | City Council Votes to Keep the Old Clock Tower Ticking; Night Market Lanterns Return to Canal Street |
| Gazette Weekend Edition | Jonah | The Lamplight Gazette | The Bridge Painters Who Only Work at Night; Night Market Lanterns Return to Canal Street |
| The Kettle's Weekly Pour | Julia | The Copper Kettle Courier | The Library Starts Lending Cake Pans; Mrs. Abernathy's Scones Win the County Fair, Again |
| Notes from the Night Walk | James | Independent | What the Fog Remembers |
| Postcards from Gull Point | Julia | Independent | Letters from a Lighthouse Keeper's Garden |

## What Each Reader Sees

A reader's dashboard lists the approved articles from their subscriptions.
A subscription to a journalist covers only that journalist's independent
articles.

| Reader | Articles on the dashboard |
|---|---|
| Richard | The Lamplight Gazette's three approved articles, and Julia's independent article, Letters from a Lighthouse Keeper's Garden |
| Rhonda | The Copper Kettle Courier's three approved articles, and the independent articles What the Fog Remembers, by James, and Letters from a Lighthouse Keeper's Garden, by Julia |
| Rosa | None, because she subscribes to nothing |

---

**The management command guides:**

- [Running Management Commands](running-management-commands.md)
- [Factory Reset](factory-reset.md)
- **The Sample Data** (this page)

[Back to the README](../README.md)
