"""Tests for script `core.sync_assets`."""
from django.test import TestCase
from moneytracker.management.commands.sync_assets import Command
from moneytracker.models import Asset, DailyAssetInfo


class TestUpdateOrCreateAsset(TestCase):
    """Test case for Command's update_or_create_asset method."""

    def setUp(self):
        """Prepare testing environment and instance variables."""
        self.command = Command()
        self.asset_name = 'TestName'
        self.asset_symbol = 'TestSymbol'
        self.asset_type = 'TestType'

    def test_update_or_create_asset(self):
        """Validate that we can create and update an asset correctly."""
        # Create an initial asset
        initial_asset = self.command.update_or_create_asset(self.asset_name,
                                                            self.asset_symbol,
                                                            self.asset_type)
        self.assertEqual(initial_asset.name, 'TestName')
        self.assertEqual(initial_asset.symbol, 'TestSymbol')
        self.assertEqual(initial_asset.type, 'TestType')

        # Update the asset
        updated_asset = self.command.update_or_create_asset(self.asset_name,
                                                            self.asset_symbol,
                                                            self.asset_type)
        self.assertEqual(updated_asset.name, 'TestName')
        self.assertEqual(updated_asset.symbol, 'TestSymbol')
        self.assertEqual(updated_asset.type, 'TestType')

        # Check that the same asset was returned
        self.assertEqual(initial_asset.pk, updated_asset.pk)


class RegisterDailyAssetInfoTest(TestCase):
    """Test case for Command's register_daily_asset_info method."""

    def setUp(self):
        """Prepare testing environment and instance variables."""
        self.command = Command()
        self.asset = Asset.objects.create(name='TestName', symbol='TestSymbol',
                                          type='TestType')

    def test_creates_new_daily_asset_info(self):
        """Validate that register_daily_asset_info works correctly."""
        # Call the function with a new price and volume
        self.command.register_daily_asset_info(asset=self.asset, price='50000',
                                               volume='1000000')

        # Check that a new DailyAssetInfo instance was created
        daily_asset_info = DailyAssetInfo.objects.first()
        self.assertEqual(daily_asset_info.asset, self.asset)
        self.assertEqual(daily_asset_info.price, float('50000'))
        self.assertEqual(daily_asset_info.volume, float('1000000'))


class TestGetCryptoTicker(TestCase):
    """Test case for Command's get_crypto_ticker method."""

    def setUp(self):
        """Prepare testing environment and instance variables."""
        self.command = Command()

    def test_get_crypto_ticker(self):
        """Validate that get crypto ticker method works correctly."""
        # Call the function with test input
        result = self.command.get_crypto_ticker('BTC-USD')

        # Use an assertion to check that the output is correct
        self.assertIsInstance(result, dict)
        self.assertIn('price', result)
        self.assertIn('volume', result)
