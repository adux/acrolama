from django import forms
from .models import Portfolio



class PortfolioCreateForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            'text',
            'sec_text',
            'upload',
        ]

class BookingCreateForm(forms.Form):
    Abo             = (
        ('SA','Season Abo'),
        ('CY','Cycle Abo'),
        ('SI','Single Ticket'),
    )
    name            = forms.CharField()
    email           = forms.CharField()
    phone           = forms.CharField()
    abo             = forms.CharField(required=False)
    option          = forms.CharField(required=False)
    comment         = forms.CharField(required=False)

