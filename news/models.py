from django.db import models


class Publication(models.Model):
    """
    A news outlet, owned by a publisher and staffed by editors and
    journalists.

    Working for a publication gives an editor or journalist rights over
    its articles and newsletters. Being removed from its staff ends
    them.
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
        return self.name


class Article(models.Model):
    """
    A news article written by a journalist, either for a publication or
    independently.

    It must be approved before readers can see it.
    """

    title = models.CharField(max_length=200)

    content = models.TextField()

    # The journalist who wrote it. Never changes.
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="articles",
    )

    # Empty for an independent article. Set when the article is created
    # and never changed, except that deleting the publication makes the
    # article independent.
    publication = models.ForeignKey(
        Publication,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Once an article is approved, it is never set back to pending.
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = "article"
        ordering = ["-created_at"]
        # Whether a role may approve articles at all. Which articles a
        # user may approve is decided by the access rules.
        permissions = [("approve_article", "Can approve article")]

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """
    A curated collection of approved articles, created by a journalist,
    either for a publication or independently.
    """

    title = models.CharField(max_length=200)

    description = models.TextField()

    # The journalist who created it. Never changes.
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="newsletters",
    )

    # Empty for an independent newsletter. Set when the newsletter is
    # created and never changed. Deleting the publication deletes its
    # newsletters.
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="newsletters",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Approved articles only: the publication's articles, or for an
    # independent newsletter, the author's own independent articles.
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
        return self.title
