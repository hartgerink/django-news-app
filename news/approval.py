import logging

import requests
from django.conf import settings
from django.core.mail import send_mass_mail

logger = logging.getLogger(__name__)

# How long to wait for the third party to answer, so a slow or missing
# server cannot hold up an approval.
THIRD_PARTY_TIMEOUT_SECONDS = 5


def get_recipients(article):
    """
    The email addresses of the readers subscribed to an approved
    article.

    A publication article goes to the publication's subscribers. An
    independent article goes to its author's subscribers.
    """
    if article.publication is not None:
        subscribers = article.publication.subscribers
    else:
        subscribers = article.author.subscribers

    return list(subscribers.values_list("email", flat=True))


def notify_subscribers(article):
    """
    Emails an approved article to each of its subscribers.

    Each reader gets their own copy, so no reader sees the other
    readers' addresses. A failure is logged, and the approval still
    stands.
    """
    where = article.publication.name if article.publication else "Independent"
    subject = f"New article: {article.title}"
    body = (
        f"{article.title}\n"
        f"By {article.author.username}, {where}\n\n"
        f"{article.content}\n"
    )

    # One message for each reader, sent from the site's own address.
    messages = [
        (subject, body, None, [address]) for address in get_recipients(article)
    ]

    try:
        send_mass_mail(messages)
    except Exception:
        logger.warning(
            f"Could not email the subscribers of article {article.pk}.",
            exc_info=True,
        )


def share_article(article):
    """
    Sends an approved article to the third-party API as JSON.

    A failure of any kind is logged, and the approval still stands.
    """
    # Plain text copies of the article's details, in the fields the
    # third party stores.
    payload = {
        "title": article.title,
        "content": article.content,
        "journalist": article.author.username,
        "publication": (
            article.publication.name if article.publication else None
        ),
        "created_at": article.created_at.isoformat(),
    }

    try:
        response = requests.post(
            settings.THIRD_PARTY_API_URL,
            json=payload,
            headers={"X-API-Key": settings.THIRD_PARTY_API_KEY},
            timeout=THIRD_PARTY_TIMEOUT_SECONDS,
        )
        # An error answer from the third party counts as a failure too.
        response.raise_for_status()
    except requests.RequestException:
        logger.warning(
            f"Could not share article {article.pk} with the third party.",
            exc_info=True,
        )
