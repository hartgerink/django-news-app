from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from ..access import newsletters_user_can_change
from ..forms import NewsletterForm
from ..models import Newsletter


@require_GET
def newsletter_list(request):
    """
    The list of every newsletter on the site, newest first, with how
    many approved articles each one contains.

    Every user sees the same list.
    """
    newsletters = (
        Newsletter.objects.select_related("author", "publication")
        .annotate(
            article_count=Count(
                "articles",
                filter=Q(articles__approved=True),
            )
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "news/newsletter_list.html",
        {"newsletters": newsletters},
    )


@require_GET
def newsletter_detail(request, newsletter_id):
    """
    The page for reading one newsletter, with its description and
    approved articles.

    An ID that is not a newsletter's gets "404 Not Found".
    """
    newsletter = get_object_or_404(
        Newsletter.objects.select_related("author", "publication"),
        pk=newsletter_id,
    )

    # Decides whether to show the Edit and Delete buttons.
    context = {
        "newsletter": newsletter,
        "articles": newsletter.articles.filter(approved=True).select_related(
            "author", "publication"
        ),
        "can_change": newsletters_user_can_change(request.user)
        .filter(pk=newsletter.pk)
        .exists(),
    }

    return render(request, "news/newsletter_detail.html", context)


# Only journalists can create newsletters. Other users are sent to their
# dashboard.
@user_passes_test(
    lambda user: user.has_perm("news.add_newsletter"),
    login_url="news:dashboard",
    redirect_field_name=None,
)
@require_http_methods(["GET", "POST"])
def create_newsletter(request):
    """
    The page where a journalist puts together a new newsletter from
    approved articles, either independently or for a publication they
    are on the staff of.
    """
    if request.method == "POST":
        form = NewsletterForm(request.POST, author=request.user)

        if form.is_valid():
            # The author is always the journalist who created it.
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()

            # Saves the chosen articles, which needs the newsletter to
            # be saved first.
            form.save_m2m()

            messages.success(
                request,
                f'Your newsletter "{newsletter.title}" was saved.',
            )
            return redirect("news:dashboard")
    else:
        form = NewsletterForm(author=request.user)

    # Shows an empty form, or the submitted form with its errors.
    return render(request, "news/newsletter_form.html", {"form": form})


@require_http_methods(["GET", "POST"])
def edit_newsletter(request, newsletter_id):
    """
    The page for editing a newsletter.

    The author can edit their own independent newsletters, and the staff
    of a publication can edit its newsletters. Anyone else gets "404 Not
    Found".
    """
    newsletter = get_object_or_404(
        newsletters_user_can_change(request.user),
        pk=newsletter_id,
    )

    if request.method == "POST":
        form = NewsletterForm(
            request.POST,
            instance=newsletter,
            author=newsletter.author,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                f'The changes to "{newsletter.title}" were saved.',
            )
            return redirect("news:dashboard")
    else:
        form = NewsletterForm(
            instance=newsletter,
            author=newsletter.author,
        )

    # Shows the newsletter's current values, or the submitted form with
    # its errors.
    return render(
        request,
        "news/newsletter_form.html",
        {"form": form, "newsletter": newsletter},
    )


@require_http_methods(["GET", "POST"])
def delete_newsletter(request, newsletter_id):
    """
    The page for deleting a newsletter, after a confirmation.

    The same users who can edit a newsletter can delete it. Anyone else
    gets "404 Not Found". The articles it contained are not deleted.
    """
    newsletter = get_object_or_404(
        newsletters_user_can_change(request.user),
        pk=newsletter_id,
    )

    if request.method == "POST":
        # Kept for the message, since the newsletter is gone once
        # deleted.
        title = newsletter.title
        newsletter.delete()

        messages.success(request, f'The newsletter "{title}" was deleted.')
        return redirect("news:dashboard")

    # Asks the user to confirm, listing the articles the newsletter
    # contains.
    return render(
        request,
        "news/newsletter_confirm_delete.html",
        {
            "newsletter": newsletter,
            "articles": newsletter.articles.select_related(
                "author", "publication"
            ),
        },
    )
