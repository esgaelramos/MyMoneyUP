"""
View Tests for the moneytracker app

This module contains unit tests that focus on the behavior of the views
within the moenytracker app. It ensures that views render the expected templates,
redirects occur as anticipated.

Note:
- For referencing URLs within these view tests, use the reverse function to get
the URL from the named URL pattern.
"""
from django.test import TestCase
from django.urls import reverse

class TrackerViewTests(TestCase):
    """
    Tests that the tracker view is working correctly.
    """
    def test_tracker_view_uses_correct_template(self):
        response = self.client.get(reverse('moneytracker:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moneytracker/tracker.html')


class AboutViewTests(TestCase):
    """
    Tests that the about view is working correctly.
    """
    def test_about_view_uses_correct_template(self):
        response = self.client.get(reverse('moneytracker:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moneytracker/about.html')


class ContactViewTests(TestCase):
    """
    Tests that the contact view is working correctly.
    """
    def test_contact_view_uses_correct_template(self):
        response = self.client.get(reverse('moneytracker:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moneytracker/contact.html')
