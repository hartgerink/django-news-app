# How Django News Works

Django News is a news website where articles come from two kinds of writers:
the staff of news publications, and independent journalists who write under
their own name. Before an article goes public, someone responsible for it
approves it: a publication's editor, or, for an independent article, its
journalist. The moment it is approved, it appears for every reader, and it is
emailed to everyone who follows its publication or its journalist.

Everyone who uses the site has one role, and the role decides what they see
and what they can do. This guide walks through the site role by role, then
follows an article from first draft to a subscriber's inbox.

## Contents

- [The Four Roles](#the-four-roles)
- [Getting Started](#getting-started)
- [Finding Your Way Around](#finding-your-way-around)
- [Readers](#readers)
- [Journalists](#journalists)
- [Editors](#editors)
- [Publishers](#publishers)
- [The Life of an Article](#the-life-of-an-article)
- [Newsletters](#newsletters)
- [Who Can Do What](#who-can-do-what)

## The Four Roles

| Role | In short |
|---|---|
| **Reader** | Reads articles and newsletters, and subscribes to publications and journalists. |
| **Journalist** | Writes articles and newsletters, independently or for the publications they work for. |
| **Editor** | Reviews and approves the articles of the publications they work for. |
| **Publisher** | Creates publications, and chooses the editors and journalists who work for them. |

Each user has exactly one role, chosen when they register. A role cannot be
changed later.

Editors and journalists can work for any number of publications, or for
none. Their rights over a publication's articles and newsletters last only
while they work for it.

## Getting Started

### Visiting the Site

Visitors who are not logged in see the **Welcome** page, which describes the
site and the four roles. The top of every page has **Home**, **Log In**, and
**Register** links.

Everything else on the site needs an account: visitors can only see the
welcome, registration, login, and password reset pages.

### Registering

On the **Register** page, choose:

- **A username:** up to 20 letters and digits, with no spaces or symbols.
- **An email address:** each account needs its own. It is where password
  reset links and article emails are sent.
- **A password,** typed twice.
- **A role:** Reader, Journalist, Editor, or Publisher.

After registering, you are logged in straight away and taken to your
dashboard.

### Logging In and Out

- **Log In** takes your username and password, then opens your dashboard.
- **Log Out** is in the account menu, under your username at the top of the
  page. It returns you to the Welcome page.

### Your Account

The **Account** page, in the account menu, shows your username and email
address, with a **Change Password** link. Usernames and email addresses
cannot be changed.

### Forgotten Passwords

1. On the **Log In** page, choose **Forgot your password?**
2. Enter your account's email address, and choose **Send Reset Link**.
3. Open the link in the email, and choose a new password.

The link works once. If it has expired or been used, the page offers to send
a new one.

> **Running the site yourself?** During development, emails are not sent.
> They are printed in the server's output instead. Long lines in them are
> split, so the reset link can come out in pieces: the **Check Your Email**
> page has a box that joins it back together.

## Finding Your Way Around

### The Navigation Bar

Once you are logged in, the top of every page has:

| Link | What it shows |
|---|---|
| **Dashboard** | Your starting page, made for your role |
| **Publications** | Every publication |
| **Journalists** | Every journalist |
| **Newsletters** | Every newsletter |
| **Articles** | Every approved article, newest first |
| *Your username* | The account menu: your role, **Account**, **Subscriptions** for readers, and **Log Out** |

### Your Dashboard

Your dashboard is the page you land on after logging in. Each role has its
own, described in that role's section below.

### Buttons Only Where You Can Use Them

Every page shows only the buttons for actions you are allowed to take. A
reader sees **Subscribe** buttons, a journalist sees **+ New Article**, and
an editor sees **Approve** on the articles waiting for them. If a button is
not there, the action is not yours to take.

After most actions, such as saving an article or changing a subscription, a
short message at the top of the page confirms what happened.

## Readers

Readers follow the publications and journalists they care about, and get
their new articles by email.

### The Reader Dashboard

The dashboard shows how many publications and journalists you subscribe to,
and lists the approved articles from your subscriptions under **From Your
Subscriptions**, newest first.

Every approved article on the site, subscribed or not, is on the
**Articles** page.

### Subscribing

There are two kinds of subscription, and they cover different articles:

| Subscribe to | You get |
|---|---|
| **A publication** | Every article it publishes |
| **A journalist** | Only their independent articles, not the ones they write for a publication |

To follow a journalist's publication work too, subscribe to the publication.

**Subscribe** and **Unsubscribe** buttons appear:

- on each publication's page,
- on each journalist's page,
- below each article, in a **Subscribe** section with a row for its
  journalist and, if it has one, its publication.

The **Publications** and **Journalists** lists mark the ones you already
subscribe to.

### The Subscriptions Page

**Subscriptions**, in the account menu, lists every publication and
journalist you subscribe to, each with an **Unsubscribe** button.

### Article Emails

When an article you subscribe to is approved, it is emailed to you, with
its title, author, publication, and full text. Each reader gets their own
copy, so no one sees anyone else's address.

## Journalists

Journalists write the site's articles and newsletters, either for the
publications they work for, or independently, under their own name.

### The Journalist Dashboard

The dashboard brings together everything you can change:

- **Pending Articles** and **Approved Articles:** your own independent
  articles, and all the articles of the publications you work for, by
  anyone on their staff.
- **Newsletters:** the same, for newsletters.
- **My Publications:** the publications you work for.

Each article and newsletter is labeled with its author, and with
**Independent** or its publication's name. The **+ New Article** and
**+ New Newsletter** buttons are at the top.

### Writing an Article

1. Choose **+ New Article**.
2. Enter a title and the article's text.
3. Choose where it belongs, under **Publication**: **Independent**, the
   default, or one of the publications you work for.
4. Save it.

A new article starts as **pending**. Only the people who can approve or
change it can read it, until it is approved.

Once an article is created, its publication cannot be changed. The edit form
shows it as text, not as a choice.

### Approving Your Own Independent Articles

You approve your own independent articles. On the dashboard, or on the
article's page, choose **Approve**, then confirm.

Articles you write for a publication are approved by that publication's
editors instead.

### Editing and Deleting Articles

You can edit and delete:

- your own independent articles,
- every article of the publications you work for, whoever wrote it.

Use the **Edit** and **Delete** buttons on the dashboard or on the article's
page. Editing an approved article keeps it approved. Deleting asks you to
confirm first, and shows how many newsletters will lose the article.

### Putting Together Newsletters

Journalists also put together newsletters from approved articles. See
[Newsletters](#newsletters).

## Editors

Editors are a publication's reviewers. They decide which of its articles go
public.

### The Editor Dashboard: Your Review Queue

The dashboard lists each publication you work for, with its pending
articles, oldest first, so the ones that have waited longest come first. If
you do not work for any publication yet, it says so.

### Approving an Article

1. Choose **Approve** beside a pending article on the dashboard, or open the
   article first to read it, and choose **Approve** on its page.
2. Confirm, on the **Approve Article** page.

Approval is permanent: an approved article cannot be set back to pending.
For what happens next, see [The Life of an Article](#the-life-of-an-article).

You approve only the articles of the publications you work for. Independent
articles are approved by their own journalists.

### Editing and Deleting

You can edit and delete the articles and newsletters of the publications you
work for, using the same pages as journalists. Editors do not write
articles or create newsletters.

## Publishers

Publishers create and own publications, and decide who works for them.

### The Publisher Dashboard

The dashboard shows a card for each publication you own, with its
description and how many editors, journalists, and approved articles it has.
Each card has **View**, **Edit**, and **Delete** buttons, and the
**+ New Publication** button is at the top.

### Creating a Publication

1. Choose **+ New Publication**.
2. Enter a name and a description. Each publication's name must be unique.
3. Choose its staff: tick any of the site's editors under **Editors**, and
   any of its journalists under **Journalists**.
4. Save it.

### Changing the Staff

On **Edit**, rename the publication, change its description, or add and
remove editors and journalists.

Someone removed from the staff loses their rights over the publication's
articles and newsletters at once, even over the articles they wrote.

### Deleting a Publication

**Delete** asks you to confirm, and shows how many articles, newsletters,
and subscribers are affected. Deleting a publication:

- turns its articles into **independent articles** of their authors. They
  keep their approval, and pending ones can then be approved by their
  authors;
- deletes its newsletters;
- deletes its subscriptions.

### What Publishers Do Not Do

Publishers manage publications, not their content. They do not write,
approve, edit, or delete articles or newsletters, and they see only approved
articles.

## The Life of an Article

1. **Written.** A journalist writes the article, for a publication or
   independently. It starts as pending.
2. **Pending.** Only the people who can approve or change it can read it.
   The article's page says so, and anyone else who tries to open it gets
   **Page Not Found**, so its existence stays private.
3. **Approved.** The person responsible approves it: one of its
   publication's editors, or, for an independent article, its journalist.
4. **Published.** At that moment:
   - it appears for every user, on the **Articles** page and on its
     publication's and journalist's pages;
   - it is emailed to its subscribers: the readers who subscribe to its
     publication, or, for an independent article, to its journalist;
   - it is shared with a partner news service, which keeps its own copy.
5. **After publication.** It can still be edited, and it stays approved.
   Edits are not emailed or shared again.

Deleting an approved article also removes it from every newsletter that
included it.

### Who Can Read a Pending Article

| Article | Who can read it before approval |
|---|---|
| A publication's article | That publication's editors and journalists |
| An independent article | Only its author |

## Newsletters

A newsletter is a curated collection of approved articles, with a title and
a description. Journalists create them, independently or for a publication
they work for.

### What a Newsletter Can Include

| Newsletter | Can include |
|---|---|
| **Independent** | Only its author's own approved independent articles |
| **A publication's** | Only that publication's approved articles, by anyone on its staff |

### Creating a Newsletter

1. Choose **+ New Newsletter** on your dashboard.
2. Enter a title and a description.
3. Choose **Independent**, or one of the publications you work for.
4. Tick the articles to include.
5. Save it.

If an article you ticked does not belong in the newsletter you chose, the
form names it, so you can untick it.

### Reading, Editing, and Deleting

- Newsletters are not approved. Every user can read a newsletter as soon as
  it is created. Its page shows each of its articles in full, so it reads
  from top to bottom.
- Newsletters are not emailed to subscribers.
- A newsletter's publication cannot be changed after it is created.
- An independent newsletter can be edited and deleted by its author. A
  publication's newsletter can be edited and deleted by that publication's
  editors and journalists.
- Deleting a newsletter does not delete its articles.

## Who Can Do What

| Action | Reader | Journalist | Editor | Publisher |
|---|:---:|:---:|:---:|:---:|
| Read approved articles and newsletters | Yes | Yes | Yes | Yes |
| Subscribe to publications and journalists | Yes | | | |
| Write articles | | Yes | | |
| Approve articles | | Own independent ones | Their publications' | |
| Edit and delete articles | | Own independent ones, and their publications' | Their publications' | |
| Create newsletters | | Yes | | |
| Edit and delete newsletters | | Own independent ones, and their publications' | Their publications' | |
| Create and manage publications and their staff | | | | Own publications |
