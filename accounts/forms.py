"""
The accounts app's form: registration, with an email address and a
role.
"""

from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.validators import RegexValidator

from .models import User


class RegistrationForm(UserCreationForm):
    """
    Form to register a new ``User`` account.

    Built on Django's ``UserCreationForm``, which provides the username
    field, the two password fields, and these checks:

    - the username is not already in use.
    - the two passwords match.
    - the password passes Django's password validators.

    This form limits usernames to 20 letters and digits, and adds the
    email and role fields from the ``User`` model. The model makes
    email required and unique, and limits role to the roles in
    ``User.ROLE_CHOICES``, so the form checks both.

    :ivar username: The username field. It replaces the one the form
        would otherwise build from the model, which allows up to 150
        characters, including ``@ . + -`` and ``_``. Here a username is
        at most 20 characters, using only the letters A to Z (upper or
        lower case) and the digits 0 to 9.
    """

    username = UsernameField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9]+$",
                message="Use only letters and digits.",
            ),
        ],
        help_text="Required. 20 characters or fewer. Letters and digits only.",
    )

    class Meta(UserCreationForm.Meta):
        # UserCreationForm is built for Django's built-in User, so it
        # must be pointed at the custom User model.
        model = User
        fields = ["username", "email", "role"]
