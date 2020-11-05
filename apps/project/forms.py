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
        # self.fields['project'].queryset = cache.get_or_set(
        #     'cache_project', Project.objects.all(), 120
        # )
        # self.fields['irregularities'].queryset = cache.get_or_set(
        #     'cache_irregularities', Irregularity.objects.all(), 120
        # )
        # self.fields['price_options'].queryset = cache.get_or_set(
        #     'cache_price_options', PriceOption.objects.all(), 120
        # )
        # self.fields['policy'].queryset = cache.get_or_set(
        #     'cache_policy', Policy.objects.all(), 120
        # )
        # self.fields['discipline'].queryset = cache.get_or_set(
        #     'cache_discipline', Discipline.objects.all(), 120
        # )
        # self.fields['teachers'].queryset = cache.get_or_set(
        #     'cache_user', User.objects.all(), 120
        # )
        # self.fields['team'].queryset = cache.get('cache_user')
        # self.fields['images'].queryset = cache.get_or_set(
        #     'cache_images', Image.objects.all(), 120
        # )
        # self.fields['videos'].queryset = cache.get_or_set(
        #     'cache_videos', Video.objects.all(), 120
        # )


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
