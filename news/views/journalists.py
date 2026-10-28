from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from accounts.models import User


@require_GET
def journalist_list(request):
    """
    The list of every journalist, by username, with the publications
    they are on the staff of and how many approved articles they have.
    """
    journalists = (
        User.objects.filter(role=User.JOURNALIST)
        .annotate(
            approved_count=Count(
                "articles",
                filter=Q(articles__approved=True),
            )
        )
        .prefetch_related("journalist_publications")
        .order_by("username")
    )

    # Only readers subscribe, so only they see which journalists they
    # are subscribed to.
    subscribed_ids = set()
    if request.user.role == User.READER:
        subscribed_ids = set(
            request.user.subscribed_journalists.values_list("pk", flat=True)
        )

    return render(
        request,
        "news/journalist_list.html",
        {
            "journalists": journalists,
            "subscribed_ids": subscribed_ids,
        },
    )


@require_GET
def journalist_detail(request, journalist_id):
    """
    The page for one journalist, with the publications they are on the
    staff of and their approved independent articles.

    An ID that is not a journalist's gets "404 Not Found".
    """
    journalist = get_object_or_404(
        User,
        pk=journalist_id,
        role=User.JOURNALIST,
    )

    # Only independent articles are listed, since a subscription to a
    # journalist covers only those.
    context = {
        "journalist": journalist,
        "publications": journalist.journalist_publications.order_by("name"),
        "approved_articles": journalist.articles.filter(
            approved=True,
            publication__isnull=True,
        ),
    }

    # Only readers subscribe, so only they see a Subscribe or
    # Unsubscribe button.
    if request.user.role == User.READER:
        context["subscribed_to_journalist"] = (
            request.user.subscribed_journalists.filter(
                pk=journalist.pk
            ).exists()
        )

    return render(request, "news/journalist_detail.html", context)
