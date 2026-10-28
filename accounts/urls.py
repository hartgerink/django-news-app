from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    # Where a visitor creates an account and chooses their role.
    path(
        "register/",
        views.register,
        name="register",
    ),
    # The logged-in user's account details, with a link to change their
    # password.
    path(
        "account/",
        views.account,
        name="account",
    ),
]
