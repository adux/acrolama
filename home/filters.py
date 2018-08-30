from .models import Accounting, Booking
import django_filters


class AccountingFilter(django_filters.FilterSet):
    class Meta:
        model = Accounting
        fields = ['category','event','pay_till','pay_date','methode','status']

class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = ['abo','reduction']

