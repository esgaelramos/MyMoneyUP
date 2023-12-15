from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin
)

from .managers import CustomUserManager



class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_("Email"), unique=True, db_index=True, null=False, blank=False)
    password = models.CharField(verbose_name=_("Password"), max_length=255, null=False, blank=False)
    is_staff = models.BooleanField(verbose_name=_("Is Staff"), default=False)
    is_superuser = models.BooleanField(verbose_name=_("Is Superuser"), default=False)

    objects: CustomUserManager = CustomUserManager()

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List = []