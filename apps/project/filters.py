import django_filters

from dal import autocomplete


from project.models import TimeLocation, Event


class EventFilter(django_filters.FilterSet):
    time_locations = django_filters.ModelChoiceFilter(
        queryset=TimeLocation.objects.all(), widget=autocomplete.ModelSelect2(
            url="tl-autocomplete",
            attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}
        )
    )

    class Meta:
        model = Event
        fields = {"project", "level"}
