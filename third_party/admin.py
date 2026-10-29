"""
The simulated third party's admin page.

Registers the articles received by the simulated third party, with
Django's default admin pages.
"""

from django.contrib import admin

from .models import ThirdPartyArticle

admin.site.register(ThirdPartyArticle)
