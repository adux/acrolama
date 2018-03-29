from django import forms

class FestForm(forms.Form):
    name        = forms.CharField(required=False)
    address     = forms.CharField(required=False)
    numero      = forms.CharField(required=False)
    email       = forms.CharField(required=False)
    option      = forms.CharField(required=False)
    allergies   = forms.CharField(required=False)
    date        = forms.DateField(required=False)
