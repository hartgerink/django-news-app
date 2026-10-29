"""
The accounts app's pages: registration, and the user's account page.
"""

from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import RegistrationForm


@login_not_required
@require_http_methods(["GET", "POST"])
def register(request):
    """
    The registration page, where a visitor creates an account and
    chooses their role.

    It is open to visitors, since they register before they have an
    account. A new user is logged in straight away and sent to their
    dashboard.

    :param request: The HTTP request.
    :returns: The registration page, or a redirect to the new user's
        dashboard once they have registered.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("news:dashboard")
    else:
        form = RegistrationForm()

    # Shows an empty form, or the submitted form with its errors.
    return render(request, "accounts/register.html", {"form": form})


@require_GET
def account(request):
    """
    The logged-in user's account page, with their username and email
    address and a link to change their password.

    :param request: The HTTP request.
    :returns: The account page.
    """
    return render(request, "accounts/account.html")
