from django.contrib import admin
from django import forms

from .models import (
    Discipline,
    Event,
    Irregularity,
    TimeOption,
    TimeLocation,
    Level,
    Location,
    Policy,
    PriceOption,
    Project,
)

from users.models import User


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)  # populate the post
        self.fields["teachers"].queryset = User.objects.filter(is_teacher=True)
        self.fields["team"].queryset = User.objects.filter(is_staff=True)


class EventAdmin(admin.ModelAdmin):
    form = EventForm

    list_display = [
        "title",
        "event_startdate",
        "event_enddate",
        "cycle",
        "category",
        "level",
        "slug",
        "published",
        "registration",
    ]
    list_select_related = ["project", "policy", "level", "discipline"]

    list_filter = ["category", "level"]
    search_fields = ["title", "event_startdate", "event_enddate"]
    save_as = True


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "public_chat_link",
    ]
    list_filter = ["manager"]


class PriceOptionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "published",
        "cycles",
        "description",
        "price_chf",
        "price_euro",
        "duo",
        "single_date",
    ]


class TimeLocationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "location",
        "get_times",
    ]
    list_select_related = ["location"]


admin.site.register(Event, EventAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(PriceOption, PriceOptionAdmin)
admin.site.register(TimeLocation, TimeLocationAdmin)
admin.site.register(Discipline)
admin.site.register(Irregularity)
admin.site.register(Level)
admin.site.register(Location)
admin.site.register(Policy)
admin.site.register(TimeOption)
