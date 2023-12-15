from django.contrib import admin
from django.urls import path, include

from .views import TermsView
from .views import Custom404View



urlpatterns = [
    path('admin/', admin.site.urls),
    # path("",include("moneytracker.urls")),
    path("terms/", TermsView.as_view(), name="terms"),

    path("authentication/", include("apps.authentication.simple_oauth.urls"))
]

handler404 = Custom404View.as_view()
