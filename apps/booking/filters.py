from dal import autocomplete

from django import forms
from django.db.models import Q

import django_filters
import datetime

from booking.widgets import M2MSelect

from booking.models import Book, Attendance, Quotation
from project.models import Event, TimeOption, TimeLocation
from users.models import User


class AttendanceFilter(django_filters.FilterSet):
    book__user = django_filters.CharFilter(method="filter_by_all_name_fields")
    book__event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(), widget=autocomplete.ModelSelect2(url="event-autocomplete")
    )
    attendance_date = django_filters.DateFilter(
        field_name="attendance_date",
        method="filter_by_date_contains",
    )

    class Meta:
        model = Attendance
        fields = {}

    def filter_by_date_contains(self, queryset, name, value):
        return queryset.filter(Q(attendance_date__icontains=value))

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(book__user__first_name__icontains=value)
            | Q(book__user__last_name__icontains=value)
            | Q(book__user__first_name__icontains=value)
            | Q(book__user__email__icontains=value)
            | Q(book__event__title__icontains=value)
        )


class AttendanceDailyFilter(django_filters.FilterSet):
    # Gets the Event the User is teacher on.
    book__event = django_filters.ChoiceFilter(
        label="Your Events", field_name="book__event", widget=autocomplete.ListSelect2(url="eventteacher-autocomplete")
    )

    attendance_date = django_filters.DateFilter(
        field_name="attendance_date",
        method="filter_by_date_contains",
        initial=datetime.datetime.now().date(),
    )

    class Meta:
        model = Attendance
        fields = {}

    def __init__(self, data=None, *args, **kwargs):
        self.user = kwargs.pop("user")

        # Simulates behaviour of the initial pre 1.0 in django-filters
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get("initial")

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super(AttendanceDailyFilter, self).__init__(data, *args, **kwargs)

        self.filters["book__event"].extra["choices"] = [
            (event.id, event.__str__) for event in Event.objects.filter(teachers=self.user)
        ]

    def filter_by_date_contains(self, queryset, name, value):
        return queryset.filter(Q(attendance_date__icontains=value))


class BookFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(method="filter_by_all_name_fields")
    event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(), widget=autocomplete.ModelSelect2(url="event-autocomplete")
    )
    times = django_filters.ModelMultipleChoiceFilter(
        queryset=TimeOption.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    start_date = django_filters.DateFilter(
        field_name="booked_at",
        lookup_expr="gt",
        label="Start date",
    )
    end_date = django_filters.DateFilter(
        field_name="booked_at",
        lookup_expr="lt",
        label="End date",
    )
    date_range = django_filters.DateRangeFilter(field_name="booked_at", label="Range")

    class Meta:
        model = Book
        fields = {"id", "status", "times", "event__level"}

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
            | Q(user__email__icontains=value)
            | Q(user__id__icontains=value)
        )


class EventFilter(django_filters.FilterSet):
    time_locations = django_filters.ModelChoiceFilter(
        queryset=TimeLocation.objects.all(), widget=autocomplete.ModelSelect2(url="tl-autocomplete")
    )

    class Meta:
        model = Event
        fields = {"project", "time_locations", "level"}


class QuotationFilter(django_filters.FilterSet):
    event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(), widget=autocomplete.ModelSelect2(url="event-autocomplete")
    )
    teachers = django_filters.ModelMultipleChoiceFilter(
        queryset=User.objects.filter(is_teacher=True), widget=M2MSelect()
    )

    class Meta:
        model = Quotation
        fields = {"event", "time_location", "teachers"}


class QuotationBookFilter(django_filters.FilterSet):
    event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(), required=True, widget=autocomplete.ModelSelect2(url="event-autocomplete")
    )
    event__time_locations = django_filters.ModelChoiceFilter(
        queryset=TimeLocation.objects.all(), required=True, widget=M2MSelect()
    )

    class Meta:
        model = Book
        exclude = {"notes"}

    @property
    def qs(self):
        parent = super().qs
        # Get the TL id entered
        pk = self.data.get("event__time_locations", None)
        if pk:
            # If the id not None get the object
            tl = TimeLocation.objects.get(id=pk)
            # Get all the TO of the TL
            to_ids = [to.id for to in tl.time_options.all()]
            # And filter bookings with only to of event
            return parent.filter(times__in=to_ids)
