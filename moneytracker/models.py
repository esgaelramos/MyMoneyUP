from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    mail = models.EmailField(max_length=254, unique=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.username
