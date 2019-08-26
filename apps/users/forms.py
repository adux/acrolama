from django import forms
from .models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class UserChangeForm(UserChangeForm):
    class Meta:
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class ProfileLoginForm(AuthenticationForm):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ["email", "password", "action", "session"]
