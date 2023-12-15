
from django.urls import path

from apps.authentication.simple_oauth.views import (
    RegisterFormView,
    LoginFormView,
    LogoutView
)



app_name="simple_oauth"
urlpatterns = [
    path("register/", RegisterFormView.as_view(), name="register"),
    path("login/", LoginFormView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

