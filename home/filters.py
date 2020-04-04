# from .models import Accounting, Booking, Event
from django import forms
from django.forms.widgets import SplitDateTimeWidget
import django_filters


Icon = (
    ("MC", "Masterclass"),
    ("FT", "Festival"),
    ("CY", "Cycle"),
    ("WS", "Workshop"),
    ("CA", "Camp"),
    ("RT", "Retreat"),
)


# class AccountingFilter(django_filters.FilterSet):
#     pay_date = django_filters.DateFromToRangeFilter(
#         widget=SplitDateTimeWidget(attrs={"placeholder": "YYYY-MM-DD"})
#     )
#     pay_till = django_filters.DateFromToRangeFilter(
#         widget=SplitDateTimeWidget(attrs={"placeholder": "YYYY-MM-DD"})
#     )
#     event__datestart = django_filters.DateFromToRangeFilter(
#         widget=SplitDateTimeWidget(attrs={"placeholder": "YYYY-MM-DD"})
#     )
#     event__cat = django_filters.ChoiceFilter(choices=Icon)

#     class Meta:
#         model = Accounting
#         fields = ["category", "event", "methode", "status"]


# class BookingFilter(django_filters.FilterSet):
#     pay_date = django_filters.DateFromToRangeFilter(
#         widget=SplitDateTimeWidget(attrs={"placeholder": "YYYY-MM-DD"})
#     )
#     pay_till = django_filters.DateFromToRangeFilter(
#         widget=SplitDateTimeWidget(attrs={"placeholder": "YYYY-MM-DD"})
#     )
#     event__datestart = django_filters.DateFromToRangeFilter(
#         widget=SplitDateTimeWidget(attrs={"placeholder": "YYYY-MM-DD"})
#     )
#     event__cat = django_filters.ChoiceFilter(choices=Icon)

#     class Meta:
#         model = Booking
#         fields = ["category", "event", "methode", "status", "abo", "reduction"]
