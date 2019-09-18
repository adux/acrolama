from django import forms

from allauth.account.forms import SignupForm
from .models import User, PRONOUN
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


class CustomSignupForm(SignupForm):
    pronoun = models.CharField(choices=PRONOUN, max_length=10, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone = models.CharField(max_length=50, blank=True)
