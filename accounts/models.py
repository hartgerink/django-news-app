"""
The accounts app's model: the custom user, with a role and
subscriptions.
"""

from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ImproperlyConfigured
from django.db import models


class User(AbstractUser):
    """
    A user of the news application, with one of four roles: reader,
    journalist, editor, or publisher.

    The role decides the user's group, and the group decides their
    permissions. Readers can also subscribe to publications and to
    journalists.

    :cvar ROLE_CHOICES: The four roles, ``READER``, ``JOURNALIST``,
        ``EDITOR``, and ``PUBLISHER``, each with the name shown for it.
    :cvar ROLE_GROUPS: The group for each role. The groups, and the
        permissions they grant, must be created during database setup
        for users to be saved.
    :ivar email: The user's email address. Required and unique, because
        password reset links are sent by email and approved articles are
        emailed to subscribers.
    :ivar role: The user's role. Each user has exactly one, chosen at
        registration, and it never changes.
    :ivar subscribed_publications: Readers only. The publications the
        reader subscribes to, covering all of each publication's
        articles.
    :ivar subscribed_journalists: Readers only, and only journalists can
        be subscribed to. The journalists the reader subscribes to,
        covering just each journalist's independent articles, not those
        they write for a publication.
    """

    READER = "reader"
    JOURNALIST = "journalist"
    EDITOR = "editor"
    PUBLISHER = "publisher"

    ROLE_CHOICES = [
        (READER, "Reader"),
        (JOURNALIST, "Journalist"),
        (EDITOR, "Editor"),
        (PUBLISHER, "Publisher"),
    ]

    ROLE_GROUPS = {
        READER: "Readers",
        JOURNALIST: "Journalists",
        EDITOR: "Editors",
        PUBLISHER: "Publishers",
    }

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=READER,
    )

    subscribed_publications = models.ManyToManyField(
        "news.Publication",
        blank=True,
        related_name="subscribers",
        db_table="publication_subscription",
    )

    subscribed_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="subscribers",
        db_table="independent_subscription",
    )

    def save(self, *args, **kwargs):
        """
        Save the user, and place them in their role's group and no
        other.

        :param args: Passed on to Django's ``Model.save()``.
        :param kwargs: Passed on to Django's ``Model.save()``.
        :raises ImproperlyConfigured: If the role's group does not
                                      exist, because the groups have
                                      not been set up yet.
        """
        # Look the group up first, so a missing group stops the save
        # instead of leaving a user with no group.
        group_name = self.ROLE_GROUPS[self.role]
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            raise ImproperlyConfigured(
                f"The {group_name} group does not exist. Complete the "
                "database setup first."
            )

        super().save(*args, **kwargs)

        self.groups.set([group])
