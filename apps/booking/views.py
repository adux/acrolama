from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Book
from .filters import BookFilter
from .forms import UpdateForm
from .utils import build_url


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
        bookings = Book.objects.all()
        context["book_list"] = bookings.order_by("event")
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
        bookings = Book.objects.all()
        context["book_list"] = bookings.order_by("event")
        context["book_filter"] = BookFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

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
