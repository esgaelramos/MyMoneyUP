"""
Unit tests for the models of the moneytracker app.

Doesn't require a database so this tests are unit tests.
"""
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User
from moneytracker.models import (
    Asset, Portfolio, CustomUser, Performance,
    PortfolioAsset, DailyAssetInfo
)


class CustomUserModelTest(TestCase):
    """Test that a CustomUser object was created susccessfully."""

    def setUp(self):
        """Set up method to initialize the test case."""
        self.django_user = User(username="Django User")

    @patch("moneytracker.models.CustomUser.save")
    def test_customuser_suscribed_creation(self, mock_save):
        """
        Test CustomUser creation with subscribed attribute as True.

        This test function checks if a CustomUser object is created
            correctly with the subscribed attribute set to True by
            verifying that:
        - The user attribute of the CustomUser object is set correctly.
        - The subscribed attribute of the CustomUser object is set to True.
        - The user attribute of the CustomUser object is equal to the provided
            Django user.
        - The __str__ method of the CustomUser object returns the expected
            value.
        - The save method of the CustomUser object is not called.
        """
        customuser_example = CustomUser(user=self.django_user)
        self.assertEqual(customuser_example.user.username, "Django User")
        self.assertEqual(customuser_example.suscribed, True)
        self.assertEqual(customuser_example.user, self.django_user)
        self.assertEqual(str(customuser_example), "Django User")
        mock_save.assert_not_called()

    @patch("moneytracker.models.CustomUser.save")
    def test_customuser_not_suscribed_creation(self, mock_save):
        """
        Test creation of CustomUser with 'subscribed' attribute set to False.

        This test function checks if a CustomUser object is created correctly
            with the 'subscribed' attribute set to False by verifying that:
        - The 'user' attribute of the CustomUser object is set correctly.
        - The 'subscribed' attribute of the CustomUser object is set to False.
        - The '__str__' method of the 'user' object returns the expected value.
        - The 'save' method of the CustomUser object is not called.
        """
        customuser_example = CustomUser(suscribed=False, user=self.django_user)
        self.assertEqual(customuser_example.user.username, "Django User")
        self.assertEqual(customuser_example.suscribed, False)
        self.assertEqual(customuser_example.user, self.django_user)
        self.assertEqual(str(customuser_example), "Django User")
        mock_save.assert_not_called()


class AssetModelTest(TestCase):
    """Test that a Asset object was instantiated susccessfully."""

    @patch("moneytracker.models.Asset.save")
    def test_asset_creation(self, mock_save):
        """
        Test the creation of an Asset object.

        This test function checks if an Asset object is created
        correctly by verifying that:
        - The name attribute of the Asset object is set correctly.
        - The symbol attribute of the Asset object is set correctly.
        - The type attribute of the Asset object is set correctly.
        - The __str__ method of the Asset object returns the expected value.
        - The save method of the Asset object is not called.
        """
        asset_example = Asset(
            name="Test Name",
            symbol="TestSymbol",
            type="Test Type"
        )

        self.assertEqual(asset_example.name, "Test Name")
        self.assertEqual(asset_example.symbol, "TestSymbol")
        self.assertEqual(asset_example.type, "Test Type")
        self.assertEqual(
            str(asset_example),
            "Test Name (TestSymbol) - Test Type"
        )
        mock_save.assert_not_called()


class PortfolioModelTest(TestCase):
    """Test instantiation of PortfolioAsset object with mocks."""

    @patch("moneytracker.models.Portfolio.save")
    @patch("moneytracker.models.Portfolio.user")
    def test_portfolio_creation(self, mock_user, mock_save):
        """
        Test the creation of a Portfolio object.

        This test function checks if a Portfolio object is created
        correctly by verifying that:
        - The user attribute of the Portfolio object is set correctly.
        - The __str__ method of the user object returns the expected value.
        - The save method of the Portfolio object is not called.
        """
        mock_user.__str__.return_value = "Mocked CustomUser"
        portfolio_example = Portfolio(user=mock_user)

        self.assertEqual(portfolio_example.user, mock_user)
        self.assertEqual(
            str(portfolio_example),
            "Portfolio of Mocked CustomUser"
        )
        mock_save.assert_not_called()


class PortfolioAssetModelTest(TestCase):
    """Test instantiation of PortfolioAsset object with mocks."""

    @patch("moneytracker.models.PortfolioAsset.save")
    @patch("moneytracker.models.PortfolioAsset.portfolio")
    @patch("moneytracker.models.PortfolioAsset.asset")
    def test_portfolioasset_creation(
        self,
        mock_asset,
        mock_portfolio,
        mock_save
    ):
        """
        Test the creation of a PortfolioAsset object.

        This test function checks if a PortfolioAsset object is created
        correctly by verifying that:
        - The portfolio attribute of the PortfolioAsset object is set
            correctly.
        - The asset attribute of the PortfolioAsset object is set correctly.
        - The quantity attribute of the PortfolioAsset object is set correctly.
        - The __str__ method of the PortfolioAsset object returns the expected
            value.
        - The save method of the PortfolioAsset object is not called.
        """
        mock_asset.name = "Mocked Asset"
        mock_portfolio.user.__str__.return_value = "Mocked Portfolio"
        portfolioasset_example = PortfolioAsset(
            portfolio=mock_portfolio, asset=mock_asset, quantity=1
        )

        self.assertEqual(portfolioasset_example.portfolio, mock_portfolio)
        self.assertEqual(portfolioasset_example.asset, mock_asset)
        self.assertEqual(portfolioasset_example.quantity, 1)
        self.assertEqual(
            str(portfolioasset_example),
            "Mocked Asset portfolio of Mocked Portfolio"
        )
        mock_save.assert_not_called()


class PerformanceModelTest(TestCase):
    """Test instantiation of PortfolioAsset object with mocks."""

    @patch("moneytracker.models.Performance.save")
    @patch("moneytracker.models.Performance.user")
    def test_performance_creation(self, mock_user, mock_save):
        """
        Test the creation of a Performance object.

        This test function checks if a Performance object is created
        correctly by verifying that:
        - The user attribute of the Performance object is set correctly.
        - The days_to_send_email attribute of the Performance object
            is set correctly.
        - The __str__ method of the user object returns the expected value.
        - The save method of the Performance object is not called.
        """
        mock_user.__str__.return_value = "Mocked CustomUser"
        performance_example = Performance(user=mock_user)

        self.assertEqual(performance_example.user, mock_user)
        self.assertEqual(performance_example.days_to_send_email, 'Monday')
        self.assertEqual(performance_example.periodicity, 'Weekly')
        self.assertEqual(
            str(performance_example),
            "Performance of Mocked CustomUser"
        )
        mock_save.assert_not_called()


class DailyAssetInfoModelTest(TestCase):
    """Test instantiation of DailyAssetInfo object with mocks."""

    @patch("moneytracker.models.DailyAssetInfo.save")
    @patch("moneytracker.models.DailyAssetInfo.asset")
    def test_daily_asset_info_creation(self, mock_asset, mock_save):
        """
        Test the creation of an DailyAssetInfo object.

        This test function checks if an DailyAssetInfo object is created
        correctly by verifying that:
        - The asset attribute of the DailyAssetInfo object is set correctly.
        - The __str__ method of the object returns the expected value.
        - The save method of the DailyAssetInfo object is not called.
        """
        mock_asset.name = "Mocked Asset"

        daily_asset_info_example = DailyAssetInfo(
            asset=mock_asset, price=100,
            volume=50.0, timestamp='2024-12-12'
        )

        self.assertEqual(daily_asset_info_example.asset, mock_asset)
        self.assertEqual(daily_asset_info_example.price, 100)
        self.assertEqual(daily_asset_info_example.volume, 50.0)
        self.assertEqual(
            str(daily_asset_info_example),
            'Mocked Asset - Price: $100 at 2024-12-12'
        )

        mock_save.assert_not_called()
