"""
The ``remove_groups_and_permissions`` management command.

Deletes the four role groups that ``setup_groups_and_permissions``
creates, which undoes it. Deleting a group also removes its
permissions and every user's membership in it. The permissions
themselves are kept, because Django creates them from the models, and
the user accounts are kept too.

Until the groups are set up again, no user can be saved, because
``User.save()`` needs their role's group to exist.

.. rubric:: How to run it

From the folder that contains ``manage.py``::

    python manage.py remove_groups_and_permissions

It asks you to type ``yes`` before deleting anything. To skip the
question::

    python manage.py remove_groups_and_permissions --no-input

To create the groups again afterward::

    python manage.py setup_groups_and_permissions

It only runs while ``DEBUG`` is ``True``, so it cannot change a live
site.
"""

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

from accounts.models import User


class Command(BaseCommand):
    """
    Delete the Readers, Publishers, Editors, and Journalists groups.

    Run it with::

        python manage.py remove_groups_and_permissions

    Other groups, permissions, and user accounts are not touched.
    """

    help = (
        "Deletes the Readers, Publishers, Editors, and Journalists groups, "
        "with their permissions and memberships. Only runs while DEBUG is "
        "True."
    )

    def add_arguments(self, parser):
        """
        Add the ``--no-input`` option, which skips the ``yes`` question.

        :param parser: The command's argument parser, from Django.
        """
        parser.add_argument(
            "--no-input",
            "--noinput",
            action="store_false",
            dest="interactive",
            help='Delete without asking you to type "yes" first.',
        )

    def handle(self, *args, **options):
        """
        Ask for confirmation, then delete the role groups.

        :param args: Positional arguments from Django. Not used.
        :param options: The command's options, from Django. The
            ``interactive`` option is ``False`` when ``--no-input`` is
            given.
        :raises CommandError: If ``DEBUG`` is ``False``, or the answer
                              is not ``yes``.
        """
        if not settings.DEBUG:
            raise CommandError(
                "remove_groups_and_permissions only runs while DEBUG is "
                "True, so it cannot change a live site."
            )

        # The role groups that exist now. For example:
        #     ["Readers", "Publishers", "Editors", "Journalists"]
        role_groups = Group.objects.filter(name__in=User.ROLE_GROUPS.values())
        names = list(role_groups.values_list("name", flat=True))

        if not names:
            self.stdout.write("There are no role groups to delete.")
            return

        summary = ", ".join(names)

        if options["interactive"]:
            self.stdout.write(
                self.style.WARNING(
                    f"This will permanently delete these groups: {summary}."
                )
            )
            answer = input('Type "yes" to continue: ')

            if answer.strip().lower() != "yes":
                raise CommandError("Cancelled. Nothing was deleted.")

        role_groups.delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {summary}."))
        self.stdout.write(
            "To create them again, run: "
            "python manage.py setup_groups_and_permissions"
        )
