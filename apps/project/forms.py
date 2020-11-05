from dal import autocomplete
from tinymce.widgets import TinyMCE

from django import forms
from django.core.cache import cache

from users.models import User
from project.models import (
    Project,
    Discipline,
    Irregularity,
    Event,
    TimeLocation,
    PriceOption,
    Policy,
)

from audiovisual.models import Image, Video


# Widgets
from booking.widgets import BootstrapedSelect2Multiple


class EventUpdateForm(forms.ModelForm):
    """
    TODO: Add clean to check conditions like right cycle number,
    """

    class Meta:
        model = Event
        fields = '__all__'
        exclude = ["slug", "team", ]
        widgets = {
            "description": TinyMCE(attrs={'cols': 40, 'rows': 20}),
            "prerequisites": TinyMCE(attrs={'cols': 40, 'rows': 20}),
            "highlights": TinyMCE(attrs={'cols': 80, 'rows': 10}),
            "included": TinyMCE(attrs={'cols': 80, 'rows': 10}),
            "food": TinyMCE(attrs={'cols': 80, 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super(EventUpdateForm, self).__init__(*args, **kwargs)
        self.fields['price_options'] = forms.MultipleChoiceField(
            choices=[(p.id, p.name) for p in cache.get_or_set('cache_price_options_all', PriceOption.objects.all(), 120)],
            widget=autocomplete.Select2Multiple(url="po-autocomplete",
                                                attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}))
        self.fields['time_locations'] = forms.MultipleChoiceField(
            choices=[(p.id, p.name) for p in cache.get_or_set('cache_time_locations_all', TimeLocation.objects.all(), 120)],
            widget=autocomplete.Select2Multiple(url="tl-autocomplete",
                                                attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}))

        self.fields['irregularities'] = forms.MultipleChoiceField(
            choices=[(p.id, p.description) for p in cache.get_or_set('cache_irregularities_all', Irregularity.objects.all().order_by("-id"), 120)],
            widget=autocomplete.Select2Multiple(url="irregularities-autocomplete",
                                                attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}))
        self.fields['teachers'] = forms.MultipleChoiceField(
            choices=[(p.id, p.get_full_name) for p in cache.get_or_set('cache_teachers_all', User.objects.filter(is_teacher=True), 120)],
            widget=autocomplete.Select2Multiple(url="irregularities-autocomplete",
                                                attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}))

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
