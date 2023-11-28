from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Asset, Portfolio, Performance, Session

# Acá registro los modelos en el admin para poder verlos en el sitio de Django

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'type')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity', 'acquisition_date')
    list_filter = ('user', 'acquisition_date')

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_portfolio_value', 'performance')
    list_filter = ('user', 'date')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_date')
    list_filter = ('user', 'login_date')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
