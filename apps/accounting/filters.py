from django import forms
from django.db.models import Q

import django_filters
import datetime

from accounting.models import Invoice
from project.models import Event


class AccountFilter(django_filters.FilterSet):
    book__user = django_filters.CharFilter(method="filter_by_all_name_fields")
    book__event = django_filters.ChoiceFilter(
        choices=[
            [o.pk, o.__str__]
            for o in Event.objects.all().order_by("-event_startdate")
        ]
    )

    pay_till = django_filters.DateFilter(
        field_name="pay_till",
        method="filter_by_date_smaller_than",
    )

    class Meta:
        model = Invoice
        fields = {"status"}

    def filter_by_date_smaller_than(self, queryset, name, value):
        return queryset.filter(
            Q(pay_till__lte=value)
        )

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(book__user__first_name__icontains=value)
            | Q(book__user__last_name__icontains=value)
            | Q(book__user__email__icontains=value)
            | Q(partner__email__icontains=value)
            | Q(partner__name__icontains=value)
        )


