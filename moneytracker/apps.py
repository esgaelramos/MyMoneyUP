"""Module for moneytracker apps in the Django application."""

from django.apps import AppConfig


class MoneytrackerConfig(AppConfig):
    """Django application config for Moneytracker.

    This class configures the Moneytracker application, setting up
    the default auto field type and the application name.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moneytracker'
