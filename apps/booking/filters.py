from django import forms
from django.db.models import Q

import django_filters

from booking.models import Book, Attendance
from project.models import Event, TimeOption


class BookFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(method='filter_by_all_name_fields')
    event = django_filters.ChoiceFilter(
        choices=[
            [o.pk, o.__str__] for o in Event.objects.all().order_by('event_startdate')
        ]
    )

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
        fields = {"status", "times"}  # : ['contains'],_


    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value) | Q(user__email__icontains=value)
        )


class AttendanceFilter(django_filters.FilterSet):

    class Meta:
        model = Attendance
        fields = {"book"}
