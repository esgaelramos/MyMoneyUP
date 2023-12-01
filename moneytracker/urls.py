from django.urls import path
from .views import Tracker, About, Contact
app_name="moneytracker"

urlpatterns = [
    path("",Tracker.as_view(),name="home"),
    path("about", About.as_view(), name="about"),
    path("contact", Contact.as_view(),name="contact")
]