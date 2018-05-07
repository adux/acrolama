from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Portfolio, Booking



class PortfolioCreateForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            'text',
            'sec_text',
            'upload',
        ]

class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = (
            'name',
            'email',
            'phone',
            'comment',
        )
        labels = {
            'name': _(''),
            'email': _(''),
            'phone': _(''),
            'comment': _(''),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (+41076...)'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Comment'}),
        }

