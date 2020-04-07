from django.contrib import admin
from django import forms

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

from users.models import User


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)  # populate the post
        self.fields["teacher"].queryset = User.objects.filter(is_teacher=True)
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

    list_filter = ["category", "level"]
    search_fields = ["title", "event_startdate", "event_enddate"]
    save_as = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.select_related(
                "project", "policy", "level", "discipline"
            ).prefetch_related(
                "time_locations__time_options",
                "irregularities",
                "price_options",
                "images",
                "videos",
                "team",
                "teacher",
            )
        return (
            qs.filter(teacher=request.user)
            .select_related("project", "policy", "level", "discipline")
            .prefetch_related(
                "time_locations__time_options",
                "irregularities",
                "price_options",
                "images",
                "videos",
                "team",
                "teacher",
            )
        )


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
