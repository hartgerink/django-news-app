# Seed demo data
# --------------
# Fills a blank database with the sample accounts, publications,
# subscriptions, articles, and newsletters in _demo_data.py, and a
# superuser for the Django admin, for looking at the site and trying it
# out by hand. Unit tests do not use it; each test creates its own
# data.
#
# It only runs on a blank database: one with no users, publications,
# articles, or newsletters. That is what keeps it simple. It creates
# everything in one pass, with no checks for what already exists.
#
# How to run it
# -------------
# From the folder that contains manage.py, after migrate_all and
# setup_groups_and_permissions:
#     python manage.py seed_demo_data
# If the database already has data, empty it first:
#     python manage.py delete_all_data
#     python manage.py seed_demo_data

from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from news.models import Article, Newsletter, Publication

from . import _demo_data as demo_data


class Command(BaseCommand):
    """
    Fill a blank database with the demo data in _demo_data.py.

    Run it on a blank database, after setup_groups_and_permissions:
        python manage.py seed_demo_data

    It stops without changing anything if the database already has any
    users, publications, articles, or newsletters, or if the role groups
    have not been set up. Everything is created in one transaction, so
    if anything fails, the database is left blank.
    """

    help = (
        "Fills a blank database with the demo accounts, publications, "
        "subscriptions, articles, and newsletters, and an admin "
        "superuser. Every demo account's password is "
        f'"{demo_data.PASSWORD}".'
    )

    def handle(self, *args, **options):
        """
        Check that the database is blank, then create the demo data.

        :raises CommandError: If the database is not blank, or the role
                              groups have not been set up yet.
        """
        self.check_database_is_blank()

        try:
            with transaction.atomic():
                users = self.create_users()
                publications = self.create_publications(users)
                subscription_count = self.create_subscriptions(
                    users, publications
                )
                articles = self.create_articles(users, publications)
                self.create_newsletters(users, publications, articles)
        except ImproperlyConfigured as error:
            # Raised by User.save() when a role's group is missing
            raise CommandError(str(error))

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(users)} users, {len(publications)} "
                f"publications, {subscription_count} subscriptions, "
                f"{len(articles)} articles, and "
                f"{len(demo_data.NEWSLETTERS)} newsletters."
            )
        )
        self.stdout.write(
            f'Every demo account\'s password is "{demo_data.PASSWORD}".'
        )

    def check_database_is_blank(self):
        """
        Stop if the database already has any users, publications,
        articles, or newsletters.

        :raises CommandError: If any of them exist, naming how many.
        """
        # For example:
        #     [("users", 8), ("articles", 10)]  # what is already there
        found = [
            (name, model.objects.count())
            for name, model in [
                ("users", User),
                ("publications", Publication),
                ("articles", Article),
                ("newsletters", Newsletter),
            ]
        ]
        found = [(name, count) for name, count in found if count]

        if found:
            summary = ", ".join(f"{count} {name}" for name, count in found)
            raise CommandError(
                f"The database is not blank: it has {summary}. Run "
                "python manage.py delete_all_data first."
            )

    def create_users(self):
        """
        Create each account in USERS, and the superuser in SUPERUSER.
        User.save() puts each one in its role's group.

        :return: The new users, by username. For example:
                 users["Paul"]  # the Publisher Paul
        """
        users = {}
        for details in demo_data.USERS:
            users[details["username"]] = User.objects.create_user(
                username=details["username"],
                email=details["email"],
                password=demo_data.PASSWORD,
                role=details["role"],
            )

        # The superuser has the default role, Reader.
        users[demo_data.SUPERUSER["username"]] = User.objects.create_superuser(
            username=demo_data.SUPERUSER["username"],
            email=demo_data.SUPERUSER["email"],
            password=demo_data.PASSWORD,
        )
        return users

    def create_publications(self, users):
        """
        Create each publication in PUBLICATIONS, with its owner and
        staff.

        :param users: The new users, by username.
        :return: The new publications, by name. For example:
                 publications[demo_data.GAZETTE]
        """
        publications = {}
        for details in demo_data.PUBLICATIONS:
            publication = Publication.objects.create(
                name=details["name"],
                owner=users[details["owner"]],
                description=details["description"],
            )
            publication.editors.set(
                [users[name] for name in details["editors"]]
            )
            publication.journalists.set(
                [users[name] for name in details["journalists"]]
            )
            publications[details["name"]] = publication
        return publications

    def create_subscriptions(self, users, publications):
        """
        Subscribe each Reader in SUBSCRIPTIONS to their publications and
        journalists.

        :param users: The new users, by username.
        :param publications: The new publications, by name.
        :return: How many subscriptions were created.
        """
        count = 0
        for details in demo_data.SUBSCRIPTIONS:
            reader = users[details["reader"]]
            reader.subscribed_publications.set(
                [publications[name] for name in details["publications"]]
            )
            reader.subscribed_journalists.set(
                [users[name] for name in details["journalists"]]
            )
            count += len(details["publications"])
            count += len(details["journalists"])
        return count

    def create_articles(self, users, publications):
        """
        Create each article in ARTICLES, dated days_ago days back.

        Articles created already approved do not email subscribers or
        share the article with the third party, since the approval
        signals only act when a pending article becomes approved.

        :param users: The new users, by username.
        :param publications: The new publications, by name.
        :return: The new articles, by title.
        """
        articles = {}
        for details in demo_data.ARTICLES:
            # None for an independent article
            publication = publications.get(details["publication"])

            article = Article.objects.create(
                title=details["title"],
                content=details["content"],
                author=users[details["author"]],
                publication=publication,
                approved=details["approved"],
            )
            self.backdate(article, details["days_ago"])
            articles[details["title"]] = article
        return articles

    def create_newsletters(self, users, publications, articles):
        """
        Create each newsletter in NEWSLETTERS, with its articles, dated
        days_ago days back.

        :param users: The new users, by username.
        :param publications: The new publications, by name.
        :param articles: The new articles, by title.
        """
        for details in demo_data.NEWSLETTERS:
            newsletter = Newsletter.objects.create(
                title=details["title"],
                description=details["description"],
                author=users[details["author"]],
                # None for an independent newsletter
                publication=publications.get(details["publication"]),
            )
            newsletter.articles.set(
                [articles[title] for title in details["articles"]]
            )
            self.backdate(newsletter, details["days_ago"])

    def backdate(self, item, days_ago):
        """
        Move an article's or newsletter's creation date back by a number
        of days.

        created_at is filled in automatically when an item is first
        saved, and that value cannot be set on creation, so it is
        changed afterward with update(), which writes straight to the
        database. For example:
            self.backdate(article, 3)  # created three days ago

        :param item: The Article or Newsletter just created.
        :param days_ago: How many days ago it should say it was created.
        """
        created_at = timezone.now() - timedelta(days=days_ago)
        type(item).objects.filter(pk=item.pk).update(created_at=created_at)
