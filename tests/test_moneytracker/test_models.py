"""
Unit tests for the models of the moneytracker app.
Doesn't require a database so this tests are unit tests.
"""
from django.test import TestCase
from moneytracker.models import Asset, CustomUser, Performance, Portfolio, PortfolioAsset
from django.contrib.auth.models import User
from unittest.mock import patch, Mock

class CustomUserModelTest(TestCase):
    """
    Test that a CustomUser object was created susccessfully
    """
    def setUp(self):
        self.django_user = User(username="Django User")

    @patch('moneytracker.models.CustomUser.save')
    def test_customuser_suscribed_creation(self, mock_save):
        customuser_example = CustomUser(user=self.django_user)
        self.assertEqual(customuser_example.user.username, "Django User")
        self.assertEqual(customuser_example.suscribed, True)
        self.assertEqual(customuser_example.user, self.django_user)
        self.assertEqual(str(customuser_example), "Django User")
        mock_save.assert_not_called()

    @patch('moneytracker.models.CustomUser.save')
    def test_customuser_not_suscribed_creation(self, mock_save):
        customuser_example = CustomUser(suscribed=False, user=self.django_user)
        self.assertEqual(customuser_example.user.username, "Django User")
        self.assertEqual(customuser_example.suscribed, False)
        self.assertEqual(customuser_example.user, self.django_user)
        self.assertEqual(str(customuser_example), "Django User")
        mock_save.assert_not_called()


class AssetModelTest(TestCase):
    """
    Test that a Asset object was instantiated susccessfully
    """
    @patch('moneytracker.models.Asset.save')
    def test_asset_creation(self, mock_save):
        asset_example = Asset(name="Test Name", symbol="TestSymbol", type="Test Type")

        self.assertEqual(asset_example.name, "Test Name")
        self.assertEqual(asset_example.symbol, "TestSymbol")
        self.assertEqual(asset_example.type, "Test Type")
        self.assertEqual(str(asset_example), "Test Name (TestSymbol) - Test Type")
        mock_save.assert_not_called()


class PortfolioModelTest(TestCase):
    """
    Test that a Portfolio object was instantiated successfully using mocks
    """
    @patch('moneytracker.models.Portfolio.save')
    @patch('moneytracker.models.Portfolio.user')
    def test_portfolio_creation(self, mock_user, mock_save):
        mock_user.__str__.return_value = "Mocked CustomUser"
        portfolio_example = Portfolio(user=mock_user)

        self.assertEqual(portfolio_example.user, mock_user)
        self.assertEqual(str(portfolio_example), 'Portfolio of Mocked CustomUser')
        mock_save.assert_not_called()


class PortfolioAssetModelTest(TestCase):
    """
    Test that a PortfolioAsset object was instantiated successfully using mocks
    """
    @patch('moneytracker.models.PortfolioAsset.save')
    @patch('moneytracker.models.PortfolioAsset.portfolio')
    @patch('moneytracker.models.PortfolioAsset.asset')
    def test_portfolioasset_creation(self, mock_asset, mock_portfolio, mock_save):
        mock_asset.name = "Mocked Asset"
        mock_portfolio.user.__str__.return_value = "Mocked Portfolio"
        portfolioasset_example = PortfolioAsset(portfolio=mock_portfolio, asset=mock_asset, quantity=1)

        self.assertEqual(portfolioasset_example.portfolio, mock_portfolio)
        self.assertEqual(portfolioasset_example.asset, mock_asset)
        self.assertEqual(portfolioasset_example.quantity, 1)
        self.assertEqual(str(portfolioasset_example), 'Mocked Asset portfolio of Mocked Portfolio')
        mock_save.assert_not_called()


class PerformanceModelTest(TestCase):
    """
    Test that a Performance object was instantiated successfully using mocks
    """
    @patch('moneytracker.models.Performance.save')
    @patch('moneytracker.models.Performance.user')
    def test_performance_creation(self, mock_user, mock_save):
        mock_user.__str__.return_value = "Mocked CustomUser"
        performance_example = Performance(user=mock_user, days_to_send_email=1)

        self.assertEqual(performance_example.user, mock_user)
        self.assertEqual(performance_example.days_to_send_email, 1)
        self.assertEqual(str(performance_example), 'Performance of Mocked CustomUser')
        mock_save.assert_not_called()
