# Delete all data
# ---------------
# Deletes every user, publication, article, and newsletter, every
# article the simulated third party received, and every login session,
# so the site can start again from empty. The groups and their
# permissions are kept, since they are setup rather than data.
#
# How to run it
# -------------
# From the folder that contains manage.py:
#     python manage.py delete_all_data
# It asks you to type "yes" before deleting anything. To skip the
# question:
#     python manage.py delete_all_data --no-input
# To fill the database again afterward:
#     python manage.py seed_demo_data
#
# It only runs while DEBUG is True, so it cannot empty a live site.

from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import User
from news.models import Article, Newsletter, Publication
from third_party.models import ThirdPartyArticle


class Command(BaseCommand):
    """
    Delete every user, publication, article, newsletter, third-party
    article, and login session.

    Run it with:
        python manage.py delete_all_data

    Superusers are deleted too; seed_demo_data makes the admin
    superuser again. The groups and their permissions are kept, so
    seed_demo_data can be run straight afterward.
    """

    help = (
        "Deletes every user, publication, article, newsletter, "
        "third-party article, and login session. Keeps the groups and "
        "their permissions. Only runs while DEBUG is True."
    )

    def add_arguments(self, parser):
        """
        Add the --no-input option, which skips the "yes" question.

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
        Ask for confirmation, then delete everything in one transaction.

        :raises CommandError: If DEBUG is False, or the answer is not
                              "yes".
        """
        if not settings.DEBUG:
            raise CommandError(
                "delete_all_data only runs while DEBUG is True, so it cannot "
                "empty a live site."
            )

        # What will be deleted, counted first so the question and the
        # final report can show the numbers. For example:
        #     ("users", 8)
        counts = [
            ("users", User.objects.count()),
            ("publications", Publication.objects.count()),
            ("articles", Article.objects.count()),
            ("newsletters", Newsletter.objects.count()),
            ("third-party articles", ThirdPartyArticle.objects.count()),
            ("login sessions", Session.objects.count()),
        ]
        summary = ", ".join(f"{count} {name}" for name, count in counts)

        if options["interactive"]:
            self.stdout.write(
                self.style.WARNING(
                    f"This will permanently delete {summary}. The groups "
                    "and their permissions are kept."
                )
            )
            answer = input('Type "yes" to continue: ')

            if answer.strip().lower() != "yes":
                raise CommandError("Cancelled. Nothing was deleted.")

        # Newsletters, third-party articles, articles, and publications
        # first, then the users, so nothing is left pointing at a
        # deleted user. Deleting the publications and users also deletes
        # their staff and subscription links, and deleting the users
        # deletes their group memberships and any API tokens.
        # Everything happens in one transaction, so if anything fails,
        # nothing is deleted.
        with transaction.atomic():
            Newsletter.objects.all().delete()
            ThirdPartyArticle.objects.all().delete()
            Article.objects.all().delete()
            Publication.objects.all().delete()
            User.objects.all().delete()
            Session.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {summary}."))
        self.stdout.write(
            "To fill the database again, run: "
            "python manage.py seed_demo_data"
        )
