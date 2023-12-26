"""Module for moneytracker models in the Django application."""

from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    """Represents a custom user in the MoneyTracker application."""

    suscribed = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        """Meta options for CustomUser model."""  # noqa: D204
        db_table = 'custom_users'

    def __str__(self) -> str:
        """Return the username as string representation of the custom user."""
        return str(self.user.username)


class Asset(models.Model):
    """Represents an asset in the MoneyTracker application."""

    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    type = models.CharField(max_length=50)

    class Meta:
        """Meta options for Asset model."""  # noqa: D204
        db_table = 'assets'

    def __str__(self) -> str:
        """Return a formatted string representation of the asset."""
        return f"{self.name} ({self.symbol}) - {self.type}"


class Portfolio(models.Model):
    """Represents a user's portfolio in the MoneyTracker application."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        """Meta options for Portfolio model."""  # noqa: D204
        db_table = 'portfolios'

    def __str__(self) -> str:
        """Return a string representation of the portfolio."""
        return f'Portfolio of {self.user}'


class PortfolioAsset(models.Model):
    """Associates assets with portfolios in the MoneyTracker application."""

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    acquisition_date = models.DateField(auto_now=True)

    class Meta:
        """Meta options for PortfolioAsset model."""  # noqa: D204
        db_table = 'portfolios_assets'
        constraints = [
            models.UniqueConstraint(fields=['portfolio', 'asset'],
                                    name='unique_portfolio_asset')
        ]

    def __str__(self) -> str:
        """Return a string representation of the portfolio asset."""
        return f'{self.asset.name} portfolio of {self.portfolio.user}'


class Performance(models.Model):
    """Represents user performance settings in the MoneyTracker application."""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    days_to_send_email = models.IntegerField(default=1)

    class Meta:
        """Meta options for Performance model."""  # noqa: D204
        db_table = 'performances'
        constraints = [
            models.UniqueConstraint(fields=['user', 'days_to_send_email'],
                                    name='unique_performance')
        ]

    def __str__(self) -> str:
        """Return a string representation of the performance settings."""
        return f'Performance of {self.user}'
    
class AssetPrice(models.Model):
    """Represents the price of an asset fetched in the MoneyTracker application."""

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for AssetPrice model."""  # noqa: D204
        db_table = 'asset_prices'

    def __str__(self) -> str:
        """Return a string representation of the asset price."""
        return f'{self.asset.name} - {self.price}$ at {self.timestamp}'
