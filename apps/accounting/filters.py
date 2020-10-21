from dal import autocomplete

from django.db.models import Q

import django_filters

from accounting.models import Invoice, BALANCE
from project.models import Event


class AccountFilter(django_filters.FilterSet):
    book__user = django_filters.CharFilter(method="filter_by_all_name_fields", label="User (by Name or Email)")
    book__event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(), widget=autocomplete.ModelSelect2(url="event-autocomplete")
    )
    pay_till = django_filters.DateFilter(field_name="pay_till", method="filter_by_date_smaller_than", label="Pay till")
    balance = django_filters.ChoiceFilter(field_name="balance", choices=BALANCE, label="Account")
    start_pay_date = django_filters.DateFilter(field_name="pay_date", lookup_expr="gt", label="Start Pay date",)
    end_pay_date = django_filters.DateFilter(field_name="pay_date", lookup_expr="lt", label="End Pay date",)
    range_pay_date = django_filters.DateRangeFilter(field_name="pay_date", label="Range Pay date")

    class Meta:
        model = Invoice
        fields = {"id", "status", "methode"}

    def filter_by_date_smaller_than(self, queryset, name, value):
        return queryset.filter(Q(pay_till__lte=value))

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(book__user__first_name__icontains=value)
            | Q(book__user__last_name__icontains=value)
            | Q(book__user__first_name__icontains=value)
            | Q(book__user__email__icontains=value)
            | Q(partner__email__icontains=value)
            | Q(partner__name__icontains=value)
        )
