from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Portfolio, Booking, NewsList

class PortfolioCreateForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            'text',
            'sec_text',
            'upload',
        ]

class BookClassCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['abo'].initial='SC'
        self.fields['abo'].required=True
        self.fields['reduction'].initial='NM'
        self.fields['day'].required=True
    class Meta:
        model = Booking
        fields = (
            'name',
            'email',
            'phone',
            'abo',
            'day',
            'reduction',
            'comment',
        )
        labels = {
            'name': _(''),
            'email': _(''),
            'phone': _(''),
            'abo': _(''),
            'day': _(''),
            'reduction': _(''),
            'comment': _(''),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (+4107611111111)'}),
            'abo': forms.Select(attrs={'checked': 'checked'}),
            'day': forms.Select(attrs={'checked': 'checked'}),
            'reduction': forms.Select(attrs={'checked': 'checked'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Comment'}),
        }

class BookEventCreateForm(forms.ModelForm):
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
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (+417600000000)'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Comments, Questions, Allergies, Injuries'}),
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsList
        fields = (
            'email',
        )
        labels = {
            'email': _(''),
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
        }
