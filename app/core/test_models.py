"""
Module for testing models.
"""
# TestCase involves databases
from django.test import TestCase
# get_user_model() retrieves your custom model, and if it fails
# it will retrieve the built-in default Django user model.
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Perform tests on models."""

    def test_create_user_with_email_successful(self):
        """Test create user account using an email is successful."""
        # Initialization: Define a test email.
        email = 'awesome@example.com'
        password = 'passkey123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Check if email is normalized for new users."""
        # Initialzation: 1st email is the registered email
        # and the 2nd one is the new email after it was normalized.
        sample_emails = [
            ['testone@EXAMPLE.COM', 'testone@example.com'],
            ['testtwo@Example.COM', 'testtwo@example.com'],
            ['abc3@ExaMple.COM', 'abc3@example.com'],
            ['abc4@EXAMPLE.com', 'abc4@example.com'],
        ]
        for email, expected in sample_emails:
            # We want to make sure that if emails are saved using
            # create_user(), they get normalized.
            user = get_user_model().objects.create_user(email, "pass123")
            self.assertEqual(user.email, expected)


    def test_new_user_without_email_raises_error(self):
        """Check that if user does not have email, then ValueError is raised."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')


    def test_create_superuser(self):
        """Test for creating a superuser."""
        # create_superuser() is a method to create super user
        user = get_user_model().objects.create_superuser(
            'abc@example.com',
            'pass123'
        )

        self.assertTrue(user.is_superuser)
        # assumes that you have basic access in db in the first place
        self.assertTrue(user.is_staff)
