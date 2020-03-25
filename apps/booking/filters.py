from django import forms
from django.db.models import Q

import django_filters
import datetime

from booking.models import Book, Attendance
from project.models import Event, TimeOption


class BookFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(method="filter_by_all_name_fields")
    event = django_filters.ChoiceFilter(
        choices=[
            [o.pk, o.__str__]
            for o in Event.objects.all().order_by("-event_startdate")
        ]
    )

    times = django_filters.ModelMultipleChoiceFilter(
        queryset=TimeOption.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    start_date = django_filters.DateFilter(
        field_name='booked_at',
        lookup_expr='gt',
        label='Start date',
    )
    end_date = django_filters.DateFilter(
        field_name='booked_at',
        lookup_expr='lt',
        label='End date',
    )
    date_range = django_filters.DateRangeFilter(
        field_name='booked_at',
        label='Range'
    )


    class Meta:
        model = Book
        fields = {"status", "times"}

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
            | Q(user__email__icontains=value)
        )


class AttendanceFilter(django_filters.FilterSet):
    book__user = django_filters.CharFilter(method="filter_by_all_name_fields")
    book__event = django_filters.ChoiceFilter(
        choices=[
            [o.pk, o.__str__]
            for o in Event.objects.all().order_by("-event_startdate")
        ]
    )
    attendance_date = django_filters.DateFilter(
        field_name="attendance_date", method="filter_by_date_contains",
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
            | Q(book__user__email__icontains=value)
            | Q(book__event__title__icontains=value)
        )


class AttendanceDailyFilter(django_filters.FilterSet):
    book__event = django_filters.ChoiceFilter(
    label="Your Events",
    field_name="book__event",
    )

    attendance_date = django_filters.DateFilter(
        field_name="attendance_date",
        method="filter_by_date_contains",
        initial = datetime.datetime.now().date()
    )

    class Meta:
        model = Attendance
        fields = {}

    def __init__(self, data=None, *args, **kwargs):
        self.user = kwargs.pop('user')

        # Simulates behaviour of the initial pre 1.0 in django-filters
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get('initial')

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super(AttendanceDailyFilter, self).__init__(data, *args, **kwargs)

        self.filters['book__event'].extra['choices'] = [
            (event.id, event.__str__) for event in Event.objects.filter(teacher=self.user)
        ]

    def filter_by_date_contains(self, queryset, name, value):
        return queryset.filter(Q(attendance_date__icontains=value))

