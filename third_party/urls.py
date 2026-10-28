from django.urls import path

from . import views

app_name = "third_party"

urlpatterns = [
    # Receives each approved article that the news site shares.
    path(
        "articles/",
        views.receive_article,
        name="receive_article",
    ),
]
