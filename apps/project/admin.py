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

admin.site.register(Day)
admin.site.register(Project)
admin.site.register(Event)
admin.site.register(Exception)
admin.site.register(TimeOption)
admin.site.register(PriceOption)
admin.site.register(TimeLocation)
admin.site.register(Location)
admin.site.register(Level)
admin.site.register(Policy)


