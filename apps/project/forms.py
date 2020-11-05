from dal import autocomplete
from tinymce.widgets import TinyMCE

from django import forms
from django.core.cache import cache

from users.models import User
from project.models import (
    EVENTCATEGORY,
    CYCLE,
    Project,
    Discipline,
    Irregularity,
    Event,
    Level,
    TimeLocation,
    PriceOption,
    Policy,
)

from audiovisual.models import Image, Video


# Widgets
from booking.widgets import BootstrapedSelect2Multiple


class EventUpdateForm(forms.Form):
    """
    TODO: Add clean to check conditions like right cycle number,
    """

    #         widgets = {
    #             "description": TinyMCE(attrs={),
    #             "prerequisites": TinyMCE(attrs={'cols': 40, 'rows': 20}),
    #             "highlights": TinyMCE(attrs={'cols': 80, 'rows': 10}),
    #             "included": TinyMCE(attrs={'cols': 80, 'rows': 10}),
    #             "food": TinyMCE(attrs={'cols': 80, 'rows': 10}),
    #         }

    def __init__(self, *args, **kwargs):
        super(EventUpdateForm, self).__init__(*args, **kwargs)
        self.fields["price_options"] = forms.MultipleChoiceField(
            choices=[
                (p.id, p.name) for p in cache.get_or_set("cache_price_options_all", PriceOption.objects.all(), 120)
            ],
            widget=autocomplete.Select2Multiple(
                url="po-autocomplete", attrs={"data-theme": "bootstrap4", "data-width": "style"}
            ),
        )
        self.fields["time_locations"] = forms.MultipleChoiceField(
            choices=[
                (p.id, p.name) for p in cache.get_or_set("cache_time_locations_all", TimeLocation.objects.all(), 120)
            ],
            widget=autocomplete.Select2Multiple(
                url="tl-autocomplete", attrs={"data-theme": "bootstrap4", "data-width": "style"}
            ),
        )

        self.fields["irregularities"] = forms.MultipleChoiceField(
            choices=[
                (p.id, p.description)
                for p in cache.get_or_set("cache_irregularities_all", Irregularity.objects.all().order_by("-id"), 120)
            ],
            widget=autocomplete.Select2Multiple(
                url="irregularities-autocomplete", attrs={"data-theme": "bootstrap4", "data-width": "style"}
            ),
        )
        self.fields["teachers"] = forms.MultipleChoiceField(
            choices=[
                (p.id, p.get_full_name)
                for p in cache.get_or_set("cache_teachers_all", User.objects.filter(is_teacher=True), 120)
            ],
            widget=autocomplete.Select2Multiple(
                url="teachers-autocomplete", attrs={"data-theme": "bootstrap4", "data-width": "style"}
            ),
        )
        self.fields["project"] = forms.ChoiceField(
            choices=[
                (p.id, p.name) for p in cache.get_or_set("cache_" + "project" + "_all", Project.objects.all(), 120)
            ]
        )
        self.fields["policy"] = forms.ChoiceField(
            choices=[(p.id, p.name) for p in cache.get_or_set("cache_" + "policy" + "_all", Policy.objects.all(), 120)]
        )
        self.fields["level"] = forms.ChoiceField(
            choices=[
                (p.id, p.get_name_display)
                for p in cache.get_or_set("cache_" + "level" + "_all", Level.objects.all(), 120)
            ]
        )
        self.fields["discipline"] = forms.ChoiceField(
            choices=[
                (p.id, p.name)
                for p in cache.get_or_set("cache_" + "discipline" + "_all", Discipline.objects.all(), 120)
            ]
        )
        self.fields["category"] = forms.ChoiceField(choices=EVENTCATEGORY)
        self.fields["cycle"] = forms.ChoiceField(choices=CYCLE)
        self.fields["title"] = forms.CharField(max_length=100)
        self.fields["max_participants"] = forms.IntegerField(min_value=2)
        self.fields["event_startdate"] = forms.DateField()
        self.fields["event_enddate"] = forms.DateField()
        self.fields["description"] = forms.CharField(widget=TinyMCE(attrs={"cols": 40, "rows": 20}))
        self.fields["prerequisites"] = forms.CharField(widget=TinyMCE(attrs={"cols": 40, "rows": 20}))
        self.fields["highlights"] = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 10}))
        self.fields["included"] = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 10}))
        self.fields["food"] = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 10}))
        self.fields["published"] = forms.BooleanField()
        self.fields["registration"] = forms.BooleanField()


class EventMinimalCreateForm(forms.ModelForm):
    """
    TODO: Add clean to check conditions like right cycle number,
    """

    class Meta:
        model = Event
        exclude = [
            "description",
            "slug",
            "event_enddate",
            "event_startdate",
        ]
        widgets = {
            "price_options": BootstrapedSelect2Multiple(url="po-autocomplete"),
            "time_locations": BootstrapedSelect2Multiple(
                url="tl-autocomplete",
            ),
            "teachers": BootstrapedSelect2Multiple(
                url="teachers-autocomplete",
            ),
        }
