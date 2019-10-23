from django import forms
from django.utils.translation import ugettext_lazy as _
from booking.models import Book
from project.models import PriceOption, TimeOption


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if args:
            slug = args[0]
            slug = slug.get('slug', '')
            if self.instance:
                self.fields['price'].queryset = PriceOption.objects.filter(
                    event__slug=slug
                )
                self.fields['time'].queryset = TimeOption.objects.filter(
                    timelocation__event__slug=slug
                )
                self.fields['price'].empty_label = 'Select an option'
                self.fields['time'].empty_label = None

    class Meta:
        model = Book
        fields = ('time', 'price', 'comment')
        labels = {
            'price': _(''),
            'time': _(''),
            'comment': _(''),
        }
        widgets = {
            'price': forms.Select(attrs={
                'checked': 'checked'
            }
                                  ),
            'time': forms.CheckboxSelectMultiple(
                attrs={
                },
            ),
            'comment': forms.Textarea(attrs={
                'cols': 35,
                'rows': 5,
                'placeholder': 'Comment'
            }),
        }
        error_messages = {
            'time': {'required': _('Time preference:')},
            'price': {'required': _('Pricing preference:')},
        }
