# Drop all tables
# ---------------
# Deletes every table in the project's database: all the site's data,
# Django's own tables, and the records of which migrations have run.
# The database itself is kept, and so are the MariaDB account's rights
# to it, so nothing needs setting up again in MariaDB.
#
# Afterward, the database is empty, and the site cannot run until the
# tables are rebuilt. The usual steps from there:
#     python manage.py migrate_all
#     python manage.py setup_groups_and_permissions
#     python manage.py seed_demo_data
#
# How to run it
# -------------
# From the folder that contains manage.py:
#     python manage.py drop_all_tables
# It asks you to type "yes" before deleting anything. To skip the
# question:
#     python manage.py drop_all_tables --no-input
#
# It only runs while DEBUG is True, so it cannot empty a live site.

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    """
    Delete every table in the project's database.

    Run it with:
        python manage.py drop_all_tables

    The database and the MariaDB account's rights to it are kept.
    """

    help = (
        "Deletes every table in the project's database, keeping the "
        "database itself. Only runs while DEBUG is True."
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
        Ask for confirmation, then delete every table in the database.

        :raises CommandError: If DEBUG is False, the database is not
                              MariaDB or MySQL, or the answer is not
                              "yes".
        """
        if not settings.DEBUG:
            raise CommandError(
                "drop_all_tables only runs while DEBUG is True, so it "
                "cannot empty a live site."
            )

        # Switching off foreign key checks, below, is MariaDB and MySQL
        # syntax, so stop on any other database.
        if connection.vendor != "mysql":
            raise CommandError(
                "drop_all_tables only works with MariaDB or MySQL."
            )

        database_name = connection.settings_dict["NAME"]

        # Every table in the database, whether or not Django created it.
        # For example:
        #     ["accounts_user", "article", "django_migrations", ...]
        tables = connection.introspection.table_names()

        if not tables:
            self.stdout.write(f"{database_name} has no tables to delete.")
            return

        if options["interactive"]:
            self.stdout.write(
                self.style.WARNING(
                    f"This will permanently delete all {len(tables)} tables "
                    f"in {database_name}, with all their data."
                )
            )
            answer = input('Type "yes" to continue: ')

            if answer.strip().lower() != "yes":
                raise CommandError("Cancelled. Nothing was deleted.")

        with connection.cursor() as cursor:
            # Tables that point at each other cannot normally be
            # deleted one at a time, so the checks are switched off
            # while they go, and on again afterward, even if a delete
            # fails.
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            try:
                for table in tables:
                    cursor.execute(
                        f"DROP TABLE {connection.ops.quote_name(table)}"
                    )
            finally:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted all {len(tables)} tables in {database_name}."
            )
        )
        self.stdout.write("To rebuild them, run: python manage.py migrate_all")
