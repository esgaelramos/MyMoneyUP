from django.contrib import admin

from .models import CustomUser, Performance, Portfolio, Asset

admin.site.register(CustomUser)
admin.site.register(Performance)
admin.site.register(Portfolio)
admin.site.register(Asset)