"""This module contains test cases for the moneytracker application."""

import datetime
from unittest.mock import patch

from django.test import TestCase
from moneytracker.management.commands.send_tracker import Command
from moneytracker.models import (
    Asset, CustomUser, DailyAssetInfo, Performance, Portfolio, PortfolioAsset,
    User
)


class GetTodayUsersTest(TestCase):
    """Tests for retrieving users whose email day is today."""

    @patch('moneytracker.management.commands.send_tracker.datetime')
    def test_get_today_users(self, mock_datetime):
        """
        Test `get_today_users`.

        Returns the user that is set to receive emails on a known date.
        """
        # Set the current date to a known value
        mock_datetime.date.today.return_value = datetime.date(2022, 1, 1)

        # Create a mock user
        user = User.objects.create(username='testuser', password='password')
        custom_user = CustomUser.objects.create(user=user)

        # Create a Performance object for the user with the same date
        Performance.objects.create(
            user=custom_user, periodicity='Daily', days_to_send_email='Sunday')

        # Call the method under test
        command = Command()
        result = command.get_today_users()

        # Assert that the user is in the result
        self.assertIn(custom_user, result)


class GetUserPortfoliosAssetsTest(TestCase):
    """Tests for retrieving portfolio assets for a given user."""

    def setUp(self):
        """Set up test data for GetUserPortfoliosAssetsTest."""
        # Create a mock user
        user = User.objects.create(username='testuser', password='password')
        self.custom_user = CustomUser.objects.create(user=user)
        # Create a mock portfolio for the user
        self.portfolio = Portfolio.objects.create(user=self.custom_user)
        # Create mock assets
        self.asset1 = Asset.objects.create(name='Asset 1', symbol='ASSET1')
        self.asset2 = Asset.objects.create(name='Asset 2', symbol='ASSET2')
        # Create portfolio assets
        self.portfolio_asset1 = PortfolioAsset.objects.create(
            portfolio=self.portfolio, asset=self.asset1, quantity=1)
        self.portfolio_asset2 = PortfolioAsset.objects.create(
            portfolio=self.portfolio, asset=self.asset2, quantity=1)

    def test_get_user_portfolios_assets(self):
        """Test `get_user_portfolios_assets` returns the correct assets."""
        # Call the method under test
        command = Command()
        result = command.get_user_portfolios_assets(user=self.custom_user)

        # Assert that the portfolio assets are in the result
        self.assertIn(self.portfolio_asset1, result)
        self.assertIn(self.portfolio_asset2, result)


class GetUserAssetsTest(TestCase):
    """Tests for retrieving all assets for a given user."""

    def setUp(self):
        """Set up test data for GetUserAssetsTest."""
        # Create a mock user
        self.user = User.objects.create(
            username='testuser', password='password')
        self.custom_user = CustomUser.objects.create(user=self.user)
        # Create a mock portfolio for the user
        self.portfolio = Portfolio.objects.create(user=self.custom_user)
        # Create mock assets
        self.asset1 = Asset.objects.create(name='Asset 1', symbol='ASSET1')
        self.asset2 = Asset.objects.create(name='Asset 2', symbol='ASSET2')
        # Create portfolio assets
        self.portfolio_asset1 = PortfolioAsset.objects.create(
            portfolio=self.portfolio, asset=self.asset1, quantity=1)
        self.portfolio_asset2 = PortfolioAsset.objects.create(
            portfolio=self.portfolio, asset=self.asset2, quantity=1)

    def test_get_user_assets(self):
        """Test `get_user_assets` returns all assets owned by a given user."""
        # Call the method under test
        command = Command()
        result = command.get_user_assets(user=self.custom_user)

        # Assert that the assets are in the result
        self.assertIn(self.asset1, result)
        self.assertIn(self.asset2, result)


class GetAssetInfoTest(TestCase):
    """Tests for retrieving asset information."""

    def setUp(self):
        """Set up test data for GetAssetInfoTest."""
        # Create a mock asset
        self.asset = Asset.objects.create(name='Asset 1', symbol='ASSET1')
        # Create a mock DailyAssetInfo for the asset
        self.daily_asset_info = DailyAssetInfo.objects.create(
            asset=self.asset, price=100.00, volume=1000.00)

    def test_get_asset_info(self):
        """Test `get_asset_info` returns the DailyAssetInfo for a given asset."""  # noqa: E501
        # Call the method under test
        command = Command()
        result = command.get_asset_info(self.asset)

        # Assert that the returned DailyAssetInfo is correct
        self.assertEqual(result, self.daily_asset_info)
