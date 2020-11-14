import logging

from django.db import models

from tinymce.widgets import TinyMCE

from django import forms
from django.core.cache import cache

from project.models import (
    EVENTCATEGORY,
    CYCLE,
    Event,
)

# Widgets
from booking.widgets import BootstrapedModelSelect2Multiple, BootstrapedSelect2Multiple


class EventUpdateForm(forms.Form):
    """
    TODO: make of fk_choices and m2m_choices 1 method for all.
    NOTE: the attname for the fk_model ends in _id wich needs to be considered
    """

    def get_fk_fields(self):
        return [f for f in self.instance._meta.fields if type(f) == models.fields.related.ForeignKey]

    def get_fk_choices(self):
        fk_choices = {}
        for field in self.get_fk_fields():
            model_name = field.related_model.__name__.lower()
            cached_query = cache.get_or_set("cache_" + model_name + "_all", field.related_model.objects.all(), 120)
            choices = [(obj.id, obj.__str__()) for obj in cached_query]
            fk_choices[field.attname] = choices
        return fk_choices

    def get_m2m_fields(self):
        return [
            field for field in self.instance._meta.get_fields() if type(field) == models.fields.related.ManyToManyField
        ]

    def get_m2m_choices(self):
        m2m_choices = {}
        for field in self.get_m2m_fields():
            model_name = field.related_model.__name__.lower()
            cached_query = cache.get_or_set("cache_" + model_name + "_all", field.related_model.objects.all(), 120)
            choices = [(obj.id, obj.__str__()) for obj in cached_query]
            m2m_choices[field.attname] = choices
        return m2m_choices

    def save(self):
        """
        TODO: solve atomicity and race conditions, atomicity is priority

        m2m_fields_name = list(map(lambda x: x.attname, m2m_fields))
        Could use comprehension too [item.upper() for item in mylis]
        """
        data = self.cleaned_data
        obj = self.instance

        # Save FK
        obj.__dict__.update(data)
        obj.save()

        # Save M2M
        # Get all the M2M fields from the Model
        m2m_fields = self.get_m2m_fields()

        # Remove Model Fields that are explicilty not included in Form
        excludes = ['team']
        for m2m_field in m2m_fields:
            if m2m_field.attname in excludes:
                m2m_fields.remove(m2m_field)
        # Filter the List and get them by attname that later will be in data[name]
        changed_m2m_fields = [field for field in m2m_fields if field.attname in self.changed_data]

        if changed_m2m_fields:
            for m2m_field in changed_m2m_fields:
                # Check if model still in query
                model_name = m2m_field.related_model.__name__.lower()
                cached_query = cache.get("cache_" + model_name + "_all")

                # If there is a cached version filter in python and dont hit db
                if cached_query is not None:
                    selected_obj = [obj for obj in cached_query if obj.id in data[m2m_field.attname]]
                    logging.error(data[m2m_field.attname])
                    logging.error(cached_query)
                    logging.error(selected_obj)
                else:
                    selected_obj = [
                        obj for obj in m2m_field.related_model.objects.filter(id__in=data[m2m_field.attname])
                    ]
                # set the selected objects
                getattr(obj, m2m_field.attname).set(selected_obj)

                # Delete cache of model
                model_name = m2m_field.related_model.__name__.lower()
                cache.delete("cache_" + model_name + "_all")

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)

        super(EventUpdateForm, self).__init__(*args, **kwargs)
        m2m_choices = self.get_m2m_choices()
        fk_choices = self.get_fk_choices()

        self.fields["price_options"] = forms.MultipleChoiceField(
            choices=m2m_choices["price_options"],
            widget=BootstrapedSelect2Multiple(url="po-autocomplete"),
        )
        self.fields["time_locations"] = forms.MultipleChoiceField(
            choices=m2m_choices["time_locations"],
            widget=BootstrapedSelect2Multiple(url="tl-autocomplete"),
        )

        self.fields["irregularities"] = forms.MultipleChoiceField(
            choices=m2m_choices["irregularities"],
            widget=BootstrapedSelect2Multiple(url="irregularities-autocomplete"),
            required=False,
        )
        self.fields["teachers"] = forms.MultipleChoiceField(
            choices=m2m_choices["teachers"],
            widget=BootstrapedSelect2Multiple(url="teachers-autocomplete"),
        )
        self.fields["images"] = forms.MultipleChoiceField(
            choices=m2m_choices["images"],
            widget=BootstrapedSelect2Multiple(url="images-autocomplete"),
        )
        self.fields["videos"] = forms.MultipleChoiceField(
            choices=m2m_choices["videos"],
            widget=BootstrapedSelect2Multiple(url="videos-autocomplete"),
            required=False,
        )
        self.fields["project_id"] = forms.ChoiceField(choices=fk_choices["project_id"], label="Project")
        self.fields["policy_id"] = forms.ChoiceField(choices=fk_choices["policy_id"], label="Policy")
        self.fields["level_id"] = forms.ChoiceField(choices=fk_choices["level_id"], label="Level")
        self.fields["discipline_id"] = forms.ChoiceField(choices=fk_choices["discipline_id"], label="Discipline")
        self.fields["category"] = forms.ChoiceField(choices=EVENTCATEGORY)
        self.fields["cycle"] = forms.ChoiceField(choices=CYCLE)
        self.fields["title"] = forms.CharField(max_length=100)
        self.fields["max_participants"] = forms.IntegerField(min_value=2)
        self.fields["event_startdate"] = forms.DateField()
        self.fields["event_enddate"] = forms.DateField()
        self.fields["description"] = forms.CharField(widget=TinyMCE(attrs={"cols": 40, "rows": 20}))
        self.fields["prerequisites"] = forms.CharField(widget=TinyMCE(attrs={"cols": 40, "rows": 20}), required=False)
        self.fields["highlights"] = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 10}), required=False)
        self.fields["included"] = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 10}), required=False)
        self.fields["food"] = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 10}), required=False)
        self.fields["published"] = forms.BooleanField(required=False)
        self.fields["registration"] = forms.BooleanField(required=False)


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
            "price_options": BootstrapedModelSelect2Multiple(url="po-autocomplete"),
            "time_locations": BootstrapedModelSelect2Multiple(
                url="tl-autocomplete",
            ),
            "teachers": BootstrapedModelSelect2Multiple(
                url="teachers-autocomplete",
            ),
        }
