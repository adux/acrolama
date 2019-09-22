from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import SignupForm
from .models import PRONOUN
# from django.contrib.auth.forms import (
#     UserCreationForm,
#     UserChangeForm,
#     AuthenticationForm,
# )

# TODO: Remove this ?
# class UserRegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         ]


# class UserChangeForm(UserChangeForm):
#     class Meta:
#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         ]


class CustomSignupForm(SignupForm):
    pronoun = forms.ChoiceField(
        choices=PRONOUN,
        label='',
    )
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(
        label='Phone',
        widget=forms.TextInput(attrs={'placeholder': '+41761234567'}))

    def signup(self, request, user):
        user.pronoun = self.cleaned_data['pronoun']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user
