from .models import Accounting, Booking
import django_filters


class AccountingFilter(django_filters.FilterSet):
    pay_date = django_filters.DateFromToRangeFilter()
    pay_till = django_filters.DateFromToRangeFilter()
    class Meta:
        model = Accounting
        fields = ['category','event','methode','status']

class BookingFilter(django_filters.FilterSet):
    pay_date = django_filters.DateFromToRangeFilter()
    pay_till = django_filters.DateFromToRangeFilter()
    class Meta:
        model = Booking
        fields = ['category','event','methode', 'status','abo','reduction']
