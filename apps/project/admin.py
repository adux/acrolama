from django.contrib import admin
from .models import (
    Day,
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


class EventAdmin(admin.ModelAdmin):
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
    list_filter = ["category", "level"]
    search_fields = ["title", "event_startdate", "event_enddate"]
    save_as = True

class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "todo",
    ]
    list_filter = ["manager"]

admin.site.register(Day)
admin.site.register(Discipline)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Irregularity)
admin.site.register(TimeOption)
admin.site.register(PriceOption)
admin.site.register(TimeLocation)
admin.site.register(Location)
admin.site.register(Level)
admin.site.register(Policy)
