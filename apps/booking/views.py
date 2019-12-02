from django.conf import settings

from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.core.mail import send_mail

from django.views.generic import (
    TemplateView,
    UpdateView,
    ListView,
    CreateView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

# Render for email template
from django.template.loader import render_to_string

# Allows querries with OR statments
# from django.db.models import Q

from .models import Book
from .filters import BookFilter
from .forms import UpdateForm, CreateForm
from .utils import build_url

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
            self.request.GET, queryset=self.get_queryset()
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
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        """
        Separetes logic based on which action button was pressed and generates
        logic based on it TODO:maybe a state machines makes more sense
        """
        if "update" in self.request.POST:
            # I think i needed this for if they book, since then the pk doesn't have
            # and id. Maybe in views its not so. TODO: check
            # if instance.pk:
            """
            Taken from
            https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
            Theres another Method with Multi wich helps for headers if needed
            """
            pre_save_object = Book.objects.get(pk=instance.pk)
            if (pre_save_object.status == "PE") and (instance.status == "IN"):
                subject = "Acrolama - Confirmation - " + str(instance.event)
                sender = "notmonkeys@acrolama.com"
                to = [instance.user.email, "acrolama@acrolama.com"]
                irregularities = Irregularity.objects.filter(
                    event__slug=instance.event.slug
                )

                p = {
                    "event": instance.event,
                    "user": instance.user,
                    "price": instance.price,
                    "times": instance.times.all(),
                    "irregularities": irregularities,
                }

                msg_plain = render_to_string(
                    settings.BASE_DIR
                    + "/apps/booking/templates/booking/email_informed.txt",
                    p,
                )
                msg_html = render_to_string(
                    settings.BASE_DIR
                    + "/apps/booking/templates/booking/email_informed.html",
                    p,
                )

                send_mail(subject, msg_plain, sender, to, html_message=msg_html)
                messages.success(self.request, "Update successful. Email Sent.")
            else:
                messages.success(self.request, "Update successful.")

        elif "create" in self.request.POST:
            instance.pk = None
            instance.id = None
            instance.status = 'PE'
            if instance.event.category == 'fas fa-cogs':
                old_event = instance.event
                try:
                    event = (
                        Event.objects.filter(
                            level=old_event.level,
                            category=old_event.category,
                            event_startdate__gt=old_event.event_enddate
                        ).get(cycle=old_event.cycle + 1)
                    )
                    instance.event = event
                    messages.success(
                        self.request,
                        "Booking for next cycle was created."
                    )
                except Event.DoesNotExist:
                    messages.warning(
                        self.request,
                        "Next Cycle does not exist. Duplicate Created"
                    )
            else:
                messages.success(self.request, "Booking of same event was duplicated.")
        instance.save()
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
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    # # TODO: There is probably a way to get all the GETs and process them?
    # def get_success_url(self, **kwargs):
    #     user = self.request.GET.get("user", "")
    #     event = self.request.GET.get("event", "")
    #     status = self.request.GET.get("status", "")
    #     pk = self.object.id
    #     url = build_url(
    #         "control_update",
    #         get={"user": user, "event": event, "status": status},
    #         # TODO im not sure this way of passing the pk is ideal :)
    #         pk={"pk": pk},
    #     )
    #     messages.success(self.request, 'Update successful.')
    #     return url

    def test_func(self):
        return staff_check(self.request.user)


class TeacherListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Book
    template_name = "booking/teacher_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_list"] = Book.objects.order_by("event")
        return context

    def test_func(self):
        return teacher_check(self.request.user)


class HerdView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "booking/herd.html"

    def test_func(self):
        return staff_check(self.request.user)
