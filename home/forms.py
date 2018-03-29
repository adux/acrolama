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
