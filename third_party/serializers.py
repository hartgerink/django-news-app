"""
The simulated third party's serializer, for the approved articles it
receives.
"""

from rest_framework import serializers

from .models import ThirdPartyArticle


class ThirdPartyArticleSerializer(serializers.ModelSerializer):
    """
    Checks an approved article sent to the simulated third party, and
    turns the saved record back into JSON.

    Every field sent is required: the title, content, journalist's
    username, publication's name, and the article's creation date and
    time. The publication is ``null`` for an independent article.

    :ivar publication: The publication's name. It can be ``null`` for
        an independent article, which is stored as blank.
    """

    publication = serializers.CharField(
        max_length=200,
        allow_null=True,
        allow_blank=True,
    )

    class Meta:
        model = ThirdPartyArticle
        fields = [
            "id",
            "title",
            "content",
            "journalist",
            "publication",
            "created_at",
            "received_at",
        ]
        read_only_fields = ["id", "received_at"]

    def validate_publication(self, publication):
        """
        Turns the null publication sent for an independent article into
        a blank one, since the model's publication can be blank but not
        null.

        :param publication: The publication's name sent, or ``None`` for
            an independent article.
        :returns: The publication's name, or an empty string for an
            independent article.
        """
        return publication or ""
