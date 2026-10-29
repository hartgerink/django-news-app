"""
The ``migrate_all`` management command.

Builds or updates every table from the models, in one step. It runs
two of Django's own commands in order:

1. ``makemigrations`` writes a migration file for any model change
   that does not have one yet.
2. ``migrate`` applies every migration that has not run yet, creating
   or changing the tables.

On an empty database, such as after ``drop_all_tables``, this creates
every table. The role groups and demo data are not part of it;
afterward::

    python manage.py setup_groups_and_permissions
    python manage.py seed_demo_data

.. rubric:: How to run it

From the folder that contains ``manage.py``::

    python manage.py migrate_all
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Run ``makemigrations``, then ``migrate``.

    Run it with::

        python manage.py migrate_all
    """

    help = (
        "Runs makemigrations, then migrate, to build or update every table "
        "from the models."
    )

    def handle(self, *args, **options):
        """
        Write any missing migrations, then apply every migration.

        :param args: Positional arguments from Django. Not used.
        :param options: The command's options, from Django. Not used.
        """
        call_command("makemigrations")
        call_command("migrate")

        self.stdout.write(self.style.SUCCESS("Migrations complete."))
