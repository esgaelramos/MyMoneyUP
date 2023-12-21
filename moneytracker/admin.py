"""Module for admin configurations in the MoneyTracker application.

This module customizes the Django admin interface for MoneyTracker models,
providing a user-friendly interface for managing application data.
"""

from django.contrib import admin

from .models import (
    Asset, CustomUser, Performance, Portfolio, PortfolioAsset
)

# Regular Admin Register
admin.site.register(Asset)
admin.site.register(CustomUser)
admin.site.register(Performance)
admin.site.register(PortfolioAsset)


# Custom Admin Register
# Define how to display the class PortfolioAsset in PortfolioAdmin
class PortfolioAssetInline(admin.TabularInline):
    """Inline admin interface for PortfolioAsset.

    This class provides a tabular inline interface in the Django admin.
    It is used to edit PortfolioAssets directly in the Portfolio admin view.
    """

    model = PortfolioAsset
    extra = 0   # Lines to add other Asset object in admin interface


class PortfolioAdmin(admin.ModelAdmin):
    """Custom admin interface for the Portfolio model.

    This class customizes the admin interface for Portfolio, integrating
    the PortfolioAssetInline to manage related PortfolioAsset objects.
    """

    inlines = [PortfolioAssetInline]


admin.site.register(Portfolio, PortfolioAdmin)
