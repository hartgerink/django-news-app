# Creating Good Documentation with Sphinx

Sphinx builds its web pages from the docstrings in the code, so the pages
are only as good as the docstrings. A docstring that explains its code
clearly, and marks its parts in a way Sphinx understands, becomes a
well-organized, easy-to-read web page.

This guide uses Django News's own docstrings as examples: one for each kind
of code they document. Each example shows the docstring as it is written,
then what Sphinx makes of it, as a model for documenting similar code.
To see a change in the pages, rebuild them, as described in
[Maintaining the Code Documentation](maintaining-the-code-documentation.md#rebuilding-the-pages).

## Contents

- [What a Good Docstring Has](#what-a-good-docstring-has)
- [A Module](#a-module)
- [A Class](#a-class)
- [A Function](#a-function)
- [A Method](#a-method)
- [A Constant](#a-constant)
- [The Markers at a Glance](#the-markers-at-a-glance)

## What a Good Docstring Has

- **A first line that sums it up.** Sphinx puts it first, so readers can
  scan a page and stop where they need to.
- **A plain explanation,** after a blank line: what the code is for, and
  anything a reader would not guess from its name.
- **Markers for its parts,** such as `:param:` and `:returns:`. Sphinx turns
  each kind into its own labeled section.
- **Code in double backticks,** such as ``` ``None`` ```, which Sphinx shows
  in a code font.

Docstrings are written in reStructuredText, the same markup as Sphinx's
`.rst` pages.

## A Module

In Python, every `.py` file is a module, whatever it holds. Classes and
functions are not modules themselves: each one lives inside a module, the
file it is written in. A module's name comes from its folder and
file name: `api/serializers.py` is the module `api.serializers`.

So every Python file gets a module docstring, as the first thing in the
file, saying what the file holds. The classes and functions in it get
docstrings of their own, as the examples below show.

From [`api/serializers.py`](../api/serializers.py):

```python
"""
The REST API's serializer, which turns articles into JSON and checks
the JSON that callers send.
"""
```

**In the documentation:** the text appears under the module's name,
`api.serializers`, before everything the module contains.

## A Class

A class's docstring says what the class stands for. For a Django model, an
`:ivar:` marker describes each of its fields.

From [`news/models.py`](../news/models.py):

```python
class Article(models.Model):
    """
    A news article written by a journalist, either for a publication or
    independently.

    It must be approved before readers can see it.

    :ivar title: The article's title.
    :ivar content: The article's text.
    :ivar author: The journalist who wrote the article. Never changes.
    :ivar publication: The publication the article is for, or ``None``
        for an independent article. Set when the article is created and
        never changed, except that deleting the publication makes the
        article independent.
    :ivar created_at: When the article was created.
    :ivar approved: Whether the article has been approved. Once an
        article is approved, it is never set back to pending.
    """
```

**In the documentation:** the class appears as
`class news.models.Article(*args, **kwargs)`, followed by the description,
then a **Variables** section listing each field in bold, with its
description.

A marker's text can run onto more lines, indented under it, as `publication`
and `approved` do here.

## A Function

A function's docstring says what it does. `:param:` describes each thing it
is given, and `:returns:` describes what it gives back.

From [`news/views/subscriptions.py`](../news/views/subscriptions.py):

```python
def redirect_back(request):
    """
    Sends the user back to the page they came from, such as the article
    page where they clicked Subscribe.

    The page is named by the form's ``next`` field. It is used only if
    it is on this site, so a form cannot send the user to another
    website. Otherwise the user goes to their dashboard.

    :param request: The HTTP request, from the submitted form.
    :returns: A redirect to the page named by ``next``, or to the
        dashboard.
    """
```

**In the documentation:** the function appears with its arguments, as
`redirect_back(request)`, followed by the description, then a
**Parameters** section and a **Returns** section.

## A Method

A method is a function that belongs to a class, and is documented the same
way. Its own arguments are described, but not `self`. `:raises:` names an
error it can raise, and when.

From [`api/serializers.py`](../api/serializers.py), in the
`ArticleSerializer` class:

```python
    def validate_publication(self, publication):
        """
        Refuses a publication the article may not have.

        A new article can be independent, or for a publication its
        author works for. An existing article keeps its publication, so
        sending a different one is refused.

        :param publication: The ``Publication`` sent, or ``None`` for an
            independent article.
        :returns: The publication, if the article may have it.
        :raises ValidationError: If an existing article's publication
            would change, or a new article's publication is not one its
            author works for.
        """
```

**In the documentation:** the method appears inside its class's entry, with
**Parameters**, **Returns**, and **Raises** sections. The **Raises** section
names `ValidationError`, with when it happens.

## A Constant

A constant is a value set once, outside any function. It has no docstring
of its own, so it is documented by comments just above it, each starting
with `#:`. Ordinary `#` comments are left out of the documentation.

From [`news/approval.py`](../news/approval.py):

```python
#: How long to wait for the third party to answer, in seconds, so a slow
#: or missing server cannot hold up an approval.
THIRD_PARTY_TIMEOUT_SECONDS = 5
```

**In the documentation:** the constant appears with its value, as
`THIRD_PARTY_TIMEOUT_SECONDS = 5`, followed by the comment's text.

## The Markers at a Glance

| Marker | Used in | Describes | Shown as |
|---|---|---|---|
| `:param name:` | Functions and methods | One thing the code is given | **Parameters** |
| `:returns:` | Functions and methods | What the code gives back | **Returns** |
| `:raises Error:` | Functions and methods | An error the code can raise, and when | **Raises** |
| `:ivar name:` | Classes | One of the class's attributes, such as a model's field | **Variables** |
| `#:` | Comments above a constant | The constant | The constant's description |

Sphinx's own guide to these markers is
[Info field lists](https://www.sphinx-doc.org/en/master/usage/domains/python.html#info-field-lists).

---

**The code documentation guides:**

- [Reading the Code Documentation](reading-the-code-documentation.md)
- **Creating Good Documentation with Sphinx** (this page)
- [Maintaining the Code Documentation](maintaining-the-code-documentation.md)

[Back to the README](../README.md)
