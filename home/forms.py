from django import forms
from .models import Portfolio, Booking



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
    name            = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email           = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone           = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    abo             = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'placeholder': 'Abo'}))
    option          = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'placeholder': 'Option'}))
    comment         = forms.CharField(label='',required=False,widget=forms.TextInput(attrs={'placeholder': 'Comment'}))
