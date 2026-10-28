from django.db import models


class ThirdPartyArticle(models.Model):
    """
    An approved article, as received by the simulated third party.

    It is the third party's own record, so it stores plain text copies
    of the article's details, with no links to the application's other
    tables.
    """

    title = models.CharField(max_length=200)

    content = models.TextField()

    # The author's username.
    journalist = models.CharField(max_length=150)

    # The publication's name, or blank for an independent article.
    publication = models.CharField(max_length=200, blank=True)

    # When the article was created in the application.
    created_at = models.DateTimeField()

    # When the third party received it.
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "third_party_article"
        ordering = ["-received_at"]

    def __str__(self):
        return self.title
