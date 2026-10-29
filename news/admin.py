"""
The news app's admin pages.

Registers the publications, articles and newsletters, with Django's
default admin pages.
"""

from django.contrib import admin

from .models import Article, Newsletter, Publication

admin.site.register(Publication)
admin.site.register(Article)
admin.site.register(Newsletter)
