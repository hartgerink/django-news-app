from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class NewsUserAdmin(UserAdmin):
    """
    Django's standard user admin pages, with the email address and role
    added, since every user needs both.
    """

    # The add page asks for the email address and role too. Without an
    # email address, a second added user would break the unique rule.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "role")}),
    )

    # The edit page shows the role too.
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    list_display = UserAdmin.list_display + ("role",)
