"""
The accounts app's admin pages: Django's user admin, with the email
address and role added.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class NewsUserAdmin(UserAdmin):
    """
    Django's standard user admin pages, with the email address and role
    added, since every user needs both.

    :cvar add_fieldsets: The fields on the add page, which asks for the
        email address and role too. Without an email address, a second
        added user would break the unique rule.
    :cvar fieldsets: The fields on the edit page, which shows the role
        too.
    :cvar list_display: The columns of the user list, with the role
        added.
    """

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "role")}),
    )

    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    list_display = UserAdmin.list_display + ("role",)
