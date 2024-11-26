import django
from django.test import TestCase

from registration import forms
from registration.users import UserModel


class RegistrationFormTests(TestCase):
    """
    Test the default registration forms.

    """

    def test_registration_form(self):
        """
        Test that ``RegistrationForm`` enforces username constraints
        and matching passwords.

        """
        # Create a user so we can verify that duplicate usernames aren't
        # permitted.
        UserModel().objects.create_user("alice", "alice@example.com", "secret")
        bad_username_error = (
            "Enter a valid username. This value may contain only letters, "
            "numbers, and @/./+/-/_ characters."
        )
        password_didnt_match_error = "The two password fields didn't match."
        if django.VERSION >= (3, 0):
            password_didnt_match_error = "The two password fields didn’t match."

        invalid_data_dicts = [
            # Non-alphanumeric username.
            {
                "data": {
                    "username": "foo/bar",
                    "email": "foo@example.com",
                    "password1": "foo",
                    "password2": "foo",
                },
                "error": ("username", [bad_username_error]),
            },
            # Already-existing username.
            {
                "data": {
                    "username": "alice",
                    "email": "alice@example.com",
                    "password1": "secret",
                    "password2": "secret",
                },
                "error": (
                    "username",
                    ["A user with that username already exists."],
                ),
            },
            # Mismatched passwords.
            {
                "data": {
                    "username": "foo",
                    "email": "foo@example.com",
                    "password1": "foo",
                    "password2": "bar",
                },
                "error": ("password2", [password_didnt_match_error]),
            },
        ]

        for invalid_dict in invalid_data_dicts:
            form = forms.RegistrationForm(data=invalid_dict["data"])
            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors[invalid_dict["error"][0]], invalid_dict["error"][1]
            )

        form = forms.RegistrationForm(
            data={
                "username": "foo",
                "email": "foo@example.com",
                "password1": "o09o@exa.c9om3",
                "password2": "o09o@exa.c9om3"
            }
        )
        self.assertTrue(form.is_valid())