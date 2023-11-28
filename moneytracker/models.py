from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Notar que traemos el objeto User que crea Django por defecto
## y luego lo citamos. por eso no creamos la clase usuario
class Asset(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.type}"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assets = models.ManyToManyField(Asset)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    acquisition_date = models.DateField()

    class Meta:
        unique_together = ('user', 'quantity', 'acquisition_date')

class Performance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    days_to_send_email = models.IntegerField()
    total_portfolio_value = models.DecimalField(max_digits=18, decimal_places=8)
    performance = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('user', 'date')

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField()