from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.core.mail import BadHeaderError
from unittest.mock import patch
from .forms import ContactForm


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("home:home")

    def test_home_view_get_request(self):
        """Test if the form is rendered correctly for a GET request."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home.html")
        self.assertIn("form", response.context)

    @patch("home.views.send_mail", side_effect=BadHeaderError)
    def test_home_view_bad_header(self, mock_send_mail):
        """Test if BadHeaderError is handled correctly."""
        data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "subject": "Test Subject",
            "message": "Test message content",
        }

        response = self.client.post(self.url, data=data)
        self.assertContains(response, "Invalid header found", status_code=200)

    def test_home_view_post_invalid_form(self):
        """Test if an invalid POST request does not send an email and re-renders form."""
        invalid_data = {  # Missing required fields
            "name": "",
            "email": "not-an-email",
            "subject": "",
            "message": "",
        }

        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home.html")
        self.assertIn("form", response.context)

        # Check that no email was sent
        self.assertEqual(len(mail.outbox), 0)


class ContactFormTests(TestCase):
    def test_valid_form(self):
        """Test form with valid data."""
        form_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "This is a test message.",
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        """Test form with missing required fields."""
        form_data = {
            "name": "John Doe",
            "email": "",
            "subject": "",
            "message": "",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("subject", form.errors)
        self.assertIn("message", form.errors)

    def test_invalid_email_format(self):
        """Test form with invalid email format."""
        form_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "subject": "Test Subject",
            "message": "This is a test message.",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
