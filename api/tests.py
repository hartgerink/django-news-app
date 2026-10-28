from io import StringIO
from unittest import mock

from django.conf import settings
from django.core import mail
from django.core.management import call_command
from rest_framework import status
from rest_framework.authtoken.models import Token

# APITestCase gives each test a fresh self.client, an APIClient that
# sends requests straight to the app, with no network. It can GET,
# POST, PATCH, and DELETE, send data as JSON, and attach a token to
# every request with credentials().
from rest_framework.test import APITestCase

from accounts.models import User
from news.models import Article, Publication

PASSWORD = "test-password-123"


class ArticleApiTests(APITestCase):
    """
    Tests for the article API, with successful and failed requests in
    each area.

    The email is caught by Django's test mail backend, in mail.outbox,
    and the request to the third party is mocked, so no test sends
    anything.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Creates the data every test starts from: two publications, a
        user of each role, and approved and pending articles.
        """
        # Users can only be saved once their role's group exists.
        call_command("setup_groups_and_permissions", stdout=StringIO())

        cls.publisher = cls.make_user("publisher", User.PUBLISHER)
        cls.gazette_editor = cls.make_user("gazette_editor", User.EDITOR)
        cls.courier_editor = cls.make_user("courier_editor", User.EDITOR)
        cls.gazette_journalist = cls.make_user(
            "gazette_journalist", User.JOURNALIST
        )
        cls.courier_journalist = cls.make_user(
            "courier_journalist", User.JOURNALIST
        )
        cls.reader = cls.make_user("reader", User.READER)

        cls.gazette = Publication.objects.create(
            owner=cls.publisher,
            name="The Lamplight Gazette",
            description="Evening news.",
        )
        cls.gazette.editors.add(cls.gazette_editor)
        cls.gazette.journalists.add(cls.gazette_journalist)

        cls.courier = Publication.objects.create(
            owner=cls.publisher,
            name="The Copper Kettle Courier",
            description="Morning news.",
        )
        cls.courier.editors.add(cls.courier_editor)
        cls.courier.journalists.add(cls.courier_journalist)

        cls.gazette_approved = cls.make_article(
            cls.gazette_journalist, cls.gazette, approved=True
        )
        cls.gazette_pending = cls.make_article(
            cls.gazette_journalist, cls.gazette, approved=False
        )
        cls.courier_approved = cls.make_article(
            cls.courier_journalist, cls.courier, approved=True
        )
        cls.courier_pending = cls.make_article(
            cls.courier_journalist, cls.courier, approved=False
        )
        cls.gazette_journalist_independent = cls.make_article(
            cls.gazette_journalist, None, approved=True
        )
        cls.gazette_journalist_independent_pending = cls.make_article(
            cls.gazette_journalist, None, approved=False
        )
        cls.courier_journalist_independent = cls.make_article(
            cls.courier_journalist, None, approved=True
        )

        cls.reader.subscribed_publications.add(cls.gazette)
        cls.reader.subscribed_journalists.add(cls.courier_journalist)

    @staticmethod
    def make_user(username, role):
        """
        Creates a user with the test password, and an email address
        based on the username.
        """
        return User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password=PASSWORD,
            role=role,
        )

    @staticmethod
    def make_article(author, publication, approved):
        """
        Creates an article for the tests. The tests need both approved
        and pending articles, and this creates either kind without
        sending an email or sharing it with the third party.
        """
        where = publication.name if publication else "Independent"
        return Article.objects.create(
            title=f"{author.username}, {where}, approved={approved}",
            content="Body.",
            author=author,
            publication=publication,
            approved=approved,
        )

    def setUp(self):
        """
        Runs automatically before each test. Django's test framework
        looks for a method with this exact name.

        It replaces requests.post, the requests library's function for
        sending an HTTP POST request, with a mock: a stand-in that sends
        nothing, and only records each call and its arguments. While a
        test runs, the stand-in replaces requests.post for all code.

        The project calls requests.post in one place: share_article in
        news/approval.py, which sends an approved article to the third
        party. So the mock is written for the tests that approve an
        article. Those tests can then check what would have been sent,
        through self.third_party_post. In every other test the mock
        goes unused, which does no harm.
        """
        # Prepares the stand-in for requests.post.
        patcher = mock.patch("requests.post")

        # Puts the stand-in in place, and keeps it for tests to check.
        self.third_party_post = patcher.start()

        # Puts the real requests.post back after the test.
        self.addCleanup(patcher.stop)

    def log_in(self, user):
        """
        A helper the tests call to act as a user. It is not a test, and
        the test framework does not run it automatically.

        It gets the user's API token, creating it if needed, and makes
        the test's client send it in the Authorization header with every
        request that follows, as a real API caller would after getting
        its token from /api/token/. Calling it again with a different
        user switches to that user. Each test starts with a fresh
        client, so a login never carries into the next test.
        """
        token, _ = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def update(self, article, changes):
        """
        A helper the tests call to update an article. It is not a test,
        and the test framework does not run it automatically.

        It sends the changes for the article through the API, as the
        user from log_in, and returns the response, for the test to
        check.

        The app waits until an approval is saved for good before it
        sends the email and the request to the third party. A test's
        changes are never saved for good, because each test is undone
        when it ends, so captureOnCommitCallbacks runs that waiting work
        as soon as the request finishes. Without it, nothing would ever
        be sent, and a test that checks nothing was sent would pass even
        if the app were wrong.
        """
        with self.captureOnCommitCallbacks(execute=True):
            return self.client.patch(
                f"/api/articles/{article.pk}/",
                changes,
                format="json",
            )

    def approve(self, article):
        """
        A helper the tests call to approve an article. It is not a test,
        and the test framework does not run it automatically.

        It sends "approved": true for the article through update, so it
        succeeds only if the user from log_in may approve the article.
        It returns the response, for the test to check.
        """
        return self.update(article, {"approved": True})

    # ==================================================================
    # ========================= Authentication =========================
    # ==================================================================

    def test_user_obtains_token_with_valid_username_and_password(self):
        """
        A user gets their token from /api/token/ with their username and
        password.
        """
        response = self.client.post(
            "/api/token/",
            {"username": self.reader.username, "password": PASSWORD},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["token"],
            Token.objects.get(user=self.reader).key,
        )

    def test_request_without_valid_token_is_rejected(self):
        """
        A request with no token, or with a token that does not exist,
        gets 401 Unauthorized.
        """

        # Test with no token.
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with invalid token
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid-token")
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ==================================================================
    # ======================== Access per role =========================
    # ==================================================================

    def test_article_list_shows_only_approved_articles_to_every_role(self):
        """
        Every role gets the same list from /api/articles/: every
        approved article, and no pending ones, even for editors and
        journalists who can read some pending articles. Those are listed
        by /api/articles/pending/ instead, for the users who can approve
        them.
        """
        approved_ids = set(
            Article.objects.filter(approved=True).values_list("pk", flat=True)
        )

        for user in [
            self.reader,
            self.gazette_journalist,
            self.gazette_editor,
            self.publisher,
        ]:
            # subTest makes each pass of the loop its own sub-test, so a
            # failure names the user's role, and the loop goes on to
            # check the remaining users.
            with self.subTest(role=user.role):
                self.log_in(user)
                response = self.client.get("/api/articles/")

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                listed_ids = {article["id"] for article in response.data}
                self.assertEqual(listed_ids, approved_ids)

    # ==================================================================
    # ====================== Subscribed articles =======================
    # ==================================================================

    def test_reader_gets_only_subscribed_articles(self):
        """
        A reader's subscribed articles are the approved articles of
        their publications, and the approved independent articles of
        their journalists.
        """
        self.log_in(self.reader)
        response = self.client.get("/api/articles/subscribed/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        listed_ids = {article["id"] for article in response.data}

        # The reader subscribes to the Gazette and to the Courier's
        # journalist, so gets exactly these two approved articles, and
        # none of the pending ones.
        expected_ids = {
            self.gazette_approved.pk,
            self.courier_journalist_independent.pk,
        }
        self.assertEqual(listed_ids, expected_ids)

    def test_only_readers_can_list_subscribed_articles(self):
        """
        A reader is allowed to list their subscribed articles. A
        journalist, an editor, and a publisher each get 403 Forbidden.
        """
        # The reader is allowed.
        self.log_in(self.reader)
        response = self.client.get("/api/articles/subscribed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Every other role is refused.
        for user in [
            self.gazette_journalist,
            self.gazette_editor,
            self.publisher,
        ]:
            with self.subTest(role=user.role):
                self.log_in(user)
                response = self.client.get("/api/articles/subscribed/")
                self.assertEqual(
                    response.status_code, status.HTTP_403_FORBIDDEN
                )

    def test_journalist_subscription_excludes_publication_articles(self):
        """
        Subscribing to a journalist covers their independent articles,
        but not the ones they write for a publication.
        """
        self.log_in(self.reader)
        response = self.client.get("/api/articles/subscribed/")

        listed_ids = {article["id"] for article in response.data}

        # The reader subscribes to the Courier's journalist, but not to
        # the Courier.
        self.assertIn(self.courier_journalist_independent.pk, listed_ids)
        self.assertNotIn(self.courier_approved.pk, listed_ids)

    # ==================================================================
    # ======================== Pending articles ========================
    # ==================================================================

    def test_pending_lists_only_articles_the_user_can_approve(self):
        """
        Each user gets only the pending articles they can approve from
        /api/articles/pending/. For an editor, that is their
        publication's pending articles. For a journalist, it is only
        their own pending independent articles, since their
        publication's are approved by its editors.
        """

        # The Gazette Editor is expected to only have access to the
        # one pending article of The Gazette:
        self.log_in(self.gazette_editor)
        response = self.client.get("/api/articles/pending/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        listed_ids = [article["id"] for article in response.data]
        self.assertEqual(listed_ids, [self.gazette_pending.pk])

        # The Gazette Journalist is expected to only have access to the
        # one pending article of of their own independent publication:
        self.log_in(self.gazette_journalist)
        response = self.client.get("/api/articles/pending/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        listed_ids = [article["id"] for article in response.data]
        self.assertEqual(
            listed_ids, [self.gazette_journalist_independent_pending.pk]
        )

    def test_only_editors_and_journalists_can_list_pending_articles(self):
        """
        An editor and a journalist are allowed to list the pending
        articles they can approve. A reader and a publisher each get 403
        Forbidden.
        """
        # The editor and the journalist are each allowed.
        for user in [
            self.gazette_editor,
            self.gazette_journalist,
        ]:
            with self.subTest(role=user.role):
                self.log_in(user)
                response = self.client.get("/api/articles/pending/")
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        # The reader and the publisher are each refused.
        for user in [
            self.reader,
            self.publisher,
        ]:
            with self.subTest(role=user.role):
                self.log_in(user)
                response = self.client.get("/api/articles/pending/")
                self.assertEqual(
                    response.status_code, status.HTTP_403_FORBIDDEN
                )

    # ==================================================================
    # ======================= Creating articles ========================
    # ==================================================================

    def test_journalist_can_create_article_for_their_publication(self):
        """
        A journalist creates an article for their publication. They are
        its author, and it starts as pending.
        """
        self.log_in(self.gazette_journalist)
        response = self.client.post(
            "/api/articles/",
            {
                "title": "A New Article",
                "content": "Body.",
                "publication": self.gazette.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(pk=response.data["id"])
        self.assertEqual(article.author, self.gazette_journalist)
        self.assertEqual(article.publication, self.gazette)
        self.assertFalse(article.approved)

    def test_reader_cannot_create_article(self):
        """
        A reader gets 403 Forbidden, and no article is created.
        """
        self.log_in(self.reader)
        response = self.client.post(
            "/api/articles/",
            {
                "title": "A Reader's Article",
                "content": "Body.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(
            Article.objects.filter(title="A Reader's Article").exists()
        )

    # ==================================================================
    # ================ Approving and deleting articles =================
    # ==================================================================

    def test_editor_can_approve_and_delete_publication_article(self):
        """
        An editor approves a pending article of their publication, and
        deletes an approved one.
        """
        self.log_in(self.gazette_editor)

        response = self.approve(self.gazette_pending)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.gazette_pending.refresh_from_db()
        self.assertTrue(self.gazette_pending.approved)

        response = self.client.delete(
            f"/api/articles/{self.gazette_approved.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Article.objects.filter(pk=self.gazette_approved.pk).exists()
        )

    def test_editor_cannot_approve_other_publication_article(self):
        """
        An editor cannot even see another publication's pending article,
        so trying to approve it gets 404 Not Found, and it stays
        pending.
        """
        self.log_in(self.gazette_editor)
        response = self.approve(self.courier_pending)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.courier_pending.refresh_from_db()
        self.assertFalse(self.courier_pending.approved)

    def test_editor_cannot_delete_other_publication_article(self):
        """
        An editor trying to delete another publication's approved
        article gets 403 Forbidden, and the article is kept. It is 403
        rather than 404 because every user can read approved articles.
        """
        self.log_in(self.gazette_editor)
        response = self.client.delete(
            f"/api/articles/{self.courier_approved.pk}/"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Article.objects.filter(pk=self.courier_approved.pk).exists()
        )

    def test_journalist_can_approve_own_independent_article(self):
        """
        A journalist approves their own pending independent article.
        """
        self.log_in(self.gazette_journalist)
        response = self.approve(self.gazette_journalist_independent_pending)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.gazette_journalist_independent_pending.refresh_from_db()
        self.assertTrue(self.gazette_journalist_independent_pending.approved)

    # ==================================================================
    # ======================== Approval actions ========================
    # ==================================================================

    def test_approval_emails_subscribers_and_shares_article(self):
        """
        Approving a Gazette article emails its subscriber and sends the
        article to the third party with the API key.
        """
        # The Gazette's editor approves its pending article. The checks
        # below test what that approval did.
        self.log_in(self.gazette_editor)
        self.approve(self.gazette_pending)

        # The email: exactly one message was sent, addressed to the
        # reader alone, the Gazette's only subscriber. Each message's
        # "to" is a list of addresses, so the outbox should hold one
        # message whose list is just the reader's.
        email_recipients = [message.to for message in mail.outbox]
        self.assertEqual(email_recipients, [[self.reader.email]])

        # The request to the third party: the article was sent exactly
        # once.
        self.third_party_post.assert_called_once()

        # Gets the arguments that call was made with, as recorded by the
        # stand-in for requests.post, and gives each part a name for the
        # checks below. call.args holds the positional arguments, and
        # call.kwargs the keyword arguments.
        call = self.third_party_post.call_args
        request_url = call.args[0]
        request_headers = call.kwargs["headers"]
        shared_article = call.kwargs["json"]

        # The URL: the request was sent to the third party's endpoint.
        self.assertEqual(request_url, settings.THIRD_PARTY_API_URL)

        # The API key: the request carried it in the X-API-Key header.
        self.assertEqual(
            request_headers, {"X-API-Key": settings.THIRD_PARTY_API_KEY}
        )

        # The article: the JSON body has the approved article's title,
        # its journalist, and its publication.
        self.assertEqual(shared_article["title"], self.gazette_pending.title)
        self.assertEqual(
            shared_article["journalist"], self.gazette_journalist.username
        )
        self.assertEqual(
            shared_article["publication"], "The Lamplight Gazette"
        )

    def test_updating_approved_article_does_not_email_or_share_again(self):
        """
        Updating an article that is already approved sends no email and
        shares nothing, even when "approved": true is sent again.
        """
        self.log_in(self.gazette_editor)
        response = self.update(
            self.gazette_approved,
            {"title": "An Updated Title", "approved": True},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)
        self.third_party_post.assert_not_called()
