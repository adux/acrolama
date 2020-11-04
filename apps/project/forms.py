from tinymce.widgets import TinyMCE

from django import forms
from django.core.cache import cache

from users.models import User
from project.models import Event, TimeLocation, PriceOption

# Widgets
from booking.widgets import BootstrapedSelect2Multiple


class EventUpdateForm(forms.ModelForm):
    """
    TODO: Add clean to check conditions like right cycle number,
    """
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ["slug", ]
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

    def __init__(self, *args, **kwargs):
        super(EventUpdateForm, self).__init__(*args, **kwargs)
        self.fields['time_locations'].queryset = cache.get_or_set(
            'cache_time_locations', TimeLocation.objects.all(), 120
        )
        self.fields['price_options'].queryset = cache.get_or_set(
            'cache_price_options', PriceOption.objects.all(), 120
        )


class EventMinimalCreateForm(forms.ModelForm):
    """
    TODO: Add clean to check conditions like right cycle number,
    """
    class Meta:
        model = Event
        exclude = ["description", "slug", "event_enddate", "event_startdate", ]
        widgets = {
            "price_options": BootstrapedSelect2Multiple(url="po-autocomplete"),
            "time_locations": BootstrapedSelect2Multiple(url="tl-autocomplete",),
            "teachers": BootstrapedSelect2Multiple(url="teachers-autocomplete",),
        }
