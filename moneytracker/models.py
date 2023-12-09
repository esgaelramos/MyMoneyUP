from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomUser(models.Model):
    suscribed = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user.username)


class Asset(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    type = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.name} ({self.symbol}) - {self.type}"


class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Portfolio of {self.user}'


class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    acquisition_date = models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['portfolio', 'asset'], name='unique_portfolio_asset')
        ]

    def __str__(self) -> str:
        return f'{self.asset.name} portfolio of {self.portfolio.user}'


class Performance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    days_to_send_email = models.IntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'days_to_send_email'], name='unique_performance')
        ]

    def __str__(self) -> str:
        return f'Performance of {self.user}'
