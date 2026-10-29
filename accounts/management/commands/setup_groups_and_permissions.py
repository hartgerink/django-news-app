"""
The ``setup_groups_and_permissions`` management command, which creates
the four role groups and gives each one its permissions.

.. rubric:: Django management commands

A management command is a task you run from the command line through
``manage.py``, such as ``migrate``, ``runserver``, or
``createsuperuser``. A project can add its own commands, and this file
is one of them.

.. rubric:: How Django finds a command

Django looks in the ``management/commands/`` folder of every app in
``INSTALLED_APPS``. Both ``management/`` and ``management/commands/``
need an ``__init__.py`` file. Each other ``.py`` file in
``management/commands/`` becomes a command named after the file. For
example, this file::

    accounts/management/commands/setup_groups_and_permissions.py

becomes::

    python manage.py setup_groups_and_permissions

.. rubric:: How a command works

The file must contain a class named exactly ``Command``, built on
Django's ``BaseCommand``. When the command runs, Django calls the
class's ``handle()`` method, which is where the work is done. The class
can also have:

- ``help``: the description shown by
  ``python manage.py help <command>``.
- ``add_arguments()``: for options, such as ``--dry-run``.

Inside ``handle()``, ``self.stdout.write()`` prints output, and raising
``CommandError`` stops the command with an error message.

.. rubric:: How to run a command

From the folder that contains ``manage.py``::

    python manage.py <command>

To list every available command, including the project's own::

    python manage.py help

To show one command's description and options::

    python manage.py help <command>
"""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

from accounts.models import User

#: The permissions each role's group gets, as Django permission
#: codenames (``action_model``). Every model here is in the news app.
#: For example::
#:
#:     "add_article"       # may create articles
#:     "view_publication"  # may view publications
#:
#: Most are the four permissions Django creates for every model: add,
#: view, change, and delete. ``approve_article`` is a custom permission,
#: declared in the ``Article`` model's ``Meta`` class. It says only that
#: a role may approve articles at all; ``news/access.py`` decides which
#: articles.
GROUP_PERMISSIONS = {
    User.READER: [
        "view_article",
        "view_newsletter",
        "view_publication",
    ],
    User.PUBLISHER: [
        "view_article",
        "view_newsletter",
        "add_publication",
        "view_publication",
        "change_publication",
        "delete_publication",
    ],
    User.EDITOR: [
        "view_article",
        "change_article",
        "delete_article",
        "approve_article",
        "view_newsletter",
        "change_newsletter",
        "delete_newsletter",
        "view_publication",
    ],
    User.JOURNALIST: [
        "add_article",
        "view_article",
        "change_article",
        "delete_article",
        "approve_article",
        "add_newsletter",
        "view_newsletter",
        "change_newsletter",
        "delete_newsletter",
        "view_publication",
    ],
}


class Command(BaseCommand):
    """
    Create the four role groups and give each group its permissions.

    Run it after the tables are built with ``migrate_all``, and again
    after ``remove_groups_and_permissions``::

        python manage.py setup_groups_and_permissions

    It is safe to run again. Groups that already exist are kept, and
    each group's permissions are replaced with exactly its list in
    :data:`GROUP_PERMISSIONS`, so the groups always match it.
    """

    help = (
        "Creates the Readers, Publishers, Editors, and Journalists groups, "
        "and sets the permissions for each group."
    )

    def handle(self, *args, **options):
        """
        Create or update each group, then set its permissions.

        :param args: Positional arguments from Django. Not used.
        :param options: The command's options, from Django. Not used.
        :raises CommandError: If a permission does not exist yet, which
                              means the migrations have not been run,
                              or a custom permission is not declared.
        """
        news_permissions = Permission.objects.filter(
            content_type__app_label="news"
        )

        for role, codenames in GROUP_PERMISSIONS.items():
            # The group's name comes from the User model, so it always
            # matches the group that User.save() puts users in.
            group_name = User.ROLE_GROUPS[role]
            group, created = Group.objects.get_or_create(name=group_name)

            permissions = news_permissions.filter(codename__in=codenames)

            # Stop if any permission is missing, instead of giving a
            # group only some of its permissions.
            if permissions.count() != len(codenames):
                found = set(permissions.values_list("codename", flat=True))
                missing = ", ".join(sorted(set(codenames) - found))
                raise CommandError(
                    f"Missing permissions for {group_name}: {missing}. "
                    "Run python manage.py migrate first, and check that "
                    "any custom permission is declared in its model."
                )

            group.permissions.set(permissions)

            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{action} {group_name} with "
                    f"{len(codenames)} permissions."
                )
            )
