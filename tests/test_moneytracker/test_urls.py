"""URL Tests for the moneytracker app.

This module contains unit tests that ensure the correct resolution of
URLs within the moneytracker app. The primary focus is to guarantee
that expected paths resolve to the correct views, ensuring the stability
of user-facing routes.

Note:
- For URL resolving tests, use the actual URL string (e.g., '/login/')
instead of the named URL pattern.
"""
from django.urls import resolve
from django.test import SimpleTestCase
from moneytracker.views import TrackerView
from moneytracker.views import AboutView
from moneytracker.views import ContactView
from moneytracker.views import UnsubscribeView


class TestUrlsResolves(SimpleTestCase):
    """Tests that the urls are resolving correctly."""

    def test_home_url_resolves(self):
        """Tests that the home url is resolving correctly."""
        view = resolve('/')
        self.assertEqual(view.func.view_class, TrackerView)

    def test_about_url_resolves(self):
        """Tests that the about url is resolving correctly."""
        view = resolve('/about/')
        self.assertEqual(view.func.view_class, AboutView)

    def test_contact_url_resolves(self):
        """Tests that the contact url is resolving correctly."""
        view = resolve('/contact/')
        self.assertEqual(view.func.view_class, ContactView)

    def test_unsubscribe_url_resolves(self):
        """Tests that the unsubscribe url is resolving correctly."""
        view = resolve("/unsubscribe/")
        self.assertEqual(view.func.view_class, UnsubscribeView)
