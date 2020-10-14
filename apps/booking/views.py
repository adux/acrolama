import datetime

from decimal import Decimal

# External apps
from dal import autocomplete
from invitations.utils import get_invitation_model

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, Q  # Queries with OR
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect

# Views
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Models
from users.models import User
from booking.models import Book, Attendance, Quotation
from project.models import Event, TimeLocation

# Filters
from booking.filters import (
    AttendanceFilter,
    AttendanceDailyFilter,
    BookFilter,
    EventFilter,
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
    check_abocounter,
    create_next_book,
    create_quotation,
    get_book,
    get_event,
    get_timelocation,
    inform_book,
    update_lastbook_abocounter,
    switch_check_attendance,
)


class EventAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return Event.objects.none()

        qs = Event.objects.all().order_by("-event_startdate", "level").select_related("level")

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

        qs = Event.objects.all().order_by("-event_startdate").select_related("level").filter(teachers=self.request.user)

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


class TimeLocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not herd_check(self.request.user):
            return TimeLocation.objects.none()

        qs = TimeLocation.objects.all().order_by("name", "location").select_related("location")

        if self.q:
            qs = qs.filter(
                Q(location__icontains=self.q) | Q(time_options__icontains=self.q) | Q(name__icontains=self.q)
            )

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
        "page_obj": response,
    }

    # Logic

    if request.method == "POST":
        checked_list = request.POST.getlist("check")
        if "create" in request.POST:
            for pk in checked_list:
                book = get_book(pk)

                # Create the next book
                if book.status == "PA":
                    try:
                        new_book = create_next_book(book, "PE")

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
                            request, messages.SUCCESS, _("Book N°" + str(new_book.id) + ": Book Created"),
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

        booking_filter = BookFilter(
            self.request.GET,
            queryset=(
                Book.objects.all()
                .select_related("event", "user", "price")
                .prefetch_related("times")
                .order_by("-booked_at")
            ),
        )

        # Paginator
        paginator = Paginator(booking_filter.qs, 24)  # Show 24 contacts per page.
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
        context["book_filter"] = booking_filter

        return context

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Get the book before save
        book = get_book(instance.id)

        if "update" in self.request.POST:
            if (book.status in ("PE", "WL")) and (instance.status == "IN"):
                inform_book(self.request, instance, book)

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
            self.request, messages.SUCCESS, _("Book created, we'll get back to you soon!"),
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
    paginator = Paginator(attendance_filter.qs, 20)  # Show 25 contacts per page.
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
                    switch_check_attendance(attendance_id, int(check_pos))
                    # Send a message
                    messages.add_message(
                        request, messages.SUCCESS, _("Updated attendance id: " + str(attendance_id)),
                    )
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR, _("Make a manual list and report the error: " + e),
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
            .select_related("book", "book__user", "book__event", "book__price")
            .prefetch_related("book__times")
        ),
        user=request.user,
    )

    if not request.GET.get("attendance_date"):
        initial_date = str(datetime.datetime.now().date())
    else:
        initial_date = request.GET.get("attendance_date")

    context = {
        "attendance_filter": attendance_filter,
        "attendance_list": attendance_filter.qs,
        "filtered_date": datetime.date.fromisoformat(initial_date),
        "date_today": datetime.datetime.now().date(),
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
            Book.objects.all()
            .select_related("event", "user", "price")
            .prefetch_related("times")
            .order_by("-booked_at")
        ),
    )

    # Pagination
    paginator = Paginator(booking_filter.qs, 24)  # Show 24 contacts per page.
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
def eventlistview(request):
    template = "booking/event_list.html"
    event_filter = EventFilter(
        request.GET,
        queryset=(
            Event.objects.all()
            .select_related("project", "policy", "discipline", "level")
            .prefetch_related("time_locations__time_options")
            .order_by("-event_startdate")
        ),
    )

    # Pagination
    paginator = Paginator(event_filter.qs, 24)  # Show 24 contacts per page.
    page = request.GET.get("page")

    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    # End Paginator

    context = {
        "event_filter": event_filter,
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
                self.request, messages.WARNING, _("Quotation is Locked"),
            )
            return redirect('quotation_list')

        return super(QuotationUpdateView, self).dispatch(request, *args, **kwargs)

    def get_checked_bookings(self):
        tl = TimeLocation.objects.get(id=self.object.time_location.id)
        to_ids = [to.id for to in tl.time_options.all()]
        filtered_list = Book.objects.filter(
            event=self.object.event.id,
            event__time_locations=self.object.time_location.id,
            times__in=to_ids
        ).select_related("user", "price", "attendance")
        return filtered_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtered_list'] = self.get_checked_bookings()
        return context

    def get_initial(self):
        # Revenue
        filtered_list = self.get_checked_bookings().filter(status='PA')
        booksparticipants = filtered_list

        if not booksparticipants:
            direct_revenue = Decimal(0)
        else:
            direct_revenue = booksparticipants.aggregate(Sum("price__price_chf"))
            direct_revenue = direct_revenue["price__price_chf__sum"]

        return {"direct_revenue": direct_revenue}

    def get_success_url(self, **kwargs):
        success_url = build_url("quotation_list")
        messages.add_message(
            self.request, messages.SUCCESS, _("Quotation update"),
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
            Book.objects.all()
            .select_related("event__level", "user", "price")
            .prefetch_related("invoice", "attendance")
        ),
    )

    if request.method == "GET":
        # Want to catch the different errors so split
        if "event" and "event__time_locations" in request.GET:
            if request.GET.get("event") != "" and request.GET.get("event__time_locations") != "":
                eventid = str(request.GET.get("event"))
                timelocationid = str(request.GET.get("event__time_locations"))
                event = get_event(eventid)
                tls = event.time_locations.all()
                tl = get_timelocation(timelocationid)
                # If the filtered TL is in the TLS of the Event
                if tl in tls:
                    # Get other template
                    template = "booking/quotation_create.html"

                    FIX_PROFIT = Decimal(100.00)
                    ADMIN_RATE = Decimal(0.25)
                    PARTNER_RATE = Decimal(0.75)

                    # Variables

                    # Revenue
                    booksparticipants = book_filter.qs.filter(status="PA").select_related("event__level")
                    summe = Decimal(0)
                    for b in booksparticipants:
                        if b.price.cycles <= 1:
                            summe += b.price.price_chf
                        elif b.price.cycles > 1:
                            summe += (b.price.price_chf/b.price.cycles)

                    if not booksparticipants:
                        direct_revenue = Decimal(0)
                    else:
                        direct_revenue = summe

                    # Rent
                    # TODO: Get rent based on place
                    related_rent = Decimal(240.00)

                    # Calc
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
                            "event": eventid,
                            "time_location": timelocationid,
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
                        request, messages.WARNING, _("Event " + str(event) + " doesn't have Time Location " + str(tl)),
                    )
            else:
                messages.add_message(
                    request, messages.WARNING, _("Missing Event or Time Location"),
                )
        else:
            # TODO: maybe
            pass

    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            participants = book_filter.qs.filter(status="PA").count()
            create_quotation(form, count=participants)
            return redirect('quotation_list')

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
            return redirect('quotation_list')

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
            email = form.cleaned_data['email']
            invite = Invitation.create(email, inviter=request.user)
            try:
                invite.send_invitation(request)
            except Exception as e:
                messages.add_message(request, messages.INFO,
                                     _("Error: " + e))
            else:
                messages.add_message(request, messages.INFO,
                                     _("Email sent to: " + email + " . We'll be in touch!")
                                     )
            return redirect('teacher_attendance')

    context = {
        "form": form,
    }
    return render(request, template, context)


class HerdView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "booking/herd.html"
    login_url = "/accounts/login/"

    def test_func(self):
        return herd_check(self.request.user)
