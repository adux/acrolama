from django.contrib import messages

from django.views.generic import TemplateView, UpdateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Book
from .filters import BookFilter
from .forms import UpdateForm, CreateForm
from .utils import build_url

from project.models import Event

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

    def form_valid(self, form):
        instance = form.save(commit=False)

        if 'update' in self.request.POST:
            instance.save()
        elif 'create' in self.request.POST:
            instance.pk = None
            instance.id = None
            old_event = instance.event
            event = Event.objects.filter(
                level=old_event.level).filter(category=old_event.category)
            print(event)

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
        messages.success(self.request, 'Update successful.')
        return url

    def test_func(self):
        return staff_check(self.request.user)


class ControlCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Book
    template_name = "booking/control_create.html"
    form_class = CreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = Book.objects.all()
        context["book_list"] = bookings.order_by("event")
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
