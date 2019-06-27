from django.contrib import admin
from django import forms
from .models import (
    Day,
    Event,
    Exception,
    TimeOption,
    TimeLocation,
    Level,
    Location,
    Policy,
    PriceOption,
    Project,
)


class EventAdmin(admin.ModelAdmin):
    list_display = [
        "event_startdate",
        "event_enddate",
        "category",
        "title",
        "slug",
        "published",
        "registration",
    ]
    list_filter = ["category", "level"]
    search_fields = ["title", "event_startdate", "event_enddate"]


admin.site.register(Day)
admin.site.register(Project)
admin.site.register(Event, EventAdmin)
admin.site.register(Exception)
admin.site.register(TimeOption)
admin.site.register(PriceOption)
admin.site.register(TimeLocation)
admin.site.register(Location)
admin.site.register(Level)
admin.site.register(Policy)
