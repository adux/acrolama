import django_filters

from project.models import TimeLocation, Event

# Widgets
from booking.widgets import BootstrapedSelect2


class EventFilter(django_filters.FilterSet):
    time_locations = django_filters.ModelChoiceFilter(
        queryset=TimeLocation.objects.all(), widget=BootstrapedSelect2(url="tl-autocomplete",)
    )

    class Meta:
        model = Event
        fields = {"project", "level"}
