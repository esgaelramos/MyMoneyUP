"""
Unit tests for the models of the moneytracker app.
Doesn't require a database so this tests are unit tests.
"""
from django.test import TestCase
from moneytracker.models import Asset
from unittest.mock import patch, Mock, PropertyMock


class AssetModelTest(TestCase):
    """
    Test that a Asset object was instantiated susccessfully
    """
    @patch('moneytracker.models.Asset.save')
    def test_asset_creation(self, mock_save):
        asset_example = Asset(name="Test Name", symbol="TestSymbol",
                            type="Test Type")
        self.assertEqual(asset_example.name, "Test Name")
        self.assertEqual(asset_example.symbol, "TestSymbol")
        self.assertEqual(asset_example.type, "Test Type")
        self.assertEqual(str(asset_example), "Test Name (TestSymbol) - Test Type")
        mock_save.assert_not_called()
