from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView, View
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm, LoginForm
from apps.administration.users.models import Users



class RegisterFormView(FormView):
    template_name = "pages/authentication/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("/")

    def form_valid(self, form: RegisterForm) -> HttpResponse:
        Users.objects.create_user(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )
        return super(RegisterFormView, self).form_valid(form)
    


class LoginFormView(FormView):
    template_name = "pages/authentication/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("/")

    def form_valid(self, form: LoginForm) -> HttpResponse:
        user=authenticate(
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )
        login(self.request, user)
        return super(LoginFormView, self).form_valid(form)



class LogoutView(View):
    def get(self, request, *args, **kwargs) -> HttpResponseRedirect:
        logout(request)
        return HttpResponseRedirect(
            redirect_to=reverse("authentication:login")
        )