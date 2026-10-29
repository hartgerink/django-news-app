"""
The news app's configuration, which connects the approval signals.
"""

from django.apps import AppConfig


class NewsConfig(AppConfig):
    """
    The news app's configuration.

    :cvar name: The app's name, which Django uses to find it.
    """

    name = "news"

    def ready(self):
        """
        Connects the approval signals when Django starts, so approving
        an article emails its subscribers and shares it with the third
        party.
        """
        # Imported here, not at the top of the file, because models can
        # only be imported once Django has loaded every app.
        from . import signals  # noqa: F401
