from django import forms
from django.utils.translation import ugettext_lazy as _
from booking.models import Book
from project.models import Event, PriceOption, TimeOption
from django.db import connection

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'name',
            'email',
            'phone',
            'price',
            'time',
            'comment',
        )
        labels = {
            'name': _(''),
            'email': _(''),
            'phone': _(''),
            'price': _(''),
            'time': _(''),
            'comment': _(''),
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (+417611111111)'}),
            'price': forms.Select(attrs={'checked': 'checked'}),
            'time': forms.Select(attrs={'checked': 'checked'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Comment'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args:
            slug = args[0]
            slug = slug.get("slug", "")
            if self.instance:
                self.fields['price'].queryset = PriceOption.objects.filter(event__slug=slug)
                self.fields['time'].queryset = TimeOption.objects.filter(timelocation__event__slug=slug)
