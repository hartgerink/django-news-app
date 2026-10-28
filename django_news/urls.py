"""
URL configuration for django_news project.

The `urlpatterns` list routes URLs to views. For more information please
see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function:
       from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    # ==================================================================
    # ========================== Django admin ==========================
    # ==================================================================
    path(
        "admin/",
        admin.site.urls,
    ),
    # ==================================================================
    # =============== Django built-in account management ===============
    # ==================================================================
    # These keep Django's plain URL names, because the password views
    # find each other by those names.
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    # Changing the password of a logged-in user, in two steps.
    # Part 1 of 2: the form for the current and new password.
    path(
        "accounts/password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    # Part 2 of 2: confirms the password was changed.
    path(
        "accounts/password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # Resetting a forgotten password by email, in four steps.
    # Part 1 of 4: the form for the account's email address.
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    # Part 2 of 4: says the reset email was sent.
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    # Part 3 of 4: opened from the link in the reset email, to choose a
    # new password.
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # Part 4 of 4: confirms the password was reset.
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # ==================================================================
    # ========================== accounts app ==========================
    # ==================================================================
    # The project's own account pages: registration and the account
    # page.
    path(
        "accounts/",
        include("accounts.urls"),
    ),
    # ==================================================================
    # ============================ news app ============================
    # ==================================================================
    # The news site's pages, starting from the home page.
    path(
        "",
        include("news.urls"),
    ),
    # ==================================================================
    # ============================ api app =============================
    # ==================================================================
    # The news site's API.
    path(
        "api/",
        include("api.urls"),
    ),
    # ==================================================================
    # ======================== third_party app =========================
    # ==================================================================
    # The simulated third party, which receives approved articles.
    path(
        "third-party/",
        include("third_party.urls"),
    ),
]
