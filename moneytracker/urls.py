from django.urls import path
from .views import Tracker, About, Contact
app_name="moneytracker"

urlpatterns = [
    path("signin",Tracker.as_view(),name="sign_in"),
    path("about", About.as_view(), name="about"),
    path("contact", Contact.as_view(),name="contact")
]