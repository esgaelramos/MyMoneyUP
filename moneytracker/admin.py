from django.contrib import admin
from .models import Asset, CustomUser, Performance, Portfolio, PortfolioAsset

admin.site.register(Asset)
admin.site.register(CustomUser)
admin.site.register(Performance)
admin.site.register(PortfolioAsset)


# Define how to display the class PortfolioAsset in PortfolioAdmin
class PortfolioAssetInline(admin.TabularInline):
    model = PortfolioAsset
    extra = 0   # Lines to add other Asset object in admin interface

class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioAssetInline]

admin.site.register(Portfolio, PortfolioAdmin)
