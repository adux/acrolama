# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import ListView

from .models import Book

# TODO: add to utils


def staff_check(user):
    return user.is_staff


# @method_decorator(login_required, name='dispatch')
# @user_passes_test(staff_check)
class ControlListView(ListView):
    model = Book
    template_name = "booking/control_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list"] = (
            Book.objects.order_by("event")
        )
        return context


class TeacherListView(ListView):
    model = Book
    template_name = "booking/teacher_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list"] = (
            Book.objects.order_by("event")
        )
        return context


def herdview(request):
    template_name = "booking/herd.html"
    return render(request, template_name)
