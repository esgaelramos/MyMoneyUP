"""Module for moneytracker urls in the Django application."""

from django.urls import path

from .views import (
    TrackerView, AboutView, ContactView,
    UnsubscribeView, check_email
)

app_name = "moneytracker"

urlpatterns = [
    path("", TrackerView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("unsubscribe/", UnsubscribeView.as_view(), name="unsubscribe"),

    path("api/check-email/", check_email, name="check_email")
]
