from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class ProfileLoginForm(AuthenticationForm):
    action = forms.CharField(max_length=60, widget=forms.HiddenInput())
    class Meta:
        model = User
        fields = ['username', 'password', 'action','session']
