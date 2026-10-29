"""
The third_party app's model: the simulated third party's record of each
approved article it receives.
"""

from django.db import models


class ThirdPartyArticle(models.Model):
    """
    An approved article, as received by the simulated third party.

    It is the third party's own record, so it stores plain text copies
    of the article's details, with no links to the application's other
    tables.

    :ivar title: The article's title.
    :ivar content: The article's text.
    :ivar journalist: The author's username.
    :ivar publication: The publication's name, or blank for an
        independent article.
    :ivar created_at: When the article was created in the application.
    :ivar received_at: When the third party received the article.
    """

    title = models.CharField(max_length=200)

    content = models.TextField()

    journalist = models.CharField(max_length=150)

    publication = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField()

    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "third_party_article"
        ordering = ["-received_at"]

    def __str__(self):
        """
        Show the article as its title, such as in the admin.

        :returns: The article's title.
        """
        return self.title
