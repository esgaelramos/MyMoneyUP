"""
Script to sync assets from the Historic Crypto Library to the database.

This script uses the Historic Crypto Library to get the list of assets
from the Coinbase API and syncs them to the database.

Example:
    python manage.py sync_assets
"""

import json
from typing import Any

import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from moneytracker.models import Asset, DailyAssetInfo


class Command(BaseCommand):
    """Class Command to custom a django admin command."""

    TOP_26_CRYPTO_PAIRS = [
        "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "XRP-USD", "DOT-USD",
        "DOGE-USD", "AVAX-USD", "LINK-USD", "LTC-USD", "BCH-USD", "ALGO-USD",
        "XLM-USD", "UNI-USD", "WBTC-USD", "ATOM-USD", "VET-USD", "FIL-USD",
        "SAND-USD", "RPL-USD", "XTZ-USD", "EOS-USD", "MKR-USD", "CRO-USD",
        "DASH-USD", "ZEC-USD"
    ]

    def update_or_create_asset(self, name: str,
                               symbol: str = '$', asset_type: str = 'x') \
            -> Asset:
        """
        Update an existing asset record or create a new one.

        Using Django's ORM.

        Args:
            name (str): Name of the asset.
            symbol (str, optional): Symbol of the asset. Defaults to '$'.
            asset_type (str, optional): Type of the asset. Defaults to 'x'.
        """
        with transaction.atomic():
            asset, created_asset = Asset.objects.update_or_create(
                name=name,
                symbol=symbol,
                type=asset_type)

            if created_asset:
                print(f"Created new asset with symbol: {symbol}")
            else:
                print(f"Updated existing asset with symbol: {symbol}")
        return asset

    def register_daily_asset_info(self, asset: Asset, price: str, volume: str):
        """Regiter a daily asset info in database usin Django's ORM.

        Args:
            asset (Asset): Asset to relate the info.
            price (str): Price of the asset.
            volume (str): Volume of the capitalization of the asset.
        """
        with transaction.atomic():
            _, created_daily_asset_info = DailyAssetInfo.objects.\
                update_or_create(asset=asset, price=price, volume=volume)
            if created_daily_asset_info:
                print(f"Created daily info of {asset}")

    def get_crypto_ticker(self, id):
        """Get cryptocurrency ticker from Coinbase API."""
        # Send a GET request to Coinbase API to get the ticker for a specific
        # product
        response = requests.get(
            f'https://api.pro.coinbase.com/products/{id}/ticker'
        )
        # Check if status code indicates a successful response
        if response.status_code in [200, 201, 202, 203, 204]:
            ticker = json.loads(response.text)
            return ticker

    def handle(self, *args: Any, **options: Any):
        """Iterate over the tickers and update/create in the database."""
        for pair in self.TOP_26_CRYPTO_PAIRS:
            display_name = pair.replace("-", "/")
            symbol = pair

            # Get ticker of asset
            ticker = self.get_crypto_ticker(symbol)
            price = ticker['price']
            volume = ticker['volume']

            asset = self.update_or_create_asset(display_name, symbol)

            self.register_daily_asset_info(asset=asset, price=price,
                                           volume=volume)
