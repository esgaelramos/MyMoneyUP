"""
View Tests for the core project

This module contains unit tests that focus on the behavior of the views
within the core project. It ensures that views render the expected templates,
redirects occur as anticipated.

Note:
- For referencing URLs within these view tests, use the reverse function to get
the URL from the named URL pattern.
"""
from django.test import TestCase
from django.urls import reverse

class TermsViewTest(TestCase):
    """
    Tests that the terms view is working correctly.
    """
    def test_terms_view_uses_correct_template(self):
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'terms/terms.html')
        
class Custom404ViewTest(TestCase):
    """
    Tests that the custom 404 view is working correctly.
    """
    def test_custom_404_view_uses_correct_template(self):
        response = self.client.get('not-exists-url')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')