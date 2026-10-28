from django.contrib import admin

from .models import Article, Newsletter, Publication

# Register the publications, articles and newsletters, with Django's
# default admin pages.
admin.site.register(Publication)
admin.site.register(Article)
admin.site.register(Newsletter)
