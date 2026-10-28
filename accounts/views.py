from django.contrib.auth import login
from django.contrib.auth.decorators import login_not_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import RegistrationForm


# Open to visitors, since they register before they have an account.
@login_not_required
@require_http_methods(["GET", "POST"])
def register(request):
    """
    The registration page, where a visitor creates an account and
    chooses their role.

    A new user is logged in straight away and sent to their dashboard.
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
    """
    return render(request, "accounts/account.html")
