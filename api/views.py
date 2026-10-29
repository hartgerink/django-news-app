"""
The REST API's article endpoints.

Every endpoint in this file needs a valid token in the
``Authorization`` header, the default for Django REST Framework (DRF)
views set in ``REST_FRAMEWORK`` in ``settings.py``. A request with a
missing or invalid token gets 401 Unauthorized before the view runs.

The endpoint that gives users their tokens is not defined here. It is
DRF's ready-made token view, routed in ``urls.py``, which returns a
user's token for their username and password.
"""

from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import User
from news.access import (
    articles_user_can_approve,
    articles_user_can_change,
    articles_visible_to,
    subscribed_articles,
)
from news.models import Article

from .serializers import ArticleSerializer


def fields_not_valid(errors):
    """
    The response to data with missing or invalid fields, listing each
    field and what is wrong with it.

    :param errors: The errors for each field, such as a serializer's
        ``errors``.
    :returns: A 400 Bad Request response, with the errors.
    """
    return Response(
        {"detail": "Some fields are missing or not valid.", "errors": errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


def contains(articles, article):
    """
    Whether a queryset of articles, such as the ones a user can change,
    includes this article.

    :param articles: A queryset of ``Article`` objects.
    :param article: The ``Article`` object to look for.
    :returns: ``True`` if the queryset includes the article, otherwise
        ``False``.
    """
    return articles.filter(pk=article.pk).exists()


@api_view(["GET", "POST"])
def articles(request):
    """
    GET lists every approved article, newest first.

    POST creates an article written by the caller, which starts as
    pending. Only journalists can create articles.

    :param request: The API request. For POST, the new article as JSON.
    :returns: For GET, the approved articles. For POST, 201 Created,
        with the new article; 403 Forbidden if the caller is not a
        journalist; or 400 Bad Request, with each missing or invalid
        field.
    """
    if request.method == "GET":
        approved = Article.objects.filter(approved=True).select_related(
            "author", "publication"
        )
        return Response(ArticleSerializer(approved, many=True).data)

    if not request.user.has_perm("news.add_article"):
        return Response(
            {"detail": "Only journalists can create articles."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ArticleSerializer(
        data=request.data, context={"request": request}
    )
    if not serializer.is_valid():
        return fields_not_valid(serializer.errors)

    # The caller is the author. Any "approved" value sent is ignored, so
    # the new article is pending.
    serializer.save(author=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def subscribed(request):
    """
    GET lists the approved articles from the caller's subscriptions,
    the same articles as on a reader's dashboard. Only readers have
    subscriptions.

    :param request: The API request.
    :returns: The articles from the caller's subscriptions, or 403
        Forbidden if the caller is not a reader.
    """
    if request.user.role != User.READER:
        return Response(
            {"detail": "Only readers have subscriptions."},
            status=status.HTTP_403_FORBIDDEN,
        )

    articles = subscribed_articles(request.user).select_related(
        "author", "publication"
    )
    return Response(ArticleSerializer(articles, many=True).data)


@api_view(["GET"])
def pending(request):
    """
    GET lists the pending articles the caller can approve, oldest
    first, so the ones that have waited longest come first: a
    publication's articles for its editors, and a journalist's own
    independent articles for them. Only editors and journalists can
    approve articles.

    :param request: The API request.
    :returns: The pending articles the caller can approve, or 403
        Forbidden if the caller cannot approve articles.
    """
    if not request.user.has_perm("news.approve_article"):
        return Response(
            {"detail": "Only editors and journalists can approve articles."},
            status=status.HTTP_403_FORBIDDEN,
        )

    articles = (
        articles_user_can_approve(request.user)
        .select_related("author", "publication")
        .order_by("created_at")
    )
    return Response(ArticleSerializer(articles, many=True).data)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def article_detail(request, article_id):
    """
    GET returns one article.

    PUT updates an article, sending every field, and PATCH updates
    only the fields sent. Either can approve a pending article by
    sending ``"approved": true``.

    DELETE deletes an article.

    Each method follows the same rules as the website.

    :param request: The API request. For PUT and PATCH, the article's
        fields as JSON.
    :param article_id: The article's ID, from the URL.
    :returns: For GET, PUT, and PATCH, the article. For DELETE, 204 No
        Content. A change the caller may not make gets 403 Forbidden,
        and data that is not valid gets 400 Bad Request, each with a
        message saying why.
    :raises Http404: If the article does not exist, or the caller may
        not read it.
    """
    # A caller who may not read the article gets 404, so the response
    # does not reveal that a pending article exists.
    article = get_object_or_404(
        articles_visible_to(request.user).select_related(
            "author", "publication"
        ),
        pk=article_id,
    )

    if request.method == "GET":
        return Response(ArticleSerializer(article).data)

    if not contains(articles_user_can_change(request.user), article):
        return Response(
            {
                "detail": "Only the author of an independent article, or "
                "the staff of an article's publication, can change or "
                "delete it."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Whether this request approves the article. Approval cannot be
    # undone, and sending "approved": true again changes nothing.
    approving = False
    if "approved" in request.data:
        try:
            approved = serializers.BooleanField().to_internal_value(
                request.data["approved"]
            )
        except serializers.ValidationError as error:
            return fields_not_valid({"approved": error.detail})

        if article.approved and not approved:
            return Response(
                {
                    "detail": "An approved article cannot be set back to "
                    "pending."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        approving = approved and not article.approved

    if approving and not contains(
        articles_user_can_approve(request.user), article
    ):
        return Response(
            {
                "detail": "Only a publication's editors can approve its "
                "articles, and only the author can approve an independent "
                "article."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ArticleSerializer(
        article,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    if not serializer.is_valid():
        return fields_not_valid(serializer.errors)

    # Saving the approval runs the approval signals, which email the
    # subscribers and share the article with the third party.
    if approving:
        serializer.save(approved=True)
    else:
        serializer.save()
    return Response(serializer.data)
