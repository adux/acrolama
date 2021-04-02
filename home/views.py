import datetime
from collections import defaultdict

from django.utils import timezone
from django.utils.decorators import classonlymethod
from django.shortcuts import render, redirect

from django.views.generic import DetailView, ListView, TemplateView
from django.views.decorators import gzip

from home.multiforms import MultiFormsView

from home.models import (
    AboutTeam,
    AboutImage,
    AboutDate,
    Faq,
    Info,
    Testimonial,
    Portfolio,
    NewsList,
)

from booking.models import Book
from project.models import Event
from users.models import User

from accounting.forms import CreditnotedateForm


class ProfileView(TemplateView):
    template_name = "home/profile.html"

    def dispatch(self, request, *args, **kwargs):
        # TODO: Change this to something more significant like account sign up
        if request.user.id is None:
            return redirect("home")

        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    # If logged in
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)
        context["user"] = user

        books = Book.objects.filter(user=user)[:5]
        forms = []
        for book in books:
            if hasattr(book, 'attendance'):
                form = CreditnotedateForm(book.attendance)
                print(form.__dict__)

            else:
                forms.append(None)

        context["books"] = books
        context["forms"] = forms

        return context


class HomeFormView(MultiFormsView):
    template_name = "home/home.html"
    gzip_page = False
    form_classes = {
        # "news": NewsForm,
    }
    success_urls = {
        # "news": reverse_lazy("home"),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about_content"] = AboutTeam.objects.all().select_related("team__avatar")
        context["about_image"] = AboutImage.objects.all().select_related("image")
        context["about_date"] = AboutDate.objects.all()
        context["testimonial"] = Testimonial.objects.all()
        context["portfolio"] = Portfolio.objects.all()[0:8].select_related("image")
        context["news"] = NewsList.objects.all().select_related("event__level", "event__discipline")

        # Events
        # All the events that haven't finished.
        event_main = (
            Event.objects.filter(event_enddate__gte=timezone.now())
            .exclude(published=False)
            .order_by("event_startdate", "level", "title")
            .select_related("level", "discipline")
            .prefetch_related("time_locations__time_option")
            .prefetch_related("time_locations__location__address")
        )

        context["event"] = (
            event_main.exclude(category="CY")
            .distinct()[:6]
        )

        # Classes
        classes = (
            event_main.filter(category="CY")
            .distinct()
        )

        context["next"] = classes.filter(
            event_startdate__gte=(timezone.now()),
            event_startdate__lte=(timezone.now() + datetime.timedelta(days=60))
        )

        current = classes.filter(
            event_startdate__lte=timezone.now(),
        )

        #  Note: Could do aux func/methode out of this.
        d = defaultdict(list, {k: [] for k in ('Monday', 'Tuesday', 'Wednesday', 'Friday', 'Sunday')})
        for cycle in current:
            days = cycle.get_regular_days_list()
            for day in days:
                d[day].append(cycle)

        context["current"] = dict(d)

        return context

    @classonlymethod
    def as_view(cls, **kwargs):
        """
        Optionally decorates the base view with
        django.views.decorators.gzip.gzip_page().
        """
        view = super(HomeFormView, cls).as_view(**kwargs)
        return gzip.gzip_page(view) if cls.gzip_page else view


def faqview(request):
    qs_faq = Faq.objects.all()
    template_name = "home/faq.html"
    context = {"faq": qs_faq}
    return render(request, template_name, context)


class InfoDetailView(DetailView):
    model = Info
    context_object_name = "info"


class EventListView(ListView):
    model = Event
    template_name = "home/event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list"] = (
            Event.objects.order_by("event_startdate")
            .exclude(category="CY")
            .exclude(published=False)
            .filter(event_enddate__gte=timezone.now())
        )
        return context


class ClassListView(ListView):
    model = Event
    template_name = "home/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list"] = (
            Event.objects.order_by("event_startdate")
            .filter(category="CY")
            .filter(event_enddate__gte=timezone.now())
            .exclude(published=False)
        )
        return context
