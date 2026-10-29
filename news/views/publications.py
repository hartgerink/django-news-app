"""
The publication pages: the list of publications, and the pages for
reading about, creating, editing, and deleting a publication.
"""

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from accounts.models import User

from ..access import publications_user_can_manage
from ..forms import PublicationForm
from ..models import Publication


@require_GET
def publication_list(request):
    """
    The list of every publication, by name, with its owner and how many
    approved articles it has.

    Publishers, editors and journalists see their own publications
    first, under My Publications, and the rest under Other
    Publications. Readers see one list.

    :param request: The HTTP request.
    :returns: The publication list page.
    """
    publications = (
        Publication.objects.select_related("owner")
        .annotate(
            approved_count=Count(
                "articles",
                filter=Q(articles__approved=True),
            )
        )
        .order_by("name")
    )

    # Only readers subscribe, so only they see which publications they
    # are subscribed to.
    subscribed_ids = set()
    if request.user.role == User.READER:
        subscribed_ids = set(
            request.user.subscribed_publications.values_list("pk", flat=True)
        )

    # A user's own publications: the ones a publisher owns, or the ones
    # an editor or journalist is on the staff of. Readers have none.
    user = request.user
    mine = None
    if user.role == User.PUBLISHER:
        mine = Q(owner=user)
        none_yet = "You don't own any publications yet."
    elif user.role == User.JOURNALIST:
        mine = Q(journalists=user)
        none_yet = "You are not on the staff of any publication yet."
    elif user.role == User.EDITOR:
        mine = Q(editors=user)
        none_yet = "You are not on the staff of any publication yet."

    # Each section has a heading, its publications, and what to say when
    # it has none.
    if mine is not None:
        sections = [
            {
                "heading": "My Publications",
                "publications": publications.filter(mine),
                "empty": none_yet,
            },
            {
                "heading": "Other Publications",
                "publications": publications.exclude(mine),
                "empty": "There are no other publications yet.",
            },
        ]
    else:
        sections = [
            {
                "heading": None,
                "publications": publications,
                "empty": "There are no publications yet.",
            },
        ]

    return render(
        request,
        "news/publication_list.html",
        {"sections": sections, "subscribed_ids": subscribed_ids},
    )


@require_GET
def publication_detail(request, publication_id):
    """
    The page for one publication, with its description, owner, staff,
    approved articles and newsletters.

    An ID that is not a publication's gets "404 Not Found".

    :param request: The HTTP request.
    :param publication_id: The publication's ID, from the URL.
    :returns: The publication's page.
    :raises Http404: If the publication does not exist.
    """
    publication = get_object_or_404(
        Publication.objects.select_related("owner"),
        pk=publication_id,
    )
    user = request.user

    articles = publication.articles.select_related("author")

    # Only the publication's staff can see its pending articles. Its
    # owner sees only approved content.
    sees_pending = (
        publication.editors.filter(pk=user.pk).exists()
        or publication.journalists.filter(pk=user.pk).exists()
    )

    # can_manage decides whether to show the Edit and Delete buttons.
    context = {
        "publication": publication,
        "editors": publication.editors.order_by("username"),
        "journalists": publication.journalists.order_by("username"),
        "approved_articles": articles.filter(approved=True),
        "sees_pending": sees_pending,
        "newsletters": publication.newsletters.select_related("author"),
        "can_manage": publications_user_can_manage(
            user, "news.change_publication"
        )
        .filter(pk=publication.pk)
        .exists(),
    }

    if sees_pending:
        context["pending_articles"] = articles.filter(approved=False)

    # Only readers subscribe, so only they see a Subscribe or
    # Unsubscribe button.
    if user.role == User.READER:
        context["subscribed_to_publication"] = (
            user.subscribed_publications.filter(pk=publication.pk).exists()
        )

    return render(request, "news/publication_detail.html", context)


@user_passes_test(
    lambda user: user.has_perm("news.add_publication"),
    login_url="news:dashboard",
    redirect_field_name=None,
)
@require_http_methods(["GET", "POST"])
def create_publication(request):
    """
    The page where a publisher creates a new publication and chooses
    its editors and journalists.

    Only publishers can create publications. Other users are sent to
    their dashboard.

    :param request: The HTTP request.
    :returns: The publication form, or a redirect to the dashboard once
        the publication is created.
    """
    if request.method == "POST":
        form = PublicationForm(request.POST)

        if form.is_valid():
            # The owner is always the publisher who created it.
            publication = form.save(commit=False)
            publication.owner = request.user
            publication.save()

            # Saves the chosen staff, which needs the publication to be
            # saved first.
            form.save_m2m()

            messages.success(
                request,
                f'Your publication "{publication.name}" was created.',
            )
            return redirect("news:dashboard")
    else:
        form = PublicationForm()

    # Shows an empty form, or the submitted form with its errors.
    return render(request, "news/publication_form.html", {"form": form})


@require_http_methods(["GET", "POST"])
def edit_publication(request, publication_id):
    """
    The page where a publisher edits a publication they own, including
    its staff.

    An editor or journalist taken off the staff loses their rights over
    its content. Anyone but the owner gets "404 Not Found".

    :param request: The HTTP request.
    :param publication_id: The publication's ID, from the URL.
    :returns: The publication form, or a redirect to the dashboard once
        the changes are saved.
    :raises Http404: If the publication does not exist, or the user is
        not its owner.
    """
    publication = get_object_or_404(
        publications_user_can_manage(request.user, "news.change_publication"),
        pk=publication_id,
    )

    if request.method == "POST":
        form = PublicationForm(request.POST, instance=publication)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                f'Your changes to "{publication.name}" were saved.',
            )
            return redirect("news:dashboard")
    else:
        form = PublicationForm(instance=publication)

    # Shows the publication's current values, or the submitted form with
    # its errors.
    return render(
        request,
        "news/publication_form.html",
        {"form": form, "publication": publication},
    )


@require_http_methods(["GET", "POST"])
def delete_publication(request, publication_id):
    """
    The page where a publisher deletes a publication they own, after a
    confirmation.

    Its articles become independent and keep their approval. Its
    newsletters and the subscriptions to it are deleted. Anyone but the
    owner gets "404 Not Found".

    :param request: The HTTP request.
    :param publication_id: The publication's ID, from the URL.
    :returns: The confirmation page, or a redirect to the dashboard once
        the publication is deleted.
    :raises Http404: If the publication does not exist, or the user is
        not its owner.
    """
    publication = get_object_or_404(
        publications_user_can_manage(request.user, "news.delete_publication"),
        pk=publication_id,
    )

    if request.method == "POST":
        # Kept for the message, since the publication is gone once
        # deleted.
        name = publication.name
        publication.delete()

        messages.success(request, f'Your publication "{name}" was deleted.')
        return redirect("news:dashboard")

    # Asks the publisher to confirm, showing how many articles,
    # newsletters and subscribers are affected.
    return render(
        request,
        "news/publication_confirm_delete.html",
        {
            "publication": publication,
            "article_count": publication.articles.count(),
            "newsletter_count": publication.newsletters.count(),
            "subscriber_count": publication.subscribers.count(),
        },
    )
