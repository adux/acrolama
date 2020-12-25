import django_filters
import datetime

from dal.autocomplete import ListSelect2

from django.db.models import Q

# Widgets
from herdi.widgets import BootstrapedSelect2, BootstrapedModelSelect2Multiple

# Models
from booking.models import Book, Attendance, Quotation
from project.models import Event, TimeOption, TimeLocation
from users.models import User


class AttendanceFilter(django_filters.FilterSet):
    book__user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        widget=BootstrapedSelect2(url="user-autocomplete"),
        label="User"
    )
    book__event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(),
        widget=BootstrapedSelect2(url="event-autocomplete"),
        label="Event"
    )
    attendance_date = django_filters.DateFilter(
        field_name="attendance_date",
        method="filter_by_date_contains",
    )

    class Meta:
        model = Attendance
        fields = {'id'}

    def filter_by_date_contains(self, queryset, name, value):
        return queryset.filter(Q(attendance_date__icontains=value))


class AttendanceDailyFilter(django_filters.FilterSet):
    # Gets the Event the User is te acher on.
    book__event = django_filters.ChoiceFilter(
        label="Your Events", field_name="book__event", widget=ListSelect2(
            url="event-teacher-autocomplete",
            attrs={'data-theme': 'bootstrap4', 'data-width': 'style'}
        )
    )

    attendance_date = django_filters.DateFilter(
        field_name="attendance_date",
        method="filter_by_date_contains",
        initial=datetime.datetime.now().date(),
    )

    class Meta:
        model = Attendance
        fields = {}

    def __init__(self, data=None, *args, **kwargs):
        self.user = kwargs.pop("user")

        # Simulates behaviour of the initial pre 1.0 in django-filters
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get("initial")

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super(AttendanceDailyFilter, self).__init__(data, *args, **kwargs)

        self.filters["book__event"].extra["choices"] = [
            (event.id, event.__str__) for event in Event.objects.filter(teachers=self.user)
        ]

    def filter_by_date_contains(self, queryset, name, value):
        return queryset.filter(Q(attendance_date__icontains=value))


class BookFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), widget=BootstrapedSelect2(url=("user-autocomplete"))
    )
    event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(), widget=BootstrapedSelect2(url="event-autocomplete",)
    )
    times = django_filters.ModelMultipleChoiceFilter(
        queryset=TimeOption.objects.all(), widget=BootstrapedModelSelect2Multiple(url="to-autocomplete",)
    )
    start_date = django_filters.DateFilter(
        field_name="booked_at",
        lookup_expr="gt",
        label="Start date",
    )
    end_date = django_filters.DateFilter(
        field_name="booked_at",
        lookup_expr="lt",
        label="End date",
    )
    date_range = django_filters.DateRangeFilter(field_name="booked_at", label="Range")

    class Meta:
        model = Book
        fields = {"id", "status", "times", "event__level"}

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
            | Q(user__email__icontains=value)
            | Q(user__id__icontains=value)
        )


class QuotationFilter(django_filters.FilterSet):
    event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(),
        widget=BootstrapedSelect2(url="event-autocomplete")
    )
    teachers = django_filters.ModelMultipleChoiceFilter(
        queryset=User.objects.filter(is_teacher=True),
        widget=BootstrapedModelSelect2Multiple(url="teachers-autocomplete")
    )
    time_location = django_filters.ModelChoiceFilter(
        queryset=TimeLocation.objects.all(),
        widget=BootstrapedSelect2(url="tl-autocomplete",)
    )

    class Meta:
        model = Quotation
        fields = {"id", "event", "time_location", "locked"}


class QuotationBookFilter(django_filters.FilterSet):
    event = django_filters.ModelChoiceFilter(
        queryset=Event.objects.all(), required=True, widget=BootstrapedSelect2(url="event-autocomplete",)
    )
    event__time_locations = django_filters.ModelChoiceFilter(
        queryset=TimeLocation.objects.all(), required=True, widget=BootstrapedSelect2(url="tl-autocomplete",)
    )

    class Meta:
        model = Book
        exclude = {"notes"}

    @property
    def qs(self):
        """
        Filters the Books of the Quotation to be only the ones matching the Selected TimeLocation
        by looking into the TimeOptions match between both
        """
        parent = super().qs
        # Get the TL id entered
        pk = self.data.get("event__time_locations", None)
        if pk:
            # If the id not None get the object
            time_location = TimeLocation.objects.get(id=pk)
            # And filter bookings with only to of event
            return parent.filter(times=time_location.time_option)
