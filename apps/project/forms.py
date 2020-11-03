from tinymce.widgets import TinyMCE

from django import forms

from project.models import Event

# Widgets
from booking.widgets import BootstrapedSelect2Multiple


class EventUpdateForm(forms.ModelForm):
    """
    TODO: Add clean to check conditions like right cycle number,
    """
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            "price_options": BootstrapedSelect2Multiple(url="po-autocomplete",),
            "time_locations": BootstrapedSelect2Multiple(url="tl-autocomplete",),
            "irregularities": BootstrapedSelect2Multiple(url="irregularities-autocomplete",),
            "teachers": BootstrapedSelect2Multiple(url="teachers-autocomplete",),
            "description": TinyMCE(attrs={'cols': 40, 'rows': 20}),
            "prerequisites": TinyMCE(attrs={'cols': 40, 'rows': 20}),
            "highlights": TinyMCE(attrs={'cols': 80, 'rows': 10}),
            "included": TinyMCE(attrs={'cols': 80, 'rows': 10}),
            "food": TinyMCE(attrs={'cols': 80, 'rows': 10}),
        }


class EventMinimalCreateForm(forms.ModelForm):
    """
    TODO: Add clean to check conditions like right cycle number,
    """
    class Meta:
        model = Event
        exclude = ["description", ]
        widgets = {
            "price_options": BootstrapedSelect2Multiple(url="po-autocomplete"),
            "time_locations": BootstrapedSelect2Multiple(url="tl-autocomplete",),
            "teachers": BootstrapedSelect2Multiple(url="teachers-autocomplete",),
        }
