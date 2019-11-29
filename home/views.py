from django.contrib import messages

from django.db.models import Q

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render

from django.views.generic import DetailView, ListView


from home.multiforms import MultiFormsView
from home.models import (
    AboutTeam,
    AboutImage,
    AboutDate,
    Faq,
    Info,
    Testimonial,
    Portfolio,
)
from home.forms import NewsForm

from project.models import Event, TimeOption


class HomeFormView(MultiFormsView):
    template_name = "home/home.html"
    form_classes = {
        "news": NewsForm,
    }
    success_urls = {
        "news": reverse_lazy("home"),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about_content"] = AboutTeam.objects.all()
        context["about_image"] = AboutImage.objects.all()
        context["about_date"] = AboutDate.objects.all()
        context["testimonial"] = Testimonial.objects.all()
        context["portfolio"] = Portfolio.objects.all()[0:8]
        context["event"] = (
            Event.objects.filter(event_enddate__gte=timezone.now())
            .order_by("event_startdate", "level", "title")
            .exclude(published=False)
            .exclude(category="fas fa-cogs")
            .distinct()[:6]
        )
        # Classes
        classes = (
            Event.objects.filter(
                event_enddate__gte=timezone.now(),
                event_startdate__lt=timezone.now() + timezone.timedelta(days=90),
                category="fas fa-cogs"
            )
            .order_by("event_startdate", "title")
            .exclude(published=False)
            .distinct()
        )
        introClasses = classes.filter(level="1")
        intermediateClasses = classes.filter(Q(level="2") | Q(level="3"))
        advancedClasses = classes.filter(level="4")

        context["intro"] = introClasses
        context["intermediate"] = intermediateClasses
        context["advanced"] = advancedClasses

        # TODO: With time solve this messs :D
        # timeoption = TimeOption.objects.filter(
        #     timelocation__event__slug=slug
        # )
        """
        to =
            {% for to in obj.time_locations.all %}
                {% for rd in to.time_options.all %}
                    {% ifchanged %}
                        {% if rd.regular_days != Null %}
                        {{ rd.regular_days|default_if_none:"" }}'S {%if rd.regular_days.count == 1 %}·{% endif %}
                        {% endif %}
                    {% endifchanged%}
                {% endfor %}
            {% endfor %}
        """
        return context

    def news_form_valid(self, form):
        instance = form.save(commit=False)
        form_name = form.cleaned_data.get("action")
        email = form.cleaned_data.get("email")
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Thanks. Please confirm your email: {email}",
        )
        instance.save()
        return HttpResponseRedirect(self.get_success_url(form_name))


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
            .exclude(category="fas fa-cogs")
            .exclude(published=False)
        )
        return context


class ClassListView(ListView):
    model = Event
    template_name = "home/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list"] = (
            Event.objects.order_by("event_startdate")
            .filter(category="fas fa-cogs")
            .exclude(published=False)
        )
        return context
