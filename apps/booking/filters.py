import django_filters

from booking.models import Book


class BookFilter(django_filters.FilterSet):
    year_joined = django_filters.NumberFilter(
        field_name='booked_at',
        lookup_expr='year'
    )
    month_joined = django_filters.NumberFilter(
        field_name='booked_at',
        lookup_expr='month'
    )

    class Meta:
        model = Book
        fields = {
            'user',
            'event',  # : ['contains'],
            'status',
        }
