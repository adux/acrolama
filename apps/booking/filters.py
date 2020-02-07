from django import forms
from django.db.models import Q

import django_filters

from booking.models import Book, Attendance
from project.models import Event, TimeOption


class BookFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(method="filter_by_all_name_fields")
    event = django_filters.ChoiceFilter(
        choices=[
            [o.pk, o.__str__] for o in Event.objects.all().order_by("-event_startdate")
        ]
    )

    times = django_filters.ModelMultipleChoiceFilter(
        queryset=TimeOption.objects.all(), widget=forms.CheckboxSelectMultiple
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
        field_name="attendance_date",
        method="filter_by_date_contains",
    )

    class Meta:
        model = Attendance
        fields = {}

    def filter_by_date_contains(self, queryset, name, value):
        return queryset.filter(
            Q(attendance_date__icontains=value)
        )

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(book__user__first_name__icontains=value)
            | Q(book__user__last_name__icontains=value)
            | Q(book__user__email__icontains=value)
            | Q(book__event__title__icontains=value)
        )
