import datetime

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _

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

from .models import Book, Attendance
from .filters import BookFilter, AttendanceFilter
from .forms import UpdateForm, CreateForm # AttendanceDailyForm
from .utils import build_url, email_sender, datelistgenerator
from .services import (
    createAttendance,
    updateSwitchCheckAttendance,
    createAmountBookingAttendance,
)

from project.models import Event, Irregularity

# Tests for the UserPassesTestMixin
def staff_check(user):
    return user.is_staff


def teacher_check(user):
    return user.is_teacher


# General Update view
class ControlListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Book
    template_name = "booking/control_list.html"
    ordering = ["event"]

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
            ),
        )
        context["filter"] = self.request.GET
        return context

    def test_func(self):
        return staff_check(self.request.user)


class ControlUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Book
    template_name = "booking/control_update.html"
    form_class = UpdateForm

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
            ),
        )
        return context

    def form_valid(self, form):
        """
        Separetes logic depending on which action button was pressed.
        """
        instance = form.save(commit=False)
        if "update" in self.request.POST:
            """
            Separate action depending on previous to recent status
            """
            pre_save_obj = Book.objects.get(pk=instance.pk)
            if (pre_save_obj.status == "PE") and (instance.status == "IN"):
                try:
                    email_sender(instance, "Informed")
                except:
                    messages.add_message(
                        self.request, messages.ERROR, _("Error Email")
                    )
                else:
                    messages.add_message(
                        self.request, messages.INFO, _("Informed email sent.")
                    )
            elif (pre_save_obj.status == "IN") and (instance.status == "PA"):
                if instance.price.cycles == 1:
                    try:
                        instance.save()
                        createAttendance(instance)
                    except:
                        messages.add_message(
                            self.request, messages.ERROR, _("Error Attendance")
                        )
                    else:
                        messages.add_message(
                            self.request,
                            messages.INFO,
                            _("Assitance created."),
                        )
                elif instance.price.cycles > 1:
                    #  This are Cycles, Events dont have prices of amount > 1
                    try:
                        instance.save()
                        createAttendance(instance)
                        print("Create Booking")
                        createAmountBookingAttendance(
                            instance, "PA", instance.price.cycles
                        )
                    except:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            _("Error Create Book")
                        )
                    else:
                        messages.add_message(
                            self.request, messages.INFO, _("Booking Created")
                        )
            else:
                messages.success(self.request, "Update successful.")
        elif "create" in self.request.POST:
            instance.pk = None
            instance.id = None
            instance.status = "PE"
            if instance.event.category == "fas fa-cogs":
                old_event = instance.event
                try:
                    event = Event.objects.filter(
                        level=old_event.level,
                        category=old_event.category,
                        event_startdate__gt=old_event.event_enddate,
                    ).get(cycle=old_event.cycle + 1)
                    instance.event = event
                    messages.success(
                        self.request, "Booking for next cycle was created."
                    )
                except Event.DoesNotExist:
                    messages.warning(
                        self.request,
                        "Next Cycle does not exist. Duplicate Created",
                    )
            else:
                messages.success(
                    self.request, "Booking of same event was duplicated."
                )
        return super().form_valid(form)

    # TODO: There is probably a way to get all the GETs and process them?
    def get_success_url(self, **kwargs):
        user = self.request.GET.get("user", "")
        event = self.request.GET.get("event", "")
        status = self.request.GET.get("status", "")
        pk = self.object.id
        url = build_url(
            "control_update",
            get={"user": user, "event": event, "status": status},
            # TODO im not sure this way of passing the pk is ideal :)
            pk={"pk": pk},
        )
        return url

    def test_func(self):
        return staff_check(self.request.user)


class ControlCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Book
    template_name = "booking/control_create.html"
    form_class = CreateForm

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
            ),
        )
        return context

    def test_func(self):
        return staff_check(self.request.user)


#TEst for teachers only
def attendance_daily_view(request):
    template = "booking/attendance_list_daily.html"
    attendance_today_list = Attendance.objects.filter(
        attendance_date__contains=[datetime.datetime.now().date()]
    )

    context = {'attendance_list' : attendance_today_list}

    if request.method == 'POST':
        check_list= request.POST.getlist('check')
        try:
            for values in check_list:
                values_split = values.split(' ')
                attendance_id = values_split[0]
                check_pos = values_split[1]
                #Check that booking exists
                if attendance_today_list.filter(id=attendance_id).exists():
                    attendance = attendance_today_list.get(id=attendance_id)
                    # And checking is false
                    # if not attendance.attendance_check[int(check_pos)]:
                    updateSwitchCheckAttendance(attendance_id, int(check_pos))

            messages.add_message(
                request, messages.SUCCESS, _("List Updated")
            )
        except:
            messages.add_message(
                request, messages.ERROR, _("Make a manual list and report the error please.")
            )

    return render(request, template, context)


class AttendanceMainListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "booking/attendance_list_main.html"

    def post(self, request, *args, **kwargs):
        pk_list = request.POST.getlist('edit')
        print(pk_list)
        return request

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attendance_filter"] = AsstianceFilter(
            self.request.GET,
            queryset=(
                Assitance.objects.all()
                .select_related("book")
            ),
        )
        return context

    def test_func(self):
        return staff_check(self.request.user)


class AttendanceListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "booking/attendance_list.html"

    def post(self, request, *args, **kwargs):
        pk_list = request.POST.getlist('edit')
        print(pk_list)
        return request

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attendance_list"] = Attendance.objects.filter(
            attendance_date__contains=[datetime.datetime.now().date()]
        )
        return context

    def test_func(self):
        return staff_check(self.request.user)


class HerdView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "booking/herd.html"

    def test_func(self):
        return staff_check(self.request.user)
