"""View Tests for the moneytracker app.

This module contains unit tests that focus on the behavior of the
views within the moenytracker app. It ensures that views render the
expected templates, redirects occur as anticipated.

Note:
- For referencing URLs within these view tests, use the reverse
function to get the URL from the named URL pattern.
"""
from unittest.mock import patch, Mock

from django.core import mail
from django.test import TestCase
from django.urls import reverse


class TrackerViewTests(TestCase):
    """Tests that the tracker view is working correctly."""

    def test_tracker_view_uses_correct_template(self):
        """Tests that the tracker view uses the correct template."""
        response = self.client.get(reverse('moneytracker:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moneytracker/tracker.html')

    @patch('moneytracker.models.Asset.objects.all')
    def test_tracker_view_get_method(self, mock_assets_all):
        """Test that the tracker view get method is working correctly."""
        mock_assets = [Mock(name='Asset1'), Mock(name='Asset2')]
        mock_assets_all.return_value = mock_assets

        response = self.client.get(reverse('moneytracker:home'))
        self.assertEqual(response.context['assets'], mock_assets)

    # The complex of the next test represents the same complexity of
    # the view itself. For this reason, never stop to refactor the view
    # until the tests are passing. :)
    # Naturally, 'get_or_create' are named in mocks 'goc' for brevity.
    @patch('moneytracker.models.User.objects.get_or_create')
    @patch('moneytracker.models.CustomUser.objects.get_or_create')
    @patch('moneytracker.models.Portfolio.objects.get_or_create')
    @patch('moneytracker.models.Asset.objects.get')
    @patch('moneytracker.models.PortfolioAsset.objects.create')
    def test_tracker_view_post_method(self, mock_portfolio_asset_create,
                                      mock_asset_get, mock_portfolio_goc,
                                      mock_custom_user_goc, mock_user_goc):
        """Test that the tracker view post method is working correctly."""
        mock_user_goc.return_value = (Mock(), True)
        mock_custom_user_goc.return_value = (Mock(), True)
        mock_portfolio_goc.return_value = (Mock(), True)

        response = self.client.post(reverse('moneytracker:home'), {
            'email': 'test@example.com',
            'assets': ['1', '2']
        })

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Confirmation of Portfolio Creation')
        self.assertEqual(mock_asset_get.call_count, 2)
        self.assertEqual(mock_portfolio_asset_create.call_count, 2)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('moneytracker:about'))

        mock_portfolio_asset_create.assert_called()
        mock_asset_get.assert_called()
        mock_portfolio_goc.assert_called_once()
        mock_custom_user_goc.assert_called_once()
        mock_user_goc.assert_called_once_with(email='test@example.com')


class AboutViewTests(TestCase):
    """Tests that the about view is working correctly."""

    def test_about_view_uses_correct_template(self):
        """Tests that the about view uses the correct template."""
        response = self.client.get(reverse('moneytracker:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moneytracker/about.html')


class ContactViewTests(TestCase):
    """Tests that the contact view is working correctly."""

    def test_contact_view_uses_correct_template(self):
        """Test that the contact view uses the correct template."""
        response = self.client.get(reverse('moneytracker:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moneytracker/contact.html')

    def test_contact_view_post_method(self):
        """Test that the contact view post method is working correctly."""
        response = self.client.post(reverse('moneytracker:contact'), {
            'subject': 'Test Subject',
            'message': 'Test Message',
            'to_email': 'test@example.com',
        })

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        self.assertEqual(response.status_code, 200)


class UnsubscribeViewTests(TestCase):
    """Tests that the about view is working correctly."""

    def test_about_view_uses_correct_template(self):
        """Tests that the unsuscribe view uses the correct template."""
        response = self.client.get(reverse('moneytracker:unsubscribe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moneytracker/unsubscribe.html')
