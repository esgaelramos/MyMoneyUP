"""
Unit tests for the models of the moneytracker app.
Doesn't require a database so this tests are unit tests.
"""
from django.test import TestCase
from moneytracker.models import Asset, CustomUser
from django.contrib.auth.models import User
from unittest.mock import patch

class CustomUserModelTest(TestCase):
    """
    Test that a CustomUser object was created susccessfully
    """
    def setUp(self):
        self.django_user = User(username="Django User")

    @patch('moneytracker.models.CustomUser.save')
    def test_customuser_suscribed_creation(self, mock_save):
        customuser_example = CustomUser(suscribed=True, user=self.django_user)
        self.assertEqual(customuser_example.user.username, "Django User")
        self.assertEqual(customuser_example.suscribed, True)
        self.assertEqual(customuser_example.user, self.django_user)
        mock_save.assert_not_called()

    @patch('moneytracker.models.CustomUser.save')
    def test_customuser_not_suscribed_creation(self, mock_save):
        customuser_example = CustomUser(suscribed=False, user=self.django_user)
        self.assertEqual(customuser_example.user.username, "Django User")
        self.assertEqual(customuser_example.suscribed, False)
        self.assertEqual(customuser_example.user, self.django_user)
        mock_save.assert_not_called()


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
