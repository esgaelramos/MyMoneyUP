"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

from .views import TermsView
from .views import Custom404View


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("moneytracker.urls")),
    path("terms/", TermsView.as_view(), name="terms"),
]

handler404 = Custom404View.as_view()
