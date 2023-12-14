"""
Test cases for the models of the moneytracker app.
Requiere a database (default: sqlite3) so this tests are integration tests.
Only here check the 'contrains' conflicts and working. 
"""
import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.utils import IntegrityError
from moneytracker.models import Asset, CustomUser, Performance, Portfolio, PortfolioAsset

class CustomUserModelIntegrationTest(TestCase):
    """
    Test that a CustomUser object was created susccessfully
    """
    def setUp(self):
        self.django_user = User.objects.create(username='Django User')

    def test_customuser_suscribed_creation(self):
        customuser_example = CustomUser.objects.create(user=self.django_user)

        self.assertEqual(customuser_example.user.username, 'Django User')
        self.assertEqual(customuser_example.suscribed, True)
        self.assertEqual(customuser_example.user, self.django_user)

    def test_customuser_not_suscribed_creation(self):
        customuser_example = CustomUser.objects.create(suscribed=False, user=self.django_user)

        self.assertEqual(customuser_example.user.username, 'Django User')
        self.assertEqual(customuser_example.suscribed, False)
        self.assertEqual(customuser_example.user, self.django_user)


class AssetModelIntegrationTest(TestCase):
    """
    Test that a Asset object was created susccessfully
    """
    def test_asset_creation(self):
        asset_example = Asset.objects.create(name='Test Name',
                                            symbol='TestSymbol',
                                            type="Test Type")

        self.assertEqual(asset_example.name, 'Test Name')
        self.assertEqual(asset_example.symbol, 'TestSymbol')
        self.assertEqual(asset_example.type, "Test Type")


class PortfolioModelIntegrationTest(TestCase):
    """
    Test that a Portfolio object was created susccessfully
    """
    def setUp(self):
        django_user = User.objects.create(username='Django User')
        self.customuser_example = CustomUser.objects.create(user=django_user)
        
    def test_portfolio_creation(self):
        portfolio_example = Portfolio.objects.create(user=self.customuser_example)

        self.assertEqual(portfolio_example.user.user.username, 'Django User')


class PortfolioAssetModelIntegrationTest(TestCase):
    """"
    Test that a PortfolioAsset object was created susccessfully
    """
    def setUp(self):
        django_user = User.objects.create(username='DjangoUser')
        custom_user = CustomUser.objects.create(user=django_user)
        self.asset = Asset.objects.create(name='Test Asset', symbol='TA', type='Test Type')
        self.portfolio = Portfolio.objects.create(user=custom_user)

    def test_portfolio_asset_creation(self):
        acquisition_date = datetime.date.today()
        portfolio_asset_example = PortfolioAsset.objects.create(
            portfolio=self.portfolio,
            asset=self.asset,
            quantity=10.0,
            acquisition_date=acquisition_date
        )

        self.assertEqual(portfolio_asset_example.portfolio.user.user.username, 'DjangoUser')
        self.assertEqual(portfolio_asset_example.asset.name, 'Test Asset')
        self.assertEqual(portfolio_asset_example.quantity, 10.0)
        self.assertEqual(portfolio_asset_example.acquisition_date, datetime.date.today())

    def test_unique_portfolio_asset_contraint(self):
        acquisition_date = datetime.date.today()
        PortfolioAsset.objects.create(
            portfolio=self.portfolio,
            asset=self.asset,
            quantity=10.0,
            acquisition_date=acquisition_date
        )
        # Try create a second object PortfolioAsset with same values and catch the exception
        with self.assertRaises(IntegrityError):
            PortfolioAsset.objects.create(
                portfolio=self.portfolio,
                asset=self.asset,
                quantity=10.0,
                acquisition_date=acquisition_date
            )
        

class PerformanceModelIntegrationTest(TestCase):
    """
    Test that a Performance object was created successfully
    """
    def setUp(self):
        django_user = User.objects.create(username='TestUser')
        self.custom_user = CustomUser.objects.create(user=django_user)

    def test_performance_creation(self):
        performance_example = Performance.objects.create(user=self.custom_user, days_to_send_email=7)

        self.assertEqual(performance_example.user.user.username, 'TestUser')
        self.assertEqual(performance_example.days_to_send_email, 7)

    def test_unique_performance_constraint(self):
        Performance.objects.create(user=self.custom_user, days_to_send_email=7)

        # Try create a second object Performace with same values and catch the exception
        with self.assertRaises(IntegrityError):
            Performance.objects.create(user=self.custom_user, days_to_send_email=7)


class CheckLoadDataTest(TestCase):
    """
    Test that the data was loaded correctly from the data_initial.json fixture!
    """
    def test_loaddata(self):
        # Check that the database is empty at the beginning
        self.assertEqual(Asset.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(Portfolio.objects.count(), 0)
        self.assertEqual(PortfolioAsset.objects.count(), 0)
        self.assertEqual(Performance.objects.count(), 0)

        call_command('loaddata', 'moneytracker/data_init', verbosity=0)

        # Check that the database is not empty after load the data
        self.assertNotEqual(Asset.objects.count(), 0)
        self.assertNotEqual(CustomUser.objects.count(), 0)
        self.assertNotEqual(Portfolio.objects.count(), 0)
        self.assertNotEqual(PortfolioAsset.objects.count(), 0)
        self.assertNotEqual(Performance.objects.count(), 0)
