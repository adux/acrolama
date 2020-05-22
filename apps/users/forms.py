from django import forms
from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import SignupForm
from .models import PRONOUN


class CustomSignupForm(SignupForm):
    # pronoun = forms.ChoiceField(
    #     choices=PRONOUN,
    #     label="",
    #     widget=forms.Select(attrs={"placeholder": "Select"}),
    # )
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(label="Phone", widget=forms.TextInput(attrs={"placeholder": "+41761234567"}),)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # user.pronoun = self.cleaned_data["pronoun"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone = self.cleaned_data["phone"]
        user.save()
        return user
