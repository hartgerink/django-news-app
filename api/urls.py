from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "api"

urlpatterns = [
    # Takes a username and password, and returns that user's token,
    # creating it the first time. Its view, obtain_auth_token, comes
    # built into Django REST framework, unlike the views below, which
    # are written in this app's views.py.
    path(
        "token/",
        obtain_auth_token,
        name="token",
    ),
    # Every approved article, and creating an article.
    path(
        "articles/",
        views.articles,
        name="articles",
    ),
    # The approved articles from a reader's subscriptions.
    path(
        "articles/subscribed/",
        views.subscribed,
        name="subscribed",
    ),
    # The pending articles the caller can approve.
    path(
        "articles/pending/",
        views.pending,
        name="pending",
    ),
    # Reading, updating, approving, and deleting one article.
    path(
        "articles/<int:article_id>/",
        views.article_detail,
        name="article_detail",
    ),
]
