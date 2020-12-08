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
        "project",
        "category",
        "cycle",
        "level",
        "published",
        "registration",
        "slug",
    ]
    list_select_related = ["project", "policy", "level", "discipline"]

    list_filter = ["project", "category", "level"]
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
        "time_option",
    ]
    list_select_related = ["location"]


class TimeOptionadmin(admin.ModelAdmin):
    list_display = [
        "name",
        "regular_day",
        "open_starttime",
        "class_starttime",
        "class_endtime",
        "open_endtime",
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(PriceOption, PriceOptionAdmin)
admin.site.register(TimeLocation, TimeLocationAdmin)
admin.site.register(Discipline)
admin.site.register(Irregularity)
admin.site.register(Level)
admin.site.register(Location)
admin.site.register(Policy)
admin.site.register(TimeOption, TimeOptionadmin)
