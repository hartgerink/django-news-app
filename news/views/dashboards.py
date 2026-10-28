from django.contrib.auth.decorators import login_not_required
from django.db.models import Count, Prefetch, Q
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from accounts.models import User

from ..access import (
    articles_user_can_change,
    newsletters_user_can_change,
    subscribed_articles,
)
from ..models import Article


# Open to visitors, since it is the first page they see.
@login_not_required
@require_GET
def welcome(request):
    """
    The welcome page for visitors, with links to log in and register.

    A logged-in user is sent to their dashboard instead.
    """
    if request.user.is_authenticated:
        return redirect("news:dashboard")

    return render(request, "news/welcome.html")


# Each role has its own dashboard, below. They have no URL of their own,
# since dashboard() shows the one that matches the user's role.


def reader_dashboard(request):
    """
    The reader's dashboard, with how many publications and journalists
    they subscribe to, and the approved articles from those
    subscriptions, newest first.
    """
    reader = request.user

    context = {
        "publication_count": reader.subscribed_publications.count(),
        "journalist_count": reader.subscribed_journalists.count(),
        "subscribed_articles": subscribed_articles(reader).select_related(
            "author", "publication"
        ),
    }
    return render(request, "news/dashboard_reader.html", context)


def journalist_dashboard(request):
    """
    The journalist's dashboard, with the articles and newsletters they
    can change, and the publications they are on the staff of.

    That covers their own independent work and all the content of their
    publications, including what other staff members wrote.
    """
    journalist = request.user

    articles = articles_user_can_change(journalist).select_related(
        "author", "publication"
    )

    context = {
        "pending_articles": articles.filter(approved=False),
        "approved_articles": articles.filter(approved=True),
        "newsletters": newsletters_user_can_change(journalist).select_related(
            "author", "publication"
        ),
        "publications": journalist.journalist_publications.order_by("name"),
    }
    return render(request, "news/dashboard_journalist.html", context)


def editor_dashboard(request):
    """
    The editor's dashboard: their review queue.

    It lists each publication they are on the staff of, with its pending
    articles, oldest first, so the ones that have waited longest come
    first.
    """
    publications = request.user.editor_publications.order_by(
        "name"
    ).prefetch_related(
        Prefetch(
            "articles",
            queryset=Article.objects.filter(approved=False)
            .select_related("author")
            .order_by("created_at"),
            to_attr="pending_articles",
        )
    )

    return render(
        request,
        "news/dashboard_editor.html",
        {"publications": publications},
    )


def publisher_dashboard(request):
    """
    The publisher's dashboard, with each publication they own and how
    many editors, journalists and approved articles it has.
    """
    # Publishers see only approved content, so pending articles are not
    # counted.
    publications = request.user.owned_publications.annotate(
        editor_count=Count(
            "editors",
            distinct=True,
        ),
        journalist_count=Count(
            "journalists",
            distinct=True,
        ),
        approved_count=Count(
            "articles",
            filter=Q(articles__approved=True),
            distinct=True,
        ),
    ).order_by("name")

    return render(
        request,
        "news/dashboard_publisher.html",
        {"publications": publications},
    )


@require_GET
def dashboard(request):
    """
    The logged-in user's dashboard, where users land after logging in
    or registering.

    Every role shares this one page, which shows the dashboard for the
    user's role.
    """
    dashboards = {
        User.READER: reader_dashboard,
        User.JOURNALIST: journalist_dashboard,
        User.EDITOR: editor_dashboard,
        User.PUBLISHER: publisher_dashboard,
    }

    # A user without a known role gets the reader's dashboard, which
    # shows only approved content.
    role_dashboard = dashboards.get(request.user.role, reader_dashboard)
    return role_dashboard(request)
