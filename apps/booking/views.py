import datetime

from decimal import Decimal

# External apps
from dal import autocomplete
from invitations.utils import get_invitation_model

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.db.models import Q  # Queries with OR
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect

# Views
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Models
from audiovisual.models import Image, Video
from users.models import User
from booking.models import Book, Attendance, Quotation
from project.models import (
    Event,
    TimeOption,
    TimeLocation,
    PriceOption,
    Irregularity,
)

# Filters
from booking.filters import (
    AttendanceFilter,
    AttendanceDailyFilter,
    BookFilter,
    QuotationFilter,
    QuotationBookFilter,
)

# Forms
from booking.forms import (
    BookUpdateForm,
    BookCreateForm,
    AttendanceUpdateForm,
    QuotationCreateForm,
    QuotationLockForm,
    InvitationForm,
)

# Utils
from booking.utils import (
    build_url,
    staff_check,
    herd_check,
)

# Services
from booking.services import (
    book_create_next,
    book_inform,
    book_get,
    check_abocounter,
    create_quotation,
    update_lastbook_abocounter,
    attendance_toggle_check
)
from project.services import event_get, timelocation_get


# TODO: Move all autocomplete to herdi or home
class EventAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return Event.objects.none()

        qs = Event.objects.all().order_by("-event_startdate", "level").select_related("project", "level")

        if self.q:
            qs = qs.filter(
                Q(category__icontains=self.q) | Q(level__name__icontains=self.q) | Q(title__icontains=self.q)
            )

        return qs


class EventTeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return Event.objects.none()

        qs = Event.objects.all().order_by("-event_startdate").select_related("project", "level").filter(teachers=self.request.user)

        if self.q:
            qs = qs.filter(
                Q(category__icontains=self.q) | Q(level__name__icontains=self.q) | Q(title__icontains=self.q)
            )

        return qs


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return User.objects.none()

        qs = User.objects.all().order_by("last_name")

        if self.q:
            qs = qs.filter(
                Q(email__icontains=self.q) | Q(first_name__icontains=self.q) | Q(last_name__icontains=self.q)
            )

        return qs


class TeachersAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return User.objects.none()

        qs = cache.get_or_set('cache_teachers_all', User.objects.all().order_by("last_name").filter(is_teacher=True), 120)

        if self.q:
            qs = qs.filter(
                Q(email__icontains=self.q) | Q(first_name__icontains=self.q) | Q(last_name__icontains=self.q)
            )

        return qs


class TimeOptionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return TimeOption.objects.none()

        qs = TimeOption.objects.all().order_by("name")

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q)
                | Q(regular_day__icontains=self.q)
            )

        return qs


class TimeLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return TimeLocation.objects.none()

        # qs = TimeLocation.objects.all().order_by("name", "location").select_related("location")
        qs = cache.get_or_set('cache_time_locations', TimeLocation.objects.all(), 120)

        if self.q:
            qs = qs.filter(
                Q(location__name__icontains=self.q)
                | Q(time_options__name__icontains=self.q)
                | Q(name__icontains=self.q)
            )

        return qs


class IrregularityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return Irregularity.objects.none()

        qs = cache.get_or_set('cache_irregularities_all', Irregularity.objects.all().order_by("-id"), 120)

        if self.q:
            qs = qs.filter(
                Q(time_location__name__icontains=self.q)
                | Q(description__icontains=self.q)
            )

        return qs


class PriceOptionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not staff_check(self.request.user):
            return PriceOption.objects.none()

        # qs = PriceOption.objects.all().order_by("name")
        qs = cache.get_or_set('cache_price_options_all', PriceOption.objects.all(), 120)

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(price_chf__icontains=self.q) | Q(name__icontains=self.q))

        return qs


class ImagesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not staff_check(self.request.user):
            return Image.objects.none()

        # qs = PriceOption.objects.all().order_by("name")
        qs = cache.get_or_set('cache_image_all', Image.objects.all(), 120)

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs


class VideosAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not staff_check(self.request.user):
            return Video.objects.none()

        # qs = PriceOption.objects.all().order_by("name")
        qs = cache.get_or_set('cache_video_all', Video.objects.all(), 120)

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs


@login_required
@user_passes_test(staff_check)
def bookinglistview(request):
    template = "booking/booking_list.html"
    booking_filter = BookFilter(
        request.GET,
        queryset=(
            Book.objects.all()
            .select_related("event", "user", "price")
            .prefetch_related("times")
            .order_by("-booked_at")
        ),
    )

    form = BookCreateForm()

    # Pagination
    paginator = Paginator(booking_filter.qs, 24)  # Show 24 contacts per page.
    page = request.GET.get("page")

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    # Context

    context = {
        "book_filter": booking_filter,
        "filter": request.GET,
        "bookingcreate_form": form,
        "page_obj": response,
    }

    # Logic

    if request.method == "POST":
        if "newbooking" in request.POST:
            form = BookCreateForm(request.POST or None)
            if form.is_valid():
                form.save()

        checked_list = request.POST.getlist("check")
        if checked_list is None:
            return

        if "create" in request.POST:
            for pk in checked_list:
                book = book_get(pk)

                # Create the next book
                if book.status == "PA":
                    try:
                        new_book = book_create_next(book, "PE")

                        # Check if it has a counter and update last_book
                        if book.price.cycles > 1:

                            try:
                                exists = check_abocounter(book.id)
                            except Exception as e:
                                messages.add_message(
                                    request,
                                    messages.WARNING,
                                    _("Error on Abo Counter. Please report: " + str(e)),
                                )

                            if exists:
                                update_lastbook_abocounter(book.id, new_book.id)

                    except Exception as e:
                        messages.add_message(
                            request,
                            messages.WARNING,
                            _("Book N°" + str(book.id) + ": Doesn't seem to have a next Event. Error: " + str(e)),
                        )
                    else:
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            _("Book N°" + str(new_book.id) + ": Book Created"),
                        )

                else:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        _("Book N°: " + str(book.id) + " is not 'Participant'"),
                    )

    return render(request, template, context)


class BookUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Book
    template_name = "booking/booking_update.html"
    form_class = BookUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book_filter = BookFilter(
            self.request.GET,
            queryset=(
                Book.objects.all()
                .select_related("event", "user", "price")
                .prefetch_related("times")
                .order_by("-booked_at")
            ),
        )

        bookingcreate_form = BookCreateForm()

        # Paginator
        paginator = Paginator(book_filter.qs, 24)  # Show 24 contacts per page.
        page = self.request.GET.get("page")
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        # Context
        context["page_obj"] = response
        context["filter"] = self.request.GET
        context["book_filter"] = book_filter
        context["bookingcreate_form"] = bookingcreate_form

        return context

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Get the book before save
        book = book_get(instance.id)

        if "update" in self.request.POST:
            if (book.status in ("PE", "WL")) and (instance.status == "IN"):
                book_inform(self.request, instance, book)

        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        pk = self.object.id
        url = build_url(
            "booking_update",
            get=self.request.GET.items(),
            # Reverse requires a mapping, like a dict
            pk={"pk": pk},
        )
        return url

    def test_func(self):
        return staff_check(self.request.user)


class BookCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Book
    template_name = "booking/booking_create.html"
    form_class = BookCreateForm

    def get_success_url(self, **kwargs):
        success_url = build_url(
            "teacher_attendance",
            get={
                "book__event": self.request.GET.get("book__event", ""),
                "attendance_date": self.request.GET.get("attendance_date", ""),
            },
        )
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Book created, we'll get back to you soon!"),
        )
        return success_url

    def test_func(self):
        return herd_check(self.request.user)


@login_required
@user_passes_test(staff_check)
def attendancelistview(request):
    template = "booking/attendance_list.html"
    attendance_filter = AttendanceFilter(
        request.GET,
        queryset=(
            Attendance.objects.all()
            .select_related("book", "book__event", "book__user", "book__price")
            .prefetch_related("book__times")
        ),
    )

    # Pagination
    paginator = Paginator(attendance_filter.qs, 24)  # Show 25 contacts per page.
    page = request.GET.get("page")
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    context = {
        "attendance_filter": attendance_filter,
        "filter": request.GET,
        "page_obj": response,
    }

    return render(request, template, context)


@login_required
@user_passes_test(herd_check)
def attendance_daily_view(request):
    template = "booking/attendance_list_daily.html"

    if request.method == "POST":
        if "update" in request.POST:
            check_list = request.POST.getlist("check")
            try:
                for values in check_list:
                    #  FIXME: need to implement a backend validation
                    # values are get in temp
                    values_split = values.split(" ")
                    attendance_id = values_split[0]
                    check_pos = values_split[1]
                    # Make the actual Switch
                    attendance_toggle_check(attendance_id, int(check_pos))
                    # Send a message
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        _("Updated attendance id: " + str(attendance_id)),
                    )
            except Exception as e:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _("Make a manual list and report the error: " + e),
                )
            else:
                success_url = build_url(
                    "teacher_attendance",
                    get={
                        "book__event": request.POST.get("filtered_event", ""),
                        "attendance_date": request.POST.get("filtered_date"),
                    },
                )
                return HttpResponseRedirect(success_url)

    attendance_filter = AttendanceDailyFilter(
        request.GET,
        queryset=(
            Attendance.objects.filter(book__event__teachers=request.user)
            .exclude(book__status="CA")
            .exclude(book__status="SW")
            .exclude(book__invoice__status="CA")
            .exclude(book__invoice__status="ST")
            .select_related("book", "book__user", "book__event", "book__price")
            .prefetch_related("book__times")
        ),
        user=request.user,
    )

    date_today = datetime.datetime.now().date()

    if not request.GET.get("attendance_date"):
        initial_date = str(date_today)
    else:
        initial_date = request.GET.get("attendance_date")

    context = {
        "attendance_filter": attendance_filter,
        "attendance_list": attendance_filter.qs,
        "filtered_date": datetime.date.fromisoformat(initial_date),
        "date_today": date_today,
    }
    return render(request, template, context)


class AttendanceUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Attendance
    template_name = "booking/attendance_update.html"
    form_class = AttendanceUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter
        attendance_filter = AttendanceFilter(
            self.request.GET,
            queryset=(
                Attendance.objects.all()
                .select_related("book", "book__user", "book__event", "book__price")
                .prefetch_related("book__times")
            ),
        )

        # Paginator
        paginator = Paginator(attendance_filter.qs, 20)
        page = self.request.GET.get("page")
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        context["page_obj"] = response
        context["filter"] = self.request.GET
        context["attendance_filter"] = attendance_filter
        return context

    def get_success_url(self, **kwargs):
        pk = self.object.id
        url = build_url(
            "attendance_update",
            get=self.request.GET.items(),
            pk={"pk": pk},
        )
        return url

    def test_func(self):
        return staff_check(self.request.user)


@login_required
@user_passes_test(staff_check)
def contactlistview(request):
    template = "booking/contact_list.html"
    booking_filter = BookFilter(
        request.GET,
        queryset=(
            Book.objects.all().select_related("event", "user", "price").prefetch_related("times").order_by("-booked_at")
        ),
    )

    # Pagination
    paginator = Paginator(booking_filter.qs, 30)  # Show 24 contacts per page.
    page = request.GET.get("page")

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    # End Paginator

    context = {
        "book_filter": booking_filter,
        "filter": request.GET,
        "page_obj": response,
    }

    return render(request, template, context)


@login_required
@user_passes_test(staff_check)
def quotationlistview(request):
    template = "booking/quotation_list.html"
    quotation_filter = QuotationFilter(
        request.GET,
        queryset=(
            Quotation.objects.all()
            .select_related("event", "time_location__location")
            .prefetch_related("teachers", "direct_costs", "time_location__time_options")
            .order_by("-id")
        ),
    )

    # Pagination
    paginator = Paginator(quotation_filter.qs, 24)  # Show 25 contacts per page.
    page = request.GET.get("page")
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    context = {
        "quotation_filter": quotation_filter,
        "page_obj": response,
    }
    return render(request, template, context)


class QuotationUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Quotation
    template_name = "booking/quotation_update.html"
    form_class = QuotationCreateForm

    def dispatch(self, request, *args, **kwargs):
        # TODO: Not sure if this makes two queries
        self.object = self.get_object()

        if self.object.locked:
            messages.add_message(
                self.request,
                messages.WARNING,
                _("Quotation is Locked"),
            )
            return redirect("quotation_list")

        return super(QuotationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_quotation_bookings(self):
        """
        Gets all the booings with same Event, Location and Time Option
        """
        time_location_of_quotation = TimeLocation.objects.get(id=self.object.time_location.id)
        time_options_id_list = [to.id for to in time_location_of_quotation.time_options.all()]
        filtered_list = Book.objects.filter(
            event=self.object.event.id,
            event__time_locations=self.object.time_location.id,
            times__in=time_options_id_list,
        ).select_related("event__level", "user", "price", "attendance")
        return filtered_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtered_list"] = self.get_quotation_bookings()
        return context

    def get_initial(self):
        """
        Respect the Previous Fix and Rent but update initial Profits
        Manual change of profit should just happen in the Lock view
        """
        # Revenue
        books_participants = self.get_quotation_bookings().filter(status="PA")
        summe = Decimal(0)

        # TODO: Apply condition in DataBase and aggregate the sum there
        #     direct_revenue = books_participants.aggregate(Sum("price__price_chf"))
        #     direct_revenue = direct_revenue["price__price_chf__sum"]

        for book in books_participants:
            if book.price.cycles < 2:
                summe += book.price.price_chf
            elif book.price.cycles > 1:
                summe += book.price.price_chf / book.price.cycles

        if not books_participants:
            direct_revenue = Decimal(0)
        else:
            direct_revenue = summe

        # Recalculate Profits
        ADMIN_RATE = Decimal(0.25)
        PARTNER_RATE = Decimal(0.75)

        # Calculate Profits
        profit = direct_revenue - self.object.related_rent - self.object.fix_profit
        admin_profit = round(profit * ADMIN_RATE, 2)
        partner_profit = round(profit * PARTNER_RATE, 2)

        initial = {"direct_revenue": direct_revenue, "admin_profit": admin_profit, "partner_profit": partner_profit}

        return initial

    def get_success_url(self, **kwargs):
        success_url = build_url("quotation_list")
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Quotation update"),
        )
        return success_url

    def test_func(self):
        return staff_check(self.request.user)


@login_required
@user_passes_test(staff_check)
def quotationcreateview(request):
    template = "booking/quotation_filter.html"
    form = QuotationCreateForm

    # Filters
    book_filter = QuotationBookFilter(
        request.GET,
        queryset=(
            Book.objects.all().select_related("event__level", "user", "price").prefetch_related("invoice", "attendance")
        ),
    )

    if request.method == "GET":
        # Want to catch the different errors so split
        if "event" and "event__time_locations" in request.GET:
            if request.GET.get("event") != "" and request.GET.get("event__time_locations") != "":

                event_id = str(request.GET.get("event"))
                filter_time_location_id = str(request.GET.get("event__time_locations"))

                event = event_get(event_id)
                event_time_locations = event.time_locations.all()
                filter_time_location = timelocation_get(filter_time_location_id)

                # If the filtered TL is in the TLS of the Event
                if filter_time_location in event_time_locations:
                    # Get other template
                    template = "booking/quotation_create.html"

                    FIX_PROFIT = Decimal(100.00)
                    ADMIN_RATE = Decimal(0.25)
                    PARTNER_RATE = Decimal(0.75)

                    # Variables

                    # Revenue
                    books_participants = book_filter.qs.filter(status="PA").select_related("event__level")
                    summe = Decimal(0)

                    for book in books_participants:
                        if book.price.cycles < 2:
                            summe += book.price.price_chf
                        elif book.price.cycles > 1:
                            summe += book.price.price_chf / book.price.cycles

                    if not books_participants:
                        direct_revenue = Decimal(0)
                    else:
                        direct_revenue = summe

                    # Rent
                    # TODO: Get rent based on place
                    related_rent = Decimal(240.00)

                    # Calculate Profits
                    profit = direct_revenue - related_rent - FIX_PROFIT
                    admin_profit = round(profit * ADMIN_RATE, 2)
                    partner_profit = round(profit * PARTNER_RATE, 2)

                    # Select Initial

                    # Teachers
                    try:
                        teachers = [t.id for t in event.teachers.all()]
                    except AttributeError:
                        teachers = [""]

                    form = form(
                        initial={
                            "event": event_id,
                            "time_location": filter_time_location_id,
                            "teachers": teachers,
                            "related_rent": related_rent,
                            "direct_revenue": direct_revenue,
                            "related_rent": related_rent,
                            "fix_profit": FIX_PROFIT,
                            "admin_profit": admin_profit,
                            "partner_profit": partner_profit,
                        },
                        auto_id=False,
                    )
                else:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        _("Event " + str(event) + " doesn't have Time Location " + str(filter_time_location_id)),
                    )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    _("Missing Event or Time Location"),
                )
        else:
            # TODO: maybe
            pass

    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            participants = book_filter.qs.filter(status="PA").count()
            try:
                create_quotation(form, count=participants)
            except Exception as e:
                messages.add_message(request, messages.WARNING, _("Error: " + str(e)))

            return redirect("quotation_list")

    # Context
    context = {
        "book_filter": book_filter,
        "filtered_list": book_filter.qs,
        "form": form,
    }

    return render(request, template, context)


@login_required
@user_passes_test(staff_check)
def quotationlockview(request, pk):
    template = "booking/quotation_lock.html"
    queryset = Quotation.objects.get(pk=pk)
    form = QuotationLockForm(request.POST or None, instance=queryset)

    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.locked = True
            obj.locked_at = datetime.datetime.now()
            obj.save()
            return redirect("quotation_list")

    context = {
        "form": form,
    }
    return render(request, template, context)


@login_required
@user_passes_test(herd_check)
def invitationsendview(request):
    template = "booking/invitation_create.html"
    form = InvitationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            Invitation = get_invitation_model()
            email = form.cleaned_data["email"]
            invite = Invitation.create(email, inviter=request.user)
            try:
                invite.send_invitation(request)
            except Exception as e:
                messages.add_message(request, messages.INFO, _("Error: " + e))
            else:
                messages.add_message(request, messages.INFO, _("Email sent to: " + email + " . We'll be in touch!"))
            return redirect("teacher_attendance")

    context = {
        "form": form,
    }
    return render(request, template, context)


class HerdView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "booking/herd.html"
    login_url = "/accounts/login/"

    def test_func(self):
        return herd_check(self.request.user)
