from typing import (
    Union,
    Dict,
    Any
)

from django.db import models
from django.contrib.auth.models import BaseUserManager



class CustomUserManager(BaseUserManager, models.Manager):

    def _create_user(
            self,
            email: str,
            password: str,
            is_staff: bool = False,
            is_superuser: bool = False,
            **extra_fields: Dict[str, Any]
        ):
        user = self.model(
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self.db)

        return user


    def create_user(
            self,
            email: str,
            password: str,
            **extra_fields: Dict[str, Any]
        ):
        return self._create_user(email, password, False, False, **extra_fields)


    def create_superuser(
            self,
            email: str,
            password: str,
            **extra_fields: Dict[str, Any]
        ):
        return self._create_user(email, password, True, True, **extra_fields)