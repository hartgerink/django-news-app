# Access rules for who may see, change, approve, and manage content.
# Every page and API view follows them by calling these functions, so
# each rule is written once and no two pages can disagree.
#
# Group permissions decide which kinds of actions a role may take. These
# functions decide which publications, articles, and newsletters each
# action applies to. A user's rights over a publication's content come
# from working for it now, so a former editor or journalist has none.

from django.db.models import Q

from .models import Article, Newsletter, Publication


def publications_user_can_manage(user, permission):
    """
    The publications a user may edit or delete.

    A publication is included when all of these are true:
        The user has the permission. Only the Publishers group has it.
        The owner of the publication is the user.

    :param user: User object
    :param permission: The permission the user must have, such as
                       "news.change_publication"
    :return: A queryset of Publication objects.
    """
    if not user.has_perm(permission):
        return Publication.objects.none()

    return Publication.objects.filter(owner=user)


def articles_visible_to(user):
    """
    Distinct articles the user may read.

    An article is included when any one of these is true:
    - The article has been approved.
    - The author of the article is the user, and the article is not
      assigned to a publication.
    - The user is an editor of the article's publication.
    - The user is a journalist of the article's publication.

    Publishers and readers see only approved articles.

    :param user: User object
    :return: A queryset of Article objects.
    """
    return Article.objects.filter(
        Q(approved=True)
        | Q(author=user, publication__isnull=True)
        | Q(publication__editors=user)
        | Q(publication__journalists=user)
    ).distinct()


def subscribed_articles(reader):
    """
    Approved articles from the reader's subscriptions.

    An article is included when it is approved, and any one of these is
    true:
    - Its publication is one the reader subscribes to.
    - Its author is a journalist the reader subscribes to, and the
      article is not assigned to a publication. A subscription to a
      journalist covers only their independent articles.

    :param reader: User object
    :return: A queryset of Article objects.
    """
    return Article.objects.filter(
        Q(publication__in=reader.subscribed_publications.all())
        | Q(
            author__in=reader.subscribed_journalists.all(),
            publication__isnull=True,
        ),
        approved=True,
    )


def articles_user_can_approve(user):
    """
    The pending articles the user may approve.

    An article is included when the user has the approve_article
    permission, the article has not been approved already, and any one
    of these is true:
    - The user is an editor of the article's publication.
    - The author of the article is the user, and the article is not
      assigned to a publication.

    :param user: User object
    :return: A queryset of Article objects.
    """
    if not user.has_perm("news.approve_article"):
        return Article.objects.none()

    return Article.objects.filter(
        Q(publication__editors=user)
        | Q(author=user, publication__isnull=True),
        approved=False,
    )


def articles_user_can_change(user):
    """
    Distinct articles the user may edit or delete.

    An article is included when any one of these is true:
    - The author of the article is the user, and the article is not
      assigned to a publication.
    - The user is an editor of the article's publication.
    - The user is a journalist of the article's publication.

    :param user: User object
    :return: A queryset of Article objects.
    """
    return Article.objects.filter(
        Q(author=user, publication__isnull=True)
        | Q(publication__editors=user)
        | Q(publication__journalists=user)
    ).distinct()


def articles_for_newsletter(journalist, publication):
    """
    The approved articles that can go in a newsletter.

    For an independent newsletter (publication is None), an article is
    included when all of these are true:
        The article has been approved.
        The author of the article is the journalist.
        The article is not assigned to a publication.

    For a publication's newsletter, an article is included when all of
    these are true:
        The article has been approved.
        The article is assigned to the publication.

    :param journalist: User object
    :param publication: Publication object, or None for an independent
                        newsletter
    :return: A queryset of Article objects.
    """
    approved = Article.objects.filter(approved=True)

    if publication is None:
        return approved.filter(author=journalist, publication__isnull=True)

    return approved.filter(publication=publication)


def newsletters_user_can_change(user):
    """
    Distinct newsletters the user may edit or delete.

    A newsletter is included when any one of these is true:
    - The author of the newsletter is the user, and the newsletter is
      not assigned to a publication.
    - The user is an editor of the newsletter's publication.
    - The user is a journalist of the newsletter's publication.

    :param user: User object
    :return: A queryset of Newsletter objects.
    """
    return Newsletter.objects.filter(
        Q(author=user, publication__isnull=True)
        | Q(publication__editors=user)
        | Q(publication__journalists=user)
    ).distinct()
