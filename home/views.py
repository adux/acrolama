import datetime
from collections import defaultdict

from django.utils import timezone
from django.utils.decorators import classonlymethod
from django.shortcuts import render

from django.views.generic import DetailView, ListView
from django.views.decorators import gzip

from home.multiforms import MultiFormsView
from home.cacheview import CacheMixin

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

from project.models import Event


class HomeFormView(CacheMixin, MultiFormsView):
    template_name = "home/home.html"
    gzip_page = True
    form_classes = {
        # "news": NewsForm,
    }
    success_urls = {
        # "news": reverse_lazy("home"),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about_content"] = AboutTeam.objects.all()
        context["about_image"] = AboutImage.objects.all().select_related("image")
        context["about_date"] = AboutDate.objects.all()
        context["testimonial"] = Testimonial.objects.all()
        context["portfolio"] = Portfolio.objects.all()[0:8].select_related("image")
        context["news"] = NewsList.objects.all()

        # Events
        event_main = (
            Event.objects.all()
            .select_related("level", "discipline")
            .prefetch_related("time_locations__time_option")
            .prefetch_related("time_locations__location")
        )
        event = (
            event_main.filter(event_enddate__gte=timezone.now())
            .order_by("event_startdate")
            .exclude(published=False)
            .exclude(category="CY")
            .distinct()[:6]
        )
        context["event"] = event

        # Classes
        classes = (
            event_main.filter(category="CY")
            .order_by("event_startdate", "level", "title")
            .exclude(published=False)
            .distinct()
        )

        context["next"] = classes.filter(
            event_startdate__gte=(timezone.now()),
            event_startdate__lte=(timezone.now() + datetime.timedelta(days=60))
        )

        current = classes.filter(
            event_startdate__lte=timezone.now(),
            event_enddate__gte=timezone.now(),
        )

        d = defaultdict(list, {k: [] for k in ('Monday', 'Tuesday', 'Wednesday', 'Friday', 'Sunday')})
        for cycle in current:
            days = cycle.get_regular_days_list()
            for day in days:
                d[day].append(cycle)

        context["current"] = dict(d)

        # context["intermediate"] = classes.filter(Q(level="2") | Q(level="3"))
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
