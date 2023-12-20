"""
URL Tests for the core project.

This module contains unit tests that ensure the correct resolution of URLs
within the core project. The primary focus is to guarantee that expected paths
resolve to the correct views, ensuring the stability of user-facing routes.

Note:
- For URL resolving tests, use the actual URL string (e.g., '/login/')
instead of the named URL pattern.
"""
from django.urls import resolve
from django.test import SimpleTestCase
from core.views import TermsView


class TestUrlsResolves(SimpleTestCase):
    """Tests that the urls are resolving correctly."""

    def test_terms_url_resolves(self):
        """Tests that the terms url is resolving correctly."""
        view = resolve("/terms/")
        self.assertEqual(view.func.view_class, TermsView)
