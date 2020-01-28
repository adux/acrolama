from django import forms

import django_filters

from booking.models import Book, Attendance
from project.models import TimeOption


class BookFilter(django_filters.FilterSet):
    year_joined = django_filters.NumberFilter(
        field_name="booked_at", lookup_expr="year"
    )

    month_joined = django_filters.NumberFilter(
        field_name="booked_at", lookup_expr="month"
    )

    times = django_filters.ModelMultipleChoiceFilter(
        queryset=TimeOption.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Book
        fields = {"user", "event", "status", "times"}  # : ['contains'],


class AttendanceFilter(django_filters.FilterSet):

    class Meta:
        model = Attendance
        fields = {"book"}
