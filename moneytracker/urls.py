from django.urls import path
from .views import TrackerView, AboutView, ContactView
app_name="moneytracker"

urlpatterns = [
    path("",TrackerView.as_view(),name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(),name="contact")
]
