"""
The REST API's serializer, which turns articles into JSON and checks
the JSON that callers send.
"""

from rest_framework import serializers

from news.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Turns an article into JSON, and checks the JSON sent to create or
    update one.

    A caller sends the title, the content, and, for a new article, its
    publication's ID, or ``null`` for an independent article. The
    author, approval, and creation time are set by the application.

    To check the publication of a new article, the serializer needs the
    request in its context, since the caller is the author.

    :ivar author: The author's username, which is easier to read than
        their ID.
    """

    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "author",
            "publication",
            "approved",
            "created_at",
        ]
        read_only_fields = ["approved", "created_at"]

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
        article = self.instance
        if article is not None:
            if publication != article.publication:
                raise serializers.ValidationError(
                    "An article's publication cannot change once it is "
                    "created."
                )
            return publication

        if publication is None:
            return publication

        author = self.context["request"].user
        if not author.journalist_publications.filter(
            pk=publication.pk
        ).exists():
            raise serializers.ValidationError(
                "Choose a publication you work for, or null for an "
                "independent article."
            )
        return publication
