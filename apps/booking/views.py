import datetime

from django.conf import settings

# from django.contrib.postgres.fields import ArrayField
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.urls import reverse

from django.core.mail import send_mail

from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    FormView,
)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Render for email template
from django.template.loader import render_to_string

# Allows querries with OR statments
# from django.db.models import Q

from booking.models import Book, Attendance
from booking.filters import BookFilter, AttendanceFilter, AttendanceDailyFilter
from booking.forms import UpdateBookForm, CreateBookForm, UpdateAttendanceForm
from booking.utils import (
    build_url,
    email_sender,
    datelistgenerator,
    teacher_check,
    staff_check,
    herd_check,
)

from booking.services import (
    get_book,
    createNextBook,
    createInvoiceFromBook,
    createAttendance,
    createNextBookAttendance,
    updateSwitchCheckAttendance,
)

from project.models import Event, Irregularity

@login_required
@user_passes_test(staff_check)
def bookinglistview(request):
    template = "booking/booking_list.html"
    booking_filter = BookFilter(
        request.GET,
        queryset=(
            Book.objects.all()
            .select_related("event")
            .select_related("user")
            .select_related("price")
            .prefetch_related("times")
            .prefetch_related("times__regular_days")
            .order_by("-booked_at")
        ),
    )

    # Pagination
    paginator = Paginator(booking_filter.qs, 20)  # Show 25 contacts per page.
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

    if request.method == "POST":
        checked_list = request.POST.getlist("check")
        if "create" in request.POST:
            for pk in checked_list:
                book = get_book(pk)
                if book.price.abonament & (book.price.cycles == 1):
                    try:
                        new_book = createNextBook(book, "PE")
                    except:
                        messages.add_message(
                            request,
                            messages.WARNING,
                            _(
                                "Book N°"
                                + str(book.id)
                                + ": Doesn't seem to have a next Event"
                            ),
                        )
                    else:
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            _("Book N°" + str(new_book.id) + ": Book Created"),
                        )
                elif book.price.abonament & (book.price.cycles > 1):
                    messages.add_message(
                        request,
                        messages.INFO,
                        _(
                            "Book N°"
                            + str(book.id)
                            + ": Abo for more then 1 Cycle. Next are created after payment"
                        ),
                    )
                else:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        _("Book N°" + str(book.id) + ": Not a Abo, not posible to determine next Event."),
                    )
    return render(request, template, context)


class BookUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Book
    template_name = "booking/booking_update.html"
    form_class = UpdateBookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_filter = BookFilter(
            self.request.GET,
            queryset=(
                Book.objects.all()
                .select_related("event")
                .select_related("user")
                .select_related("price")
                .prefetch_related("times")
                .prefetch_related("times__regular_days")
                .order_by("-booked_at")
            ),
        )
        # related_invoice = Invoice.objects.get(
        context["book_filter"] = booking_filter
        paginator = Paginator(
            booking_filter.qs, 20
        )  # Show 25 contacts per page.
        page = self.request.GET.get("page")
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)
        context["page_obj"] = response
        context["filter"] = self.request.GET
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        book = get_book(instance.id)

        if "update" in self.request.POST:
            if (book.status == "PE") and (instance.status == "IN"):
                try:
                    email_sender(instance, "Informed")
                except:
                    messages.add_message(
                        self.request, messages.WARNING, _("Error Email")
                    )
                else:
                    messages.add_message(
                        self.request, messages.INFO, _("Informed email sent.")
                    )
                try:
                    createAttendance(instance)
                except:
                    messages.add_message(
                        self.request,
                        messages.WARNING,
                        _("Error creating Attendance"),
                    )
                else:
                    messages.add_message(
                        self.request, messages.INFO, _("Attendance created")
                    )
                try:
                    createInvoiceFromBook(instance)
                except:
                    messages.add_message(
                        self.request,
                        messages.WARNING,
                        _("Error creating Invoice"),
                    )
                else:
                    messages.add_message(
                        self.request, messages.INFO, _("Invoice Created")
                    )
            elif (book.status == "IN") and (instance.status == "PA"):
                messages.add_message(
                    self.request,
                    messages.INFO,
                    _("Please change to participant only if Invoice payed."),
                )
            instance.save()
        elif "create" in self.request.POST:
            try:
                book = createNextBook(instance, "PE")
            except UnboundLocalError:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _(
                        "Book N°"
                        + str(book.id)
                        + ": Doesn't seem to have a next Event"
                    ),
                )
            else:
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    _("Book N°" + str(book.id) + ": Book Created"),
                )
        return super().form_valid(form)

    # TODO: There is probably a way to get all the GETs and process them?
    def get_success_url(self, **kwargs):
        user = self.request.GET.get("user", "")
        event = self.request.GET.get("event", "")
        status = self.request.GET.get("status", "")
        start_date = self.request.GET.get("start_date", "")
        end_date = self.request.GET.get("end_date", "")
        pk = self.object.id
        url = build_url(
            "booking_update",
            get={"user": user, "event": event, "status": status, "start_date": start_date, "end_date": end_date},
            # TODO im not sure this way of passing the pk is ideal :)
            pk={"pk": pk},
        )
        return url

    def test_func(self):
        return staff_check(self.request.user)


class BookCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Book
    template_name = "booking/booking_create.html"
    form_class = CreateBookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_filter"] = BookFilter(
            self.request.GET,
            queryset=(
                Book.objects.all()
                .select_related("event")
                .select_related("user")
                .select_related("price")
                .prefetch_related("times")
                .prefetch_related("times__regular_days")
                .order_by("-booked_at")
            ),
        )
        return context

    def test_func(self):
        return staff_check(self.request.user)


@login_required
@user_passes_test(staff_check)
def attendancelistview(request):
    template = "booking/attendance_list.html"
    attendance_filter = AttendanceFilter(
        request.GET,
        queryset=(
            Attendance.objects.all()
            .select_related("book")
            .select_related("book__event")
            .select_related("book__user")
            .select_related("book__price")
            .prefetch_related("book__times")
            .prefetch_related("book__times__regular_days")
        ),
    )

    # Pagination
    paginator = Paginator(
        attendance_filter.qs, 20
    )  # Show 25 contacts per page.
    page = request.GET.get("page")
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)

    # End Paginator

    context = {
        "attendance_filter": attendance_filter,
        "filter": request.GET,
        "page_obj": response,
    }

    if request.method == "POST":
        checked_list = request.POST.getlist("check")
        if "create" in request.POST:
            pass
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
                    #Prepare de data
                    values_split = values.split(" ")
                    attendance_id = values_split[0]
                    check_pos = values_split[1]
                    #Make the actual Switch
                    updateSwitchCheckAttendance(attendance_id, int(check_pos))
                    #Send a message
                    messages.add_message(request, messages.SUCCESS, _("Updated attendance id: " + str(attendance_id)))
            except:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _("Make a manual list and report the error please."),
                )
            else:
                success_url = build_url(
                    "teacher_attendance",
                    get={
                        "book__event": request.POST.get("filtered_event", ""),
                        "attendance_date": request.POST.get("filtered_date"),
                    },
                )
                print(success_url)
                return HttpResponseRedirect(success_url)


    attendance_filter = AttendanceDailyFilter(
        request.GET,
        queryset=(
            Attendance.objects.filter(book__event__teacher=request.user)
            .select_related("book")
            .select_related("book__event")
            .select_related("book__user")
            .select_related("book__price")
            .prefetch_related("book__times")
            .prefetch_related("book__times__regular_days")
        ),
        user=request.user,
    )

    if not request.GET.get('attendance_date'):
        initial_date = str(datetime.datetime.now().date())
    else:
        initial_date = request.GET.get('attendance_date')

    context = {
        "attendance_filter": attendance_filter,
        "attendance_list": attendance_filter.qs,
        "filtered_date": datetime.date.fromisoformat(initial_date),
        "date_today": datetime.datetime.now().date(),
    }
    return render(request, template, context)


class AttendanceUpdateView(
    UserPassesTestMixin, LoginRequiredMixin, UpdateView
):
    model = Attendance
    template_name = "booking/attendance_update.html"
    form_class = UpdateAttendanceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendance_filter = AttendanceFilter(
            self.request.GET,
            queryset=(
                Attendance.objects.all()
                .select_related("book")
                .select_related("book__event")
                .select_related("book__user")
                .select_related("book__price")
                .prefetch_related("book__times")
                .prefetch_related("book__times__regular_days")
            ),
        )

        context["attendance_filter"] = attendance_filter
        paginator = Paginator(
            attendance_filter.qs, 20
        )  # Show 25 contacts per page.
        page = self.request.GET.get("page")
        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)
        context["page_obj"] = response
        context["filter"] = self.request.GET
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)

        if "update" in self.request.POST:
            instance.save()
        return super().form_valid(form)

    # TODO: There is probably a way to get all the GETs and process them all at ones.
    def get_success_url(self, **kwargs):
        user = self.request.GET.get("book__user", "")
        event = self.request.GET.get("book__event", "")
        attendance_date = self.request.GET.get("attendance_date", "")
        pk = self.object.id
        url = build_url(
            "attendance_update",
            get={
                "book__user": user,
                "book__event": event,
                "attendance_date": attendance_date,
            },
            pk={"pk": pk},
        )
        return url

    def test_func(self):
        return staff_check(self.request.user)


class HerdView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "booking/herd.html"

    def test_func(self):
        return herd_check(self.request.user)
