from django.contrib import admin

from .models import ThirdPartyArticle

# Register the articles received by the simulated third party, with
# Django's default admin pages.
admin.site.register(ThirdPartyArticle)
