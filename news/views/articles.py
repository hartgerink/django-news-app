from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from accounts.models import User

from ..access import (
    articles_user_can_approve,
    articles_user_can_change,
    articles_visible_to,
)
from ..forms import ArticleForm
from ..models import Article


@require_GET
def article_list(request):
    """
    The list of every approved article on the site, newest first, from
    all publications and all independent journalists.

    Every user sees the same list. It is not limited to the user's
    subscriptions. Pending articles are not listed here. They appear on
    the dashboards of the people who work on them.
    """
    articles = Article.objects.filter(approved=True).select_related(
        "author", "publication"
    )

    return render(
        request,
        "news/article_list.html",
        {"articles": articles},
    )


# Only journalists can write articles. Other users are sent to their
# dashboard.
@user_passes_test(
    lambda user: user.has_perm("news.add_article"),
    login_url="news:dashboard",
    redirect_field_name=None,
)
@require_http_methods(["GET", "POST"])
def create_article(request):
    """
    The page where a journalist writes a new article, either
    independently or for a publication they are on the staff of.

    A new article is pending until it is approved.
    """
    if request.method == "POST":
        form = ArticleForm(request.POST, author=request.user)

        if form.is_valid():
            # The author is always the journalist who wrote it.
            article = form.save(commit=False)
            article.author = request.user
            article.save()

            messages.success(
                request,
                f'Your article "{article.title}" was saved as pending.',
            )
            return redirect("news:dashboard")
    else:
        form = ArticleForm(author=request.user)

    # Shows an empty form, or the submitted form with its errors.
    return render(request, "news/article_form.html", {"form": form})


@require_GET
def article_detail(request, article_id):
    """
    The page for reading one article.

    A user who may not see the article gets "404 Not Found", so the page
    does not reveal that a pending article exists.
    """
    article = get_object_or_404(
        articles_visible_to(request.user).select_related(
            "author", "publication"
        ),
        pk=article_id,
    )

    # Decides which of the Approve, Edit and Delete buttons to show.
    context = {
        "article": article,
        "can_approve": articles_user_can_approve(request.user)
        .filter(pk=article.pk)
        .exists(),
        "can_change": articles_user_can_change(request.user)
        .filter(pk=article.pk)
        .exists(),
    }

    # Only readers subscribe, so only they see Subscribe and Unsubscribe
    # buttons for the article's journalist and publication.
    if request.user.role == User.READER:
        reader = request.user
        context["subscribed_to_author"] = reader.subscribed_journalists.filter(
            pk=article.author_id
        ).exists()
        context["subscribed_to_publication"] = (
            article.publication_id is not None
            and reader.subscribed_publications.filter(
                pk=article.publication_id
            ).exists()
        )

    return render(request, "news/article_detail.html", context)


@require_http_methods(["GET", "POST"])
def approve_article(request, article_id):
    """
    The page for approving a pending article, after a confirmation.

    An editor approves the articles of their publication, and a
    journalist approves their own independent articles. Anyone else gets
    "404 Not Found".
    """
    article = get_object_or_404(
        articles_user_can_approve(request.user).select_related(
            "author", "publication"
        ),
        pk=article_id,
    )

    if request.method == "POST":
        article.approved = True
        article.save()

        messages.success(
            request,
            f'"{article.title}" is approved.',
        )
        return redirect("news:dashboard")

    # Asks the user to confirm before approving.
    return render(
        request,
        "news/article_confirm_approve.html",
        {"article": article},
    )


@require_http_methods(["GET", "POST"])
def edit_article(request, article_id):
    """
    The page for editing an article.

    The author can edit their own independent articles, and the staff of
    a publication can edit its articles. Anyone else gets "404 Not
    Found". An approved article stays approved.
    """
    article = get_object_or_404(
        articles_user_can_change(request.user),
        pk=article_id,
    )

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            instance=article,
            author=article.author,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                f'The changes to "{article.title}" were saved.',
            )
            return redirect("news:dashboard")
    else:
        form = ArticleForm(
            instance=article,
            author=article.author,
        )

    # Shows the article's current values, or the submitted form with its
    # errors.
    return render(
        request,
        "news/article_form.html",
        {"form": form, "article": article},
    )


@require_http_methods(["GET", "POST"])
def delete_article(request, article_id):
    """
    The page for deleting an article, after a confirmation.

    The same users who can edit an article can delete it. Anyone else
    gets "404 Not Found". Deleting it also removes it from every
    newsletter that included it.
    """
    article = get_object_or_404(
        articles_user_can_change(request.user),
        pk=article_id,
    )

    if request.method == "POST":
        # Kept for the message, since the article is gone once deleted.
        title = article.title
        article.delete()

        messages.success(request, f'The article "{title}" was deleted.')
        return redirect("news:dashboard")

    # Asks the user to confirm, showing how many newsletters will lose
    # the article.
    return render(
        request,
        "news/article_confirm_delete.html",
        {
            "article": article,
            "newsletter_count": article.newsletters.count(),
        },
    )
