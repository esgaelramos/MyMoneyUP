"""
Test cases for the models of the moneytracker app.
Requiere a database (default: sqlite3) so this tests are integration tests.
"""
from django.test import TestCase
from moneytracker.models import Asset, CustomUser
from django.contrib.auth.models import User

class CustomUserModelIntegrationTest(TestCase):
    """
    Test that a CustomUser object was created susccessfully
    """
    def setUp(self):
        self.django_user = User.objects.create(username="Django User")

    def test_customuser_suscribed_creation(self):
        customuser_example = CustomUser.objects.create(suscribed=True, user=self.django_user)
        self.assertEqual(customuser_example.user.username, "Django User")
        self.assertEqual(customuser_example.suscribed, True)
        self.assertEqual(customuser_example.user, self.django_user)

    def test_customuser_not_suscribed_creation(self):
        customuser_example = CustomUser.objects.create(suscribed=False, user=self.django_user)
        self.assertEqual(customuser_example.user.username, "Django User")
        self.assertEqual(customuser_example.suscribed, False)
        self.assertEqual(customuser_example.user, self.django_user)


class AssetModelIntegrationTest(TestCase):
    """
    Test that a Asset object was created susccessfully
    """
    def test_asset_creation(self):
        asset_example = Asset.objects.create(name="Test Name",
                                            symbol="TestSymbol",
                                            type="Test Type")
        self.assertEqual(asset_example.name, "Test Name")
        self.assertEqual(asset_example.symbol, "TestSymbol")
        self.assertEqual(asset_example.type, "Test Type")
