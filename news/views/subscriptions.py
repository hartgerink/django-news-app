from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET, require_POST

from accounts.models import User

from ..models import Publication


def redirect_back(request):
    """
    Sends the user back to the page they came from, such as the article
    page where they clicked Subscribe.

    The page is named by the form's "next" field. It is used only if it
    is on this site, so a form cannot send the user to another website.
    Otherwise the user goes to their dashboard.
    """
    next_page = request.POST.get("next", "")

    if url_has_allowed_host_and_scheme(
        next_page,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_page)

    return redirect("news:dashboard")


# Only readers have subscriptions. Other users are sent to their
# dashboard.
reader_required = user_passes_test(
    lambda user: user.role == User.READER,
    login_url="news:dashboard",
    redirect_field_name=None,
)


def change_subscription(request, subscriptions, target):
    """
    Subscribes the reader to a journalist or publication, or
    unsubscribes them, as the form's "action" field says.

    The reader is then sent back to the page they came from, with a
    message saying what changed.
    """
    if request.POST.get("action") == "unsubscribe":
        subscriptions.remove(target)
        messages.success(request, f"You are no longer subscribed to {target}.")
    else:
        subscriptions.add(target)
        messages.success(request, f"You are now subscribed to {target}.")

    return redirect_back(request)


# Only a submitted form can change a subscription, never a link.
@reader_required
@require_POST
def journalist_subscription(request, journalist_id):
    """
    Subscribes the reader to a journalist, or unsubscribes them.

    An ID that is not a journalist's gets "404 Not Found".
    """
    journalist = get_object_or_404(
        User,
        pk=journalist_id,
        role=User.JOURNALIST,
    )
    return change_subscription(
        request, request.user.subscribed_journalists, journalist
    )


# Only a submitted form can change a subscription, never a link.
@reader_required
@require_POST
def publication_subscription(request, publication_id):
    """
    Subscribes the reader to a publication, or unsubscribes them.

    An ID that is not a publication's gets "404 Not Found".
    """
    publication = get_object_or_404(Publication, pk=publication_id)
    return change_subscription(
        request, request.user.subscribed_publications, publication
    )


@reader_required
@require_GET
def subscriptions(request):
    """
    The reader's subscriptions page, listing the publications and
    journalists they are subscribed to.
    """
    reader = request.user

    context = {
        "publications": reader.subscribed_publications.order_by("name"),
        "journalists": reader.subscribed_journalists.order_by("username"),
    }
    return render(request, "news/subscriptions.html", context)
