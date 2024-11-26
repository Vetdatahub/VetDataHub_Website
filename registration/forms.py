"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""

from django import forms
from django.contrib.auth.forms import BaseUserCreationForm

from .users import UserModel
from .users import UsernameField
from .utils import _

User = UserModel()


class RegistrationForm(BaseUserCreationForm):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """

    required_css_class = "required "
    email = forms.EmailField(label=_("E-mail"))

    class Meta:
        model = User
        fields = (UsernameField(), "email")



class ResendActivationForm(forms.Form):
    required_css_class = "required"
    email = forms.EmailField(label=_("E-mail"))
