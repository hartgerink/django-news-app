"""
The approval signals, which email an article to its subscribers and
share it with the third party when it is approved.

Django calls these handlers before and after every ``Article`` is
saved. They are connected when the app starts, in
``NewsConfig.ready()``.
"""

from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .approval import notify_subscribers, share_article
from .models import Article


@receiver(pre_save, sender=Article)
def remember_previous_approval(sender, instance, **kwargs):
    """
    Before an article is saved, notes whether it was pending, so
    :func:`announce_approval` can tell whether this save approved it.

    :param sender: The model being saved, ``Article``.
    :param instance: The ``Article`` about to be saved.
    :param kwargs: The other arguments of Django's ``pre_save`` signal.
        Not used.
    """
    if instance.pk is None:
        # A new article has no earlier version to compare with, so
        # creating one is never an approval, even when it is created
        # already approved, such as by the demo data.
        instance._was_pending = False
    else:
        instance._was_pending = Article.objects.filter(
            pk=instance.pk,
            approved=False,
        ).exists()


@receiver(post_save, sender=Article)
def announce_approval(sender, instance, **kwargs):
    """
    After an article is saved, emails it to its subscribers and shares
    it with the third party, but only when this save approved it.

    Approving from a page, the admin or the API all run this once, and
    later updates to the article run nothing.

    :param sender: The model that was saved, ``Article``.
    :param instance: The ``Article`` just saved.
    :param kwargs: The other arguments of Django's ``post_save`` signal.
        Not used.
    """
    if instance.approved and instance._was_pending:
        # Waits until the approval is saved for good, so nothing is sent
        # for an approval that is undone.
        transaction.on_commit(lambda: notify_subscribers(instance))
        transaction.on_commit(lambda: share_article(instance))
