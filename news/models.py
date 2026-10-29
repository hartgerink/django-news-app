"""
The news app's models: publications, articles, and newsletters.

Each model sets its own table name, such as ``publication``, in place
of Django's default, such as ``news_publication``.
"""

from django.db import models


class Publication(models.Model):
    """
    A news outlet, owned by a publisher and staffed by editors and
    journalists.

    Working for a publication gives an editor or journalist rights over
    its articles and newsletters. Being removed from its staff ends
    them.

    :ivar owner: The publisher who owns the publication.
    :ivar name: The publication's name, unique across the site.
    :ivar description: A description of the publication.
    :ivar editors: The editors who work for the publication.
    :ivar journalists: The journalists who work for the publication.
    """

    owner = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="owned_publications",
        limit_choices_to={"role": "publisher"},
    )

    name = models.CharField(max_length=200, unique=True)

    description = models.TextField()

    editors = models.ManyToManyField(
        "accounts.User",
        blank=True,
        related_name="editor_publications",
        limit_choices_to={"role": "editor"},
        db_table="publication_editor",
    )

    journalists = models.ManyToManyField(
        "accounts.User",
        blank=True,
        related_name="journalist_publications",
        limit_choices_to={"role": "journalist"},
        db_table="publication_journalist",
    )

    class Meta:
        db_table = "publication"

    def __str__(self):
        """
        Show the publication as its name, such as in the admin and in
        form choices.

        :returns: The publication's name.
        """
        return self.name


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

    title = models.CharField(max_length=200)

    content = models.TextField()

    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="articles",
    )

    publication = models.ForeignKey(
        Publication,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)

    class Meta:
        db_table = "article"
        ordering = ["-created_at"]
        # Whether a role may approve articles at all. Which articles a
        # user may approve is decided by the access rules.
        permissions = [("approve_article", "Can approve article")]

    def __str__(self):
        """
        Show the article as its title, such as in the admin and in form
        choices.

        :returns: The article's title.
        """
        return self.title


class Newsletter(models.Model):
    """
    A curated collection of approved articles, created by a journalist,
    either for a publication or independently.

    :ivar title: The newsletter's title.
    :ivar description: A description of the newsletter.
    :ivar author: The journalist who created the newsletter. Never
        changes.
    :ivar publication: The publication the newsletter is for, or
        ``None`` for an independent newsletter. Set when the newsletter
        is created and never changed. Deleting the publication deletes
        its newsletters.
    :ivar created_at: When the newsletter was created.
    :ivar articles: The articles in the newsletter. Approved articles
        only: the publication's articles, or, for an independent
        newsletter, the author's own independent articles.
    """

    title = models.CharField(max_length=200)

    description = models.TextField()

    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="newsletters",
    )

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="newsletters",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    articles = models.ManyToManyField(
        Article,
        blank=True,
        limit_choices_to={"approved": True},
        related_name="newsletters",
        db_table="newsletter_article",
    )

    class Meta:
        db_table = "newsletter"
        ordering = ["-created_at"]

    def __str__(self):
        """
        Show the newsletter as its title, such as in the admin.

        :returns: The newsletter's title.
        """
        return self.title
