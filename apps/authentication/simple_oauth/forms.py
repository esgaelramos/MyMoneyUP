from django import forms
from django.contrib.auth import authenticate

from apps.administration.users.models import Users



class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electronico",
        required=True,
        widget=forms.EmailInput()
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput()
    )

    def clean(self):
        clean_data = super(LoginForm, self).clean()
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Los datos de usuario no son correctos.")

        return clean_data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput()
    )

    repeat_password = forms.CharField(
        label="Repite la contraseña",
        required=True,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = Users
        fields = (
            "email",
        )

    def clean_repeat_password(self):
        if self.cleaned_data["password"] != self.cleaned_data["repeat_password"]:
            self.add_error["repeat_password", "Las Contraseñas no coinciden."]